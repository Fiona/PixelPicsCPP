"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
import sys, os

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
        'full_screen' : 1
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
    
    # Self explanitory object pointers and lists
    fps_text = None
    gui = None
    manager = None

    # Stuff we need to keep track of
    current_zoom_level = 1.0
    minimum_zoom_level = 1.0


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

        # Switch to new state
        self.game_state = state

        # Create everything we require
        if state == GAME_STATE_LOGO:
            self.gui.switch_gui_state_to(GUI_STATE_LOGO if gui_state is None else gui_state)
        elif state == GAME_STATE_MENU:
            self.gui.fade_toggle(speed = 120, colour = col)
            self.gui.switch_gui_state_to(GUI_STATE_MENU if gui_state is None else gui_state)
        elif state == GAME_STATE_PUZZLE:
            self.current_zoom_level = 1.0
            self.lives = INITIAL_LIVES
            self.timer = 0
            #self.manager.load_puzzle("MarksAmezzinPuzzles0001", "Cat0001.puz")
            #self.manager.load_puzzle("testfree0001", "forty0001.puz")
            self.manager.load_puzzle("test0001", "seven0001.puz")
            self.gui.fade_toggle(speed = 120)
            self.gui.switch_gui_state_to(GUI_STATE_PUZZLE if gui_state is None else gui_state)
        elif state == GAME_STATE_DESIGNER:
            self.gui.fade_toggle(speed = 20, colour = col)
            self.gui.switch_gui_state_to(GUI_STATE_DESIGNER_PACKS if gui_state is None else gui_state)
        elif state == GAME_STATE_TEST:
            self.current_zoom_level = 1.0
            self.lives = INITIAL_LIVES
            self.timer = 0
            self.manager.load_puzzle(self.manager.current_puzzle_pack, self.manager.current_puzzle_file)
            self.gui.fade_toggle(speed = 120)
            self.gui.switch_gui_state_to(GUI_STATE_PUZZLE if gui_state is None else gui_state)


Game(core)
