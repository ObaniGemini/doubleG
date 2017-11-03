import pygame

from screen import *




class Button:

    def __init__(self, pos, text, left_padding):
        self.pos = pos
        self.size = (int_val(32), int_val(16))
        self.left_padding = left_padding
        
        font = pygame.font.SysFont("Comic Sans MS", int(self.size[1]/2))
        self.text = label = font.render(text, 1, pygame.Color(0, 0, 0, 255))

        self.hovered = False
        self.taint = 20


    def update(self):
        if self.hovered and self.taint < 120:
            self.taint += 4
        elif not self.hovered and self.taint > 20:
            self.taint -= 4
        
        self.canvas = pygame.Surface(self.size, pygame.SRCALPHA)
        self.canvas.fill(pygame.Color(0, 0, 0, self.taint))
        self.canvas.blit(self.text, (self.left_padding, (self.size[1]/4)+int_val(1)))




class Menu:

    def __init__(self, canvas):
        self.canvas = canvas
        self.buttons = []
        self.add_button((int_val(24), int_val(10)), "Play", int_val(10))
        self.add_button((int_val(24), int_val(30)), "Quit", int_val(10))


    def add_button(self, pos, text, left_padding):
        self.buttons.append([Button(pos, text, left_padding), text])


    def update(self, canvas):
        self.signal = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.signal = "Quit"
            elif event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_ESCAPE:
                    self.signal = "Quit"
                elif k == pygame.K_F11:
                    fullscreen = not fullscreen
                    self.update_screen(fullscreen)

            for button_array in self.buttons:
                button = button_array[0]
                moving = False
                if event.type == pygame.MOUSEMOTION:
                    if event.pos[0] > button.pos[0] and event.pos[0] < (button.pos[0] + button.size[0]) and event.pos[1] > button.pos[1] and event.pos[1] < (button.pos[1] + button.size[1]):
                        button.hovered = True
                        moving = True
                    
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.hovered and event.button == 1:
                        if button_array[1] == "Play":
                            self.signal = "Play"
                        elif button_array[1] == "Quit":
                            self.signal = "Quit"
                
                if not moving:
                    button.hovered = False
        
        for button_array in self.buttons:
            button = button_array[0]
            button.update()
            canvas.blit(button.canvas, button.pos)
