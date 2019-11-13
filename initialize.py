#!/usr/bin/env python3
# raspberry
import RPi.GPIO as GPIO
import datetime


class Initialize(object):
    """This class initializes the fraction collector and resets it to position
     0/0 on the x/y grids coordinate system. """
    def __init__(self):
        # callable variables used in this Method
        self.out_pins = []
        self.in_pins = []
        self.mask_dl = []
        self.mask_dr = []
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

        # define end switch pins as inputs
        GPIO.setup(self.pins_stepper1["stop_1"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins_stepper2["stop_2"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # gather in and out pins in two variables
        for key in sorted(self.pins_stepper1.keys()):  # included the 'sorted' function to make sure that
            # out_pins is in the correct order
            value = self.pins_stepper1[key]
            gpio_function = GPIO.gpio_function(value)
            if gpio_function == 1:
                self.in_pins.append(value)
            elif gpio_function == 0:
                self.out_pins.append(value)
            else:
                print("Pin with number {} is not defined.".format(value))

        for key in sorted(self.pins_stepper2.keys()):
            value = self.pins_stepper2[key]
            gpio_function = GPIO.gpio_function(value)
            if gpio_function == 1:
                self.in_pins.append(value)
            elif gpio_function == 0:
                self.out_pins.append(value)
            else:
                print("Pin with number {} is not defined.".format(value))

        print("out pins: {}, in pins: {}".format(self.out_pins, self.in_pins))

        # define pattern for each step of the steppers
        patterns = [[1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1], [0, 1, 1, 0]]
        # turn stepper in direction "left"
        self.mask_dl = patterns[0:4]
        # turn stepper in direction "right"
        self.mask_dr = list(reversed(patterns[0:4]))
        # add 'global' statement to access stop_xA before function _stop_move was called.
        global stop_xA, stop_yB
        stop_xA = 0
        stop_yB = 0

        def _stop_move_xA(stop):
            print("{:%d. %b. %Y, %H:%M:%S }".format(datetime.datetime.now()))  # introducing this line of code solves
            # the problem of this function always running into stop_xA = 0 with subsequent malfunction of dependant
            # code after the first successful iteration.
            # https://raspberrypi.stackexchange.com/questions/14105/how-does-python-gpio-bouncetime-parameter-work
            global stop_xA
            if GPIO.input(stop) == 0:  # end switch pressed
                stop_xA = 1
                print("End switch A pressed.")
            else:  # end switch released or not pressed
                stop_xA = 0
                print("End switch A released.")

        def _stop_move_yB(stop):
            print("{:%d. %b. %Y, %H:%M:%S }".format(datetime.datetime.now()))
            global stop_yB
            if GPIO.input(stop) == 0:  # end switch pressed
                stop_yB = 1
                print("End switch B pressed.")
            else:  # end switch released or not pressed
                stop_yB = 0
                print("End switch B released.")

        GPIO.add_event_detect(self.pins_stepper1["stop_1"],
                              GPIO.BOTH,
                              callback=_stop_move_xA,
                              bouncetime=200)
        GPIO.add_event_detect(self.pins_stepper2["stop_2"],
                              GPIO.BOTH,
                              callback=_stop_move_yB,
                              bouncetime=200)