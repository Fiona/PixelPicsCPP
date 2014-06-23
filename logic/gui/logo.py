"""
PixelPics - Nonogram game
Copyright (c) 2014 Stompy Blondie Games http://stompyblondie.com
"""

# Engine imports
from core import *

# game imports
from consts import *
from helpers import lerp


                        
class Stompyblondie_Logo(Process):
    frame_switch_times = [
        (1, 30),
        (2, 10),
        (3, 5),
        (1, 15),
        (2, 10),
        (3, 5),
        (1, 15),
        (2, 10),
        (3, 5),
        (1, 10)
        ]
    
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_stompyblondie_logo']
        self.x = (self.game.settings['screen_width']/2)
        self.y = (self.game.settings['screen_height']/2)
        self.z = Z_STOMPYBLONDIE_LOGO
        self.iter = 0
        self.frame = 0

    def Execute(self):
        if self.frame == len(self.frame_switch_times) - 1:
            return
        self.iter += 1
        if self.iter >= self.frame_switch_times[self.frame][1]:
            self.frame += 1
            self.image_sequence = self.frame_switch_times[self.frame][0]
            self.iter = 0
        

class Stompyblondie_Logo_Text(Process):
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_stompyblondie_logo_text']
        self.x = (self.game.settings['screen_width']/2) + 450
        self.y = (self.game.settings['screen_height']/2) + 50
        self.z = Z_STOMPYBLONDIE_LOGO
        self.scale = 0.0
        self.scale_state = 0
        self.iter = 0
        self.scale_pos = (0.0, self.image.height)
        
    
    def Execute(self):
        self.iter += 1
        if self.scale_state == 0:
            self.scale = lerp(self.iter, 10, 0.0, 1.2)
            if self.iter == 10:
                self.scale_state = 1
                self.iter = 0
        elif self.scale_state == 1:
            self.scale = lerp(self.iter, 5, 1.2, 1.0)
            if self.iter == 5:
                self.scale_state = 2
                self.iter = 0
