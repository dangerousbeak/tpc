#!/usr/bin/python
from game import Game, State
from racing import Racing
from quiet import QuietAttract

game = Game({
    "quiet": QuietAttract,
    "racing": Racing,
})

try:
    if game.buttons.back:
        game.play("racing")
    else:
        game.play("quiet")

except KeyboardInterrupt:  
    print("Quit.")
  
finally:  
    game.cleanup()

