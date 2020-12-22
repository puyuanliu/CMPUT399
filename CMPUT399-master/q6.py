#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev.ev3 import *
from time import sleep
from math import *

WHEEL_RADIUS = 5.5/2
LENGTH_BETWEEN_WHEELS = 11.8

motor_l = LargeMotor(OUTPUT_A) #A is the left motor 
motor_r = LargeMotor(OUTPUT_B) #B is the Right motor 

command = [[80,60,2], [60,60,1], [-50,80,2]]
xy_positions = [(0,0)]

initial_angle = 0

# move robot
for i in range (len(command)):
        wl = command[i][0]*10
        wr = command[i][1]*10
        time = command[i][2]
        
        motor_l.run_timed(speed_sp=wl, time_sp=time*1000000)
        motor_r.run_timed(speed_sp=wr, time_sp=time*1000000)
        sleep(time)
        
        # calculations
        vl = 2*pi*WHEEL_RADIUS*(wl/360)
        vr = 2*pi*WHEEL_RADIUS*(wr/360)
        v = (vr+vl)/2

        #print('ia',initial_angle)
        turn_angle = (vr-vl)/LENGTH_BETWEEN_WHEELS
        #print('ta',turn_angle)
        theta = (turn_angle*time)+initial_angle
        #print('theta',theta)
        #print()

        if wl == wr:
                x = v*cos(initial_angle)*time
                y = v*sin(initial_angle)*time
        else:
                x = (v/turn_angle)*sin(theta)
                y = -(v/turn_angle)*cos(theta)
                initial_angle = theta

        xy_positions.append((x,y))

x,y = 0,0
for a,b in (xy_positions):
        x+=a
        y+=b

print(xy_positions)
print(x,y)
print(initial_angle)
