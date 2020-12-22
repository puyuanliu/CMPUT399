#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev.ev3 import *
from time import sleep

motor_l = LargeMotor(OUTPUT_A) #A is the left motor 
motor_r = LargeMotor(OUTPUT_B) #B is the Right motor 

# run both motors at same speed for 3 seconds
for i in range (3):
	motor_l.run_timed(speed_sp=600, time_sp=3000000)
	motor_r.run_timed(speed_sp=600, time_sp=3000000)
	sleep(3)
