"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
import random, pickle, os

# Game engine imports
from core import *

# Game imports
from consts import *
from helpers import Net_Process_POST
from gui.gui_elements import *



class GUI_sharing_container(GUI_element):
    """
    All elements in the sharing screen live inside this thing.
    """
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_CONTAINERS
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.pack_num_to_be_uploaded = None
        
        self.net_process = None
        self.net_callback = None
        self.loading_indicator = None

        GUI_sharing_tab_newest(self.game, self)
        GUI_sharing_tab_top(self.game, self)
        GUI_sharing_tab_top_week(self.game, self)
        GUI_sharing_tab_upload(self.game, self)
        GUI_sharing_back(self.game, self)

        if self.game.gui.gui_state == GUI_STATE_SHARING_NEWEST:
            GUI_sharing_title(self.game, self, "Newest Puzzles")
        elif self.game.gui.gui_state == GUI_STATE_SHARING_TOP:
            GUI_sharing_title(self.game, self, "Top Rated Puzzles")
        elif self.game.gui.gui_state == GUI_STATE_SHARING_TOP_WEEK:
            GUI_sharing_title(self.game, self, "Top Rated Puzzles This Week")
        elif self.game.gui.gui_state == GUI_STATE_SHARING_UPLOAD:
            GUI_sharing_title(self.game, self, "My Puzzles")
            GUI_sharing_upload_scroll_window(self.game, self)

        #GUI_sharing_test_button(self.game, self)
        
        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_four_colours = True
        self.primitive_square_colour = (
              (.7,.65,.8,1.0),
              (.5,.4,.6,1.0),
              (.5,.4,.6,1.0),
              (.7,.65,.8,1.0),
            )


    def Execute(self):
        if not self.net_process is None:
            if self.net_process.is_complete():
                self.loading_indicator.Kill()
                self.loading_indicator = None                                
                if self.net_process.got_error:
                    GUI_element_dialog_box(
                        self.game,
                        self,
                        "Network error",
                        ["A network error occured!", "Please check your internet connection is functioning properly."],
                        callback = self.return_to_menu
                        )
                    self.net_process = None
                    return
                if 'error' in self.net_process.response:
                    GUI_element_dialog_box(
                        self.game,
                        self,
                        "Error",
                        ["The server returned an error:", str(self.net_process.response['error'])]
                        )
                    self.net_process = None
                elif not self.net_callback is None:
                    response = self.net_process.response
                    self.net_process = None
                    self.net_callback(response)


    def return_to_menu(self):
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 20)
        

    def make_request_to_server(self, url, data = {}, callback = None, task_text = None):
        if not self.net_process is None:
            return

        self.net_process = Net_Process_POST(SHARING_ADDRESS + url, data)
        self.net_callback = callback
        self.loading_indicator = GUI_sharing_loading_indicator(self.game, self, task_text)



class Attempt_Upload_Pack(object):

    def __init__(self, game, path, pack, container, successful_callback):
        self.game = game
        self.path = path
        self.pack = pack
        self.container = container
        self.successful_callback = successful_callback
        self.puzzles_processed = []

        if self.pack.shared:
            GUI_element_dialog_box(
                self.game,
                self.container,
                "Very Unexpected Error",
                ["This pack has already been shared!"]
                )
            return

        if not self.game.author_id == self.pack.author_id:
            GUI_element_dialog_box(
                self.game,
                self.container,
                "Very Unexpected Error",
                ["You are not authorised to share this pack!"]
                )
            return
            
        pack_info = {
            'name' : self.pack.name,
            'author_name' : self.pack.author_name,
            'author_id' : self.pack.author_id,
            'uuid' : self.pack.uuid,
            'freemode' : self.pack.freemode,
            'num_puzzles' : len(self.pack.puzzles)
            }
        self.container.make_request_to_server("new_pack/", pack_info, self.upload_puzzle, task_text = "Transfering pack data")


    def upload_puzzle(self, response):
        puzzle_to_do = None
        for i in self.pack.puzzles:
            if not i in self.puzzles_processed:
                puzzle_to_do = i
                break
        if puzzle_to_do is None:
            self.finalise_pack()
            return

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, self.path, puzzle_to_do), "rb")
            puzzle = pickle.load(f)
            f.close()
        except IOError as e:
            GUI_element_dialog_box(
                self.game,
                self.container,
                "Unexpected Error",
                ["There was an error loading the puzzle", str(puzzle_to_do)]
                )
            return

        self.puzzles_processed.append(puzzle_to_do)
        puzzle_info = {
            "name" : puzzle.name,
            "pack" : self.pack.uuid,
            "width" : puzzle.width,
            "height" : puzzle.height,
            "background" : puzzle.background,
            "cells" : puzzle.cells
            }
        self.container.make_request_to_server("new_puzzle/", puzzle_info, self.upload_puzzle, task_text = "Transfering puzzle " + str(len(self.puzzles_processed)) + " out of " + str(len(self.pack.puzzles)))


    def finalise_pack(self):
        self.container.make_request_to_server("finalise_pack/", {'pack' : self.pack.uuid}, self.successful_callback, task_text = "Finalising pack")
        
        
        
class GUI_sharing_loading_indicator(GUI_element):
    def __init__(self, game, parent, task_text):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()

        self.z = Z_GUI_OBJECT_LEVEL_11
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.text = Text(self.game.core.media.fonts['puzzle_hint_numbers'], self.width / 2, (self.height / 2) - 16, TEXT_ALIGN_CENTER, "Loading . . . ")
        self.text.z = self.z - 1
        self.text.colour = (1.0, 1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.3, .3, .3, 1.0)

        self.task_text = None
        if not task_text is None:
            self.task_text = Text(self.game.core.media.fonts['menu_subtitles'], self.width / 2, (self.height / 2) + 20, TEXT_ALIGN_CENTER, str(task_text))
            self.task_text.z = self.z - 1
            self.task_text.colour = (.7, .7, .7, 1.0)
            self.task_text.shadow = 2
            self.task_text.shadow_colour = (.3, .3, .3, 1.0)
            
        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.primitive_square_width = self.width
        self.primitive_square_height = 100
        self.primitive_square_x = 0.0
        self.primitive_square_y = (self.height / 2) - 50
        self.primitive_square_colour = (0.0,0.0,0.0,.3)


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text.Kill()
        if not self.task_text is None:
            self.task_text.Kill()
        


class GUI_sharing_test_button(GUI_element_button):
    generic_button = True
    generic_button_text = "test me"
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = 200
        self.y = 200
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def mouse_left_up(self):
        stuff = [
            [
              [(255, 255, 255), True],
              [(255, 255, 255), True],
              [(255, 255, 255), False],
              [(255, 200, 155), False],
            ],
            [
              [(255, 255, 255), True],
              [(255, 134, 255), False],
              [(255, 255, 255), False],
              [(255, 200, 155), True],
            ],
            [
              [(255, 255, 255), False],
              [(255, 255, 255), True],
              [(255, 250, 255), True],
              [(255, 200, 155), False],
            ],
          ]
        self.parent.make_request_to_server("test/", {'hello' : 'pikachu', 'width' : 10, 'stuff' : stuff}, self.get_response)


    def get_response(self, response):
        print response



class GUI_sharing_tab_newest(GUI_element_button):
    generic_button = True
    generic_button_text = "Newest Puzzles"
    toggle_button = True
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = 150
        self.y = 100
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def update(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_NEWEST:
            self.toggle_state = True
        else:
            self.toggle_state = False
        GUI_element_button.update(self)
        

    def mouse_left_up(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_NEWEST:
            return
        self.game.gui.switch_gui_state_to(GUI_STATE_SHARING_NEWEST)



class GUI_sharing_tab_top(GUI_element_button):
    generic_button = True
    generic_button_text = "Top Rated"
    toggle_button = True
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = 300
        self.y = 100
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def update(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_TOP:
            self.toggle_state = True
        else:
            self.toggle_state = False
        GUI_element_button.update(self)
        

    def mouse_left_up(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_TOP:
            return
        self.game.gui.switch_gui_state_to(GUI_STATE_SHARING_TOP)



class GUI_sharing_tab_top_week(GUI_element_button):
    generic_button = True
    generic_button_text = "Top Rated This Week"
    toggle_button = True
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = 410
        self.y = 100
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def update(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_TOP_WEEK:
            self.toggle_state = True
        else:
            self.toggle_state = False
        GUI_element_button.update(self)
        

    def mouse_left_up(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_TOP_WEEK:
            return
        self.game.gui.switch_gui_state_to(GUI_STATE_SHARING_TOP_WEEK)
        


class GUI_sharing_tab_upload(GUI_element_button):
    generic_button = True
    generic_button_text = "My Puzzles"
    toggle_button = True
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = 600
        self.y = 100
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.gui_init()


    def update(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_UPLOAD:
            self.toggle_state = True
        else:
            self.toggle_state = False
        GUI_element_button.update(self)
        

    def mouse_left_up(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_UPLOAD:
            return
        self.game.gui.switch_gui_state_to(GUI_STATE_SHARING_UPLOAD)



class GUI_sharing_title(GUI_element):
    def __init__(self, game, parent, subtitle = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_5
        
        self.text = Text(self.game.core.media.fonts['menu_titles'], 10, 10, TEXT_ALIGN_TOP_LEFT, "Download Puzzles")
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
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_width = 200
        self.primitive_square_height = self.text.text_height + 40
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_four_colours = True
        self.primitive_square_colour = (
            (.3,.2,.4,1.0),
            (.4,.3,.5,.0),
            (.4,.3,.5,.0),
            (.3,.2,.4,1.0),
            )


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text.Kill()
        if not self.subtitle is None:
            self.subtitle.Kill()



class GUI_sharing_back(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_go_back']
        self.gui_init()
        self.x = 16
        self.y = 95
        self.width = 128
        self.text = Text(self.game.core.media.fonts['category_button_completed_count'], 64, self.y, TEXT_ALIGN_TOP_LEFT, "Back")
        self.text.z = self.z - 1
        self.text.colour = (1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.2, .2, .2)


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 20)


    def On_Exit(self):
        self.text.Kill()



class GUI_sharing_upload_scroll_window(GUI_element_scroll_window):
    pack_items = []
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_4
        self.x = 50
        self.y = 175
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
            last_item = GUI_sharing_upload_pack_item(self.game, self, pack, i, count)
            self.pack_items.append(last_item)
            if not pack.shared:
                self.pack_items.append(
                    GUI_sharing_packs_button_upload(self.game, self, pack, i, count)
                    )
            count += 1
            
        if last_item is None:
            self.contents_height = 0
        else:
            self.contents_height = last_item.y + last_item.height + 10


    def finished_upload(self, response):
        if self.parent.pack_num_to_be_uploaded is None:
            return

        self.game.manager.set_as_shared(self.parent.pack_num_to_be_uploaded)
        self.reread_pack_items()
        self.parent.pack_num_to_be_uploaded = None
        


class GUI_sharing_upload_pack_item(GUI_element):
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

        self.text_pack_shared = None
        if pack.shared:
            self.text_pack_shared = Text(self.game.core.media.fonts['designer_pack_name'], self.x + self.width + self.scroll_element.x - 85, 0.0, TEXT_ALIGN_CENTER, "Shared!")
            self.text_pack_shared.z = self.z - 2
            self.text_pack_shared.colour = (1.0, 1.0, 1.0)
            self.text_pack_shared.shadow = 2
            self.text_pack_shared.shadow_colour = (.1, .1, .1)

        self.adjust_text_positions()

        self.draw_strategy = "gui_designer_packs_pack_item"


    def Execute(self):
        self.update()
        self.adjust_text_positions()


    def adjust_text_positions(self):
        self.text_pack_name.y = self.y + self.scroll_element.y + 2 - self.scroll_element.contents_scroll_location
        self.text_pack_name.clip = self.clip
        self.text_pack_author.y = self.y + self.scroll_element.y + 25 - self.scroll_element.contents_scroll_location
        self.text_pack_author.clip = self.clip
        if not self.text_pack_shared is None:
            self.text_pack_shared.y = self.y + self.scroll_element.y + 24 - self.scroll_element.contents_scroll_location
            self.text_pack_shared.clip = self.clip


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text_pack_name.Kill()
        self.text_pack_author.Kill()
        if not self.text_pack_shared is None:
            self.text_pack_shared.Kill()
            


class GUI_sharing_packs_button_upload(GUI_element_button):
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 200
        self.y = (50 * display_count) + 10 + (10 * display_count) + 12
        self.image = self.game.core.media.gfx['gui_button_sharing_upload']
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.parent.pack_num_to_be_uploaded = self.pack_num
        Attempt_Upload_Pack(self.game, self.game.manager.pack_directory_list[self.pack_num], self.pack, self.parent.parent, self.parent.finished_upload)

