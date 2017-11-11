import pygame

from screen import *



class Tile:

    def __init__(self, index, size):
        self.index = index
        self.size = size


    def draw_tile(self, tiles_index, canvas):
        array_x = []
        array_y = []
        for i in tiles_index:
            array_x.append(i[0])
            array_y.append(i[1])

        pos_x = (self.index[0]*self.size)
        pos_y = (self.index[1]*self.size)
        color = pygame.Color(0, 0, 0)

#        if not self.index[0] in array_x:
        pygame.draw.line(canvas, color, (pos_x, pos_y), (pos_x, (pos_y + self.size)), 1)
#        if not (self.index[0] + 1) in array_x:
        pygame.draw.line(canvas, color, (pos_x, pos_y), ((pos_x + self.size), pos_y), 1)
#        if not self.index[1] in array_y:
        pygame.draw.line(canvas, color, ((pos_x + self.size), pos_y), ((pos_x + self.size), (pos_y + self.size)), 1)
#        if not (self.index[1] + 1) in array_y:
        pygame.draw.line(canvas, color, (pos_x, (pos_y + self.size)), ((pos_x + self.size), (pos_y + self.size)), 1)




class TileMap:

    def __init__(self, camera):
        self.tiles = []
        self.tiles_index = []
        self.updated = False
        self.spawn_pos = (0,0)
        self.camera = camera
        self.size = int_val(8)


    def add_square_tile(self, index):
        if not index in self.tiles_index:
            self.tiles_index.append(index)
            self.tiles.append(Tile(index, self.size))


    def draw_square_tiles(self, canvas):
        for tile in self.tiles:
            tile.draw_tile(self.tiles_index, canvas)


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
                index = (j, i)
                if column == 'x':
                    self.add_square_tile(index)
                if column == 'V':
                    self.spawn_pos = (self.size+index[0]*self.size, self.size+index[1]*self.size)
                j += 1
            i += 1
        self.canvas = pygame.Surface((self.size*(h_size+1), self.size*(v_size+1)), pygame.SRCALPHA)
        self.canvas.convert()
        self.draw_square_tiles(self.canvas)
        self.updated = True


    def get_spawn(self):
        return self.spawn_pos


    def update(self, canvas, player):

        for i in range(4):
            player.can_move[i] = True

        left, right, up, down = 0, 1, 2, 3

        x0 = int(player.next_pos[0]/self.size)

        x_left1 = int((player.pos[0] - player.size - int_val(1/2))/self.size)
        x_left2 = int((player.next_pos[0] - player.size - int_val(1/2))/self.size)

        x_right1 = int((player.pos[0] + player.size + int_val(1/2))/self.size)
        x_right2 = int((player.next_pos[0] + player.size + int_val(1/2))/self.size)

        y0 = int(player.next_pos[1]/self.size)

        y_up1 = int((player.pos[1] - player.size - int_val(1/2))/self.size)
        y_up2 = int((player.next_pos[1] - player.size - int_val(1/2))/self.size)

        y_down1 = int((player.pos[1] + player.size + int_val(1/2))/self.size)
        y_down2 = int((player.next_pos[1] + player.size + int_val(1/2))/self.size)
        

        for index in self.tiles_index:
            if x0 == index[0]:
                if (y_up1 >= index[1] and y_up2 <= index[1]):
                    player.can_move[up] = False
                    player.collider[up] = index[1]
                if (y_down1 <= index[1] and y_down2 >= index[1]):
                    player.can_move[down] = False
                    player.collider[down] = index[1]
            if y0 == index[1]:
                if (x_left1 > index[0] and x_left2 <= index[0]):
                    player.can_move[left] = False
                    player.collider[left] = index[0]
                if (x_right1 <= index[0] and x_right2 >= index[0]):
                    player.can_move[right] = False
                    player.collider[right] = index[0]

        player.update_player(canvas)

        canvas.blit(self.canvas, self.camera.pos)