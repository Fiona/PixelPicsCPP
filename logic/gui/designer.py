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

        self.scroll = GUI_designer_packs_packs_list_scroll_window(self.game, self)

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



class GUI_designer_packs_packs_list_scroll_window(GUI_element_scroll_window):
    pack_items = []
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_4
        self.x = 50
        self.y = 200
        self.width = self.game.settings['screen_width'] - 100
        self.height = self.game.settings['screen_height'] - 250
        self.gui_init()
        self.reread_pack_items()


    def reread_pack_items(self):
        for x in self.pack_items:
            x.Kill()
        self.contents_scroll_location = 0.0
        self.pack_items = []
        last_item = None
        count = 0

        for i,pack in enumerate(self.game.manager.packs):
            if not pack.author_id == self.game.author_id:
                continue
            last_item = GUI_designer_packs_pack_item(self.game, self, pack, i, count)
            #GUI_designer_packs_button_edit_pack(self.game, self, pack, i, count)
            #GUI_designer_packs_button_delete_pack(self.game, self, pack, i, count)
            self.pack_items.append(last_item)
            self.pack_items.append(
                GUI_designer_packs_button_edit_pack(self.game, self, pack, i, count)
            )
            self.pack_items.append(
                GUI_designer_packs_button_delete_pack(self.game, self, pack, i, count)
            )
            count += 1
            
        if last_item is None:
            self.contents_height = 0
        else:
            self.contents_height = last_item.y + last_item.height + 10



class GUI_designer_packs_pack_item(GUI_element):
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_5 - 1
        self.x = 10
        self.y = (50 * display_count) + 10 + (10 * display_count)
        self.width = self.parent.width - 64
        self.height = 50
        self.alpha = .1
        self.gui_init()

        self.text_pack_name = Text(self.game.core.media.fonts['designer_pack_name'], self.x + self.scroll_element.x + 5, 0.0, TEXT_ALIGN_TOP_LEFT, str(self.pack.name))
        self.text_pack_name.z = self.z - 2
        self.text_pack_name.colour = (1.0, 1.0, 1.0)
        self.text_pack_name.shadow = 2
        self.text_pack_name.shadow_colour = (.1, .1, .1)

        self.text_pack_author = Text(self.game.core.media.fonts['designer_pack_author'], self.x + self.scroll_element.x + 15, 0.0, TEXT_ALIGN_TOP_LEFT, str("by " + self.pack.author_name))
        self.text_pack_author.z = self.z - 2
        self.text_pack_author.colour = (1.0, 1.0, 1.0)

        self.draw_strategy = "gui_designer_packs_pack_item"


    def Execute(self):
        self.update()
        self.text_pack_name.y = self.y + self.scroll_element.y + 2 - self.scroll_element.contents_scroll_location
        self.text_pack_name.clip = self.clip
        self.text_pack_author.y = self.y + self.scroll_element.y + 25 - self.scroll_element.contents_scroll_location
        self.text_pack_author.clip = self.clip


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text_pack_name.Kill()
        self.text_pack_author.Kill()


    def mouse_not_over(self):
        self.alpha = .47

        
    def mouse_over(self):
        self.alpha = .78

        
    def mouse_left_up(self):
        self.game.manager.load_pack(self.game.manager.pack_directory_list[self.pack_num])
        self.game.gui.fade_toggle(lambda: self.game.gui.switch_gui_state_to(GUI_STATE_DESIGNER_PUZZLES), speed = 20)
        


class GUI_designer_packs_button_edit_pack(GUI_element_button):
    generic_button = False
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 121
        self.y = (50 * display_count) + 10 + (10 * display_count) + 3
        self.image = self.game.core.media.gfx['gui_button_designer_edit']
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_designer_packs_edit_pack_dialog(self.game, self.parent.parent, self.pack, self.pack_num)

        

class GUI_designer_packs_button_delete_pack(GUI_element_button):
    generic_button = False
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 121
        self.y = (50 * display_count) + 10 + (10 * display_count) + 27
        self.image = self.game.core.media.gfx['gui_button_designer_delete']
        self.gui_init()


    def confirm(self):
        try:
            self.game.manager.delete_pack(self.pack_num)
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.parent.reread_pack_items()


    def mouse_left_up(self):
        self.conf_box = GUI_element_confirmation_box(
            self.game,
            self,
            "Really Delete?",
            ["Are you sure you want to delete this pack", ("%s?" % self.pack.name), "All puzzles within it will be permanently deleted."],
            confirm_callback = self.confirm
            )



class GUI_designer_packs_edit_pack_dialog(GUI_element_window):
    title = "Edit Pack"
    height = 240
    width = 450
    objs = {}

    def __init__(self, game, parent = None, pack = None, pack_num = 8):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.pack = pack
        self.pack_num = pack_num        
        self.gui_init()

    
    def gui_init(self):
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.x = (self.game.settings['screen_width'] / 2) - (self.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) - (self.height / 2)
        GUI_element_window.gui_init(self)

        self.objs = {}
        y = 0
        for text in ["Using this dialog you can edit the name", "and author name for this pack."]:
            txt = Text(self.game.core.media.fonts['basic'], self.x + 30, self.y + 30 + y, TEXT_ALIGN_TOP_LEFT, text)
            txt.z = self.z - 2
            txt.colour = (0.0, 0.0, 0.0)
            self.objs['text_' + str(y)] = txt
            y += 15

        self.pack_name_text = GUI_designer_packs_add_pack_pack_name_text_input(self.game, self)
        self.pack_name_text.set_current_text_to(self.pack.name)
        self.author_text = GUI_designer_packs_add_pack_author_text_input(self.game, self)
        self.author_text.set_current_text_to(self.pack.author_name)
        GUI_designer_packs_edit_pack_pack_confirm_button(self.game, self)
        GUI_designer_packs_edit_pack_pack_cancel_button(self.game, self)

        txt = Text(self.game.core.media.fonts['basic'], self.x + 30, self.y + 147, TEXT_ALIGN_TOP_LEFT, "Game mode: ")
        txt.z = self.z - 2
        txt.colour = (0.0, 0.0, 0.0)
        self.objs['text_dropdown'] = txt        
        self.puzzle_type_dropdown = GUI_designer_packs_edit_pack_puzzle_type_dropdown(self.game, self)
        self.puzzle_type_dropdown.change_selected_item(1 if self.pack.freemode else 0)
        
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


    def edit_pack(self):
        dont_kill = False
        
        try:
            self.game.manager.edit_pack(self.pack_num, self.pack_name_text.current_text, self.author_text.current_text, True if self.puzzle_type_dropdown.selected_item == 1 else False)
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



class GUI_designer_packs_edit_pack_pack_confirm_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Edt Pack"

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
        self.parent.edit_pack()



class GUI_designer_packs_edit_pack_pack_cancel_button(GUI_element_button):
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
