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
        self.set_volume(1.0)

    def set_volume(self, volume):
        if volume < 0:
            volume = 0
        if volume > 2.0:  # Will anything above 1.0 work? I dunno
            volume = 2.0
        if volume == self.volume:
            return

        self.volume = volume
        self.mixer.music.set_volume(volume)

    def volume_up(self):
        self.set_volume(self.volume + 0.1)

    def volume_down(self):
        self.set_volume(self.volume - 0.1)

    def play_background(self, filename, loop=False):
        if self.playing_music == filename:
            return;

        self.mixer.music.set_volume(self.volume)
        self.mixer.music.load('/home/pi/tpc/sounds/{}'.format(filename))
        if loop:
            self.mixer.music.play(-1)  #negative number = loop forever
        else:
            self.mixer.music.play()
        self.playing_music = filename

    def stop_background(self):
        self.playing_music = None
        self.mixer.music.stop() #kill the background racetrack sounds

    def get_sound(self, sound_name, ext):
        sound = self.sounds.get(sound_name)
        if sound is None:
            sound = mixer.Sound("/home/pi/tpc/sounds/{}.{}".format(sound_name, ext))
            self.sounds[sound_name] = sound
        return sound
    
    def play(self, sound_name, ext="wav"):
        sound = self.get_sound(sound_name, ext)
        empty_channel = self.mixer.find_channel()
        if not empty_channel:
            return
        empty_channel.set_volume(self.volume)
        empty_channel.play(sound)

    def play_random(self, sound_names, ext="wav"):
        sound_name = sound_names[randrange(0, len(sound_names))]
        return self.play(sound_name, ext)
