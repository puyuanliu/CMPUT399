#!/usr/bin/python3       
# RUN ON BRICK
from ev3dev.ev3 import *
from time import sleep
import time
from math import *
import socket
pi = 3.1415926
mot1 = LargeMotor(OUTPUT_C)  # right motor wheel
mot2 = LargeMotor(OUTPUT_D)  # left motor wheel
motor_base = Largemotor(OUTPUT_B)
motor_claw = MediumMotor(OUTPUT_A)
t = 2
t_2 = 2
WHEEL_D = 0.056  # outer wheel diameter in meters
LENGTH = 0.17  # length between the centres of the left and right wheel in meters
SPD = 200  # the speed that each motor travels
current_theta = pi / 2


def setup_client(host, port):
    global current_theta
    # create a socket object
    print("setting up client")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to hostname on the port.
    s.connect(("169.254.177.247", port))
    # Receive no more than 1024 bytes
    reach = False # status that if the robot has reach the destination
    msg = s.recv(1024).decode("UTF-8")  # receive the data from the serve
    drive_robot(msg)
    sleep(0.5)
    print("Finish")
    s.send('Finish'.encode("UTF-8"))
    msg = ''
    while msg != "Reach":
        msg = s.recv(1024).decode("UTF-8")
        print(msg)
        print("\n")
        if msg =="Go left":
            turn_left(2, spd = 10)
            current_theta-=2
            sleep(0.1)
        elif msg == "Go right":
            turn_right(2, spd = 10)
            current_theta+=2
            sleep(0.1)
        elif msg == "Go up":
            move_forward(0.005, spd = 10)
            sleep(0.1)
        elif msg == "Go down":
            move_backwards(0.005, spd = 10)
            sleep(0.1)
        s.send('Finish'.encode("UTF-8"))
    sleep(0.5)
    turn_left(180)
    msg = s.recv(1024).decode("UTF-8")
    #drive_robot(msg)
    #grab_ball

    s.close()


def deg_to_rad(d):
    return d * (pi / 180)


# move backwards
def move_backwards(dist, spd=SPD):
    # how many full rotations the robot wheels should make to move backwards
    pos = (dist / (pi * WHEEL_D)) * 360

    mot1.run_to_rel_pos(position_sp=-pos, speed_sp=spd, stop_action="hold")
    mot2.run_to_rel_pos(position_sp=-pos, speed_sp=spd, stop_action="hold")
    time.sleep(pos/spd)

# turn the robot right
def turn_right(position, spd=SPD):
    mot1.run_to_rel_pos(position_sp=-position, speed_sp=spd, stop_action="hold")
    mot2.run_to_rel_pos(position_sp=position, speed_sp=spd, stop_action="hold")

    time.sleep(position/spd)


# turn the robot left
def turn_left(position, spd=SPD):
    mot1.run_to_rel_pos(position_sp=position, speed_sp=spd, stop_action="hold")
    mot2.run_to_rel_pos(position_sp=-position, speed_sp=spd, stop_action="hold")

    time.sleep(position/spd)


def rotate_to_des_theta(theta, current_theta, spd=SPD):
    print('theta for atan2 = ', theta)
    print('current_theta = ', current_theta)
    new_theta = theta - current_theta
    print('new_theta', new_theta)
    if new_theta < -pi:
        new_theta += 2 * pi
    elif new_theta > pi:
        new_theta -= 2 * pi
    distance = new_theta * (LENGTH / 2)
    print('distance', distance)
    position = abs((distance / (pi * WHEEL_D)) * (360))  # it doesn't matter whether the position is pos or neg
    print('position = ', position)
    if new_theta > 0:  # turn left
        turn_left(position, spd)
    else:  # turn right
        turn_right(position, spd)


def move_forward(distance, spd=SPD):
    # how many full rotations the robot wheels should make to move forwards
    position = (distance / (pi * WHEEL_D)) * (360)
    print('forward_rotate_distance = ', position)
    mot1.run_to_rel_pos(position_sp=position, speed_sp=spd, stop_action="coast")
    mot2.run_to_rel_pos(position_sp=position, speed_sp=spd, stop_action="coast")

    time.sleep(position/spd)


def drive_robot(string_coord):
    global current_theta
    sequence = string_coord.split(' ')
    # current x and y positions of the robot's centre
    curr_x = float(sequence[0])
    curr_y = float(sequence[1])
    i = 2  # index of the sequence
    # assumption, initially the robot is at (0,0) and facing 90 degrees which is current_theta
    while i < len(sequence)-1:
        # desired x and y positions
        des_x = float(sequence[i])
        print(sequence[i])
        des_y = float(sequence[i + 1])
        print(sequence[i + 1])
        # distance between the current position and the desired position, and it's in metres
        des_d = sqrt((des_x - curr_x) ** 2 + (des_y - curr_y) ** 2)
        print('des_d = ', des_d)
        # the angle the robot must rotate
        theta = atan2((des_y - curr_y), (des_x - curr_x))
        # call to rotate the robot by the difference of theta and current angle
        rotate_to_des_theta(theta, current_theta)
        # current angle the robot is facing after rotation
        current_theta = theta
        # after rotating for desired angle
        # we make the robot drive forward for the amount of distance
        move_forward(des_d / 100)  # divide by 100 to change the units from metres to cm
        print("I reached after move_forward")
        sleep(0.1)
        # current coordinate the robot is at
        curr_x = des_x
        curr_y = des_y
        # its incremented by two because the i = x_coordinate and i+1 is y_coordinate
        i += 2


def grab():
    global t, t_2
    motor_base.run_timed(speed_sp=100, time_sp=t)
    sleep(t)
    motor_claw.run_timed(speed_sp=-100, time_sp=t2)
    sleep(t2)
    motor_base.run_timed(speed_sp=-100, time_sp=t)
    sleep(t)


if __name__ == "__main__":
    host = socket.gethostname()
    port = 9999
    setup_client(host, port)
