"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
import os, random

# Game engine imports
from core import *

# Game imports
from consts import *
from helpers  import *
from gui.gui_elements import *
from gui.mascot import *


class GUI_puzzle_select_container(GUI_element):
    """
    All elements in puzzle selection screen live inside this thing.
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
        #self.colour = (.8, .8, 1.0)
        self.colour = (1.0, .7, .5)

        GUI_category_go_back(self.game, self)
        self.puzzle_name = Hover_text(self.game, self.game.settings['screen_width'] / 2, 50)
        self.puzzle_best_time = Hover_text(self.game, self.game.settings['screen_width'] / 2, 95)

        self.text_offset_x = 0.0
        self.text_offset_y = 0.0

        i = 0
        for puzzle_filename in self.game.manager.current_pack.order:
            GUI_puzzle_puzzle_item(self.game, self, puzzle_filename, self.game.manager.current_pack.puzzles[puzzle_filename], i)
            i += 1
            
        # Draw strategy data
        self.draw_strategy = "puzzle_select"


    def Execute(self):
        self.update()
        self.puzzle_name.set_text("")
        self.puzzle_best_time.set_text("")
        
        self.text_offset_x += 5.0
        self.text_offset_y -= 5.0


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.puzzle_name.Kill()
        self.puzzle_best_time.Kill()

        

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
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_CATEGORY_SELECT), speed = 20)


    def On_Exit(self):
        self.text.Kill()



class Hover_text(Process):
    def __init__(self, game, x, y):
        Process.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.current_text = ""
        
        self.text = Text(
            self.game.core.media.fonts['puzzle_message'],
            self.x,
            self.y,
            TEXT_ALIGN_CENTER,
            self.current_text,
            )
        self.text.colour = (1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.3, .3, .3, .5)

        self.text.z = self.z - 1

        # Draw strategy data
        self.draw_strategy = ""
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_colour = (0.0, 0.0, 0.0, .3)
        

    def set_text(self, text):
        self.current_text = text
        self.text.text = self.current_text

        if not text == "":
            self.draw_strategy = "primitive_square"
            self.primitive_square_width = self.text.text_width + 40.0
            self.primitive_square_height = self.text.text_height + 4.0
            self.primitive_square_x = self.x - (self.text.text_width/2) - 20.0
            self.primitive_square_y = self.y - (self.text.text_height/2) - 2.0
        else:
            self.draw_strategy = ""
            

    def On_Exit(self):
        self.text.Kill()



class GUI_puzzle_puzzle_item(GUI_element_button):
    def __init__(self, game, parent, puzzle_filename, puzzle_info, puzzle_num):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.puzzle_filename = puzzle_filename
        self.puzzle_info = puzzle_info
        self.puzzle_num = puzzle_num
        self.gui_init()
        self.width = 100
        self.height = 100
        self.alpha = .47
        column = self.puzzle_num % 5
        row = self.puzzle_num / 5
        puzzle_box_size = (1024, 768)
        self.x = float((puzzle_box_size[0] / 5) * column) + self.width - (self.width / 2)
        self.y = 100.0 + float((puzzle_box_size[1] / 5) * row) + self.height - (self.height / 2)

        if self.game.settings['screen_width'] > puzzle_box_size[0]:
            self.x += (self.game.settings['screen_width'] - puzzle_box_size[0]) / 2
        if self.game.settings['screen_height'] > puzzle_box_size[1]:
            self.y += (self.game.settings['screen_height'] - puzzle_box_size[1]) / 2
            
        self.z = Z_GUI_OBJECT_LEVEL_4

        if self.game.manager.current_puzzle_pack in self.game.player.cleared_puzzles and self.puzzle_filename in self.game.player.cleared_puzzles[self.game.manager.current_puzzle_pack]:
            self.cleared = True
        else:
            self.cleared = False

        if self.cleared:
            self.monochrome_picture = GUI_puzzle_puzzle_item_picture(
                self.game,
                self,
                self.x + (self.width / 2),
                self.y + (self.height / 2),
                puzzle_path = os.path.join(self.game.core.path_game_pack_directory, self.game.manager.current_puzzle_pack, self.puzzle_filename),
                in_colour = False,
                fade_in_time = None
                )
            self.coloured_picture = GUI_puzzle_puzzle_item_picture(
                self.game,
                self,
                self.x + (self.width / 2),
                self.y + (self.height / 2),
                puzzle_path = os.path.join(self.game.core.path_game_pack_directory, self.game.manager.current_puzzle_pack, self.puzzle_filename),
                in_colour = True,
                fade_in_time = None
                )
            self.coloured_picture.alpha = 0.0
            self.monochrome_picture.alpha = 1.0
        else:
            self.monochrome_picture = GUI_puzzle_puzzle_item_picture_unsolved(self.game, self)
            
        #self.saved_icon = GUI_puzzle_puzzle_item_saved_icon(self.game, self)
        self.saved_icon = None

        if self.cleared:
            self.solved_icon = GUI_puzzle_puzzle_item_solved_icon(self.game, self)
        else:
            self.solved_icon = None

        # draw strategy
        self.draw_strategy = "puzzle_select_puzzle_item"


    def mouse_left_up(self):
        self.game.manager.current_puzzle_file = self.puzzle_filename
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE), speed = 40)

        
    def mouse_not_over(self):
        self.alpha = .47
        if self.cleared:
            self.coloured_picture.alpha = 0.0
            self.monochrome_picture.alpha = 1.0

        
    def mouse_over(self):
        self.alpha = .78
        
        if self.cleared:        
            self.coloured_picture.alpha = 1.0
            self.monochrome_picture.alpha = 0.0
            
            self.parent.puzzle_name.set_text(str(self.puzzle_info[0]))

            if self.game.manager.current_puzzle_pack in self.game.player.puzzle_scores and self.puzzle_filename in self.game.player.puzzle_scores[self.game.manager.current_puzzle_pack]:
                seconds = int(self.game.player.puzzle_scores[self.game.manager.current_puzzle_pack][self.puzzle_filename][0] / 60)
                minutes = int(seconds / 60)
                hours = int(minutes / 60)
                seconds = seconds - (minutes * 60)
                minutes = minutes - (hours * 60)
                time_text = str(hours).rjust(2, "0") + ":" + str(minutes).rjust(2, "0") + ":" + str(seconds).rjust(2, "0")
                self.parent.puzzle_best_time.set_text("Best time: " + str(time_text))
            else:
                self.parent.puzzle_best_time.set_text("Best time: 00:00:00")
        else:
            self.parent.puzzle_name.set_text("? ? ? ?")
            self.parent.puzzle_best_time.set_text("Best time: 00:00:00")
            

    def On_Exit(self):
        GUI_element_button.On_Exit(self)
        self.monochrome_picture.Kill()
        if self.saved_icon:
            self.saved_icon.Kill()
        if self.cleared:
            self.coloured_picture.Kill()
            self.solved_icon.Kill()       



class GUI_puzzle_puzzle_item_picture_unsolved(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_puzzle_image_unsolved']
        self.x = self.parent.x + (self.parent.width / 2)
        self.y = self.parent.y + (self.parent.height / 2)
        self.width = self.image.width 
        self.height = self.image.height
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.draw_strategy = "gui_designer_monochrome_puzzle_image"


    def get_screen_draw_position(self):
        return (self.x - (self.image.width / 2), self.y - (self.image.height / 2))



class GUI_puzzle_puzzle_item_picture(Puzzle_image):
    def gui_init(self):
        Puzzle_image.gui_init(self)
        self.draw_strategy = "gui_designer_monochrome_puzzle_image"        
        
    def set_position_z_scale(self, x, y):        
        self.z = Z_GUI_OBJECT_LEVEL_5
        scale_start = self.height if self.height > self.width else self.width
        self.scale = .01 * ((64 / scale_start) * 100)
        self.x = x - ((self.width * self.scale) / 2)
        self.y = y - ((self.height * self.scale) / 2)



class GUI_puzzle_puzzle_item_saved_icon(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 40 + (self.parent.width / 2)
        self.y = self.parent.y - 40 + (self.parent.height / 2)
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.image = self.game.core.media.gfx['gui_puzzle_select_saved_icon']
        self.rotation = 16



class GUI_puzzle_puzzle_item_solved_icon(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x - 40 + (self.parent.width / 2)
        self.y = self.parent.y + 40 + (self.parent.height / 2)
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.image = self.game.core.media.gfx['gui_puzzle_select_solved_icon']
