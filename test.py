import RPi.GPIO as GPIO
from time import *
import initialize as ini

system = ini.Initialize()
try:
    while True:
        print("A: ", ini.stop_xA)
        print("B: ", ini.stop_yB)
        sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nBye")
