import pygame

from sound import *
from screen import *
from random import *
from shapes import *
from tiles import *



class TileMap:

    def __init__(self, camera):
        self.updated = False
        self.spawn_pos = (0,0)
        self.camera = camera
        self.size = int_val(8)

        self.goals = None
        self.signal = ""

        for name in ["jumppad", "pickup1", "pickup2", "pickup3"]:
            add_sound(name)

        set_volume("jumppad", 0.75)


    def add_tile(self, tile, index):
        if tile == "square":
            if not index in self.tiles_index:
                self.tiles_index.append(index)
                self.tiles.append(Tile(index, self.size))
        elif tile == "lava":
            if not index in self.lava_tiles_index:
                self.lava_tiles_index.append(index)
                self.lava_tiles.append(Lava(index, self.size))
        elif tile == "jumppad":
            self.jumppad_tiles.append(Jumppad(index, self.size, 5))
            self.tiles_index.append(index)
        elif "repulsiveH" in tile:
            side = 1
            if "left" in tile:
                side = -1
            self.repulsive_tiles.append(RepulsiveHorizontal(index, self.size, side))
        elif "repulsiveV" in tile:
            side = 1
            if "up" in tile:
                side = -1
            self.repulsive_tiles.append(RepulsiveVertical(index, self.size, side))



    def draw_square_tiles(self):
        for tile in self.tiles:
            tile.draw_tile(self.tiles_index)
        for tile in self.jumppad_tiles:
            tile.draw_tile()
        for layer in self.decor_tiles:
            layer_index = self.decor_tiles.index(layer)
            for tile in layer:
                tile.draw_tile(self.decor_tiles_index[layer_index], True)



    def convert_file(self, level):
        FILE = open('levels/level_'+str(level)+'.txt','r')
        level_text = [list(line.replace('\n','')) for line in FILE]
        FILE.close()

        self.tiles = []
        self.tiles_index = []

        self.lava_tiles = []
        self.lava_tiles_index = []

        self.jumppad_tiles = []

        self.repulsive_tiles = []

        self.decor_tiles = []
        self.decor_tiles_index = []

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
                    self.add_tile("square", index)
                elif column == 'L':
                    self.add_tile("lava", index)
                elif column == 'J':
                    self.add_tile("jumppad", index)
                elif column == 'l':
                    self.add_tile("repulsiveH_left", index)
                elif column == 'r':
                    self.add_tile("repulsiveH_right", index)
                elif column == 'u':
                    self.add_tile("repulsiveV_up", index)
                elif column == 'd':
                    self.add_tile("repulsiveV_down", index)
                elif column == 'V':
                    self.spawn_pos = (index[0]*self.size+self.size//2, index[1]*self.size+self.size//2)
                elif column == 'G':
                    goals.insert(0, (index))
                elif column == 'K':
                    goals.append(index)
                j += 1
            i += 1

        size = 0
        while size < Screen.decors:
            size += 1
            self.decor_tiles.append([])
            self.decor_tiles_index.append([])
            for i in range(self.v_size):
                for j in range(h_size):
                    index = (i, j)
                    if randint(0, 20*int((size+1)/2)) == 0:
                        self.decor_tiles[size-1].append(Tile(index, self.size*((1*size)/2)))
                        self.decor_tiles_index[size-1].append(index)




        if len(goals) != 0:
            self.goals = Goals(goals, self.size)
        self.draw_square_tiles()
        self.updated = True


    def get_spawn(self):
        return self.spawn_pos


    def update(self, canvas, player):
        self.signal = ""

        for layer in self.decor_tiles:
            layer_index = self.decor_tiles.index(layer)+2
            for tile in layer:
                canvas.blit(tile.canvas, (tile.index[0]*tile.size+self.camera.pos[0]//layer_index, tile.index[1]*tile.size+self.camera.pos[1]//layer_index))

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
        
        collider = [-1, -1, -1, -1]
        colliding = [False, False, False, False]

        for type in [self.tiles, self.jumppad_tiles]:
            for tile in type:
                index = tile.index
                if x0 == index[0]:
                    if (y_up1 >= index[1] and y_up2 <= index[1]) and (collider[up] <= index[1] or collider[up] == -1):
                        player.can_move[up] = False
                        player.collider[up] = index[1]
                        collider[up] = index[1]
                    if (y_down1 <= index[1] and y_down2 >= index[1]) and (collider[down] >= index[1] or collider[down] == -1):
                        player.can_move[down] = False
                        player.collider[down] = index[1]
                        collider[down] = index[1]
                        if tile.name == "jumppad":
                            player.apply_impulse(0, -tile.strength)
                            play_sound("jumppad")
                            play_sound("jumppad")
                if y0 == index[1]:
                    if (x_left1 >= index[0] and x_left2 <= index[0]) and (collider[left] <= index[0] or collider[left] == -1):
                        player.can_move[left] = False
                        player.collider[left] = index[0]
                        collider[left] = index[0]
                    if (x_right1 <= index[0] and x_right2 >= index[0]) and (collider[right] >= index[0] or collider[right] == -1):
                        player.can_move[right] = False
                        player.collider[right] = index[0]
                        collider[right] = index[0]

        dead = False
        for tile in self.lava_tiles:
            index = tile.index
            if x0 == index[0]:
                if player.next_pos[1]//self.size == index[1] or (player.next_pos[1]+1)//self.size == index[1]:
                    dead = True
            if y0 == index[1]:
                if player.next_pos[0]//self.size == index[0] or (player.next_pos[0]+1)//self.size == index[0]:
                    dead = True

        for tile in self.repulsive_tiles:
            index = tile.index
            if "horizontal" in tile.name:
                if y0 == index[1]:
                    if tile.side == 1 and (player.next_pos[0]//self.size >= index[0] and player.next_pos[0]//self.size <= (index[0]+3)):
                        player.apply_impulse(1, 0)
                    if tile.side == -1 and (player.next_pos[0]//self.size >= (index[0]-3) and player.next_pos[0]//self.size <= index[0]):
                        player.apply_impulse(-1, 0)
            elif "vertical" in tile.name:
                if x0 == index[0]:
                    if tile.side == 1 and (player.next_pos[1]//self.size >= index[1] and player.next_pos[1]//self.size <= (index[1]+3)):
                        player.apply_impulse(0, 1)
                    if tile.side == -1 and (player.next_pos[1]//self.size >= (index[1]-3) and player.next_pos[1]//self.size <= index[1]):
                        player.apply_impulse(0, -1)


        player.update_player(canvas)
        for tile in self.lava_tiles:
            canvas.blit(tile.update([self.lava_tiles_index, self.tiles_index], self.camera.pos), tile.pos)

        for tile in self.tiles:
            canvas.blit(tile.canvas, (tile.index[0]*tile.size+self.camera.pos[0], tile.index[1]*tile.size+self.camera.pos[1]))

        for tile in self.jumppad_tiles:
            canvas.blit(tile.canvas, (tile.index[0]*tile.size+self.camera.pos[0], tile.index[1]*tile.size+self.camera.pos[1]))
            tile.update(canvas, self.camera.pos)

        for tile in self.repulsive_tiles:
            tile.update(canvas, self.camera.pos)
        player.next_pos = player.update_pos(player.next_pos, player.update_force())

        if len(self.goals.keys) != 0:
            for index in self.goals.keys:
                if index == (player.pos[0]//self.size, player.pos[1]//self.size):
                    if len(self.goals.keys) == 1 or self.goals.keys.index(index) != 0:
                        if len(self.goals.keys) != 1:
                            play_sound("pickup"+str(randint(1, 3)))
                        del self.goals.keys[self.goals.keys.index(index)]

        if self.goals != None and self.updated:
            if self.goals.keys != []:
                self.goals.update(canvas, self.camera.pos)
            else:
                self.updated = False
                self.signal = "End"

        if player.pos[1]//self.size > (self.v_size+4) or dead:
            self.signal = "Die"

        player.update_hud(canvas)