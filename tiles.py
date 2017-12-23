import pygame

from math import *
from screen import *
from random import *
from shapes import *


"""
File containing all the Tiles classes :

If a class contains the "update()" function, that's it is animated

- Tile : A simple Tile drawn one time
- Goals : one class instancing all the Goals/Keys to be drawn in one time
- Lava : An animated lava tile
- Repulsive : An invisible tile just visible by its "repulsive" animation
"""



class Tile:

    def __init__(self, index, size):
        self.index = index
        self.size = size
        self.name = "tile"

    def draw_tile(self, tiles_index, decor=False):
        black = pygame.Color(0, 0, 0)

        alpha = 255
        if decor:
            alpha = 100
            self.canvas = pygame.Surface((self.size+1, self.size+1), pygame.SRCALPHA)
        else:
            self.canvas = pygame.Surface((self.size+1, self.size+1))
        rand = randint(100, 125)

        draw_rect(self.canvas, self.size, (0, 0), rand, rand, rand, alpha)
        if not ((self.index[0], self.index[1]-1) in tiles_index):
            pygame.draw.line(self.canvas, black, (0, 0), (self.size, 0), 1)
        if not ((self.index[0]+1, self.index[1]) in tiles_index):
            pygame.draw.line(self.canvas, black, (self.size, 0), (self.size, self.size), 1)
        if not ((self.index[0], self.index[1]+1) in tiles_index):
            pygame.draw.line(self.canvas, black, (self.size, self.size), (0, self.size), 1)
        if not ((self.index[0]-1, self.index[1]) in tiles_index):
            pygame.draw.line(self.canvas, black, (0, self.size), (0, 0), 1)




class Goals:

    def __init__(self, indexes, size):
        self.keys = []
        self.key_colors = []
        for i in indexes:
            self.keys.append(i)
            self.key_colors.append([randint(25, 100), randint(25, 100), randint(25, 100)])

        self.size = size
        self.angle = 0

    def update(self, canvas, camera_pos):
        self.angle += 1
        if self.angle >= 360:
            self.angle = 0

        goal_pos = (self.keys[0][0]*self.size+camera_pos[0], self.keys[0][1]*self.size+camera_pos[1])

        for j in range(1,7):
            draw_square(canvas, self.size/4, self.angle*j, goal_pos)

        for i in range (1, len(self.keys)):
            col = self.key_colors[i]
            pos = (self.keys[i][0]*self.size+camera_pos[0], self.keys[i][1]*self.size+camera_pos[1])
            for j in range(1,4):
                draw_square(canvas, self.size/4, self.angle*j, pos, 0, col[0], col[1], col[2])
            draw_square(canvas, self.size/2, self.angle*i, (goal_pos[0]-self.size/2, goal_pos[1]-self.size/2), 0, col[0], col[1], col[2])




class Lava:

    def __init__(self, index, size):
        self.index = index
        self.size = size
        self.canvas = None
        self.name = "lava"

        #Animation stuff
        self.speed_factor = randint(5, 15)
        self.step = 0
        self.color_step = 0
        self.side = 1
        self.color_side = 2

    def update(self, tile_groups, camera_pos):
        self.pos = self.index[0]*self.size+camera_pos[0], self.index[1]*self.size+camera_pos[1]
        size = (self.size, self.size)

        if self.canvas == None:
            color = pygame.Color(255, 0, 0)
            self.canvas = pygame.Surface((self.size, self.size))
            self.canvas.fill(color)

        for tiles_index in tile_groups:
            if (self.index[0], self.index[1]-1) in tiles_index:
                self.pos = self.index[0]*self.size+camera_pos[0], self.index[1]*self.size+camera_pos[1]
                size = (self.size, self.size)
                break
            else:
                self.step += self.speed_factor*self.side

                if self.step >= self.size*4:
                    self.step = self.size*4
                    self.side = -1
                elif self.step <= 0:
                    self.step = 0
                    self.side = 1

                decal = (int_val(self.step)//self.size)
                size = (size[0], size[1]-decal)
                self.pos = self.pos[0], self.pos[1]+decal

        self.color_step += self.color_side

        if self.color_step >= 60:
            self.color_step = 60
            self.color_side = -2
        elif self.color_step <= 0:
            self.color_step = 0
            self.color_side = 2

        color = pygame.Color(255-self.color_step, 0, 0)
        self.canvas = pygame.Surface(size)
        self.canvas.fill(color)
        return self.canvas





class Jumppad:

    def __init__(self, index, size, strength):
        self.index = index
        self.size = size
        self.name = "jumppad"
        self.strength = strength
        self.step = 0


    def draw_tile(self):
        color1 = pygame.Color(50, 50, 50)

        self.canvas = pygame.Surface((self.size+1, self.size+1))
        self.canvas.fill(pygame.Color(200-self.strength*5, 200-self.strength*10, 200-self.strength*10))

        last = [0, 0]
        canvas = []
        for i in range(2):
            canvas.append(pygame.Surface((self.size, self.size//8)))
            canvas.append(pygame.Surface((self.size//8, self.size)))
        for i in canvas:
            i.fill(pygame.Color(200, 200, 200))
        canvas.append(pygame.Surface((self.size//2, self.size//2)))
        canvas[4].fill(pygame.Color(100, 100, 120))

        self.canvas.blit(canvas[0], (0, 0))
        self.canvas.blit(canvas[1], (self.size-self.size//8, 0))
        self.canvas.blit(canvas[2], (0, self.size-self.size//8))
        self.canvas.blit(canvas[3], (0, 0))
        self.canvas.blit(canvas[4], (self.size//4, self.size//4))


        for i in [self.size, self.size-self.size//8, self.size-self.size//4]:
            pygame.draw.line(self.canvas, color1, (self.size-i, self.size-i), (i, self.size-i), 1)
            pygame.draw.line(self.canvas, color1, (i, self.size-i), (i, i), 1)
            pygame.draw.line(self.canvas, color1, (i, i), (self.size-i, i), 1)
            pygame.draw.line(self.canvas, color1, (self.size-i, i), (self.size-i, self.size-i), 1)


    def update(self, canvas, camera_pos):
        self.step += 1
        if self.step < 10:
            for i in range(3):
                y_pos = self.index[1]*self.size+camera_pos[1]-int(((self.step*(i+1/2))/10)*self.size)
                pygame.draw.line(canvas, pygame.Color(i*50, i*50, 255), (self.index[0]*self.size+camera_pos[0], y_pos), ((self.index[0]+1)*self.size+camera_pos[0], y_pos), 1)
        if self.step > 25:
           self.step = 0



class RepulsiveHorizontal:

    def __init__(self, index, size, side):
        self.name = "repulsive horizontal"
        self.index = index
        self.size = size
        self.step = 0
        self.side = side

    def update(self, canvas, camera_pos):
        self.step += 1
        if abs(self.step) >= 8:
            self.step = 0

        for i in range(0, 8):
            x_pos = (self.index[0]+((1-self.side)//2))*self.size+int_val((self.step+i*8)/2)*self.side+camera_pos[0]
            y_size = int(((self.step + 8*i)/128)*self.size)
            pygame.draw.line(canvas, pygame.Color(randint(0, 200), randint(0, 200), randint(0, 200)), (x_pos, (self.index[1]*self.size)+y_size+camera_pos[1]), (x_pos, ((self.index[1]+1)*self.size)-y_size+camera_pos[1]), 1)


class RepulsiveVertical:

    def __init__(self, index, size, side):
        self.name = "repulsive vertical"
        self.index = index
        self.size = size
        self.step = 0
        self.side = side

    def update(self, canvas, camera_pos):
        self.step += 1
        if abs(self.step) >= 8:
            self.step = 0

        for i in range(0, 8):
            y_pos = (self.index[1]+((1-self.side)//2))*self.size+int_val((self.step+i*8)/2)*self.side+camera_pos[1]
            x_size = int(((self.step + 8*i)/128)*self.size)
            pygame.draw.line(canvas, pygame.Color(randint(0, 150), randint(0, 150), randint(0, 150)), ((self.index[0]*self.size)+x_size+camera_pos[0], y_pos), (((self.index[0]+1)*self.size)-x_size+camera_pos[0], y_pos), 1)