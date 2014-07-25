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
        self.init_wait = True if self.game.settings['full_screen'] else False
        self.play_initial_sound = False

    def Execute(self):
        # initial full screen wait
        if self.init_wait:
            self.iter += 1
            if self.iter == 60:
                self.init_wait = False
                self.iter = 0
            return

        if self.play_initial_sound == False:
            self.game.core.media.sfx['screams'].play(0)
            self.play_initial_sound = True
            
        # Do the animation
        if self.frame == len(self.frame_switch_times) - 1:
            return
        self.iter += 1
        if self.iter >= self.frame_switch_times[self.frame][1]:
            self.frame += 1
            self.image_sequence = self.frame_switch_times[self.frame][0]
            if self.image_sequence == 3:
                self.game.core.media.sfx['stomp'].play(0)                
            if self.frame == 5:
                self.game.core.media.sfx['car_alarm'].play(0)
            self.iter = 0

    def On_Exit(self):
        self.game.core.media.sfx['car_alarm'].stop()
        self.game.core.media.sfx['screams'].stop()
        self.game.core.media.sfx['stomp'].stop()
        self.game.core.media.sfx['logo_bubble'].stop()
        

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
        self.game.core.media.sfx['logo_bubble'].play(0)        
    
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
