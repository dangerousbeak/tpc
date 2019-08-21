#!/usr/bin/python
from enum import IntEnum
import RPi.GPIO as GPIO
import time


class SwitchedOutput(object):
    def __init__(self, gpios):
        #set these ports as output ports:
        self.GPIOlist = gpios
        for i in self.GPIOlist:
            GPIO.setup(i, GPIO.OUT)

        self.light_state = [ False for i in self.all() ]
        self.reset()

    def on_value(self, i):
      return GPIO.LOW

    def off_value(self, i):
      return GPIO.HIGH

    def reset(self): #force actual GPIO output state to match light_state
        for i in self.all():
            state = self.on_value(i) if self.light_state[i] else self.off_value(i)
            GPIO.output(self.GPIOlist[i], state) 

    def turn_on(self, light_number):
        if self.light_state[light_number]:
           return
        GPIO.output(self.GPIOlist[light_number], self.on_value(light_number))
        self.light_state[light_number] = True

    def turn_off(self, light_number):
        if not self.light_state[light_number]:
           return
        GPIO.output(self.GPIOlist[light_number], self.off_value(light_number))
        self.light_state[light_number] = False

    def turn_on_only(self, light_number):
        self.turn_off_all()
        self.turn_on(light_number)

    def turn_off_all(self):
        for i in self.all():
            self.turn_off(i)
            
    def turn_on_all(self):
        for i in self.all():
            self.turn_on(i)

    def all(self):
        return range(0, len(self.GPIOlist))


class Lights(SwitchedOutput):
    def __init__(self):
        # GPIO | Relay# | Controls
        #----------------------------------
        # 07      01     Light 1 - Sm Yellow (Pre-stage)
        # 08      02     Light 2 - Sm Yellow (Stage)
        # 04      03     Light 3 - Big Yellow (Amber 1)
        # 17      04     Light 4 - Big Yellow (Amber 2)
        # 27      05     Light 5 - Big Yellow (Amber 3)
        # 22      06     Light 6 - Big Green (Start)
        # 10      07     Light 7 - Big Red (False Start)
        # 09      08     Unused
        super(Lights, self).__init__([7, 8, 4, 17, 27, 22, 10, 9])


class Outlets(SwitchedOutput):
    def __init__(self):
        super(Outlets, self).__init__([16, 20])

    def on_value(self, i):
      return GPIO.HIGH

    def off_value(self, i):
      return GPIO.LOW

