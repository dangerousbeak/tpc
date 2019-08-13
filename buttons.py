#!/usr/bin/python
from enum import IntEnum
import RPi.GPIO as GPIO
import time

class Button(IntEnum):
    BLACK = 5
    BLUE = 6
    GREEN = 13
    YELLOW = 19
    RED = 26
    BEAM = 11
    BIG = 21
    BACK = 18

class Opto(IntEnum):
    SIDE = 14
    FRONT = 15

class SwitchedInput:
    def __init__(self, gpios):
        self.gpios = list(gpios)
        
        for b in gpios:
            GPIO.setup(int(b), GPIO.IN)
        
    def all_pressed(self):
        return [ b for b in self.gpios
                 if self.pressed(b) ]

    def pressed(self, b):
        return GPIO.input(b)

  
class Buttons(SwitchedInput):
    def __init__(self):
        super(Buttons, self).__init__(Button)
        
    @property
    def black(self):
        return self.pressed(Button.BLACK)

    @property
    def blue(self):
        return self.pressed(Button.BLUE)

    @property
    def red(self):
        return self.pressed(Button.RED)
    
    @property
    def yellow(self):
        return self.pressed(Button.YELLOW)
    
    @property
    def big(self):
        return self.pressed(Button.BIG)

        
class Optos(SwitchedInput):
    def __init__(self):
        super(Optos, self).__init__(Opto)  

    def all_broken(self):
        return [ b for b in list(Opto)
                 if self.broken(b) ]

    def broken(self, b):
        return GPIO.input(b)

    @property
    def side(self):
        return self.pressed(Opto.SIDE)
    
    @property
    def front(self):
        return self.pressed(Opto.FRONT)
