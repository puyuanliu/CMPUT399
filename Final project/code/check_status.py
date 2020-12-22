
###################################################################################################################
# This file contains the code used for the checking purpose
###################################################################################################################
import numpy as np

desired_destination = (305, 478) # coordinate of the target in image space when we can just grab the ball


def check_close(p_1, p_2):
    # Input is the coordinate of the robot and that of the destination
    # The function output False if they are not too close
    # It returns True if they are indeed too close to each other
    standard = 27
    p_1 = np.array([p_1[0], p_1[1], 1])
    p_1 = p_1.transpose()
    p_2 = np.array([p_1[0], p_2[1], 1])
    p_2 = p_2.transpose()
    r_1 = solve_matrix(calibration_matrix,p_1)
    r_2 = solve_matrix(calibration_matrix,p_2)
    distance = math.sqrt((r_1[0] - r_2[0])**2 + (r_1[1] - r_2[1])**2)/10
    print("Distance between robot and destination is:", distance)
    if distance > standard:
        return False
    else:
        return True


def check_middle(frame):
    # This function checks if the target has reach the desired coordinate
    # It will output the order that the robot should move such that the target
    # will appear in the expected position in image space
    global desired_destination
    obstacle_color_lower = np.array([0, 37, 0])
    obstacle_color_upper = np.array([25, 255, 255])
    obstacle_point, rectangle_point = get_color_position(frame, obstacle_color_lower, obstacle_color_upper)
    width = cap.get(3)  # float
    height = cap.get(4) # float
    print(obstacle_point)
    w_half = width/2
    standard = 15
    if len(obstacle_point) != 0:
        if math.sqrt((obstacle_point[0][0][0] - desired_destination[0])**2 + (obstacle_point[0][0][1] - desired_destination[1])**2) <standard:
            return "Reach"
        elif (obstacle_point[0][0][0] - desired_destination[0])> standard:
            return "Go right"
        elif (obstacle_point[0][0][0] - desired_destination[0])< -standard:
            return "Go left"
        elif (obstacle_point[0][0][1] - desired_destination[1])>6:
            return "Go down"
        elif (obstacle_point[0][0][1] - desired_destination[1])< -6:
            return "Go up"
        else:
            return "Reach"
    return False


def check(obstacle_list):
    # This function checks if there are obstacle that is very closed to each other
    # If 2 obstacle is too close to each other and there is no way for the robot to
    # go through their separation, we will merge the 2 obstacle together
    # It will output the list such that all obstacle that are too close to each other
    # has been merged
    is_pass = False
    if not is_pass:
        is_pass = True
        for i in obstacle_list:
            for j in obstacle_list:
                if i != j:
                    distance = (i[0][0] - j[0][0])**2 + (i[0][1] - j[0][1])**2  # [(87.0, 411.5), 13.905224800109863]
                    if distance < (i[1] + j[1])**2:
                        middle = ((i[0][0] + j[0][0])/2, (i[0][1] + j[0][1])/2)
                        new_radius = i[1] + j[1]
                        obstacle_list.remove(i)
                        obstacle_list.remove(j)
                        obstacle_list.append([middle, new_radius])
                        is_pass = False
                        break
        for i in obstacle_list:
            for j in obstacle_list:
                if i != j:
                    distance = (i[0][0] - j[0][0]) ** 2 + (i[0][1] - j[0][1]) ** 2  # [(87.0, 411.5), 13.905224800109863]
                    if distance < i[1] ** 2 + j[1] ** 2:
                        is_pass = False
    return obstacle_list


def check_all_obstacle(path_x, path_y, obstacle):
    # This function checks if all the obstacle has been successfully avoided
    check = False
    for index in range(0, len(path_x)):
        x = path_x[index]
        y = path_y[index]
        for data in obstacle:
            radius = data[1]
            d = (x - data[0][0]) ** 2 + (y - data[0][1]) ** 2
            if d < radius ** 2:
                check = True
                break
    return check


def check_obstacle(x, y, obstacle, radius):
    # This function check if a single obstacle lies in path between the origin and destination
    check = False
    d = (x - obstacle[0]) ** 2 + (y - obstacle[1]) ** 2
    if d < radius ** 2:
        # print("Current d is ", d)
        check = True
    return check




