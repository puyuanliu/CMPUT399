
###################################################################################################################
# This file contains the function that do the path plan
###################################################################################################################
from global_variables import*
from check_status import*
import cv2


def get_path(start, end, obstacle):
    # This function is the main structure of the path plan
    # Input is the staring point and destination, together with a list of the center of the obstacle point
    # No output, it will directly make change to the path list in the global variables
    global path_x, path_y,array_size
    path_x = np.linspace(start[0], end[0], array_size)
    path_y = np.linspace(start[1], end[1], array_size)
    while check_all_obstacle(path_x, path_y, obstacle):
        for part_obstacle in obstacle:
            while path_plan(part_obstacle):
                pass


def path_plan(obstacle):
    # This function fo the path plan to avoid single obstacle
    global path_x, path_y, start_record, end_record
    radius = obstacle[1]
    obstacle = obstacle[0]
    pointer = 0
    counter = 0
    process = False
    while pointer < len(path_x):
        exist = check_obstacle(path_x[pointer], path_y[pointer], obstacle, radius)
        if exist:
            counter += 1
        else:
            if counter == 0:
                pass
            else:
                break
        pointer += 1
    if counter != 0:
        process = True
    if process:
        direction = check_direction(obstacle)
        temp_radius = math.sqrt((path_x[pointer - 1] - path_x[pointer - counter]) ** 2 + (
                    path_y[pointer - 1] - path_y[pointer - counter]) ** 2) / 2
        temp_x = path_x.copy()
        temp_y = path_y.copy()
        amount = do_avoid(pointer - counter - 1, pointer, temp_radius, direction)
        counter_2 = 0
        for index in range(start_record, end_record):
            if (path_x[index] - obstacle[0])**2 + (path_y[index] - obstacle[1])**2 < radius**2:
                counter_2 += 1
        if counter_2 > amount*0.9:
            if direction == "up":
                direction = "down"
            else:
                direction ="up"
            path_x = temp_x
            path_y = temp_y
            do_avoid(pointer - counter - 1, pointer, temp_radius, direction)
    return process


def do_avoid(start, end, radius, direction):
    # This function is the actual function that makes change to the path
    # input is the starting point and destination, radius of the obstacle
    # direction is some parameter for this specific algorithm
    global path_x, path_y, start_record, end_record
    amount = 0
    start_record = start
    end_record = end
    slope = (path_y[end] - path_y[start]) / (path_x[end] - path_x[start])
    k = -1 / slope
    counter = start
    angle = np.linspace(0, math.pi, end - start + 1)
    for theta in angle:
        d = radius * math.sin(theta)
        if direction == "up":
            if k < 0:
                deltax = math.sqrt(d ** 2 / (1 + k ** 2))
                deltay = k * deltax
            else:
                deltax = -math.sqrt(d ** 2 / (1 + k ** 2))
                deltay = k * deltax
        else:
            if k < 0:
                deltax = -math.sqrt(d ** 2 / (1 + k ** 2))
                deltay = k * deltax
            else:
                deltax = math.sqrt(d ** 2 / (1 + k ** 2))
                deltay = k * deltax
        path_x[counter] += deltax
        path_y[counter] += deltay
        amount += 1
        counter += 1
    return amount


def check_direction(obstacle):
    global path_x, path_y, start_record, end_record
    smallest = 1000000
    small_point = ()
    index = -1
    for i in range(start_record, (start_record+end_record)//2):
        if (path_x[i] - obstacle[0]) ** 2 + (path_y[i] - obstacle[1]) ** 2 < smallest:
            small_point = (path_x[i], path_y[i])
            smallest = (path_x[i] - obstacle[0]) ** 2 + (path_y[i] - obstacle[1]) ** 2
            index = i
    smallest = 1000000
    second_small_point = ()
    for i in range(start_record, (start_record+end_record)//2):
        if (path_x[i] - obstacle[0]) ** 2 + (path_y[i] - obstacle[1]) ** 2 < smallest and i != index:
            second_small_point = (path_x[i], path_y[i])
            smallest = (path_x[i] - obstacle[0]) ** 2 + (path_y[i] - obstacle[1]) ** 2
    if small_point[1] < obstacle[1] or second_small_point[1] < obstacle[1]:
        direction = "up"
    else:
        direction = "down"
    #print("Direction is !!!!: ", direction)
    print(small_point, second_small_point, obstacle)
    return direction
