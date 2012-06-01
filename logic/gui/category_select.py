"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
import random
from collections import OrderedDict

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

        GUI_category_go_back(self.game, self)

        category_names = OrderedDict([
            ("Tutorial", (.5, 1.0, .5)),
            ("Effortless", (1.0, .5, .5)),
            ("Light", (1.0, .5, .5)),
            ("Piece Of Cake", (.5, 1.0, 1.0)),
            ("Uncomplicated", (1.0, .5, 1.0)),
            ("Manageable", (1.0, 1.0, .5)),
            ("Troublesome", (1.0, 1.0, .5)),
            ("Formidable", (1.0, 1.0, .5)),
            ("Demanding", (1.0, 1.0, .5)),
            ("Heavy", (1.0, 1.0, .5)),
            ("Challenging!", (1.0, 1.0, .5))
            ])
        self.category_objs = []

        i = 0
        self.last_category = None
        self.first_category = None
        for name,colour in category_names.items():
            self.last_category = GUI_category_select_select_category_button(self.game, self, i, name, colour)
            self.category_objs.append(self.last_category)
            if self.first_category is None:
                self.first_category = self.last_category
            i += 1

        self.scroll_speed = 0.0

        self.text_offset_x = 0.0
        self.text_offset_y = 0.0

        # Draw strategy data
        self.draw_strategy = "category_select"


    def Execute(self):
        self.update()

        if self.game.gui.mouse.x > (self.game.settings['screen_width'] - 512) and self.game.gui.mouse.y < 50:
            if self.first_category.y > self.first_category.image.height:
                self.scroll_speed = 0.0
            else:
                self.scroll_speed -= .2
        if self.game.gui.mouse.x > (self.game.settings['screen_width'] - 512) and self.game.gui.mouse.y > (self.game.settings['screen_height'] - 50):
            if self.last_category.y < self.game.settings['screen_height'] - (self.last_category.image.height * 2):
                self.scroll_speed = 0.0
            else:
                self.scroll_speed += .2

        self.scroll_speed *= .95

        if self.scroll_speed > 7.0:
            self.scroll_speed = 7.0
        if self.scroll_speed < -7.0:
            self.scroll_speed = -7.0
            
        for cat in self.category_objs:
            cat.y -= self.scroll_speed
            cat.update_obj_positions()

        self.text_offset_x -= 5.0
        self.text_offset_y += 5.0



class GUI_category_select_select_category_button(GUI_element_button):
    generic_button = False
    objs = {}
    
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

        self.objs = {}

        text = Text(self.game.core.media.fonts['category_button_name'], 0, 0, TEXT_ALIGN_CENTER, name)
        text.z = self.z - 1
        text.colour = (1.0, 1.0, 1.0)
        text.shadow = 2
        text.shadow_colour = (.2, .2, .2)
        self.objs['cat_name'] = text

        text = Text(self.game.core.media.fonts['category_button_completed_count'], 0, 0, TEXT_ALIGN_TOP_RIGHT, "10")
        text.z = self.z - 1
        text.colour = (1.0, 1.0, 1.0)
        text.shadow = 2
        text.shadow_colour = (.2, .2, .2)
        self.objs['completed_count'] = text

        text = Text(self.game.core.media.fonts['category_button_total_count'], 0, 0, TEXT_ALIGN_TOP_LEFT, "15")
        text.z = self.z - 1
        text.colour = (1.0, 1.0, 1.0)
        text.shadow = 2
        text.shadow_colour = (.2, .2, .2)
        self.objs['total_count'] = text

        text = Text(self.game.core.media.fonts['category_button_total_count'], 0, 0, TEXT_ALIGN_TOP_LEFT, "solved")
        text.z = self.z - 1
        text.colour = (1.0, 1.0, 1.0)
        text.shadow = 1
        text.shadow_colour = (.2, .2, .2)
        self.objs['solved'] = text

        self.objs['tick'] = GUI_category_completed_tick(self.game)

        self.update_obj_positions()


    def Execute(self):
        GUI_element_button.update(self)
        

    def update_obj_positions(self):
        self.objs['cat_name'].x = self.x + (self.image.width/2) - 32
        self.objs['cat_name'].y = self.y + (self.image.height/2)

        self.objs['completed_count'].x = self.x + 460
        self.objs['completed_count'].y = self.y + 6

        self.objs['total_count'].x = self.x + 470
        self.objs['total_count'].y = self.y + 27

        self.objs['solved'].x = self.x + 437
        self.objs['solved'].y = self.y + 40

        self.objs['tick'].x = self.x + 64
        self.objs['tick'].y = self.y + 32


    def mouse_left_up(self):
        return

    
    def On_Exit(self):
        GUI_element_button.On_Exit(self)
        for x in self.objs:
            self.objs[x].Kill()



class GUI_category_completed_tick(Process):
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_category_complete_tick']
        self.z = Z_GUI_OBJECT_LEVEL_3



class GUI_category_go_back(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_go_back']
        self.gui_init()
        self.x = 16
        self.y = 16
        self.width = 128
        self.text = Text(self.game.core.media.fonts['category_button_completed_count'], 64, 16, TEXT_ALIGN_TOP_LEFT, "Back")
        self.text.z = self.z - 1
        self.text.colour = (1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.2, .2, .2)


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 20)


    def On_Exit(self):
        self.text.Kill()
