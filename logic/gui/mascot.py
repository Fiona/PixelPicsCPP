"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
import random

# Game engine imports
from core import *

# Game imports
from consts import *
from helpers import lerp


class Mascot(Process):
    
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_chips_happy']
        self.speech_bubble = None
        self.shift_amount = 15
        self.set_location()
        self.initial_position = self.x, self.y
        self.dir = 0
        self.iter = 0


    def On_Exit(self):
        if self.speech_bubble:
            self.speech_bubble.Kill()


    def Execute(self):
        if self.dir == 0:
            self.iter += 1
            self.y = lerp(self.iter, 60, self.initial_position[1], self.initial_position[1] + self.shift_amount)
            if self.y >= self.initial_position[1] + self.shift_amount:
                self.iter = 0
                self.dir = 1
                self.y = self.initial_position[1] + self.shift_amount
        else:
            self.iter += 1
            self.y = lerp(self.iter, 60, self.initial_position[1] + self.shift_amount, self.initial_position[1])
            if self.y <= self.initial_position[1]:
                self.iter = 0
                self.dir = 0
                self.y = self.initial_position[1]
            

    def set_location(self):
        self.x = 100
        self.y = 100
        self.z = Z_MASCOT
    

    def set_speech(self, to_say):
        if self.speech_bubble:
            self.speech_bubble.Kill()
        if len(to_say) > 0:
            self.speech_bubble = self.create_speech_bubble(to_say)
        else:
            self.speech_bubble = None


    def create_speech_bubble(self, to_say):
        return Speech_Bubble(self.game, self, to_say)
    
        

class Mascot_Category_Select(Mascot):

    def Execute(self):
        Mascot.Execute(self)
        if self.game.gui.block_gui_mouse_input:
            return
        coordinates = (self.game.gui.mouse.x, self.game.gui.mouse.y)
        x = self.x - (self.image.width / 2)
        y = self.y - (self.image.height / 2)
        if (coordinates[0] > x and \
            coordinates[0] < x + self.image.width and \
            coordinates[1] > y and \
            coordinates[1] < y + self.image.height and \
            self.game.core.mouse.left_up):
            self.game.core.media.sfx['meow1'].play(0)
               
                        
    def set_location(self):
        self.x = (self.game.settings['screen_width'] / 2) - (self.image.width / 2) - 25
        self.y = self.game.settings['screen_height'] / 2
        self.z = Z_MASCOT
        self.set_speech("Pick a category of puzzles to play!")



class Mascot_Main_Menu(Mascot):
    def Execute(self):
        Mascot.Execute(self)
        if self.alpha < 1.0:
            self.iter2 += 1
            self.alpha = lerp(self.iter2, 60, 0.0, 1.0)


    def set_location(self):
        self.x = (self.game.settings['screen_width'] / 2) - 175
        self.y = (self.game.settings['screen_height'] / 2) + 420
        self.z = Z_GUI_OBJECT_LEVEL_3
        self.scale = .4
        self.shift_amount = 5
        self.alpha = 0.0
        self.iter2 = 0

        if self.game.player.first_run:
            self.game.player.first_run = False
            self.game.save_player(self.game.player)
            self.set_speech(["Hey, is this is your", "first time playing?", "Would you like to learn", "how to play?"])
        else:
            items = [
                ["Did you know that you", "can zoom in and out of", "puzzles with your", "mouse wheel?"],
                ["If you finish a puzzle", "without losing a life then", "you earn a star!", "Try to get a star on", "all puzzles!"],
                ["You can move around a", "puzzle with your middle", "mouse button, cool!"],
                ["Did you check out the", "puzzle designer yet?", "You can even share your", "creations online!"],
                ["Did you know that", "PixelPics auto-saves", " puzzle progress in case", "of a powercut?", "That's handy!"],
                ["Check the Extra Puzzles", "menu for even more", "puzzles made by people", "all over the world!"],
                ["Cats rule!"],
                ["Meow meow meow!", "Mr-eeow mow!", "Mow mow...", ".. MEOW!"],
                ]
            self.set_speech(random.choice(items))
            

    def create_speech_bubble(self, to_say):
        return Main_Menu_Speech_Bubble(self.game, self, to_say)


    def first_time(self):
        self.game.manager.load_pack("0001", user_created = False)
        self.game.manager.current_puzzle_file = "0001.puz"
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_TUTORIAL), speed = 40, stop_music = True)



class Speech_Bubble(Process):
    def __init__(self, game, parent, to_say):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.to_say = to_say
        self.x = self.parent.x
        self.y = self.parent.y - (self.parent.image.height / 2) 
        self.z = Z_MASCOT
        self.image = self.game.core.media.gfx['gui_speech_bubble']

        self.text = Text(self.game.core.media.fonts['speech_bubble'], self.x, self.y - 30, TEXT_ALIGN_CENTER, to_say)
        self.text.z = self.z
        self.text.colour = (.7,.5,0)
        self.text.shadow = 2
        self.text.shadow_colour = (.3,.2,0)


    def On_Exit(self):
        self.text.Kill()
        


class Main_Menu_Speech_Bubble(Process):
    def __init__(self, game, parent, to_say):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.to_say = to_say
        self.image = self.game.core.media.gfx['gui_title_speech_bubble']
        self.x = self.parent.x - (self.image.width / 2) - 20
        self.y = self.parent.y - 300
        self.z = Z_GUI_OBJECT_LEVEL_3

        self.text = []

        y = self.y - 110
        for s in to_say:
            text = Text(self.game.core.media.fonts['title_speech_bubble'], self.x, y, TEXT_ALIGN_TOP, s)
            text.z = self.z - 1
            text.colour = (.3, .3, .3)
            self.text.append(text)
            y += text.text_height


    def On_Exit(self):
        for x in self.text:
            x.Kill()
        
