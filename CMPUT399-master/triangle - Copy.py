#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev.ev3 import *
from time import sleep
#from math import pi
motor1 = LargeMotor(OUTPUT_A) #A is the left motor 
motor2 = LargeMotor(OUTPUT_B) #B is the Right motor 
count = 0

#w = (pi/2) * (6/2.75)
#v = w * (180/pi)

while count < 3:
	motor1.run_timed(speed_sp=600, time_sp=1500000)
	motor2.run_timed(speed_sp=600, time_sp=1500000)
	sleep(1.2)
	motor1.run_timed(speed_sp=-272, time_sp=1000000)
	motor2.run_timed(speed_sp=272, time_sp=1000000)
	sleep(1)
	count += 1
motor1.stop(stop_action="hold")
motor2.stop(stop_action="hold")