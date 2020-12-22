
###################################################################################################################
# This file contains all the global variables
###################################################################################################################

previous_points_1 = np.array([[]])
previous_points_2 = np.array([[]])
path_x = np.array([])
path_y = np.array([])
calibration_matrix = np.array([[-823.145746111204, 66.6043425954179, -0.0163278589684892],
[-84.4442490647844, -835.704409692803, -0.0552721538677904],
[1481790.09380990, 346018.874365405, 2452.18461779398]]) # Calibration matrix of the camera
calibration_matrix = calibration_matrix.transpose()
window_name = "webcam"
point_1 = ()  # initial end effector coordinates
point_2 = ()  # initial destination coordinates
first_point = False
second_point = False
start_record = 1
array_size = 400
end_record = array_size
OPENCV_OBJECT_TRACKERS = {"csrt": cv2.TrackerCSRT_create, "kcf": cv2.TrackerKCF_create, "boosting": cv2.TrackerBoosting_create,
                          "mil": cv2.TrackerMIL_create, "tld": cv2.TrackerTLD_create, "medianflow": cv2.TrackerMedianFlow_create, "mosse": cv2.TrackerMOSSE_create}
tracker = OPENCV_OBJECT_TRACKERS['kcf']()
obstacle_color_lower = np.array([114, 24, 0])
obstacle_color_upper = np.array([119, 155, 255])
destination_color_lower = np.array([])
destination_color_upper = np.array([])
point_copy = ' '
# global variables