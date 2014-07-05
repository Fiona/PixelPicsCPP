"""
PixelPics - Nonograme game
Copyright (c) 2014 Stompy Blondie Games http://stompyblondie.com
"""

# python imports
import copy, random, math

# Game engine imports
from core import *

# Game imports
from consts import *
from helpers  import *
from gui.gui_elements import *
from gui.options import *
from solver import verify_puzzle, ContradictionException, AmbiguousException, GuessesExceededException
from gui.main_menu import GUI_main_menu_title_letter



class GUI_puzzle_title(GUI_element):

    title_state = 0
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.x = self.game.settings['screen_width'] / 2
        self.z = Z_GUI_OBJECT_LEVEL_4
        self.height = 300       
        self.life = 0
        self.dying = False
        

    def Execute(self):
        self.life += 1
        if self.dying:
            self.alpha -= .05
            for x in self.letters:
                x.alpha = self.alpha
            if self.alpha <= 0.0:
                self.Kill()


    def die(self):
        self.dying = True
        

    def get_screen_draw_position(self):
        return (self.x - (self.image.width / 2), self.y - (self.image.height / 2))


    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.letters:
            x.Kill()



class GUI_ready_title(GUI_puzzle_title):

    def __init__(self, game, parent = None):
        GUI_puzzle_title.__init__(self, game, parent)
        self.y = 200
        self.letters = []
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "R", -227, 0, 20))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "e_normal", -120, 3, 30))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "a", -10, 5, 40))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "d", 105, -3, 50))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "y", 215, 22, 60))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "?", 305, -3, 70))



class GUI_cleared_title(GUI_puzzle_title):

    def __init__(self, game, parent = None):
        GUI_puzzle_title.__init__(self, game, parent)
        self.y = 80
        self.letters = []
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "C", -305, 0, 20))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "l", -230, -2, 30))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "e_normal", -150, 4, 40))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "a", -40, 8, 50))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "r", 55, 10, 60))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "e_normal", 147, 4, 70))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "d", 255, 0, 80))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "!", 340, -2, 90))



class GUI_failed_title(GUI_puzzle_title):

    def __init__(self, game, parent = None):
        GUI_puzzle_title.__init__(self, game, parent)
        self.y = 150
        self.letters = []
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "F", -214, 0, 20))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "a", -109, 4, 30))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "i", -29, -6, 40))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "l", 21, -4, 50))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "e_normal", 101, 2, 60))
        self.letters.append(GUI_main_menu_title_letter(self.game, self, "d", 211, -4, 70))



class GUI_puzzle_container(GUI_element):
    """
    All elements in the puzzle player live inside this thing.
    """
    objs = []
    tool = DRAWING_TOOL_STATE_DRAW
    paused = False
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_CONTAINERS
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.objs = []
        self.game.paused = False
        self.create_puzzle_element()
        if not self.game.freemode:
            self.objs.append(Player_lives(self.game))
        self.objs.append(Timer(self.game))        

        self.pause_button = GUI_puzzle_pause_button(self.game, self)


    def Execute(self):
        GUI_element.Execute(self)
        if self.game.paused or not self.puzzle.state == PUZZLE_STATE_SOLVING:
            return
        for x in self.objs:
            x.show()
        if self.game.gui.mouse.x > self.game.settings['screen_width'] - 200 and \
           self.game.gui.mouse.x < self.game.settings['screen_width'] and \
           self.game.gui.mouse.y > self.game.settings['screen_height'] - 90 and \
           self.game.gui.mouse.y < self.game.settings['screen_height']:
            for x in self.objs:
                x.hide()
        

    def create_puzzle_element(self):
        self.puzzle = GUI_puzzle(self.game, self)


    def show_menu(self):
        self.game.paused = True
        self.menu = GUI_puzzle_pause_menu(self.game, self)        


    def On_Exit(self):
        GUI_element.On_Exit(self)
        if not self.pause_button is None:
            self.pause_button.Kill()
        for x in self.objs:
            x.Kill()



class GUI_puzzle_pause_button(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_7
        self.image = self.game.core.media.gfx['gui_button_puzzle_menu']
        self.gui_init()
        self.x = -16
        self.y = -16
        self.width = 105
        self.height = 105
        self.dying = False


    def Execute(self):
        if self.dying:
            self.alpha -= 0.05
            if self.alpha < 0:
                self.parent.pause_button = None
                self.Kill()
        else:
            self.update()
            

    def fade_and_die(self):
        self.dying = True


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.show_menu()



class GUI_puzzle_pause_menu(GUI_element):

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']

        GUI_puzzle_pause_menu_resume_button(self.game, self)
        GUI_puzzle_pause_menu_options_button(self.game, self)
        GUI_puzzle_pause_menu_stop_button(self.game, self)
        GUI_puzzle_pause_menu_restart_button(self.game, self)
        
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_colour = (0.0, 0.0, 0.0, .4)


    def Get_rid(self):
        self.game.paused = False
        self.Kill()


    def Restart_puzzle(self):
        if self.game.game_state == GAME_STATE_TEST:
            self.game.manager.reset_puzzle_state()
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_TEST), speed = 20)
        elif self.game.game_state == GAME_STATE_TUTORIAL:
            self.game.manager.reset_puzzle_state()
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_TUTORIAL), speed = 20)
        else:
            self.game.manager.reset_puzzle_state()
            self.game.manager.delete_current_puzzle_save()
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE), speed = 20)
            
        
    def Stop_playing(self):
        if self.game.game_state == GAME_STATE_TEST:
            self.game.gui.fade_toggle(self.parent.puzzle.back_to_designer, speed = 60)
        elif self.game.game_state == GAME_STATE_TUTORIAL:
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_CATEGORY_SELECT), speed = 60)
        else:            
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE_SELECT), speed = 60)
            self.game.manager.save_current_puzzle_state()
        self.Kill()



class GUI_puzzle_pause_menu_resume_button(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 6
        self.image = self.game.core.media.gfx['gui_menu_button_resume_game']
        self.x = (self.game.settings['screen_width'] / 2) - (self.image.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) - 112
        self.height = 54
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.Get_rid()



class GUI_puzzle_pause_menu_options_button(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 5
        self.image = self.game.core.media.gfx['gui_button_main_menu_options']
        self.x = (self.game.settings['screen_width'] / 2) - (self.image.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) - 64
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        GUI_options(self.game, self.parent)




class GUI_puzzle_pause_menu_restart_button(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 4

        self.image = self.game.core.media.gfx['gui_menu_button_restart_puzzle']

        if self.game.game_state == GAME_STATE_TUTORIAL:
            self.image = self.game.core.media.gfx['gui_menu_button_restart_tutorial']

        self.x = (self.game.settings['screen_width'] / 2) - (self.image.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) - 16
        self.height = 54
        
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.conf_box = GUI_element_confirmation_box(
            self.game,
            self,
            "Restart puzzle",
            ["This will restart the current puzzle from the beginning.", "Are you sure you wish to restart this puzzle?"],
            confirm_callback = self.parent.Restart_puzzle
            )



class GUI_puzzle_pause_menu_stop_button(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 3

        self.image = self.game.core.media.gfx['gui_menu_button_save_quit']

        if self.game.game_state == GAME_STATE_TEST:
            self.image = self.game.core.media.gfx['gui_menu_button_stop_testing']
        elif self.game.game_state == GAME_STATE_TUTORIAL:
            self.image = self.game.core.media.gfx['gui_menu_button_quit_tutorial']

        self.x = (self.game.settings['screen_width'] / 2) - (self.image.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) + 32
        self.height = 54
        
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.Stop_playing()



class GUI_puzzle(GUI_element):
    """
    The main puzzle grid. Draws it, creates texts and responds to mouse clicks.
    """
    hovered_column = -1
    hovered_row = -1
    last_hovered_cell = (None, None)
    last_state_set = "ignore"
    
    cell_marker_objs = {}
    title_text = None
    completed_image = None
    camera_pos = [0.0, 0.0]
    currently_panning = False
    remember_mouse_pos = (0,0)

    hint_alpha = 1.0
    objs = []
    text = None
    state = PUZZLE_STATE_READY_MESSAGE

    made_mistake = False
    
    puzzle_solver = None
    puzzle_solver_state = None

    fill_stack = []
    checked_fill_stack = []

    reset_drawing_all_blacks = True
    reset_drawing_all_whites = True
    black_chunks_to_redraw = []
    white_chunks_to_redraw = []

    black_squares_to_ignore = []
    white_squares_to_ignore = []

    markers_dont_die = False    

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent        
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_1

        self.reload_puzzle_display()
        self.reload_puzzle_background()
        
        # Init stuff
        self.objs = []
        self.additional_text = None
        self.wait_time = 0
        self.camera_pos = [0.0, 0.0]
        self.hint_alpha = 1.0

        self.x = 0
        self.y = 0
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']

        self.designer = False
        self.tutorial = False
        self.hide_hint_numbers = False
        self.marker_objs = []

        # --- DESIGNER ONLY ---
        if self.game.game_state == GAME_STATE_DESIGNER:
            self.state = PUZZLE_STATE_SOLVING
            self.designer = True
            self.puzzle_solver_state = True
        # --- DESIGNER ONLY ---
        if self.game.game_state == GAME_STATE_TUTORIAL:
            self.state = PUZZLE_STATE_SOLVING
            #self.tutorial = True
            self.hint_alpha = .1

        self.grid_width = float(PUZZLE_CELL_WIDTH * self.game.manager.current_puzzle.width)
        self.grid_height = float(PUZZLE_CELL_HEIGHT * self.game.manager.current_puzzle.height)

        self.black_chunks_to_redraw = []
        self.white_chunks_to_redraw = []
                
        self.adjust_gui_coords()
        self.adjust_text_hint_coords()

        self.camera_pos = [0.0, 0.0]

        self.anim_state = 0
        self.iter = 0

        self.shown_nameplate = False
        self.click_to_continue = False
        self.buttons_to_continue = False
        self.finished_special_puzzle = False
        self.made_mistake = False

        self.current_locked_row = None
        self.current_locked_col = None
               
        self.PUZZLE_VERIFIER_ITERATIONS = PUZZLE_VERIFIER_ITERATIONS

        # For unlockable special states
        self.init_starred_all = self.game.manager.all_main_packs_starred
        self.init_last_pack_unlocked = self.game.manager.last_pack_unlocked
        self.init_cleared_all_main_categories = self.game.manager.cleared_all_main_categories
        self.game.special_finish_state = None
        

    def reload_puzzle_background(self):
        # Draw strategy data
        self.parent.text_offset_x = 0.0
        self.parent.text_offset_y = 0.0
        if self.game.game_state == GAME_STATE_TUTORIAL:
            self.parent.draw_strategy = "tutorial_background"
        elif self.game.game_state == GAME_STATE_DESIGNER:
            self.parent.draw_strategy = "designer_background"
        else:
            self.parent.draw_strategy = "balloons_background"
            
        """
        if BACKGROUNDS[self.game.manager.current_puzzle.background]['type'] == BACKGROUND_TYPE_COLOUR:
            self.parent.draw_strategy = "primitive_square"
            self.parent.draw_strategy_call_parent = False
            self.parent.primitive_square_width = self.game.settings['screen_width']
            self.parent.primitive_square_height = self.game.settings['screen_height']
            self.parent.primitive_square_x = 0.0
            self.parent.primitive_square_y = 0.0
            self.parent.primitive_square_four_colours = True
            self.parent.primitive_square_colour = (
                BACKGROUNDS[self.game.manager.current_puzzle.background]['data'],
                BACKGROUNDS[self.game.manager.current_puzzle.background]['data'],
                (1.0,1.0,1.0,1.0),
                BACKGROUNDS[self.game.manager.current_puzzle.background]['data'],
                )
                """
        

    def Execute(self):
        self.draw_strategy_camera_x = self.camera_pos[0]
        self.draw_strategy_camera_y = self.camera_pos[1]
        self.draw_strategy_current_zoom_level = self.game.current_zoom_level
        self.reset_drawing_all_blacks = False
        self.reset_drawing_all_whites = False
        self.black_chunks_to_redraw = []
        self.white_chunks_to_redraw = []

        if not self.game.paused:
            self.parent.text_offset_x += 5.0
            self.parent.text_offset_y -= 5.0

        self.adjust_gui_coords()
        self.adjust_text_hint_coords()

        # ****************
        # PUZZLE_STATE - Ready message displaying
        # ****************
        if self.state == PUZZLE_STATE_READY_MESSAGE:
            self.game.gui.block_gui_mouse_input = True
            self.game.gui.block_gui_keyboard_input = True
            self.game.gui.mouse.alpha = 0.0
            if self.wait_time == 120:
                self.title_text = GUI_ready_title(self.game, self)
            if not self.title_text is None and self.title_text.life > 100:
                self.title_text.die()
                self.title_text = None
                self.game.gui.mouse.alpha = 1.0
                self.game.gui.block_gui_mouse_input = False
                self.game.gui.block_gui_keyboard_input = False
                self.state = PUZZLE_STATE_SOLVING

        # ****************
        # PUZZLE_STATE - Actually solving the puzzle, marking cells
        # ****************
        if self.state == PUZZLE_STATE_SOLVING:
            if not self.game.paused:
                self.game.timer+= 1
                if not self.game.game_state == GAME_STATE_TUTORIAL:
                    self.do_bump_scrolling()
                if not self.game.game_state in [GAME_STATE_TEST, GAME_STATE_TUTORIAL] and (self.game.timer % 30) == 0:
                    self.game.manager.save_current_puzzle_state()
                
            # --- DESIGNER ONLY ---            
            if self.game.game_state == GAME_STATE_DESIGNER:
                 if self.puzzle_solver_state is None:
                     if self.puzzle_solver is None:
                         self.puzzle_solver = verify_puzzle(self.game.manager.current_puzzle)
                     if self.game.core.current_fps < 50 and self.PUZZLE_VERIFIER_ITERATIONS > 10:
                         self.PUZZLE_VERIFIER_ITERATIONS -= 10
                     if self.game.core.current_fps > 50 and self.PUZZLE_VERIFIER_ITERATIONS < PUZZLE_VERIFIER_MAX_ITERATIONS:
                         self.PUZZLE_VERIFIER_ITERATIONS += 10
                     for i in xrange(self.PUZZLE_VERIFIER_ITERATIONS):
                         try:
                             self.puzzle_solver_state = self.puzzle_solver.next()
                         except (ContradictionException, AmbiguousException, GuessesExceededException) as e:
                             self.puzzle_solver_state = False
                             break
                         if self.puzzle_solver_state == True:
                             break
            # --- DESIGNER ONLY ---

            # --- DEBUG ONLY ---
            if DEBUG:
                if self.game.core.Keyboard_key_released(key.F11):
                    self.set_cleared()                    
            # --- DEBUG ONLY ---            


        # ****************
        # PUZZLE_STATE - Player has failed the puzzle, display message
        # ****************
        if self.state == PUZZLE_STATE_FAILED:
            if self.anim_state == 0:
                self.hovered_column = -1
                self.hovered_row = -1
                self.parent.pause_button.fade_and_die()

                if self.title_text is None and self.additional_text is None:
                    self.game.gui.block_gui_keyboard_input = True
                    self.game.gui.block_gui_mouse_input = True
                    self.game.gui.mouse.alpha = 0.0
                    self.title_text = GUI_failed_title(self.game, self)
                    self.game.puzzle_music_stop = True
                    if self.game.settings['cat_mode']:
                        self.game.core.media.sfx['catmode-failure'].play(0)
                    else:
                        self.game.core.media.sfx['failure'].play(0)
                    self.game.fade_out_music(250)
                    self.wait_time = 0
                    self.game.manager.delete_current_puzzle_save()

                self.anim_state = 1

            elif self.anim_state == 1:
                if self.hint_alpha > 0.0:
                    if self.iter < 120:
                        self.zoom_out_fade_and_position(self.iter, 120)
                        self.iter += 1
                else:
                    self.anim_state = 2
                    self.iter = 0
                    self.wait_time = 0
            elif self.anim_state == 2:
                if self.wait_time == 1:
                    self.game.gui.block_gui_mouse_input = False
                    self.game.gui.mouse.alpha = 1.0
                    self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL                    
                    self.objs.append(
                        Button_Retry_Puzzle(self.game, self)
                        )
                    self.objs.append(
                        Button_Select_Puzzle(self.game, self)
                        )
                    
        # ****************
        # PUZZLE_STATE - Puzzle has been cleared, display the coloured image and cleared message
        # ****************
        if self.state == PUZZLE_STATE_CLEARED:
            if self.anim_state == 0:
                self.hovered_column = -1
                self.hovered_row = -1
                self.parent.pause_button.fade_and_die()

                self.has_record = False
                if (not self.game.manager.current_pack.uuid in self.game.player.puzzle_scores or \
                    not self.game.manager.current_puzzle_file in self.game.player.puzzle_scores[self.game.manager.current_pack.uuid] or \
                    self.game.timer < self.game.player.puzzle_scores[self.game.manager.current_pack.uuid][self.game.manager.current_puzzle_file][0]):
                    self.has_record = True

                if self.title_text is None and self.additional_text is None:                    
                    self.game.gui.block_gui_keyboard_input = True
                    if not self.game.game_state == GAME_STATE_TUTORIAL:                    
                        self.game.gui.block_gui_mouse_input = True
                        self.game.gui.mouse.alpha = 0.0
                    self.title_text = GUI_cleared_title(self.game, self)
                    self.wait_time = 0
                    self.game.puzzle_music_stop = True
                    self.game.core.media.sfx['success'].play(0)
                    self.game.fade_out_music(250)
                self.anim_state = 1

            elif self.anim_state == 1:
                if self.hint_alpha > 0.0:
                    if self.iter < 100:
                        self.zoom_out_fade_and_position(self.iter, 100)
                        self.iter += 1
                else:
                    Finished_puzzle_image(self.game, self, self.grid_x, self.grid_y)
                    self.anim_state = 2
                    self.iter = 0

            elif self.anim_state == 2:
                if not self.click_to_continue and self.wait_time > 100:

                    if not self.shown_nameplate:
                        self.objs.append(
                                Puzzle_nameplate_text(
                                    self.game,
                                    self.game.settings['screen_width'] / 2,
                                    self.grid_gui_y + self.grid_gui_height + 40,
                                    str(self.game.manager.current_puzzle.name)
                                )
                            )
                        self.shown_nameplate = True

                    if (not self.game.game_state == GAME_STATE_TUTORIAL) and (not self.click_to_continue and not self.buttons_to_continue):
                        self.click_to_continue = False
                        self.buttons_to_continue = False

                        self.finished_special_puzzle = self.have_finished_special_puzzle()

                        # Special states show a click to continue instead of a next puzzle button
                        if self.finished_special_puzzle:
                            self.additional_text = Text(
                                self.game.core.media.fonts['puzzle_click_to_continue'],
                                self.game.settings['screen_width'] - 10,
                                self.game.settings['screen_height'] - 10,
                                TEXT_ALIGN_BOTTOM_RIGHT,
                                "Click to continue..."
                                )
                            self.additional_text.colour = (0.4, 0.4, 0.4)
                            self.additional_text.alpha = 0.0
                            self.additional_text.z = Z_GUI_OBJECT_LEVEL_4
                            self.objs.append(self.additional_text)
                            
                            self.click_to_continue = True
                            
                if self.wait_time == 150 and not self.game.game_state in [GAME_STATE_TEST, GAME_STATE_TUTORIAL]:
                    has_perfect = False

                    if self.game.lives == INITIAL_LIVES:
                        self.objs.append(
                            Puzzle_perfect_star(self.game, self)
                            )
                        has_perfect = True

                    if self.has_record:
                        self.objs.append(
                            Puzzle_record_clock(self.game, self, has_perfect = has_perfect)
                            )

                # Show two buttons to go to next puzzle if so
                if self.wait_time == 180 and not self.finished_special_puzzle:
                    self.game.gui.block_gui_mouse_input = False
                    self.game.gui.mouse.alpha = 1.0
                    self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL
                    if not self.game.game_state == GAME_STATE_TUTORIAL:
                        self.objs.append(
                            Button_Next_Puzzle(self.game, self)
                            )
                        self.objs.append(
                            Button_Select_Puzzle(self.game, self)
                            )
                        self.buttons_to_continue = True

                if self.wait_time > 200:
                    if not self.additional_text is None and self.additional_text.alpha < 1.0:
                        self.additional_text.alpha += 0.01
                    self.finish_cleared_anim()
                    
                if self.click_to_continue and self.game.core.mouse.left_up:
                    self.close_puzzle_cleanup()
                    self.close_puzzle()
            
        self.wait_time += 1
        self.update()


    def close_puzzle_cleanup(self):
        if self.game.game_state == GAME_STATE_TUTORIAL:
            self.game.player_action_cleared_puzzle(self.game.manager.current_pack.uuid, self.game.manager.current_puzzle_file)
        else:
            self.game.player_action_cleared_puzzle(self.game.manager.current_pack.uuid, self.game.manager.current_puzzle_file)
            self.game.manager.delete_current_puzzle_save()
        self.game.gui.block_gui_mouse_input = False
        self.game.gui.block_gui_keyboard_input = False
        

    def close_puzzle(self):
        if self.game.game_state == GAME_STATE_TEST:
            self.game.gui.fade_toggle(self.back_to_designer, speed = 60)
        elif self.game.game_state == GAME_STATE_TUTORIAL:
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_CATEGORY_SELECT), speed = 60)
        else:
            if self.game.special_finish_state in [SPECIAL_FINISH_OTHER, None]:
                self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE_SELECT), speed = 60)
            elif self.game.special_finish_state == SPECIAL_FINISH_LAST_PACK:
                self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_CATEGORY_SELECT), speed = 60)                
            elif self.game.special_finish_state == SPECIAL_FINISH_STARRED:
                self.game.gui.block_gui_mouse_input = False
                self.game.gui.mouse.alpha = 1.0
                self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL                                    
                GUI_element_dialog_box(
                    self.game,
                    self.parent,
                    "Wow!",
                    ["You've managed to get a star on every puzzle in PixelPics!", " ", "Have you tried any player-made puzzles from the", "'Extra Puzzles' section?"],
                    callback = lambda: self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 60)
                    )
            elif self.game.special_finish_state == SPECIAL_FINISH_CLEARED:
                self.game.gui.block_gui_mouse_input = False
                self.game.gui.mouse.alpha = 1.0
                self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL                                    
                GUI_element_dialog_box(
                    self.game,
                    self.parent,
                    "Wow!",
                    ["You've finished every puzzle in PixelPics! Amazing!", " ",
                     "How many puzzles have you earnt a star on?", "Can you get them all?"],
                    callback = lambda: self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 60)
                    )
                
        

    def go_next_puzzle(self):
        idx = self.game.manager.current_pack.order.index(self.game.manager.current_puzzle_file)
        self.game.manager.current_puzzle_file = self.game.manager.current_pack.order[idx+1]

        if self.game.manager.user_created_puzzles:
            save_path = self.game.core.path_saves_user_directory
        else:
            save_path = self.game.core.path_saves_game_directory
        
        if os.path.exists(os.path.join(save_path, self.game.manager.current_puzzle_pack + "_" + self.game.manager.current_puzzle_file + FILE_SAVES_EXTENSION)):
            self.game.manager.load_puzzle_state_from = self.game.manager.current_puzzle_pack + "_" + self.game.manager.current_puzzle_file + FILE_SAVES_EXTENSION
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE), speed = 40, stop_music = True)


    def have_finished_special_puzzle(self):
        # Playing in test mode is special
        if self.game.game_state == GAME_STATE_TEST:
            self.game.special_finish_state = SPECIAL_FINISH_OTHER
            return True
        
        # These special states only apply to built-in puzzles
        if not self.game.manager.user_created_puzzles:
            self.close_puzzle_cleanup()
            
            # If we have just, with that one, starred all the puzzles then it's special
            if not self.init_starred_all and self.game.manager.all_main_packs_starred:
                self.game.special_finish_state = SPECIAL_FINISH_STARRED
                return True

            # If we've finished all main puzzles
            if not self.init_cleared_all_main_categories and self.game.manager.cleared_all_main_categories:
                self.game.special_finish_state = SPECIAL_FINISH_CLEARED
                return True

            # If we've unlocked the final pack!
            if not self.init_last_pack_unlocked and self.game.manager.last_pack_unlocked:
                self.game.special_finish_state = SPECIAL_FINISH_LAST_PACK
                return True

            # If we've unlocked a category
            if not self.game.category_to_unlock is None:
                self.game.special_finish_state = SPECIAL_FINISH_UNLOCKED
                return True
            
        # If we're playing the last puzzle in a pack it's special
        idx = self.game.manager.current_pack.order.index(self.game.manager.current_puzzle_file)
        if len(self.game.manager.current_pack.puzzles) == idx+1:
            self.game.special_finish_state = SPECIAL_FINISH_OTHER
            return True

        # Not special
        return False


    def back_to_designer(self):
        self.game.manager.load_puzzle(self.game.manager.current_puzzle_pack, self.game.manager.current_puzzle_file, set_state = True)
        self.game.switch_game_state_to(GAME_STATE_DESIGNER, gui_state = GUI_STATE_DESIGNER_DESIGNER)
        

    def reload_puzzle_display(self):
        self.hint_alpha = 1.0
        
        self.grid_width = float(PUZZLE_CELL_WIDTH * self.game.manager.current_puzzle.width)
        self.grid_height = float(PUZZLE_CELL_HEIGHT * self.game.manager.current_puzzle.height)

        self.grid_x = 0
        self.grid_y = 0

        # display row hint numbers
        #for x in self.cell_marker_objs:
        #    self.cell_marker_objs[x].Kill()
        if not self.text is None:
            for x in self.text:
                for i in self.text[x]:
                    for j in i:
                        j.Kill()
        self.text = {'rows' : [], 'cols' : []}

        hint_alpha = 0.2 if self.game.game_state == GAME_STATE_TUTORIAL else 1.0
        shadow_hint_alpha = 0.1 if self.game.game_state == GAME_STATE_TUTORIAL else .5

        for row_num, number_list in enumerate(self.game.manager.current_puzzle.row_numbers):
            # --- DESIGNER ONLY ---
            if self.game.game_state == GAME_STATE_DESIGNER:
                continue
            # --- DESIGNER ONLY ---
            self.text['rows'].append([])
            for index, number in enumerate(number_list[::-1]):
                text = Text(self.game.core.media.fonts['puzzle_hint_numbers'], 0, 0, TEXT_ALIGN_TOP_LEFT, str(number))
                col = PUZZLE_HINT_COMPLETED_COLOUR if number_list == (0,) else PUZZLE_HINT_COLOUR
                text.colour = (col[0], col[1], col[2], hint_alpha)
                text.shadow = 2
                text.shadow_colour = (.5, .5, .5, shadow_hint_alpha)
                text.generate_mipmaps = True
                text.z = Z_GUI_OBJECT_LEVEL_5
                self.text['rows'][row_num].append(text)

        # column
        for col_num, number_list in enumerate(self.game.manager.current_puzzle.column_numbers):
            # --- DESIGNER ONLY ---
            if self.game.game_state == GAME_STATE_DESIGNER:
                continue
            # --- DESIGNER ONLY ---
            self.text['cols'].append([])
            for index, number in enumerate(number_list[::-1]):
                text = Text(self.game.core.media.fonts['puzzle_hint_numbers'], 0, 0, TEXT_ALIGN_TOP_LEFT, str(number))
                col = PUZZLE_HINT_COMPLETED_COLOUR if number_list == (0,) else PUZZLE_HINT_COLOUR
                text.colour = (col[0], col[1], col[2], hint_alpha)
                text.shadow = 2
                text.shadow_colour = (.5, .5, .5, shadow_hint_alpha)
                text.generate_mipmaps = True
                text.z = Z_GUI_OBJECT_LEVEL_5
                self.text['cols'][col_num].append(text)

        # Brute force checking line completion because lazy
        if not self.game.game_state == GAME_STATE_DESIGNER:
            for i in range(self.game.manager.current_puzzle.width):
                for j in range(self.game.manager.current_puzzle.height):
                    self.check_line_completion(j, i)
       
        # Determine optimum zoom level
        self.hint_number_lengths_row = max(map(len, self.game.manager.current_puzzle.row_numbers)) + 2
        self.row_number_width = self.hint_number_lengths_row * PUZZLE_CELL_WIDTH
        
        self.hint_number_lengths_column = max(map(len, self.game.manager.current_puzzle.column_numbers)) + 2
        self.column_number_height = self.hint_number_lengths_column * PUZZLE_CELL_HEIGHT

        self.game.current_zoom_level = min(
            float(self.game.settings['screen_width']) / (self.grid_width + self.row_number_width),
            float(self.game.settings['screen_height']) / (self.grid_height + self.column_number_height)
            )

        if self.game.current_zoom_level > 1.0:
            self.game.current_zoom_level = 1.0
        self.game.minimum_zoom_level = self.game.current_zoom_level

        # --- DESIGNER ONLY ---
        if self.game.game_state == GAME_STATE_DESIGNER:
            self.game.minimum_zoom_level /= 2
        # --- DESIGNER ONLY ---

        # Work out initial placement of the grid
        self.grid_x = int(self.row_number_width - ((self.row_number_width + self.grid_width) / 2) - PUZZLE_CELL_WIDTH)
        self.grid_y = int(self.column_number_height - ((self.column_number_height + self.grid_height) / 2) - PUZZLE_CELL_HEIGHT)
        
        # Reset the drawing
        self.draw_strategy_reset_vectors = True
        self.reset_drawing_blacks()
        self.reset_drawing_whites()

        self.draw_strategy = "puzzle"
        self.draw_strategy_screen_width = self.game.settings['screen_width']
        self.draw_strategy_screen_height = self.game.settings['screen_height']
        self.draw_strategy_camera_x = self.camera_pos[0]
        self.draw_strategy_camera_y = self.camera_pos[1]
        self.draw_strategy_current_zoom_level = self.game.current_zoom_level
        self.draw_strategy_current_puzzle_width = self.game.manager.current_puzzle.width
        self.draw_strategy_current_puzzle_height = self.game.manager.current_puzzle.height
        self.draw_strategy_current_puzzle_state = self.game.manager.current_puzzle_state
        self.draw_strategy_reset_hint_gradients = False
        self.draw_strategy_tutorial_row_highlight = -1
        self.draw_strategy_tutorial_col_highlight = -1

        self.display_rectangle_marker = False
        self.rectangle_marker_top_left = (0, 0)
        self.rectangle_marker_bottom_right = (0, 0)

        

    def zoom_out_fade_and_position(self, num, target):
        self.hint_alpha = lerp(num, target, self.hint_alpha, 0.0)
        for x in self.text:
            for i in self.text[x]:
                for j in i:
                    j.alpha = self.hint_alpha

        for x in self.parent.objs:
            x.alpha = self.hint_alpha

        self.draw_strategy_reset_hint_gradients = True
        
        self.camera_pos[0] = lerp(num, target, self.camera_pos[0], 0.0)
        self.camera_pos[1] = lerp(num, target, self.camera_pos[1], 0.0)

        self.grid_x = int(lerp(num, target, self.grid_x, -(self.grid_width/2)))
        self.grid_y = int(lerp(num, target, self.grid_y, -(self.grid_height/2)))

        self.game.current_zoom_level = lerp(num, target, self.game.current_zoom_level, self.game.minimum_zoom_level)


    def adjust_gui_coords(self):
        # Adjust my x/y
        self.grid_gui_x = ((self.grid_x - self.camera_pos[0]) * self.game.current_zoom_level) + (self.game.settings['screen_width'] / 2)
        self.grid_gui_y = ((self.grid_y - self.camera_pos[1]) * self.game.current_zoom_level) + (self.game.settings['screen_height'] / 2)

        # Adjust my size
        self.grid_gui_width = self.grid_width * self.game.current_zoom_level
        self.grid_gui_height = self.grid_height * self.game.current_zoom_level


    def adjust_text_hint_coords(self):
        hint_alpha = 0.0 if self.hide_hint_numbers else 1.0
        if self.game.paused:
            hint_alpha = 0.0
            
        # Don't even ask about this, it works, alright?
        for row_num, number_list in enumerate(self.text['rows']):
            grid_x = self.grid_gui_x
            if self.hovered_row > -1 and row_num == self.hovered_row:
                if self.grid_gui_x - (((len(self.game.manager.current_puzzle.row_numbers[row_num]) * PUZZLE_CELL_WIDTH)) * self.game.current_zoom_level) < 0:
                    grid_x = (PUZZLE_CELL_WIDTH * len(self.game.manager.current_puzzle.row_numbers[row_num])) * self.game.current_zoom_level
                    if grid_x > self.game.gui.mouse.x:
                        grid_x = self.grid_gui_x
                            
            for index, text in enumerate(number_list):
                if self.state == PUZZLE_STATE_SOLVING:
                    text.alpha = 1.0 if self.draw_strategy_tutorial_row_highlight == row_num else hint_alpha
                text.x = grid_x - (((PUZZLE_CELL_WIDTH * index) + (PUZZLE_CELL_WIDTH / 2)) * self.game.current_zoom_level) - ((text.text_width/2) * self.game.current_zoom_level)
                text.y = self.grid_gui_y + (((PUZZLE_CELL_HEIGHT * row_num) + (PUZZLE_CELL_HEIGHT / 2)) * self.game.current_zoom_level) - ((text.text_height/2) * self.game.current_zoom_level)
                text.scale = self.game.current_zoom_level
                if grid_x == self.grid_gui_x:
                    text.z = Z_GUI_OBJECT_LEVEL_5
                else:
                    text.z = Z_GUI_OBJECT_LEVEL_7

        for col_num, number_list in enumerate(self.text['cols']):
            grid_y = self.grid_gui_y                
            if self.hovered_column > -1 and col_num == self.hovered_column:
                if self.grid_gui_y - (((len(self.game.manager.current_puzzle.column_numbers[col_num]) * PUZZLE_CELL_HEIGHT)) * self.game.current_zoom_level) < 0:
                    grid_y = (PUZZLE_CELL_HEIGHT * len(self.game.manager.current_puzzle.column_numbers[col_num])) * self.game.current_zoom_level
                    if grid_y > self.game.gui.mouse.y:
                        grid_y = self.grid_gui_y
                            
            for index, text in enumerate(number_list):
                if self.state == PUZZLE_STATE_SOLVING:
                    text.alpha = 1.0 if self.draw_strategy_tutorial_col_highlight == col_num else hint_alpha
                text.x = self.grid_gui_x + (((PUZZLE_CELL_WIDTH * col_num) + (PUZZLE_CELL_WIDTH / 2)) * self.game.current_zoom_level) - ((text.text_width/2) * self.game.current_zoom_level)
                text.y = grid_y - (((PUZZLE_CELL_HEIGHT * index) + (PUZZLE_CELL_HEIGHT / 2)) * self.game.current_zoom_level) - ((text.text_height/2) * self.game.current_zoom_level)
                text.scale = self.game.current_zoom_level
                if grid_y == self.grid_gui_y:
                    text.z = Z_GUI_OBJECT_LEVEL_5
                else:
                    text.z = Z_GUI_OBJECT_LEVEL_7


    def do_bump_scrolling(self):
        # Early exit if middle click panning
        if self.currently_panning:
            return

        # Keyboard key scrolling
        diff = [0, 0]
        
        if self.game.core.Keyboard_key_down(key.LEFT):
            diff[0] += BUMP_SCROLL_SPEED
        if self.game.core.Keyboard_key_down(key.RIGHT):
            diff[0] -= BUMP_SCROLL_SPEED
        if self.game.core.Keyboard_key_down(key.UP):
            diff[1] += BUMP_SCROLL_SPEED
        if self.game.core.Keyboard_key_down(key.DOWN):
            diff[1] -= BUMP_SCROLL_SPEED
            
        self.adjust_camera_pos(diff[0], diff[1])

        # All bump scrolling below here
        if not self.game.settings['bump_scroll']:
            return

        diff = [0, 0]
        
        if self.game.gui.mouse.x < BUMP_SCROLL_BORDER_WIDTH:
            diff[0] += BUMP_SCROLL_SPEED
        if self.game.gui.mouse.x > self.game.settings['screen_width'] - BUMP_SCROLL_BORDER_WIDTH:
            diff[0] -= BUMP_SCROLL_SPEED
        if self.game.gui.mouse.y < BUMP_SCROLL_BORDER_WIDTH:
            diff[1] += BUMP_SCROLL_SPEED
        if self.game.gui.mouse.y > self.game.settings['screen_height'] - BUMP_SCROLL_BORDER_WIDTH:
            diff[1] -= BUMP_SCROLL_SPEED
            
        self.adjust_camera_pos(diff[0], diff[1])
        

    def mouse_over(self):
        if not self.state == PUZZLE_STATE_SOLVING or self.currently_panning:
            return

        self.remember_mouse_pos = (self.game.gui.mouse.x, self.game.gui.mouse.y)

        if self.game.gui.mouse.x > self.grid_gui_x and \
               self.game.gui.mouse.x < self.grid_gui_x + self.grid_gui_width and \
               self.game.gui.mouse.y > self.grid_gui_y and \
               self.game.gui.mouse.y < self.grid_gui_y + self.grid_gui_height:
            self.last_hovered_cell = (self.hovered_row, self.hovered_column)
            self.game.cursor_tool_state = self.parent.tool
            mouse_x = self.game.gui.mouse.x - self.grid_gui_x 
            mouse_y = self.game.gui.mouse.y - self.grid_gui_y
            self.hovered_column = int(mouse_x / (PUZZLE_CELL_WIDTH * self.game.current_zoom_level))
            self.hovered_row = int(mouse_y / (PUZZLE_CELL_HEIGHT  * self.game.current_zoom_level))
        else:
            self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL
            self.last_hovered_cell = (self.hovered_row, self.hovered_column)
            self.hovered_column = -1
            self.hovered_row = -1
            self.last_state_set = "ignore"
            self.made_mistake = False
            self.current_locked_row = None
            self.current_locked_col = None

            if self.parent.tool == DRAWING_TOOL_STATE_RECTANGLE:
                self.display_rectangle_marker = False

        if self.parent.tool == DRAWING_TOOL_STATE_RECTANGLE and self.display_rectangle_marker:
            if -1 in self.rectangle_marker_top_left or  -1 in self.rectangle_marker_bottom_right:
                self.display_rectangle_marker = False
            else:
                self.rectangle_marker_bottom_right = (self.hovered_row, self.hovered_column)
            

    def mouse_left_down(self):
        if self.game.settings['mouse_left_empty']:
            self.default_mouse_left_down()
        else:
            self.default_mouse_right_down()


    def default_mouse_left_down(self):
        if not self.state == PUZZLE_STATE_SOLVING or self.currently_panning:
            return
        
        if self.parent.tool == DRAWING_TOOL_STATE_RECTANGLE and not self.display_rectangle_marker:
            self.display_rectangle_marker = True
            self.rectangle_marker_top_left = (self.hovered_row, self.hovered_column)
            self.rectangle_marker_bottom_right = (self.hovered_row, self.hovered_column)

        if not self.parent.tool == DRAWING_TOOL_STATE_DRAW:
            return

        if self.made_mistake:
            return

        if self.last_state_set == "ignore" or not self.last_hovered_cell == (self.hovered_row, self.hovered_column):
            # --- DESIGNER ONLY ---
            if self.game.game_state == GAME_STATE_DESIGNER:
                self.mark_cell(True, (self.hovered_row, self.hovered_column))
            # --- DESIGNER ONLY ---
            else:
                self.mark_cell(False, (self.hovered_row, self.hovered_column))
                

    def mouse_right_down(self):
        if self.game.settings['mouse_left_empty']:
            self.default_mouse_right_down()
        else:
            self.default_mouse_left_down()


    def default_mouse_right_down(self):
        if not self.state == PUZZLE_STATE_SOLVING or self.currently_panning:
            return

        if self.made_mistake:
            return

        if self.parent.tool == DRAWING_TOOL_STATE_RECTANGLE and not self.display_rectangle_marker:
            self.display_rectangle_marker = True
            self.rectangle_marker_top_left = (self.hovered_row, self.hovered_column)
            self.rectangle_marker_bottom_right = (self.hovered_row, self.hovered_column)

        if not self.parent.tool == DRAWING_TOOL_STATE_DRAW:
            return

        if self.game.settings['lock_drawing']:
            if self.current_locked_row is None and self.current_locked_col is None:
                if self.last_hovered_cell[0] != self.hovered_row:
                    self.current_locked_col = self.hovered_column
                elif self.last_hovered_cell[1] != self.hovered_column:
                    self.current_locked_row = self.hovered_row
            else:
                if not self.current_locked_row is None and not self.hovered_row == self.current_locked_row:
                    return
                if not self.current_locked_col is None and not self.hovered_column == self.current_locked_col:
                    return
        
        if self.last_state_set == "ignore" or not self.last_hovered_cell == (self.hovered_row, self.hovered_column):
            self.mark_cell(True, (self.hovered_row, self.hovered_column))


    def mouse_left_up(self):
        if self.game.settings['mouse_left_empty']:
            self.default_mouse_left_up()
        else:
            self.default_mouse_right_up()


    def default_mouse_left_up(self):
        if not self.state == PUZZLE_STATE_SOLVING or self.currently_panning:
            return

        if self.game.settings['cat_mode']:
            self.game.core.media.sfx['catmode-empty_square'].stop()

        self.made_mistake = False
        
        if self.parent.tool == DRAWING_TOOL_STATE_FILL:
            cell_list = []
            self.checked_fill_stack = []
            self.fill_stack = [(self.hovered_row, self.hovered_column)]
            while self.fill_at(True, cell_list):
                pass
            if len(cell_list) > 0:
                self.parent.need_to_save = True        
                self.change_cells(cell_list, True)

        elif self.parent.tool == DRAWING_TOOL_STATE_RECTANGLE:
            self.draw_rectangle(True, self.rectangle_marker_top_left, self.rectangle_marker_bottom_right)
            self.display_rectangle_marker = False
        
        self.last_state_set = "ignore"


    def mouse_right_up(self):
        if self.game.settings['mouse_left_empty']:
            self.default_mouse_right_up()
        else:
            self.default_mouse_left_up()


    def default_mouse_right_up(self):
        if not self.state == PUZZLE_STATE_SOLVING or self.currently_panning:
            return

        self.current_locked_row = None
        self.current_locked_col = None
        self.made_mistake = False

        if self.parent.tool == DRAWING_TOOL_STATE_FILL:
            cell_list = []
            self.checked_fill_stack = []
            self.fill_stack = [(self.hovered_row, self.hovered_column)]
            while self.fill_at(None, cell_list):
                pass
            if len(cell_list) > 0:
                self.parent.need_to_save = True        
                self.change_cells(cell_list, None)

        elif self.parent.tool == DRAWING_TOOL_STATE_RECTANGLE:
            self.draw_rectangle(None, self.rectangle_marker_top_left, self.rectangle_marker_bottom_right)
            self.display_rectangle_marker = False
        
        self.last_state_set = "ignore"


    def mouse_middle_down(self):
        if not self.state == PUZZLE_STATE_SOLVING:
            return
        if self.game.game_state == GAME_STATE_TUTORIAL:
            return

        #diff = (self.game.gui.mouse.x - self.remember_mouse_pos[0], self.game.gui.mouse.y - self.remember_mouse_pos[1])
        #self.adjust_camera_pos(diff[0], diff[1])
        self.adjust_camera_pos(-self.game.core.mouse.x_rel, -self.game.core.mouse.y_rel)

        self.currently_panning = True
        self.game.gui.mouse.alpha = 0.0
        self.game.core.mouse.set_pos(int(self.remember_mouse_pos[0]), int(self.remember_mouse_pos[1]))
        

    def mouse_middle_up(self):
        if not self.state == PUZZLE_STATE_SOLVING:
            return

        self.remember_mouse_pos = (0, 0)
        self.currently_panning = False
        self.game.gui.mouse.alpha = 1.0


    def fill_at(self, value, cell_list):
        cell = self.fill_stack.pop()
        
        if -1 in cell or self.game.manager.current_puzzle_state[cell[0]][cell[1]] == value or cell in self.checked_fill_stack:
            return len(self.fill_stack) > 0
        
        self.checked_fill_stack.append(cell)
        cell_list.append(cell)

        surrounding_cells = [
            (cell[0] - 1, cell[1]),
            (cell[0] + 1, cell[1]),
            (cell[0], cell[1] - 1),
            (cell[0], cell[1] + 1)
            ]

        for cell_check in surrounding_cells:
            if cell_check in self.checked_fill_stack:
                continue
            if cell_check[0] < 0 or cell_check[1] < 0:
                self.checked_fill_stack.append(cell_check)
                continue
            if cell_check[0] < len(self.game.manager.current_puzzle_state) and cell_check[1] < len(self.game.manager.current_puzzle_state[cell_check[0]]):
                self.fill_stack.append(cell_check)

        return len(self.fill_stack) > 0


    def draw_rectangle(self, value, top_left, bottom_right):
        if -1 in top_left or -1 in bottom_right:
            return
        cell_list = []
        for y in range(top_left[0], bottom_right[0] + 1):
            for x in range(top_left[1], bottom_right[1] + 1):
                cell_list.append((y, x))
        if len(cell_list) > 0:
            self.change_cells(cell_list, value)
        

    def adjust_camera_pos(self, x, y):
        self.camera_pos[0] -= x
        self.camera_pos[1] -= y
        
        if self.camera_pos[0] < -((self.grid_width + self.row_number_width) / 2):
            self.camera_pos[0] = -((self.grid_width + self.row_number_width) / 2)
        if self.camera_pos[0] > (self.grid_width + self.row_number_width) / 2:
            self.camera_pos[0] = (self.grid_width + self.row_number_width) / 2
            
        if self.camera_pos[1] < -((self.grid_height + self.column_number_height) / 2):
            self.camera_pos[1] = -((self.grid_height + self.column_number_height) / 2)
        if self.camera_pos[1] > (self.grid_height + self.column_number_height) / 2:
            self.camera_pos[1] = (self.grid_height + self.column_number_height) / 2


    def change_cells(self, cells, to):
        undo_data = []
        redo_data = []
        for x in cells:
            undo_data.append((x[0], x[1], self.game.manager.current_puzzle_state[x[0]][x[1]]))
            redo_data.append((x[0], x[1], to))
        self.do_change_cells(redo_data)
        # --- DESIGNER ONLY ---
        if self.game.game_state == GAME_STATE_DESIGNER:
            self.parent.add_new_action((self.do_change_cells, undo_data, redo_data))
        # --- DESIGNER ONLY ---

        
    def do_change_cells(self, data):
        for cell in data:
            self.game.manager.current_puzzle_state[cell[0]][cell[1]] = cell[2]
            # --- DESIGNER ONLY ---
            if self.game.game_state == GAME_STATE_DESIGNER:
                self.game.manager.set_puzzle_cell(
                    self.game.manager.current_puzzle,
                    cell[1], cell[0],
                    self.game.manager.current_puzzle_state[cell[0]][cell[1]],
                    colour = [0.0, 0.0, 0.0] if self.game.manager.current_puzzle_state[cell[0]][cell[1]] else [0.0, 0.0, 1.0])
            # --- DESIGNER ONLY ---
                
            self.reset_drawing_blacks((cell[0], cell[1]))
            self.reset_drawing_whites((cell[0], cell[1]))

        if self.game.game_state in [GAME_STATE_PUZZLE, GAME_STATE_TEST, GAME_STATE_TUTORIAL]:
            self.check_line_completion(cell[0], cell[1])
            if self.game.manager.is_current_puzzle_complete():
                self.set_cleared()
        # --- DESIGNER ONLY ---
        elif self.game.game_state == GAME_STATE_DESIGNER:
            self.game.manager.work_out_puzzle_hint_numbers(self.game.manager.current_puzzle)
            self.puzzle_solver_state = None
            if not self.puzzle_solver is None:
                del(self.puzzle_solver)
            self.puzzle_solver = None
        # --- DESIGNER ONLY ---


    def mark_cell(self, state, cell, skip_animation = False):
        if -1 in cell:
            return

        # --- DESIGNER ONLY ---
        if self.game.game_state == GAME_STATE_DESIGNER:
            if state == False:
                return
            self.parent.need_to_save = True        
        # --- DESIGNER ONLY ---

        # If we're not in freemode and we've already put a black in, we can't shift it.
        if not self.game.game_state == GAME_STATE_DESIGNER and not self.game.freemode and self.game.manager.current_puzzle_state[cell[0]][cell[1]]:
            return

        if self.game.manager.current_puzzle_state[cell[0]][cell[1]] is None:
            if not self.last_state_set == "ignore" and not self.last_state_set == state:
                return
            
            self.last_state_set = state
            self.change_cells([(cell[0], cell[1])], state)
            self.cell_marker_objs[(cell[0], cell[1])] = Puzzle_marker(self.game, self, cell[0], cell[1], state, skip_animation)
        else:
            if not self.last_state_set == "ignore" and not self.last_state_set == None:
                return

            if self.game.manager.current_puzzle_state[cell[0]][cell[1]] == True:
                Puzzle_marker(self.game, self, cell[0], cell[1], True, skip_animation, dying = True)
                self.reset_drawing_blacks((cell[0], cell[1]))
            else:                
                Puzzle_marker(self.game, self, cell[0], cell[1], False, skip_animation, dying = True)
                self.reset_drawing_whites((cell[0], cell[1]))

            self.last_state_set = None
            self.change_cells([(cell[0], cell[1])], None)

        # If not in freemode and we've just put a black in and it doesn't go there then we've messed up.
        # We have to undo the move.
        if not self.game.freemode and self.game.manager.current_puzzle_state[cell[0]][cell[1]] and not self.game.manager.current_puzzle.cells[cell[0]][cell[1]][0]:
            self.cell_marker_objs[(cell[0], cell[1])].incorrect()
            self.reset_drawing_whites((cell[0], cell[1]))
            self.change_cells([(cell[0], cell[1])], False)
            self.cell_marker_objs[cell] = Puzzle_marker(self.game, self, cell[0], cell[1], False, skip_animation)
            self.game.lives -= 1
            self.made_mistake = True
            if self.game.lives <= 0:
                self.state = PUZZLE_STATE_FAILED
            self.game.core.media.sfx['incorrect_square'].play(0)
            return

        # play sound effect on drawing
        if self.last_state_set is True:
            self.game.core.media.sfx['fill_square'].play(0)
        elif self.last_state_set is False:
            if self.game.settings['cat_mode']:
                self.game.core.media.sfx['catmode-empty_square'].play(-1)
            else:
                self.game.core.media.sfx['empty_square'].play(0)


    def check_line_completion(self, row_index, column_index):
        ##########################
        # ROW CHECKING
        ##########################
        # First check if the entire row is finished and colour appropriately
        row_complete = self.game.manager.check_row_completion(row_index)
        if row_complete:
            col = PUZZLE_HINT_COMPLETED_COLOUR
        else:
            col = PUZZLE_HINT_COLOUR
            
        for text in self.text['rows'][row_index]:
            text.colour = col

        # If the line isn't complete then we check each cell along the row comparing them to the solution hints
        if not row_complete:

            # Check left to right, then right to left
            row_numbers = self.game.manager.current_puzzle.row_numbers[row_index]
            left_to_right = True
            for iteration_list in [enumerate(self.game.manager.current_puzzle.cells[row_index]), reverse_enumerate(self.game.manager.current_puzzle.cells[row_index])]:
                
                # If starting from the left, we're dealing with the last text object drawn
                # and we check till we get to the far right of the row
                if left_to_right:
                    text_num = len(row_numbers) - 1
                    col_end = len(self.game.manager.current_puzzle.cells[row_index]) - 1
                # If starting from the right, we're dealing with the first text object drawn
                # and we check till we get to the start of the row
                else:
                    text_num = 0
                    col_end = 0

                # count_num keeps track of how many times we find a filled in square
                count_num = 0

                # For every column index and current cell value in this row.
                for col, cell in iteration_list:

                    # If the cell is filled in then we keep track of that
                    if self.game.manager.current_puzzle_state[row_index][col]:
                        count_num += 1

                    # If we're at the end (or start if going right to left) or we've come across a cell that isn't filled in
                    # then we can check if the current number of filled in cells matches the current hint number we're checking
                    if (col == col_end or not self.game.manager.current_puzzle_state[row_index][col]):

                        # If it does match the current hint number, then colour the relevant hint
                        if self.game.manager.current_puzzle.row_numbers[row_index][len(row_numbers) - 1 - text_num] == count_num:
                            self.text['rows'][row_index][text_num].colour = PUZZLE_HINT_COMPLETED_COLOUR

                            # Increment or decrement the hint number we're checking. If we become out of bounds we're finished with this row
                            if left_to_right:
                                text_num -= 1
                                if text_num < 0:
                                    break
                            else:
                                text_num += 1
                                if text_num > len(row_numbers) - 1:
                                    break

                        # If we don't match and we've found matching blocks, then we've come across a big contradiction and nothing else in this
                        # row is relevant.
                        elif count_num > 0:
                            break

                        # Reset the count of the number of blocks we're checking. We're on to a new hint now.
                        count_num = 0

                    # If we find a blank square, then there's no point contining to check this row.
                    if self.game.manager.current_puzzle_state[row_index][col] is None:
                        break

                # After checking all the rows from left to right, we flip and do the other direction
                left_to_right = not left_to_right

            # If the total cells filled is more than the total number of cells in this row then something is very wrong and we reset the colours
            # of every hint
            total_num = 0
            row_is_messed_up = True
            for cell in self.game.manager.current_puzzle_state[row_index]:
                if cell:
                    total_num += 1
                # If we've filled the entire line and the "check_row_completion" was inconclusive
                # then we can assume that something royally messed up and so the entire row will be marked as unsolved.
                if cell is None:
                    row_is_messed_up = False
                    
            if row_is_messed_up or total_num > sum(self.game.manager.current_puzzle.row_numbers[row_index]):
                for text in self.text['rows'][row_index]:
                    text.colour = PUZZLE_HINT_COLOUR

        ##########################
        # COLUMNS CHECKING
        ##########################
        # First check if the entire column is finished and colour appropriately
        column_complete = self.game.manager.check_column_completion(column_index)
        if column_complete:
            col = PUZZLE_HINT_COMPLETED_COLOUR
        else:
            col = PUZZLE_HINT_COLOUR

        for text in self.text['cols'][column_index]:
            text.colour = col
        
        # If the line isn't complete then we check column cells as we checked the row before
        if not column_complete:

            # Check top to bottom, then bottom to top            
            column_cells = self.game.manager.get_column_cells(self.game.manager.current_puzzle, column_index)            
            column_numbers = self.game.manager.current_puzzle.column_numbers[column_index]
            top_to_bottom = True
            for iteration_list in [enumerate(column_cells), reverse_enumerate(column_cells)]:
                
                # If starting from top, we're dealing with the last text object drawn
                # and we check till we get to the bottom
                if top_to_bottom:
                    text_num = len(column_numbers) - 1
                    row_end = len(column_cells) - 1
                # If starting from bottom, we're dealing with the first text object drawn
                # and we check till we get to the start of the column
                else:
                    text_num = 0
                    row_end = 0
                    
                # count_num keeps track of how many times we find a filled in square
                count_num = 0

                # For every row index and current cell value in this row.
                for row, cell in iteration_list:

                    # If the cell is filled in then we keep track of that                    
                    if self.game.manager.current_puzzle_state[row][column_index]:
                        count_num += 1

                    # If we're at the end (or start if going bottom to top) or we've come across a cell that isn't filled in
                    # then we can check if the current number of filled in cells matches the current hint number we're checking
                    if (row == row_end or not self.game.manager.current_puzzle_state[row][column_index]):

                        # If it does match the current hint number, then colour the relevant hint                        
                        if self.game.manager.current_puzzle.column_numbers[column_index][len(column_numbers) - 1 - text_num] == count_num:
                            self.text['cols'][column_index][text_num].colour = PUZZLE_HINT_COMPLETED_COLOUR

                            # Increment or decrement the hint number we're checking. If we become out of bounds we're finished with this column
                            if top_to_bottom:
                                text_num -= 1
                                if text_num < 0:
                                    break                                
                            else:
                                text_num += 1
                                if text_num > len(column_numbers) - 1:
                                    break

                        # If we don't match and we've found matching blocks, then we've come across a big contradiction and nothing else in this
                        # column is relevant.
                        elif count_num > 0:
                            break
                                
                        # Reset the count of the number of blocks we're checking. We're on to a new hint now.
                        count_num = 0

                    # If we find a blank square, then there's no point contining to check this column.                            
                    if self.game.manager.current_puzzle_state[row][column_index] is None:
                        break
                    
                # After checking all the rows from top to bottom, we flip and do the other direction
                top_to_bottom = not top_to_bottom

            # If the total cells filled is more than the total number of cells in this column then something is very wrong and we reset the colours
            # of every hint
            total_num = 0
            column_is_messed_up = True
            for row, cell in enumerate(column_cells):
                if self.game.manager.current_puzzle_state[row][column_index]:
                    total_num += 1
                # If we've filled the entire line and the "check_row_completion" was inconclusive
                # then we can assume that something royally messed up and so the entire col will be marked as unsolved.
                if self.game.manager.current_puzzle_state[row][column_index] is None:
                    column_is_messed_up = False
                    
            if column_is_messed_up or total_num > sum(self.game.manager.current_puzzle.column_numbers[column_index]):
                for text in self.text['cols'][column_index]:
                    text.colour = PUZZLE_HINT_COLOUR


    def reset_drawing_blacks(self, cell = None):
        if cell is None:
            self.reset_drawing_all_blacks = True
        elif not (cell[0] / PUZZLE_RENDER_CHUNK_SIZE, cell[1] / PUZZLE_RENDER_CHUNK_SIZE) in self.black_chunks_to_redraw:
            self.black_chunks_to_redraw.append((cell[0] / PUZZLE_RENDER_CHUNK_SIZE, cell[1] / PUZZLE_RENDER_CHUNK_SIZE))


    def reset_drawing_whites(self, cell = None):
        if cell is None:
            self.reset_drawing_all_whites = True
        elif not (cell[0] / PUZZLE_RENDER_CHUNK_SIZE, cell[1] / PUZZLE_RENDER_CHUNK_SIZE) in self.white_chunks_to_redraw:
            self.white_chunks_to_redraw.append((cell[0] / PUZZLE_RENDER_CHUNK_SIZE, cell[1] / PUZZLE_RENDER_CHUNK_SIZE))


    def set_cleared(self):
        self.state = PUZZLE_STATE_CLEARED


    def finish_cleared_anim(self):
        pass


    def kill_all_visible_markers(self):
        it_changes_during_the_iteration = copy.copy(self.cell_marker_objs)
        for x in it_changes_during_the_iteration:
            self.cell_marker_objs[x].Kill()
        self.cell_marker_objs = {}


    def On_Exit(self):        
        GUI_element.On_Exit(self)
        for x in self.cell_marker_objs:
            self.cell_marker_objs[x].Kill()
        for x in self.text:
            for i in self.text[x]:
                for j in i:
                    j.Kill()
        if not self.title_text is None:
            self.title_text.Kill()
        for x in self.objs:
            x.Kill()
            

    
class Puzzle_marker(Process):
    
    dying = False
    is_incorrect = False
    
    def __init__(self, game, puzzle, row, col, state, skip_animation, dying = False):
        Process.__init__(self)
        self.game = game
        self.puzzle = puzzle
        self.row = row
        self.col = col
        self.state = state
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.priority = PRIORITY_MARKERS
        if self.game.game_state == GAME_STATE_DESIGNER:
            self.image = self.game.core.media.gfx['gui_puzzle_cell_black_designer']
        else:
            self.image = self.game.core.media.gfx['gui_puzzle_cell_white' if not state else 'gui_puzzle_cell_black']
        self.rem_img = self.image
        self.dying = dying
        self.is_incorrect = False
        self.incorrect_y_movement = 0
        self.custom_scale = 1.0

        if skip_animation:
            if self.state:
                self.puzzle.reset_drawing_blacks((row, col))
            else:
                self.puzzle.reset_drawing_whites((row, col))
            self.Kill()
            return

        self.marker_state = 0
        self.iter = 0
        
        if self.dying:
            if self.state:
                self.puzzle.reset_drawing_blacks((row, col))
            else:
                self.puzzle.reset_drawing_whites((row, col))
            self.alpha = 1.0
        else:
            if self.state:
                self.puzzle.black_squares_to_ignore.append((row, col))
            else:
                self.puzzle.white_squares_to_ignore.append((row, col))
                
            self.alpha = 0.0
            self.marker_state = 1

        self.update_pos()
        

    def Execute(self):
        if self.marker_state == 1:
            self.iter += 1
            self.alpha = lerp(self.iter, 10, self.alpha, 1.0)
            if self.iter > 10:
                if self.state:
                    self.puzzle.black_squares_to_ignore.remove((self.row, self.col))
                else:
                    self.puzzle.white_squares_to_ignore.remove((self.row, self.col))
                self.marker_state = 0
                self.iter = 0
            else:
                self.update_pos()
                return

        if self.is_incorrect:
            self.colour = (1.0, 0, 0)
            self.z = Z_GUI_OBJECT_LEVEL_3
            self.flash = 0

            self.iter += 1
            self.alpha = lerp(self.iter, 120, self.alpha, 0.0)
            self.incorrect_y_movement = lerp(self.iter, 120, self.incorrect_y_movement, self.image.height/2)
            self.flash += 1
            if self.flash == 10:
                self.flash = 0
            self.image = None if self.flash >= 5 else self.rem_img

            if self.iter > 120:
                self.Kill()
                return

        elif self.dying:
            self.iter += 1
            self.alpha = lerp(self.iter, 10, self.alpha, 0.0)
            if self.iter > 10:
                self.Kill()
                return
        else:
            if self.state:
                self.puzzle.reset_drawing_blacks((self.row, self.col))
            else:
                self.puzzle.reset_drawing_whites((self.row, self.col))
            if not self.puzzle.markers_dont_die:
                self.Kill()

        self.update_pos()


    def incorrect(self):
        self.is_incorrect = True
    

    def update_pos(self):
        self.scale = self.custom_scale * self.game.current_zoom_level
        self.x = self.puzzle.grid_gui_x + ((self.col * PUZZLE_CELL_WIDTH) * self.game.current_zoom_level)
        self.y = self.puzzle.grid_gui_y + ((self.incorrect_y_movement + (self.row * PUZZLE_CELL_HEIGHT)) * self.game.current_zoom_level)


    def get_screen_draw_position(self):
        return self.x, self.y


    def On_Exit(self):
        if (self.row, self.col) in self.puzzle.cell_marker_objs:
            del(self.puzzle.cell_marker_objs[(self.row, self.col)])
        if self.state:
            if (self.row, self.col) in self.puzzle.black_squares_to_ignore:
                self.puzzle.black_squares_to_ignore.remove((self.row, self.col))
            self.puzzle.reset_drawing_blacks((self.row, self.col))                
        else:
            if (self.row, self.col) in self.puzzle.white_squares_to_ignore:
                self.puzzle.white_squares_to_ignore.remove((self.row, self.col))
            self.puzzle.reset_drawing_whites((self.row, self.col))
    
    

class Puzzle_pixel_message(Pixel_message):

    def __init__(self, game, x, y, z = Z_GUI_OBJECT_LEVEL_9, wait = 3):
        Pixel_message.__init__(self, game, x, y, z, wait)
        
        self.draw_strategy = "puzzle_pixel_message"
        self.draw_strategy_screen_width = self.game.settings['screen_width']



class Title_ready(Puzzle_pixel_message):
    pattern = [
        " XXX                      ",
        "X   X            X     XXX",
        "X   X            X       X",
        "X XX  XXX XXX  XXX X X  X ",
        "X  X  XX  X X  X X X X    ",
        "X   X XXX XXXX XXX  XX  X ",
        "                   XX     "
        ]
    


class Title_cleared(Puzzle_pixel_message):
    pattern = [
        " XXX                          ",
        "X   X X                    X X",
        "X     X                    X X",
        "X     X XXX XXX   XX XXX XXX X",
        "X   X X XX  X X  X   XX  X X  ",
        " XXX  X XXX XXXX X   XXX XXX X"
        ]




class Title_failed(Puzzle_pixel_message):
    pattern = [
        " XXXX                 ",
        "X            X       X",
        "X            X       X",
        "XXXX  XXX  X X XXX XXX",
        "X     X X  X X XX  X X",
        "X     XXXX X X XXX XXX"
        ]



class Finished_puzzle_image(Puzzle_image):
    def set_position_z_scale(self, x, y):
        self.x = (x * self.game.current_zoom_level) + (self.game.settings['screen_width'] / 2)
        self.y = (y * self.game.current_zoom_level) + (self.game.settings['screen_height'] / 2)
        self.z = Z_GUI_OBJECT_LEVEL_4
        self.scale = PUZZLE_CELL_WIDTH * self.game.minimum_zoom_level


class Puzzle_nameplate_text(Process):
    def __init__(self, game, x, y, text):
        Process.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.z = Z_GUI_OBJECT_LEVEL_7
        self.text = Text(
            self.game.core.media.fonts['puzzle_message'],
            self.x,
            self.y,
            TEXT_ALIGN_CENTER,
            text,
            )
        self.text.colour = (0.95, 0.58, 0.09)
        self.text.shadow = 2
        self.text.shadow_colour = (.5, .5, .5, .5)
        self.text.alpha = 0.0
        
        self.text.z = self.z - 5
        self.do_fade = True
        self.iter = 0
        self.alpha = 0.0

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_width = self.text.text_width + 40.0
        self.primitive_square_height = self.text.text_height + 6.0
        self.primitive_square_x = self.x - (self.text.text_width/2) - 20.0
        self.primitive_square_y = self.y - (self.text.text_height/2) - 2.0
        self.primitive_square_colour = (1.0, 1.0, 1.0, 0.0)
        

    def Execute(self):
        if self.do_fade == False:
            return
        self.iter += 1
        self.alpha = lerp(self.iter, 60, 0.0, 1.0)
        self.text.alpha = self.alpha
        colour_alpha = lerp(self.iter, 60, 0.0, .6)
        self.primitive_square_colour = (1.0, 1.0, 1.0, colour_alpha)
        if self.iter > 60:
            self.do_fade = False


    def On_Exit(self):
        self.text.Kill()



class Player_lives(Process):
    lives_objs = []
    current_lives = 0
    
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.z = Z_GUI_OBJECT_LEVEL_6        
        self.current_lives = self.game.lives
        self.lives_objs = []
        for x in range(self.game.lives):
            self.lives_objs.append(Player_lives_life(self.game, x))
        self.lives_objs[self.game.lives-1].current = True
        self.alpha = 1.0

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_x = self.game.settings['screen_width'] - 200.0
        self.primitive_square_y = self.game.settings['screen_height'] - 55.0
        self.primitive_square_width = 200.0
        self.primitive_square_height = 55.0
        self.primitive_square_colour = (1.0, 1.0, 1.0, 0.5)


    def Execute(self):
        if self.game.lives < self.current_lives:
            self.lives_objs[self.current_lives - 1].die()
            del(self.lives_objs[self.current_lives - 1])
            if len(self.lives_objs):
                self.lives_objs[self.game.lives - 1].current = True
        self.current_lives = self.game.lives

        self.primitive_square_colour = (1.0, 1.0, 1.0, self.alpha - .5)
        for x in self.lives_objs:
            x.alpha = self.alpha


    def show(self):
        self.draw_strategy = "primitive_square"
        self.alpha = 1.0
        
        
    def hide(self):
        self.draw_strategy = ""
        self.alpha = 0.0


    def get_screen_draw_position(self):
        return self.x, self.y


    def On_Exit(self):
        for x in self.lives_objs:
            x.Kill()



class Player_lives_life(Process):
    current = False
    scale_dir = True
    dying = False
    def __init__(self, game, num):
        Process.__init__(self)
        self.game = game
        self.num = num
        self.image = self.game.core.media.gfx['gui_heart']
        self.x = self.game.settings['screen_width'] - ((40 * (num + 1)) + 32)
        self.y = self.game.settings['screen_height'] - 60
        self.z = Z_GUI_OBJECT_LEVEL_6 - 1
        self.scale_pos = (float(self.image.width / 2), float(self.image.height / 2))
        self.scale = .6
        self.dying = False
        self.iter = 0
        

    def Execute(self):
        if self.dying:
            self.iter += 1
            self.y = lerp(self.iter, 120, self.init_y, self.init_y + 30)
            self.alpha = lerp(self.iter, 120, 1.0, 0.0)
            if self.iter > 120:
                self.Kill()

        elif self.current:
            self.iter += 1
            self.scale = lerp(self.iter, 60, .6 if self.scale_dir else .8, .8 if self.scale_dir else .6)
            if self.iter > 60:
                self.iter = 0
                self.scale_dir = not self.scale_dir                


    def get_screen_draw_position(self):
        return self.x, self.y

    
    def die(self):
        self.dying = True
        self.init_y = self.y
        self.image_sequence = 2
        self.scale = .6



class Timer(Process):
    
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.z = Z_GUI_OBJECT_LEVEL_6            
        self.text = Text(self.game.core.media.fonts['puzzle_timer'], self.game.settings['screen_width'] - 40, self.game.settings['screen_height'] - 62, TEXT_ALIGN_CENTER_RIGHT, "00:00:00")
        self.text.colour = (0.95, 0.58, 0.09)
        self.text.shadow = 1
        self.text.shadow_colour = (.6, .6, .6, .5)
        self.text.z = self.z - 1
        self.alpha = 1.0

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_x = self.game.settings['screen_width'] - 200.0
        self.primitive_square_y = self.game.settings['screen_height'] - 82.0
        self.primitive_square_width = 200.0
        self.primitive_square_height = 27.0
        self.primitive_square_colour = (1.0, 1.0, 1.0, .5)


    def Execute(self):
        if self.game.timer == 0:
            self.text.text = "00:00:00"
        else:
            seconds = int(self.game.timer / 60)
            minutes = int(seconds / 60)
            hours = int(minutes / 60)
            
            seconds = seconds - (minutes * 60)
            minutes = minutes - (hours * 60)
                
            self.text.text = str(hours).rjust(2, "0") + ":" + str(minutes).rjust(2, "0") + ":" + str(seconds).rjust(2, "0")

        self.primitive_square_colour = (1.0, 1.0, 1.0, self.alpha - .5)            
        self.text.alpha = self.alpha
        
            
    def show(self):
        self.draw_strategy = "primitive_square"
        self.alpha = 1.0
        
        
    def hide(self):
        self.draw_strategy = ""
        self.alpha = 0.0
        

    def get_screen_draw_position(self):
        return self.x, self.y


    def On_Exit(self):
        self.text.Kill()



class Puzzle_perfect_star(Process):
    def __init__(self, game, parent = False):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_6            
        self.image = self.game.core.media.gfx['gui_category_complete_star']
        self.x = 64
        self.y = self.game.settings['screen_height'] - (self.image.height / 2)
        self.scale = 0.0
        
        self.state = 0
        self.iter = 0
        self.text = None


    def Execute(self):
        if self.state == 0:
            self.scale = lerp(self.iter, 30, 0, 1.2)
            self.iter += 1
            if self.scale >= 1.1:
                self.state = 1
                self.iter = 0
        elif self.state == 1:
            if self.iter < 15:
                self.scale = lerp(self.iter, 15, 1.2, 1.0)
                self.iter += 1
            else:
                self.scale = 1.0
                self.state = 2
                self.iter = 0
                self.text = Text(
                    self.game.core.media.fonts['puzzle_special_icons'],
                    self.x + ((self.image.width / 2) - 15),
                    self.y,
                    TEXT_ALIGN_CENTER_LEFT,
                    "Perfect!"
                    )
                self.text.colour = (0.95, 0.58, 0.09)
                self.text.shadow = 2
                self.text.shadow_colour = (.5, .5, .5, .5)
                self.text.alpha = 0.0
                self.text.z = self.z - 2
        elif self.state == 2:
            if self.text.alpha < 1.0:
                self.text.alpha += .05
            

    def On_Exit(self):
        if not self.text is None:
            self.text.Kill()


    def get_screen_draw_position(self):
        return (
            self.x - ((self.image.width * self.scale) / 2),
            self.y - ((self.image.height * self.scale) / 2)
            )



class Puzzle_record_clock(Process):
    def __init__(self, game, parent, has_perfect = True):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.has_perfect = has_perfect
        self.z = Z_GUI_OBJECT_LEVEL_6 - 2         
        self.image = self.game.core.media.gfx['gui_puzzle_record_clock']
        self.x = 64
        self.y = self.game.settings['screen_height'] - (self.image.height / 2)
        self.scale = 0.0

        self.waiting = False
        
        if self.has_perfect:
            self.y -= 90
            self.waiting = True
        
        self.state = 0
        self.iter = 0
        self.text = None


    def Execute(self):
        if self.state == 0:
            if self.waiting:
                self.iter += 1
                if self.iter == 40:
                    self.iter = 0
                    self.waiting = False
                return
            self.scale = lerp(self.iter, 30, 0, 1.2)
            self.iter += 1
            if self.scale >= 1.1:
                self.state = 1
                self.iter = 0
        elif self.state == 1:
            if self.iter < 15:
                self.scale = lerp(self.iter, 15, 1.2, 1.0)
                self.iter += 1
            else:
                self.scale = 1.0
                self.state = 2
                self.iter = 0
                self.text = Text(
                    self.game.core.media.fonts['puzzle_special_icons'],
                    self.x + ((self.image.width / 2) - 15),
                    self.y,
                    TEXT_ALIGN_CENTER_LEFT,
                    "Record!"
                    )
                self.text.colour = (0.95, 0.58, 0.09)
                self.text.shadow = 2
                self.text.shadow_colour = (.5, .5, .5, .5)
                self.text.alpha = 0.0
                self.text.z = self.z - 2
        elif self.state == 2:
            if self.text.alpha < 1.0:
                self.text.alpha += .05
        

    def On_Exit(self):
        if not self.text is None:
            self.text.Kill()


    def get_screen_draw_position(self):
        return (
            self.x - ((self.image.width * self.scale) / 2),
            self.y - ((self.image.height * self.scale) / 2)
            )



class Button_Next_Puzzle(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_7
        self.image = self.game.core.media.gfx['gui_button_next_puzzle']
        self.gui_init()
        self.x = self.game.settings['screen_width'] - self.image.width + 32
        self.y = self.game.settings['screen_height'] - self.image.height + 16
        self.width = 200
        self.height = 90
        self.alpha = 0.0
        self.wait_to_display = 50
        

    def Execute(self):
        self.update()
        self.wait_to_display -= 1
        if self.wait_to_display > 0:
            return
        if self.alpha < 1.0:
            self.alpha += .05
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.go_next_puzzle()



class Button_Select_Puzzle(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_7
        self.image = self.game.core.media.gfx['gui_button_select_puzzle']
        self.x = 32
        self.y = 32
        self.width = 100
        self.height = 100
        self.gui_init()
        self.alpha = 0.0
        self.wait_to_display = 50
        

    def Execute(self):
        self.update()
        self.wait_to_display -= 1
        if self.wait_to_display > 0:
            return
        if self.alpha < 1.0:
            self.alpha += .05
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.close_puzzle_cleanup()
        self.parent.close_puzzle()



class Button_Retry_Puzzle(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = Z_GUI_OBJECT_LEVEL_7
        self.image = self.game.core.media.gfx['gui_button_retry_puzzle']
        self.gui_init()
        self.x = self.game.settings['screen_width'] - self.image.width + 32
        self.y = self.game.settings['screen_height'] - self.image.height + 16
        self.width = 200
        self.height = 90
        self.alpha = 0.0
        self.wait_to_display = 50
        

    def Execute(self):
        self.update()
        self.wait_to_display -= 1
        if self.wait_to_display > 0:
            return
        if self.alpha < 1.0:
            self.alpha += .05
            

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.game.game_state == GAME_STATE_TEST:
            self.game.manager.reset_puzzle_state()
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_TEST), speed = 20)
        elif self.game.game_state == GAME_STATE_TUTORIAL:
            self.game.manager.reset_puzzle_state()
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_TUTORIAL), speed = 20)
        else:
            self.game.manager.reset_puzzle_state()
            self.game.manager.delete_current_puzzle_save()
            self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_PUZZLE), speed = 20)
