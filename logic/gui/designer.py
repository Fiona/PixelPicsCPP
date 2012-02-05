"""
PixelPics - Nonograme game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
import os, pickle

# Game engine imports
from core import *

# Game imports
from consts import *
from gui.gui_elements import *
from gui.puzzle import GUI_puzzle


###############################################################
############ PUZZLE PACK LISTINGS ############################
###############################################################



class GUI_designer_packs_container(GUI_element):
    """
    All elements in the packs selection/editing/deleting live here.
    """
    objs = []
    scroll = None
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_CONTAINERS
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.alpha = 0.1

        GUI_designer_title(self.game, self)
        GUI_designer_packs_back(self.game, self)
        GUI_designer_packs_create_pack(self.game, self)
        
        self.objs = []

        subtitle = Text(self.game.core.media.fonts['basic'], self.game.settings['screen_width']/2, 100, TEXT_ALIGN_CENTER, "Puzzles are placed in collections called \"Packs\".")
        subtitle.colour = (.2, .2, .2)
        subtitle.z = Z_GUI_OBJECT_LEVEL_5
        self.objs.append(subtitle)

        subtitle2 = Text(self.game.core.media.fonts['basic'], self.game.settings['screen_width']/2, 120, TEXT_ALIGN_CENTER, "Select a pack to add your puzzle to or Create one if there are none.")
        subtitle2.colour = (.2, .2, .2)
        subtitle2.z = subtitle.z
        self.objs.append(subtitle2)

        #self.scroll = GUI_designer_packs_packs_list_scroll_window(self.game, self)

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
              (.7,1.0,.7,1.0),
              (.7,1.0,.7,1.0),
              (1.0,1.0,1.0,1.0)                
            )


    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.objs:
            x.Kill()



class GUI_designer_title(GUI_element):
    def __init__(self, game, parent, subtitle = None, no_background = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.no_background = no_background
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_5
        
        self.text = Text(self.game.core.media.fonts['menu_titles'], 10, 10, TEXT_ALIGN_TOP_LEFT, "Puzzle Designer")
        self.text.colour = (.2, .9, .2)
        self.text.shadow_colour = (.2, .2, .2)
        self.text.shadow = 2
        self.text.z = self.z - 1

        if not subtitle is None:
            self.subtitle = Text(self.game.core.media.fonts['menu_subtitles'], 30, 50, TEXT_ALIGN_TOP_LEFT, subtitle)
            self.subtitle.colour = (.2, .5, .2)
            self.subtitle.shadow_colour = (.2, .2, .2)
            self.subtitle.shadow = 2
            self.subtitle.z = self.z - 2
        else:
            self.subtitle = None

        # Draw strategy data
        if not self.no_background:
            self.draw_strategy = "primitive_square"
            self.draw_strategy_call_parent = False
            self.primitive_square_width = 200
            self.primitive_square_height = self.text.text_height + 20 + (0 if self.subtitle is None else 20)
            self.primitive_square_x = 0.0
            self.primitive_square_y = 0.0
            self.primitive_square_four_colours = True
            self.primitive_square_colour = (
                (.5, .8, .7, 1.0),
                (1.0, 1.0, 1.0, 0.0),
                (1.0, 1.0, 1.0, 0.0),
                (.5, .8, .7, 1.0)
                )


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text.Kill()
        if not self.subtitle is None:
            self.subtitle.Kill()



class GUI_designer_packs_back(GUI_element_button):
    generic_button = True
    generic_button_text = "< Back"
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = 50
        self.y = 160
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def mouse_left_up(self):
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 20)



class GUI_designer_packs_create_pack(GUI_element_button):
    generic_button = True
    generic_button_text = "Create Pack"
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.y = 160
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()
        self.x = self.game.settings['screen_width'] - self.width - 50
        self.generic_button_text_object.x = self.x + 9


    def mouse_left_up(self):
        GUI_designer_packs_add_pack_dialog(self.game, self.parent)
