import pygame

from random import *
from screen import *
from buttons import *
from sound import *



class Menu:

    def __init__(self, canvas, music_playing):
        self.name = "Menu"
        self.canvas = canvas
        self.buttons = []
        self.labels = []

        self.font1 = "Comic Sans MS"

        self.res = []
        for i in range(1, 5):
            self.res.append(str(320*i)+"x"+str(240*i))

        self.dropdown = False

        for name in ["hit1", "hit2", "hit3", "hit4", "hit5", "hit6", "wave1", "wave2", "wave3", "pop1", "pop2", "pop3", "pop4", "pop5", "click", "doum"]:
            add_sound(name)

        set_volume("wave1", 0.5)
        set_volume("wave2", 0.5)
        set_volume("wave3", 0.5)
        set_volume("click", 0.6)
        set_volume("doum", 0.1)

        self.music_playing = music_playing
        self.anim_label = None
        self.anim_step = 0
        self.anim_state = [False ,False, False, False, False, False, False, False]
        self.buttons_state = [False, False, False, False, False, False, False, False]
        self.step = 1
        self.random_color = (randint(0, 1), randint(0, 1), randint(0, 1))
        self.spawned = False


    def clear(self):
        clear_sounds()

    def add_button(self, button_type, text, pos, arg1=None, arg2=None, arg3=None):
        if button_type == "checkbox":
            self.buttons.append(CheckButton(text, pos))
        elif button_type == "button":
            self.buttons.append(Button(text, pos))
        elif button_type == "slider":
            self.buttons.append(Slider(text, pos, arg1, arg2, arg3))


    def show_dropdown(self):
        self.dropdown = not self.dropdown
        play_sound("click")
        play_sound("doum")
        if self.dropdown:
            for i in range(len(self.res)):
                self.buttons.append(Button(self.res[i], (0, int_val(14)+i*int_val(6)), 32, 6))
        else:
            for i in range(len(self.res)):
                self.buttons.pop(6) #Index from which start the res buttons index

    def title_anim(self, canvas):
        self.anim_step += self.step
        if self.spawned:
            if self.anim_step >= 200:
                self.anim_step = 200
                self.step = -6
            elif self.anim_step <= 0:
                self.anim_step = 0
                self.random_color = (randint(0, 1), randint(0, 1), randint(0, 1))
                self.step = 6
            rc = self.random_color
            self.anim_label = Label("DOUBLE G", (0, int_val(24)), 22, self.font1, pygame.Color(rc[0]*self.anim_step, rc[1]*self.anim_step, rc[2]*self.anim_step))
        else:
            if self.anim_step >= 200:
                self.anim_step = 200
                self.spawned = True
                return

            a = self.anim_step

            def switch_state(actions_list): #actions[0] : cond, actions[1] = state_index, actions[2] = text, actions[3] = pos, actions[4] = size
                for action in actions_list:
                    if action[0]:
                        if not self.anim_state[action[1]] or action[1] == 7:
                            for i in range(0, len(self.anim_state)):
                                self.anim_state[i] = False
                            if action[1] == 7:
                                if self.step == 1 and not self.music_playing:
                                    play_sound("wave"+str(randint(1, 3)), -1)
                                self.step = 2
                                self.anim_label = Label(action[2], action[3], action[4], self.font1, pygame.Color(self.anim_step*self.random_color[0], self.anim_step*self.random_color[1], self.anim_step*self.random_color[2]))
                            else:
                                self.anim_label = Label(action[2], action[3], action[4], self.font1, pygame.Color(100+randint(0, 1)*50, 100+randint(0, 1)*50, 100+randint(0, 1)*50))
                                play_sound("hit"+str(randint(1, 6)))
                            self.anim_state[action[1]] = True
                        break


            def add_buttons(actions_list): #action[0] = cond, action[1] = type
                for action in actions_list:
                    if action[0]:
                        if not self.buttons_state[action[1]]:
                            if action[2] == "label":    #action[3] = text, action[4] = pos, action[5] = size, action[6] = color
                                self.labels.append(Label(action[3], action[4], action[5], self.font1, action[6]))
                            else:                       #action[3] = text, action[4] = pos
                                if action[2] == "slider":
                                    self.add_button(action[2], action[3], action[4], action[5], action[6], action[7])   #action[5] = size, action[6] = scope, action[7] = init_value
                                else:
                                    self.add_button(action[2], action[3], action[4])
                            play_sound("pop"+str(randint(1, 5)))
                            self.buttons_state[action[1]] = True
                        break


            switch_state([[a<=10, 0, "D", (int_val(15), 0), 101], \
                          [a<=20, 1, "O", (int_val(11.75), 0), 101], \
                          [a<=30, 2, "U", (int_val(15), 0), 101], \
                          [a<=40, 3, "B", (int_val(15), 0), 101], \
                          [a<=50, 4, "L", (int_val(16.25), 0), 101], \
                          [a<=60, 5, "E", (int_val(16.25), 0), 101], \
                          [a<=70, 6, "G", (int_val(13.75), 0), 101], \
                          [a>70, 7, "DOUBLE G", (0, int_val(24)), 22]])


            if a>120:
                add_buttons([[a<=130, 0, "button", "Play", (int_val(48), 0)], \
                             [a<=140, 1, "button", "Quit", (int_val(48), int_val(46))], \
                             [a<=150, 2, "checkbox", ["Fullscreen", "Windowed"], (0, int_val(46))], \
                             [a<=160, 3, "button", "Resolution", (0, 0)], \
                             [a<=170, 4, "slider", "Decors", (int_val(38), int_val(17.5)), [int_val(28), int_val(4)], [0, 17], Screen.decors], \
                             [a<=180, 5, "slider", "Speed Slider", (int_val(38), int_val(39.25)), [int_val(28), int_val(4)], [1, 31], 31 - Screen.speed], \
                             [a<=190, 6, "label", "Decors", (int_val(17.5), int_val(16.5)), 8, pygame.Color(0, 30, 75)], \
                             [a<=200, 7, "label", "Speed", (int_val(19), int_val(38.5)), 8, pygame.Color(0, 30, 75)]])



    def update(self, canvas):
        self.signal = ""

        self.title_anim(canvas)
        
        escape_key = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.signal = "Force Quit"
            elif event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_ESCAPE:
                    escape_key = True
                    self.signal = "Quit"
                elif k == pygame.K_F12:
                    self.signal = "Save Screen"

            for button in self.buttons:
                pressing = False
                moving = False
                if button.text == "Windowed" and not Screen.fullscreen:
                    button.flip_side()
                elif button.text == "Fullscreen" and Screen.fullscreen:
                    button.flip_side()

                if event.type == pygame.MOUSEMOTION:
                    if button.shape.collidepoint(event.pos):
                        button.hovered = True
                        moving = True
                    if button.text == "Speed Slider" and button.hovered and event.buttons[0] == 1: #Switch on "move"
                        value = button.value
                        self.signal = ["Speed", 31 - button.set_value(event.pos)]
                        if value != button.value:
                            play_sound("doum")
                    elif button.text == "Decors" and button.hovered and event.buttons[0] == 1: #Switch on "move"
                        value = button.value
                        self.signal = ["Decors", button.set_value(event.pos)]
                        if value != button.value:
                            play_sound("doum")
                
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.hovered and event.button == 1:
                        pressing = True
                        if button.text == "Speed Slider":   #Switch on "click"
                            self.signal = ["Speed", 31 - button.set_value(event.pos)]
                            play_sound("doum")
                        elif button.text == "Decors":       #Switch on "click"
                            self.signal = ["Decors", button.set_value(event.pos)]
                            play_sound("doum")
                        elif button.text == "Play":
                            self.signal = "Play"
                        elif button.text == "Fullscreen" or button.text == "Windowed":
                            self.signal = "Display Mode"
                            button.flip_side()
                        elif button.text == "Quit":
                            self.signal = "Quit"
                        elif button.text == "Resolution" or button.text in self.res:
                            self.show_dropdown()
                        if button.text in self.res:
                            self.signal = ["Resolution", (self.res.index(button.text) + 1)*4]
                    
                if not moving and not pressing:
                    button.hovered = False

        canvas.blit(self.anim_label.canvas, self.anim_label.pos)
        if self.signal != "":
            if type(self.signal) == list:
                pass
            else:
                if not escape_key:
                    play_sound("click")
                    play_sound("doum")
            if self.signal in ["Quit", "Play"]:
                pass


        for label in self.labels:
            canvas.blit(label.canvas, label.pos)

        for button in self.buttons:
            button.update()
            canvas.blit(button.canvas, button.pos)