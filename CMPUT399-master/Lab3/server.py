#!/usr/bin/python

import socket
import cv2
import numpy as np

# global varibles
previous_points_1 = np.array([[]]) # previous end effector coordinates
previous_points_2 = np.array([[]]) # previous destination coordinates 
point_1 = ()                       # initial end effector coordinates
point_2 = ()                       # initial destination coordinates                      
old_frame_grey = 0                 # old frame
first_point = False                # if first point has been selected
second_point = False               # if second point has been selected
cap = cv2.VideoCapture(1)          
LKP = dict(winSize=(12, 12), maxLevel=10,
           criteria=(cv2.TERM_CRITERIA_EPS | cv2.TermCriteria_COUNT, 50, 10))  # Luca kandace parameter
# global varibles


def capture_frames(clientsocket):
    # This function is the main structure of the program
    global previous_points_1, previous_points_2, old_frame_grey, cap
    window_name = "webcam"
    cv2.setMouseCallback(window_name, select_point) # detec mouse click
    cv2.namedWindow(window_name) # name the window
    while True:
        restart() # destination is reached, restart the whole process
        key = cv2.waitKey(1) # wait 1
        guess = 16 # Angle of initial move
        J,deltay = initialize(guess, window_name) # Get initial Jaccobian
        print("condition number is: ", np.linalg.cond(J))
        not_stop = True # destination has not been reached
        pre_x, pre_y = previous_points_1.ravel() 
        first_run = True # first time run
        while not_stop: # When the robot has not reach the final destination
            ret, img = cap.read()  # read the frame from the camera
            frame_grey = get_gray(img)
            # handle current frame
            if first_point and second_point:
                draw_circle(img, point_1) # draw the circle of the starting point and destination, track end effector and destination
                current_point_1, status, error = cv2.calcOpticalFlowPyrLK(old_frame_grey, frame_grey, previous_points_1, None, **LKP)
                x_1, y_1 = current_point_1.ravel()
                draw_circle(img, (x_1, y_1), color=(0, 255, 0), thickness=-1)
                draw_circle(img, point_2)
                current_point_2, status, error = cv2.calcOpticalFlowPyrLK(old_frame_grey, frame_grey, previous_points_2, None, **LKP)
                x_2, y_2 = current_point_2.ravel()
                draw_circle(img, (x_2, y_2), color=(0, 255, 255), thickness=-1)
                old_frame_grey = frame_grey.copy()
                test = np.linalg.norm(np.array([x_2 - x_1, y_2 - y_1]))
                #if test <30: # if it is close to the end effector
                #    clientsocket.send("brake".encode("UTF-8")) # send a brake message to the robot
                #    break
                if first_run:
                    e = np.array([[x_2 - x_1, y_2 - y_1]]) # error
                    e = e.transpose() 
                    q = get_theta(J, e) # get the angle that need to move
                    q_1,q_2 = q.ravel() # revel from array
                    clientsocket.send((str(q_1) + " " + str(q_2)).encode("UTF-8")) # give the angle to the robot
                    first_run = False 
            # send calculated information to ev3
                try:
                    # Try to receive the message that it has finished the move 
                    clientsocket.recv(1024).decode("UTF-8")
                    # If the motion has been finished
                    # calculate the new move
                    e = np.array([[x_2 - x_1, y_2 - y_1]]) # update
                    e = e.transpose()   
                    deltay = np.array([[x_1 - pre_x, y_1 - pre_y]]) 
                    deltay = deltay.transpose()
                    J = calculate_J(J, q, deltay)
                    q_1,q_2 = q.ravel()
                    clientsocket.send((str(q_1) + " " + str(q_2)).encode("UTF-8")) # send the new angle to robot
                    pre_x, pre_y = current_points_1.ravel() #update
                except:
                    pass
                previous_points_1 = current_point_1 # update
                previous_points_2 = current_point_2
            cv2.imshow(window_name, img) # show it out
            key = cv2.waitKey(1)
            # check if esc key pressed

        if key == ord('q'): # brake when q is pressed
            clientsocket.close()
            cv2.destroyWindow("webcam")
            break
           
    cap.release()
    cv2.destroyAllWindows()


def draw_circle(img, center_point, radius=6, color=(255, 0, 0), thickness=3):
    # center point is the center of the circle (x,y). radius is the radius of the circle.
    # If -1 is passed for closed figures like circles, it will fill the shape. default thickness
    # color : Color of the shape. for BGR, pass it as a tuple, eg: (255,0,0) for blue. For grayscale, just pass the scalar value.
    # thickness : if -1 is passed for closed figures like circles, it will fill the shape, default thickness = 1.
    cv2.circle(img, center_point, radius, color, thickness)


def select_point(event, x, y, flags, params):
    # The function detect if the first point or the second point is selected.
    # input is the event and the coordinates of the selected x,y
    global first_point, second_point, point_1, point_2, previous_points_1, previous_points_2, old_frame_grey, cap
    if event == cv2.EVENT_LBUTTONDOWN:
        if first_point is False: # if the first point is not selected
            first_point = True
            point_1 = (x, y)
            previous_points_1 = np.array([[x, y]], dtype=np.float32)
        else: # if the first point is already selected
            second_point = True
            point_2 = (x, y)
            previous_points_2 = np.array([[x, y]], dtype=np.float32)
            ret, frame = cap.read()  # read the frame from the camera
            old_frame_grey = get_gray(frame)


def get_gray(frame):
    # Input is the image
    # Return the gray version of the image
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def calculate_J(J, q, delta_y):
    # Input is the current Jacobian matrix, q, and delta_Y
    # output is the updated Jacobian
    # following code is the btoyden update
    norm = np.linalg.norm(q)
    norm = norm*norm
    J = J + np.dot((delta_y - np.dot(J, q)) / norm, q.transpose())
    return J

def initialize(initial_guess,window_name):
    #This function initialize and return the jacobian and delta y
    # Input is the angle for initial motion and the name of current window
    #cv2.setMouseCallback(window_name, select_point)
    while not first_point: # while the first point is not selected
        ret, img = cap.read()  # read the frame from the camera
        cv2.imshow(window_name, img)
        cv2.waitKey(1)
        pass
    current_position = point_1
    theta = [initial_guess,0] # calculate the components of the initial Jcobian
    clientsocket.send((str(theta[0]) + " " + str(theta[1])).encode("UTF-8")) # send the angle to the robot
    new_position = initialize_update(window_name)
    delta_1_1 = (new_position[0] - current_position[0])/initial_guess
    delta_2_1 = (new_position[1] - current_position[1])/initial_guess
    current_position= new_position
    theta = [0,initial_guess]
    clientsocket.send((str(theta[0]) + " " + str(theta[1])).encode("UTF-8"))
    new_position = initialize_update(window_name)
    delta_1_2 = (new_position[0]- current_position[0])/initial_guess
    delta_2_2 = (new_position[1] - current_position[1])/initial_guess
    J = np.array([[delta_1_1, delta_1_2],[delta_2_1, delta_2_2]]) # build the initial Jacobian
    delta_y = np.array([new_position[0] - point_1[0], new_position[1] - point_1[1]]) # initial delta_y
    delta_y = delta_y.transpose()
    print("Initial J is", J)
    return J, delta_y



def get_theta(J,e):
    # This function takes the current Jacobian and  error
    # Output is the angle that needs to be moved
    inverse = np.linalg.inv(J)
    delta_theta = 0.3*np.dot(inverse, e)
    return delta_theta

def initialize_update(window_name):
    # This function output the position of the end effector after the motion
    # a function that is used to update the image frame during the initialization
    global previous_points_1
    clientsocket.settimeout(0.01)
    ret, img = cap.read()  # read the frame from the camera
    old_frame_grey = get_gray(img)
    finish = False
    while not finish:
        try:
            clientsocket.recv(1024).decode("UTF-8")
            finish = True
        except:
            ret, img = cap.read()  # read the frame from the camera
            frame_grey = get_gray(img)
            current_position, status, error = cv2.calcOpticalFlowPyrLK(old_frame_grey, frame_grey, previous_points_1, None, **LKP)
            x_1, y_1 = current_position.ravel()
            draw_circle(img, (x_1, y_1), color=(0, 255, 0), thickness=-1)
            old_frame_grey = frame_grey
            cv2.imshow(window_name, img)
            cv2.waitKey(1)
            previous_points_1 = current_position
    x_1, y_1 =previous_points_1.ravel()
    return x_1,y_1


def restart():
    # This function initialize everything and prepare for the new process
    global previous_points_1, previous_points_2, old_frame_grey, point_1, point_2,first_point,second_point
    old_frame_grey = 0
    previous_points_1 = np.array([[]])
    previous_points_2 = np.array([[]])
    point_1 = ()
    point_2 = ()
    first_point = False
    second_point = False

if __name__ == "__main__":
    # setup server socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "169.254.177.247"
    port = 9999
    serversocket.bind((host, port))
    # queue up to 5 requests
    serversocket.listen(5)
    clientsocket, addr = serversocket.accept()
    print("Connected to: %s" % str(addr))
    capture_frames(clientsocket)
