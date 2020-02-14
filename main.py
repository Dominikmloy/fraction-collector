#!/usr/bin/env python3
# raspberry
import RPi.GPIO as GPIO
import move
from time import *


# Instantiate the class 'Move' from the module 'move.py' to enable access to functions and variables.
commands = move.Move()

# Move the dispenser head to its initial position x/y = 0/0.
commands.move_initial(commands.speeds["s25"], commands.speeds["s0"])
commands.move_initial2(commands.speeds["s25"], commands.speeds["s0"])

# program: serve wells from a 96 well plate: A1-> A12 -> B12 -> B1
# go to well A1
commands.move_left(2, sum(commands.steps_stepper_2) - 16, commands.speeds["s50"])  # -16: drives to far.
commands.move_right(1, commands.steps_stepper_1[0], commands.speeds["s50"])

# wait 3s (i.e. the time to collect your sample)
sleep(3)
# for-clause. Iterates over the elements of the list 'steps_stepper_2'
# and drives the target steps to the right (A1 -> A12)
for i in list(reversed(commands.steps_stepper_2))[:-1]:
    commands.move_right(2, i, commands.speeds["s50"])
    sleep(3)
# drives stepper 1 target steps to the right (A12 -> B12)
commands.move_right(1, commands.steps_stepper_1[1], commands.speeds["s50"])
sleep(3)
# drives stepper 2 target steps to the left (B12 -> B1)
for i in commands.steps_stepper_2[1:]:
    commands.move_left(2, i, commands.speeds["s50"])
    sleep(3)
# removes access to and any voltage from the GPIO pins.
GPIO.cleanup()
