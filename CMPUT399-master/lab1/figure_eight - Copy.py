#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev.ev3 import *
from time import sleep
from math import pi

motor_l = LargeMotor(OUTPUT_A) #A is the left motor 
motor_r = LargeMotor(OUTPUT_B) #B is the Right motor 

WHEEL_RADIUS = 2.77
LENGTH_BETWEEN_WHEELS = 11.95
TURN_ANGLE = 2*pi
TURN_DURATION = 5
CIRCLE_RADIUS = 15

wr_minus_wl = TURN_ANGLE*LENGTH_BETWEEN_WHEELS/WHEEL_RADIUS

wr_plus_wl = CIRCLE_RADIUS*wr_minus_wl/(LENGTH_BETWEEN_WHEELS/2)

wl = (wr_plus_wl - wr_minus_wl)/2
wr= wr_plus_wl - wl

wl_in_deg = wl*(180/pi)
wr_in_deg = wr*(180/pi)

print(wl,wr)
print(wl_in_deg,wr_in_deg)


for i in range (3):
	motor_l.run_timed(speed_sp=wl_in_deg/TURN_DURATION, time_sp=(TURN_DURATION+0.18)*1000)
	motor_r.run_timed(speed_sp=wr_in_deg/TURN_DURATION, time_sp=(TURN_DURATION+0.18)*1000)
	sleep(TURN_DURATION+0.18)
	motor_l.run_timed(speed_sp=wr_in_deg/TURN_DURATION, time_sp=(TURN_DURATION+0.30)*1000)
	motor_r.run_timed(speed_sp=wl_in_deg/TURN_DURATION, time_sp=(TURN_DURATION+0.30)*1000)
	sleep(TURN_DURATION+0.30)

motor_l.stop(stop_action='hold')
motor_r.stop(stop_action='hold')
