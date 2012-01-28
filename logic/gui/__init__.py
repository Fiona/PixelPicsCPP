"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
import sys, os

# Game engine imports
from core import *

# Game imports
from consts import *
from helpers  import *
from gui.logo import *
from gui.main_menu import *
from gui.puzzle import *
#from gui.designer import *



class Mouse(Process):
    """
    An instance is created and stored in the GUI object.
    """
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.z = Z_MOUSE


    def Execute(self):
        self.x = self.game.core.mouse.x
        self.y = self.game.core.mouse.y


    def get_screen_draw_position(self):
        return self.x, self.y

        

class GUI(Process):
    """ High level gui handler """
    # Current gui state
    gui_state = None
        
    # This is a dictionary of gui state names pointing to dictionaries of gui names poiting to gui elements visible in that state
    current_visible_gui_elements = {
        GUI_STATE_LOGO : {},
        GUI_STATE_MENU : {},
        GUI_STATE_PUZZLE : {},
        GUI_STATE_DESIGNER_PACKS : {},
        GUI_STATE_DESIGNER_PUZZLES : {},
        GUI_STATE_DESIGNER_DESIGNER : {}
        }

    # goes up every frame, resets when changing game state
    current_game_state_gui_ticks = 0

    # Points to the parent window which all GUI objects will sit in and recieve input from this, can change during game
    parent_window = None

    # Simple flag you can use to stop the player escaping for instance
    block_gui_keyboard_input = False

    # Simple flag you can use to stop any input to the gui taking place
    block_gui_mouse_input = False

    # Pointer to the mouse process
    mouse = None

    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.alpha = 1.0
        self.fading = 1.0
        self.fade_to = 0
        self.fading_done = False
        self.z = -5000
        self.priority = PRIORITY_GUI
        self.iter = 0

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_width = self.game.settings['screen_width']
        self.primitive_square_height = self.game.settings['screen_height']
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_colour = (0.0, 0.0, 0.0, 1.0)
        self.mouse = Mouse(self.game)


    def Execute(self):
        self.current_game_state_gui_ticks += 1

        # Handle the fading stuff
        if not self.fading == None and self.fading_done == False:
            self.iter += 1
            self.alpha = lerp(self.iter, self.fade_speed, self.fading, self.fade_to)
            if self.iter == self.fade_speed:
                self.alpha = self.fade_to
                self.fading = None
                self.fading_done = True
                self.iter = 0
                if not self.fading_callback == None:
                    self.fading_callback()

        # Colour of fade
        self.primitive_square_colour = (self.fade_colour[0], self.fade_colour[1], self.fade_colour[2], self.alpha)

        # Block input on fade
        if not self.fading == None and self.fading_done == False:
            return

        if self.game.game_state == GAME_STATE_LOGO:
            """
            LOGO SCREEN
            """
            if self.current_game_state_gui_ticks == 30:
                self.current_visible_gui_elements[GAME_STATE_LOGO]['stompyblondie_logo_text'] = Stompyblondie_Logo_Text(self.game)
                #self.game.play_sound_effect("stompyblondie")
            if self.current_game_state_gui_ticks == 120 or self.game.core.Keyboard_key_down(key.ESCAPE):
                self.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), colour = (0,0,0))

        elif self.game.game_state == GAME_STATE_MENU:
            """
            MAIN MENU
            """
            if not self.block_gui_keyboard_input:
                # Quit on escape
                if self.game.core.Keyboard_key_released(key.ESCAPE):
                    self.game.quit_game()
                    
        elif self.game.game_state == GAME_STATE_PUZZLE:
            """
            IN A PUZZLE
            """
            if not self.block_gui_keyboard_input:
                # Back to menu on escape
                if self.game.core.Keyboard_key_released(key.ESCAPE):
                    self.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 120)

            if not self.block_gui_mouse_input:
                self.do_mouse_wheel_zooming()
        """
        elif self.game.game_state == GAME_STATE_DESIGNER:
            """
        #IN DESINGER MODE
        """
            if self.gui_state == GUI_STATE_DESIGNER_DESIGNER:
                self.do_mouse_wheel_zooming()

        elif self.game.game_state == GAME_STATE_TEST:
            """
        #TESTING A PUZZLE
        """
            if not self.block_gui_mouse_input:
                self.do_mouse_wheel_zooming()
        """

        # sort out the current mouse image
        if not self.mouse.image is None:
            self.mouse.image = self.game.core.media.gfx['gui_cursor_' + str(self.game.cursor_tool_state)]

        # Handle overall gui input
        if not self.parent_window is None:
            mouse_over = self.parent_window.handle_input((self.mouse.x, self.mouse.y))
            if not mouse_over is None and not self.block_gui_mouse_input:

                if not mouse_over._currently_hovered:
                    mouse_over.mouse_enter()
                    mouse_over._currently_hovered = True

                mouse_over.mouse_over()

                if self.game.core.mouse.left_down:
                    mouse_over.mouse_left_down()
                elif self.game.core.mouse.left_up:
                    mouse_over.mouse_left_up()

                if self.game.core.mouse.right_down:
                    mouse_over.mouse_right_down()
                elif self.game.core.mouse.right_up:
                    mouse_over.mouse_right_up()

                if self.game.core.mouse.middle_down:
                    mouse_over.mouse_middle_down()
                elif self.game.core.mouse.middle_up:
                    mouse_over.mouse_middle_up()

                if self.game.core.mouse.wheel_down:
                    mouse_over.mouse_wheel_down()
                elif self.game.core.mouse.wheel_up:
                    mouse_over.mouse_wheel_up()



    def do_mouse_wheel_zooming(self):
        # Mouse wheel zooming
        if self.game.core.mouse.wheel_down:
            self.game.current_zoom_level *= 0.75
        if self.game.core.mouse.wheel_up:
            self.game.current_zoom_level *= 1.25

        # Adjust zoom level
        if self.game.current_zoom_level > 1.00:
            self.game.current_zoom_level = 1.00
        if self.game.current_zoom_level < self.game.minimum_zoom_level:
            self.game.current_zoom_level = self.game.minimum_zoom_level
        

    def switch_gui_state_to(self, state):
        if self.gui_state in [GUI_STATE_DESIGNER_PACKS, GUI_STATE_DESIGNER_PUZZLES, GUI_STATE_DESIGNER_DESIGNER]:
            self.destroy_current_gui_state()
        
        self.gui_state = state
        self.current_game_state_gui_ticks = 0
        self.parent_window = None
                                                  
        if self.gui_state == GUI_STATE_LOGO:
            self.mouse.alpha = 1.0
            self.mouse.z = Z_MOUSE
            self.mouse.image = None
            self.current_visible_gui_elements[GUI_STATE_LOGO]['stompyblondie_logo'] = Stompyblondie_Logo(self.game)
        if self.gui_state == GUI_STATE_MENU:
            self.mouse.alpha = 1.0
            self.mouse.image = self.game.core.media.gfx['gui_cursor_' + str(DRAWING_TOOL_STATE_NORMAL)]
            self.current_visible_gui_elements[GUI_STATE_MENU]['main_menu_container'] = GUI_main_menu_container(self.game)
            self.parent_window = self.current_visible_gui_elements[GUI_STATE_MENU]['main_menu_container']
        if self.gui_state == GUI_STATE_PUZZLE:
            self.mouse.image = self.game.core.media.gfx['gui_cursor_' + str(DRAWING_TOOL_STATE_NORMAL)]
            self.current_visible_gui_elements[GUI_STATE_PUZZLE]['puzzle_container'] = GUI_puzzle_container(self.game)
            self.parent_window = self.current_visible_gui_elements[GUI_STATE_PUZZLE]['puzzle_container']
        """
        if self.gui_state == GUI_STATE_DESIGNER_PACKS:
            self.current_visible_gui_elements[GUI_STATE_DESIGNER_PACKS]['designer_packs_container'] = GUI_designer_packs_container(self.game)
            self.parent_window = self.current_visible_gui_elements[GUI_STATE_DESIGNER_PACKS]['designer_packs_container']
        if self.gui_state == GUI_STATE_DESIGNER_PUZZLES:
            self.current_visible_gui_elements[GUI_STATE_DESIGNER_PUZZLES]['designer_puzzles_container'] = GUI_designer_puzzles_container(self.game)
            self.parent_window = self.current_visible_gui_elements[GUI_STATE_DESIGNER_PUZZLES]['designer_puzzles_container']
            self.fade_toggle(speed = 20, colour = (1.0, 1.0, 1.0))
        if self.gui_state == GUI_STATE_DESIGNER_DESIGNER:
            MyrmidonGame.engine['input'].mouse.alpha = 1.0
            MyrmidonGame.engine['input'].mouse.image = self.game.media.graphics['gui']['cursor_' + str(DRAWING_TOOL_STATE_NORMAL)]
            self.current_visible_gui_elements[GUI_STATE_DESIGNER_DESIGNER]['designer_designer_container'] = GUI_designer_designer_container(self.game)
            self.parent_window = self.current_visible_gui_elements[GUI_STATE_DESIGNER_DESIGNER]['designer_designer_container']
            self.fade_toggle(speed = 20, colour = (1.0, 1.0, 1.0))
            """


    def destroy_current_gui_state(self):
        if self.gui_state is None:
            return
        for x in self.current_visible_gui_elements[self.gui_state]:
            self.current_visible_gui_elements[self.gui_state][x].Kill()
        self.current_visible_gui_elements[self.gui_state] = {}


    fading = None
    fade_to = 0.0
    fade_speed = 15
    fade_colour = (0, 0, 0)
    fading_done = False
    fading_callback = None

    
    def fade_toggle(self, callback = None, speed = 15, colour = (1.0, 1.0, 1.0)):
        if not self.fading_done:
            return
        self.fade_speed = speed
        self.fading_callback = callback
        self.fading = self.alpha
        self.fade_colour = colour
        self.fade_to = 1.0 if self.fading < 1.0 else 0.0
        self.fading_done = False
