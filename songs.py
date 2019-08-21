from game import Zone, State, Exit
from random import randrange
from buttons import Button


WAITING ="WAITING"
MORNING_TRAIN = "MT"
MASTER_PAINTER = "MP"
DONE = "DONE"


class Songs(Zone):
    
    def enter(self):
        return State(WAITING)

    def enter_state(self, state):
        g = self.game
        sub_state = state.sub_state

        if state == WAITING:
            return State(WAITING, delay=1000)

        if state == MORNING_TRAIN:
            g.sounds.play_background("morning train.MP3")
            return State(MASTER_PAINTER, delay=192) #3 min 12 seconds

        if state == MASTER_PAINTER:
            g.sounds.play_background("The Old Masterbater.mp3")
            return State(DONE, delay=165) #2 min 45 seconds

        if state == DONE:
            return Exit("racing")

    def idle(self, state):
        g = self.game
        sub_state = state.sub_state

        if g.optos.beam:
            return State(MORNING_TRAIN)
