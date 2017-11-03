import pygame

from math import *


class SquareCollision:

    def __init__(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect
    
    def set_rect(self, rect):
        self.rect = rect

    def is_colliding(self, rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False
"""
    def is_inside(self, rect):
        points = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]
        check = False
        for point in points:
            if self.rect.collidepoint(point):
                check = True
                break
        if check:
            
        else:
            return ""
"""