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
        self.colour = (1.0, .7, .5)

        self.title = Text(self.game.core.media.fonts['menu_titles'], 20, 10, TEXT_ALIGN_TOP_LEFT, str(self.game.manager.current_pack.name))
        self.title.z = Z_GUI_OBJECT_LEVEL_2
        self.title.colour = (0.95, 0.58, 0.09)
        self.title.shadow = 2
        self.title.shadow_colour = (0.7, 0.7, 0.7)

        self.author = None
        if not self.game.manager.user_created_puzzles:
            self.author = Text(self.game.core.media.fonts['menu_subtitles'], 40, 55, TEXT_ALIGN_TOP_LEFT, "by " + str(self.game.manager.current_pack.author_name))
            self.author.z = Z_GUI_OBJECT_LEVEL_2
            self.author.colour = (0.45, 0.45, 0.45)
            self.author.shadow = 2
            self.author.shadow_colour = (0.9, 0.9, 0.9)

        GUI_puzzle_select_go_back(self.game, self)
        self.mascot_object = Mascot_Puzzle_Select(self.game)        
        self.puzzle_name = Hover_text(
            self.game,
            self.game.settings['screen_width'] / 2,
            (self.game.settings['screen_height'] / 2) - 350
            )
        self.puzzle_best_time = Hover_text(
            self.game,
            self.game.settings['screen_width'] / 2,
            (self.game.settings['screen_height'] / 2) - 310)
        self.puzzle_size = Hover_text(
            self.game,
            (self.game.settings['screen_width'] / 2) + 200,
            (self.game.settings['screen_height'] / 2) - 310,
            "puzzle_select_size",
            2.0
            )

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
        self.draw_strategy = "category_select"


    def Execute(self):
        self.update()
        self.puzzle_name.set_text("")
        self.puzzle_best_time.set_text("")
        self.puzzle_size.set_text("")
        
        self.text_offset_x += 5.0
        self.text_offset_y -= 5.0


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.title.Kill()
        self.mascot_object.Kill()
        self.puzzle_name.Kill()
        self.puzzle_best_time.Kill()
        self.puzzle_size.Kill()
        if not self.author is None:
            self.author.Kill()

        

class GUI_puzzle_select_go_back(GUI_element_button):
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
        if self.game.manager.user_created_puzzles:
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_SHARING, gui_state = GUI_STATE_SHARING_DOWNLOADED), speed = 20)
        else:
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_CATEGORY_SELECT), speed = 20)



class Hover_text(Process):
    def __init__(self, game, x, y, font = "puzzle_select_hover_text", x_pad = 20.0):
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
    generic_button = False
    
    def __init__(self, game, parent, puzzle_filename, puzzle_info, puzzle_num):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.puzzle_filename = puzzle_filename
        self.puzzle_info = puzzle_info
        self.puzzle_num = puzzle_num
        self.image = self.game.core.media.gfx['gui_puzzle_select_puzzle_box']
        self.gui_init()
        self.width = 128
        self.height = 128
        
        column = self.puzzle_num % 5
        row = self.puzzle_num / 5
        puzzle_box_size = (870, 625)
        self.x = float((puzzle_box_size[0] / 5) * column) + self.width - (self.width / 2)
        self.y = 100.0 + float((puzzle_box_size[1] / 5) * row) + self.height - (self.height / 2) - 130

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
            self.x,
            self.y + 5,
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
            if self.game.manager.current_pack.uuid in self.game.player.puzzle_scores and self.puzzle_filename in self.game.player.puzzle_scores[self.game.manager.current_pack.uuid]:
                if self.game.manager.current_pack.freemode:
                    seconds = int(self.game.player.puzzle_scores[self.game.manager.current_pack.uuid][self.puzzle_filename][0] / 60)
                    if int(seconds / 60) <= 30:
                        self.star_icon = GUI_puzzle_puzzle_item_star_icon(self.game, self)
                else:
                    if self.game.player.puzzle_scores[self.game.manager.current_pack.uuid][self.puzzle_filename][1] == 4:
                        self.star_icon = GUI_puzzle_puzzle_item_star_icon(self.game, self)
            if self.star_icon is None:
                self.solved_icon = GUI_puzzle_puzzle_item_solved_icon(self.game, self)


    def Execute(self):
        self.image_sequence = 1
        GUI_element_button.Execute(self)
        

    def mouse_left_down(self):
        self.image_sequence = 2
        if self.cleared:
            self.monochrome_picture.press()
            self.coloured_picture.press()
        else:
            self.monochrome_picture.press()
        

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.game.manager.current_puzzle_file = self.puzzle_filename
        if self.saved_icon:
            self.game.manager.load_puzzle_state_from = self.game.manager.current_puzzle_pack + "_" + self.puzzle_filename + FILE_SAVES_EXTENSION
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE), speed = 40, stop_music = True)
        if not self.cleared:
            self.monochrome_picture.un_press()

        
    def mouse_not_over(self):
        if self.cleared:
            if self.coloured_picture.alpha > 0.0:
                self.coloured_picture.alpha -= .1
        else:
            self.monochrome_picture.un_press()
            self.monochrome_picture.stop_pulse()
        self.hover_sound = False

        
    def mouse_over(self):
        if self.play_sound and not self.hover_sound:
            self.game.core.media.sfx['button_hover'].play(0)
            self.hover_sound = True
            
        if self.cleared:        
            if self.coloured_picture.alpha < 1.0:
                self.coloured_picture.alpha += .1
            
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
            self.monochrome_picture.pulse()
            
        self.parent.puzzle_size.set_text(str(self.puzzle_info[1]) + "x" + str(self.puzzle_info[2]))
            

    def On_Exit(self):
        GUI_element_button.On_Exit(self)
        self.number_text.Kill()
        self.monochrome_picture.Kill()
        if self.saved_icon:
            self.saved_icon.Kill()
        if self.cleared:
            self.coloured_picture.Kill()
            if self.solved_icon:
                self.solved_icon.Kill()       
            if self.star_icon:
                self.star_icon.Kill()



class GUI_puzzle_puzzle_item_picture_unsolved(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_puzzle_image_unsolved']
        self.set_position()
        self.width = self.image.width 
        self.height = self.image.height
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.dir = 1


    def pulse(self):
        if self.dir == 1:
            if self.scale > .8:
                self.scale -= .01
            else:
                self.scale = .8
                self.dir = 2
        else:
            if self.scale < 1.0:
                self.scale += .01
            else:
                self.scale = 1.0
                self.dir = 1
            

    def stop_pulse(self):
        if self.scale < 1.0:
            self.scale += .01
        else:
            self.scale = 1.0
        self.dir = 1


    def press(self):
        self.set_position(True)


    def un_press(self):
        self.set_position()
        
            
    def set_position(self, shift = False):
        self.x = self.parent.x + (self.parent.width / 2)
        self.y = self.parent.y + (self.parent.height / 2)
        if shift:
            self.x += 2
            self.y += 2


    def get_screen_draw_position(self):
        return (self.x - ((self.image.width * self.scale) / 2), self.y - ((self.image.height * self.scale) / 2))



class GUI_puzzle_puzzle_item_picture(Puzzle_image):
    def Execute(self):
        self.set_position()
        Puzzle_image.Execute(self)


    def gui_init(self):
        Puzzle_image.gui_init(self)
        #self.draw_strategy = "gui_designer_monochrome_puzzle_image"        
        
    def set_position_z_scale(self, x, y):        
        self.z = Z_GUI_OBJECT_LEVEL_5
        if self.in_colour:
            self.z -= 1
        scale_start = self.height if self.height > self.width else self.width
        self.scale = .01 * ((84.0 / scale_start) * 100)
        self.start_x = x
        self.start_y = y
        self.set_position()
          

    def set_position(self, shift = False):
        self.x = self.start_x - ((self.width * self.scale) / 2)
        self.y = self.start_y - ((self.height * self.scale) / 2)
        if shift:
            self.x += 2
            self.y += 2

        
    def press(self):
        self.set_position(True)
        


class GUI_puzzle_puzzle_item_saved_icon(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x - 40 + (self.parent.width / 2)
        self.y = self.parent.y + 45 + (self.parent.height / 2)
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.image = self.game.core.media.gfx['gui_puzzle_select_saved_icon']
        self.rotation = 16



class GUI_puzzle_puzzle_item_solved_icon(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 40 + (self.parent.width / 2)
        self.y = self.parent.y + 45 + (self.parent.height / 2)
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.image = self.game.core.media.gfx['gui_puzzle_select_solved_icon']



class GUI_puzzle_puzzle_item_star_icon(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 40 + (self.parent.width / 2)
        self.y = self.parent.y + 45 + (self.parent.height / 2)
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.image = self.game.core.media.gfx['gui_puzzle_select_star_icon']




class GUI_puzzle_select_rating_star_container(GUI_element):
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent

        self.x = self.game.settings['screen_width'] - 225
        self.y = self.game.settings['screen_height'] - 130
        self.z = Z_GUI_OBJECT_LEVEL_5

        self.text = Text(
            self.game.core.media.fonts["puzzle_select_rate_pack_text"],
            self.x + 15,
            self.y - 35,
            TEXT_ALIGN_TOP_LEFT,
            "Rate this pack!"
            )
        self.text.z = Z_GUI_OBJECT_LEVEL_6
        self.text.colour = (.4, .4, .4)
        self.text.shadow = 2
        self.text.shadow_colour = (1.0, 1.0, 1.0, .5)
        
        self.width = 42 * 5
        self.height = 40
        #self.x = self.text.text_width + 32
        self.gui_init()

        self.hovering = False

        self.stars = []
        for i in range(5):
            self.stars.append(GUI_puzzle_select_rating_star_star(self.game, self, i))


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
        self.x = self.parent.x + (42 * num)
        self.y = self.parent.y
        self.width = 40
        self.height = 40
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
    generic_button = False
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.game.settings['screen_width'] - 180
        self.y = self.game.settings['screen_height'] - 70
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.image = self.game.core.media.gfx['gui_puzzle_select_button_report']
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        GUI_puzzle_select_report_dialog(self.game, self.parent)



class GUI_puzzle_select_report_dialog(GUI_element_window):
    title = "Report Puzzle"
    height = 195
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
            txt = Text(self.game.core.media.fonts['window_text'], self.x + 28, self.y + 45 + y, TEXT_ALIGN_TOP_LEFT, text)
            txt.z = self.z - 2
            txt.colour = (0.3,0.3,0.3)
            self.objs['text_' + str(y)] = txt
            y += txt.text_height + 2

        GUI_puzzle_select_report_dialog_submit_button(self.game, self)
        GUI_puzzle_select_report_dialog_cancel_button(self.game, self)

        txt = Text(self.game.core.media.fonts['window_text'], self.x + 30, self.y + 117, TEXT_ALIGN_TOP_LEFT, "Report type: ")
        txt.z = self.z - 2
        txt.colour = (0.3, 0.3, 0.3)
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
        self.display_y = self.parent.y + 110
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
        self.x = self.parent.x + (self.parent.width / 2) - (self.width) - 70
        self.y = self.parent.y + 150
        self.gui_init()


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
        self.x = self.parent.x + (self.parent.width / 2) + 10
        self.y = self.parent.y + 150
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.Kill()
