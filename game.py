#!/usr/bin/python
import RPi.GPIO as GPIO
from buttons import Buttons, Optos, Button
from lights import Lights, Outlets
from sounds import Sounds
from countdown import Countdown
import time
from datetime import datetime

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


class Exit:
    def __init__(self, value):
        self.value = value


class Game:
    def __init__(self, modes):
        GPIO.setmode(GPIO.BCM)  #set up to use gpio port numbers (instead of pin #s)

        self.buttons = Buttons()
        self.optos = Optos()
        self.lights = Lights()
        self.outlets = Outlets()
        self.sounds = Sounds()
        self.clock = Countdown(12)

        self.modes = modes
        self.last_time = time.localtime()

    def cleanup(self):
        self.lights.turn_off_all()
        GPIO.cleanup()  #clean exit of GPIO ports

    def time(self):
        return int(round(time.time() * 1000))

    def find_mode(self, name):
        return self.modes[name](self, name)
        
    def run(self, game_mode, state=None):
        start_state = game_mode.enter()
        state = state or start_state
        try:
            timer_start = self.time()
            while state:
                start_time = self.time()

                print("{}:{}".format(game_mode, state))
                new_state = game_mode.enter_state(state)
                if isinstance(new_state, Exit):
                    return new_state
                    
                next_time = start_time + new_state.delay*1000

                next_state = None
                while not next_state:
                    now = self.time()
                    if now > next_time:
                        next_state = new_state
                        next_state.delay = 0
                        break

                    state.timer = (now - timer_start) / 1000.0

                    ret = self.idle(game_mode)
                    if isinstance(ret, Exit):
                        return ret
                    
                    ret = game_mode.idle(state)
                    if isinstance(ret, Exit):
                        return ret
                    if isinstance(ret, State):
                        next_state = ret

                if next_state.state != state.state:
                    game_mode.exit_state(state)
                    timer_start = now
                    
                state = next_state
                
        finally:
            game_mode.exit()

    def idle(self, game_mode):
        # This is global stuff
        
        if self.buttons.switched( Button.BACK ):
            self.sounds.play("beep")
            if self.buttons.back:
                return Exit("racing")
            else:
                self.sounds.play("gurble")
                return Exit("quiet")

        if self.buttons.check( (Button.GREEN, Button.RED, Button.YELLOW) ):
            return Exit("songs")

        if game_mode.name == "songs":
            if self.buttons.black:
                self.sounds.volume_up()
                self.sounds.play("beep")
            if self.buttons.blue:
                self.sounds.volume_down()
                self.sounds.play("beep")


        # Put in stuff for time check & volume changes, e.g.
        # if it was before 7am and now it's after 7am
        # then return Exit("songs")
        if self.check_time(0):  # At midnight
            self.sounds.set_volume(0.7)

        if self.check_time(2):  # At 2am
            self.sounds.set_volume(0.2)

        if self.check_time(4):  # At 4am
            return Exit("quiet")

        if self.check_time(8):  # At 8am (choose wisely)
            self.sounds.set_volume(1)
            return Exit("songs")

        self.last_time = time.localtime()

    def play(self, name):
        game_mode = self.find_mode(name)
        state = None
        print("Starting {}".format(game_mode))
        
        while True:
            result = self.run(game_mode, state)
            print("{} exited: {}".format(game_mode, result.value))
            game_mode, state = self.mode_exited(game_mode, result.value)
            print("Switching to {}".format(game_mode))
            
    def mode_exited(self, game_mode, value):
        return self.find_mode(value), None

    def check_time(self, hr):
        now = time.localtime()
        if hr == 0:
            return self.last_time.tm_hour > 20
        return self.last_time.tm_hour < hr and now.tm_hour == hr

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
