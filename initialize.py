# raspberry
# !/usr/bin/python
import os
import sys
from time import *
import RPi.GPIO as GPIO


class Initialize(object):
    """This class initializes the fraction collector and resets it to position
     0/0 on the x/y grids coordinate system. """
    def __init__(self):
        # map pins to a stepper and end switch
        self.pins_stepper1 = {"A": 18, "B": 23, "C": 24, "D": 25, "stop_1": 27}
        self.pins_stepper2 = {"A": 5, "B": 6, "C": 13, "D": 26, "stop_2": 17}
        # define stepper pins as outputs and
        # set the output of the stepper pins to low (achieved using "False")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for item in self.pins_stepper1:
            if item in "ABCD":
                GPIO.setup(self.pins_stepper1[item], GPIO.OUT)  # defines as output
                GPIO.setup(self.pins_stepper1[item], False)     # set to low
        for item in self.pins_stepper2:
            if item in "ABCD":
                GPIO.setup(self.pins_stepper2[item], GPIO.OUT)  # defines as output
                GPIO.setup(self.pins_stepper2[item], False)     # set to low
        # define end switch pins as
        GPIO.setup(self.pins_stepper1["stop_1"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins_stepper2["stop_2"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # gather in and out pins in two variables
        self.out_pins = []
        self.in_pins = []
        for value in self.pins_stepper1.values():
            gpio_function = GPIO.gpio_function(value)
            if gpio_function == 1:
                self.in_pins.append(value)
            elif gpio_function == 0:
                self.out_pins.append(value)
            else:
                print("Pin with number {} is not defined.".format(value))
        for value in self.pins_stepper2.values():
            gpio_function = GPIO.gpio_function(value)
            if gpio_function == 1:
                self.in_pins.append(value)
            elif gpio_function == 0:
                self.out_pins.append(value)
            else:
                print("Pin with number {} is not defined.".format(value))
        print("out pins: {}, in pins: {}".format(self.out_pins, self.in_pins))

