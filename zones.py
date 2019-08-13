from game import Zone, State
from random import randrange


ATTRACT ="ATTRACT"
PRESTAGE = "PRESTAGE"
STAGE = "STAGE"
BLINK = "BLINK"
FAULT = "FAULT"
GO = "GO"
RUNNING = "RUNNING"
WAITING_TO_CROSS = "WAITING TO CROSS"
GAVE_UP = "GAVE UP"
END_OF_RACE = "END OF RACE"


class Racing(Zone):
    
    def enter(self):
        return State(ATTRACT)

    def exit(self):
        self.game.sounds.stop_music()

    def enter_state(self, state):
        g = self.game
        sub_state = state.sub_state

        if state == ATTRACT:
            if state.sub_state == 0:
                g.clock.reset()
                g.sounds.play_music()
                self.random_time = self.random_sound_time(state)
                
            if not sub_state % 2:
                g.lights.turn_on(7)  #turn on Button light
                g.outlets.turn_on_all()
            else:
                g.lights.turn_off(7)  #turn off Button light
                g.outlets.turn_off_all()
            
            return State(ATTRACT, sub_state+1, delay=1)
        
        if state == PRESTAGE:
            g.sounds.play("prestage")
            g.lights.turn_on_only(0)
            return State(STAGE, delay=3)

        if state == STAGE:
            g.sounds.play("racers ready")
            g.lights.turn_on(1)
            return State(BLINK, delay=2)

        if state == BLINK:
            self.game.sounds.stop_music()
            
            if sub_state % 15 == 0:
                g.sounds.play("revving 1")
                
            if not sub_state % 2:
                g.lights.turn_on(7)  #turn on Button light
                g.outlets.turn_on_all()
            else:
                g.lights.turn_off(7)  #turn off Button light
                g.outlets.turn_off_all()

            # Eventually, time out
            if sub_state == 50:
                return State(GAVE_UP)
            
            return State(BLINK, sub_state+1, delay=0.5)

        if state == FAULT:
            g.lights.turn_on(6)  #turn on Red Light
            g.sounds.play("disqualified")
            return State(STAGE, delay=5)

        if state == GO:
            g.sounds.play("short beep")
            g.lights.turn_on(2 + sub_state)
            if sub_state == 2:
                return State(WAITING_TO_CROSS, delay=1)
            return State(GO, sub_state+1, delay=1)

        if state == WAITING_TO_CROSS:
            g.lights.turn_on(5)
            g.clock.start()
            g.sounds.play_music()
            g.sounds.play("long beep")
            g.sounds.play("3 - pulling away")
            return State(GAVE_UP, delay=10)

        if state == GAVE_UP:
            g.sounds.play("crash")
            return State(ATTRACT, delay=5)
        
        if state == RUNNING:
            if not sub_state: #substate 0=haven't crossed, 1=crossed
                return State(RUNNING, 1, delay=10)
            return State(GAVE_UP, delay=180)

        if state == END_OF_RACE:
            g.clock.stop()
            g.sounds.play("1 - arriving")
            #stop the clock
            return State(ATTRACT, delay=10)
        
        raise ValueError("Unknown state {}".format(state))

    def exit_state(self, state):
        g = self.game
                
        if state == BLINK:
            g.outlets.turn_on_all()
            return

        if state == GO:
            g.lights.turn_off_all()
            return
        
        pass

    def idle(self, state):
        g = self.game
        sub_state = state.sub_state

        if g.buttons.black:
            if state != ATTRACT:
                g.sounds.play("crash")
                return State(ATTRACT)
            return None
        
        if state == ATTRACT:
            if state.timer > self.random_time:
                g.sounds.play_random([
                    "disqualified",
                    "revving 1",
                    "crash",
                    "beep",
                ])
                self.random_time = self.random_sound_time(state)
                
            if g.buttons.big:
                return State(PRESTAGE)
            return

        if state == BLINK:
            if g.buttons.big:
                return State(GO)
            return

        if state == GO:
            if g.buttons.beam:
                return State(FAULT)
            return
                
        if state == WAITING_TO_CROSS:
            if g.buttons.beam:
                return State(RUNNING)
            return

        if state == RUNNING:
            if sub_state == 1 and g.buttons.beam:
                return State(END_OF_RACE)
            return

    def random_sound_time(self, state):
        return state.timer + randrange(3,5)
