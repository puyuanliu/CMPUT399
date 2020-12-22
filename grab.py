import cv2
import sys
import numpy as np
import time
import math
cap = cv2.VideoCapture(1)
window_name = "webcam"
ret, frame = cap.read()
time.sleep(0.1)
desired_destination = (326, 250)


def main():
    result = False
    cv2.namedWindow(window_name)
    cv2.namedWindow('image')
    while not result:
        ret, frame = cap.read()
        check_middle(frame)
        key = cv2.waitKey(1)
        cv2.imshow(window_name,frame)
    cap.release()
    cv2.destroyAllWindows()


def check_middle(frame):
    global desired_destination
    obstacle_color_lower = np.array([0, 37, 0])
    obstacle_color_upper = np.array([25, 255, 255])
    obstacle_point, rectangle_point = get_color_position(frame, obstacle_color_lower, obstacle_color_upper)
    width = cap.get(3)  # float
    height = cap.get(4) # float
    print(obstacle_point)
    w_half = width/2
    standard = 25
    if len(obstacle_point) != 0:
        if math.sqrt((obstacle_point[0][0][0] - desired_destination[0])**2 + (obstacle_point[0][0][1] - desired_destination[1])**2) <standard:
            print("Reach")
        elif (obstacle_point[0][0][0] - desired_destination[0])> standard:
            print("Go right")
        elif (obstacle_point[0][0][0] - desired_destination[0])< -standard:
            print("Go left")
        elif (obstacle_point[0][0][1] - desired_destination[1])>standard:
            print("Go down")
        elif (obstacle_point[0][0][1] - desired_destination[1])< -standard:
            print("Go up")
        else:
            print("Reach")
    return False


def get_color_position(frame, lower, upper):
    fidelity = False
    ROOT_NODE = -1
    fidelityValue = .7
    if len(sys.argv) > 2:
        fidelity = bool(sys.argv[2])
    if len(sys.argv) > 3:
        fidelityValue = float(sys.argv[3])
    # For images
    imgCopy = frame.copy()
    img = cv2.medianBlur(frame, 15)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('image', mask)
    mask = cv2.erode(mask, None, iterations=2)
    img = cv2.dilate(mask, None, iterations=2)

    # img = cv2.adaptiveBilateralFilter(img, (5, 5), 150) # Preserve edges
    # img = cv2.blur(img, (3,3))
    imgt = img
    # _, imgt = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY_INV)
    imgt = cv2.morphologyEx(imgt, cv2.MORPH_OPEN, (5, 5))
    img2 = imgt.copy()
    _, c, h = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    fidelityRange = 0
    if fidelity:
        maxArea = .0
        for i in c:  # With images it is convenient to know the greater area
            area = cv2.contourArea(i)
            if area > maxArea:
                maxArea = area
        fidelityRange = maxArea - (
                maxArea * fidelityValue)  # If objects have same size it prevents false detection
    totalContours = 0
    br = []
    bc = []
    for i in range(len(c)):
        if h[0][i][3] == ROOT_NODE and cv2.contourArea(c[i]) >= fidelityRange:
            totalContours += 1
            approx = cv2.approxPolyDP(c[i], 3, True)
            br.append(cv2.boundingRect(approx))
            (x, y), r = cv2.minEnclosingCircle(approx) # get the center and radius of the circle containing the obstacle
            bc.append([(x, y), r+20])
    return bc, br


main()