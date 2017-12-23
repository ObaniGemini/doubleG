import pygame
import time

from sound import *
from screen import *
from bg_anim import *
from transitions import *

from world import *
from menu import *


music = Music()

class Game:

    def __init__ (self):
        self.signal = ""

        self.size = (int_val(80), int_val(60))
        self.update_screen()

        self.background_canvas = pygame.Surface(self.size)
        self.background = BackgroundAnim(self.background_canvas)
        
        self.main_canvas = pygame.Surface(self.size, pygame.SRCALPHA)

        self.transition = Transition()

        for name in ["restart", "win1", "win2", "win3"]: #This doesn't seem to work, I have no idea why
            add_sound(name)

        self.max_level = 6
        
        self.background_canvas.convert()
        self.main_canvas.convert()

        self.scene = Menu(self.main_canvas, music.is_playing())
        self.run()



    def update_screen(self):
        if Screen.fullscreen:
            try:
                self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.FULLSCREEN)
            except:
                Screen.fullscreen = False
                print("Your screen isn't large enough for fullscreen ("+str(self.size[0])+"x"+str(self.size[1])+")")
                self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        else:
            self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)


    def run (self):
        done = False
        timer = pygame.time
        switching = False
        level = 1

        while not done:
            saving = False
            self.main_canvas = pygame.Surface(self.size, pygame.SRCALPHA)

            if switching:
                if self.signal == "Win":
                    level += 1
                    if level > self.max_level:
                        self.signal = "Start Menu"
                if self.signal == "Start Menu":
                    self.scene.clear()
                    self.scene = Menu(self.main_canvas, music.is_playing())
                    level = 1
                else:
                    self.scene.clear()
                    if not music.is_playing():
                        music.play("theme_1", -1)
                    self.scene = World(self.main_canvas, level)
                switching = False
                self.background.reset()
                self.signal = ""

            self.scene.update(self.main_canvas)
            if self.scene.name == "Menu":            
                self.background.anim_1()
            else:
                self.background.anim_2()

            if not (self.transition.state == "Started" or self.transition.state == "Ended"):
                if self.scene.signal == "Play":
                    self.signal = "Start Game"
                elif self.scene.signal == "Restart":
                    self.signal = "Restart"
                elif self.scene.signal == "Win":
                    self.signal = "Win"
                elif self.scene.signal == "Quit Game" or self.scene.signal == "Finish":
                    self.signal = "Start Menu"
                elif self.scene.signal == "Quit":
                    self.signal = "Quit"
                elif self.scene.signal == "Force Quit":
                    self.signal = "Force Quit"
                elif self.scene.signal == "Display Mode":
                    Screen.fullscreen = not Screen.fullscreen
                    self.update_screen()
                elif self.scene.signal == "Save Screen":
                    saving = True


            if self.transition.state == "Started":
                self.transition.anim(self.main_canvas)
            elif self.transition.state == "Start":
                self.transition.type = "Open"
                self.transition.anim(self.main_canvas)
            elif self.transition.state == "" and (self.signal == "Quit" or self.signal == "Start Game" or self.signal == "Start Menu" or self.signal == "Restart" or self.signal == "Win"):
                if self.signal == "Restart":
                    self.transition.r = 1
                    play_sound("restart")
                elif self.signal == "Win" or self.signal == "Finish":
                    self.transition.b = 0.25
                    self.transition.g = 0.1
                    play_sound("win"+str(randint(1, 3)))
                self.transition.type = "Close"
                self.transition.anim(self.main_canvas)
            elif self.transition.state == "" and self.transition.type == "Close":
                self.transition.type = "Open"
                self.transition.anim(self.main_canvas)


            if self.transition.state == "Ended":
                if self.signal == "Quit":
                    done = True
                elif self.signal in ["Start Game", "Start Menu", "Restart", "Win"]:
                    switching = True
                self.transition.state = ""


            if self.signal == "Force Quit":
                done = True
            elif type(self.scene.signal) == list:
                if self.scene.signal[0] == "Resolution":
                    Screen.ratio = self.scene.signal[1]
                    self.signal = "Restart"
                    done = True
                elif self.scene.signal[0] == "Speed":
                    Screen.speed = self.scene.signal[1]
                elif self.scene.signal[0] == "Decors":
                    Screen.decors = self.scene.signal[1]

            timer.wait(Screen.speed) #Sets the speed of execution of the game
            
            self.window.blit(self.background_canvas, (0, 0))
            self.window.blit(self.main_canvas, (0, 0))

            if saving:
                pygame.image.save(self.window, time.strftime("screenshots/screenshot%Y.%m.%d_%H.%M.%S.png"))
            pygame.display.flip()

        if self.signal == "Restart":
            clear_sounds()
            self.scene.clear()
            self.__init__()
        else:
            pygame.quit()



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('This is an easter egg')
    game = Game()