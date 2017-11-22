import pygame
from math import *

from shape import Shape

def draw_square (canvas, scale, rot, pos, mode=0, r=0, g=0, b=0, a=255):
    SCALE = (scale * 2)
    surface = pygame.Surface((SCALE*2, SCALE*2), pygame.SRCALPHA, 32)
    ROT = radians(rot+45)
    color = pygame.Color(r, g, b, a)

    for i in range(0, 4):
        positioning = [\
                      (SCALE+int((SCALE+1)*cos(ROT + (pi/2)*i)), SCALE+int((SCALE+1)*sin(ROT + (pi/2)*i))), \
                      (SCALE+int((SCALE+1)*cos(ROT + (pi/2)*(i+1))), SCALE+int((SCALE+1)*sin(ROT + (pi/2)*(i+1))))\
                      ]

        if mode == 0:
            pygame.draw.line(surface, color, positioning[0], positioning[1], 1)
        elif mode == 1:
            pygame.draw.aaline(surface, color, positioning[0], positioning[1], 1)
    canvas.blit(surface, pos)

def draw_rect(canvas, scale, pos, r=0, g=0, b=0, a=255):
    surface = pygame.Surface((scale, scale), pygame.SRCALPHA, 32)
    surface.fill(pygame.Color(r, g, b, a))
    canvas.blit(surface, pos)
