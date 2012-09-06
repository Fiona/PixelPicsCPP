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
from helpers import Net_Process_POST
from gui.gui_elements import *



class GUI_sharing_container(GUI_element):
    """
    All elements in the sharing screen live inside this thing.
    """
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_CONTAINERS
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']

        self.net_process = None
        self.net_callback = None
        self.loading_indicator = None

        GUI_sharing_test_button(self.game, self)
        
        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_four_colours = True
        self.primitive_square_colour = (
              (1.0,1.0,1.0,1.0),
              (.7,.65,.8,1.0),
              (.7,.65,.8,1.0),
              (1.0,1.0,1.0,1.0)                
            )


    def Execute(self):
        if not self.net_process is None:
            if self.net_process.is_complete():
                if self.net_process.got_error:
                    GUI_element_dialog_box(
                        self.game,
                        self,
                        "Network error",
                        ["A network error occured!", "Please check your internet connection is functioning properly."],
                        callback = self.return_to_menu
                        )
                    return
                if not self.net_callback is None:
                    self.net_callback(self.net_process.response)
                self.net_process = None
                self.loading_indicator.Kill()
                self.loading_indicator = None                


    def return_to_menu(self):
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 20)
        

    def make_request_to_server(self, url, data = {}, callback = None):
        if not self.net_process is None:
            return

        self.net_process = Net_Process_POST(SHARING_ADDRESS + url, data)
        self.net_callback = callback
        self.loading_indicator = GUI_sharing_loading_indicator(self.game, self)



class GUI_sharing_loading_indicator(GUI_element):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()

        self.z = Z_GUI_OBJECT_LEVEL_11
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.text = Text(self.game.core.media.fonts['puzzle_hint_numbers'], self.width / 2, self.height / 2, TEXT_ALIGN_CENTER, "Loading . . . ")
        self.text.z = self.z - 1
        self.text.colour = (1.0, 1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.3, .3, .3, 1.0)
        
        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.primitive_square_width = self.width
        self.primitive_square_height = 100
        self.primitive_square_x = 0.0
        self.primitive_square_y = (self.height / 2) - 50
        self.primitive_square_colour = (0.0,0.0,0.0,.3)


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text.Kill()
        


class GUI_sharing_test_button(GUI_element_button):
    generic_button = True
    generic_button_text = "test me"
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = 200
        self.y = 200
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def mouse_left_up(self):
        self.parent.make_request_to_server("test/", {'hello' : 'pikachu'}, self.get_response)


    def get_response(self, response):
        print response
