#!/usr/bin/env python3
# raspberry
import RPi.GPIO as GPIO
from time import *
import initialize as ini


class Move(object):
    """
    Holds all the commands and attributes to move both steppers. Move_initial and move_initial2 move
    both steppers to position 0/0 on the x/y grids coordinate system. move_left means that the stepper
    is turning left. The carriage, however, is moving right due to the positioning of the steppers.
    Same is true for move_right.
    """
    def __init__(self):
        # initialize components and wiring
        # global step counter to know the exact position of the dispenser head
        global step_counter_stepper_1
        global step_counter_stepper_2
        # speeds: 0.3 sec is very slow -> no stepping errors
        # 0.002 sec is possible without errors
        self.speeds = {"s100": 0.005, "s75": 0.01, "s50": 0.025, "s25": 0.05, "s0": 0.1}
        # Instantiate the class 'Initialize' from 'initialize.py' to enable access to its functions
        # and to set up the mapping of the GPIO pins to the steppers and end switches.
        self.system = ini.Initialize()
        step_counter_stepper_1 = 0
        self.maximum_steps_stepper_1 = 260  # dependent on the fraction collectors dimensions
        step_counter_stepper_2 = 0
        self.maximum_steps_stepper_2 = 340  # dependent on the fraction collectors dimensions
        self.total_sub_steps = len(self.system.mask_dl)
        # steps for a 96 well plate. These steps were found empirically, that's why the steps between wells
        # are different from each other. They compensate the offset of steps to the well plate's dimensions.
        self.steps_stepper_1 = [43, 28, 27, 27, 28, 27, 28, 28]  # steps from positions zero to wells A - H.
        self.steps_stepper_2 = [35, 28, 27, 27, 28, 27, 28, 27, 27, 28, 27, 28]  # steps from pos. 0 to wells 12 - 1.

    def move_initial(self, speed_1, speed_2):  # Could be improved by using threading and
        # running both steppers in parallel.
        """
        Calling this function moves stepper one to the starting position and resets
        step_counter_stepper_1 to 0.
        """
        try:
            # drive first stepper until end switch is pressed.
            count_sub_steps = 0  # one step consists of four sub-steps
            while not ini.stop_xA:
                for pin in range(len(self.system.mask_dl)):  # elements in mask_dl
                    pin_id = self.system.out_pins[pin]  # assign out pins
                    if self.system.mask_dl[count_sub_steps][pin] != 0:
                        GPIO.output(pin_id, True)
                    else:
                        GPIO.output(pin_id, False)
                count_sub_steps += 1
                if count_sub_steps >= self.total_sub_steps:  # one step was completed
                    count_sub_steps = 0

                sleep(speed_1)
            sleep(0.5)
            # drive first stepper until end switch is released.
            # This position is defined as 0 - position.
            count_sub_steps = 0
            while ini.stop_xA:
                for pin in range(len(self.system.mask_dr)):  # elements in mask_dr
                    pin_id = self.system.out_pins[pin]  # assign out pins
                    if self.system.mask_dr[count_sub_steps][pin] != 0:
                        GPIO.output(pin_id, True)
                    else:
                        GPIO.output(pin_id, False)
                count_sub_steps += 1
                if count_sub_steps >= self.total_sub_steps:  # one step was completed
                    count_sub_steps = 0

                sleep(speed_2)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("x")
            return False
        global step_counter_stepper_1
        step_counter_stepper_1 = 0
        # the next three lines of code set the output of all pins to 0, probably slowing down
        # or preventing the heating of the motor drivers.
        for pin in range(len(self.system.mask_dl)):  # elements in mask_dl
            pin_id = self.system.out_pins[pin]
            GPIO.output(pin_id, False)

    def move_initial2(self, speed_1, speed_2):
        """Calling this function moves stepper two to the starting position and resets
            step_counter_stepper_2 to 0. """
        try:
            # drive first stepper until end switch is pressed.
            count_sub_steps = 0  # one step consists of four sub-steps
            while not ini.stop_yB:
                for pin in range(len(self.system.mask_dr)):  # elements in mask_dl
                    pin_id = self.system.out_pins[pin + 4]  # assign out pins.
                    # +4: because first 4 pins belong to stepper 1
                    if self.system.mask_dr[count_sub_steps][pin] != 0:
                        GPIO.output(pin_id, True)
                    else:
                        GPIO.output(pin_id, False)
                count_sub_steps += 1
                if count_sub_steps >= self.total_sub_steps:  # one step was completed
                    count_sub_steps = 0

                sleep(speed_1)
            sleep(0.5)
            # drive first stepper until end switch is released.
            # This position is defined as 0 - position.
            count_sub_steps = 0
            while ini.stop_yB:
                for pin in range(len(self.system.mask_dl)):  # elements in mask_dr
                    pin_id = self.system.out_pins[pin + 4]  # assign out pins.
                    # +4: because first 4 pins belong to stepper 1
                    if self.system.mask_dl[count_sub_steps][pin] != 0:
                        GPIO.output(pin_id, True)
                    else:
                        GPIO.output(pin_id, False)
                count_sub_steps += 1
                if count_sub_steps >= self.total_sub_steps:  # one step was completed
                    count_sub_steps = 0

                sleep(speed_2)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("x")
            return False
        global step_counter_stepper_2
        step_counter_stepper_2 = 0
        # the next three lines of code set the output of all pins to 0, probably slowing down
        # or preventing the heating of the motor drivers.
        for pin in range(len(self.system.mask_dr)):
            pin_id = self.system.out_pins[pin]
            GPIO.output(pin_id, False)

    def move_left(self, stepper, steps, speed):
        """
        This function moves target stepper (1 or 2) the target number of steps to the left (clockwise).
        Speed variable is taken from initialize.py. Steps taken are added to the step counter.
        If the step threshold is crossed, a warning is printed and the program aborts.
        """
        # check if maximum number of steps is exceeded
        if stepper == 1:
            global step_counter_stepper_1
            total_steps = step_counter_stepper_1 - steps
            if total_steps <= 0:
                steps_remaining = step_counter_stepper_1
                print("Steps ({}) exceed number of remaining steps ({}). Program aborted.".format(steps,
                                                                                                  steps_remaining))
                return
            else:
                step_counter_stepper_1 -= steps
        elif stepper == 2:
            global step_counter_stepper_2
            total_steps = step_counter_stepper_2 + steps
            if total_steps >= self.maximum_steps_stepper_2:
                steps_remaining = self.maximum_steps_stepper_2 - step_counter_stepper_2
                print("Steps ({}) exceed number of remaining steps ({}). Program aborted.".format(steps,
                                                                                                  steps_remaining))
                return
            else:
                step_counter_stepper_2 += steps
        else:
            print("Argument '{}' for 'stepper' invalid. Please use '1' or '2'".format(stepper))
            return
        # move stepper target steps to the left.
        try:
            count_sub_steps = 0
            for i in range(0, steps):
                for pin in range(len(self.system.mask_dl)):
                    if stepper == 1:
                        pin_id = self.system.out_pins[pin]
                        if self.system.mask_dl[count_sub_steps][pin] != 0:
                            GPIO.output(pin_id, True)
                        else:
                            GPIO.output(pin_id, False)
                    elif stepper == 2:
                        pin_id = self.system.out_pins[pin + 4]
                        if self.system.mask_dl[count_sub_steps][pin] != 0:
                            GPIO.output(pin_id, True)
                        else:
                            GPIO.output(pin_id, False)
                    else:
                        print("Argument '{}' for 'stepper' invalid. Please use '1' or '2'".format(stepper))
                        return
                count_sub_steps += 1
                if count_sub_steps >= self.total_sub_steps:  # one step was completed
                    count_sub_steps = 0

                sleep(speed)
        except KeyboardInterrupt:
            GPIO.cleanup()
            return False
        # the next three lines of code set the output of all pins to 0, probably slowing down
        # or preventing the heating of the motor drivers.
        for pin in range(len(self.system.mask_dl)):
            pin_id = self.system.out_pins[pin]
            GPIO.output(pin_id, False)

    def move_right(self, stepper, steps, speed):
        """
        This function moves target stepper (1 or 2) the target number of steps to the right (counter-clockwise).
        Speed variable is taken from initialize.py. Steps taken are added to the step counter.
        If the step threshold is crossed, a warning is printed and the program aborts.
        """
        # check if maximum number of steps is exceeded
        if stepper == 1:
            global step_counter_stepper_1
            total_steps = step_counter_stepper_1 + steps
            if total_steps >= self.maximum_steps_stepper_1:
                steps_remaining = self.maximum_steps_stepper_1 - step_counter_stepper_1
                print("Steps ({}) exceed number of remaining steps ({}). Program aborted.".format(steps,
                                                                                                  steps_remaining))
                return
            else:
                step_counter_stepper_1 += steps
        elif stepper == 2:
            global step_counter_stepper_2
            total_steps = step_counter_stepper_2 - steps
            if total_steps <= 0:
                steps_remaining = step_counter_stepper_2
                print("Steps ({}) exceed number of remaining steps ({}). Program aborted.".format(steps,
                                                                                                  steps_remaining))
                return
            else:
                step_counter_stepper_2 -= steps
        else:
            print("Argument '{}' for 'stepper' invalid. Please use '1' or '2'".format(stepper))
            return
        # move stepper target steps to the left.
        try:
            count_sub_steps = 0
            for i in range(0, steps):
                for pin in range(len(self.system.mask_dr)):
                    if stepper == 1:
                        pin_id = self.system.out_pins[pin]
                        if self.system.mask_dr[count_sub_steps][pin] != 0:
                            GPIO.output(pin_id, True)
                        else:
                            GPIO.output(pin_id, False)
                    elif stepper == 2:
                        pin_id = self.system.out_pins[pin + 4]
                        if self.system.mask_dr[count_sub_steps][pin] != 0:
                            GPIO.output(pin_id, True)
                        else:
                            GPIO.output(pin_id, False)
                    else:
                        print("Argument '{}' for 'stepper' invalid. Please use '1' or '2'".format(stepper))
                        return
                count_sub_steps += 1
                if count_sub_steps >= self.total_sub_steps:  # one step was completed
                    count_sub_steps = 0

                sleep(speed)
        except KeyboardInterrupt:
            GPIO.cleanup()
            return False
        # the next three lines of code set the output of all pins to 0, probably slowing down
        # or preventing the heating of the motor drivers.
        for pin in range(len(self.system.mask_dr)):
            pin_id = self.system.out_pins[pin]
            GPIO.output(pin_id, False)
