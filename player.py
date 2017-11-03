import pygame

from screen import *
from shapes import *
from collision import *

class Player:
    
    def __init__(self, init_pos, camera):
        self.pos = init_pos
        self.size = int_val(1)
        self.camera = camera

        self.images = Shapes((int_val(80), int_val(60)))
        self.layer = pygame.sprite.Group()
        self.update_shape()

        self.colliding = False
        self.force = (0.0, 0.0)


    def set_size(self, size):
        self.size = size

    def get_pos(self):
        return self.pos

    def get_force(self):
        return self.force

    def get_shape(self):
        return self.shape.get_rect()

    def update_shape(self):
        self.shape = SquareCollision(pygame.Rect(self.pos[0]-self.size, self.pos[1]-self.size, self.size*2, self.size*2))

    def update_pos(self, pos, to):
        return (pos[0]+to[0], pos[1]+to[1])
 
    def update_force(self, force):
        return (int(force[0]), int(force[1]))


    def is_pressed(self, key_enum):
        if pygame.key.get_pressed()[key_enum] == 1:
            return True


    def update(self, canvas):
        h_force = self.force[0]
        v_force = self.force[1]

        side = 0
        pressed = False


        if (self.is_pressed(pygame.K_q) or self.is_pressed(pygame.K_LEFT)):
           side = -1
        if (self.is_pressed(pygame.K_d) or self.is_pressed(pygame.K_RIGHT)):
            side = 1
        if (self.is_pressed(pygame.K_z) or self.is_pressed(pygame.K_UP)) and not pressed:
            pressed = True
            if self.colliding:
                v_force = float_val(-3.5)
            elif v_force <= 0:
                v_force -= float_val(0.125)


        if not (pressed and v_force >= float_val(0.75)):
            v_force += float_val(0.25)

        h_force = float_val(1.5*side)
        if self.colliding or self.is_pressed(pygame.K_RETURN):
            v_force = 0
        
        self.force = (h_force, v_force)
        pos = (0, 0)
        pos = self.update_pos(self.pos, self.update_force(self.force))


        self.pos = pos
        self.camera.update_to((self.pos[0]-int_val(40), self.pos[1]-int_val(30)))
        self.layer.add(self.images.draw_square((int_val(40), int_val(30)), self.size, 0))
        self.layer.draw(canvas)
        self.update_shape()
        self.layer.empty()