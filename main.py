#!/usr/bin/env python3
# raspberry
import RPi.GPIO as GPIO
import move
from time import *

commands = move.Move()
commands.move_initial(commands.speeds["s25"], commands.speeds["s0"])
commands.move_initial2(commands.speeds["s25"], commands.speeds["s0"])
# program: serve wells A1-> A12 -> B12 -> B1
# go to well A1
commands.move_left(2, sum(commands.steps_stepper_2) - 16, commands.speeds["s50"])  # -16: drives to far.
commands.move_right(1, commands.steps_stepper_1[0], commands.speeds["s50"])
sleep(3)
for i in list(reversed(commands.steps_stepper_2))[:-1]:
    commands.move_right(2, i, commands.speeds["s50"])
    sleep(3)
commands.move_right(1, commands.steps_stepper_1[1], commands.speeds["s50"])
sleep(3)
for i in commands.steps_stepper_2[1:]:
    commands.move_left(2, i, commands.speeds["s50"])
    sleep(3)
GPIO.cleanup()
