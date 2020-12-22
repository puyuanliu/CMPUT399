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
WHEEL_D = 0.055  # outer wheel diameter in meters
LENGTH = 0.167  # length between the centres of the left and right wheel in meters
SPD = 200  # the speed that each motor travels
current_theta = pi / 2
motor_base = LargeMotor(OUTPUT_B)
motor_claw = MediumMotor(OUTPUT_A)
gy = GyroSensor()
value = gy.value()
initial_differecne = value - 90
t = 3.5
t2 = 2.5


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
    drive_robot(msg, s)
    print("Finish")
    s.send('Finish'.encode("UTF-8"))
    sleep(17)
    msg = ''
    real_angle = gy.value() - initial_differecne
    real_angle = deg_to_rad(real_angle)
    need_move = real_angle - current_theta
    #turn_left_real(need_move)
    print("GY value is", gy.value())
    print("Initial difference is", initial_differecne)
    while msg != "Reach":
        msg = s.recv(1024).decode("UTF-8")
        print(msg)
        print("\n")
        if msg =="Go left":
            turn_left(2, spd = 10)
            current_theta-=0.5
            sleep(0.1)
        elif msg == "Go right":
            turn_right(2, spd = 10)
            current_theta+=0.5
            sleep(0.1)
        elif msg == "Go up":
            move_forward(0.005, spd = 10)
            sleep(0.1)
        elif msg == "Go down":
            move_backwards(0.005, spd = 10)
            sleep(0.1)
        s.send('Finish'.encode("UTF-8"))
    grab_ball()
    turn_left_real(pi)
    s.send('grab'.encode("UTF-8"))
    msg = s.recv(1024).decode("UTF-8")
    drive_robot(msg, s)
    s.close()


def turn_left_real(angle):
    # 90 deg turn variables
    WHEEL_RADIUS = 5.50/2
    LENGTH_BETWEEN_WHEELS = 16.7
    TURN_ANGLE = angle
    TURN_DURATION = 2
    CIRCLE_RADIUS = 0

    # straight static variables
    STRAIGHT_TIME = 1.7
    STRAIGHT_DISTANCE = 25

    wr_minus_wl = TURN_ANGLE * LENGTH_BETWEEN_WHEELS / WHEEL_RADIUS

    wr_plus_wl = CIRCLE_RADIUS * wr_minus_wl / (LENGTH_BETWEEN_WHEELS / 2)

    wl = (wr_plus_wl - wr_minus_wl) / 2
    wr = wr_plus_wl - wl

    wl_in_deg = wl * (180 / pi)
    wr_in_deg = wr * (180 / pi)


    straight_speed = (((STRAIGHT_DISTANCE / STRAIGHT_TIME) / WHEEL_RADIUS)) * (180 / pi)

    mot1.run_timed(speed_sp=wl_in_deg / TURN_DURATION, time_sp=(TURN_DURATION) * 1000)
    mot2.run_timed(speed_sp=wr_in_deg / TURN_DURATION, time_sp=(TURN_DURATION) * 1000)
    sleep(TURN_DURATION)

    mot1.stop(stop_action='hold')
    mot1.stop(stop_action='hold')


def grab_ball():
    motor_claw.run_to_rel_pos(position_sp=100, speed_sp=100, stop_action="hold")
    sleep(t2)
    motor_base.run_timed(speed_sp=-100, time_sp=t * 1000)
    sleep(t)
    motor_claw.run_to_rel_pos(position_sp=-100, speed_sp=100, stop_action="hold")
    sleep(t2)
    motor_base.run_timed(speed_sp=100, time_sp=t * 1000)
    sleep(t)


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
    new_theta = theta - current_theta
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
    mot1.run_to_rel_pos(position_sp=position, speed_sp=spd, stop_action="hold")
    mot2.run_to_rel_pos(position_sp=position, speed_sp=spd, stop_action="hold")

    time.sleep(position/spd)


def drive_robot(string_coord, s):
    global current_theta
    sequence = string_coord.split(' ')
    # current x and y positions of the robot's centre
    is_pass = False
    cc = 0
    while not is_pass:
        try:
            float(sequence[cc])
            is_pass = True
        except:
            cc+=1
    curr_x = float(sequence[0])
    curr_y = float(sequence[1])
    i = 2  # index of the sequence
    # assumption, initially the robot is at (0,0) and facing 90 degrees which is current_theta
    while i < len(sequence)-1:
        # desired x and y positions
        des_x = float(sequence[i])
        print(sequence[i])
        print(sequence[i + 1])
        des_y = float(sequence[i + 1])
        print(sequence[i + 1])
        # distance between the current position and the desired position, and it's in metres
        des_d = sqrt((des_x - curr_x) ** 2 + (des_y - curr_y) ** 2)
        # the angle the robot must rotate
        theta = atan2((des_y - curr_y), (des_x - curr_x))
        # call to rotate the robot by the difference of theta and current angle
        rotate_to_des_theta(theta, current_theta)
        # current angle the robot is facing after rotation
        current_theta = theta
        # after rotating for desired angle
        # we make the robot drive forward for the amount of distance
        move_forward(des_d / 100)  # divide by 100 to change the units from metres to cm
        sleep(0.3)
        # current coordinate the robot is at
        curr_x = des_x
        curr_y = des_y
        # its incremented by two because the i = x_coordinate and i+1 is y_coordinate
        i += 2
        s.send('test'.encode("UTF-8"))
        temp_mes = s.recv(1024).decode("UTF-8")  # receive the data from the serve
        print(temp_mes)
        if temp_mes == "pass":
            pass
        elif temp_mes == "stop":
            break


if __name__ == "__main__":
    host = socket.gethostname()
    port = 9999
    setup_client(host, port)


