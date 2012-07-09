"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

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
        self.set_location()


    def On_Exit(self):
        if self.speech_bubble:
            self.speech_bubble.Kill()
            

    def set_location(self):
        self.x = 100
        self.y = 100
        self.z = Z_MASCOT
    

    def set_speech(self, to_say):
        if self.speech_bubble:
            self.speech_bubble.Kill()
        self.speech_bubble = Speech_Bubble(self.game, self, to_say)

        

class Mascot_Category_Select(Mascot):

    def Execute(self):
        if self.dir == 0:
            self.iter += 1
            self.y = lerp(self.iter, 60, self.initial_position[1], self.initial_position[1] + 15)
            if self.y >= self.initial_position[1] + 15:
                self.iter = 0
                self.dir = 1
                self.y = self.initial_position[1] + 15
        else:
            self.iter += 1
            self.y = lerp(self.iter, 60, self.initial_position[1] + 15, self.initial_position[1])
            if self.y <= self.initial_position[1]:
                self.iter = 0
                self.dir = 0
                self.y = self.initial_position[1]
                
        
    def set_location(self):
        self.x = (self.game.settings['screen_width'] / 2) - (self.image.width / 2) - 25
        self.y = self.game.settings['screen_height'] / 2
        self.z = Z_MASCOT
        self.initial_position = self.x, self.y
        self.dir = 0
        self.iter = 0
        self.set_speech("Pick a category of puzzles to play!")
    


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
        
