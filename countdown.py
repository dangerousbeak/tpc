#!/usr/bin/python
import RPi.GPIO as GPIO
import time

class Countdown:
    def __init__(self, pin):
        self.state = 0;
        GPIO.setup(pin, GPIO.OUT)

    def pulse(self):
        GPIO.output(12, GPIO.LOW)
        time.sleep(0.04)
        GPIO.output(12, GPIO.HIGH)
        self.state = (self.state + 1) % 3

    def go_to(self, new_state):
        while self.state != new_state:
            self.pulse()
            if self.state == 0:
                time.sleep(0.08)
                GPIO.output(12, GPIO.LOW)
                time.sleep(0.04)
                GPIO.output(12, GPIO.HIGH)
    
    def reset(self):
        self.go_to(0)

    def start(self):
        self.go_to(1)

    def stop(self):
        self.go_to(2)
