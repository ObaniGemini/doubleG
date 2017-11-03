import pygame

from screen import *
from shapes import *
from math import *



class BackgroundAnim:

    def __init__(self, canvas):
        self.bgcolor = pygame.Color(255, 255, 255, 255)
        self.size = (int_val(80), int_val(60))

        self.background = pygame.sprite.Group()
        self.shapes = Shapes(self.size)

        self.canvas = canvas
        self.clear()



    def anim_square(self, active=True):
        if active:
            ANGLE = self.angle

            self.background.add(self.shapes.draw_square((self.size[0]/2, self.size[1]/2), ANGLE*0.75, self.angle*4, 1, self.side))
            self.background.draw(self.canvas)

            self.background.empty()

            if self.side > 1:
                self.angle -= 2
            else:
                self.angle += 2

            if abs(self.angle) >= 360:
                self.angle = 0
                self.side += 1
                if self.side == 4:
                    self.side = 0


    def clear(self):
        self.canvas.fill(self.bgcolor)
        self.angle = 0
        self._side = 0