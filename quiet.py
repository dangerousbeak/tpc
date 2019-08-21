from game import Zone, State, Exit
from random import randrange
from buttons import Button


ATTRACT ="ATTRACT"
PATTERN1 = "PATTERN 1"
PATTERN2 = "PATTERN 2"

class QuietAttract(Zone):
    
    def enter(self):
        return State(PATTERN1)

    def enter_state(self, state):
        g = self.game
        sub_state = state.sub_state

##        if state == ATTRACT:
##            if not sub_state % 2:
##                g.lights.turn_on(7)  #turn on Button light
##                g.outlets.turn_on_all()
##            else:
##                g.lights.turn_off(7)  #turn off Button light
##                g.outlets.turn_off_all()
##            
##            return State(ATTRACT, sub_state+1, delay=1)

        if state == PATTERN1:
            interval = 0.05 #smallest delay between light changes
            if sub_state == 0:
                g.outlets.turn_on_all() #turn OFF outlet lights in case they ended in off state -- BACKWARDS ON/OFF!           
                g.lights.turn_off_all()  #turn OFF all traffic lights

            if sub_state > 10/interval: #change after 300 sec = 5 min at this pattern 
                return State(PATTERN2)
            
            if round(sub_state*interval) % 4: #every 7 seconds
                g.lights.turn_on_only(sub_state % 8)
                
            if round(sub_state*interval) % 3: #every 4 seconds
                if sub_state % 2:  #Alternate flashing rope lights
                    g.outlets.turn_on(0)
                    g.outlets.turn_off(1)
                else:
                    g.outlets.turn_on(1)
                    g.outlets.turn_off(0)
                    
            return State(PATTERN1, sub_state+1, delay=interval)

        if state == PATTERN2:
            g.outlets.turn_off_all() #turn ON outlet lights in case they ended in off state -- BACKWARDS ON/OFF!           
            g.lights.turn_on_all()  #turn ON all traffic lights
            return State(PATTERN1, delay=20)



    def idle(self, state):
        g = self.game
        sub_state = state.sub_state
        if g.buttons.big:
            g.sounds.play("beep")


