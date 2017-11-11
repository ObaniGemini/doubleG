import pygame

from screen import *
from shapes import *



class Player:

    def __init__(self, spawn_pos, camera):
        self.pos = spawn_pos
        self.next_pos = spawn_pos        #used for collision checks
        self.spawn_pos = spawn_pos

        self.size = int_val(1)
        self.camera = camera

        self.images = Shapes((int_val(80), int_val(60)))
        self.layer = pygame.sprite.Group()
        
        self.can_move = [True, True, True, True]
        self.collider = [0, 0, 0, 0]
        self.force = (0.0, 0.0)

        self.jetpack_cooldown = False
        self.jetpack_fuel = 80

        self.update_shape()


    def set_size(self, size):
        self.size = size

    def get_pos(self):
        return self.pos

    def get_force(self):
        return self.force

    def update_shape(self):
        self.shape = pygame.Rect(self.pos[0] - self.size, self.pos[1] - self.size, self.size*2, self.size*2)

    def update_pos(self, pos, to):
        return (pos[0]+to[0], pos[1]+to[1])
 
    def update_force(self):
        return (int(self.force[0]/1000), int(self.force[1]/1000))

    def apply_impulse(self, x, y):
        self.force = (self.force[0] + int_val(x*1000), self.force[1] + int_val(y*1000))


    def is_pressed(self, key_enum):
        if pygame.key.get_pressed()[key_enum] == 1:
            return True


    def update(self):
        left, right, up, down = 0, 1, 2, 3

        side = 0
        pressed = False

        self.force = (0, self.force[1])
        if not self.can_move[down]:
            self.force = (self.force[0], 0)

        side = 0

        if self.is_pressed(pygame.K_LEFT) and self.can_move[left]:
            side = -1
        if self.is_pressed(pygame.K_RIGHT) and self.can_move[right]:
            side += 1

        self.apply_impulse(1.5*side, 0)

        pressed = False
        if self.is_pressed(pygame.K_UP) and self.can_move[up]:
            pressed = True
            if self.can_move[down]:
                if not self.jetpack_cooldown and self.jetpack_fuel > 0:
                    self.apply_impulse(0, -0.8)
                    self.jetpack_fuel -= 8
                else:
                    self.jetpack_cooldown = True
            else:
                self.apply_impulse(0, -4)
        if self.jetpack_fuel < 80:
            self.jetpack_fuel += 2
        elif self.jetpack_fuel == 80:
            self.jetpack_cooldown = False


        if self.can_move[down]:
            self.apply_impulse(0, 0.4)

        self.next_pos = self.update_pos(self.pos, self.update_force())


    def update_hud(self, canvas):
        if self.jetpack_fuel > 0:
            taint = 0
            if not self.jetpack_cooldown:
                taint = self.jetpack_fuel*3

            jetpack = pygame.Surface((int_val(self.jetpack_fuel), int_val(4)), pygame.SRCALPHA)
            jetpack.fill(pygame.Color(255-taint, 0, 0, 150))
            canvas.blit(jetpack, (0, 0))


    def update_player(self, canvas):
        left, right, up, down = 0, 1, 2, 3

        if not self.can_move[left] and self.next_pos[0] <= self.pos[0]:
            self.next_pos = (((self.collider[left]+1)*int_val(8)+self.size+int_val(1/2)), self.next_pos[1])
        if not self.can_move[right] and self.next_pos[0] >= self.pos[0]:
            self.next_pos = ((self.collider[right]*int_val(8)-self.size-int_val(1/2)), self.next_pos[1])
        if not self.can_move[up] and self.next_pos[1] <= self.pos[1]:
            self.next_pos = (self.next_pos[0], ((self.collider[up]+1)*int_val(8)+self.size+int_val(1/2)))
        if not self.can_move[down] and self.next_pos[1] >= self.pos[1]:
            self.next_pos = (self.next_pos[0], (self.collider[down]*int_val(8)-self.size-int_val(1/2)))

        
        if self.next_pos[1] > 3000:
            self.next_pos = self.spawn_pos
            self.force = (0, 0)


        self.pos = self.next_pos
        self.camera.update_to((self.pos[0]-int_val(40), self.pos[1]-int_val(30)))
        self.update_shape()

        self.layer.add(self.images.draw_square((int_val(40), int_val(30)), self.size, 0))
        self.layer.draw(canvas)
        self.layer.empty()

        self.update_hud(canvas)