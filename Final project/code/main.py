import math
import numpy as np
import time
import cv2
import sys
import socket
from global_variables import *
from path_plan import*
from check_status import *
from others import *


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # connect the server to the robot client
host = "169.254.177.247"
port = 9999
serversocket.bind((host, port))
# queue up to 5 requests
serversocket.listen(5)
clientsocket, addr = serversocket.accept()
print("Connected to: %s" % str(addr))
cap = cv2.VideoCapture(1)


def main():
    # main structure of the function
    global path_x, path_y, window_name, point_1, point_2, first_point, tracker, obstacle_color_lower, obstacle_color_upper
    cv2.namedWindow(window_name) # create widow
    rectangle_point = []
    obstacle_point = []
    old_frame_grey = 0
    LKP = dict(winSize=(13, 13), maxLevel=15, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TermCriteria_COUNT, 40, 0.03)) # optical flow tracker for the destination
    Finish = False # The robot has not reach the destination
    close = False # The robot is not too close to the destination
    create = True # We need to create a path to the destination
    point_1ist = []
    while True:
        clientsocket.settimeout(0.000001)
        cv2.setMouseCallback(window_name, select_point) # detect mouse selection for destination
        ret, frame = cap.read() # read from camera
        frame_grey = get_gray(frame) # get the grey version of the frame
        key = cv2.waitKey(1)
        if key == ord("s"):
            initBB = cv2.selectROI(window_name, frame, fromCenter=False, showCrosshair=True) # tracker for the robot
            tracker.init(frame, initBB)
            first_point = True # The starting point has been selected
        if first_point:
            success, rect = track(frame) # draw the tracking rectangle
            point_copy = point_1 # copy the starting point so there is a way to come back
            if success:
                cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)
                point_1 = ((rect[0] + rect[0] + rect[2])/2 , (rect[1] + rect[1] + rect[3])/2)
            else:
                print("lost track")
        if create: # If we need to do the path plan
            obstacle_point, rectangle_point = get_color_position(frame, obstacle_color_lower, obstacle_color_upper)
            obstacle_point = check(obstacle_point)
        if create and first_point and second_point: # If starting point and destination are all selected and we need to satrt
            give_path() # we give the path that the robot need to move to the client
        for obstacle in rectangle_point:  # draw the obstacle when find them
            cv2.rectangle(frame, (obstacle[0], obstacle[1]), (obstacle[0] + obstacle[2], obstacle[1] + obstacle[3]), (255, 255, 0), 3)
        for obstacle in obstacle_point: # draw the circle of the obstacle
            draw_circle(frame,obstacle[0], radius = round(obstacle[1]))
        if second_point: # if destination is selected, we track the destination and draw the tracker
            draw_circle(frame, point_2)
            temp = np.array([[point_2[0], point_2[1]]], dtype = np.float32)
            current_point_2, status, error = cv2.calcOpticalFlowPyrLK(old_frame_grey, frame_grey, temp, None, **LKP)
            x_2, y_2 = current_point_2.ravel()
            point_2 = (x_2, y_2)
        if key == ord('q'):  # brake when q is pressed
            break
        temp_num = 0
        ratio = int(array_size / 50)
        if first_point and second_point:
            close = check_close(point_1, point_2)
        for index in range(0, int(len(path_x)//ratio)-1):
            temp_num += ratio
            draw_circle(frame, (path_x[temp_num], path_y[temp_num]), radius = 1, color=(150, 210, 50)) # draw the path
        cv2.imshow(window_name, frame)  # show it out
        old_frame_grey = frame_grey.copy()
        try:
            # Try to receive the message that it has finished the move
            msg = clientsocket.recv(1024).decode("UTF-8")
            # If the motion has been finished
            # calculate the new move
            print(msg)
            if msg == "Finish":
                Finish = True
            if msg == "test":
                if close:
                    clientsocket.send("stop".encode("UTF-8"))
                else:
                    clientsocket.send("pass".encode("UTF-8"))
        except:
            pass
        if Finish: # The robot has reached the destination
            cap.release()
            cv2.destroyAllWindows()
            time.sleep(15)
            # Sleep 15 seconds so I have time to plug out the global camera and plug in the local camera T_T
            cap2 = cv2.VideoCapture(1)
            cv2.namedWindow('grab')
            ret, frame_2 = cap2.read()
            order = check_middle(frame_2)
            clientsocket.send(order.encode("UTF-8"))
            cv2.imshow('grab', frame_2)
            while True:
                ret, frame_2 = cap2.read()
                key = cv2.waitKey(1)
                order = check_middle(frame_2) # give the order to the robot to make it to reach the right position such that it can just grab the ball
                cv2.imshow('grab', frame_2)
                try:
                    msg = clientsocket.recv(1024).decode("UTF-8")
                    if msg =="Finish":
                        clientsocket.send(order.encode("UTF-8"))
                    elif msg == "grab":
                        break
                except:
                    pass
            temp = point_2 # we switch the destination and the starting point
            point_2 = point_copy
            point_1 = temp
            give_path() # we give the path from the destination to the original point to the robot
            break # everything is done, break the loop
    cv2.destroyAllWindows()


def give_path():
    # This function gived the desired path to the server
    get_path(point_1, point_2, obstacle_point, frame)
    temp_point = np.array([point_1[0], point_1[1], 1])
    temp_point = temp_point.transpose()
    temp_solution = solve_matrix(calibration_matrix, temp_point)
    text = str(int(temp_solution[0]) / 10) + ' ' + str(-1 * int(temp_solution[1]) / 10) + ' '
    ratio = int(array_size / 50)
    temp_num = 0
    for num in range(0, int(len(path_x) // ratio) - 1):
        temp_num += ratio
        point = np.array([path_x[temp_num], path_y[temp_num], 1])
        point = point.transpose()
        result = solve_matrix(calibration_matrix, point)
        text = text + str(int(result[0]) / 10) + " " + str(-1 * int(result[1]) / 10) + " "
        point_1ist.append(result)
    clientsocket.send(text.encode("UTF-8"))  # send a brake message to the robot
    create = False


def select_point(event, x, y, flags, params):
    # This function detect if there is a mouse click on the screen to select the point
    global second_point,point_2
    if event == cv2.EVENT_LBUTTONDOWN:
        second_point = True
        point_2 = (x, y)


main()
