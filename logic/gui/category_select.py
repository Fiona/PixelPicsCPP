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
        self.scroll_up = False
        self.scroll_down = False
        
        self.title = Text(self.game.core.media.fonts['menu_titles'], 20, 10, TEXT_ALIGN_TOP_LEFT, "Category Select")
        self.title.z = Z_GUI_OBJECT_LEVEL_2
        self.title.colour = (0.95, 0.58, 0.09)
        self.title.shadow = 2
        self.title.shadow_colour = (0.7, 0.7, 0.7)

        GUI_category_go_back(self.game, self)
        self.mascot_object = Mascot_Category_Select(self.game)

        GUI_category_select_up_button(self.game, self)
        GUI_category_select_down_button(self.game, self)
        
        if not self.game.category_to_unlock == None:
            self.mascot_object.set_speech(["Wow, you unlocked", "a new category!"])
            self.game.gui.block_gui_keyboard_input = True
            self.game.gui.block_gui_mouse_input = True
            self.game.gui.mouse.alpha = 0.0

        categories = [
            ("Tutorial",         "0001", (.5, 1.0, .5)),
            ("Effortless",       "0002", (1.0, .5, .5)),
            ("Light",            "0003", (.5, .5, 1.0)),
            ("Piece Of Cake",    "0004", (.5, 1.0, 1.0)),
            ("Uncomplicated",    "0005", (1.0, .5, 1.0)),
            ("Manageable",       "0006", (1.0, 1.0, .5)),
            ("Troublesome",      "0007", (1.0, 1.0, .5)),
            ("Formidable",       "0008", (1.0, 1.0, .5)),
            ("Demanding",        "0009", (1.0, 1.0, .5)),
            ("Heavy",            "0010", (1.0, 1.0, .5)),
            ("Final Challenge",  "last", (1.0, 1.0, .5))
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

        # Draw strategy data
        self.text_offset_x = 0.0
        self.text_offset_y = 0.0
        self.draw_strategy = "balloons_background"


    def Execute(self):
        self.update()

        if not self.game.gui.block_gui_mouse_input:
            if self.game.gui.mouse.x > ((self.game.settings['screen_width'] / 2) - 100) and self.game.gui.mouse.y < 50:
                    self.scroll_up = True
            if self.game.gui.mouse.x > ((self.game.settings['screen_width'] / 2) - 100) and self.game.gui.mouse.y > (self.game.settings['screen_height'] - 50):
                    self.scroll_down = True

            if self.game.gui.mouse.x > ((self.game.settings['screen_width'] / 2) - 100) and self.game.core.mouse.wheel_up:
                self.scroll_speed -= 4.0
            if self.game.gui.mouse.x > ((self.game.settings['screen_width'] / 2) - 100) and self.game.core.mouse.wheel_down:
                self.scroll_speed += 4.0
                
        if self.scroll_up:
            self.scroll_speed -= .5
        elif self.scroll_down:
            self.scroll_speed += .5 

        if self.first_category.y > 75 and self.scroll_speed < 0:
            self.scroll_speed = 0.0
        if self.last_category.y < self.game.settings['screen_height'] - 128 and self.scroll_speed > 0:
            self.scroll_speed = 0.0
            
        self.scroll_speed *= .95
            
        if self.scroll_speed > 7.0:
            self.scroll_speed = 7.0
        if self.scroll_speed < -7.0:
            self.scroll_speed = -7.0

        self.scroll_up = False
        self.scroll_down = False
            
        for cat in self.category_objs:
            cat.y -= self.scroll_speed
            cat.update_obj_positions()

        self.text_offset_x -= 3.0
        self.text_offset_y += 3.0

        

    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.mascot_object.Kill()
        self.title.Kill()
        


class GUI_category_select_select_category_button(GUI_element_button):
    generic_button = False
    objs = {}
    
    def __init__(self, game, parent = None, num = 0, pack_dir = "", name = "? ? ? ? ?", colour = (1.0, 1.0, 1.0)):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.pack_dir = pack_dir
        self.pack_uuid = self.game.manager.extract_pack_uuid(pack_dir, user_created = False)
        self.z = self.parent.z - 3
        self.image = self.game.core.media.gfx['gui_button_select_category']
        self.gui_init()
        self.x = (self.game.settings['screen_width'] / 2) - 100
        self.y = 75 + (80 * num) + (40 * num)
        self.width = 466
        self.height = 80
        self.normal_colour = colour        

        self.objs = {}

        self.objs['shadow'] = Select_category_button_shadow(self.game, self)
        
        text = Text(self.game.core.media.fonts['category_button_name'], 0, 0, TEXT_ALIGN_TOP_LEFT, name)
        text.z = self.z - 3
        text.colour = (1.0, 1.0, 1.0)
        self.objs['cat_name'] = text

        if self.game.category_to_unlock == self.pack_dir or not self.pack_dir in self.game.player.unlocked_categories:
            self.objs['status_icon'] = GUI_category_locked(self.game)
            self.colour = (1.0, 1.0, 1.0)
            self.disabled = True
        else:
            self.colour = self.normal_colour
            self.create_unlocked_objects()

        self.iter = 0

        self.lock_icon = None
        self.unlock_mask = None
        if self.game.category_to_unlock == self.pack_dir:
            self.anim_state = 0
        else:
            self.anim_state = -1            
            
        self.update_obj_positions()


    def Execute(self):
        GUI_element_button.update(self)

        self.iter += 1
        if self.anim_state == 0:
            if self.y > self.game.settings['screen_height'] - self.image.height:
                self.parent.scroll_speed += .5
            else:
                self.anim_state = 1
        if self.anim_state == 1:
            if self.iter > 60:
                self.iter = 0
                self.anim_state = 2
                self.unlock_mask = GUI_category_select_select_category_button_unlock_overlay(self.game, self)
        elif self.anim_state == 2:
            self.unlock_mask.alpha = lerp(self.iter, 120, 0.0, 1.0)
            #self.objs['status_icon'].alpha = lerp(self.iter, 60, self.objs['status_icon'].alpha, 0.0)
            #self.objs['status_icon'].scale = lerp(self.iter, 60, self.objs['status_icon'].scale, 0.0)
            if self.iter > 120:
                self.iter = 0
                self.objs['status_icon'].image_sequence = 2
                self.anim_state = 3
                self.game.core.media.sfx['unlock'].play(0)
        elif self.anim_state == 3:
            if self.iter > 5:
                self.iter = 0
                self.anim_state = 4
                self.iter = 0
                self.game.category_to_unlock = None
                self.game.gui.block_gui_keyboard_input = False
                self.game.gui.block_gui_mouse_input = False
                self.game.gui.mouse.alpha = 1.0
                self.disabled = False
                self.colour = self.normal_colour
                self.lock_icon = self.objs['status_icon']
                del(self.objs['status_icon'])
                self.create_unlocked_objects()
        elif self.anim_state == 4:
            self.lock_icon.alpha = lerp(self.iter, 120, 1.0, 0.0)
            self.unlock_mask.alpha = lerp(self.iter, 120, 1.0, 0.0)
            if self.iter > 120:
                self.lock_icon.Kill()
                self.unlock_mask.Kill()
                self.lock_icon = None
                self.unlock_mask = None
                self.anim_state = 5
                

    def create_unlocked_objects(self):
        if self.pack_uuid in self.game.player.cleared_categories:
            if self.pack_uuid in self.game.manager.starred_packs:
                self.objs['status_icon'] = GUI_category_completed_star(self.game)
            else:
                self.objs['status_icon'] = GUI_category_completed_tick(self.game)
            
        if self.pack_dir == "0001":
            return
        
        completed = len(self.game.player.cleared_puzzles[self.pack_uuid]) if self.pack_uuid in self.game.player.cleared_puzzles else 0
        text = Text(self.game.core.media.fonts['category_button_completed_count'], 0, 0, TEXT_ALIGN_TOP_RIGHT, str(completed) + "/" + str(len(self.game.manager.game_packs[self.pack_dir].puzzles)))
        text.z = self.z - 1
        text.colour = (1.0, 1.0, 1.0)
        self.objs['completed_count'] = text

        text = Text(self.game.core.media.fonts['category_button_solved_text'], 0, 0, TEXT_ALIGN_TOP_RIGHT, "solved")
        text.z = self.z - 1
        text.colour = (1.0, 1.0, 1.0)
        self.objs['solved'] = text
        

    def update_obj_positions(self):
        self.objs['cat_name'].x = self.x + 60
        self.objs['cat_name'].y = self.y + 15

        if 'completed_count' in self.objs:
            self.objs['completed_count'].x = self.x + 447
            self.objs['completed_count'].y = self.y + 10

        if 'solved' in self.objs:
            self.objs['solved'].x = self.x + 447
            self.objs['solved'].y = self.y + 40

        if 'status_icon' in self.objs:
            self.objs['status_icon'].x = self.x + 10
            self.objs['status_icon'].y = self.y + 60

        if not self.lock_icon is None:
            self.lock_icon.x = self.x + 10
            self.lock_icon.y = self.y + 60

        if not self.unlock_mask is None:
            self.unlock_mask.x = self.x
            self.unlock_mask.y = self.y

        self.objs['shadow'].x = self.x
        self.objs['shadow'].y = self.y


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        self.game.manager.load_pack(self.pack_dir, user_created = False)
        if self.pack_dir == "0001":
            self.game.manager.current_puzzle_file = "0001.puz"
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_TUTORIAL), speed = 40, stop_music = True)
        else:
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE_SELECT), speed = 20)

    
    def On_Exit(self):
        GUI_element_button.On_Exit(self)
        if not self.lock_icon is None:
            self.lock_icon.Kill()
        if not self.unlock_mask is None:
            self.unlock_mask.Kill()
        for x in self.objs:
            self.objs[x].Kill()



class Select_category_button_shadow(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z + 1
        self.x = self.parent.x
        self.y = self.parent.y
        self.image = self.game.core.media.gfx['gui_button_select_category_shadow']


    def get_screen_draw_position(self):
        return (self.x, self.y)

    

class GUI_category_select_select_category_button_unlock_overlay(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.x = self.parent.x
        self.y = self.parent.y
        self.alpha = 0.0
        self.image = self.game.core.media.gfx['gui_button_select_category_unlock_mask']


    def get_screen_draw_position(self):
        return (self.x, self.y)



class GUI_category_completed_tick(Process):
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_category_complete_tick']
        self.z = Z_GUI_OBJECT_LEVEL_3



class GUI_category_completed_star(Process):
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_category_complete_star']
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
        self.x = 8
        self.y = self.game.settings['screen_height'] - self.image.height
        self.width = 128


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 20)



class GUI_category_select_up_button(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_scroll_button_up']
        self.gui_init()
        self.x = (self.game.settings['screen_width'] / 2) + 450 - (self.image.height / 2)
        self.y = 100 - (self.image.width / 2)


    def mouse_left_down(self):
        GUI_element_button.mouse_left_down(self)
        self.parent.scroll_up = True
        
    

class GUI_category_select_down_button(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_scroll_button_down']
        self.gui_init()
        self.x = (self.game.settings['screen_width'] / 2) + 450 - (self.image.height / 2)
        self.y = self.game.settings['screen_height'] - 100 - (self.image.width / 2)


    def mouse_left_down(self):
        GUI_element_button.mouse_left_down(self)
        self.parent.scroll_down = True

