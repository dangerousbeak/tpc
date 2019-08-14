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
    BIG = 21
    BACK = 18

class Opto(IntEnum):
    BEAM = 11
    INNER = 14
    OUTER = 15


class SwitchedInput:
    def __init__(self, gpios):
        self.gpios = gpios
        self._muted = {}
        
        for b, pud in gpios.items():
            GPIO.setup(int(b), GPIO.IN, pull_up_down=pud)
        
    def triggered(self, b):
        return GPIO.input(b) == (self.gpios[b] == GPIO.PUD_DOWN)

    def all_triggered(self):
        return [ b for b in self.gpios
                 if self.triggered(b) ]

    def check(self, b, mute_time=1.0):
        pressed = self.triggered(b)
        now = time.time()
        muted_until = self._muted.get(b)
        if muted_until is not None:
            if pressed or now < muted_until:
                return False
            del self._muted[b]

        if not pressed:
            return False
        
        self._muted[b] = now + mute_time
        print("button: {}".format(b))
        return True

  
class Buttons(SwitchedInput):
    def __init__(self):
        super(Buttons, self).__init__({
            b: GPIO.PUD_DOWN
            for b in list(Button)
        })
        
    @property
    def black(self):
        return self.check(Button.BLACK)

    @property
    def blue(self):
        return self.check(Button.BLUE)

    @property
    def red(self):
        return self.check(Button.RED)
    
    @property
    def yellow(self):
        return self.check(Button.YELLOW)
    
    @property
    def big(self):
        return self.check(Button.BIG)


class Optos(SwitchedInput):
    def __init__(self):
        super(Optos, self).__init__({
            Opto.BEAM: GPIO.PUD_DOWN,
            Opto.INNER: GPIO.PUD_UP,
            Opto.OUTER: GPIO.PUD_UP,
        })

    @property
    def beam(self):
        return self.check(Opto.BEAM)
    
    @property
    def outer(self):
        return self.check(Opto.OUTER, mute_time=6.0)
    
    @property
    def inner(self):
        return self.check(Opto.INNER, mute_time=6.0)
