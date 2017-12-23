import pygame

mixer = pygame.mixer
mixer.init(frequency=44100, size=-16, channels=2, buffer=128)
sounds = []
sounds_name = []

class Music:
    def __init__(self):
        self.music = mixer.music

    def play(self, name, loops):
        self.music.load("sounds/"+name+".ogg")
        self.music.play(loops)

    def set_volume(volume):
        self.music.set_volume(volume)

    def stop(self):
        self.music.stop()

    def is_playing(self):
        return self.music.get_busy()



def add_sound(name):
    sounds.append(mixer.Sound("sounds/"+name+".wav"))
    sounds_name.append(name)

def clear_sounds():
    for sound in sounds:
        sound.stop()
    sounds.clear()
    sounds_name.clear()


def play_sound(name, loops=0):
    if name in sounds_name:
        sounds[sounds_name.index(name)].play(loops)
    else:
        add_sound(name)
        play_sound(name, loops)
        print("Sound didn't exist and has been added")

def set_volume(name, volume):
    if name in sounds_name:
        sounds[sounds_name.index(name)].set_volume(volume)


def stop_sound(name):
    if name in sounds_name:
        sounds[sounds_name.index(name)].stop()
    else:
        print("Sound doesn't exist or has been deleted before")