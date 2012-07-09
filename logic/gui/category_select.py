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
from gui.mascot import *


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
        self.mascot_object = Mascot_Category_Select(self.game)

        categories = [
            ("Tutorial",      "0001", (.5, 1.0, .5)),
            ("Effortless",    "0002", (1.0, .5, .5)),
            ("Light",         "0003", (1.0, .5, .5)),
            ("Piece Of Cake", "0004", (.5, 1.0, 1.0)),
            ("Uncomplicated", "0005", (1.0, .5, 1.0)),
            ("Manageable",    "0006", (1.0, 1.0, .5)),
            ("Troublesome",   "0007", (1.0, 1.0, .5)),
            ("Formidable",    "0008", (1.0, 1.0, .5)),
            ("Demanding",     "0009", (1.0, 1.0, .5)),
            ("Heavy",         "0010", (1.0, 1.0, .5)),
            ("Challenging!",  "0011", (1.0, 1.0, .5))
            ]
        self.category_objs = []

        i = 0
        self.last_category = None
        self.first_category = None
        for name,pack_dir,colour in categories:
            self.last_category = GUI_category_select_select_category_button(self.game, self, i, pack_dir, name, colour)
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


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.mascot_object.Kill()
        


class GUI_category_select_select_category_button(GUI_element_button):
    generic_button = False
    objs = {}
    
    def __init__(self, game, parent = None, num = 0, pack_dir = "", name = "? ? ? ? ?", colour = (1.0, 1.0, 1.0)):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.pack_dir = pack_dir
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_select_category']
        self.gui_init()
        self.x = (self.game.settings['screen_width'] / 2) - 25
        self.y = self.image.height + (self.image.height * num) + (32 * num)
        self.colour = colour

        self.objs = {}

        text = Text(self.game.core.media.fonts['category_button_name'], 0, 0, TEXT_ALIGN_CENTER, name)
        text.z = self.z - 1
        text.colour = (1.0, 1.0, 1.0)
        text.shadow = 2
        text.shadow_colour = (.2, .2, .2)
        self.objs['cat_name'] = text

        if not self.pack_dir in self.game.player.unlocked_categories:
            self.objs['status_icon'] = GUI_category_locked(self.game)
            self.colour = (1.0, 1.0, 1.0)
            self.disabled = True
        else:
            completed = len(self.game.player.cleared_puzzles[self.pack_dir]) if self.pack_dir in self.game.player.cleared_puzzles else 0
            text = Text(self.game.core.media.fonts['category_button_completed_count'], 0, 0, TEXT_ALIGN_TOP_RIGHT, str(completed))
            text.z = self.z - 1
            text.colour = (1.0, 1.0, 1.0)
            text.shadow = 2
            text.shadow_colour = (.2, .2, .2)
            self.objs['completed_count'] = text

            text = Text(self.game.core.media.fonts['category_button_total_count'], 0, 0, TEXT_ALIGN_TOP_LEFT, str(len(self.game.manager.game_packs[self.pack_dir].puzzles)))
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

            if self.pack_dir in self.game.player.cleared_categories:
                self.objs['status_icon'] = GUI_category_completed_tick(self.game)
            
        self.update_obj_positions()


    def Execute(self):
        GUI_element_button.update(self)
        

    def update_obj_positions(self):
        self.objs['cat_name'].x = self.x + (self.image.width/2) - 32
        self.objs['cat_name'].y = self.y + (self.image.height/2)

        if 'completed_count' in self.objs:
            self.objs['completed_count'].x = self.x + 460
            self.objs['completed_count'].y = self.y + 6

        if 'total_count' in self.objs:
            self.objs['total_count'].x = self.x + 470
            self.objs['total_count'].y = self.y + 27

        if 'solved' in self.objs:
            self.objs['solved'].x = self.x + 437
            self.objs['solved'].y = self.y + 40

        if 'status_icon' in self.objs:
            self.objs['status_icon'].x = self.x + 64
            self.objs['status_icon'].y = self.y + 32


    def mouse_left_up(self):
        self.game.manager.load_pack(self.pack_dir, user_created = False)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE_SELECT), speed = 20)

    
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



class GUI_category_locked(Process):
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_category_locked']
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
