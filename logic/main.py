"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
import sys, os, pickle

# Game engine imports
from core import *

# Game imports
sys.path.append(os.path.join(os.getcwd(), "logic"))
from consts import *
from gui import GUI, Mouse
from puzzle import Puzzle_manager


class Game(Process):
    """
    Main game process.
    """
    # Major game settings like screen size and audio volume
    # If you change settings you need to call core.settings.save() to make sure they're updated.
    settings = {
        'screen_width' : 1,
        'screen_height' : 1,
        'full_screen' : 1,
        'music_on' : 1,
        'sound_effects_on' : 1,
        'music_vol' : 100,
        'sound_effects_vol' : 100
        }
    
    # UUID tying an author to puzzle packs
    author_id = ""
    
    # Current state
    game_state = 0

    # Current state of the tool, also determines cursor image
    cursor_tool_state = DRAWING_TOOL_STATE_NORMAL

    # If we're in freemode or not. If not we're not allowed to make mistakes and
    # we're able to fail puzzles.
    freemode = False

    # Player lives, only relevant when not in freemode but they're still pretty important dontchaknow
    lives = INITIAL_LIVES

    # Counts frames to keep track of how long has passed while playing a puzzle
    timer = 0

    # If true during puzzles it implies we're in a menu of some kind
    paused = False

    # list of categories in order that they are to be unlocked
    game_categories = ["0003", "0004", "0005", "0006", "0007", "0008", "0009", "0010", "0011"]

    # This is the list of packs 
    game_category_uuids = [
        'e6ee1b0e-7bba-4ba0-a9c3-b472f487216b',
        '6430bf70-477c-4986-a3a9-c30ae9a62bac',
        'a2625422-1e9e-4e82-bd8a-dc1bec88a180',
        '98536f87-9bb5-4f53-9f18-883629d5be55',
        'e8e0c564-bba7-4540-ac6b-4d4dded6b632',
        '0dacedbc-e631-4934-9138-011ca35f0517',
        'dc4d7a02-662f-404d-9bc5-d6dda5513a63',
        'b4f81a2f-cc97-409b-b63c-bb8baa04b1ae',
        '47b00a2d-745a-4b0c-9612-d3d104629746',
        '39936662-a0f1-4546-8c50-d788fbd197a9',
        ]
    
    # Name of a category that we're going to do the unlock animation on if appropriate
    category_to_unlock = None    
    
    # Self explanitory object pointers and lists
    fps_text = None
    gui = None
    manager = None

    # Stuff we need to keep track of
    current_zoom_level = 1.0
    minimum_zoom_level = 1.0

    # When is set to true, we wont get the main menu animation
    no_button_anim = False

    # Current playing music, is compared to when a music is supposed to be playing
    current_playing_music = None

    # Keeps track of what we should be playing even if we are not
    music_to_play = None
    

    def __init__(self, core):
        Process.__init__(self)
        self.core = core
        self.Init()
        

    def Init(self):
        """
        Init method for the main game.
        Stores common settings.
        """
        self.settings['screen_width'] = self.core.settings.screen_width
        self.settings['screen_height'] = self.core.settings.screen_height
        self.settings['full_screen'] = self.core.settings.full_screen
        self.settings['music_on'] = self.core.settings.music_on
        self.settings['sound_effects_on'] = self.core.settings.sound_effects_on
        self.settings['music_vol'] = self.core.settings.music_vol
        self.settings['sound_effects_vol'] = self.core.settings.sound_effects_vol
        self.settings['mouse_left_empty'] = self.core.settings.mouse_left_empty
        self.settings['bump_scroll'] = self.core.settings.bump_scroll
        self.settings['lock_drawing'] = self.core.settings.lock_drawing
        self.author_id = self.core.author_id
        self.load_player()

        # Debug display
        if DEBUG_SHOW_FPS:
            self.fps_text = Text(self.core.media.fonts["basic"], 0, 0, TEXT_ALIGN_TOP_LEFT, "blank")
            self.fps_text.colour = (0.0, 0.0, 0.0)
            self.fps_text.z = -2000
            
        self.manager = Puzzle_manager(self)
        self.gui = GUI(self)
        self.switch_game_state_to(GAME_STATE_LOGO)


    def Execute(self):
        """
        Execute method for the main game
        updates debug display
        """
        if DEBUG_SHOW_FPS:
            self.fps_text.text = "fps: " + str(self.core.current_fps)


    def save_player(self, player):
        """
        Player progress is saved in player.dat.
        It is all saved in a Player object. Pass the Player object into this to
        save it.
        """
        f = open(self.core.path_player_progress, "w+b")
        pickle.dump(player, f)
        f.close()


    def load_player(self):
        """
        Ran at the start of the game to load player progress.
        If the player.dat file doesn't exist the default state will be
        saved out instead.
        """
        try:
            f = open(self.core.path_player_progress, "r")
            self.player = pickle.load(f)
            f.close()
        except IOError:
            self.player = Player()
            self.save_player(self.player)
        

    def quit_game(self):
        """
        Immediately closes the game.
        """
        self.core.Quit()


    def switch_game_state_to(self, state, gui_state = None):
        """
        Pass in a state and this will switch to it.
        It will also clean up everying necessary to go out of the
        previous game state.
        """
        # Undo and destroy everything in the current state
        self.gui.destroy_current_gui_state()
        col = (1.0, 1.0, 1.0)
        if self.game_state == GAME_STATE_LOGO:
            col = (0, 0, 0)

        self.music_to_play = None
        
        # Switch to new state
        self.game_state = state

        # Create everything we require
        if state == GAME_STATE_LOGO:
            self.gui.switch_gui_state_to(GUI_STATE_LOGO if gui_state is None else gui_state)
        elif state == GAME_STATE_MENU:
            self.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL
            self.gui.fade_toggle(speed = 120, colour = col)
            self.gui.switch_gui_state_to(GUI_STATE_MENU if gui_state is None else gui_state)
            self.music_to_play = "title"
        elif state == GAME_STATE_PUZZLE:
            self.current_zoom_level = 1.0
            self.lives = INITIAL_LIVES
            self.timer = 0
            self.manager.load_puzzle(self.manager.current_puzzle_pack, self.manager.current_puzzle_file, user_created = self.manager.user_created_puzzles)
            #self.manager.load_puzzle("MarksAmezzinPuzzles0001", "Cat0001.puz")
            self.gui.fade_toggle(speed = 120)
            self.gui.switch_gui_state_to(GUI_STATE_PUZZLE if gui_state is None else gui_state)
            self.music_to_play = "puzzle"
        elif state == GAME_STATE_CATEGORY_SELECT:
            self.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL
            self.manager.user_created_puzzles = False
            self.gui.fade_toggle(speed = 60)
            self.gui.switch_gui_state_to(GUI_STATE_CATEGORY_SELECT if gui_state is None else gui_state)
            self.music_to_play = "select_puzzle"
        elif state == GAME_STATE_PUZZLE_SELECT:
            self.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL
            self.gui.fade_toggle(speed = 60)           
            self.gui.switch_gui_state_to(GUI_STATE_PUZZLE_SELECT if gui_state is None else gui_state)
            self.music_to_play = "select_puzzle"
        elif state == GAME_STATE_DESIGNER:
            self.manager.user_created_puzzles = True
            self.gui.fade_toggle(speed = 20, colour = col)
            self.gui.switch_gui_state_to(GUI_STATE_DESIGNER_PACKS if gui_state is None else gui_state)
            self.music_to_play = "editor"
        elif state == GAME_STATE_TEST:
            self.current_zoom_level = 1.0
            self.lives = INITIAL_LIVES
            self.timer = 0
            self.manager.load_puzzle(self.manager.current_puzzle_pack, self.manager.current_puzzle_file)
            self.gui.fade_toggle(speed = 120)
            self.gui.switch_gui_state_to(GUI_STATE_PUZZLE if gui_state is None else gui_state)
            self.music_to_play = "puzzle"
        elif state == GAME_STATE_SHARING:
            self.gui.fade_toggle(speed = 20)
            self.gui.switch_gui_state_to(GUI_STATE_SHARING_NEWEST if gui_state is None else gui_state)
            self.music_to_play = "select_puzzle"
        elif state == GAME_STATE_TUTORIAL:
            self.current_zoom_level = 1.0
            self.lives = INITIAL_LIVES
            self.timer = 0
            self.manager.load_puzzle(self.manager.current_puzzle_pack, self.manager.current_puzzle_file, user_created = False)
            self.gui.fade_toggle(speed = 120)
            self.gui.switch_gui_state_to(GUI_STATE_TUTORIAL if gui_state is None else gui_state)
            self.music_to_play = "puzzle"

        self.ensure_correct_music_playing()


    def ensure_correct_music_playing(self):
        if self.music_to_play is None:
            if not self.current_playing_music is None:
                self.core.media.music[self.current_playing_music].stop()
                self.current_playing_music = None
        elif self.core.settings.music_on:            
            if not self.music_to_play == self.current_playing_music:
                self.core.media.music[self.music_to_play].play_loop(1000)
                self.current_playing_music = self.music_to_play


    def fade_out_music(self, fade_out_time = 1000):
        if not self.current_playing_music is None:
            self.core.media.music[self.current_playing_music].stop(fade_out_time)
            self.current_playing_music = None


    def set_music_volume(self, volume):
        if not self.current_playing_music is None:
            self.core.media.music[self.current_playing_music].set_volume(volume)
        

    def player_action_cleared_puzzle(self, category_uuid, puzzle):
        # -----------
        # Save cleared puzzle and scores
        # -----------
        # create empty lists if not set
        if not category_uuid in self.player.cleared_puzzles:
            self.player.cleared_puzzles[category_uuid] = []
        if not category_uuid in self.player.puzzle_scores:
            self.player.puzzle_scores[category_uuid] = {}

        # Add to cleared lists and scores lists if necessary
        if not puzzle in self.player.cleared_puzzles[category_uuid]:
            self.player.cleared_puzzles[category_uuid].append(puzzle)

        if not puzzle in self.player.puzzle_scores[category_uuid]:
            self.player.puzzle_scores[category_uuid][puzzle] = [self.timer, self.lives]
        if self.timer < self.player.puzzle_scores[category_uuid][puzzle][0]:
            self.player.puzzle_scores[category_uuid][puzzle][0] = self.timer
        if self.lives > self.player.puzzle_scores[category_uuid][puzzle][1]:
            self.player.puzzle_scores[category_uuid][puzzle][1] = self.lives

        # Add category as being cleared if true
        if len(self.player.cleared_puzzles[category_uuid]) >= len(self.manager.current_pack.puzzles) and not category_uuid in self.player.cleared_categories:
            self.player.cleared_categories.append(category_uuid)

        # -----------
        # Handle category unlocking
        # -----------
        # Gather together how many puzzles we've finished
        num_puzzles_cleared = 0

        for cat_uuid in self.player.cleared_puzzles:
            # ignore the tutorial
            if cat_uuid == TUTORIAL_UUID:
                continue
            # we only count puzzles in the main 
            if not cat_uuid in self.game_category_uuids:
                continue
            for puzzle_name in self.player.cleared_puzzles[cat_uuid]:
                num_puzzles_cleared += 1
        
        # If we determine we should have more categories unlocked that we do
        # then we determine which category in the sequence we haven't unlocked and
        # tell the game to unlock it (this is for animation purposes only)
        # the + 2 is to take into account the default unlocks (tutorial and first category)
        if ((num_puzzles_cleared / PUZZLE_UNLOCK_THRESHOLD) + 2) > len(self.player.unlocked_categories):
            for puzzle_cat in self.game_categories:
                if not puzzle_cat in self.player.unlocked_categories:
                    self.player.unlocked_categories.append(puzzle_cat)
                    self.category_to_unlock = puzzle_cat
                    break
            
        # -----------
        # finalise
        # -----------
        self.save_player(self.player)
        self.manager.check_which_packs_starred()


    def rate_pack(self, pack_uuid, rating):
        # Set rating
        self.player.pack_ratings[pack_uuid] = int(rating)
        
        # finalise
        self.save_player(self.player)


    def report_pack(self, pack_uuid):
        # Remember
        self.player.packs_reported.append(pack_uuid)
        
        # finalise
        self.save_player(self.player)
        


class Player(object):
    """
    This object is responsible for the saved state of the player and
    their progess through the game.
    """
    def __init__(self):
        self.unlocked_categories = ["0001", "0002"]
        self.cleared_categories = []
        self.cleared_puzzles = {}
        self.saved_puzzles = {}
        self.puzzle_scores = {}
        self.pack_ratings = {}
        self.packs_reported = []
        self.first_run = True
        self.auto_save = False    
        self.sharing_content_warning_seen = False
        self.sharing_upload_content_agreed = False
        

Game(core)
