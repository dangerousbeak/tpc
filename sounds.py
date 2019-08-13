from time import time, sleep
import pygame.mixer as mixer #used for sound - documentation: https://www.pygame.org/docs/ref/mixer.html
import subprocess
from random import randrange


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

        self.sounds = {}
        self.playing_music = False

    def play_music(self):
        if self.playing_music:
            return;
        self.mixer.music.load('sounds/0 - race-track-sounds.mp3')
        self.mixer.music.play(-1)  #negative number = loop forever
        self.playing_music = True

    def stop_music(self):
        self.playing_music = False
        self.mixer.music.stop() #kill the background racetrack sounds

    def get_sound(self, sound_name, ext):
        sound = self.sounds.get(sound_name)
        if sound is None:
            sound = mixer.Sound("sounds/{}.{}".format(sound_name, ext))
            self.sounds[sound_name] = sound
        return sound
    
    def play(self, sound_name, ext="wav"):
        sound = self.get_sound(sound_name, ext)
        empty_channel = self.mixer.find_channel()
        empty_channel.play(sound)

    def play_random(self, sound_names, ext="wav"):
        sound_name = sound_names[randrange(0, len(sound_names))]
        return self.play(sound_name, ext)
