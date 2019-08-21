from game import Zone, State, Exit
from random import randrange
from buttons import Button


ATTRACT ="ATTRACT"
PRESTAGE = "PRESTAGE"
WAITING_FOR_STAGE = "WAITING_FOR_STAGE"
STAGE = "STAGE"
BLINK = "BLINK"
FAULT = "FAULT"
GO = "GO"
RUNNING = "RUNNING"
WAITING_TO_CROSS = "WAITING TO CROSS"
GAVE_UP = "GAVE UP"
FINISHED = "FINISHED"
END_OF_RACE = "END OF RACE"


class Racing(Zone):
    
    def enter(self):
        self.shut_up_until = 0
        return State(ATTRACT)

    def exit(self):
        self.game.sounds.stop_background()
        self.game.clock.reset()

    def enter_state(self, state):
        g = self.game
        sub_state = state.sub_state

        if state == ATTRACT:
            if state.sub_state == 0:
                g.clock.reset()
                g.lights.turn_off_all()
                g.sounds.play_background("0 - race-track-sounds.mp3", loop=True)
                self.random_time = self.random_sound_time(state)
                
            if not sub_state % 2:
                g.lights.turn_on(7)  #turn on Button light
                g.outlets.turn_on_all()
            else:
                g.lights.turn_off(7)  #turn off Button light
                g.outlets.turn_off_all()
            
            return State(ATTRACT, sub_state+1, delay=1)
        
        if state == PRESTAGE:
            g.outlets.turn_on_all() #turn ON outlet lights in case they ended in off state
            g.sounds.play_random([
                    "racers at prestage-1",
                    "racers at prestage-2",
                    "racers at prestage-3",
                    "racers at prestage-5",
                ])
            g.sounds.play_random([
                    "1 - arriving",
                    "1 - arriving-2",
                    "1 - arriving-3",
                    "1 - arriving-4",
                    "1 - arriving-5",
                ])
            g.lights.turn_on_only(0)
            return State(WAITING_FOR_STAGE, delay=3)

        if state == WAITING_FOR_STAGE:
            if sub_state == 3:
                return State(ATTRACT, delay=30)
            if sub_state > 0:
                g.sounds.play_random([
                    "what are you doing-1",
                    "what are you doing-2",
                    "what are you doing-4",
                    "what are you doing-7",
                    "don't just stand there I know youre there-1",
                    "don't just stand there I know youre there-2",
                 ])
            return State(WAITING_FOR_STAGE, sub_state+1, delay=10)

        if state == STAGE:
            g.lights.turn_off(6) #turn off Red Light (if prior fault)
            g.sounds.play_random([
                    "racers ready-1",
                    "racers ready-2",
                    "racers ready-3",
                    "racers ready-4",
                 ])
            g.lights.turn_on(1)
            return State(BLINK, delay=2)

        if state == BLINK:
            self.game.sounds.stop_background()
            if sub_state % 15 == 0:
                g.sounds.play_random([
                    "revving",
                    "revving 1",
                    "revving 2",
                    "revving 3",
                    "revving 4",
                    "revving 5",
                 ])
                
            if not sub_state % 2:
                g.lights.turn_on(7)  #turn on Button light
                g.outlets.turn_on_all()
            else:
                g.lights.turn_off(7)  #turn off Button light
                g.outlets.turn_off_all()

            # Eventually, time out
            if sub_state % 20 == 0:
                g.sounds.play_random([
                    "press yellow button to start race-1",
                    "press yellow button to start race-4",
                    "press yellow button to start race-5",
                 ])

            # Eventually, time out
            if sub_state == 50:
                g.sounds.play_random([
                    "cant you follow instructions-1",
                    "cant you follow instructions-3",
                    "cant you follow instructions-4",
                    "cant you follow instructions-5",
                 ])
                return State(GAVE_UP)
            
            return State(BLINK, sub_state+1, delay=0.5)  #delay is between button blinks

        if state == FAULT:
            g.lights.turn_on(6)  #turn on Red Light
            g.sounds.play_random([
                "racer disqualified-1",
                "racer disqualified-2",
                "racer disqualified-3",
                "racer disqualified-4",
                "racer disqualified-5",
                 ])
            return State(STAGE, delay=5)

        if state == GO:
            g.sounds.play("short beep")
            g.lights.turn_on(2 + sub_state)
            if sub_state == 0:
                g.outlets.turn_on_all() #turn ON outlet lights in case they ended in off state           
            if sub_state == 2:
                return State(WAITING_TO_CROSS, delay=1)
            return State(GO, sub_state+1, delay=1)

        if state == WAITING_TO_CROSS:
            if sub_state == 0:
                g.outlets.turn_on_all() #turn ON outlet lights in case they ended in off state          
                g.lights.turn_on(5)  #turn on Green Light
                g.sounds.play("long beep")
                g.clock.start()
                g.sounds.play_background("0 - race-track-sounds.mp3", loop=True)
                g.sounds.play_random([
                    "3 - pulling away",
                    "3 - pulling away-2",
                    "3 - pulling away-3",
                    ])
            if sub_state > 200:
                return State(GAVE_UP)
            if sub_state % 2:  #Alternate flashing rope lights until they cross - 200*.05 = 10 seconds
                g.outlets.turn_on(0)
                g.outlets.turn_off(1)
            else:
                g.outlets.turn_on(1)
                g.outlets.turn_off(0)
            return State(WAITING_TO_CROSS, sub_state+1, delay=0.05)

        if state == GAVE_UP:
            g.sounds.play("racer disqualified-4")
            return State(ATTRACT, delay=5)
        
        if state == RUNNING:
            if not sub_state:
                return State(RUNNING, 1, delay=10)
            return State(GAVE_UP, delay=180)


        if state == FINISHED: #Do a quick alternating flash of outlets                           
            if sub_state == 0:
                g.clock.stop()
            if not sub_state % 2:
                g.outlets.turn_on(0)
                g.outlets.turn_off(1)
            else:
                g.outlets.turn_on(1)
                g.outlets.turn_off(0)

            # Finish alternating lights
            if sub_state == 50:
                g.outlets.turn_on_all() #turn ON outlet lights in case they ended in off state
                return State(END_OF_RACE)
            
            return State(FINISHED, sub_state+1, delay=0.05)


        if state == END_OF_RACE:
            g.sounds.play_random([
                    "1 - arriving",
                    "1 - arriving-2",
                    "1 - arriving-3",
                    "1 - arriving-4",
                    "1 - arriving-5",
                ])
            #stop the clock
            return State(ATTRACT, delay=15)
        
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

        # This is just an example to change mode, but better to do in game.py
        #if g.buttons.blue:
        #    return Exit("quiet")

        # Multi button check: inner parens are important
        #if g.buttons.check( (Button.BLUE, Button.BLACK) ):
        #    g.sounds.play("crash")
        #    return State(ATTRACT)

        if g.buttons.red:
            if state.state in (GO, WAITING_TO_CROSS, GAVE_UP, RUNNING, END_OF_RACE):
                g.sounds.play_random([
                    "4 - trouble starting",
                    "4 - trouble starting-2",
                    "4 - trouble starting-3",
                    "racer down-1",
                    "racer down please use caution-1",
                    "racer down please use caution-2",
                    "racer down please use caution-3",
                    "racer down please use caution-4",
                    "racer down please use caution-5",
                    "racer down please use caution-6",
                    "racer down please use caution-7",
                ])

        if g.buttons.yellow:
            if state.state in (RUNNING):
                g.sounds.play_random([
                    "all racers must enter pit area-1",
                    "all racers must enter pit area-2",
                    "all racers must enter pit area-3",
                    "please enter pit area-1",
                    "please enter pit area-2",
                    "please enter pit area-3",
                    "please enter pit area-4",
                    "please enter pit area-5",
                    "please enter pit area-6",
                    "please enter pit area-7",
                    "please enter pit area-8",
                    "please enter pit area-9",
                    "please enter pit area-all racers-4",
                    "please enter pit area-all racers-5",
                ])
            
        if g.buttons.green:
            if state.state in (RUNNING):
                g.sounds.play_random([
                    "2 - fixing-1",
                    "2 - fixing-2",
                    "2 - fixing-3",
                    "2 - fixing-4",
                    "2 - fixing-5",
                    "2 - fixing-6",
                    "2 - fixing-7",
                    "2 - fixing-8",
                    "2 - fixing-9",
                    "2 - fixing-10",
                ])

        if g.buttons.blue:
            if state.state in (GO, WAITING_TO_CROSS, GAVE_UP, RUNNING, END_OF_RACE):
                g.sounds.play_random([
                    "cheering-1",
                    "cheering-2",
                    "cheering-3",
                    "cheering-4",
                ])

        if g.buttons.black:
            if state.state in (GO, WAITING_TO_CROSS, GAVE_UP, RUNNING, END_OF_RACE):
                g.sounds.play_random([
                    "booing-1",
                    "booing-2",
                    "booing-3",
                ])

            
        if state == ATTRACT:
            if state.timer > self.random_time:
                g.sounds.play_random([
                    "hey stoner press this button-1",
                    "hey stoner press this button-2",
                    "hey stoner press this button-3",
                    "hey stoner press this button-4",
                    "hey stoner press this button-5",
                ])
                self.random_time = self.random_sound_time(state)

            if g.optos.outer: #see if someone is nearby in attract mode
                if state.timer > self.shut_up_until:
                    g.sounds.play_random([
                        "don't just stand there I know youre there-1",
                        "don't just stand there I know youre there-2",
                    ])
                    self.shut_up_until = state.timer + randrange(5, 15) # seconds between talking

            if g.buttons.big:
                return State(PRESTAGE)
            return

        if state == WAITING_FOR_STAGE:
            if g.optos.inner: #make sure someone is one the track
                return State(STAGE) #go from pre-stage to stage
            return

        if state == BLINK:
            if g.buttons.big:
                return State(GO)
            return

        if state == GO:
            if g.optos.beam:
                return State(FAULT)
            return
                
        if state == WAITING_TO_CROSS:
            if g.optos.beam:
                g.sounds.play("beep tone")
                g.outlets.turn_on_all() #turn ON outlet lights in case they ended in off state
                return State(RUNNING)
            return

        if state == RUNNING:
            if sub_state == 1 and g.optos.beam:
                g.sounds.play("beep tone")
                g.sounds.play_random([
                    "cheering-1",
                    "cheering-2",
                    "cheering-3",
                    "cheering-4",
                ])
                return State(FINISHED)
            return

    def random_sound_time(self, state):
        if state == ATTRACT:
            return state.timer + randrange(300, 1000) #seconds. Used to play a random sound when nothing happening
        return state.timer + 10
