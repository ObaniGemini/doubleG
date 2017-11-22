import pygame

from shapes import *
from tilemap import *
from player import *

class World:

    def __init__(self, canvas):
        self.size = (int_val(80), int_val(60))
        self.canvas = canvas
        self.updating = False
        self.camera = Camera()
        self.tilemap = TileMap(self.camera)
        self.restart_level()
        self.signal = None


    def restart_level(self):
        self.tilemap.convert_file()
        self.player = Player(self.tilemap.get_spawn(), self.camera) 


    def is_updating(self):
        return self.updating

    def set_updating(self, updating):
        self.updating = updating

    def get_canvas(self):
        return self.canvas

    def update_canvas(self, size=(0, 0)):
        if not self.is_updating():
            self.canvas = pygame.Surface(self.size, pygame.SRCALPHA)
            self.canvas.convert()
            self.set_updating(True)


    def update_pos(self, pos, to):
        return (pos[0]+to[0], pos[1]+to[1])


    def update(self, canvas):
        self.set_updating(False)
        self.update_canvas()
        self.player.update()
        self.tilemap.update(canvas, self.player)
        
        self.signal = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.signal = "Force Quit"
            elif event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_ESCAPE:
                    self.signal = "Quit"
                elif k == pygame.K_F12:
                    self.signal = "Save Screen"

        if self.tilemap.signal == "End":
            self.signal = "Quit"