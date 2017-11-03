import pygame
from math import *

from shape import Shape

class Shapes:

    def __init__ (self, canvas_size):
        self.scale_x = canvas_size[0]
        self.scale_y = canvas_size[1]

    def draw_square (self, pos, scale, rot, mode=0, gradient=0):
        surface = pygame.Surface((self.scale_x, self.scale_y), pygame.SRCALPHA, 32)
        X, Y = pos
        ROT = radians(rot+45)
        color_scale = int(255*(gradient % 2))
        for i in range(0, 4):
            positioning = [\
                          ((X + 2*int(scale*cos(ROT + i*(pi/2))*self.scale_x/600)), (Y + 2*int(scale*(sin(ROT + i*(pi/2))*self.scale_x/600)))), \
                          ((X + 2*int(scale*cos(ROT + (i+1)*(pi/2))*self.scale_x/600)), (Y + 2*int(scale*(sin(ROT + (i+1)*(pi/2))*self.scale_x/600))))\
                          ]
            if mode == 0:
                pygame.draw.line(surface, pygame.Color(color_scale, color_scale, color_scale), positioning[0], positioning[1], 1)
            elif mode == 1:
                pygame.draw.aaline(surface, pygame.Color(color_scale, color_scale, color_scale), positioning[0], positioning[1], 1)
        return Shape(surface)
