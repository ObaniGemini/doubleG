import pygame

from screen import *
from shapes import *
from math import *
from random import *



class BackgroundAnim:

    def __init__(self, canvas):
        self.bgcolor = pygame.Color(255, 255, 255, 255)
        self.size = (int_val(80), int_val(60))

        self.background = pygame.sprite.Group()
        self.shapes = Shapes(self.size)
        self.stored_shapes = []


        self.canvas = canvas
        self.reset()
    
    def reset(self):
        self.canvas.fill(pygame.Color(255, 255, 255, 255))
        self.value = 0      #arbitrary value being used in different ways (time, angle,...)
        self.side = 0



    def anim_1(self, active=True):
        if active:
            angle = self.value

            self.background.add(self.shapes.draw_square((self.size[0]/2, self.size[1]/2), angle*0.75, angle*4, 1, self.side))
            self.background.draw(self.canvas)

            self.background.empty()

            if self.side > 1:
                self.value -= 2
            else:
                self.value += 2

            if abs(self.value) >= 360:
                self.value = 0
                self.side += 1
                if self.side == 4:
                    self.side = 0
    

    def anim_2(self, active=True):
        if active:
            self.value += 1
            time = self.value
            if time > 10:
                self.reset()
                
                anchor_x1 = int_val(20)*randint(0, 3)
                anchor_y1 = int_val(15)*randint(0, 3)
                
                anchor_x2 = int_val(20)*randint(1, 4)
                anchor_y2 = int_val(15)*randint(1, 4)

                canvas = pygame.Surface((abs(anchor_x2 - anchor_x1), abs(anchor_y2 - anchor_y1)), pygame.SRCALPHA)
                canvas.fill(pygame.Color(randint(0, 100), randint(0, 100), randint(0, 100), 50))
                self.stored_shapes.append([canvas, anchor_x1, anchor_y1])
                
                if len(self.stored_shapes) > 3:
                    del self.stored_shapes[0]
                
                for shape in self.stored_shapes:
                    self.canvas.blit(shape[0], (shape[1], shape[2]))
