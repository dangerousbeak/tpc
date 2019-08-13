#!/usr/bin/python
import RPi.GPIO as GPIO
from buttons import Buttons, Optos
from lights import Lights, Outlets
from sounds import Sounds
from countdown import Countdown
import time


class State:
    def __init__(self, state, sub_state=0, delay=0):
        self.state = state
        self.sub_state = sub_state
        self.delay = delay
        self.timer = 0

    def sub_state(self, sub_state):
        self.sub_state = sub_state
        return self

    def after(self, delay):
        self.delay = delay
        return self
    
    def __str__(self):
        s = "{}:{}".format(self.state, self.sub_state)
        if self.delay:
            s = s + " in {}sec".format(self.delay)
        return s

    def __eq__(self, o):
        if self is o:
            return True
        return self.state == o

    def __neq__(self, o):
        return not self == o


class Game:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  #set up to use gpio port numbers (instead of pin #s)

        self.buttons = Buttons()
        self.optos = Optos()
        self.lights = Lights()
        self.outlets = Outlets()
        self.sounds = Sounds()
        self.clock = Countdown(12)

    def cleanup(self):
        self.lights.turn_off_all()
        GPIO.cleanup()  #clean exit of GPIO ports

    def time(self):
        return int(round(time.time() * 1000))
        
    def run(self, game_mode, state=None):
        start_state = game_mode.enter()
        state = state or start_state
        try:
            timer_start = self.time()
            while state:
                start_time = self.time()

                print("{}:{}".format(game_mode, state))
                new_state = game_mode.enter_state(state)
                next_time = start_time + new_state.delay*1000

                next_state = None
                while not next_state:
                    now = self.time()
                    if now > next_time:
                        next_state = new_state
                        next_state.delay = 0
                        break

                    state.timer = (now - timer_start) / 1000.0
                    ret = game_mode.idle(state)
                    if isinstance(ret, State):
                        next_state = ret

                if next_state.state != state.state:
                    game_mode.exit_state(state)
                    timer_start = now
                    
                state = next_state
                
        finally:
            game_mode.exit()

    def idle(self):
        pass


class Zone:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        
    def enter(self):
        pass

    def exit(self):
        pass

    def enter_state(self, state):
        pass

    def exit_state(self, state):
        pass

    def idle(self, state):
        pass

    def __str__(self):
        return self.name
