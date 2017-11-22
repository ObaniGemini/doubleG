#!/usr/bin/python3

import pygame

from screen import *
from bg_anim import *
from transitions import *

from world import *
from menu import *


class Main:

    def __init__ (self):
        pygame.init()

        self.size = (int_val(80), int_val(60))
        self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        self.signal = ""
        pygame.display.set_caption('DoubleG masterace gemplay OMGWTFBDSMHAX')

        self.background_canvas = pygame.Surface(self.size)
        self.background = BackgroundAnim(self.background_canvas)
        
        self.main_canvas = pygame.Surface(self.size, pygame.SRCALPHA)

        self.transition = Transition()
        
        self.background_canvas.convert()
        self.main_canvas.convert()
        self.mixer = pygame.mixer
        self.mixer.init(frequency=11025, size=-8, channels=1, buffer=128)



    def update_screen(self, fullscreen):
        if fullscreen:
            self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        


    def run (self):
        done = False
        fullscreen = False
        timer = pygame.time
        self.scene = Menu(self.main_canvas)
        switching = False

        while not done:
            saving = False

            self.background.anim_2()

            self.main_canvas = pygame.Surface(self.size, pygame.SRCALPHA)

            if switching:
                if self.signal == "Start Menu":
                    self.scene = Menu(self.main_canvas)
                elif self.signal == "Start Game":
                    self.scene = World(self.main_canvas)
                elif self.signal == "Restart":
                    self.scene = World(self.main_canvas)
                switching = False
                self.signal = ""

            self.scene.update(self.main_canvas)

            if self.scene.signal == "Play":
                self.signal = "Start Game"
            elif self.scene.signal == "Restart":
                self.signal = "Restart"
            elif self.scene.signal == "Quit Game":
                self.signal = "Start Menu"
            elif self.scene.signal == "Quit":
                self.signal = "Quit"
            elif self.scene.signal == "Force Quit":
                self.signal = "Force Quit"
            elif self.scene.signal == "Display Mode":
                fullscreen = not fullscreen
                self.update_screen(fullscreen)
            elif self.scene.signal == "Save Screen":
                saving = True


            if self.transition.state == "Started":
                self.transition.anim(self.main_canvas)
            elif self.transition.state == "Start":
                self.transition.type = "Open"
                self.transition.anim(self.main_canvas)
            elif self.transition.state == "" and (self.signal == "Quit" or self.signal == "Start Game" or self.signal == "Start Menu" or self.signal == "Restart"):
                self.transition.type = "Close"
                self.transition.anim(self.main_canvas)
            elif self.transition.state == "" and self.transition.type == "Close":
                self.transition.type = "Open"
                self.transition.anim(self.main_canvas)


            if self.transition.state == "Ended":
                if self.signal == "Quit":
                    done = True
                elif self.signal == "Start Game" or self.signal == "Start Menu" or self.signal == "Restart":
                    switching = True
                self.transition.state = ""

            if self.signal == "Force Quit":
                done = True

            timer.wait(10) #Sets the speed of execution of the game
            
            self.window.blit(self.background_canvas, (0, 0))
            self.window.blit(self.main_canvas, (0, 0))

            if saving:
                pygame.image.save(self.window, "saved_image.png")
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.run()