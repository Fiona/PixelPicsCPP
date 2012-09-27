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


class GUI_puzzle_select_container(GUI_element_network_container):
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
        self.puzzle_size = Hover_text(self.game, (self.game.settings['screen_width'] / 2) - 225, 95, "puzzle_select_size", 2.0)

        self.text_offset_x = 0.0
        self.text_offset_y = 0.0

        i = 0
        for puzzle_filename in self.game.manager.current_pack.order:
            GUI_puzzle_puzzle_item(self.game, self, puzzle_filename, self.game.manager.current_pack.puzzles[puzzle_filename], i)
            i += 1

        if self.game.manager.user_created_puzzles:
            GUI_puzzle_select_rating_star_container(self.game, self)
            if not self.game.manager.current_pack.uuid in self.game.player.packs_reported:
                self.report_button = GUI_puzzle_select_report(self.game, self)
            
        # Draw strategy data
        self.draw_strategy = "puzzle_select"


    def Execute(self):
        self.update()
        self.puzzle_name.set_text("")
        self.puzzle_best_time.set_text("")
        self.puzzle_size.set_text("")
        
        self.text_offset_x += 5.0
        self.text_offset_y -= 5.0


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.puzzle_name.Kill()
        self.puzzle_best_time.Kill()
        self.puzzle_size.Kill()

        

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
        if self.game.manager.user_created_puzzles:
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_SHARING, gui_state = GUI_STATE_SHARING_DOWNLOADED), speed = 20)
        else:
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_CATEGORY_SELECT), speed = 20)


    def On_Exit(self):
        self.text.Kill()



class Hover_text(Process):
    def __init__(self, game, x, y, font = "puzzle_message", x_pad = 20.0):
        Process.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.x_pad = x_pad
        self.current_text = ""
        
        self.text = Text(
            self.game.core.media.fonts[font],
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
            self.primitive_square_width = self.text.text_width + (self.x_pad * 2)
            self.primitive_square_height = self.text.text_height + 4.0
            self.primitive_square_x = self.x - (self.text.text_width/2) - self.x_pad
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

        if self.game.manager.current_pack.uuid in self.game.player.cleared_puzzles and self.puzzle_filename in self.game.player.cleared_puzzles[self.game.manager.current_pack.uuid]:
            self.cleared = True
        else:
            self.cleared = False

        self.number_text = Text(
            self.game.core.media.fonts['puzzle_select_number'],
            self.x - 5,
            self.y,
            TEXT_ALIGN_TOP_RIGHT,
            str(self.puzzle_num + 1)
            )
        self.number_text.z = self.z
        self.number_text.colour = (0.0, 0.0, 0.0) if self.cleared else (0.3, 0.3, 0.3)
        self.number_text.shadow = 2
        self.number_text.shadow_colour = (.5, .5, .5, .5)

        if self.cleared:
            path_dir = self.game.core.path_user_pack_directory if self.game.manager.user_created_puzzles else self.game.core.path_game_pack_directory

            self.monochrome_picture = GUI_puzzle_puzzle_item_picture(
                self.game,
                self,
                self.x + (self.width / 2),
                self.y + (self.height / 2),
                puzzle_path = os.path.join(path_dir, self.game.manager.current_puzzle_pack, self.puzzle_filename),
                in_colour = False,
                fade_in_time = None
                )
            self.coloured_picture = GUI_puzzle_puzzle_item_picture(
                self.game,
                self,
                self.x + (self.width / 2),
                self.y + (self.height / 2),
                puzzle_path = os.path.join(path_dir, self.game.manager.current_puzzle_pack, self.puzzle_filename),
                in_colour = True,
                fade_in_time = None
                )
            self.coloured_picture.alpha = 0.0
            self.monochrome_picture.alpha = 1.0
        else:
            self.monochrome_picture = GUI_puzzle_puzzle_item_picture_unsolved(self.game, self)
            
        self.saved_icon = None
        self.solved_icon = None
        self.star_icon = None

        if self.game.manager.user_created_puzzles:
            save_path = self.game.core.path_saves_user_directory
        else:
            save_path = self.game.core.path_saves_game_directory

        if os.path.exists(os.path.join(save_path, self.game.manager.current_puzzle_pack + "_" + self.puzzle_filename + FILE_SAVES_EXTENSION)):
            self.saved_icon = GUI_puzzle_puzzle_item_saved_icon(self.game, self)
        
        if self.cleared:
            self.solved_icon = GUI_puzzle_puzzle_item_solved_icon(self.game, self)
            if self.game.manager.current_pack.uuid in self.game.player.puzzle_scores and self.puzzle_filename in self.game.player.puzzle_scores[self.game.manager.current_pack.uuid]:
                seconds = int(self.game.player.puzzle_scores[self.game.manager.current_pack.uuid][self.puzzle_filename][0] / 60)
                if int(seconds / 60) <= 30:
                    self.star_icon = GUI_puzzle_puzzle_item_star_icon(self.game, self)
                    
        # draw strategy
        self.draw_strategy = "puzzle_select_puzzle_item"


    def mouse_left_up(self):
        self.game.manager.current_puzzle_file = self.puzzle_filename
        if self.saved_icon:
            self.game.manager.load_puzzle_state_from = self.game.manager.current_puzzle_pack + "_" + self.puzzle_filename + FILE_SAVES_EXTENSION
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

            if self.game.manager.current_pack.uuid in self.game.player.puzzle_scores and self.puzzle_filename in self.game.player.puzzle_scores[self.game.manager.current_pack.uuid]:
                seconds = int(self.game.player.puzzle_scores[self.game.manager.current_pack.uuid][self.puzzle_filename][0] / 60)
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

        self.parent.puzzle_size.set_text(str(self.puzzle_info[1]) + "x" + str(self.puzzle_info[2]))
            

    def On_Exit(self):
        GUI_element_button.On_Exit(self)
        self.number_text.Kill()
        self.monochrome_picture.Kill()
        if self.saved_icon:
            self.saved_icon.Kill()
        if self.cleared:
            self.coloured_picture.Kill()
            self.solved_icon.Kill()       
            if self.star_icon:
                self.star_icon.Kill()



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
        self.scale = .01 * ((76.0 / scale_start) * 100)
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



class GUI_puzzle_puzzle_item_star_icon(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x - 40 + (self.parent.width / 2)
        self.y = self.parent.y - 40 + (self.parent.height / 2)
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.image = self.game.core.media.gfx['gui_puzzle_select_star_icon']




class GUI_puzzle_select_rating_star_container(GUI_element):
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent

        self.y = self.game.settings['screen_height'] - 40
        self.z = Z_GUI_OBJECT_LEVEL_5

        self.text = Text(
            self.game.core.media.fonts["puzzle_message"],
            10,
            self.y,
            TEXT_ALIGN_TOP_LEFT,
            "Rate this pack!"
            )
        self.text.z = Z_GUI_OBJECT_LEVEL_6
        self.text.colour = (1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.3, .3, .3, .5)
        
        self.width = 32 * 5
        self.height = 32
        self.x = self.text.text_width + 32
        self.gui_init()

        self.hovering = False

        self.stars = []
        for i in range(5):
            self.stars.append(GUI_puzzle_select_rating_star_star(self.game, self, i))
       
        self.draw_strategy = "primitive_square"
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
        self.primitive_square_x = self.x
        self.primitive_square_y = self.y
        self.primitive_square_colour = (0.0, 0.0, 0.0, .2)


    def mouse_over(self):
        self.hovering = True


    def mouse_out(self):
        self.hovering = False


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text.Kill()
        


class GUI_puzzle_select_rating_star_star(GUI_element):
    
    def __init__(self, game, parent, num):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.num = num
        self.image = self.game.core.media.gfx['gui_puzzle_select_rating_star']
        self.x = self.parent.x + (self.image.width * num)
        self.y = self.parent.y
        self.width = 32
        self.height = 32
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.gui_init()


    def update(self):
        if self.parent.hovering:
            return

        self.image_sequence = 1
       
        if self.game.manager.current_pack.uuid in self.game.player.pack_ratings:
            if self.num < self.game.player.pack_ratings[self.game.manager.current_pack.uuid]:
                self.image_sequence = 2


    def mouse_over(self):
        self.image_sequence = 2
        for i in range(5):
            self.parent.stars[i].image_sequence = 2 if i <= self.num else 1


    def rate(self, response):
        self.game.rate_pack(self.game.manager.current_pack.uuid, self.num + 1)


    def mouse_left_up(self):
        data = {
            'pack' : self.game.manager.current_pack.uuid,
            'rater' : self.game.author_id,
            'rating' : self.num + 1
            }
        self.parent.parent.make_request_to_server("rate_pack/", data, self.rate, task_text = "Rating pack")
        


class GUI_puzzle_select_report(GUI_element_button):
    generic_button = True
    generic_button_text = "Report Pack as Inappropriate"
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.game.settings['screen_width'] - 260
        self.y = self.game.settings['screen_height'] - 35
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        GUI_puzzle_select_report_dialog(self.game, self.parent)



class GUI_puzzle_select_report_dialog(GUI_element_window):
    title = "Report Puzzle"
    height = 170
    width = 490
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
        for text in ["Using this box you can report a puzzle as inappropriate.", "Select the reason for the report and submit it.", "It will be dealt with as soon as possible."]:
            txt = Text(self.game.core.media.fonts['basic'], self.x + 30, self.y + 30 + y, TEXT_ALIGN_TOP_LEFT, text)
            txt.z = self.z - 2
            txt.colour = (0.0, 0.0, 0.0)
            self.objs['text_' + str(y)] = txt
            y += 15

        GUI_puzzle_select_report_dialog_submit_button(self.game, self)
        GUI_puzzle_select_report_dialog_cancel_button(self.game, self)

        txt = Text(self.game.core.media.fonts['basic'], self.x + 30, self.y + 90, TEXT_ALIGN_TOP_LEFT, "Report type: ")
        txt.z = self.z - 2
        txt.colour = (0.0, 0.0, 0.0)
        self.objs['text_dropdown'] = txt        
        self.report_type = GUI_puzzle_select_report_type_dropdown(self.game, self)
        
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


    def report_pack(self, response):
        self.parent.report_button.Kill()
        self.parent.report_button = None
        GUI_element_dialog_box(self.game, self.parent, "Pack reported", ["This pack has been reported to Stompy Blondie", "and will be investigated as soon as possible.", "Thank you for helping make PixelPics better!"])
        self.Kill()
        

    def On_Exit(self):
        GUI_element_window.On_Exit(self)
        self.game.gui.block_gui_keyboard_input = False
        for x in self.objs:
            self.objs[x].Kill()



class GUI_puzzle_select_report_type_dropdown(GUI_element_dropdown):
    display_width = 300
    display_height = 25

    dropdown_options = [
        {'text' : "Inappropriate or offensive content", 'data' : 'offensive'},
        {'text' : "Pack is broken in some way", 'data' : 'broken'},
        {'text' : "Misleading pack name", 'data' : 'wrong'},
        {'text' : "Other", 'data' : 'other'}
        ]

    selected_item = 0
        
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.display_x = self.parent.x + 140
        self.display_y = self.parent.y + 85
        self.display_z = self.parent.z - 2
        self.gui_init()



class GUI_puzzle_select_report_dialog_submit_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Send"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) - (self.width) - 10
        self.y = self.parent.y + 120
        self.generic_button_text_object.x = self.x + 9
        self.generic_button_text_object.y = self.y + 4


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        data = {
            'pack' : self.game.manager.current_pack.uuid,
            'reporter' : self.game.author_id,
            'report_type' : self.parent.report_type.dropdown_options[self.parent.report_type.selected_item]['data']            
            }
        self.parent.parent.make_request_to_server("report_pack/", data, self.parent.report_pack, task_text = "Reporting pack")



class GUI_puzzle_select_report_dialog_cancel_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Cancel"

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2) + 10
        self.y = self.parent.y + 120
        self.generic_button_text_object.x = self.x + 9
        self.generic_button_text_object.y = self.y + 4


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.Kill()
