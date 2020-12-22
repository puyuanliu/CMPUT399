#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#http://web.eecs.utk.edu/~mclennan/Classes/102/robot_labs/Lab5.html
from ev3dev.ev3 import *
from time import sleep

motor_l = LargeMotor(OUTPUT_A) #A is the left motor
motor_r = LargeMotor(OUTPUT_B) #B is the Right motor
lightsensor_l = LightSensor(INPUT_1)
lightsensor_r = LightSensor(INPUT_2)
ultrasonic = UltrasonicSensor(INPUT_3)
button = Button()

# for coward and aggressive
def normalize_1(v, ambient):
    if v <= ambient:
        return 0
    else:
        return (v-ambient)/(100-ambient)

# for coward and aggressive

def normalize_2(v, ambient):
    if v <= ambient:
        return 1
    else:
        return 1-((v-ambient)/(62-ambient))


def normalize_3(v, ambient):
    if v <= ambient:
        return 1
    else:
        return 1-((v-ambient)/(72-ambient))


def main():
    coward=False; aggressive=False; explorer=False; love=False;
    behavior = str(input("Please select a behavior:\n1 - coward\n2 - aggressive\n3 - love\n4 - explorer\n"))
    if behavior == "1":
        coward=True
    elif behavior == "2":
        aggressive=True
    elif behavior == "3":
        love=True
    elif behavior == "4":
        explorer=True
    else:
        print("Invalid input.")
    light_l = lightsensor_l.ambient_light_intensity
    light_r = lightsensor_r.ambient_light_intensity

    ambient = (light_l+light_r)/2

    #print(ambient)
    assert ambient < 100
    
    while not button.any():
        light_l = lightsensor_l.ambient_light_intensity
        #print(light_l,light_r)
        light_r = lightsensor_r.ambient_light_intensity
        front_dist = ultrasonic.distance_centimeters

        #print(front_dist)
        if front_dist < 10:
            'turnaround'
            motor_l.run_timed(speed_sp=388.26, time_sp=1000)
            motor_r.run_timed(speed_sp=-388.26, time_sp=1000)
            sleep(1)

        if coward:
            if light_l > 100:
                light_l = 100
            elif light_r > 100:
                light_r = 100
            elif light_l < 0:
                light_l = 0
            elif light_r < 0:
                light_r = 0
            motor_l.run_forever(speed_sp=normalize_1(light_l,ambient)*1000)
            motor_r.run_forever(speed_sp=normalize_1(light_r,ambient)*1000)
        
        elif aggressive:
            if light_l > 100:
                light_l = 100
            elif light_r > 100:
                light_r = 100
            elif light_l < 0:
                light_l = 0
            elif light_r < 0:
                light_r = 0
            motor_l.run_forever(speed_sp=normalize_1(light_r,ambient)*1000)
            motor_r.run_forever(speed_sp=normalize_1(light_l,ambient)*1000)
        
        elif explorer:
            if light_l > 72:
                light_l = 72
            elif light_r > 72:
                light_r = 72
            elif light_l < 0:
                light_l = 0
            elif light_r < 0:
                light_r = 0
            motor_l.run_forever(speed_sp=normalize_3(light_r,ambient)*500)
            motor_r.run_forever(speed_sp=normalize_3(light_l,ambient)*500)
    
        elif love:
            if light_l > 62:
                light_l = 62
            elif light_r > 62:
                light_r = 62
            elif light_l < 0:
                light_l = 0
            elif light_r < 0:
                light_r = 0
            motor_l.run_forever(speed_sp=normalize_2(light_l,ambient)*500)
            motor_r.run_forever(speed_sp=normalize_2(light_r,ambient)*500)
        else:
            break
        
            
if __name__ == "__main__":
    main()
