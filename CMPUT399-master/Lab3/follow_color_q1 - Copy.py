from collections import deque
import numpy as np
import cv2
import sys

# This program analyzes the current frame and draws the desired two tracking points, 
# the two tracking points should be red and yellow respectively. 
# The returned frame will have green circle and pink center point indicated for both points, 
# for the path color for red tracking point is red and the the path color for yellow tracking point is light blue.
def main():
    # Below is the set of definition of threshold (upper and lower) value for red center
    # The value is in HSV space 
    redLower = np.array([170, 100, 100])
    redUpper = np.array([179, 255, 255])

    # Below is the set of definition of threshold (upper and lower) value for yellow center
    # The value is in HSV space 
    yellowLower = np.array([22, 100, 100])
    yellowUpper = np.array([38, 255, 255])

    # Turn on the camera
    # The camera corresponds to the USB camera (1), screen built-in camera (0) 
    camera = cv2.VideoCapture(1)
    # detect if the camera is correctly connected
    if (camera.isOpened()):
        print("camera is connected!")
    else:
        print ('Camera is not connected, please retry.')
        sys.exit()
    # initialize the list for the tracking points
    # The maxium tracking points list is 32 for each tracking point
    red_buffer = 32
    red_pts = deque(maxlen=red_buffer)
    yellow_buffer = 32
    yellow_pts = deque(maxlen=yellow_buffer)
    # iterate over each frame and detect the locaton of the robot's colored tip (red), and the target (yellow)
    while True:
        # read the frame
        (ret, frame) = camera.read()
        [red_center, red_pts] =  center_capture(frame, redLower, redUpper, red_pts)
        print('red:' ,red_center)
        draw_path(red_pts, (0, 0, 255), frame) # the path color for red tracking point is red
        [yellow_center, yellow_pts] =  center_capture(frame, yellowLower, yellowUpper, yellow_pts)
        draw_path(yellow_pts, (255, 255, 0), frame) # the path color for yellow tracking point is light blue
        print('yellow:' ,yellow_center)
        cv2.imshow('Frame', frame)
        # if detected the escape key press then close the window
        k = cv2.waitKey(5)&0xFF
        if k == 27:
            break
    camera.release()
    cv2.destroyAllWindows()

# This program analyzes the current frame and draws the desired two traking points
# the two tracking points should be red and yellow respectively
# the returned frame will have green circle and pink center point indicated for both points
# Input: frame, lower, upper
# frame is the frame that needed to be analyzed
# lower, upper is the threshold (upper and lower) value for desired tracking center in HSV space
# Return: center, pts
# pts is the list of the detected centroid 
# center is the current centroid location
def center_capture(frame, lower, upper, pts):
    # Transform the frame into the HSV space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # build the mask for red color
    mask = cv2.inRange(hsv, lower, upper)
    # erode the mask in order to be smooth
    mask = cv2.erode(mask, None, iterations=2)
    # dilate the eroded mask in order to reduce the noise point in the frame
    mask = cv2.dilate(mask, None, iterations=2)
    # detect the contours for the red target
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # initial the centroid of the contour
    center = None
    # if the contours exist:
    if len(cnts) > 0:
        # find the contours which has the largest contour area (locate the exact target)
        c = max(cnts, key = cv2.contourArea)
        # find the enclosure circle for above largest contour area
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        # M is the moment for the above largest contour area
        M = cv2.moments(c)
        # calculate the M to get the centroid
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        # start to draw the path when the redius of the enclosure circle is above 1
        if radius > 1:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.circle(frame, center, 5, (255, 0, 255), -1)
            # append the centroid to the pts list
            pts.appendleft(center)
    return [center, pts]


# This program draws the path according to the input list(pts) to the input 'frame'
# Apply the path in the input 'color' 
def draw_path(pts, color, frame):
    # iterate over the traking points list
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        # define the thickness of the path
        thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
        # draw the path
        cv2.line(frame, pts[i - 1], pts[i], color, thickness)


main()