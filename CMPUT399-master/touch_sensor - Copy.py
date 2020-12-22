#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File name: touch_sensor.py
Author: Laura Petrich
Date created: 04/09/18
Python Version: 3.5
Description: Demo program for CMPUT 399.
Use EV3 touch sensor to control led color with sound effects
"""

from ev3dev.ev3 import *

ts = TouchSensor()
leds = Leds()

print("Press the touch sensor to change the LED color!")

while True:
    if ts.is_pressed:
        Sound.speak('Touch sensor activated!')
        for led in (Leds.LEFT, Leds.RIGHT):
            Leds.set_color(led, Leds.GREEN)  