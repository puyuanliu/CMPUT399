#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep
from ev3dev.ev3 import *
motor = LargeMotor(OUTPUT_A)
assert motor.connected

button = Button()
Leds.all_off()

while True:
    if button.any():
        Sound.speak('I am a robot!')
        motor.run_timed(speed_sp=-600, time_sp=500)
        for led in (Leds.LEFT, Leds.RIGHT):
            Leds.set_color(led, Leds.RED)
    else:
        motor.stop(stop_action='brake')
    sleep(0.01)
