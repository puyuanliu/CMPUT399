
###################################################################################################################
# This file contains the function that deals with the color processing part
###################################################################################################################
import cv2
import numpy as np


def get_color_position(frame, lower, upper):
    # This function detects all the obstacle that has a color with in the color range
    # Input is the current frame and lower upper bound of the color range
    # It output a lise that contains the coordinate of all the object within the color range
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
            bc.append([(x, y), r+60])
    return bc, br


def draw_circle(img, center_point, radius=6, color=(255, 0, 0), thickness=3):
    # center point is the center of the circle (x,y). radius is the radius of the circle.
    # If -1 is passed for closed figures like circles, it will fill the shape. default thickness
    # color : Color of the shape. for BGR, pass it as a tuple, eg: (255,0,0) for blue. For grayscale, just pass the scalar value.
    # thickness : if -1 is passed for closed figures like circles, it will fill the shape, default thickness = 1.
    cv2.circle(img, (int(center_point[0]), int(center_point[1])), radius, color, thickness)

