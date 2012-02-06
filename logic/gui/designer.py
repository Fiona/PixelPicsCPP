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



class GUI_designer_packs_add_pack_dialog(GUI_element_window):
    title = "Create Pack"
    height = 240
    width = 450
    objs = {}

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()

    
    def gui_init(self):
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.x = (self.game.settings['screen_width'] / 2) - (self.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) - (self.height / 2)
        GUI_element_window.gui_init(self)

        self.objs = {}
        y = 0
        for text in ["Enter a simple descriptive name for your new pack", "and your name as the author."]:
            txt = Text(self.game.core.media.fonts['basic'], self.x + 30, self.y + 30 + y, TEXT_ALIGN_TOP_LEFT, text)
            txt.z = self.z - 2
            txt.colour = (0.0, 0.0, 0.0)
            self.objs['text_' + str(y)] = txt
            y += 15

        self.pack_name_text = GUI_designer_packs_add_pack_pack_name_text_input(self.game, self)
        self.author_text = GUI_designer_packs_add_pack_author_text_input(self.game, self)
        GUI_designer_packs_add_pack_pack_confirm_button(self.game, self)
        GUI_designer_packs_add_pack_pack_cancel_button(self.game, self)

        txt = Text(self.game.core.media.fonts['basic'], self.x + 30, self.y + 147, TEXT_ALIGN_TOP_LEFT, "Game mode: ")
        txt.z = self.z - 2
        txt.colour = (0.0, 0.0, 0.0)
        self.objs['text_dropdown'] = txt        
        self.puzzle_type_dropdown = GUI_designer_packs_edit_pack_puzzle_type_dropdown(self.game, self)
        
        self.game.gui.block_gui_keyboard_input = True
        self.x = 0
        self.y = 0
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']

        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_width = self.x + self.width
        self.primitive_square_height = self.y + self.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_colour = (0.0, 0.0, 0.0, .4)


    def add_new_pack(self):
        dont_kill = False
        
        try:
            self.game.manager.add_new_pack(self.pack_name_text.current_text, self.author_text.current_text, True if self.puzzle_type_dropdown.selected_item == 1 else False)
        except IOError as e:
            GUI_element_dialog_box(self.game, self.parent, "Input error", [str(e)])
            dont_kill = True
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.parent.scroll.reread_pack_items()
            if not dont_kill:
                self.Kill()
        

    def On_Exit(self):
        GUI_element_window.On_Exit(self)
        self.game.gui.block_gui_keyboard_input = False
        for x in self.objs:
            self.objs[x].Kill()
            


class GUI_designer_packs_add_pack_pack_name_text_input(GUI_element_text_input):
    label = "Pack name:"
    width = 380
    max_length = 25

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.x = self.parent.x + 30
        self.y = self.parent.y + 85
        self.gui_init()



class GUI_designer_packs_add_pack_author_text_input(GUI_element_text_input):
    label = "Author:"
    width = 380
    max_length = 25

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.x = self.parent.x + 30
        self.y = self.parent.y + 115
        self.gui_init()



class GUI_designer_packs_edit_pack_puzzle_type_dropdown(GUI_element_dropdown):
    display_width = 290
    display_height = 25

    dropdown_options = [
        {'text' : "Normal Mode (lives)", 'data' : 'normal'},
        {'text' : "Freemode (no lives)", 'data' : 'freemode'}
        ]

    selected_item = 0
        
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.display_x = self.parent.x + 120
        self.display_y = self.parent.y + 145
        self.display_z = self.parent.z - 2
        self.gui_init()



class GUI_designer_packs_add_pack_pack_confirm_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Add Pack"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) - (self.width) - 10
        self.y = self.parent.y + 180
        self.generic_button_text_object.x = self.x + 9
        self.generic_button_text_object.y = self.y + 4


    def mouse_left_up(self):
        self.parent.add_new_pack()



class GUI_designer_packs_add_pack_pack_cancel_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Cancel"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) + 10
        self.y = self.parent.y + 180
        self.generic_button_text_object.x = self.x + 9
        self.generic_button_text_object.y = self.y + 4


    def mouse_left_up(self):
        self.parent.Kill()


