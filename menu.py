import pygame

from screen import *


class Button:

    def __init__(self, pos, text, left_padding):
        self.pos = pos
        self.size = (int_val(36), int_val(14))
        self.left_padding = left_padding
        self.shape = pygame.Rect(self.pos, self.size)
        
        font = pygame.font.SysFont("Comic Sans MS", int(self.size[1]/2))
        self.text = text 
        self.label = font.render(text, 1, pygame.Color(0, 0, 0, 255))

        self.hovered = False
        self.taint = 160


    def update(self):
        if self.hovered and self.taint > 120:
            self.taint -= 4
        elif not self.hovered and self.taint < 160:
            self.taint += 4
        
        self.canvas = pygame.Surface(self.size, pygame.SRCALPHA)
        self.canvas.fill(pygame.Color(self.taint, self.taint, self.taint))
        self.canvas.blit(self.label, (self.left_padding, (self.size[1]/4)+int_val(1)))




class CheckButton:
    def __init__(self, pos, texts, left_paddings):
        self.pos = pos
        self.sides = [Button(pos, texts[0], left_paddings[0]), Button(pos, texts[1], left_paddings[1])]
        self.current_side = 1
        self.flip_side()
        self.hovered = False



    def update(self):
        self.sides[self.current_side].hovered = self.hovered
        self.sides[self.current_side].update()
        self.canvas = self.sides[self.current_side].canvas

    def flip_side(self):
        if self.current_side == 0:
            self.current_side = 1
        else:
            self.current_side = 0
        self.text = self.sides[self.current_side].text
        self.shape = self.sides[self.current_side].shape




class Menu:

    def __init__(self, canvas):
        self.canvas = canvas
        self.buttons = []
        self.add_button((int_val(22), int_val(7)), "Play", int_val(12.75))
        self.add_button((int_val(22), int_val(23)), ["Fullscreen", "Windowed"], [int_val(5.5), int_val(5.5)], "checkbox")
        self.add_button((int_val(22), int_val(39)), "Quit", int_val(13))


    def add_button(self, pos, text, left_padding, type="button"):
        if type == "checkbox":
            self.buttons.append(CheckButton(pos, text, left_padding))
        else:
            self.buttons.append(Button(pos, text, left_padding))


    def update(self, canvas):
        self.signal = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.signal = "Force Quit"
            elif event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_ESCAPE:
                    self.signal = "Quit"
                elif k == pygame.K_F12:
                    self.signal = "Save Screen"

            for button in self.buttons:
                moving = False
                if event.type == pygame.MOUSEMOTION:
                    if button.shape.collidepoint(event.pos):
                        button.hovered = True
                        moving = True
                    
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.hovered and event.button == 1:
                        if button.text == "Play":
                            self.signal = "Play"
                        elif button.text == "Fullscreen" or button.text == "Windowed":
                            self.signal = "Display Mode"
                            button.flip_side()
                        elif button.text == "Quit":
                            self.signal = "Quit"
                
                if not moving:
                    button.hovered = False
        
        for button in self.buttons:
            button.update()
            canvas.blit(button.canvas, button.pos)