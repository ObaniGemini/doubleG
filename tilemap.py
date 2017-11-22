import pygame

from screen import *
from random import *
from shapes import *



class Tile:

    def __init__(self, index, size):
        self.index = index
        self.size = size


    def draw_tile(self, tiles_index):
        array_x = []
        array_y = []
        for i in tiles_index:
            array_x.append(i[0])
            array_y.append(i[1])

        color = pygame.Color(0, 0, 0)
        black = pygame.Color(0, 0, 0)

        self.canvas = pygame.Surface((self.size+1, self.size+1))

        draw_rect(self.canvas, self.size, (0, 0), randint(100, 150), randint(100, 150), randint(100, 150))
        pygame.draw.line(self.canvas, black, (0, 0), (self.size, 0), 1)
        pygame.draw.line(self.canvas, black, (self.size, 0), (self.size, self.size), 1)
        pygame.draw.line(self.canvas, black, (self.size, self.size), (0, self.size), 1)
        pygame.draw.line(self.canvas, black, (0, self.size), (0, 0), 1)




class Goals:

    def __init__(self, indexes, size):
        self.keys = []
        self.key_colors = []
        for i in indexes:
            self.keys.append(i)
            self.key_colors.append([randint(50, 150), randint(50, 150), randint(50, 150)])

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




class TileMap:

    def __init__(self, camera):
        self.tiles = []
        self.tiles_index = []
        self.updated = False
        self.spawn_pos = (0,0)
        self.camera = camera
        self.size = int_val(8)

        self.goals = None
        self.signal = ""


    def add_square_tile(self, index):
        if not index in self.tiles_index:
            self.tiles_index.append(index)
            self.tiles.append(Tile(index, self.size))


    def draw_square_tiles(self):
        for tile in self.tiles:
            tile.draw_tile(self.tiles_index)


    def convert_file(self):
        FILE = open('levels/level_1.txt','r')
        level_text = [list(line.replace('\n','')) for line in FILE]
        FILE.close()

        i = 0
        goals = []
        self.v_size = len(level_text)
        h_size = len(level_text[0])
        self.goals = None

        while i < self.v_size:
            line = level_text.pop(0)
            j = 0
            while j < h_size:
                column = line.pop(0)
                index = (j, i)
                if column == 'x':
                    self.add_square_tile(index)
                elif column == 'V':
                    self.spawn_pos = (self.size+index[0]*self.size, self.size+index[1]*self.size)
                elif column == 'G':
                    goals.insert(0, (index))
                elif column == 'K':
                    goals.append(index)
                j += 1
            i += 1

        if len(goals) != 0:
            self.goals = Goals(goals, self.size)
        self.draw_square_tiles()
        self.updated = True


    def get_spawn(self):
        return self.spawn_pos


    def update(self, canvas, player):

        for i in range(4):
            player.can_move[i] = True

        left, right, up, down = 0, 1, 2, 3

        x0 = player.next_pos[0]//self.size

        x_left1 = (player.pos[0] - player.size - int_val(1/2))//self.size
        x_left2 = (player.next_pos[0] - player.size - int_val(1/2))//self.size

        x_right1 = (player.pos[0] + player.size + int_val(1/2))/self.size
        x_right2 = (player.next_pos[0] + player.size + int_val(1/2))/self.size

        y0 = player.next_pos[1]//self.size

        y_up1 = (player.pos[1] - player.size - int_val(1/2))//self.size
        y_up2 = (player.next_pos[1] - player.size - int_val(1/2))//self.size

        y_down1 = (player.pos[1] + player.size + int_val(1/2))//self.size
        y_down2 = (player.next_pos[1] + player.size + int_val(1/2))//self.size
        
        collider = [0, 0, 0, 0]

        for tile in self.tiles:
            index = tile.index
            if x0 == index[0]:
                if (y_up1 >= index[1] and y_up2 <= index[1]):
                    player.can_move[up] = False
                    player.collider[up] = index[1]
                    collider[up] = index[1]
                if (y_down1 <= index[1] and y_down2 >= index[1]):
                    player.can_move[down] = False
                    player.collider[down] = index[1]
                    collider[down] = index[1]
            if y0 == index[1]:
                if (x_left1 >= index[0] and x_left2 <= index[0]):
                    player.can_move[left] = False
                    player.collider[left] = index[0]
                    collider[left] = index[0]
                if (x_right1 <= index[0] and x_right2 >= index[0]):
                    player.can_move[right] = False
                    player.collider[right] = index[0]
                    collider[right] = index[0]
            canvas.blit(tile.canvas, (tile.index[0]*tile.size+self.camera.pos[0], tile.index[1]*tile.size+self.camera.pos[1]))

        if len(self.goals.keys) != 0:
            for index in self.goals.keys:
                if index == (player.pos[0]//self.size, player.pos[1]//self.size):
                    if len(self.goals.keys) == 1 or self.goals.keys.index(index) != 0:
                        del self.goals.keys[self.goals.keys.index(index)]

        if self.goals != None:
            if self.goals.keys != []:
                self.goals.update(canvas, self.camera.pos)
            else:
                self.signal = "End"

        if player.pos[1]//self.size > (self.v_size+4):
            self.signal = "Die"
        player.update_player(canvas)