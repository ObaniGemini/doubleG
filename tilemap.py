import pygame

from screen import *
from collision import *



class Tile:

    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.shape = SquareCollision(pygame.Rect(self.pos[0] - self.size, self.pos[1] - self.size, self.pos[0] + self.size, self.pos[0] + self.size))


    def draw_tile(self, tiles_pos, canvas):
        array_x = []
        array_y = []
        for i in tiles_pos:
            array_x.append(i[0])
            array_y.append(i[1])

        size = self.size

        if not (self.pos[0] - size*2) in array_x:
            pygame.draw.line(canvas, pygame.Color(0, 0, 0), ((self.pos[0] - size), (self.pos[1] - size)), ((self.pos[0] - size), (self.pos[1] + size)), 1)
        if not (self.pos[0] + size*2) in array_x:
            pygame.draw.line(canvas, pygame.Color(0, 0, 0), ((self.pos[0] + size), (self.pos[1] - size)), ((self.pos[0] + size), (self.pos[1] + size)), 1)
        if not (self.pos[1] - size*2) in array_y:
            pygame.draw.line(canvas, pygame.Color(0, 0, 0), ((self.pos[0] - size), (self.pos[1] - size)), ((self.pos[0] + size), (self.pos[1] - size)), 1)
        if not (self.pos[1] + size*2) in array_y:
            pygame.draw.line(canvas, pygame.Color(0, 0, 0), ((self.pos[0] - size), (self.pos[1] + size)), ((self.pos[0] + size), (self.pos[1] + size)), 1)




class TileMap:

    def __init__(self, camera):
        self.tiles = []
        self.tiles_pos = []
        self.updated = False
        self.spawn_pos = (0,0)
        self.camera = camera
        self.size = int_val(4)


    def add_square_tile(self, pos):
        if not pos in self.tiles_pos:
            self.tiles_pos.append(pos)
            self.tiles.append(Tile(pos, self.size))


    def draw_square_tiles(self, canvas):
        for tile in self.tiles:
            tile.draw_tile(self.tiles_pos, canvas)


    def convert_file(self):
        FILE = open('levels/level_1.txt','r')
        level_text = [list(line.replace('\n','')) for line in FILE]
        FILE.close()

        v_size = len(level_text)
        h_size = len(level_text[0])

        i = 0
        while i < v_size:
            line = level_text.pop(0)
            j = 0
            while j < h_size:
                column = line.pop(0)
                pos = (self.size+self.size*j*2, self.size+self.size*i*2)
                if column == 'x':
                    self.add_square_tile(pos)
                if column == 'V':
                    self.spawn_pos = pos
                j += 1
            i += 1
        self.canvas = pygame.Surface((self.size*2*(h_size+1), self.size*2*(v_size+1)), pygame.SRCALPHA)
        self.canvas.convert()
        self.draw_square_tiles(self.canvas)
        self.updated = True


    def get_spawn(self):
        return self.spawn_pos


    def update(self, canvas, player):
        checked = False
        for tile in self.tiles:
            if not checked:
                if tile.shape.is_colliding(player.get_shape()):
                    checked = True
                    player.colliding = True
        if not checked:
            player.colliding = False

        canvas.blit(self.canvas, self.camera.pos)