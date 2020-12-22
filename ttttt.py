import math
import numpy as np
import matplotlib.pyplot as plt
import time

path_x = np.array([])
path_y = np.array([])
start_record = 1
end_record = 500


def main(start, end, obstacle):
    global path_x, path_y
    path_x = np.linspace(start[0], end[0], 500)
    path_y = np.linspace(start[1], end[1], 500)
    #print("\nCurrent x is : ", path_x)
    #print("\nCurrent y is : ", path_y)
    while check_all_obstalce(path_x, path_y, obstacle):
        for part_obstacle in obstacle:
            while path_plan(part_obstacle):
                #print("\nCurrent x is : ", path_x)
                #print("\nCurrent y is : ", path_y)
                plt.plot(path_x, path_y, '.')
                radius = part_obstacle[1]
                circle = plt.Circle(obstacle[0][0], obstacle[0][1], color='k', fill=False)
                plt.gcf().gca().add_artist(circle)
                plt.plot(part_obstacle[0][0],part_obstacle[0][1],'ro')
                circle_2 = plt.Circle(obstacle[1][0], obstacle[1][1], color='k', fill=False)
                plt.gcf().gca().add_artist(circle_2)
                plt.gca().axes.set_xlim([0, 600])
                plt.gca().axes.set_ylim([0, 600])
                plt.show()
                pass


def path_plan(obstacle):
    global path_x, path_y,start_record, end_record
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
        for index in range(start_record,end_record):
            if (path_x[index] - obstacle[0])**2 + (path_y[index] - obstacle[1])**2 < radius**2:
                print((path_x[index] - obstacle[0]) ** 2 + (path_y[index] - obstacle[1]) ** 2, radius**2)
                counter_2 += 1
        print(counter_2, amount)
        if counter_2 > amount*0.9:
            if direction == "up":
                direction = "down"
            else:
                direction ="up"
            path_x = temp_x
            path_y = temp_y
            do_avoid(pointer - counter - 1, pointer, temp_radius, direction)
    #print("ssss", process)
    return process


def check_all_obstalce(path_x, path_y, obstacle):
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
    check = False
    d = (x - obstacle[0]) ** 2 + (y - obstacle[1]) ** 2
    if d < radius ** 2:
        # print("Current d is ", d)
        check = True
    return check


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


def do_avoid(start, end, radius, direction):
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
        # print("Sin theta is ", math.sin(theta))
        # print("theta is", theta)
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
        #print("K is ", k)
        path_x[counter] += deltax
        path_y[counter] += deltay
        amount += 1
        # print("d and k is ",d, k)
        # print("Current counter is",counter)
        # print("deltax and delta y are ", deltax, deltay)
        counter += 1
    return amount


main((188, 111) , (390*1.3, 362*1.3) , [[(450.6985168457031, 391.8382263183594), 27.886213779449463], [(309.5, 251.5), 58.13800811767578], [(9.0, 73.0), 55.0351824760437]])
LU =np.array([[532.667399775138, 22.8743319601163,	77588.4238370610], [25.1417459239959,	534.947802618773,	47553.8696071811],[0.0654805738580426,	0.117939490291985,	368.065254778159]])

A = LU
rhs = np.array([501,179,1])
b = rhs.transpose()
temp = np.linalg.solve(A,b)
print(temp) # computing Q^T*b (project b onto the range of A)
