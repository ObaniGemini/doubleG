import pygame

from screen import *



class Transition:

    def __init__(self):
        self.state = "Start"
        self.type = ""
        self.value = 0
        self.r, self.g, self.b = 0, 0, 0


    def anim(self, canvas):
        if self.state == "Start" or self.state == "":
            self.state = "Started"
            self.smoothing = 63
            self.value = 0
            if self.type == "Open":
                self.value = int_val(80)

        if self.type == "Close":
            self.value += int_val(self.smoothing)//8
            r, g, b = int(self.r*189), int(self.g*189), int(self.b*189)
        elif self.type == "Open":
            self.value -= int_val(self.smoothing)//8
            r, g, b = int(self.r*(self.smoothing*3)), int(self.g*(self.smoothing*3)), int(self.b*(self.smoothing*3))

        if self.state == "Started":
            if self.value >= int_val(80):
                self.value = int_val(80)
                self.state = "Ended"
            elif self.value <= 0:
                self.value = 0
                self.state = "Ended"
                self.r, self.g, self.b = 0, 0, 0

        if self.smoothing > 0:
            self.smoothing -= 3

        surface = pygame.Surface((self.value, int_val(60)))
        surface.fill(pygame.Color(r, g, b))
        canvas.blit(surface, (0, 0))