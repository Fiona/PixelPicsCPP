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
from helpers  import *
from gui.gui_elements import *


class GUI_category_select_container(GUI_element):
    """
    All elements in the menu live inside this thing.
    """
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_CONTAINERS
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.alpha = .1

        GUI_category_select_select_category_button(self.game, self, 0, "Tutorial", (.5, 1.0, .5))
        GUI_category_select_select_category_button(self.game, self, 1, "Effortless", (1.0, .5, .5))
        GUI_category_select_select_category_button(self.game, self, 2, "Light", (1.0, .5, .5))
        GUI_category_select_select_category_button(self.game, self, 3, "Piece Of Cake", (.5, 1.0, 1.0))
        GUI_category_select_select_category_button(self.game, self, 4, "Uncomplicated", (1.0, .5, 1.0))
        GUI_category_select_select_category_button(self.game, self, 5, "Manageable", (1.0, 1.0, .5))
        GUI_category_select_select_category_button(self.game, self, 6, "Troublesome", (1.0, 1.0, .5))
        GUI_category_select_select_category_button(self.game, self, 7, "Formidable", (1.0, 1.0, .5))
        GUI_category_select_select_category_button(self.game, self, 8, "Demanding", (1.0, 1.0, .5))
        GUI_category_select_select_category_button(self.game, self, 9, "Heavy", (1.0, 1.0, .5))
        GUI_category_select_select_category_button(self.game, self, 10, "Challenging!", (1.0, 1.0, .5))

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
              (.7,1.0,1.0,1.0),
              (.7,1.0,1.0,1.0),
              (1.0,1.0,1.0,1.0)                
            )


    def Execute(self):
        self.update()




class GUI_category_select_select_category_button(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None, num = 0, name = "? ? ? ? ?", colour = (1.0, 1.0, 1.0)):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_select_category']
        self.gui_init()
        self.x = (self.game.settings['screen_width']) - self.image.width - 64
        self.y = self.image.height + (self.image.height * num) + (32 * num)
        self.colour = colour

        self.text = Text(self.game.core.media.fonts['category_button_name'], self.x + (self.image.width/2) - 32, self.y + (self.image.height/2), TEXT_ALIGN_CENTER, name)
        self.text.z = self.z - 1
        self.text.colour = (1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.2, .2, .2)


    def mouse_left_up(self):
        return

    
    def On_Exit(self):
        GUI_element_button.On_Exit(self)
        self.text.Kill()
