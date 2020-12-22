#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev.ev3 import *
from time import sleep
from math import pi

motor_l = LargeMotor(OUTPUT_A) #A is the left motor 
motor_r = LargeMotor(OUTPUT_B) #B is the Right motor 

# 90 deg turn variables
WHEEL_RADIUS = 2.77
LENGTH_BETWEEN_WHEELS = 11.95
TURN_ANGLE = pi/2
TURN_DURATION = 2
CIRCLE_RADIUS = 0

# straight static variables
SIDE = 10
STRAIGHT_TIME = 2
STRAIGHT_DISTANCE = 10

wr_minus_wl = TURN_ANGLE*LENGTH_BETWEEN_WHEELS/WHEEL_RADIUS

wr_plus_wl = CIRCLE_RADIUS*wr_minus_wl/(LENGTH_BETWEEN_WHEELS/2)

wl = (wr_plus_wl - wr_minus_wl)/2
wr= wr_plus_wl - wl

wl_in_deg = wl*(180/pi)
wr_in_deg = wr*(180/pi)

# V = Ωr, Ω = V/r, V*dura = SIDE, dura = SIDE/V = SIDE/(Ωr)
straight_speed = (10/WHEEL_RADIUS)*(180/pi)


for i in range (4):
	motor_l.run_timed(speed_sp = 100, time_sp = STRAIGHT_TIME*1000)
	motor_r.run_timed(speed_sp = 100, time_sp = STRAIGHT_TIME*1000)
	sleep(STRAIGHT_TIME)

	motor_l.run_timed(speed_sp=wl_in_deg/TURN_DURATION, time_sp=(TURN_DURATION)*1000)
	motor_r.run_timed(speed_sp=wr_in_deg/TURN_DURATION, time_sp=(TURN_DURATION)*1000)
	sleep(TURN_DURATION)

motor_l.stop(stop_action='hold')
motor_r.stop(stop_action='hold')
