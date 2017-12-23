import pygame

from sound import *
from screen import *
from shapes import *
from random import *



class Player:

    def __init__(self, spawn_pos, camera):
        self.spawned = False
        self.anim_step = 20
        self.random_speed = []
        for i in range(0, 6):
            self.random_speed.append(randint(-40, 40))

        self.pos = spawn_pos
        self.next_pos = spawn_pos        #used for collision checks
        self.spawn_pos = spawn_pos

        self.size = int_val(1)
        self.camera = camera
        
        self.can_move = [True, True, True, True]
        self.collider = [0, 0, 0, 0]
        self.force = (0.0, 0.0)

        self.jetpack_cooldown = False
        self.jetpack_fuel = 0
        self.jetpack_playing = False

        self.angle = 0

        for name in ["jump", "jetpack", "jetpack_out"]:
            add_sound(name)

        set_volume("jetpack", 0.7)
        set_volume("jetpack_out", 0.6)

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
        return (self.force[0]//1000, self.force[1]//1000)

    def apply_impulse(self, x, y):
        self.force = (self.force[0] + int_val(x*1000), self.force[1] + int_val(y*1000))


    def is_pressed(self, key_enum):
        if pygame.key.get_pressed()[key_enum] == 1:
            return True


    def use_jetpack(self, strength):
        if not self.jetpack_cooldown:
            if self.jetpack_fuel > 0:
                if not self.jetpack_playing:
                    self.jetpack_playing = True
                    play_sound("jetpack")
                self.apply_impulse(0, strength)
                self.jetpack_fuel -= 4
                if self.jetpack_fuel < 0:
                    play_sound("jetpack_out")
            else:
                self.jetpack_cooldown = True

    def update(self):
        left, right, up, down = 0, 1, 2, 3

        if (not self.can_move[down] and self.force[1] >= 0) or (not self.can_move[up] and self.force[1] <= 0):
            self.force = (self.force[0], 0)
        side = 0

        if self.spawned:
            if self.is_pressed(pygame.K_LEFT) and self.can_move[left]:
                side = -1
            if self.is_pressed(pygame.K_RIGHT) and self.can_move[right]:
                side += 1

        if side == 0 or (side == 1 and self.force[0] < 0) or (side == -1 and self.force[0] > 0):
            self.force = (self.force[0]-self.force[0]//4, self.force[1])
        if side == 0 or abs(self.angle) == 80:
            if abs(self.angle) <= 80 and self.angle != 0:
                self.angle += 16 * (self.angle/abs(self.angle))
            else:
                self.angle = 0
        else:
            self.angle += 16*side

        if abs(self.force[0]) < 10000:
            self.apply_impulse(0.3*side, 0)

        pressed = False
        if self.spawned:
            if self.is_pressed(pygame.K_UP) and self.can_move[up]:
                if self.can_move[down]:
                    pressed = True
                    self.use_jetpack(-0.25)
                else:
                    play_sound("jump")
                    self.apply_impulse(0, -2.5)

        if self.is_pressed(pygame.K_DOWN) and self.can_move[down]:
            pressed = True
            self.use_jetpack(0.25)

        if self.jetpack_fuel < 76:
            if (not pressed or self.jetpack_cooldown) and self.jetpack_playing:
                self.jetpack_playing = False
                stop_sound("jetpack")
            self.jetpack_fuel += 1
        elif self.jetpack_fuel == 76:
            self.jetpack_cooldown = False



        if self.can_move[down]:
            self.apply_impulse(0, 0.15)

        if self.is_pressed(pygame.K_RETURN):
            self.force = (0, 0)

        self.next_pos = self.update_pos(self.pos, self.update_force())


    def update_hud(self, canvas):
        if self.jetpack_fuel > 0:
            taint = pygame.Color(40+int(200-self.jetpack_fuel*(5/2)), 40+int(40-self.jetpack_fuel/2), 40, 150)
            if not self.jetpack_cooldown:
                taint = pygame.Color(40, 40+80-self.jetpack_fuel, 40+int(120-self.jetpack_fuel*(3/2)), 150)

            x0, y0 = canvas.get_width(), canvas.get_height()
            x1, x2 = int_val(self.jetpack_fuel), int_val(4)
            y1, y2 = int_val(4), int_val((self.jetpack_fuel/76*56))
            for i in [(0, 0), (x0-x1, y0-y1)]:
                jetpack = pygame.Surface((x1, y1), pygame.SRCALPHA)
                jetpack.fill(taint)
                canvas.blit(jetpack, i)
            for i in [(0, y0-y2), (x0-x2, 0)]:
                jetpack = pygame.Surface((x2, y2), pygame.SRCALPHA)
                jetpack.fill(taint)
                canvas.blit(jetpack, i)


    def update_player(self, canvas):
        left, right, up, down = 0, 1, 2, 3

        if not self.can_move[left] and self.force[0] < 0:#self.next_pos[0] < self.pos[0]:
            self.next_pos = (((self.collider[left]+1)*int_val(8)+self.size+int_val(1/2)), self.next_pos[1])
        if not self.can_move[right] and self.force[0] > 0:#self.next_pos[0] > self.pos[0]:
            self.next_pos = ((self.collider[right]*int_val(8)-self.size-int_val(1/2)), self.next_pos[1])
        if not self.can_move[up] and self.force[1] < 0:#self.next_pos[1] < self.pos[1]:
            self.next_pos = (self.next_pos[0], ((self.collider[up]+1)*int_val(8)+self.size+int_val(1/2)))
        if not self.can_move[down] and self.force[1] > 0:#self.next_pos[1] > self.pos[1]:
            self.next_pos = (self.next_pos[0], (self.collider[down]*int_val(8)-self.size-int_val(1/2)))

        self.pos = self.next_pos
        self.camera.update_to((self.pos[0]-int_val(40), self.pos[1]-int_val(30)))
        self.update_shape()

        if self.spawned:
            draw_square(canvas, self.size, self.angle, (int_val(40)-self.size*2, int_val(30)-self.size*2))
        else:
            if self.anim_step >= 1:
                for i in range(1, 6):
                    draw_square(canvas, int(self.size*(self.anim_step/8)*i), self.angle+self.anim_step*self.random_speed[i-1], (int_val(40)-self.size*(self.anim_step/4)*i, int_val(30)-self.size*(self.anim_step/4)*i))
            else:
                draw_square(canvas, self.size, self.angle, (int_val(40)-self.size*2, int_val(30)-self.size*2))

            self.anim_step -= 1
            if self.anim_step == -2:
                self.spawned = True