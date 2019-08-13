#!/usr/bin/python
from game import Game, State
from zones import Racing, BLINK

game = Game()

try:
    game_mode = Racing(game, "racing")
    state = None  # State(BLINK)
    game.run(game_mode, state=state)

except KeyboardInterrupt:  
    print("Quit.")
  
finally:  
    game.cleanup()




