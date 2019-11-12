#raspberry
#!/usr/bin/python
# import os
# import sys
import RPi.GPIO as GPIO
import move
from time import *

commands = move.Move()
commands.move_initial(commands.speeds["s25"], commands.speeds["s0"])
commands.move_initial2(commands.speeds["s25"], commands.speeds["s0"])
for i in commands.steps_stepper_1:
    commands.move_right(1, i, commands.speeds["s50"])
    sleep(5)
GPIO.cleanup()