import pygame

from screen import *



class Label:

    def __init__(self, text, pos, size, font, color):
        self.pos = pos
        font = pygame.font.SysFont(font, int_val(size))
        self.canvas = font.render(text, 1, color)



class Button:

    def __init__(self, text, pos, size_x=32, size_y=14):
        self.pos = pos
        self.size = (int_val(size_x), int_val(size_y))
        self.shape = pygame.Rect(self.pos, self.size)
        
        self.text = text
        self.text_size = size_y
        if len(self.text)*4 > size_x:
            self.text_size = size_x//4 
        self.label = Label(text, (self.size[0]//2//len(self.text), self.size[1]//2//self.text_size*5), self.text_size, "Comic Sans MS", pygame.Color(0, 0, 0))

        self.hovered = False
        self.taint = 160


    def update(self):
        if self.hovered and self.taint > 120:
            self.taint -= 4
        elif not self.hovered and self.taint < 160:
            self.taint += 4
        
        self.canvas = pygame.Surface(self.size)
        self.canvas.fill(pygame.Color(self.taint, self.taint, self.taint))
        self.canvas.blit(self.label.canvas, self.label.pos)




class CheckButton:

    def __init__(self, texts, pos, size_x=32, size_y=14):
        self.pos = pos
        self.sides = [Button(texts[0], pos, size_x, size_y), Button(texts[1], pos, size_x, size_y)]
        self.current_side = 1
        self.flip_side()
        self.hovered = False


    def update(self):
        for side in self.sides:
            side.hovered = self.hovered
            side.update()
        self.canvas = self.sides[self.current_side].canvas


    def flip_side(self):
        self.current_side += 1
        if self.current_side > 1:
            self.current_side = 0
        self.text = self.sides[self.current_side].text
        self.shape = self.sides[self.current_side].shape




class Slider:

    def __init__(self, text, pos, size, scope, inital_value):
        self.text = text
        self.pos = pos
        self.width = size[0]
        self.height = size[1]
        self.scope = scope
        self.scale = scope[1] - scope[0]

        self.shape = pygame.Rect(self.pos, (self.width+self.height, self.height))
        self.value = inital_value

        self.taint = 100
        self.hovered = False


    def draw(self, canvas):
        last = [0, 0]
        for i in [[canvas.get_width()-1, 0], [canvas.get_width()-1, canvas.get_height()-1], [0, canvas.get_height()-1], [0, 0]]:
            pygame.draw.line(canvas, pygame.Color(20, 20, 20), (last[0], last[1]), (i[0], i[1]), 1)
            last = i


    def set_value(self, pos):
        value = int(((pos[0] - self.pos[0])/self.width)*self.scale)
        if value < self.scope[1] and value >= self.scope[0]: #value can be equal to lower of scope but not higher
            self.value = value
        return self.value



    def update(self):
        if self.hovered and self.taint > 40:
            self.taint -= 6
        elif not self.hovered and self.taint < 100:
            self.taint += 6

        self.canvas = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.line = pygame.Surface((self.width, self.height//2))
        self.line.fill(pygame.Color(100, 100, 100))

        self.square = pygame.Surface((self.height, self.height))
        self.square.fill(pygame.Color(100, self.taint, self.taint))

        self.label = Label(str(self.value), (self.height//8, self.height//5), self.height//int_val(1), "Comic Sans MS", pygame.Color(int(50*(self.value/self.scale))+200, int(50*((self.scale-self.value)/self.scale))+200, 200))

        self.draw(self.line)
        self.draw(self.square)
        self.square.blit(self.label.canvas, self.label.pos)

        self.canvas.blit(self.line, (0, self.height//4))
        self.canvas.blit(self.square, (int(((self.width-self.height)*self.value)/self.scale), 0))



