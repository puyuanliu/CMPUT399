
#############################################################
# This function is used to determine the position of the target when
# we can grab the target
# Basically, we put the ball to the right position that the robot can
# just grab it, then record the corresponding position of the ball
# in the image space.
#################################################################

import cv2
import sys
import numpy as np
import time
window_name = "webcam"
cap = cv2.VideoCapture(1)
ret, frame = cap.read()
time.sleep(0.1)
def main():
    result = False
    cv2.namedWindow(window_name)
    while True:
        ret, frame = cap.read()
        key = cv2.waitKey(1)
        temp = check_middle(frame)
        cv2.imshow(window_name,frame)



def check_middle(frame):
    obstacle_color_lower = np.array([0, 117, 0])
    obstacle_color_upper = np.array([13, 255, 255])
    obstacle_point, rectangle_point = get_color_position(frame, obstacle_color_lower, obstacle_color_upper)
    width = cap.get(3)  # float
    height = cap.get(4) # float
    print(obstacle_point)
    w_half = width/2
    if len(obstacle_point) != 0:
        if (obstacle_point[0][0][0] - w_half)**2 <5:
            print(obstacle_point[0][0][0] - w_half)
            return False
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
    # 腐蚀操作
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 根据阈值构建掩膜
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('image', mask)
    # 腐蚀操作
    mask = cv2.erode(mask, None, iterations=2)
    # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
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