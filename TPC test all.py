#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from buttons import Buttons, Optos
from lights import Lights, Outlets
from sounds import Sounds
from countdown import Countdown

GPIO.setmode(GPIO.BCM)

buttons = Buttons()
optos = Optos()
lights = Lights()
outlets = Outlets()
sounds = Sounds()

def check_buttons():
    global buttons, optos
    
    x = buttons.all_pressed()
    if x:
        print(x)

    x = optos.all_broken()
    if x:
        print(x)

lights.turn_off_all()
outlets.turn_off_all()

print("Starting countdown")
countdown = Countdown(12)
countdown.start()
time.sleep(3)
countdown.stop()
time.sleep(2)
countdown.reset()
time.sleep(3)
print("Done")

# Sleep time variables
sleeptime = 0.1

# MAIN LOOP =====
# ===============

try:
    for i in range (0,5):
        countdown.start()
        for j in range (0,1):
            outlets.turn_on_all()

            for i in lights.all():
                lights.turn_on_only(i)
                time.sleep(sleeptime)
                lights.turn_off(i)
                check_buttons();

            outlets.turn_off_all()

            for i in reversed(lights.all()):
                lights.turn_on_only(i)
                time.sleep(sleeptime)
                lights.turn_off(i)
                check_buttons();

            for i in outlets.all():
                outlets.turn_on_only(i)
                time.sleep(sleeptime)

        sleeptime *= (1/.9)
        countdown.reset()
        time.sleep(3)

    lights.turn_off_all()
    outlets.turn_off_all()
        
    countdown.reset()
# End program cleanly with keyboard
except KeyboardInterrupt:
    print(" Quit")

    # Reset GPIO settings

    countdown.reset()
    GPIO.cleanup()
