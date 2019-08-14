#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from enum import IntEnum


RESET = 0
STARTED = 1
STOPPED = 2


class Countdown:
    def __init__(self, pin):
        self.state = RESET;
        GPIO.setup(pin, GPIO.OUT)

    def pulse(self):
        GPIO.output(12, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(12, GPIO.HIGH)

        if self.state == RESET:
            self.state = STARTED
            
        elif self.state == STARTED:
            self.state = STOPPED
            
        elif self.state == STOPPED:
            self.state = RESET
            time.sleep(0.01)
            GPIO.output(12, GPIO.LOW)
            time.sleep(0.03)
            GPIO.output(12, GPIO.HIGH)


    def go_to(self, new_state):
        while self.state != new_state:
            self.pulse()

    def reset(self):
        self.go_to(RESET)

    def start(self):
        self.go_to(STARTED)

    def stop(self):
        self.go_to(STOPPED)
