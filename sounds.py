from time import time, sleep
import pygame.mixer as mixer #used for sound - documentation: https://www.pygame.org/docs/ref/mixer.html
import subprocess


subprocess.call(["amixer", "-c", "0", "cset", "numid=3", "1"])
# to force audio output to HDMI use:
# amixer -c 0 cset numid=3 2
# to force audio output to headphones use:
# amixer -c 0 cset numid=3 1


class Sounds(object):
    def __init__(self):
        mixer.pre_init(44100, -16, 2, 2048) #frequency, size, channels, buffersize
        mixer.init() #initialize the mixer module
        mixer.quit() #for some reason quitting and re-initializing removes sound lag
        mixer.init(44100, -16, 2, 2048)
        self.mixer = mixer

        self.beep = mixer.Sound('sounds/beep.wav')
        self.shortbeep = mixer.Sound('sounds/short beep.wav')
        self.longbeep = mixer.Sound('sounds/long beep.wav')
        self.prestage = mixer.Sound('sounds/prestage.wav')
        self.stage = mixer.Sound('sounds/racers ready.wav')
        self.fault = mixer.Sound('sounds/disqualified.wav')
        self.revving = mixer.Sound('sounds/revving 1.wav')
        self.leaving = mixer.Sound('sounds/3 - pulling away.wav')
        self.arriving = mixer.Sound('sounds/1 - arriving.wav')

    def play_music(self):
        self.mixer.music.load('sounds/0 - race-track-sounds.mp3')
        self.mixer.music.play(-1)  #negative number = loop forever

    def stop_music(self):
        mixer.music.stop() #kill the background racetrack sounds

    def play_sound(self, sound):
        empty_channel = self.mixer.find_channel()
        empty_channel.play(sound)
