#!/usr/bin/python
from enum import IntEnum
import RPi.GPIO as GPIO
import time

# GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO5 as input (button)  
# GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO11 as input (beambreak)  

class Button(IntEnum):
    BLACK = 5
    BLUE = 6
    GREEN = 13
    YELLOW = 19
    RED = 26
    BIG = 21
    BACK = 18

class Opto(IntEnum):
    SIDE = 14
    FRONT = 15
    BEAM = 11

class SwitchedInput:
    def __init__(self, gpios):
        self.gpios = list(gpios)
        self._muted = {}
        
        for b in gpios:
            GPIO.setup(int(b), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    def all_pressed(self):
        return [ b for b in self.gpios
                 if self.pressed(b) ]

    def pressed(self, b, mute_time=1.0):
        pressed = GPIO.input(b)
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
        return self.pressed(b)

    @property
    def beam(self):
        return self.pressed(Opto.BEAM)
    
    @property
    def side(self):
        return self.pressed(Opto.SIDE)
    
    @property
    def front(self):
        return self.pressed(Opto.FRONT)
