#!/usr/bin/python3

import pygame

from screen import *
from bg_anim import *
from world import *
from menu import *


class Main:

    def __init__ (self):
        pygame.init()

        self.size = (int_val(80), int_val(60))
        self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        pygame.display.set_caption('DoubleG masterace gemplay OMGWTFBDSMHAX')

        self.background_canvas = pygame.Surface(self.size)
        self.background = BackgroundAnim(self.background_canvas)
        
        self.main_canvas = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.background_canvas.convert()
        self.main_canvas.convert()



    def update_screen(self, fullscreen):
        if fullscreen:
            self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        


    def run (self):
        done = False
        fullscreen = False
        timer = pygame.time
        
        menu = True
        switching = False
        self.scene = Menu(self.main_canvas)

        while not done:
            self.main_canvas = pygame.Surface(self.size, pygame.SRCALPHA)
            if menu and switching:
                self.scene = Menu(self.main_canvas)
            elif not menu and switching:
                self.scene = World(self.main_canvas)
            switching = False

            self.scene.update(self.main_canvas)
            
            if self.scene.signal == "Play":
                switching = True
                menu = False
            elif self.scene.signal == "Quit":
                if menu:
                    done = True
                else:
                    switching = True
                    menu = True
            elif self.scene.signal == "Force Quit":
                done = True
            elif self.scene.signal == "Display Mode":
                fullscreen = not fullscreen
                self.update_screen(fullscreen)

            self.background.anim_2()

            timer.wait(10) #Sets the speed of execution of the game
            
            self.window.blit(self.background_canvas, (0, 0))
            self.window.blit(self.main_canvas, (0, 0))
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.run()