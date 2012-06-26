"""
PixelPics - Nonograme game
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


class GUI_main_menu_container(GUI_element):
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
        GUI_main_menu_title(self.game, self, self.game.no_button_anim)
        self.game.no_button_anim = True
        
        self.objs = []
        for x in range(10):
            self.objs.append(
                Main_menu_background(self.game)
                )

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
              (.9,1.0,1.0,1.0),
              (.9,1.0,1.0,1.0),
              (1.0,1.0,1.0,1.0)                
            )


    def Execute(self):
        self.update()


    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.objs:
            x.Kill()



class GUI_main_menu_title(GUI_element):

    title_message = None
    title_state = 0
    
    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.x = 0.0
        self.y = 100.0
        self.title_state = 0
        self.wait = 0
        self.no_button_anim = no_button_anim
        
        self.title_message = Pixel_message(self.game, self.x, self.y, z = Z_GUI_OBJECT_LEVEL_3)
        
        if self.no_button_anim:
            self.title_message.finish()
            self.wait = 220


    def Execute(self):
        self.update()

        if self.title_state == 0:

            if self.game.core.Keyboard_key_released(key.ESCAPE):
                self.title_message.finish()
                self.wait = 220
                self.no_button_anim = True
                
            self.wait += 1
            if self.wait >= 220:
                GUI_main_menu_play_button(self.game, self, self.no_button_anim)
                GUI_main_menu_options_button(self.game, self, self.no_button_anim)
                GUI_main_menu_puzzle_designer_button(self.game, self, self.no_button_anim)
                GUI_main_menu_quit_button(self.game, self, self.no_button_anim)
                GUI_main_menu_credits_button(self.game, self)
                self.title_state = 1
                self.wait = 0

        if self.title_state == 1:
            self.wait += 1
            if self.wait >= 30:
                if self.game.player.first_run:
                    self.conf_box = GUI_element_confirmation_box(
                        self.game,
                        self,
                        "Play Tutorial?",
                        ["This is your first time playing PixelPics.", "Would you like to learn how to play?"],
                        confirm_callback = self.first_time
                        )
                    self.game.player.first_run = False
                    self.game.save_player(self.game.player)
                self.title_state = 2

        

    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.title_message.Kill()


    def first_time(self):
        pass
    


class GUI_main_menu_button(GUI_element_button):
    generic_button = True
    width = 150

    def main_menu_button_init(self, y_shift_to = 0, y_shift = 0, iter_wait = 0):
        self.x = self.game.settings['screen_width'] / 2
        self.y_to = self.game.settings['screen_height'] / 2 + y_shift_to
        self.y = self.game.settings['screen_height'] + y_shift
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()
        self.x -= (self.width / 2)
        self.generic_button_text_object.x -= (self.width / 2)
        self.main_menu_button_state = 0
        self.iter = 0
        self.iter_wait = iter_wait

        
    def Execute(self):
        self.update()
        if self.main_menu_button_state == 0:
            self.iter += 1
            self.y = lerp(self.iter, self.iter_wait, self.y, self.y_to)
            self.generic_button_text_object.y = self.y + 4
            if self.iter > self.iter_wait:
                self.main_menu_button_state = 1

        

class GUI_main_menu_play_button(GUI_main_menu_button):
    generic_button_text = "Play!"

    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.main_menu_button_init(y_shift_to = -80, iter_wait = 50)

        if no_button_anim:
            self.y = self.y_to
            self.generic_button_text_object.y = self.y + 4
            self.main_menu_button_state = 1


    def mouse_left_up(self):
        #self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE), speed = 120)
        GUI_main_menu_puzzle_type_selection(self.game, self.parent)



class GUI_main_menu_puzzle_designer_button(GUI_main_menu_button):
    generic_button_text = "Puzzle Designer"

    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.main_menu_button_init(y_shift_to = -40, y_shift = 40, iter_wait = 100)

        if no_button_anim:
            self.y = self.y_to
            self.generic_button_text_object.y = self.y + 4
            self.main_menu_button_state = 1


    def mouse_left_up(self):
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_DESIGNER), speed = 20)



class GUI_main_menu_options_button(GUI_main_menu_button):
    generic_button_text = "Options"

    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.main_menu_button_init(y_shift = 80, iter_wait = 150)

        if no_button_anim:
            self.y = self.y_to
            self.generic_button_text_object.y = self.y + 4
            self.main_menu_button_state = 1


    def mouse_left_up(self):
        pass



class GUI_main_menu_quit_button(GUI_main_menu_button):
    generic_button_text = "Quit"

    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.main_menu_button_init(y_shift_to = 40, y_shift = 120, iter_wait = 200)

        if no_button_anim:
            self.y = self.y_to
            self.generic_button_text_object.y = self.y + 4
            self.main_menu_button_state = 1


    def mouse_left_up(self):
        self.conf_box = GUI_element_confirmation_box(
            self.game,
            self,
            "Really Quit?",
            ["Are you sure you want to quit?"],
            confirm_callback = self.confirm
            )


    def confirm(self):
        self.game.quit_game()



class Main_menu_background(Process):
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_main_menu_background']
        self.y = int(random.randrange(0 - self.image.height, self.game.settings['screen_height']) / 64) * 64
        self.reposition()
        self.z = Z_GUI_OBJECT_LEVEL_1
        self.alpha = .2
        rotation = (0, 90, 180, 270)
        self.rotation = random.choice(rotation)


    def Execute(self):
        self.y += .3
        if self.y > self.game.settings['screen_height'] + (self.image.height/2):
            self.y = -(self.image.height / 2)
            self.reposition()
            
    
    def reposition(self):
        self.x = int(random.randrange(0, self.game.settings['screen_width']) / 64) * 64



class GUI_main_menu_credits_button(GUI_element_button):
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.game.settings['screen_width'] - 128.0
        self.y = self.game.settings['screen_height'] - 100.0
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.image = self.game.core.media.gfx['gui_stompyblondie_logo_mini']
        self.gui_init()
        self.alpha = 0.0

        self.text = Text(self.game.core.media.fonts['basic'], self.x + 55.0, self.y + 75.0, TEXT_ALIGN_TOP_LEFT, "Credits")
        self.text.z = self.z - 1
        self.text.alpha = 0.0
        self.text.colour = (0.0, 0.0, 0.0)


    def Execute(self):
        if self.alpha < 1.0:
            self.alpha += .05
        self.update()

    
    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        GUI_main_menu_credits(self.game, self)
        

    def mouse_over(self):
        GUI_element_button.mouse_over(self)
        self.text.alpha = 1.0


    def mouse_out(self):
        GUI_element_button.mouse_out(self)
        self.text.alpha = 0.0


    def get_screen_draw_position(self):
        return (self.x, self.y)


    def On_Exit(self):
        GUI_element_button.On_Exit(self)
        self.text.Kill()



class GUI_main_menu_credits(GUI_element_window):
    title = "Credits"
    height = 420
    width = 450
    objs = {}
    text_to_write = [
        "PixelPics",
        "",
        "Dedicated to Felix",
        "",
        "",
        " -- Programming -- ",
        "Fiona Burrows",
        "",
        " -- Additional Programming -- ",
        "Mark Frimston",
        "",
        " -- Visuals -- ",
        "Fiona Burrows",
        "",
        " -- Audio -- ",
        "Fiona Burrows",
        "",
        " -- Level Design -- ",
        "Fiona Burrows",
        "Mark Frimston",
        "",
        "Stompy Blondie Games, 2011-2012",
        ]

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
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
        for text in self.text_to_write:
            txt = Text(self.game.core.media.fonts['basic'], self.x + (self.width/2), self.y + 30 + y, TEXT_ALIGN_CENTER, text)
            txt.z = self.z - 2
            txt.colour = (0.0, 0.0, 0.0)
            self.objs['text_' + str(y)] = txt
            y += 15

        GUI_main_menu_credits_close_button(self.game, self)

        self.game.gui.block_gui_keyboard_input = True
        self.x = 0
        self.y = 0
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']


    def On_Exit(self):
        GUI_element_window.On_Exit(self)
        self.game.gui.block_gui_keyboard_input = False
        for x in self.objs:
            self.objs[x].Kill()



class GUI_main_menu_credits_close_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Close"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.gui_init()
        self.x = self.parent.x + self.parent.width - 100
        self.y = self.parent.y + self.parent.height - 50
        self.generic_button_text_object.x = self.x + 9
        self.generic_button_text_object.y = self.y + 4


    def mouse_left_up(self):
        self.parent.Kill()


        
class GUI_main_menu_puzzle_type_selection(GUI_element):
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.gui_init()

        GUI_main_menu_puzzle_type_select_main(self.game, self)
        GUI_main_menu_puzzle_type_select_downloaded(self.game, self)
        GUI_main_menu_puzzle_type_select_go_back(self.game, self)
        
        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_colour = (0.0, 0.0, 0.0, .4)



class GUI_main_menu_puzzle_type_select_main(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_puzzle_type_select_main']
        self.gui_init()
        self.x = -self.image.width
        self.y = (self.game.settings['screen_height'] / 2) - (self.image.height / 2)
        self.x_to = (self.game.settings['screen_width'] / 2) - self.image.width

        self.button_state = 0
        self.iter = 0
        self.iter_wait = 20

        
    def Execute(self):
        self.update()
        if self.button_state == 0:
            self.iter += 1
            self.x = lerp(self.iter, self.iter_wait, self.x, self.x_to)
            if self.iter > self.iter_wait:
                self.button_state = 1


    def mouse_left_up(self):
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_CATEGORY_SELECT), speed = 60)



class GUI_main_menu_puzzle_type_select_downloaded(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_puzzle_type_select_downloaded']
        self.gui_init()
        self.x = self.game.settings['screen_width']
        self.y = (self.game.settings['screen_height'] / 2) - (self.image.height / 2)
        self.x_to = (self.game.settings['screen_width'] / 2)

        self.button_state = 0
        self.iter = 0
        self.iter_wait = 20

        
    def Execute(self):
        self.update()
        if self.button_state == 0:
            self.iter += 1
            self.x = lerp(self.iter, self.iter_wait, self.x, self.x_to)
            if self.iter > self.iter_wait:
                self.button_state = 1


    def mouse_left_up(self):
        self.parent.Kill()



class GUI_main_menu_puzzle_type_select_go_back(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_go_back']
        self.gui_init()
        self.x = (self.game.settings['screen_width'] / 2) - 256
        self.y = (self.game.settings['screen_height'] / 2) + 40


    def mouse_left_up(self):
        self.parent.Kill()
