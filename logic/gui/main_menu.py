"""
PixelPics - Nonograme game
Copyright (c) 2014 Stompy Blondie Games http://stompyblondie.com
"""

# python imports
import random

# Game engine imports
from core import *

# Game imports
from consts import *
from helpers  import *
from gui.gui_elements import *
from gui.options import *
from gui.mascot import Mascot_Main_Menu


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
        self.title = GUI_main_menu_title(self.game, self, self.game.no_button_anim)
        self.game.no_button_anim = True
        
        self.objs = []
        for x in range(10):
            self.objs.append(
                Main_menu_background(self.game)
                )

        if not DEMO:
            if self.game.manager.all_main_packs_starred:
                for x in range(20):
                    self.objs.append(
                        Reward_star(self.game, x)
                        )

        self.firework_counter_to = random.randint(20, 60)
        self.firework_counter = 0

        if self.game.special_finish_state == SPECIAL_FINISH_STARRED:
            self.msg_count = 60

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
              (1.0,1.0,1.0,1.0),
              (.84,.89,0.94,1.0),
              (.84,.89,0.94,1.0),
            )


    def Execute(self):
        self.update()
        if DEMO:
            return
        if self.game.manager.cleared_all_main_categories:
            if self.firework_counter == self.firework_counter_to:
                self.firework_counter_to = random.randint(10, 20)
                self.firework_counter = 0
                self.objs.append(
                    Firework(self.game)
                    )
            self.firework_counter += 1
        if self.game.special_finish_state == SPECIAL_FINISH_STARRED:
            self.msg_count -= 1
            if self.msg_count == 0:
                self.game.special_finish_state = None
                GUI_element_dialog_box(
                    self.game,
                    self,
                    "Oh?",
                    ["'Cat Mode' is now available."]
                    )


    def quit_game(self):
        self.title.quit_game()
        

    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.objs:
            x.Kill()



class GUI_main_menu_title(GUI_element):

    title_state = 0
    
    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.x = self.game.settings['screen_width'] / 2
        self.y = (self.game.settings['screen_height'] / 2) - 180
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.image = self.game.core.media.gfx['gui_title_bg']
        self.title_state = 0
        self.wait = 0
        self.no_button_anim = no_button_anim
        self.height = 300       
        self.mascot = None
        
        self.letters = []
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "p", -183, -45, 20))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "i", -103, -50, 30))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "x", 0, -40, 110))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "e", 108, -42, 40))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "l", 188, -48, 50))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "p", -138, 84, 60))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "i", -50, 79, 70))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "c", 37, 90, 80))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "s", 138, 91, 90))

        if self.no_button_anim:
            self.finish()
            self.wait = 220

        self.draw_strategy = "main_menu_title"
        self.draw_strategy_screen_width = self.game.settings['screen_width']


    def Execute(self):
        self.update()

        if self.title_state == 0:

            if self.game.core.Keyboard_key_released(key.ESCAPE):
                self.finish()
                self.wait = 100
                self.no_button_anim = True
                
            self.wait += 1
            if self.wait >= 100:
                GUI_main_menu_play_button(self.game, self, self.no_button_anim)
                GUI_main_menu_sharing_button(self.game, self, self.no_button_anim)
                GUI_main_menu_puzzle_designer_button(self.game, self, self.no_button_anim)
                GUI_main_menu_options_button(self.game, self, self.no_button_anim)
                self.quit_button = GUI_main_menu_quit_button(self.game, self, self.no_button_anim)
                GUI_main_menu_credits_button(self.game, self)
                self.mascot = Mascot_Main_Menu(self.game)
                self.title_state = 1
                self.wait = 0
                if DEMO:
                    GUI_main_menu_buy_full_button(self.game, self)
                    
        if self.title_state == 1:
            self.wait += 1
            if self.wait >= 30:
                self.title_state = 2


    def quit_game(self):
        if self.title_state == 2:
            self.quit_button.mouse_left_up()
        

    def finish(self):
        for x in self.letters:
            x.finish()
        

    def get_screen_draw_position(self):
        return (self.x - (self.image.width / 2), self.y - (self.image.height / 2))


    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.letters:
            x.Kill()
        if not self.mascot is None:
            self.mascot.Kill()



class GUI_main_menu_title_letter(Process):

    def __init__(self, game, parent, image, x, y, bubble_wait):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_title_' + str(image)]
        self.z = Z_GUI_OBJECT_LEVEL_5 - 40
        self.x = self.parent.x + x
        self.y = self.parent.y + y
        self.initial_y = self.y
        self.bubble_wait = bubble_wait
        self.is_x = False
        self.is_s = False
        if image == 'x':
            self.is_x = True
        if image == 's':
            self.is_s = True
        self.scale = 0.0
        self.wait = 0
        self.state = 0
        self.iter = 0


    def Execute(self):   
        if self.state == 0:
            self.wait += 1
            if self.wait == self.bubble_wait:
                self.state = 1
                self.wait = 0
                if self.is_x:
                    self.scale = 1.0                
        elif self.state == 1:
            if self.is_x:
                self.wait += 1
                if self.wait == 2:
                    self.image_sequence += 1
                    self.wait = 0
                if self.image_sequence == 6:
                    self.state = 3
            else:
                self.scale = lerp(self.iter, 10, 0, 1.2)
                self.iter += 1
                if self.scale >= 1.1:
                    self.state = 2
                    self.iter = 0
        elif self.state == 2:
            if self.iter >= 5:
                if self.is_s:
                    for x in self.parent.letters:
                        if not x.is_x:
                            x.finish()
            else:
                self.scale = lerp(self.iter, 5, 1.2, 1.0)
                self.iter += 1                
        elif self.state == 3:
            if not self.is_x:
                self.wait += 1
                if self.wait == self.bubble_wait:
                    self.wait = 0
                    self.iter = 0
                    self.state = 4            
        elif self.state == 4:
            self.y = lerp(self.iter, 5, self.initial_y, self.initial_y - 5)
            if self.iter >= 5:
                self.state = 5
                self.iter = 0
            self.iter += 1
        elif self.state == 5:
            if self.iter >= 5:
                if self.is_s:
                    for x in self.parent.letters:
                        x.state = 3
                        x.iter = 0
                        x.wait = 0
            else:
                self.y = lerp(self.iter, 5, self.initial_y - 5, self.initial_y)
            self.iter += 1
                

    def finish(self):
        if self.state < 3:
            self.scale = 1.0
            if self.is_x:
                self.image_sequence = 6
            self.state = 3
            self.wait = 0
            self.iter = 0
            self.bubble_wait += 60
            

    def get_screen_draw_position(self):
        return (
            self.x - ((self.image.width * self.scale) / 2),
            self.y - ((self.image.height * self.scale) / 2)
            )

                


class GUI_main_menu_button(GUI_element_button):
    generic_button = False

    def main_menu_button_init(self, y_shift_to = 0, y_shift = 0, iter_wait = 0):
        self.x = self.game.settings['screen_width'] / 2
        self.y_to = self.game.settings['screen_height'] / 2 + y_shift_to
        self.y = self.game.settings['screen_height'] + y_shift
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()
        self.x -= (self.image.width / 2)
        self.main_menu_button_state = 0
        self.iter = 0
        self.iter_wait = iter_wait
        self.full_game_only = None
        if self.disabled:
            self.full_game_only = Full_Game_Only_Notice(self.game, self)

    def Execute(self):
        self.update()
        if self.main_menu_button_state == 0:
            self.iter += 1
            self.y = lerp(self.iter, self.iter_wait, self.y, self.y_to)
            if self.iter > self.iter_wait:
                self.main_menu_button_state = 1

    def On_Exit(self):
        if not self.full_game_only is None:
            self.full_game_only.Kill()

        

class GUI_main_menu_play_button(GUI_main_menu_button):
    
    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_main_menu_play']
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.main_menu_button_init(y_shift_to = 40, iter_wait = 50)
        if no_button_anim:
            self.y = self.y_to
            self.main_menu_button_state = 1

    def mouse_left_up(self):
        GUI_main_menu_button.mouse_left_up(self)
        no_download_items = True
        for pack in self.game.manager.packs:
            if pack.author_id == self.game.author_id:
                continue
            no_download_items = False
            break
        if no_download_items:
            self.game.manager.user_created_puzzles = False
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_CATEGORY_SELECT), speed = 30, stop_music = True)
        else:
            GUI_main_menu_puzzle_type_selection(self.game, self.parent)



class GUI_main_menu_puzzle_designer_button(GUI_main_menu_button):

    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_main_menu_designer']
        self.z = Z_GUI_OBJECT_LEVEL_2        
        self.disabled = DEMO
        self.main_menu_button_init(y_shift_to = 150, y_shift = 100, iter_wait = 150)
        if no_button_anim:
            self.y = self.y_to
            self.main_menu_button_state = 1

    def mouse_left_up(self):
        if self.disabled:
            return
        GUI_main_menu_button.mouse_left_up(self)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_DESIGNER), speed = 20, stop_music = True)



class GUI_main_menu_sharing_button(GUI_main_menu_button):

    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_main_menu_extras']
        self.z = Z_GUI_OBJECT_LEVEL_2        
        self.disabled = DEMO
        self.main_menu_button_init(y_shift_to = 95, y_shift = 50, iter_wait = 100)
        if no_button_anim:
            self.y = self.y_to
            self.main_menu_button_state = 1

    def mouse_left_up(self):
        if self.disabled:
            return
        GUI_main_menu_button.mouse_left_up(self)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_SHARING), speed = 20)


            
class Full_Game_Only_Notice(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['full_game_stamp']
        self.z = self.parent.z - 1
        self.scale = .5
        self.alpha = 0.0
        
    def Execute(self):
        self.x = self.parent.x + 350
        self.y = self.parent.y + 80
        if self.parent.main_menu_button_state == 1 and self.alpha < 1.0:
            self.alpha += 0.1
            

class GUI_main_menu_options_button(GUI_main_menu_button):

    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_main_menu_options']
        self.z = Z_GUI_OBJECT_LEVEL_2        
        self.main_menu_button_init(y_shift_to = 205, y_shift = 150, iter_wait = 200)

        if no_button_anim:
            self.y = self.y_to
            self.main_menu_button_state = 1


    def mouse_left_up(self):
        GUI_main_menu_button.mouse_left_up(self)
        GUI_options(self.game, self.parent)



class GUI_main_menu_quit_button(GUI_main_menu_button):

    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_main_menu_quit']
        self.z = Z_GUI_OBJECT_LEVEL_2        
        self.main_menu_button_init(y_shift_to = 260, y_shift = 200, iter_wait = 250)

        if no_button_anim:
            self.y = self.y_to
            self.main_menu_button_state = 1


    def mouse_left_up(self):
        GUI_main_menu_button.mouse_left_up(self)
        self.conf_box = GUI_element_confirmation_box(
            self.game,
            self,
            "Really Quit?",
            ["Are you sure you want to quit?"],
            confirm_callback = self.confirm
            )


    def confirm(self):
        self.game.quit_game()


class GUI_main_menu_buy_full_button(GUI_main_menu_button):

    def __init__(self, game, parent = None, no_button_anim = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['title_button_buy_full']
        self.z = Z_GUI_OBJECT_LEVEL_2        
        self.main_menu_button_init(y_shift_to = 230, y_shift = 150, iter_wait = 200)
        self.x += 300
        if no_button_anim:
            self.y = self.y_to
            self.main_menu_button_state = 1


    def mouse_left_up(self):
        GUI_main_menu_button.mouse_left_up(self)
        import webbrowser
        webbrowser.open("http://pixelpicsgame.com", new = 2)


class Main_menu_background(Process):
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_main_menu_background']
        self.y = int(random.randrange(0 - self.image.height, self.game.settings['screen_height']) / 64) * 64
        self.reposition()
        self.z = Z_GUI_OBJECT_LEVEL_0
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
    frame_switch_times = [
        (1, 10),
        (2, 10),
        (3, 5),
        (1, 15),
        (2, 10),
        (3, 5),
        (1, 15),
        (2, 10),
        (3, 5),
        (1, 10)
        ]

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.game.settings['screen_width'] - 128.0
        self.y = self.game.settings['screen_height'] - 130.0
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.image = self.game.core.media.gfx['gui_stompyblondie_logo_mini']
        self.gui_init()
        self.alpha = 0.0
        self.iter = 0
        self.frame = 0
        self.animate = False
        self.text = Text(self.game.core.media.fonts['basic'], self.x - 20, self.y + 50, TEXT_ALIGN_TOP_LEFT, "Credits")
        self.text.z = self.z - 1
        self.text.alpha = 0.0
        self.text.colour = (0.0, 0.0, 0.0)


    def Execute(self):
        if self.alpha < 1.0:
            self.alpha += .05
        #self.update()
        if self.animate:
            if self.frame == len(self.frame_switch_times) - 1:
                self.frame = 0
            self.iter += 1
            if self.iter >= self.frame_switch_times[self.frame][1]:
                self.frame += 1
                self.image_sequence = self.frame_switch_times[self.frame][0]
                self.iter = 0
            
        else:
            self.image_sequence = 1

    
    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        GUI_main_menu_credits(self.game, self)
        

    def mouse_over(self):
        #GUI_element_button.mouse_over(self)
        self.animate = True
        self.text.alpha = 1.0


    def mouse_out(self):
        #GUI_element_button.mouse_out(self)
        self.animate = False
        self.text.alpha = 0.0


    def get_screen_draw_position(self):
        return (self.x, self.y)


    def On_Exit(self):
        GUI_element_button.On_Exit(self)
        self.text.Kill()



class GUI_main_menu_credits(GUI_element_window):
    title = "Credits"
    height = 660
    width = 520
    objs = {}
    text_to_write = [
        "PixelPics",
        "Dedicated to Felix",
        "",
        " -- Programming -- ",
        "Fiona Burrows",
        "",
        " -- Additional Programming -- ",
        "Mark Frimston",
        "",
        " -- Visuals -- ",
        "Fiona Burrows & Mark Frimston",
        "",
        " -- SFX -- ",
        "Fiona Burrows",
        "",
        " -- Music -- ",
        "Back On Track, Comparsa, Samba Stings, No Frills Salsa,",
        "Beachfront Celebration, No Frills Cumbia,",
        "Hackbeat, Modern Jazz Samba, Tango De Manzana",
        "by Kevin MacLeod (incompetech.com)",
        "",
        "Brazil Samba by http://bensound.com",
        "",
        " -- Level Design -- ",
        "Fiona Burrows & Mark Frimston",
        "",
        "Copyright (c) 2014 Stompy Blondie Games",
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
        y = 30
        for text in self.text_to_write:
            txt = Text(self.game.core.media.fonts['window_text'], self.x + (self.width/2), self.y + 30 + y, TEXT_ALIGN_CENTER, text)
            txt.z = self.z - 2
            txt.colour = (0.3,0.3,0.3)
            self.objs['text_' + str(y)] = txt
            y += 20

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
        self.z = Z_GUI_OBJECT_LEVEL_9
        self.x = self.parent.x + self.parent.width - 100
        self.y = self.parent.y + self.parent.height - 50
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.Kill()


        
class GUI_main_menu_puzzle_type_selection(GUI_element):
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.game.gui.block_gui_keyboard_input = True

        self.gui_init()

        GUI_main_menu_puzzle_type_select_main(self.game, self)
        GUI_main_menu_puzzle_type_select_downloaded(self.game, self)
        self.back_button = GUI_main_menu_puzzle_type_select_go_back(self.game, self)
        
        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_colour = (0.0, 0.0, 0.0, .4)


    def Execute(self):
        self.update()
        if self.game.core.Keyboard_key_released(key.ESCAPE):
            self.back_button.mouse_left_up()
        

    def On_Exit(self):
        GUI_element.On_Exit(self)        
        self.game.gui.block_gui_keyboard_input = False
        


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
        self.x_to = (self.game.settings['screen_width'] / 2) - self.image.width + 6.0

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
        GUI_element_button.mouse_left_up(self)
        self.game.manager.user_created_puzzles = False
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_CATEGORY_SELECT), speed = 30, stop_music = True)



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
        GUI_element_button.mouse_left_up(self)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_SHARING, gui_state = GUI_STATE_SHARING_DOWNLOADED), speed = 30, stop_music = True)



class GUI_main_menu_puzzle_type_select_go_back(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_go_back']
        self.gui_init()
        self.x = 0.0
        self.y = self.game.settings['screen_height'] - 128


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.Kill()



class Reward_star(Process):
    def __init__(self, game, z):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_reward_star']
        self.y = random.randrange(-self.image.height, self.game.settings['screen_height'])
        self.reposition()
        self.z = Z_GUI_OBJECT_LEVEL_2 + 1 + z


    def Execute(self):
        self.rotation -= self.rot
        self.y += 1.0
        self.x -= self.x_shift
        if self.y > self.game.settings['screen_height'] + self.image.height or self.x < -self.image.width or self.x > self.game.settings['screen_width'] + self.image.width:
            self.y = -self.image.height
            self.reposition()
            
    
    def reposition(self):
        self.x = int(random.randrange(0, self.game.settings['screen_width']) / 64) * 64
        self.rotation = random.randrange(360)
        self.rot = random.randrange(-2, 2)
        if self.rot == 0:
            self.rot = 1
        self.x_shift = random.randrange(-10, 10) * .1



class Firework(Process):
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image = self.game.core.media.gfx['gui_title_firework']
        self.x = random.randrange(self.image.width, self.game.settings['screen_width'])
        self.y = random.randrange(-self.image.height, self.game.settings['screen_height'])
        self.y_origin = self.y
        self.z = Z_GUI_OBJECT_LEVEL_7-1
        self.alpha = 1.0
        self.scale = .5
        self.image_sequence = random.randint(1, 4)
        self.target_scale = .7 + (random.random() * .3)
        colours = [
            (1.0, 1.0, 1.0),
            (1.0, 0.3, 0.3),
            (0.3, 1.0, 0.3),
            (0.3, 0.3, 1.0),
            (1.0, 1.0, 0.3),
            (0.3, 1.0, 1.0),
            (1.0, 0.3, 1.0),
            ]
        self.colour = random.choice(colours)
        self.state = 0
        self.iter = 0
        self.iter_wait = 20
        self.y_to_move = 0.0
        rand_sound = random.randint(1, 6)
        if rand_sound < 4:
            self.game.core.media.sfx['firework' + str(rand_sound)].play(0)


    def Execute(self):
        if self.y_to_move < 2.0:
            self.y_to_move += .02
        self.y += self.y_to_move
        
        if self.state == 0:
            self.iter += 1
            self.scale = inverse_sequare_lerp(self.iter, self.iter_wait, 0.5, self.target_scale)
            if self.iter > self.iter_wait:
                self.iter_wait = 50
                self.iter = 0
                self.state = 1
        elif self.state == 1:
            self.iter += 1
            self.alpha = lerp(self.iter, self.iter_wait, 1.0, 0.0, smooth = False)
            if self.iter > self.iter_wait:
                self.Kill()
                
    def get_screen_draw_position(self):
        return self.x - ((self.image.width * self.scale) / 2), self.y - ((self.image.height * self.scale) / 2)
