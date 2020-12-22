
###################################################################################################################
# This file contains all other functions
###################################################################################################################
import numpy as np
import cv2
from global_variables import *


def get_gray(frame):
    # Input is the image
    # Return the gray version of the image
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def solve_matrix(matrix, y):
    # This function solve the given matrix
    result = np.linalg.solve(matrix, y)
    temp = [result[0] / result[2], result[1] / result[2]]
    return temp


def track(frame):
    # This function tracks certain object
    # Input is the current frame
    # Output is the status of tracking and the rectangle that contains the object
    global tracker
    (success, box) = tracker.update(frame)
    rect = success
    if success:
        (x, y, w, h) = [int(v) for v in box]
        rect = (x, y, w, h)
    return success, rect