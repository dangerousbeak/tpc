#!/usr/bin/python
from game import Game, State
from racing import Racing
from quiet import QuietAttract
from songs import Songs

game = Game({
    "quiet": QuietAttract,
    "racing": Racing,
    "songs": Songs,
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

