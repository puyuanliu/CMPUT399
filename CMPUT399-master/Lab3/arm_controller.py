from ev3dev.ev3 import *
from math import *
import numpy as np
from time import sleep


class ArmController():

    #Static Variables
    #We neeed these variables shared across all instances (if any) of this class
    driver_gear_teeth = 24
    follower_gear_teeth= 56
    #How many rotiations does the driver gear has to do for a full rotation of
    #the follower gear.
    gear_ratio = follower_gear_teeth/driver_gear_teeth

    #In centimeters
    link_1_length = 8.5 #8.5
    link_2_length = 13.5 #13.4

    base_motor = LargeMotor(OUTPUT_A)
    joint_motor = LargeMotor(OUTPUT_B)
    #End of Static Variables

    def __init__(self):
        self.base_ArmController.base_motornitial = ArmController.base_motor.position
        self.joint_ArmController.base_motornitial = ArmController.joint_motor.position
        self.initial = True
        self.r_1 = ArmController.link_1_length
        self.r_2 = ArmController.link_2_length
        self.eps = 2 * 10e-7
        self.current_x = 0
        self.current_y = 0
        self.step_angle_degree = 3
        self.step_angle = pi*(self.step_angle_degree/180)  #angle movement for every step
        self.current_theta_1 = 0
        self.current_theta_2 = 0
        self.ultrasonic1 = UltrasonicSensor(INPUT_2)
        self.ultrasonic2 = UltrasonicSensor(INPUT_3)

    # Input: base_rotation_angle [int]. The angle (in degrees) by which we want the base to rotate
    # Output: [int]. The number of ticks that the base motor has to move in order
    #   to rotate the base by the desired base_rotation_angle. The sign indicates the direction
    #   in which the base motor will move (positive is clockwise).
    # Note: The direction of movement of the base motor is opposite
    #   to the direction in which the base is rotating.
    def get_base_motor_ticks(self,base_rotation_angle):
        return base_rotation_angle*ArmController.gear_ratio*-1

    #Input: base_motor_ticks [int]. The number of ticks that we want the base motor to move
    # Output: [int]. The angle (in degrees) by which the base is going to rotate after the base motor has
    #   moved the desired number of ticks. The sign indicates direction
    #   in which the base will rotate (positive is clockwise)
    # Note: The direction of movement of the base motor is opposite
    #   to the direction in which the base is rotating.
    def get_base_rotation_angle(self,base_motor_ticks):
        return base_motor_ticks/ArmController.gear_ratio*-1

    def degrees_to_radians(self,angle_in_degrees):
        return (angle_in_degrees*pi)/180

    def radians_to_degrees(self,angle_in_radians):
        return (angle_in_radians*180)/pi

    #Input: angle [int]. The angle (in degrees) which we want the base to rotate
    def rotate_base(self,angle):
        # The angular speed for a rotation of the base is going to be 180 degrees/second.
        # In here we have to take into account the gear system that drives the base
        # and perform the appropriate conversions to make sure that the base motor rotates the base
        # at the desired angular speed (180 degrees/second) to the given angle
        ArmController.base_motor.run_to_rel_pos(position_sp=self.get_base_motor_ticks(angle), speed_sp=self.get_base_motor_ticks(180)*0.3, stop_action="hold")

    # Input: angle [int]. The (angle in degrees) which we want the joint to rotate
    def rotate_joint(self,angle):
        # The angular speed for a rotation of the joint is going to be 180 degrees/second
        ArmController.joint_motor.run_to_rel_pos(position_sp=angle, speed_sp=180*0.5, stop_action="hold")

    def __get_base_motor_position(self):
        return ArmController.base_motor.position - self.base_ArmController.base_motornitial

    def __get_joint_motor_position(self):
        return ArmController.joint_motor.position - self.joint_ArmController.base_motornitial

    def get_x(self):
        # This function return the current x
        base_angle = self.get_base_rotation_angle(self.__get_base_motor_position())
        joint_angle = self.__get_joint_motor_position()
        return ArmController.link_1_length*cos(self.degrees_to_radians(base_angle)) + ArmController.link_2_length*cos(self.degrees_to_radians(joint_angle + base_angle))

    def get_y(self):
        # This function returns the currenty
        base_angle = self.get_base_rotation_angle(self.__get_base_motor_position())
        joint_angle = self.__get_joint_motor_position()
        return ArmController.link_1_length*sin(self.degrees_to_radians(base_angle)) + ArmController.link_2_length*sin(self.degrees_to_radians(joint_angle + base_angle))

    def stop_motors(self):
        # This function stop all motors
        ArmController.joint_motor.stop()
        ArmController.base_motor.stop()

    def avoid_obstacle(self):
        # This function helps avoid the obstacles
        self.calibration() # initialize the angle

        limit_value = 7
        while not Button().any():
            self.ultrasonic1_read = self.ultrasonic1.distance_centimeters
            [current_i, current_o] = self.arm_angle_get()
            # print(current_i)

            if (self.ultrasonic1_read < limit_value):
                self.aviod_forward()

            if (current_i < 180):
                ArmController.base_motor.run_timed(speed_sp=-100, time_sp=1000)
            else:
                self.move(ArmController.joint_motor, 0)
                self.backup()
        ArmController.joint_motor.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
        ArmController.base_motor.run_timed(time_sp=30, speed_sp=0, stop_action='coast')

    # This function calibrates the current motor angle to [0,0] respectically

    def calibration(self):
        ArmController.base_motor.position.position = 0
        ArmController.joint_motor.position = 0

    # The program will detect the obstacle when moving the arms towards its destionation
    # limit value: the distance that will activate the avoid_forward subprogram, it is set to 7cms.
    # ultrasonic_read: current reading value of the ultrasonic sensor
    # this is the recursively called function that respect to (opposite to) forwardgoing(), it moves the base(inner) motor to the original position
    def backup(self):
        while not Button().any():
            limit_value = 7
            self.ultrasonic2_read = self.ultrasonic2.distance_centimeters
            [current_i, current_o] = self.arm_angle_get()
            # print(current_i)

            if (self.ultrasonic2_read < limit_value):
                self.avoid_backward()

            if (current_i > 0):
                ArmController.base_motor.run_timed(speed_sp=100, time_sp=1000)
            else:
                # move(ArmController.base_motor, 0, GEARRATIO)
                # move(ArmController.joint_motor, 0)
                self.move(ArmController.joint_motor, 0)
                forwardgoing()

        ArmController.joint_motor.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
        ArmController.base_motor.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
        
# The program will detect the obstacle when moving the arms towards its destination
# limit value: the distance that will activate the avoid_forward subprogram, it is set to 7cms.
# ultrasonic_read: current reading value of the ultrasonic sensor
def forwardgoing():
    while not button.any():
        limit_value = 7 
        ultrasonic1_read = ultrasonic1.distance_centimeters
        [current_i,current_o] = arm_angle_get()
        #print(current_i)

        if (ultrasonic1_read < limit_value):
            avoid_forward()

        if (current_i < 180):
            motor_i.run_timed(speed_sp=-100, time_sp=1000)
        else:
            #move(motor_i, 0, GEARRATIO)
            #move(motor_o, 0)
            move(motor_o, 0)
            backup()
    motor_o.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
    motor_i.run_timed(time_sp=30, speed_sp=0, stop_action='coast')


    # this function poses the action of avoiding the obstacles when moving from (-maxium,0) to (maxium,0)
    # it stops the inner motor and move the outer motor backwards to avoid the obstacles
    def avoid_backward(self):
        ArmController.joint_motor.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
        ArmController.base_motor.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
        while not Button().any():
            [current_i, current_o] = self.arm_angle_get()
            if (current_o < 150):
                ArmController.joint_motor.run_timed(speed_sp=400, time_sp=10)
            else:
                break

    # This function get the current actual angle of the two arms after considering the Gear-transformations
    # Return: [current_i,current_o]
    # return value is in the format of [current_i,current_o] which cooresponds to the angle of inner and outer motor
    def arm_angle_get(self):
        # ArmController.base_motor = LargeMotor(OUTPUT_A)
        # ArmController.joint_motor = LargeMotor(OUTPUT_B)
        current_i = ArmController.base_motor.position
        current_o = ArmController.joint_motor.position
        current_i = -current_i / GEARRATIO
        return [current_i, current_o]

    # This program moves a motor to a specific angle using PID
    # Applys to motor with/without gears
    # Args: motor,setpoint(deg), gearratio
    def move(self, motor, setpoint, gearratio=0):
        if gearratio != 0:
            setpoint = -setpoint * gearratio

        # initialize default values
        previous_error = 0
        integral = 0
        # initialize Kp,Ki,Kd,dt
        Kp = 3.5;
        Ki = 0;
        Kd = 0
        dt = 0.1
        while True:
            pos = motor.position
            error = setpoint - pos
            # exit while loop if error within tolerance
            if abs(error) <= 15:
                motor.stop(stop_action='hold')
                motor.stop(stop_action='coast')
                break

            integral += error * dt
            derivative = (error - previous_error) / dt
            output = Kp * error + Ki * integral + Kd * derivative

            # contraint output to motor maximum caoacity
            if output > 999:
                output = 999
            elif output < -999:
                output = -999
            # print('output',output)
            previous_error = error
            # print(error)
            if (output <= 30) and (output >= -30):
                output = output * 5
            motor.run_timed(speed_sp=output, time_sp=dt * 1000)
            sleep(dt)
        return motor.position

