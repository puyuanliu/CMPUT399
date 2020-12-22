#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev.ev3 import *
from time import sleep
from math import pi

motor_l = LargeMotor(OUTPUT_A) #A is the left motor 
motor_r = LargeMotor(OUTPUT_B) #B is the Right motor 

WHEEL_RADIUS = 5.5/2
LENGTH_BETWEEN_WHEELS = 11.8
TURN_ANGLE = pi/2
TURN_DURATION = 4
CIRCLE_RADIUS = 0

wr_minus_wl = TURN_ANGLE*LENGTH_BETWEEN_WHEELS/WHEEL_RADIUS

wr_plus_wl = CIRCLE_RADIUS*wr_minus_wl/(LENGTH_BETWEEN_WHEELS/2)

wl = (wr_plus_wl - wr_minus_wl)/2
wr= wr_plus_wl - wl

wl_in_deg = ((wr_plus_wl - wr_minus_wl)/2)*(180/pi)
wr_in_deg = (wr_plus_wl - wl)*(180/pi)

print(wl,wr)
print(wl_in_deg,wr_in_deg)

"""
for i in range (3):
	motor_l.run_timed(speed_sp=90, time_sp=4000000, stop_action='brake')
	motor_r.run_timed(speed_sp=90, time_sp=4000000, stop_action='brake')
	sleep(4000000)	
	
	motor_l.run_timed(speed_sp=wl_in_deg/TURN_DURATION, time_sp=TURN_DURATION*1000000, stop_action='brake')
	motor_r.run_timed(speed_sp=wr_in_deg/TURN_DURATION, time_sp=TURN_DURATION*1000000, stop_action='brake')
	sleep(TURN_DURATION)
	
	motor_l.run_timed(speed_sp=90, time_sp=2000000, stop_action='brake')
	motor_r.run_timed(speed_sp=90, time_sp=2000000, stop_action='brake')
	sleep(2000000)	
	
	motor_l.run_timed(speed_sp=wr_in_deg/TURN_DURATION, time_sp=TURN_DURATION*1000000, stop_action='brake')
	motor_r.run_timed(speed_sp=wl_in_deg/TURN_DURATION, time_sp=TURN_DURATION*1000000, stop_action='brake')
	sleep(TURN_DURATION)
	
	motor_l.run_timed(speed_sp=90, time_sp=4000000, stop_action='brake')
	motor_r.run_timed(speed_sp=90, time_sp=4000000, stop_action='brake')
	sleep(4000000)	
	
	motor_l.run_timed(speed_sp=wl_in_deg/TURN_DURATION, time_sp=TURN_DURATION*1000000, stop_action='brake')
	motor_r.run_timed(speed_sp=wr_in_deg/TURN_DURATION, time_sp=TURN_DURATION*1000000, stop_action='brake')
	sleep(TURN_DURATION)
	
	motor_l.run_timed(speed_sp=90, time_sp=2000000, stop_action='brake')
	motor_r.run_timed(speed_sp=90, time_sp=2000000, stop_action='brake')
	sleep(2000000)	
	
	motor_l.run_timed(speed_sp=wr_in_deg/TURN_DURATION, time_sp=TURN_DURATION*1000000, stop_action='brake')
	motor_r.run_timed(speed_sp=wl_in_deg/TURN_DURATION, time_sp=TURN_DURATION*1000000, stop_action='brake')
	sleep(TURN_DURATION)	
"""
