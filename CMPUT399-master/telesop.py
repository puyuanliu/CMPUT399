#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File name: teleop.py
Author: Laura Petrich
Date created: 04/09/18
Python Version: 3.5
Description: Demo program for CMPUT 399.
Run in terminal connected to EV3 brick by ssh.
Use laptop keys to control led color.
"""

from time import sleep
from ev3dev.ev3 import *

button = Button()
Leds.all_off()

while not button.any():
    key = input("Please enter a color:")
    led_color = key[0].lower()
    for led in (Leds.LEFT, Leds.RIGHT):
        if led_color == 'g':
            Leds.set_color(led, Leds.GREEN)
        elif led_color == 'r':
            Leds.set_color(led, Leds.RED)
        elif led_color == 'a':
            Leds.set_color(led, Leds.AMBER)
        elif led_color == 'y':
            Leds.set_color(led, Leds.YELLOW)
        elif led_color == 'o':
            Leds.set_color(led, Leds.ORANGE)
        elif led_color == 'b':
            Leds.set_color(led, Leds.BLACK)
        else:
            Leds.all_off()
    sleep(0.01)
