############################################################################################################
# This file is used to test whether the camera calibration is working well
# It calculate the distance from 2 point from image
# Then we can compare the calculated distance with the actual distance to see if the calibration works

############################################################################################################


import numpy as np
import cv2
import math

point_list = []

matrix = np.array([[-833.813412916852, -112.064383970158, -0.0743343115248786], [80.3378664849669, -832.646963416356, -0.0534219677475282],
[935224.255428330, 622087.654711363, 2469.92217354929]]) #Calibration matrix

matrix = matrix.transpose()

def select_point(event, x, y, flags, params):
    global point_list
    if event == cv2.EVENT_LBUTTONDOWN:
        point_list.append((x,y))
        print(x,y)

cap = cv2.VideoCapture(1)
cv2.namedWindow("Trackbars")
cap.set(3, 1280)
cap.set(4, 960)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([0, 145, 115])
    upper_blue = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    cv2.setMouseCallback("frame", select_point)

    key = cv2.waitKey(1)
    if key == ord('q'):  # brake when q is pressed
        break
    if len(point_list) == 2:
        break
y1 = np.array([point_list[0][0], point_list[0][1], 1])
y1 = y1.transpose()
y2 = np.array([point_list[1][0], point_list[1][1], 1])
y2 = y2.transpose()
print(y1, y2)
print(matrix)
result_1 = np.linalg.solve(matrix, y1)
result_2 = np.linalg.solve(matrix, y2)
print(result_1, result_2)
print(math.sqrt((result_1[0]/result_1[2] - result_2[0]/result_2[2])**2 + (result_1[1]/result_2[2] - result_2[1]/result_2[2])**2))


