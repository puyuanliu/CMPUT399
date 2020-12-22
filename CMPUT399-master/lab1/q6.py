#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev.ev3 import *
from time import sleep
from math import *




WHEEL_RADIUS = 2.77
LENGTH_BETWEEN_WHEELS = 11.95

motor_l = LargeMotor(OUTPUT_A) #A is the left motor 
motor_r = LargeMotor(OUTPUT_B) #B is the Right motor 

#command = [[80,60,2], [60,60,1], [-50,80,2]]
command = [[60,10,4]]
last_angle = 0
x=0; y=0;

for i in range(len(command)):
    wl = command[i][0]*10
    wr = command[i][1]*10
    t = command[i][2]
    
    motor_l.run_timed(speed_sp=wl, time_sp=t*1000)
    motor_r.run_timed(speed_sp=wr, time_sp=t*1000)
    sleep(t)
    #motor_l.stop(stop_action='hold')
    #motor_r.stop(stop_action='hold')    
    

    wr = wr*pi/180
    wl = wl*pi/180
    
    
    v = (wr+wl)*WHEEL_RADIUS/2
    
    if wr == wl:
        x += v*t*cos(last_angle)
        y += v*t*sin(last_angle)

    else:
        omega = (wr-wl)*WHEEL_RADIUS/LENGTH_BETWEEN_WHEELS
        x += (v*sin(omega*t+last_angle)-v*sin(last_angle))/omega
        y += (-v*cos(omega*t+last_angle)+v*cos(last_angle))/omega
        last_angle += omega*t
    
    print("x,y:",x,y)
    print("ori:",last_angle%(2*pi),"rad", (last_angle*180/pi)%360,"deg")
    print()

motor_l.stop(stop_action='hold')
motor_r.stop(stop_action='hold') 

