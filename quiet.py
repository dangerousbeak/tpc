from game import Zone, State, Exit
from random import randrange
from buttons import Button


ATTRACT ="ATTRACT"


class QuietAttract(Zone):
    
    def enter(self):
        return State(ATTRACT)

    def enter_state(self, state):
        g = self.game
        sub_state = state.sub_state

        if state == ATTRACT:
            if not sub_state % 2:
                g.lights.turn_on(7)  #turn on Button light
                g.outlets.turn_on_all()
            else:
                g.lights.turn_off(7)  #turn off Button light
                g.outlets.turn_off_all()
            
            return State(ATTRACT, sub_state+1, delay=1)

    def idle(self, state):
        g = self.game
        sub_state = state.sub_state

        # This is just an example
        if g.buttons.blue:
            return Exit("racing")


