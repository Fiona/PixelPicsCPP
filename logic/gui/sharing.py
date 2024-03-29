"""
PixelPics - Nonogram game
Copyright (c) 2014 Stompy Blondie Games http://stompyblondie.com
"""

# python imports
import random, pickle, os

# Game engine imports
from core import *

# Game imports
from consts import *
from gui.gui_elements import *
from puzzle import Puzzle, Pack



class GUI_sharing_container(GUI_element_network_container):
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
        
        GUI_sharing_tab_newest(self.game, self)
        GUI_sharing_tab_top(self.game, self)
        GUI_sharing_tab_top_week(self.game, self)
        GUI_sharing_tab_upload(self.game, self)
        GUI_sharing_tab_downloaded(self.game, self)
        GUI_sharing_back(self.game, self)

        if not self.game.player.sharing_content_warning_seen:
            self.game.player.sharing_content_warning_seen = True
            self.game.save_player(self.game.player)
            GUI_element_dialog_box(
                self.game,
                self,
                "Content Warning",
                ["Please note that packs downloaded through this", "service are entirely user created.", "Stompy Blondie Games are not responsible for", "any inappropriate or offensive content encountered."],
                callback = self.create_scroll_window
                )
        else:
            self.create_scroll_window()
            
        #GUI_sharing_test_button(self.game, self)
        
        # Draw strategy data
        self.draw_strategy = "present_background"
        self.text_offset_x = 0.0
        self.text_offset_y = 0.0


    def Execute(self):
        GUI_element_network_container.Execute(self)
        self.text_offset_x += 5.0
        self.text_offset_y -= 5.0
        

    def create_scroll_window(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_NEWEST:
            GUI_sharing_title(self.game, self, "Newest Puzzles")
            GUI_sharing_newest_puzzles_scroll_window(self.game, self)
        elif self.game.gui.gui_state == GUI_STATE_SHARING_TOP:
            GUI_sharing_title(self.game, self, "Top Rated Puzzles")
            GUI_sharing_top_puzzles_scroll_window(self.game, self)
        elif self.game.gui.gui_state == GUI_STATE_SHARING_TOP_WEEK:
            GUI_sharing_title(self.game, self, "Top Rated Puzzles This Week")
            GUI_sharing_top_week_puzzles_scroll_window(self.game, self)
        elif self.game.gui.gui_state == GUI_STATE_SHARING_UPLOAD:
            GUI_sharing_title(self.game, self, "My Puzzles")
            GUI_sharing_upload_scroll_window(self.game, self)
        elif self.game.gui.gui_state == GUI_STATE_SHARING_DOWNLOADED:
            GUI_sharing_title(self.game, self, "Downloaded Puzzles")
            GUI_sharing_downloaded_scroll_window(self.game, self)
        


class Attempt_Download_Pack(object):
    def __init__(self, game, pack, container, successful_callback):
        self.game = game
        self.pack = pack
        self.container = container
        self.successful_callback = successful_callback
        self.puzzle_downloading  = 1

        # Check pack hasn't already been downloaded
        if self.pack['uuid'] in self.game.manager.pack_uuids:
            GUI_element_dialog_box(
                self.game,
                self.container,
                "Very Unexpected Error",
                ["This pack has already been downloaded."]
                )
            return

        # check the pack doesn't belong to us already
        if self.pack['author_id'] == self.game.author_id:
            GUI_element_dialog_box(
                self.game,
                self.container,
                "Very Unexpected Error",
                ["This pack belongs to you anyway!"]
                )
            return

        # Make sure we have all the info we need to construct it
        for i in ['size', 'uuid', 'author', 'name', 'size', 'freemode']:
            if not i in self.pack:
                GUI_element_dialog_box(
                    self.game,
                    self,
                    "Error",
                    ["We don't have all the expected data on this pack."]
                    )
                return

        # Make directory for this pack
        try:
            self.pack_directory = self.game.manager.generate_unique_filename(self.game.core.path_user_pack_directory)
            os.mkdir(os.path.join(self.game.core.path_user_pack_directory, self.pack_directory))
        except IOError as e:
            GUI_element_dialog_box(
                self.game,
                self,
                "Error",
                ["There was an error making the directory for this pack."]
                )
            return

        # Make pack object
        self.new_pack = Pack()
        self.new_pack.uuid = self.pack['uuid']
        self.new_pack.author_id = self.pack['author_id']
        self.new_pack.author_name = self.pack['author']
        self.new_pack.name = self.pack['name']
        self.new_pack.freemode = self.pack['freemode']
        self.new_pack.puzzles = {}
        self.new_pack.order = []        

        # Download first puzzle
        self.make_puzzle_dowwnload_request()


    def make_puzzle_dowwnload_request(self):
        self.container.make_request_to_server(
            "download_puzzle/",
            {'pack' : self.pack['uuid'], 'puzzle_num' : self.puzzle_downloading},
            self.download_puzzle,
            task_text = "Downloading puzzle " + str(self.puzzle_downloading) + "/" + str(self.pack['size'])
            )


    def download_puzzle(self, response):
        # make sure that everything that should be here is here
        for i in ['name', 'width', 'height', 'background', 'cells']:
            if not i in response:
                GUI_element_dialog_box(
                    self.game,
                    self,
                    "Error",
                    ["Missing expected data for puzzle."]
                    )
                return

        for i in ['name', 'pack', 'background']:
            if response[i].strip() == "":
                GUI_element_dialog_box(
                    self.game,
                    self,
                    "Error",
                    ["Missing expected data for puzzle."]
                    )
                return
            
        if len(response['cells']) == 0:
            GUI_element_dialog_box(
                self.game,
                self,
                "Error",
                ["Cells data for puzzle is empty."]
                )
            return

        # make sure it's the right pack!
        if not self.new_pack.uuid == response['pack']:
            GUI_element_dialog_box(
                self.game,
                self,
                "Error",
                ["Puzzle recieved is not for pack we are attempting to download."]
                )
            return
        
        # make sure pack doesn't need any more puzzles
        if len(self.new_pack.puzzles) >= self.pack['size']:
            GUI_element_dialog_box(
                self.game,
                self,
                "Error",
                ["Pack has too many puzzles already."]
                )
            return
        
        # ensure sizes aren't out of bounds
        if response['width'] < MIN_PUZZLE_SIZE or response['height'] < MIN_PUZZLE_SIZE \
               or response['width'] > MAX_PUZZLE_SIZE or response['height'] > MAX_PUZZLE_SIZE:
            GUI_element_dialog_box(
                self.game,
                self,
                "Error",
                ["Puzzle with out of bound sizes submitted."]
                )
            return

        # make sure each row and column isn't a crazy size
        if len(response['cells']) < response['height'] or len(response['cells']) > response['height']:
            GUI_element_dialog_box(
                self.game,
                self,
                "Error",
                ["Puzzle row count is inconsistent."]
                )
            return

        for col in response['cells']:
            if len(col) < response['width'] or len(col) > response['width']:
                GUI_element_dialog_box(
                    self.game,
                    self,
                    "Error",
                    ["Puzzle column count is inconsistent."]
                    )
                return
            # make sure each cell is correct
            for cell in col:
                if len(cell) != 2 or len(cell[1]) != 3:
                    GUI_element_dialog_box(
                        self.game,
                        self,
                        "Error",
                        ["Puzzle has a malformed cell."]
                        )
                    return

        # Get name for puzzle file
        puzzle_filename = self.game.manager.generate_unique_filename(os.path.join(self.game.core.path_user_pack_directory, self.pack_directory), extension = FILE_PUZZLE_EXTENSION)
        
        # create new puzzle object
        puzzle = Puzzle()
        puzzle.name = response['name']
        puzzle.width = response['width']
        puzzle.height = response['height']
        puzzle.cells = response['cells']
        puzzle.background = response['background']

        puzzle.row_numbers = [(0,)] * puzzle.height
        puzzle.column_numbers = [(0,)] * puzzle.width
        self.game.manager.work_out_puzzle_hint_numbers(puzzle)
        
        # write it to a file
        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, self.pack_directory, puzzle_filename), "wb")
            pickle.dump(puzzle, f)
            f.close()             
        except IOError as e:
            GUI_element_dialog_box(
                self.game,
                self,
                "Error",
                ["There was an error writing this puzzle to a file."]
                )
            return

        # add to current pack
        self.new_pack.order.append(puzzle_filename)
        self.new_pack.puzzles[puzzle_filename] = [puzzle.name, puzzle.width, puzzle.height]

        # Either complete the pack or request the next puzzle
        if self.puzzle_downloading == self.pack['size']:
            self.container.make_request_to_server(
                "finish_pack_download/",
                {'pack' : self.new_pack.uuid},
                self.complete_pack,
                task_text = "Finishing pack download"
                )
        else:
            self.puzzle_downloading += 1
            self.make_puzzle_dowwnload_request()
            

    def complete_pack(self, response):
        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, self.pack_directory, FILE_PACK_INFO_FILE), "wb")
            pickle.dump(self.new_pack, f)
            f.close()             
        except IOError as e:
            GUI_element_dialog_box(
                self.game,
                self,
                "Error",
                ["There was an error writing this pack to a file."]
                )
            return

        self.game.manager.load_packs()
        self.successful_callback()



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
        for i in self.pack.order:
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
    generic_button = False
    toggle_button = True
    no_click_when_toggled = True
    toggle_frame = 4
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_sharing_tab_newest']
        self.x = 125
        self.y = 85
        self.width = 158
        self.height = 77
        self.gui_init()


    def update(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_NEWEST:
            self.toggle_state = True
            self.z = Z_GUI_OBJECT_LEVEL_4
        else:
            self.toggle_state = False
            self.z = Z_GUI_OBJECT_LEVEL_3 - 2
        GUI_element_button.update(self)
        

    def mouse_left_up(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_NEWEST:
            return
        self.game.gui.switch_gui_state_to(GUI_STATE_SHARING_NEWEST)



class GUI_sharing_tab_top(GUI_element_button):
    generic_button = False
    toggle_button = True
    no_click_when_toggled = True
    toggle_frame = 4
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_sharing_tab_top']
        self.x = 270
        self.y = 85
        self.width = 158
        self.height = 77
        self.gui_init()


    def update(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_TOP:
            self.toggle_state = True
            self.z = Z_GUI_OBJECT_LEVEL_4
        else:
            self.toggle_state = False
            self.z = Z_GUI_OBJECT_LEVEL_3 - 1
        GUI_element_button.update(self)
        

    def mouse_left_up(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_TOP:
            return
        self.game.gui.switch_gui_state_to(GUI_STATE_SHARING_TOP)



class GUI_sharing_tab_top_week(GUI_element_button):
    generic_button = False
    toggle_button = True
    no_click_when_toggled = True
    toggle_frame = 4
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_sharing_tab_top_week']
        self.x = 415
        self.y = 85
        self.width = 158
        self.height = 77
        self.gui_init()


    def update(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_TOP_WEEK:
            self.toggle_state = True
            self.z = Z_GUI_OBJECT_LEVEL_4
        else:
            self.toggle_state = False
            self.z = Z_GUI_OBJECT_LEVEL_3
        GUI_element_button.update(self)
        

    def mouse_left_up(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_TOP_WEEK:
            return
        self.game.gui.switch_gui_state_to(GUI_STATE_SHARING_TOP_WEEK)
        


class GUI_sharing_tab_upload(GUI_element_button):
    generic_button = False
    toggle_button = True
    no_click_when_toggled = True
    toggle_frame = 4
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_sharing_tab_my_puzzles']
        self.x = self.game.settings['screen_width'] - 375
        self.y = 85
        self.width = 158
        self.height = 77
        self.gui_init()


    def update(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_UPLOAD:
            self.toggle_state = True
            self.z = Z_GUI_OBJECT_LEVEL_4
        else:
            self.toggle_state = False
            self.z = Z_GUI_OBJECT_LEVEL_3 - 1
        GUI_element_button.update(self)
        

    def mouse_left_up(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_UPLOAD:
            return
        self.game.gui.switch_gui_state_to(GUI_STATE_SHARING_UPLOAD)



class GUI_sharing_tab_downloaded(GUI_element_button):
    generic_button = False
    toggle_button = True
    no_click_when_toggled = True
    toggle_frame = 4
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.image = self.game.core.media.gfx['gui_button_sharing_tab_downloaded']
        self.x = self.game.settings['screen_width'] - 230
        self.y = 85
        self.width = 158
        self.height = 77
        self.gui_init()
        

    def update(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_DOWNLOADED:
            self.toggle_state = True
            self.z = Z_GUI_OBJECT_LEVEL_4
        else:
            self.toggle_state = False
            self.z = Z_GUI_OBJECT_LEVEL_3
        GUI_element_button.update(self)
        

    def mouse_left_up(self):
        if self.game.gui.gui_state == GUI_STATE_SHARING_DOWNLOADED:
            return
        self.game.gui.switch_gui_state_to(GUI_STATE_SHARING_DOWNLOADED)



class GUI_sharing_title(GUI_element):
    def __init__(self, game, parent, subtitle = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_5
        
        self.text = Text(self.game.core.media.fonts['menu_titles'], 10, 10, TEXT_ALIGN_TOP_LEFT, "Download Puzzles")
        self.text.colour = (0.95, 0.58, 0.09)
        self.text.shadow = 2
        self.text.shadow_colour = (0.7, 0.7, 0.7)
        self.text.z = self.z - 1

        if not subtitle is None:
            self.subtitle = Text(self.game.core.media.fonts['menu_subtitles'], 30, 50, TEXT_ALIGN_TOP_LEFT, subtitle)
            self.subtitle.colour = (0.45, 0.45, 0.45)
            self.subtitle.shadow = 2
            self.subtitle.shadow_colour = (0.9, 0.9, 0.9)
            self.subtitle.z = self.z - 2
        else:
            self.subtitle = None


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
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.image = self.game.core.media.gfx['gui_button_go_back']
        self.gui_init()
        self.x = -8
        self.y = self.game.settings['screen_height'] - self.image.height - 16


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 20)



class GUI_sharing_upload_scroll_window(GUI_element_scroll_window):
    pack_items = []
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.x = 127
        self.y = 160
        self.width = self.game.settings['screen_width'] - 200
        self.height = self.game.settings['screen_height'] - 200
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
        

    def upload_button_clicked(self, pack_num):
        self.parent.pack_num_to_be_uploaded = pack_num

        if not self.game.player.sharing_upload_content_agreed:
            GUI_element_confirmation_box(
                self.game,
                self,
                "Upload Terms",
                [
                  "To upload a pack to the PixelPics server you must agree to the following terms:",
                  "* You will not upload a pack containing inappropriate or offensive content. This",
                  "  includes but is not limited to nudity, excessive violence, sexism, racism",
                  "  and homophobia.",
                  "* Pack names must accurately describe the containing puzzles and not be misleading.",
                  "* Packs must not be intentionally harmful.",
                  "* Packs can be be removed from the service by Stompy Blondie at any time and for any",
                  "  reason.",
                  "* Your access to the service can be terminated at any time if you violate any of",
                  "  these terms.",
                  "Do you agree?"
                ],
                confirm_callback = self.Agreed_to_terms
                )
        else:
            self.Agreed_to_terms(pack_num)


    def Agreed_to_terms(self, pack_num):
        self.game.player.sharing_upload_content_agreed = True
        self.game.save_player(self.game.player)
        GUI_element_confirmation_box(
            self.game,
            self,
            "Do you want to share?",
            [
              "Are you sure you want to share this pack?",
              '"' + self.game.manager.packs[pack_num].name + '"',
              "Note that you can't share it again,",
              "so make sure you have finished this pack."
            ],
            confirm_callback = lambda: Attempt_Upload_Pack(self.game, self.game.manager.pack_directory_list[pack_num], self.game.manager.packs[pack_num], self.parent, self.finished_upload)
            )
        


class GUI_sharing_upload_pack_item(GUI_element):
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

        self.text_pack_name = Text(self.game.core.media.fonts['designer_pack_name'], self.x + self.scroll_element.x + 5, 0.0, TEXT_ALIGN_TOP_LEFT, str(self.pack.name))
        self.text_pack_name.z = self.z - 2
        self.text_pack_name.colour = (0.95, 0.58, 0.09, 1.0)
        self.text_pack_name.shadow = 2
        self.text_pack_name.shadow_colour = (.8, .8, .8)

        self.text_pack_author = Text(self.game.core.media.fonts['designer_pack_author'], self.x + self.scroll_element.x + 15, 0.0, TEXT_ALIGN_TOP_LEFT, str("by " + self.pack.author_name))
        self.text_pack_author.z = self.z - 2
        self.text_pack_author.colour = (.55, .55, .55)
        self.text_pack_author.shadow = 2
        self.text_pack_author.shadow_colour = (.8, .8, .8)

        self.text_pack_shared = None
        if pack.shared:
            self.text_pack_shared = Text(self.game.core.media.fonts['sharing_your_pack_message'], self.x + self.width + self.scroll_element.x - 85, 0.0, TEXT_ALIGN_CENTER, "Shared!")
            self.text_pack_shared.z = self.z - 2
            self.text_pack_shared.colour = (.55, .55, .55)

        self.adjust_text_positions()

        self.draw_strategy = "gui_designer_packs_pack_item"


    def Execute(self):
        self.update()
        self.adjust_text_positions()


    def mouse_left_up(self):
        if not self.pack.shared:
            self.parent.upload_button_clicked(self.pack_num)


    def adjust_text_positions(self):
        self.text_pack_name.y = self.y + self.scroll_element.y + 2 - self.scroll_element.contents_scroll_location
        self.text_pack_name.clip = self.clip
        self.text_pack_author.y = self.y + self.scroll_element.y + 35 - self.scroll_element.contents_scroll_location
        self.text_pack_author.clip = self.clip
        if not self.text_pack_shared is None:
            self.text_pack_shared.y = self.y + self.scroll_element.y + 30 - self.scroll_element.contents_scroll_location
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
        self.x = self.parent.width - 140
        self.y = (65 * display_count) + 5 + (10 * display_count) + 12
        self.image = self.game.core.media.gfx['gui_button_sharing_upload']
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.upload_button_clicked(self.pack_num)



class GUI_sharing_load_puzzles_scroll_window(GUI_element_scroll_window):
    pack_items = []
    url = ""
    task_text = None
    current_page = 1
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.x = 127
        self.y = 160
        self.width = self.game.settings['screen_width'] - 200
        self.height = self.game.settings['screen_height'] - 200
        self.text_num_pages = None
        self.gui_init()
        self.current_page = 1
        self.next_button = None
        self.prev_button = None
        self.go_to_page(self.current_page)


    def Execute(self):
        self.update()
        self.adjust_text_positions()


    def go_to_page(self, page):
        self.current_page = page
        self.parent.make_request_to_server(self.url, {'page' : page}, self.display_loaded_packs, task_text = self.task_text)


    def display_loaded_packs(self, response):
        # kill, reset etc
        for x in self.pack_items:
            x.Kill()
        if not self.next_button is None:
            self.next_button.Kill()
            self.next_button = None
        if not self.prev_button is None:
            self.prev_button.Kill()
            self.prev_button = None
        self.contents_scroll_location = 0.0
        self.pack_items = []
        
        # Make sure we got everything
        for i in ['num_pages', 'success', 'packs']:
            if not i in response:
                GUI_element_dialog_box(
                    self.game,
                    self,
                    "Error",
                    ["Not all expected data was returned by the server."]
                    )
                return
            
        self.num_pages = response['num_pages']
        self.raw_pack_data = response['packs']

        # Create objects for each pack
        self.create_pack_objects()

        # page number
        if not self.text_num_pages is None:
            self.text_num_pages.Kill()
        self.text_num_pages = Text(self.game.core.media.fonts['sharing_page_number'], self.x + (self.width / 2), self.y + self.contents_height - 30, TEXT_ALIGN_TOP, "Page " + str(self.current_page) + " of " + str(self.num_pages))


        self.text_num_pages.z = self.z - 2
        self.text_num_pages.colour = (.55, .55, .55)
        self.contents_height += 128

        # prev/next page buttons
        next_disabled = False if self.current_page < self.num_pages else True
        self.next_button = GUI_sharing_packs_button_next(self.game, self, next_disabled)
        prev_disabled = False if self.current_page > 1 else True
        self.prev_button = GUI_sharing_packs_button_prev(self.game, self, prev_disabled)

        self.adjust_text_positions()
                    

    def create_pack_objects(self):
        if len(self.pack_items):
            for i in self.pack_items:
                i.Kill()
        self.pack_items = []
        last_item = None
        count = 0
        for i,pack in enumerate(self.raw_pack_data):
            last_item = GUI_sharing_load_puzzles_pack_item(self.game, self, pack, i, count)
            self.pack_items.append(last_item)
            count += 1
            
        if last_item is None:
            self.contents_height = 0
        else:
            self.contents_height = last_item.y + last_item.height
        

    def finished_download(self):
        self.create_pack_objects()
        

    def adjust_text_positions(self):
        if not self.text_num_pages is None:
            height = self.contents_height if self.contents_height > self.height else self.height
            self.text_num_pages.y = self.y + height - 60 - self.contents_scroll_location
            self.text_num_pages.clip = (self.x, self.y, self.width, self.height)
            

    def On_Exit(self):
        GUI_element.On_Exit(self)
        if not self.text_num_pages is None:
            self.text_num_pages.Kill()



class GUI_sharing_load_puzzles_pack_item(GUI_element):
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

        self.text_pack_name = Text(self.game.core.media.fonts['designer_pack_name'], self.x + self.scroll_element.x + 155, 0.0, TEXT_ALIGN_TOP_LEFT, str(self.pack['name']))
        self.text_pack_name.z = self.z - 2
        self.text_pack_name.colour = (0.95, 0.58, 0.09, 1.0)
        self.text_pack_name.shadow = 2
        self.text_pack_name.shadow_colour = (.8, .8, .8)

        self.text_pack_author = Text(self.game.core.media.fonts['designer_pack_author'], self.x + self.scroll_element.x + 170, 0.0, TEXT_ALIGN_TOP_LEFT, str("by " + self.pack['author']))
        self.text_pack_author.z = self.z - 2
        self.text_pack_author.colour = (.55, .55, .55)
        self.text_pack_author.shadow = 2
        self.text_pack_author.shadow_colour = (.8, .8, .8)

        self.text_pack_puzzle_count = Text(self.game.core.media.fonts['designer_pack_author'], self.x + self.scroll_element.x + 15, 0.0, TEXT_ALIGN_TOP_LEFT, str(str(self.pack['size']) + " Puzzles"))
        self.text_pack_puzzle_count.z = self.z - 2
        self.text_pack_puzzle_count.colour = (.55, .55, .55)
        self.text_pack_puzzle_count.shadow = 2
        self.text_pack_puzzle_count.shadow_colour = (.8, .8, .8)

        self.text_pack_yours = None
        
        if self.pack['uuid'] in self.game.manager.pack_uuids:
            if self.pack['author_id'] == self.game.author_id:
                self.text_pack_yours = Text(self.game.core.media.fonts['sharing_your_pack_message'], self.x + self.width + self.scroll_element.x - 100, 0.0, TEXT_ALIGN_CENTER, "Your pack")
                self.text_pack_yours.z = self.z - 2
                self.text_pack_yours.colour = (.55, .55, .55)
            else:
                self.button = GUI_sharing_packs_button_play(self.game, self, self.pack, self.pack_num, display_count)
        else:
            self.button = GUI_sharing_packs_button_download(self.game, self, self.pack, self.pack_num, display_count)

        self.rating_stars = GUI_sharing_packs_rating_stars(self.game, self, int(self.pack['rating_average']), display_count)
            
        self.adjust_text_positions()
        
        self.draw_strategy = "gui_designer_packs_pack_item"

    def mouse_left_up(self):
        if self.pack['uuid'] in self.game.manager.pack_uuids:
            if self.pack['author_id'] == self.game.author_id:
                return
        self.button.mouse_left_up()


    def Execute(self):
        self.update()
        self.adjust_text_positions()

    def adjust_text_positions(self):
        self.text_pack_name.y = self.y + self.scroll_element.y + 2 - self.scroll_element.contents_scroll_location
        self.text_pack_name.clip = self.clip
        self.text_pack_author.y = self.y + self.scroll_element.y + 35 - self.scroll_element.contents_scroll_location
        self.text_pack_author.clip = self.clip
        self.text_pack_puzzle_count.y = self.y + self.scroll_element.y + 35 - self.scroll_element.contents_scroll_location
        self.text_pack_puzzle_count.clip = self.clip
        if not self.text_pack_yours is None:
            self.text_pack_yours.y = self.y + self.scroll_element.y + 30 - self.scroll_element.contents_scroll_location
            self.text_pack_yours.clip = self.clip

    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text_pack_name.Kill()
        self.text_pack_author.Kill()
        self.text_pack_puzzle_count.Kill()
        if not self.text_pack_yours is None:
            self.text_pack_yours.Kill()
            

class GUI_sharing_packs_rating_stars(GUI_element):
    def __init__(self, game, parent, rating, display_count):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        if rating < 0 or rating > 5:
            rating = 0
        self.scroll_element = self.parent.parent
        self.x = 25
        self.y = (65 * display_count) + 10 + (10 * display_count) + 12
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.image = self.game.core.media.gfx['gui_sharing_rating_stars']
        self.image_sequence = rating + 1
        self.gui_init()
        


class GUI_sharing_packs_button_download(GUI_element_button):
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 60
        self.y = (65 * display_count) + 5 + (10 * display_count) + 12
        self.image = self.game.core.media.gfx['gui_button_sharing_download']
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        Attempt_Download_Pack(self.game, self.pack, self.parent.parent.parent, self.parent.parent.finished_download)



class GUI_sharing_packs_button_play(GUI_element_button):
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 60
        self.y = (65 * display_count) + 5 + (10 * display_count) + 12
        self.image = self.game.core.media.gfx['gui_button_sharing_play']
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.game.manager.user_created_puzzles = True
        self.game.manager.load_pack(
            self.game.manager.pack_directory_list[self.game.manager.pack_uuids.index(self.pack['uuid'])],
            user_created = True
            )
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE_SELECT), speed = 20)



class GUI_sharing_packs_button_next(GUI_element_button):
    def __init__(self, game, parent = None, disabled = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = (self.parent.width / 2) + 130
        height = self.parent.contents_height if self.parent.contents_height > self.parent.height else self.parent.height        
        self.y = height - 70 - self.parent.contents_scroll_location
        self.image = self.game.core.media.gfx['gui_button_sharing_next']
        self.disabled = disabled
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        self.parent.go_to_page(self.parent.current_page + 1)
        


class GUI_sharing_packs_button_prev(GUI_element_button):
    def __init__(self, game, parent = None, disabled = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = (self.parent.width / 2) - 240
        height = self.parent.contents_height if self.parent.contents_height > self.parent.height else self.parent.height        
        self.y = height - 70 - self.parent.contents_scroll_location
        self.image = self.game.core.media.gfx['gui_button_sharing_prev']
        self.disabled = disabled
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return
        self.parent.go_to_page(self.parent.current_page - 1)
        


class GUI_sharing_newest_puzzles_scroll_window(GUI_sharing_load_puzzles_scroll_window):
    url = "newest/"
    task_text = "Downloading pack info"


class GUI_sharing_top_puzzles_scroll_window(GUI_sharing_load_puzzles_scroll_window):
    url = "top/"
    task_text = "Downloading pack info"


class GUI_sharing_top_week_puzzles_scroll_window(GUI_sharing_load_puzzles_scroll_window):
    url = "top_week/"
    task_text = "Downloading pack info"



class GUI_sharing_downloaded_scroll_window(GUI_element_scroll_window):
    pack_items = []
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.x = 127
        self.y = 160
        self.width = self.game.settings['screen_width'] - 200
        self.height = self.game.settings['screen_height'] - 200
        self.gui_init()
        self.reread_pack_items()


    def reread_pack_items(self):
        for x in self.pack_items:
            x.Kill()
        self.contents_scroll_location = 0.0
        self.pack_items = []
        last_item = None
        count = 0

        for i,pack in reversed(list(enumerate(self.game.manager.packs))):
            if pack.author_id == self.game.author_id:
                continue
            last_item = GUI_sharing_downloaded_pack_item(self.game, self, pack, i, count)
            self.pack_items.append(last_item)
            self.pack_items.append(
                GUI_sharing_packs_downloaded_button_play(self.game, self, pack, i, count)
                )
            self.pack_items.append(
                GUI_sharing_packs_downloaded_button_delete(self.game, self, pack, i, count)
                )
            count += 1
            
        if last_item is None:
            self.contents_height = 0
        else:
            self.contents_height = last_item.y + last_item.height + 10



class GUI_sharing_downloaded_pack_item(GUI_element):
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.pack = pack
        self.pack_num = pack_num
        self.pack_dir = self.game.manager.pack_directory_list[self.pack_num]
        self.z = Z_GUI_OBJECT_LEVEL_5 - 1
        self.x = 15
        self.y = (65 * display_count) + 15 + (10 * display_count)
        self.width = self.parent.width - 80
        self.height = 65
        self.alpha = .1
        self.gui_init()

        self.text_pack_name = Text(self.game.core.media.fonts['designer_pack_name'], self.x + self.scroll_element.x + 5, 0.0, TEXT_ALIGN_TOP_LEFT, str(self.pack.name))
        self.text_pack_name.z = self.z - 2
        self.text_pack_name.colour = (0.95, 0.58, 0.09, 1.0)
        self.text_pack_name.shadow = 2
        self.text_pack_name.shadow_colour = (.8, .8, .8)

        self.text_pack_author = Text(self.game.core.media.fonts['designer_pack_author'], self.x + self.scroll_element.x + 15, 0.0, TEXT_ALIGN_TOP_LEFT, str("by " + self.pack.author_name))
        self.text_pack_author.z = self.z - 2
        self.text_pack_author.colour = (.55, .55, .55)
        self.text_pack_author.shadow = 2
        self.text_pack_author.shadow_colour = (.8, .8, .8)

        completed = len(self.game.player.cleared_puzzles[self.pack.uuid]) if self.pack.uuid in self.game.player.cleared_puzzles else 0
        text = Text(self.game.core.media.fonts['category_button_total_count'], self.x + self.width - 70, 0, TEXT_ALIGN_TOP, str(completed) + " of " + str(len(self.pack.puzzles)))
        text.z = self.z - 1
        text.colour = (.55, .55, .55)
        text.shadow = 2
        text.shadow_colour = (.8, .8, .8)
        self.text_total_count = text

        text = Text(self.game.core.media.fonts['category_button_total_count'], self.x + self.width - 70, 0, TEXT_ALIGN_TOP, "solved")
        text.z = self.z - 1
        text.colour = (.55, .55, .55)
        text.shadow = 2
        text.shadow_colour = (.8, .8, .8)
        self.text_solved = text

        self.adjust_text_positions()

        self.draw_strategy = "gui_designer_packs_pack_item"

    def mouse_left_up(self):
        self.game.manager.user_created_puzzles = True
        self.game.manager.load_pack(self.game.manager.pack_directory_list[self.pack_num], user_created = True)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE_SELECT), speed = 20)

    def Execute(self):
        self.update()
        self.adjust_text_positions()

    def adjust_text_positions(self):
        self.text_pack_name.y = self.y + self.scroll_element.y + 2 - self.scroll_element.contents_scroll_location
        self.text_pack_name.clip = self.clip

        self.text_pack_author.y = self.y + self.scroll_element.y + 35 - self.scroll_element.contents_scroll_location
        self.text_pack_author.clip = self.clip

        self.text_total_count.y = self.y + self.scroll_element.y + 8 - self.scroll_element.contents_scroll_location
        self.text_total_count.clip = self.clip

        self.text_solved.y = self.y + self.scroll_element.y + 26 - self.scroll_element.contents_scroll_location
        self.text_solved.clip = self.clip


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text_pack_name.Kill()
        self.text_pack_author.Kill()
        self.text_total_count.Kill()
        self.text_solved.Kill()


        
class GUI_sharing_packs_downloaded_button_play(GUI_element_button):
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 205
        self.y = (65 * display_count) + 5 + (10 * display_count) + 12
        self.image = self.game.core.media.gfx['gui_button_sharing_play']
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.game.manager.user_created_puzzles = True
        self.game.manager.load_pack(self.game.manager.pack_directory_list[self.pack_num], user_created = True)
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE_SELECT), speed = 20)



class GUI_sharing_packs_downloaded_button_delete(GUI_element_button):
    def __init__(self, game, parent = None, pack = None, pack_num = 0, display_count = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.scroll_element = self.parent
        self.pack = pack
        self.pack_num = pack_num
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.x = self.parent.width - 140
        self.y = (65 * display_count) + 5 + (10 * display_count) + 12
        self.image = self.game.core.media.gfx['gui_button_sharing_delete']
        self.gui_init()
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        GUI_element_confirmation_box(
            self.game,
            self,
            "Delete Pack",
            ["This will delete this puzzle pack from your computer.",
             "Are you sure you want to delete this?"],
            confirm_callback = self.delete
            )


    def delete(self):
        try:
            self.game.manager.delete_user_created_pack(self.game.manager.pack_directory_list[self.pack_num])
        except Exception as e:
            GUI_element_dialog_box(self.game, self.parent, "Error", [str(e)])
        finally:
            self.parent.reread_pack_items()
