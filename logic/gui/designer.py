"""
PixelPics - Nonograme game
Copyright (c) 2014 Stompy Blondie Games http://stompyblondie.com
"""

# python imports
import os, pickle

# Game engine imports
from core import *

# Game imports
from consts import *
from gui.gui_elements import *
from gui.puzzle_view import GUI_puzzle



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

        GUI_designer_title(self.game, self, title = "Select Pack")
        self.back_button = GUI_designer_packs_back(self.game, self)
        GUI_designer_packs_create_pack(self.game, self)
        
        self.objs = []

        subtitle = Text(self.game.core.media.fonts['basic'], self.game.settings['screen_width']/2, 90, TEXT_ALIGN_CENTER, "Puzzles are placed in collections called \"Packs\".")
        subtitle.colour = (.4, .4, .4)
        subtitle.z = Z_GUI_OBJECT_LEVEL_5
        self.objs.append(subtitle)

        subtitle2 = Text(self.game.core.media.fonts['basic'], self.game.settings['screen_width']/2, 110, TEXT_ALIGN_CENTER, "Select a pack to add your puzzle to or Create one if there are none.")
        subtitle2.colour = (.4, .4, .4)
        subtitle2.z = subtitle.z
        self.objs.append(subtitle2)

        self.scroll = GUI_designer_packs_packs_list_scroll_window(self.game, self)

        # Draw strategy data
        self.draw_strategy = "designer_background"
        self.text_offset_x = 0.0
        self.text_offset_y = 0.0


    def Execute(self):
        self.text_offset_x += 5.0
        self.text_offset_y -= 5.0

        if not self.game.gui.block_gui_keyboard_input:
            if self.game.core.Keyboard_key_released(key.ESCAPE):
                self.back_button.mouse_left_up()
                

    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.objs:
            x.Kill()



class GUI_designer_title(GUI_element):
    def __init__(self, game, parent, title = "Select Pack", subtitle = None, no_background = False, small = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.no_background = no_background
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_5

        self.text = Text(self.game.core.media.fonts['menu_titles_small' if small else 'menu_titles'], 20, 10, TEXT_ALIGN_TOP_LEFT, title)
        if small:
            self.text.y -= 8
        self.text.z = self.z - 2
        self.text.colour = (0.95, 0.58, 0.09)
        self.text.shadow = 2
        self.text.shadow_colour = (0.7, 0.7, 0.7)

        if not subtitle is None:
            self.subtitle = Text(self.game.core.media.fonts['menu_subtitles_small' if small else 'menu_subtitles'], 30, 50, TEXT_ALIGN_TOP_LEFT, subtitle)
            if small:
                self.subtitle.x += 16
                self.subtitle.y -= 16
            self.subtitle.colour = (.8, .8, .8)
            self.subtitle.shadow_colour = (.5, .5, .5)
            self.subtitle.shadow = 2
            self.subtitle.z = self.z - 4
        else:
            self.subtitle = None


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text.Kill()
        if not self.subtitle is None:
            self.subtitle.Kill()



class GUI_designer_packs_back(GUI_element_button):
    generic_button = False
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_go_back']
        self.x = -8
        self.y = self.game.settings['screen_height'] - self.image.height - 16
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 20)



class GUI_designer_packs_create_pack(GUI_element_button):
    generic_button = False
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_create']
        self.x = self.game.settings['screen_width'] - self.image.width + 8
        self.y = 125
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        GUI_designer_packs_add_pack_dialog(self.game, self.parent)



class GUI_designer_packs_add_pack_dialog(GUI_element_window):
    title = "Create Pack"
    height = 210
    width = 480
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
        for text in ["Enter a simple descriptive name for your", "new pack and your name as the author."]:
            txt = Text(self.game.core.media.fonts['window_text'], self.x + 28, self.y + 45 + y, TEXT_ALIGN_TOP_LEFT, text)
            txt.z = self.z - 2
            txt.colour = (0.3, 0.3, 0.3)
            self.objs['text_' + str(y)] = txt
            y += txt.text_height + 2 

        self.pack_name_text = GUI_designer_packs_add_pack_pack_name_text_input(self.game, self)
        self.author_text = GUI_designer_packs_add_pack_author_text_input(self.game, self)
        GUI_designer_packs_add_pack_pack_confirm_button(self.game, self)
        GUI_designer_packs_add_pack_pack_cancel_button(self.game, self)
        """
        txt = Text(self.game.core.media.fonts['window_text'], self.x + 30, self.y + 165, TEXT_ALIGN_TOP_LEFT, "Game mode: ")
        txt.z = self.z - 2
        txt.colour = (0.3, 0.3, 0.3)
        self.objs['text_dropdown'] = txt        
        self.puzzle_type_dropdown = GUI_designer_packs_edit_pack_puzzle_type_dropdown(self.game, self)
        """
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
            #self.game.manager.add_new_pack(self.pack_name_text.current_text, self.author_text.current_text, True if self.puzzle_type_dropdown.selected_item == 1 else False)
            self.game.manager.add_new_pack(self.pack_name_text.current_text, self.author_text.current_text, freemode = False)
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
        self.y = self.parent.y + 100
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
        self.y = self.parent.y + 130
        self.gui_init()



class GUI_designer_packs_edit_pack_puzzle_type_dropdown(GUI_element_dropdown):
    display_width = 270

    dropdown_options = [
        {'text' : "Lives on (Easy)", 'data' : 'normal'},
        {'text' : "Lives off (Hard)", 'data' : 'freemode'}
        ]

    selected_item = 0
        
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.display_x = self.parent.x + 140
        self.display_y = self.parent.y + 160
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
        self.y = self.parent.y + self.parent.height - 45
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
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
        self.y = self.parent.y + self.parent.height - 45
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.Kill()



class GUI_designer_packs_packs_list_scroll_window(GUI_element_scroll_window):
    pack_items = []
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_4
        self.x = 114
        self.y = 150
        self.width = self.game.settings['screen_width'] - 226
        self.height = self.game.settings['screen_height'] - 190
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
            self.pack_items.append(last_item)
            self.pack_items.append(
                GUI_designer_packs_button_open_pack(self.game, self, pack, i, count)
            )
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
            self.contents_height = last_item.y + last_item.height + 20



class GUI_designer_packs_pack_item(GUI_element):
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_5 - 1
        self.x = 15
        self.y = (65 * display_count) + 15 + (10 * display_count)
        self.width = self.parent.width - 80
        self.height = 65
        self.alpha = .1
        self.gui_init()

        self.text_pack_name = Text(self.game.core.media.fonts['designer_pack_name'], self.x + self.scroll_element.x + 4, 0.0, TEXT_ALIGN_TOP_LEFT, str(self.pack.name))
        self.text_pack_name.z = self.z - 2
        self.text_pack_name.colour = (0.95, 0.58, 0.09, 1.0)
        self.text_pack_name.shadow = 2
        self.text_pack_name.shadow_colour = (.8, .8, .8)

        self.text_pack_author = Text(self.game.core.media.fonts['designer_pack_author'], self.x + self.scroll_element.x + 16, 0.0, TEXT_ALIGN_TOP_LEFT, str("by " + self.pack.author_name))
        self.text_pack_author.z = self.z - 2
        self.text_pack_author.colour = (.55, .55, .55)
        self.text_pack_author.shadow = 2
        self.text_pack_author.shadow_colour = (.8, .8, .8)

        self.draw_strategy = "gui_designer_packs_pack_item"


    def Execute(self):
        self.update()
        self.text_pack_name.y = self.y + self.scroll_element.y + 0 - self.scroll_element.contents_scroll_location
        self.text_pack_name.clip = self.clip
        self.text_pack_author.y = self.y + self.scroll_element.y + 35 - self.scroll_element.contents_scroll_location
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
        

class GUI_designer_packs_button_open_pack(GUI_element_button):
    generic_button = False
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 245
        self.y = (65 * display_count) + 15 + (10 * display_count) + 3
        self.image = self.game.core.media.gfx['gui_button_designer_open']
        self.gui_init()

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
        self.x = self.parent.width - 185
        self.y = (65 * display_count) + 15 + (10 * display_count) + 3
        self.image = self.game.core.media.gfx['gui_button_designer_edit']
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
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
        self.x = self.parent.width - 125
        self.y = (65 * display_count) + 15 + (10 * display_count) + 3
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
        GUI_element_button.mouse_left_up(self)
        self.conf_box = GUI_element_confirmation_box(
            self.game,
            self,
            "Really Delete?",
            ["Are you sure you want to delete this pack", ("%s?" % self.pack.name), "All puzzles within it will be permanently deleted."],
            confirm_callback = self.confirm
            )



class GUI_designer_packs_edit_pack_dialog(GUI_element_window):
    title = "Edit Pack"
    height = 245
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
            txt = Text(self.game.core.media.fonts['window_text'], self.x + 28, self.y + 45 + y, TEXT_ALIGN_TOP_LEFT, text)
            txt.z = self.z - 2
            txt.colour = (0.3, 0.3, 0.3)
            self.objs['text_' + str(y)] = txt
            y += txt.text_height + 2 

        self.pack_name_text = GUI_designer_packs_add_pack_pack_name_text_input(self.game, self)
        self.pack_name_text.set_current_text_to(self.pack.name)
        self.author_text = GUI_designer_packs_add_pack_author_text_input(self.game, self)
        self.author_text.set_current_text_to(self.pack.author_name)
        GUI_designer_packs_edit_pack_pack_confirm_button(self.game, self)
        GUI_designer_packs_edit_pack_pack_cancel_button(self.game, self)

        txt = Text(self.game.core.media.fonts['window_text'], self.x + 30, self.y + 165, TEXT_ALIGN_TOP_LEFT, "Game mode: ")
        txt.z = self.z - 2
        txt.colour = (0.3, 0.3, 0.3)
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
        self.y = self.parent.y + 200
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


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
        self.y = self.parent.y + 200
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


    def mouse_left_up(self):
        self.parent.Kill()




###############################################################
################## PUZZLE LISTINGS ############################
###############################################################



class GUI_designer_puzzles_container(GUI_element):
    """
    All elements in the puzzle list selection/editing/deleting live here.
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

        GUI_designer_title(self.game, self, title  = str(self.game.manager.current_pack.name), subtitle  = "by " + str(self.game.manager.current_pack.author_name))
        self.back_button = GUI_designer_puzzles_back(self.game, self)
        GUI_designer_puzzles_create_puzzle(self.game, self)

        self.objs = []

        subtitle = Text(self.game.core.media.fonts['basic'], self.game.settings['screen_width']/2, 100, TEXT_ALIGN_CENTER, "This is a list of puzzles in the current pack. Select a puzzle to design it or Create one if there are none.")
        subtitle.colour = (.4, .4, .4)
        subtitle.z = Z_GUI_OBJECT_LEVEL_5
        self.objs.append(subtitle)

        if len(self.game.manager.current_pack.order) > 1:
            subtitle2 = Text(self.game.core.media.fonts['basic'], self.game.settings['screen_width']/2, 120, TEXT_ALIGN_CENTER, "Use the arrows to the left to reorder puzzles.")
            subtitle2.colour = (.4, .4, .4)
            subtitle2.z = subtitle.z
            self.objs.append(subtitle2)

        self.scroll = GUI_designer_puzzles_puzzles_list_scroll_window(self.game, self)
        
        # Draw strategy data
        self.draw_strategy = "designer_background"
        self.text_offset_x = 0.0
        self.text_offset_y = 0.0


    def Execute(self):
        self.text_offset_x += 5.0
        self.text_offset_y -= 5.0

        if not self.game.gui.block_gui_keyboard_input:
            if self.game.core.Keyboard_key_released(key.ESCAPE):
                self.back_button.mouse_left_up()


    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.objs:
            x.Kill()



class GUI_designer_puzzles_back(GUI_element_button):
    generic_button = True
    generic_button_text = "< Back"
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_go_back']
        self.x = -8
        self.y = self.game.settings['screen_height'] - self.image.height - 16
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def mouse_left_up(self):
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_DESIGNER), speed = 20)



class GUI_designer_puzzles_create_puzzle(GUI_element_button):
    generic_button = False
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_create']
        self.x = self.game.settings['screen_width'] - self.image.width + 8
        self.y = 125
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def mouse_left_up(self):
        if len(self.game.manager.current_pack.puzzles) >= MAX_PUZZLES_PER_PACK: 
            GUI_element_dialog_box(self.game, self.parent, "Puzzle limit hit", ["You can have no more than " + str(MAX_PUZZLES_PER_PACK) + " puzzles", "in a single pack."])
            return        
        GUI_designer_puzzles_add_puzzle_dialog(self.game, self.parent)



class GUI_designer_puzzles_add_puzzle_dialog(GUI_element_window):
    title = "Create Puzzle"
    height = 200
    width = 450
    objs = {}

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()

        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_width = self.x + self.width
        self.primitive_square_height = self.y + self.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_colour = (0.0, 0.0, 0.0, .4)

    
    def gui_init(self):
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.x = (self.game.settings['screen_width'] / 2) - (self.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) - (self.height / 2)
        GUI_element_window.gui_init(self)

        self.objs = {}
        y = 0
        for text in ["Which size puzzle would you like to create?", "You can alter this later."]:
            txt = Text(self.game.core.media.fonts['window_text'], self.x + 28, self.y + 45 + y, TEXT_ALIGN_TOP_LEFT, text)
            txt.z = self.z - 2
            txt.colour = (0.3, 0.3, 0.3)
            self.objs['text_' + str(y)] = txt
            y += txt.text_height + 2 

        #self.puzzle_name_text = GUI_designer_puzzles_add_puzzle_puzzle_name_text_input(self.game, self)
        self.puzzle_width = GUI_designer_puzzles_add_puzzle_puzzle_width_input(self.game, self)
        self.puzzle_height = GUI_designer_puzzles_add_puzzle_puzzle_height_input(self.game, self)
        GUI_designer_puzzles_add_puzzle_puzzle_confirm_button(self.game, self)
        GUI_designer_puzzle_add_puzzle_puzzle_cancel_button(self.game, self)
        self.game.gui.block_gui_keyboard_input = True
        self.x = 0
        self.y = 0
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']


    def add_new_puzzle(self):
        dont_kill = False
        
        try:
            self.game.manager.add_new_puzzle("New Puzzle", self.game.manager.current_puzzle_pack, width = self.puzzle_width.current_value, height = self.puzzle_height.current_value)
        except IOError as e:
            GUI_element_dialog_box(self.game, self.parent, "Input error", [str(e)])
            dont_kill = True
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.game.manager.load_pack(self.game.manager.current_puzzle_pack)
            self.parent.scroll.reread_puzzles()
            if not dont_kill:
                self.Kill()
        

    def On_Exit(self):
        GUI_element_window.On_Exit(self)
        self.game.gui.block_gui_keyboard_input = False
        for x in self.objs:
            self.objs[x].Kill()



class GUI_designer_puzzles_add_puzzle_puzzle_name_text_input(GUI_element_text_input):
    label = "Puzzle name:"
    width = 380
    max_length = 25

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.x = self.parent.x + 30
        self.y = self.parent.y + 65
        self.gui_init()



class GUI_designer_puzzles_add_puzzle_puzzle_width_input(GUI_element_spinner):
    label = "Width:  "
    min_value = 5
    max_value = 40
    jump_count = 5

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.x = self.parent.x + 30
        self.y = self.parent.y + 95
        self.current_value = 5
        self.gui_init()



class GUI_designer_puzzles_add_puzzle_puzzle_height_input(GUI_element_spinner):
    label = "Height: "
    min_value = 5
    max_value = 40
    jump_count = 5

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.x = self.parent.x + 30
        self.y = self.parent.y + 125
        self.current_value = 5
        self.gui_init()



class GUI_designer_puzzles_add_puzzle_puzzle_confirm_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Add Puzzle"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) - (self.width) - 10
        self.y = self.parent.y + 160
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


    def mouse_left_up(self):
        self.parent.add_new_puzzle()



class GUI_designer_puzzle_add_puzzle_puzzle_cancel_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Cancel"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) + 10
        self.y = self.parent.y + 160
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


    def mouse_left_up(self):
        self.parent.Kill()



class GUI_designer_puzzles_puzzles_list_scroll_window(GUI_element_scroll_window):
    puzzle_items = []
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_4
        self.x = 114
        self.y = 150
        self.width = self.game.settings['screen_width'] - 226
        self.height = self.game.settings['screen_height'] - 190
        self.gui_init()
        self.reread_puzzles()


    def reread_puzzles(self):
        for x in self.puzzle_items:
            x.Kill()
        self.contents_scroll_location = 0.0
        self.puzzle_items = []
        num = 0
        last_item = None
        for puzzle_filename in self.game.manager.current_pack.order:
            last_item = GUI_designer_puzzles_puzzle_item(self.game, self, num, puzzle_filename, self.game.manager.current_pack.puzzles[puzzle_filename])
            self.puzzle_items.append(last_item)

            self.puzzle_items.append(
                GUI_designer_puzzles_button_edit_puzzle(self.game, self, num, puzzle_filename, self.game.manager.current_pack.puzzles[puzzle_filename])
            )
            self.puzzle_items.append(
                GUI_designer_puzzles_button_delete_puzzle(self.game, self, num, puzzle_filename, self.game.manager.current_pack.puzzles[puzzle_filename])
            )
            if not num == 0:
                self.puzzle_items.append(
                    GUI_designer_puzzles_button_move_puzzle_down(self.game, self, num, puzzle_filename, self.game.manager.current_pack.puzzles[puzzle_filename])
                    )
            if not num == len(self.game.manager.current_pack.order) - 1:
                self.puzzle_items.append(
                    GUI_designer_puzzles_button_move_puzzle_up(self.game, self, num, puzzle_filename, self.game.manager.current_pack.puzzles[puzzle_filename])
                    )

            num += 1

        if last_item is None:
            self.contents_height = 0
        else:
            self.contents_height = last_item.y + last_item.height + 10



class GUI_designer_puzzles_puzzle_item(GUI_element):

    def __init__(self, game, parent = None, puzzle_num = 0, puzzle_filename = None, puzzle_info = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.puzzle_num = puzzle_num
        self.puzzle_filename = puzzle_filename
        self.puzzle_info = puzzle_info
        self.z = Z_GUI_OBJECT_LEVEL_5

        self.x = 50
        self.y = (65 * self.puzzle_num) + 15 + (10 * self.puzzle_num)
        self.width = self.parent.width - 110
        self.height = 65
        self.gui_init()

        self.text_puzzle_name = Text(self.game.core.media.fonts['designer_pack_name'], self.x + self.scroll_element.x + 65, 0, TEXT_ALIGN_TOP_LEFT, str(self.puzzle_info[0]))
        self.text_puzzle_name.z = self.z - 1
        self.text_puzzle_name.colour = (0.95, 0.58, 0.09, 1.0)
        self.text_puzzle_name.shadow = 2
        self.text_puzzle_name.shadow_colour = (.8, .8, .8)

        self.text_puzzle_size = Text(self.game.core.media.fonts['designer_pack_author'], self.x + self.scroll_element.x + 75, 0, TEXT_ALIGN_TOP_LEFT, str(self.puzzle_info[1]) + "x" + str(self.puzzle_info[2]))
        self.text_puzzle_size.z = self.z - 2
        self.text_puzzle_size.colour = (.55, .55, .55)
        self.text_puzzle_size.shadow = 2
        self.text_puzzle_size.shadow_colour = (.8, .8, .8)

        Monochrome_puzzle_image(
            self.game,
            self,
            self.x + 6,
            self.y + 7,
            puzzle_path = os.path.join(self.game.core.path_user_pack_directory, self.game.manager.current_puzzle_pack, self.puzzle_filename),
            in_colour = False,
            fade_in_time = None
            )
            
        self.draw_strategy = "gui_designer_packs_pack_item"


    def Execute(self):
        self.update()

        self.text_puzzle_name.y = self.y + self.scroll_element.y + 0 - self.scroll_element.contents_scroll_location
        self.text_puzzle_name.clip = self.clip
        self.text_puzzle_size.y = self.y + self.scroll_element.y + 35 - self.scroll_element.contents_scroll_location
        self.text_puzzle_size.clip = self.clip
            
            
    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text_puzzle_name.Kill()
        self.text_puzzle_size.Kill()


    def mouse_not_over(self):
        self.alpha = .47

        
    def mouse_over(self):
        self.alpha = .78

        
    def mouse_left_up(self):
        self.game.manager.load_puzzle(self.game.manager.current_puzzle_pack, self.puzzle_filename, set_state = True)
        self.game.freemode = True
        self.game.gui.fade_toggle(lambda: self.game.gui.switch_gui_state_to(GUI_STATE_DESIGNER_DESIGNER), speed = 20)



class Monochrome_puzzle_image(Puzzle_image):
    
    def gui_init(self):
        Puzzle_image.gui_init(self)
        self.scroll_element = self.parent.parent
        #self.draw_strategy = "gui_designer_monochrome_puzzle_image"
        
        
    def set_position_z_scale(self, x, y):        
        self.x = x
        self.y = y
        self.z = Z_GUI_OBJECT_LEVEL_7 - 1
        scale_start = self.height if self.height > self.width else self.width
        self.scale = .01 * ((DESIGNER_PUZZLE_ICON_HEIGHT / scale_start) * 100)



class GUI_designer_puzzles_button_edit_puzzle(GUI_element_button):
    generic_button = False
    
    def __init__(self, game, parent = None, puzzle_num = 0, puzzle_filename = None, puzzle_info = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.puzzle_num = puzzle_num
        self.puzzle_filename = puzzle_filename
        self.puzzle_info = puzzle_info
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 185
        self.y = (65 * self.puzzle_num) + 15 + (10 * self.puzzle_num) + 3
        self.image = self.game.core.media.gfx['gui_button_designer_open']
        self.gui_init()
            

    def mouse_left_up(self):
        self.game.manager.load_puzzle(self.game.manager.current_puzzle_pack, self.puzzle_filename, set_state = True)
        self.game.freemode = True
        self.game.gui.fade_toggle(lambda: self.game.gui.switch_gui_state_to(GUI_STATE_DESIGNER_DESIGNER), speed = 20)
        #GUI_designer_puzzles_edit_puzzle_dialog(self.game, self.parent.parent, self.puzzle_filename, self.puzzle_info)



class GUI_designer_puzzles_button_delete_puzzle(GUI_element_button):
    generic_button = False
    
    def __init__(self, game, parent = None, puzzle_num = 0, puzzle_filename = None, puzzle_info = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.puzzle_num = puzzle_num
        self.puzzle_filename = puzzle_filename
        self.puzzle_info = puzzle_info
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 125
        self.y = (65 * self.puzzle_num) + 15 + (10 * self.puzzle_num) + 3
        self.image = self.game.core.media.gfx['gui_button_designer_delete']
        self.gui_init()


    def confirm(self):
        try:
            self.game.manager.delete_puzzle(self.game.manager.current_puzzle_pack, self.puzzle_filename)
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.game.manager.load_pack(self.game.manager.current_puzzle_pack)
            self.parent.reread_puzzles()


    def mouse_left_up(self):
        self.conf_box = GUI_element_confirmation_box(
            self.game,
            self,
            "Really Delete?",
            ["Are you sure you want to delete this puzzle", str("%s?" % self.puzzle_info[0]), "It will be permanently deleted."],
            confirm_callback = self.confirm
            )



class GUI_designer_puzzles_edit_puzzle_dialog(GUI_element_window):
    title = "Edit Puzzle"
    height = 150
    width = 500
    objs = {}

    def __init__(self, game, parent = None, puzzle_filename = None, puzzle_info = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.puzzle_filename = puzzle_filename
        self.puzzle_info = puzzle_info
        self.gui_init()

    
    def gui_init(self):
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.x = (self.game.settings['screen_width'] / 2) - (self.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) - (self.height / 2)
        GUI_element_window.gui_init(self)

        self.objs = {}
        y = 0
        for text in ["Using this dialog you can edit the name for this puzzle."]:
            txt = Text(self.game.core.media.fonts['window_text'], self.x + 28, self.y + 45 + y, TEXT_ALIGN_TOP_LEFT, text)
            txt.z = self.z - 2
            txt.colour = (0.3, 0.3, 0.3)
            self.objs['text_' + str(y)] = txt
            y += txt.text_height + 2 

        self.puzzle_name_text = GUI_designer_puzzles_add_puzzle_puzzle_name_text_input(self.game, self)
        self.puzzle_name_text.set_current_text_to(self.puzzle_info[0])
        GUI_designer_puzzles_edit_puzzle_puzzle_confirm_button(self.game, self)
        GUI_designer_puzzle_edit_puzzle_puzzle_cancel_button(self.game, self)
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


    def edit_puzzle(self):
        dont_kill = False

        try:
            self.game.manager.edit_puzzle(self.game.manager.current_puzzle_pack, self.puzzle_filename, self.puzzle_name_text.current_text)
        except IOError as e:
            GUI_element_dialog_box(self.game, self.parent, "Input error", [str(e)])
            dont_kill = True
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.game.manager.load_pack(self.game.manager.current_puzzle_pack)
            self.parent.scroll.reread_puzzles()
            if not dont_kill:
                self.Kill()

                
    def On_Exit(self):
        GUI_element_window.On_Exit(self)
        self.game.gui.block_gui_keyboard_input = False
        for x in self.objs:
            self.objs[x].Kill()
            


class GUI_designer_puzzles_edit_puzzle_puzzle_confirm_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Confirm"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) - (self.width) - 10
        self.y = self.parent.y + 100
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


    def mouse_left_up(self):
        self.parent.edit_puzzle()



class GUI_designer_puzzle_edit_puzzle_puzzle_cancel_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Cancel"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) + 10
        self.y = self.parent.y + 100
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


    def mouse_left_up(self):
        self.parent.Kill()



class GUI_designer_puzzles_button_move_puzzle_down(GUI_element_button):
    generic_button = False
    width = 32
    height = 32
    def __init__(self, game, parent = None, puzzle_num = 0, puzzle_filename = None, puzzle_info = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.puzzle_num = puzzle_num
        self.puzzle_filename = puzzle_filename
        self.puzzle_info = puzzle_info
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.x - 100
        self.y = (65 * self.puzzle_num) + 15 + (10 * self.puzzle_num) + 5
        self.image = self.game.core.media.gfx['gui_button_designer_move_down']
        self.gui_init()
            

    def mouse_left_up(self):
        try:
            self.game.manager.move_pack_puzzle_down(self.game.manager.current_puzzle_pack, self.puzzle_filename)
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.game.manager.load_pack(self.game.manager.current_puzzle_pack)
            self.parent.reread_puzzles()



class GUI_designer_puzzles_button_move_puzzle_up(GUI_element_button):
    generic_button = False
    width = 32
    height = 32
    def __init__(self, game, parent = None, puzzle_num = 0, puzzle_filename = None, puzzle_info = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.puzzle_num = puzzle_num
        self.puzzle_filename = puzzle_filename
        self.puzzle_info = puzzle_info
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.x - 100
        self.y = (65 * self.puzzle_num) + 15 + (10 * self.puzzle_num) + 33
        self.image = self.game.core.media.gfx['gui_button_designer_move_up']
        self.gui_init()
            

    def mouse_left_up(self):
        try:
            self.game.manager.move_pack_puzzle_up(self.game.manager.current_puzzle_pack, self.puzzle_filename)
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.game.manager.load_pack(self.game.manager.current_puzzle_pack)
            self.parent.reread_puzzles()



###############################################################
######################## DESIGNER #############################
###############################################################



class Undo_manager_mixin(object):
    """
    Used as a mixin, this gives an object access to a number of members
    and methods related to undo/redo.
    Expects self.game to be set in the child class.
    GUI_puzzle should call methods from this directly.
    """
    action_stack = []
    stack_pos = -1


    def reset_stack(self):
        self.action_stack = []
        self.stack_pos = -1


    def can_undo(self):
        return True if len(self.action_stack) > 0 and self.stack_pos > -1 else False


    def can_redo(self):
        return True if len(self.action_stack) > 0 and not self.stack_pos + 1 == len(self.action_stack) else False
        

    def trim_stack(self):
        if len(self.action_stack) > MAX_UNDO_STACK:
            self.action_stack = self.action_stack[-MAX_UNDO_STACK:]
            

    def add_new_action(self, action):
        self.trim_stack()
        self.action_stack = self.action_stack[:self.stack_pos+1]
        self.action_stack.append(action)
        self.stack_pos = len(self.action_stack)-1


    def undo(self):
        if not self.can_undo():
            return

        undo_action = self.action_stack[self.stack_pos]
        self.stack_pos -= 1

        undo_action[0](undo_action[1])


    def redo(self):
        if not self.can_redo():
            return
        
        redo_action = self.action_stack[self.stack_pos + 1]
        self.stack_pos += 1

        redo_action[0](redo_action[2])



class GUI_designer_designer_container(GUI_element, Undo_manager_mixin):
    """
    All elements in the actual puzzle drawing designer live here.
    """
    title = None
    puzzle_object = None

    need_to_save = False

    tool = DRAWING_TOOL_STATE_DRAW
    tool_message_display = False 

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_CONTAINERS
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.alpha = 0.1

        GUI_designer_designer_menu_bar(self.game, self)
        self.set_title(self.game.manager.current_puzzle.name, str(self.game.manager.current_puzzle.width) + " x " + str(self.game.manager.current_puzzle.height))
        self.back_button = GUI_designer_designer_back(self.game, self)
        self.puzzle_object = GUI_puzzle(self.game, self)
        GUI_verify_status(self.game, self, self.puzzle_object)
        GUI_designer_designer_edit_name_button(self.game, self)
        GUI_designer_designer_change_size_button(self.game, self)
        #GUI_designer_designer_change_puzzle_background_button(self.game, self)
        GUI_designer_designer_undo_button(self.game, self)
        GUI_designer_designer_redo_button(self.game, self)

        self.tool_buttons = []
        self.tool_buttons.append(GUI_designer_designer_flood_fill_button(self.game, self))
        #self.tool_buttons.append(GUI_designer_designer_rectangle_button(self.game, self))

        """
        self.tool_message = Text(self.game.core.media.fonts['menu_subtitles'], self.game.settings['screen_width'] / 2,  150, TEXT_ALIGN_CENTER, "Left click to fill squares. Right click to clear.")
        self.tool_message.colour = (.2,.2,.2)
        self.tool_message.z = Z_GUI_OBJECT_LEVEL_4
        """ 

    def Execute(self):
        self.update()
        #self.tool_message.alpha = 1.0 if self.tool_message_display else 0.0

        if not self.game.gui.block_gui_keyboard_input:
            if self.game.core.Keyboard_key_released(key.ESCAPE):
                self.back_button.mouse_left_up()


    def untoggle_tools(self, ignore):
        for tool in self.tool_buttons:
            if not tool == ignore:
                tool.toggle_state = False


    def set_title(self, title, subtitle):
        if not self.title is None:
            self.title.Kill()
        self.title = GUI_designer_title(self.game, self, title = str(title), subtitle = str(subtitle), no_background = True, small = True)


    def On_Exit(self):
        GUI_element.On_Exit(self)
        #self.tool_message.Kill()



class GUI_designer_designer_menu_bar(GUI_element):
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_4
        self.width = self.game.settings['screen_width']
        self.height = 144
        self.alpha = 0.3
        self.draw_strategy = "gui_designer_designer_menu_bar"


    def mouse_over(self):
        self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL



class GUI_designer_designer_back(GUI_element_button):
    generic_button = False
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_back']
        self.x = 8
        self.y = 65
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.width = 68
        self.height = 68
        self.gui_init()


    def action(self):
        self.game.gui.fade_toggle(lambda: self.game.gui.switch_gui_state_to(GUI_STATE_DESIGNER_PUZZLES), speed = 20)


    def mouse_left_up(self):
        if self.parent.need_to_save:
            GUI_element_confirmation_box(
                self.game,
                self,
                "Really Quit?",
                ["Are you sure you want to leave the puzzle designer?", "All unsaved changes will be lost."],
                confirm_callback = self.action
                )
        else:
            self.action()



class GUI_verify_status(GUI_element):
    def __init__(self, game, parent, puzzle):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.puzzle = puzzle
        self.x = self.game.settings['screen_width'] - 410
        self.y = -8
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.current_solver_state = None
        self.text = Text(self.game.core.media.fonts['verifier_status'], self.x + 64, self.y + 120, TEXT_ALIGN_CENTER, "Solving")
        self.text.colour = (.5,.5,.5)
        self.text.z = self.z
        self.image = self.game.core.media.gfx['gui_verify_status']
        self.gui_init()
        self.objs = []
        self.throbber_sequence = 1
        self.throbber_count = 0

    def Execute(self):
        if not self.current_solver_state == self.puzzle.puzzle_solver_state: 
            self.current_solver_state = self.puzzle.puzzle_solver_state
            for x in self.objs:
                x.Kill()
            self.objs = []
            if self.current_solver_state is None:
                self.image = self.game.core.media.gfx['gui_designer_throbber']
                self.text.text = "Verifying Puzzle"                    
            elif self.current_solver_state == True:
                self.image = self.game.core.media.gfx['gui_verify_status']
                self.image_sequence = 2
                self.text.text = "Valid Puzzle"
                self.objs.append(
                    GUI_designer_designer_save_puzzle_button(self.game, self)
                    )
                self.objs.append(
                    GUI_designer_designer_colour_puzzle_button(self.game, self)
                    )
                self.objs.append(
                    GUI_designer_designer_test_puzzle_button(self.game, self)
                    )
            elif self.current_solver_state == False:
                self.image = self.game.core.media.gfx['gui_verify_status']
                self.image_sequence = 3                    
                self.text.text = "Invalid Puzzle"
                self.objs.append(
                    GUI_designer_designer_save_puzzle_button(self.game, self, force_disabled = True)
                    )
                self.objs.append(
                    GUI_designer_designer_colour_puzzle_button(self.game, self, force_disabled = True)
                    )
                self.objs.append(
                    GUI_designer_designer_test_puzzle_button(self.game, self, force_disabled = True)
                    )
                self.objs.append(
                    GUI_designer_designer_invalid_puzzle_question_mark_button(self.game, self)
                    )

        if self.current_solver_state is None:
            self.throbber_count += 1
            self.image_sequence = self.throbber_sequence
            if self.throbber_count > 5:
                self.throbber_count = 0
                self.throbber_sequence += 1
                if self.throbber_sequence > 10:
                    self.throbber_sequence = 1                    
            
        self.update()


    def On_Exit(self):
        self.text.Kill()
        for x in self.objs:
            x.Kill()



class GUI_designer_designer_invalid_puzzle_question_mark_button(GUI_element_button):
    generic_button = False
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_help']
        self.x = self.game.settings['screen_width'] - 280
        self.y = 16
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_dialog_box(
            self.game, self.parent, "What does this mean?",
            [
            "All PixelPics puzzles must be solvable using logical solving techniques.",
            "PixelPics runs a number of algoritms to determine if your puzzle",
            "can be solved without resorting to guessing.",
            " ",
            "It's usually easy to alter your puzzle to make them solvable.",
            "Keep experimenting by changing only a few squares at a time.",
            ]
            )



class GUI_designer_designer_save_puzzle_button(GUI_element_button):
    generic_button = False
    disabled = True
    width = 68
    height = 68
    def __init__(self, game, parent, force_disabled = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_save']
        self.x = self.game.settings['screen_width'] - 240
        self.y = 65
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.force_disabled = force_disabled
        self.gui_init()


    def Execute(self):
        self.update()
        if self.force_disabled:
            self.disabled = True
        else:
            self.disabled = not self.parent.parent.need_to_save


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        try:
            self.game.manager.save_puzzle(self.game.manager.current_puzzle_pack, self.game.manager.current_puzzle_file, self.game.manager.current_puzzle)
            self.parent.parent.need_to_save = False
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.game.manager.load_pack(self.game.manager.current_puzzle_pack)



class GUI_designer_designer_colour_puzzle_button(GUI_element_button):
    width = 68
    height = 68
    generic_button = False
    def __init__(self, game, parent, force_disabled = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_paint']
        self.x = self.game.settings['screen_width'] - 160
        self.y = 65
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.force_disabled = force_disabled
        self.gui_init()


    def Execute(self):
        self.update()
        if self.force_disabled:
            self.disabled = True
        else:
            self.disabled = self.parent.parent.need_to_save


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        self.game.gui.fade_toggle(lambda: self.game.gui.switch_gui_state_to(GUI_STATE_DESIGNER_COLOUR), speed = 10)



class GUI_designer_designer_test_puzzle_button(GUI_element_button):
    width = 68
    height = 68
    generic_button = False
    def __init__(self, game, parent, force_disabled = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_test']
        self.x = self.game.settings['screen_width'] - 80
        self.y = 65
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.force_disabled = force_disabled
        self.gui_init()


    def Execute(self):
        self.update()
        if self.force_disabled:
            self.disabled = True
        else:
            self.disabled = self.parent.parent.need_to_save


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        self.game.manager.reset_puzzle_state()
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_TEST), speed = 20)



class GUI_designer_designer_edit_name_button(GUI_element_button):
    generic_button = False
    width = 68
    height = 68
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_name']
        self.x = self.game.settings['screen_width'] - 590
        self.y = 65
        self.width = 68
        self.height = 68
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def mouse_left_up(self):
        GUI_designer_puzzles_edit_name_dialog(self.game, self.parent, self.game.manager.current_puzzle_file, self.game.manager.current_pack.puzzles[self.game.manager.current_puzzle_file])



class GUI_designer_designer_change_size_button(GUI_element_button):
    generic_button = False
    width = 68
    height = 68
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_size']
        self.x = self.game.settings['screen_width'] - 510
        self.y = 65
        self.width = 68
        self.height = 68
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def mouse_left_up(self):
        GUI_designer_puzzles_change_size_dialog(self.game, self.parent)



class GUI_designer_puzzles_edit_name_dialog(GUI_designer_puzzles_edit_puzzle_dialog):
    title = "Edit Name"
    def edit_puzzle(self):
        dont_kill = False
        try:
            self.game.manager.current_puzzle.name = self.puzzle_name_text.current_text
        except IOError as e:
            GUI_element_dialog_box(self.game, self.parent, "Input error", [str(e)])
            dont_kill = True
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.parent.need_to_save = True
            self.parent.set_title(self.puzzle_name_text.current_text, str(self.game.manager.current_puzzle.width) + " x " + str(self.game.manager.current_puzzle.height))
            if not dont_kill:
                self.Kill()



class GUI_designer_puzzles_change_size_dialog(GUI_element_window):
    title = "Change Size"
    height = 210
    width = 500
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
        for text in ["Using this dialog you can edit the size of this puzzle.", "Note that reducing the size could cause you to lose", "some of the shape you've drawn."]:
            txt = Text(self.game.core.media.fonts['window_text'], self.x + 28, self.y + 45 + y, TEXT_ALIGN_TOP_LEFT, text)
            txt.z = self.z - 2
            txt.colour = (0.3, 0.3, 0.3)
            self.objs['text_' + str(y)] = txt
            y += txt.text_height + 2 

        self.puzzle_width = GUI_designer_puzzle_change_size_width_spinner(self.game, self)
        self.puzzle_width.set_current_value(self.game.manager.current_puzzle.width)
        self.puzzle_height = GUI_designer_puzzle_change_size_height_spinner(self.game, self)
        self.puzzle_height.set_current_value(self.game.manager.current_puzzle.height)
        GUI_designer_puzzle_change_size_confirm_button(self.game, self)
        GUI_designer_puzzle_change_size_cancel_button(self.game, self)
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


    def edit_puzzle(self):
        dont_kill = False

        try:
            self.game.manager.change_current_puzzle_size(self.puzzle_width.current_value, self.puzzle_height.current_value)
        except IOError as e:
            GUI_element_dialog_box(self.game, self.parent, "Input error", [str(e)])
            dont_kill = True
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.parent.puzzle_object.reload_puzzle_display()
            self.parent.need_to_save = True
            self.parent.reset_stack()
            self.parent.set_title(self.game.manager.current_puzzle.name, str(self.puzzle_width.current_value) + " x " + str(self.puzzle_height.current_value))
            if not dont_kill:
                self.Kill()

                
    def On_Exit(self):
        GUI_element_window.On_Exit(self)
        self.game.gui.block_gui_keyboard_input = False
        for x in self.objs:
            self.objs[x].Kill()
            


class GUI_designer_puzzle_change_size_width_spinner(GUI_element_spinner):
    label = "Width:  "
    min_value = 5
    max_value = 40
    jump_count = 5

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.x = self.parent.x + 30
        self.y = self.parent.y + 110
        self.gui_init()



class GUI_designer_puzzle_change_size_height_spinner(GUI_element_spinner):
    label = "Height: "
    min_value = 5
    max_value = 40
    jump_count = 5

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.x = self.parent.x + 30
        self.y = self.parent.y + 140
        self.gui_init()



class GUI_designer_puzzle_change_size_confirm_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Confirm"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) - (self.width) - 10
        self.y = self.parent.y + 170
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


    def mouse_left_up(self):
        self.parent.edit_puzzle()



class GUI_designer_puzzle_change_size_cancel_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Cancel"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) + 10
        self.y = self.parent.y + 170
        self.generic_button_text_object.x = self.x + (self.width / 2)
        self.generic_button_text_object.y = self.y + (self.height / 2)


    def mouse_left_up(self):
        self.parent.Kill()



class GUI_designer_designer_change_puzzle_background_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Change Puzzle Background"
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = 350
        self.y = 60
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def mouse_left_up(self):
        GUI_designer_puzzles_change_puzzle_background_dialog(self.game, self.parent)
    


class GUI_designer_designer_undo_button(GUI_element_button):
    generic_button = False
    width = 68
    height = 68
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_undo']
        self.x = self.game.settings['screen_width'] - 770
        self.y = 65
        self.width = 68
        self.height = 68
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def Execute(self):
        self.disabled = not self.parent.can_undo()
        self.update()


    def mouse_left_up(self):
        self.parent.undo()



class GUI_designer_designer_redo_button(GUI_element_button):
    generic_button = False
    width = 68
    height = 68
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_redo']
        self.x = self.game.settings['screen_width'] - 690
        self.y = 65
        self.width = 68
        self.height = 68
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def Execute(self):
        self.disabled = not self.parent.can_redo()
        self.update()


    def mouse_left_up(self):
        self.parent.redo()
        


class GUI_designer_designer_flood_fill_button(GUI_element_button):
    generic_button = False
    width = 68
    height = 68
    toggle_button = True
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_fill']
        self.x = self.game.settings['screen_width'] - 870
        self.y = 65
        self.width = 68
        self.height = 68
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def mouse_left_up(self):
        self.parent.untoggle_tools(self)
        self.mouse_left_up_toggle()
        if self.toggle_state:
            self.parent.tool = DRAWING_TOOL_STATE_FILL
            self.parent.tool_message_display = True
        else:
            self.parent.tool = DRAWING_TOOL_STATE_DRAW
            self.parent.tool_message_display = False



class GUI_designer_designer_rectangle_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Rectangle"
    toggle_button = True
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = 450
        self.y = 90
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def mouse_left_up(self):
        self.parent.untoggle_tools(self)
        self.mouse_left_up_toggle()
        if self.toggle_state:
            self.parent.tool = DRAWING_TOOL_STATE_RECTANGLE
            self.parent.tool_message_display = True
        else:
            self.parent.tool = DRAWING_TOOL_STATE_DRAW
            self.parent.tool_message_display = False



class GUI_designer_puzzles_change_puzzle_background_dialog(GUI_element_window):
    title = "Puzzle Background"
    height = 490
    width = 550
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

        GUI_designer_puzzle_change_puzzle_background_cancel_button(self.game, self)
        GUI_designer_puzzle_change_puzzle_background_apply_button(self.game, self)
        GUI_designer_puzzle_change_puzzle_background_scroll_window(self.game, self)

        self.selected_background = self.game.manager.current_puzzle.background
        
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


    def edit_puzzle(self):
        dont_kill = False

        try:
            self.game.manager.change_current_puzzle_background(self.selected_background)
        except IOError as e:
            GUI_element_dialog_box(self.game, self.parent, "Input error", [str(e)])
            dont_kill = True
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            #self.parent.puzzle_object.reload_puzzle_background()
            if not dont_kill:
                self.Kill()

                
    def On_Exit(self):
        GUI_element_window.On_Exit(self)
        self.game.gui.block_gui_keyboard_input = False
        for x in self.objs:
            self.objs[x].Kill()



class GUI_designer_puzzle_change_puzzle_background_apply_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Apply"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + self.parent.width - 175
        self.y = self.parent.y + self.parent.height - 50
        self.generic_button_text_object.x = self.x + 9
        self.generic_button_text_object.y = self.y + 4


    def mouse_left_up(self):
        self.parent.edit_puzzle()



class GUI_designer_puzzle_change_puzzle_background_cancel_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Cancel"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + self.parent.width - 100
        self.y = self.parent.y + self.parent.height - 50
        self.generic_button_text_object.x = self.x + 9
        self.generic_button_text_object.y = self.y + 4


    def mouse_left_up(self):
        self.parent.Kill()



class GUI_designer_puzzle_change_puzzle_background_scroll_window(GUI_element_scroll_window):
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.x = self.parent.x + 25
        self.y = self.parent.y + 30
        self.width = 500
        self.height = 400
        self.gui_init()

        num = 0
        for background_name in BACKGROUNDS:
            GUI_designer_puzzle_change_puzzle_background_item(self.game, self, background_name, num)
            num+=1



class GUI_designer_puzzle_change_puzzle_background_item(GUI_element):
    def __init__(self, game, parent = None, background = "", num = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.z = self.parent.z - 2
        self.x = ((num % 3) * 128) + ((num % 3) * 16) + 16
        self.y = ((num / 3) * 128) + ((num / 3) * 16) + 16
        self.width = 128
        self.height = 128
        self.gui_init()
        
        self.draw_strategy = "designer_puzzle_background_item"
        self.draw_strategy_colour = (
            BACKGROUNDS[background]['data'],
            BACKGROUNDS[background]['data'],
            (1.0,1.0,1.0,1.0),
            BACKGROUNDS[background]['data'],
            )

        self.hover = False
        self.is_current = False
        self.background = background


    def mouse_over(self):
        self.hover = True


    def mouse_not_over(self):
        self.hover = False


    def mouse_left_up(self):
        self.parent.parent.selected_background = self.background


    def Execute(self):
        self.update()
        self.is_current = (self.parent.parent.selected_background == self.background)
    


###############################################################
######################## COLOURING ############################
###############################################################



class GUI_designer_colour_container(GUI_element, Undo_manager_mixin):
    """
    Container for all elements in the puzzle colouring in book
    """
    title = None
    puzzle_object = None

    need_to_save = False

    tool = DRAWING_TOOL_STATE_DRAW

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_CONTAINERS
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.alpha = 0.1

        GUI_designer_colour_menu_bar(self.game, self)
        self.title = GUI_designer_title(
            self.game,
            self,
            title = str(self.game.manager.current_puzzle.name),
            subtitle = str(self.game.manager.current_puzzle.width) + " x " + str(self.game.manager.current_puzzle.height),
            no_background = True,
            small = True
            )
        self.back_button = GUI_designer_designer_back(self.game, self)
        self.puzzle_object = GUI_designer_colour_puzzle(self.game, self)
        #GUI_designer_designer_change_puzzle_background_button(self.game, self)
        GUI_designer_colour_undo_button(self.game, self)
        GUI_designer_colour_redo_button(self.game, self)

        GUI_designer_colour_copy_from_puzzle_button(self.game, self)
        GUI_designer_colour_save_puzzle_button(self.game, self)
        GUI_designer_colour_puzzle_button(self.game, self)
        GUI_designer_colour_test_puzzle_button(self.game, self)
        GUI_designer_colour_flood_fill_button(self.game, self)

        self.palette_object = GUI_designer_colour_colour_picker(self.game, self)
        self.value_slider_object = GUI_designer_colour_value_slider(self.game, self)        
        self.current_colour_object = GUI_designer_colour_current_colour(self.game, self)

        self.text_offset_x = 0.0
        self.text_offset_y = 0.0
        self.draw_strategy = "designer_background"


    def Execute(self):
        self.text_offset_x += 5.0
        self.text_offset_y -= 5.0
        self.update()

        if not self.game.gui.block_gui_keyboard_input:
            if self.game.core.Keyboard_key_released(key.ESCAPE):
                self.back_button.mouse_left_up()


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.puzzle_object.Kill()
        self.palette_object.Kill()
        self.value_slider_object.Kill()
        self.current_colour_object.Kill()



class GUI_designer_colour_puzzle(GUI_element):
    """
    The colourable element
    """
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent        
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_1
        self.reload_puzzle_display()

        # Init stuff
        self.camera_pos = [0.0, 0.0]
        self.remember_mouse_pos = (0, 0)
        self.currently_panning = False        
        self.last_hovered_cell = (-1, -1)
        self.hovered_column = -1
        self.hovered_row = -1

        self.x = 0
        self.y = 0
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.grid_width = float(PUZZLE_CELL_WIDTH * self.game.manager.current_puzzle.width)
        self.grid_height = float(PUZZLE_CELL_HEIGHT * self.game.manager.current_puzzle.height)
        
        self.adjust_gui_coords()
        self.camera_pos = [0.0, 64.0]

        self.puzzle_display = GUI_designer_colour_puzzle_display(self.game, self, self.grid_x, self.grid_y)
        

    def Execute(self):
        self.adjust_gui_coords()
        

    def reload_puzzle_display(self):
        self.grid_width = float(PUZZLE_CELL_WIDTH * self.game.manager.current_puzzle.width)
        self.grid_height = float(PUZZLE_CELL_HEIGHT * self.game.manager.current_puzzle.height)

        self.grid_x = 0.0
        self.grid_y = 0.0

        # Determine optimum zoom level
        self.game.current_zoom_level = min(
            (float(self.game.settings['screen_width']) / (self.grid_width)),
            (float(self.game.settings['screen_height']) / (self.grid_height + 256))
            )

        if self.game.current_zoom_level > 1.0:
            self.game.current_zoom_level = 1.0
        self.game.minimum_zoom_level = self.game.current_zoom_level / 2

        # Work out initial placement of the grid
        self.grid_x = (-((self.grid_width) / 2))
        self.grid_y = (-((self.grid_height - (256 if self.game.current_zoom_level < 1.0 else 0)) / 2))
        
        self.draw_strategy = "primitive_square"
        self.primitive_square_colour = (0.0,0.0,0.0,1.0)


    def adjust_gui_coords(self):
        # Adjust my x/y
        self.grid_gui_x = ((self.grid_x - self.camera_pos[0]) * self.game.current_zoom_level) + (self.game.settings['screen_width'] / 2)
        self.grid_gui_y = ((self.grid_y - self.camera_pos[1]) * self.game.current_zoom_level) + (self.game.settings['screen_height'] / 2)

        # Adjust my size
        self.grid_gui_width = self.grid_width * self.game.current_zoom_level
        self.grid_gui_height = self.grid_height * self.game.current_zoom_level

        self.primitive_square_x = self.grid_gui_x - 1.0
        self.primitive_square_y = self.grid_gui_y - 1.0
        self.primitive_square_width = self.grid_gui_width + 2.0
        self.primitive_square_height = self.grid_gui_height + 2.0


    def adjust_camera_pos(self, x, y):
        self.camera_pos[0] -= x
        self.camera_pos[1] -= y
        
        if self.camera_pos[0] < -((self.grid_width) / 2):
            self.camera_pos[0] = -((self.grid_width) / 2)
        if self.camera_pos[0] > (self.grid_width) / 2:
            self.camera_pos[0] = (self.grid_width) / 2
            
        if self.camera_pos[1] < -((self.grid_height) / 2):
            self.camera_pos[1] = -((self.grid_height) / 2)
        if self.camera_pos[1] > (self.grid_height) / 2:
            self.camera_pos[1] = (self.grid_height) / 2


    def mouse_over(self):
        if self.currently_panning:
            return

        self.remember_mouse_pos = (self.game.gui.mouse.x, self.game.gui.mouse.y)

        if self.game.gui.mouse.x > self.grid_gui_x and \
               self.game.gui.mouse.x < self.grid_gui_x + self.grid_gui_width and \
               self.game.gui.mouse.y > self.grid_gui_y and \
               self.game.gui.mouse.y < self.grid_gui_y + self.grid_gui_height:
            self.last_hovered_cell = (self.hovered_row, self.hovered_column)
            mouse_x = self.game.gui.mouse.x - self.grid_gui_x 
            mouse_y = self.game.gui.mouse.y - self.grid_gui_y
            self.hovered_column = int(mouse_x / (PUZZLE_CELL_WIDTH * self.game.current_zoom_level))
            self.hovered_row = int(mouse_y / (PUZZLE_CELL_HEIGHT  * self.game.current_zoom_level))
        else:
            self.last_hovered_cell = (self.hovered_row, self.hovered_column)
            self.hovered_column = -1
            self.hovered_row = -1


    def mouse_middle_down(self):
        diff = (self.game.gui.mouse.x - self.remember_mouse_pos[0], self.game.gui.mouse.y - self.remember_mouse_pos[1])
        self.adjust_camera_pos(diff[0], diff[1])

        self.currently_panning = True
        self.game.gui.mouse.alpha = 0.0
        self.game.core.mouse.set_pos(int(self.remember_mouse_pos[0]), int(self.remember_mouse_pos[1]))
        

    def mouse_middle_up(self):
        self.remember_mouse_pos = (0, 0)
        self.currently_panning = False
        self.game.gui.mouse.alpha = 1.0


    def mouse_left_down(self):
        if self.currently_panning:
            return

        if not self.parent.tool == DRAWING_TOOL_STATE_DRAW:
            return

        self.game.core.media.sfx['paint'].play(0)                
        self.colour_cell(list(self.parent.palette_object.selected_hsv_colour), (self.hovered_row, self.hovered_column))


    def mouse_left_up(self):
        if self.parent.tool == DRAWING_TOOL_STATE_FILL:
            cell_list = []
            self.checked_fill_stack = []
            self.fill_stack = [(self.hovered_row, self.hovered_column)]
            start_colour = list(self.game.manager.current_puzzle.cells[self.hovered_row][self.hovered_column][1])
            while self.fill_at(start_colour, list(self.parent.palette_object.selected_hsv_colour), cell_list):
                pass
            if len(cell_list) > 0:
                self.parent.need_to_save = True        
                self.change_cells(cell_list, list(self.parent.palette_object.selected_hsv_colour))
                self.game.core.media.sfx['fill'].play(0)                


    def mouse_right_up(self):
        if self.currently_panning:
            return

        if -1 in (self.hovered_row, self.hovered_column):
            return

        self.game.core.media.sfx['pipette'].play(0)                
        self.parent.palette_object.change_selected_colour(list(self.game.manager.current_puzzle.cells[self.hovered_row][self.hovered_column][1]))


    def colour_cell(self, hsv_colour, cell):
        if -1 in cell:
            return

        if self.game.manager.current_puzzle.cells[cell[0]][cell[1]][1] == hsv_colour:
            return

        self.parent.need_to_save = True

        self.change_cells([(cell[0], cell[1])], hsv_colour)


    def change_cells(self, cells, to):
        undo_data = []
        redo_data = []
        for x in cells:
            undo_data.append((x[0], x[1], self.game.manager.current_puzzle.cells[x[0]][x[1]][1]))
            redo_data.append((x[0], x[1], to))
        self.do_change_cells(redo_data)
        self.parent.add_new_action((self.do_change_cells, undo_data, redo_data))


    def do_change_cells(self, data):
        for cell in data:
            self.game.manager.set_puzzle_cell(
                self.game.manager.current_puzzle,
                cell[1], cell[0],
                self.game.manager.current_puzzle.cells[cell[0]][cell[1]][0],
                cell[2]
                )

        self.puzzle_display.reload_image()


    def fill_at(self, start_colour, value, cell_list):
        cell = self.fill_stack.pop()

        if -1 in cell or not self.game.manager.current_puzzle.cells[cell[0]][cell[1]][1] == start_colour or cell in self.checked_fill_stack:
            return len(self.fill_stack) > 0
        
        self.checked_fill_stack.append(cell)
        cell_list.append(cell)

        surrounding_cells = [
            (cell[0] - 1, cell[1]),
            (cell[0] + 1, cell[1]),
            (cell[0], cell[1] - 1),
            (cell[0], cell[1] + 1)
            ]

        for cell_check in surrounding_cells:
            if cell_check in self.checked_fill_stack:
                continue
            if cell_check[0] < 0 or cell_check[1] < 0:
                self.checked_fill_stack.append(cell_check)
                continue
            if cell_check[0] < len(self.game.manager.current_puzzle.cells) and cell_check[1] < len(self.game.manager.current_puzzle.cells[cell_check[0]]):
                self.fill_stack.append(cell_check)

        return len(self.fill_stack) > 0



class GUI_designer_colour_puzzle_display(Puzzle_image):
    def set_position_z_scale(self, x, y):
        self.x = ((x - self.parent.camera_pos[0]) * self.game.current_zoom_level) + (self.game.settings['screen_width'] / 2)
        self.y = ((y - self.parent.camera_pos[1]) * self.game.current_zoom_level) + (self.game.settings['screen_height'] / 2)
        self.z = self.parent.z - 1
        self.scale = PUZZLE_CELL_WIDTH * self.game.current_zoom_level



class GUI_designer_colour_menu_bar(GUI_element):
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_4
        self.width = self.game.settings['screen_width']
        self.height = 144
        self.alpha = 0.3
        self.draw_strategy = "gui_designer_designer_menu_bar"


    def mouse_over(self):
        self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL



class GUI_designer_colour_copy_from_puzzle_button(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_copy']
        self.x = self.game.settings['screen_width'] - 940
        self.y = 65
        self.width = 68
        self.height = 68
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def confirm(self):
        try:
            self.game.manager.set_cell_colours_to_values(self.game.manager.current_puzzle)
            self.parent.need_to_save = True
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.parent.puzzle_object.puzzle_display.reload_image()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        self.conf_box = GUI_element_confirmation_box(
            self.game,
            self,
            "Really Reset Colouring?",
            ["This will reset all colours to resemble the puzzle solution.", "This is useful to have a starting point for colouring.", "Are you sure you want to do this?"],
            confirm_callback = self.confirm
            )



class GUI_designer_colour_save_puzzle_button(GUI_element_button):
    generic_button = False
    disabled = True
    width = 68
    height = 68
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_save']
        self.x = self.game.settings['screen_width'] - 240
        self.y = 65
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def Execute(self):
        self.update()
        self.disabled = not self.parent.need_to_save


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        try:
            self.game.manager.save_puzzle(self.game.manager.current_puzzle_pack, self.game.manager.current_puzzle_file, self.game.manager.current_puzzle)
            self.parent.need_to_save = False
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.game.manager.load_pack(self.game.manager.current_puzzle_pack)



class GUI_designer_colour_puzzle_button(GUI_element_button):
    width = 68
    height = 68
    generic_button = False
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_puzzle']
        self.x = self.game.settings['screen_width'] - 160
        self.y = 65
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def Execute(self):
        self.update()
        self.disabled = self.parent.need_to_save


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        self.game.gui.fade_toggle(lambda: self.game.gui.switch_gui_state_to(GUI_STATE_DESIGNER_DESIGNER), speed = 10)



class GUI_designer_colour_test_puzzle_button(GUI_element_button):
    width = 68
    height = 68
    generic_button = False
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_test']
        self.x = self.game.settings['screen_width'] - 80
        self.y = 65
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def Execute(self):
        self.update()
        self.disabled = self.parent.need_to_save


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        self.game.manager.reset_puzzle_state()
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_TEST), speed = 20)



class GUI_designer_colour_colour_picker(GUI_element):

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.y = 65
        self.x = self.game.settings['screen_width'] - 600
        self.y = 15
        self.z = Z_GUI_OBJECT_LEVEL_7
        self.width = 316 #austin
        self.height = 118

        self.selected_hsv_colour = [0.0, 0.0, 1.0]
        self.selected_rgb_colour = self.game.core.HSVtoRGB(*self.selected_hsv_colour)
        
        self.create_image_as_pallete(self.width, self.height)
        self.gui_init()
        self.cursor = GUI_designer_colour_colour_picker_cursor(self.game, self)
        
        self.draw_strategy = "primitive_square"
        self.primitive_square_width = self.width + 2
        self.primitive_square_height = self.height + 2
        self.primitive_square_x = self.x - 1
        self.primitive_square_y = self.y - 1
        self.primitive_square_colour = (0.0,0.0,0.0,1.0)


    def change_selected_colour(self, col):
        self.selected_hsv_colour = col
        self.selected_rgb_colour = self.game.core.HSVtoRGB(*self.selected_hsv_colour)

        
    def mouse_left_down(self):
        self.selected_hsv_colour[0] = ((self.game.gui.mouse.x - self.x) / self.width) * 1.0
        self.selected_hsv_colour[1] = ((self.game.gui.mouse.y - self.y) / self.height) * 1.0
        self.selected_rgb_colour = self.game.core.HSVtoRGB(*self.selected_hsv_colour)

        
    def Execute(self):
        self.update()
        self.cursor.x = self.x + (self.width * self.selected_hsv_colour[0])
        self.cursor.y = self.y + (self.height * self.selected_hsv_colour[1])


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.destroy_puzzle_image()
        self.cursor.Kill()
        
    

class GUI_designer_colour_colour_picker_cursor(Process):

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x
        self.y = self.parent.y
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_palette_cursor']
        self.clip = (self.parent.x, self.parent.y, self.parent.width, self.parent.height)



class GUI_designer_colour_current_colour(GUI_element):

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.width = 64
        self.height = 45
        self.x = self.game.settings['screen_width'] - 240
        self.y = 15
        #self.x = self.parent.value_slider_object.x + self.parent.value_slider_object.width + 16
        #self.y = self.parent.value_slider_object.y + (self.parent.value_slider_object.height / 2) - (self.height / 2)
        self.z = Z_GUI_OBJECT_LEVEL_7        
        
        self.gui_init()

        self.draw_strategy = "designer_colour_current_colour"


    def Execute(self):
        self.update()
        self.colour = (
            (float(self.parent.palette_object.selected_rgb_colour[0]) / 255) * 1.0,
            (float(self.parent.palette_object.selected_rgb_colour[1]) / 255) * 1.0,
            (float(self.parent.palette_object.selected_rgb_colour[2]) / 255) * 1.0,
            )
        


class GUI_designer_colour_value_slider(GUI_element):

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.palette_object.x + self.parent.palette_object.width + 8
        self.y = self.parent.palette_object.y
        self.z = Z_GUI_OBJECT_LEVEL_7        
        self.width = 16
        self.height = 118
        self.gui_init()

        self.draw_strategy = "designer_colour_value_slider"
        self.primitive_square_colour = (
            (0.0,0.0,0.0,1.0),
            (0.0,0.0,0.0,1.0),
            (1.0,1.0,1.0,1.0),
            (1.0,1.0,1.0,1.0),
            )

        self.slider_cursor = GUI_designer_colour_value_slider_cursor(self.game, self)


    def Execute(self):
        self.update()
        hsv_sans_v = self.game.core.HSVtoRGB(self.parent.palette_object.selected_hsv_colour[0], self.parent.palette_object.selected_hsv_colour[1], 1.0)
        self.colour = (
            (float(hsv_sans_v[0]) / 255) * 1.0,
            (float(hsv_sans_v[1]) / 255) * 1.0,
            (float(hsv_sans_v[2]) / 255) * 1.0,
            )
        self.slider_cursor.y = self.y + (self.height * self.parent.palette_object.selected_hsv_colour[2])


    def mouse_left_down(self):
        self.parent.palette_object.selected_hsv_colour[2] = ((self.game.gui.mouse.y - self.y) / self.height) * 1.0
        self.parent.palette_object.selected_rgb_colour = self.game.core.HSVtoRGB(*self.parent.palette_object.selected_hsv_colour)


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.slider_cursor.Kill()



class GUI_designer_colour_value_slider_cursor(Process):

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x
        self.y = self.parent.y
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_value_slider']
        self.clip = (self.parent.x, self.parent.y, self.parent.width, self.parent.height)


    def get_screen_draw_position(self):
        return (self.x, self.y - (self.image.height / 2))



class GUI_designer_colour_undo_button(GUI_element_button):
    generic_button = False
    width = 68
    height = 68
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_undo']
        self.x = self.game.settings['screen_width'] - 770
        self.y = 65
        self.width = 68
        self.height = 68
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def Execute(self):
        self.disabled = not self.parent.can_undo()
        self.update()


    def mouse_left_up(self):
        self.parent.undo()



class GUI_designer_colour_redo_button(GUI_element_button):
    generic_button = False
    width = 68
    height = 68
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_redo']
        self.x = self.game.settings['screen_width'] - 690
        self.y = 65
        self.width = 68
        self.height = 68
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def Execute(self):
        self.disabled = not self.parent.can_redo()
        self.update()


    def mouse_left_up(self):
        self.parent.redo()



class GUI_designer_colour_flood_fill_button(GUI_element_button):
    generic_button = False
    toggle_button = True
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_designer_fill']
        self.x = self.game.settings['screen_width'] - 860
        self.y = 65
        self.width = 68
        self.height = 68
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.gui_init()


    def mouse_left_up(self):
        self.mouse_left_up_toggle()
        if self.toggle_state:
            self.parent.tool = DRAWING_TOOL_STATE_FILL
            self.parent.tool_message_display = True
        else:
            self.parent.tool = DRAWING_TOOL_STATE_DRAW
            self.parent.tool_message_display = False
