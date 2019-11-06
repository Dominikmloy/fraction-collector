#raspberry
#!/usr/bin/python
import os
import sys
import RPi.GPIO as GPIO
from time import *
import initialize as ini
# import threading # this module is going to be used in future versions to enable the simultaneous addressing
# of pumps and steppers.

# initialize components and wiring
system = ini.Initialize()
step_counter_stepper_1 = 0
step_counter_stepper_2 = 0
total_sub_steps = len(system.mask_dl)
# this function could be improved by using threading and running both steppers in parallel


def move_initial(speed_1, speed_2):
    try:
        # drive first stepper until end switch is pressed.
        count_sub_steps = 0  # one step consists of four sub-steps
        while not ini.stop_xA:
            for pin in range(len(system.mask_dl)):  # elements in mask_dl
                pin_id = system.out_pins[pin]  # assign out pins
                if system.mask_dl[count_sub_steps][pin] != 0:
                    GPIO.output(pin_id, True)
                else:
                    GPIO.output(pin_id, False)
            count_sub_steps += 1
            if count_sub_steps >= total_sub_steps:  # one step was completed
                count_sub_steps = 0
            sleep(speed_1)
        sleep(0.5)
        # drive first stepper until end switch is released.
        # This position is defined as 0 - position.
        count_sub_steps = 0
        while ini.stop_xA:
            for pin in range(len(system.mask_dr)):  # elements in mask_dr
                pin_id = system.out_pins[pin]  # assign out pins
                if system.mask_dr[count_sub_steps][pin] != 0:
                    GPIO.output(pin_id, True)
                else:
                    GPIO.output(pin_id, False)
            count_sub_steps += 1
            if count_sub_steps >= total_sub_steps:  # one step was completed
                count_sub_steps = 0
            sleep(speed_2)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("x")
        return False


move_initial(system.speeds["s25"], system.speeds["s0"])
GPIO.cleanup()
#todo: ticks = 0

