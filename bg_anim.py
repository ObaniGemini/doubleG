import pygame

from screen import *
from shapes import *
from math import *
from random import *



class BackgroundAnim:

    def __init__(self, canvas):
        self.bgcolor = pygame.Color(255, 255, 255, 255)
        self.size = (int_val(80), int_val(60))
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

            if self.side > 1:
                self.value -= 2
                c = (255, 255, 255, 255)
            else:
                self.value += 2
                c = (randint(0, 200), randint(0, 200), randint(0, 200), 50)
            ANGLE = abs(angle)
            draw_square(self.canvas, ANGLE*0.75, angle*4, (self.canvas.get_width()//2-ANGLE*1.5, self.canvas.get_height()//2-ANGLE*1.5), 0, c[0], c[1], c[2], c[3])

            if abs(self.value) >= 360:
                self.value = 0
                self.side += 1
                if self.side == 4:
                    self.side = 0
    

    def anim_2(self, active=True):
        if active:
            self.value += 1
            time = self.value
            if time > 5:
                self.reset()
                
                anchor_x1 = int_val(20)*randint(0, 3)
                anchor_y1 = int_val(15)*randint(0, 3)
                
                anchor_x2 = int_val(20)*randint(1, 4)
                anchor_y2 = int_val(15)*randint(1, 4)

                canvas = pygame.Surface((abs(anchor_x2 - anchor_x1), abs(anchor_y2 - anchor_y1)))
                canvas.fill(pygame.Color(randint(220, 240), randint(220, 240), randint(220, 240)))
                self.stored_shapes.append([canvas, anchor_x1, anchor_y1])
                
                if len(self.stored_shapes) > 3:
                    del self.stored_shapes[0]
                
                for shape in self.stored_shapes:
                    self.canvas.blit(shape[0], (shape[1], shape[2]))