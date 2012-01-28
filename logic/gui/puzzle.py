"""
PixelPics - Nonograme game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
import copy, random, math

# Game engine imports
from core import *

# Game imports
from consts import *
from helpers  import *
from gui.gui_elements import *
#from solver import verify_puzzle, ContradictionException, AmbiguousException, GuessesExceededException



class GUI_puzzle_container(GUI_element):
    """
    All elements in the puzzle player live inside this thing.
    """
    objs = []
    tool = DRAWING_TOOL_STATE_DRAW
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.z = Z_GUI_CONTAINERS
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.objs = []
        
        GUI_puzzle(self.game, self)
        if not self.game.freemode:
            self.objs.append(Player_lives(self.game))
        self.objs.append(Timer(self.game))

        # Draw strat
        if BACKGROUNDS[self.game.manager.current_puzzle.background]['type'] == BACKGROUND_TYPE_COLOUR:
            self.draw_strategy = "primitive_square"
            self.draw_strategy_call_parent = False
            self.primitive_square_width = self.width
            self.primitive_square_height = self.height
            self.primitive_square_x = 0.0
            self.primitive_square_y = 0.0
            self.primitive_square_four_colours = True
            self.primitive_square_colour = (
                BACKGROUNDS[self.game.manager.current_puzzle.background]['data'],
                (1.0,1.0,1.0,1.0),
                (1.0,1.0,1.0,1.0),
                BACKGROUNDS[self.game.manager.current_puzzle.background]['data'],
                )


    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.objs:
            x.Kill()



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

    puzzle_solver = None
    puzzle_solver_state = None

    fill_stack = []
    checked_fill_stack = []

    black_squares_to_ignore = []
    white_squares_to_ignore = []

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent        
        self.gui_init()
        self.z = Z_GUI_OBJECT_LEVEL_1

        self.reload_puzzle_display()
        
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

        # --- DESIGNER ONLY ---
        if self.game.game_state == GAME_STATE_DESIGNER:
            self.state = PUZZLE_STATE_SOLVING
        # --- DESIGNER ONLY ---

        self.grid_width = float(PUZZLE_CELL_WIDTH * self.game.manager.current_puzzle.width)
        self.grid_height = float(PUZZLE_CELL_HEIGHT * self.game.manager.current_puzzle.height)

        self.grid_x = 0
        self.grid_y = 0

        self.draw_strategy = "puzzle"
        self.draw_strategy_screen_width = self.game.settings['screen_width']
        self.draw_strategy_screen_height = self.game.settings['screen_height']
        self.draw_strategy_camera_x = self.camera_pos[0]
        self.draw_strategy_camera_y = self.camera_pos[1]
        self.draw_strategy_current_zoom_level = self.game.current_zoom_level
        self.draw_strategy_current_puzzle_width = self.game.manager.current_puzzle.width
        self.draw_strategy_current_puzzle_height = self.game.manager.current_puzzle.height

    def Execute(self):
        self.draw_strategy_camera_x = self.camera_pos[0]
        self.draw_strategy_camera_y = self.camera_pos[1]
        self.draw_strategy_current_zoom_level = self.game.current_zoom_level

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
                self.title_text = Title_ready(self.game, 0, 100, wait = 1)
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
            self.game.timer += 1

            # --- DESIGNER ONLY ---
            if self.game.game_state == GAME_STATE_DESIGNER:
                 if self.puzzle_solver_state is None:
                     if self.puzzle_solver is None:
                         self.puzzle_solver = verify_puzzle(self.game.manager.current_puzzle)
                     for i in xrange(PUZZLE_VERIFIER_ITERATIONS):
                         try:
                             self.puzzle_solver_state = self.puzzle_solver.next()
                         except (ContradictionException, AmbiguousException, GuessesExceededException) as e:
                             self.puzzle_solver_state = False
                             break
                         if self.puzzle_solver_state == True:
                             break
            # --- DESIGNER ONLY ---

        self.wait_time += 1
        self.update()


    def back_to_designer(self):
        self.game.manager.load_puzzle(self.game.manager.current_puzzle_pack, self.game.manager.current_puzzle_file, set_state = True)
        self.game.switch_game_state_to(GAME_STATE_DESIGNER, gui_state = GUI_STATE_DESIGNER_DESIGNER)
        

    def reload_puzzle_display(self):
        self.grid_width = float(PUZZLE_CELL_WIDTH * self.game.manager.current_puzzle.width)
        self.grid_height = float(PUZZLE_CELL_HEIGHT * self.game.manager.current_puzzle.height)

        self.grid_x = 0
        self.grid_y = 0

        # display row hint numbers
        for x in self.cell_marker_objs:
            self.cell_marker_objs[x].Kill()
        if not self.text is None:
            for x in self.text:
                for i in self.text[x]:
                    for j in i:
                        j.Kill()
        self.text = {'rows' : [], 'cols' : []}
        
        for row_num, number_list in enumerate(self.game.manager.current_puzzle.row_numbers):
            # --- DESIGNER ONLY ---
            if self.game.game_state == GAME_STATE_DESIGNER:
                continue
            # --- DESIGNER ONLY ---
            self.text['rows'].append([])
            for index, number in enumerate(number_list[::-1]):
                text = Text(self.game.core.media.fonts['puzzle_hint_numbers'], 0, 0, TEXT_ALIGN_TOP_LEFT, str(number))
                text.colour = PUZZLE_HINT_COMPLETED_COLOUR if number_list == (0,) else PUZZLE_HINT_COLOUR
                text.shadow = 2
                text.shadow_colour = (.3, .3, .3, .5)
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
                text.colour = PUZZLE_HINT_COMPLETED_COLOUR if number_list == (0,) else PUZZLE_HINT_COLOUR
                text.shadow = 2
                text.shadow_colour = (.3, .3, .3, .5)
                text.z = Z_GUI_OBJECT_LEVEL_5
                self.text['cols'][col_num].append(text)

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

        # Work out initial placement of the grid
        self.grid_x = self.row_number_width - ((self.row_number_width + self.grid_width) / 2) - PUZZLE_CELL_WIDTH
        self.grid_y = self.column_number_height - ((self.column_number_height + self.grid_height) / 2) - PUZZLE_CELL_HEIGHT


    def zoom_out_fade_and_position(self, num):
        self.hint_alpha = lerp(num, 120, self.hint_alpha, 0.0)
        for x in self.text:
            for i in self.text[x]:
                for j in i:
                    j.alpha = self.hint_alpha

        self.camera_pos[0] = lerp(num, 120, self.camera_pos[0], 0.0)
        self.camera_pos[1] = lerp(num, 120, self.camera_pos[1], 0.0)

        self.grid_x = lerp(num, 120, self.grid_x, -(self.grid_width/2))
        self.grid_y = lerp(num, 120, self.grid_y, -(self.grid_height/2))

        self.game.current_zoom_level = lerp(num, 120, self.game.current_zoom_level, self.game.minimum_zoom_level)

        self.adjust_gui_coords()
        self.adjust_text_hint_coords()                


    def adjust_gui_coords(self):
        # Adjust my x/y
        self.grid_gui_x = ((self.grid_x - self.camera_pos[0]) * self.game.current_zoom_level) + (self.game.settings['screen_width'] / 2)
        self.grid_gui_y = ((self.grid_y - self.camera_pos[1]) * self.game.current_zoom_level) + (self.game.settings['screen_height'] / 2)

        # Adjust my size
        self.grid_gui_width = self.grid_width * self.game.current_zoom_level
        self.grid_gui_height = self.grid_height * self.game.current_zoom_level


    def adjust_text_hint_coords(self):
        # Don't even ask about this, it works, alright?
        for row_num, number_list in enumerate(self.text['rows']):
            grid_x = self.grid_gui_x
            if self.hovered_row > -1 and row_num == self.hovered_row:
                if self.grid_gui_x - (((len(self.game.manager.current_puzzle.row_numbers[row_num]) * PUZZLE_CELL_WIDTH)) * self.game.current_zoom_level) < 0:
                    grid_x = (PUZZLE_CELL_WIDTH * len(self.game.manager.current_puzzle.row_numbers[row_num])) * self.game.current_zoom_level
                    if grid_x > self.game.gui.mouse.x:
                        grid_x = self.grid_gui_x
                            
            for index, text in enumerate(number_list):
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
                text.x = self.grid_gui_x + (((PUZZLE_CELL_WIDTH * col_num) + (PUZZLE_CELL_WIDTH / 2)) * self.game.current_zoom_level) - ((text.text_width/2) * self.game.current_zoom_level)
                text.y = grid_y - (((PUZZLE_CELL_HEIGHT * index) + (PUZZLE_CELL_HEIGHT / 2)) * self.game.current_zoom_level) - ((text.text_height/2) * self.game.current_zoom_level)
                text.scale = self.game.current_zoom_level
                if grid_y == self.grid_gui_y:
                    text.z = Z_GUI_OBJECT_LEVEL_5
                else:
                    text.z = Z_GUI_OBJECT_LEVEL_7


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


    def mouse_left_down(self):
        if not self.state == PUZZLE_STATE_SOLVING or self.currently_panning:
            return

        if not self.parent.tool == DRAWING_TOOL_STATE_DRAW:
            return
        
        if self.last_state_set == "ignore" or not self.last_hovered_cell == (self.hovered_row, self.hovered_column):
            # --- DESIGNER ONLY ---
            if self.game.game_state == GAME_STATE_DESIGNER:
                self.mark_cell(True, (self.hovered_row, self.hovered_column))
            # --- DESIGNER ONLY ---
            else:
                self.mark_cell(False, (self.hovered_row, self.hovered_column))


    def mouse_right_down(self):
        if not self.state == PUZZLE_STATE_SOLVING or self.currently_panning:
            return

        if not self.parent.tool == DRAWING_TOOL_STATE_DRAW:
            return
        
        if self.last_state_set == "ignore" or not self.last_hovered_cell == (self.hovered_row, self.hovered_column):
            self.mark_cell(True, (self.hovered_row, self.hovered_column))


    def mouse_left_up(self):
        if not self.state == PUZZLE_STATE_SOLVING or self.currently_panning:
            return

        if self.parent.tool == DRAWING_TOOL_STATE_FILL:
            cell_list = []
            self.checked_fill_stack = []
            self.fill_stack = [(self.hovered_row, self.hovered_column)]
            while self.fill_at(True, cell_list):
                pass
            if len(cell_list) > 0:
                self.parent.need_to_save = True        
                self.change_cells(cell_list, True)
        
        self.last_state_set = "ignore"


    def mouse_right_up(self):
        if not self.state == PUZZLE_STATE_SOLVING or self.currently_panning:
            return

        if self.parent.tool == DRAWING_TOOL_STATE_FILL:
            cell_list = []
            self.checked_fill_stack = []
            self.fill_stack = [(self.hovered_row, self.hovered_column)]
            while self.fill_at(None, cell_list):
                pass
            if len(cell_list) > 0:
                self.parent.need_to_save = True        
                self.change_cells(cell_list, None)
        
        self.last_state_set = "ignore"


    def mouse_middle_down(self):
        if not self.state == PUZZLE_STATE_SOLVING:
            return

        diff = (self.game.gui.mouse.x - self.remember_mouse_pos[0], self.game.gui.mouse.y - self.remember_mouse_pos[1])
        self.adjust_camera_pos(diff[0], diff[1])

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
        
        if None in cell or self.game.manager.current_puzzle_state[cell[0]][cell[1]] == value or cell in self.checked_fill_stack:
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
                self.game.manager.set_puzzle_cell(self.game.manager.current_puzzle, cell[1], cell[0], self.game.manager.current_puzzle_state[cell[0]][cell[1]])
            # --- DESIGNER ONLY ---
                
            self.reset_drawing_blacks((cell[0], cell[1]))
            self.reset_drawing_whites((cell[0], cell[1]))

        if self.game.game_state in [GAME_STATE_PUZZLE, GAME_STATE_TEST]:
            self.check_line_completion(cell[0], cell[1])
            if self.game.manager.is_current_puzzle_complete():
                self.state = PUZZLE_STATE_CLEARED
        # --- DESIGNER ONLY ---
        elif self.game.game_state == GAME_STATE_DESIGNER:
            self.game.manager.work_out_puzzle_hint_numbers(self.game.manager.current_puzzle)
            self.puzzle_solver_state = None
            self.puzzle_solver = None
        # --- DESIGNER ONLY ---


    def mark_cell(self, state, cell, skip_animation = False):
        if None in cell:
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
            if self.game.lives <= 0:
                self.state = PUZZLE_STATE_FAILED
            return


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
            for cell in self.game.manager.current_puzzle_state[row_index]:
                if cell:
                    total_num += 1
            if total_num > sum(self.game.manager.current_puzzle.row_numbers[row_index]):
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
            for row, cell in enumerate(column_cells):
                if self.game.manager.current_puzzle_state[row][column_index]:
                    total_num += 1
            if total_num > sum(self.game.manager.current_puzzle.column_numbers[column_index]):
                for text in self.text['cols'][column_index]:
                    text.colour = PUZZLE_HINT_COLOUR


    def reset_drawing_blacks(self, cell = None):
        pass


    def reset_drawing_whites(self, cell = None):
        pass


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

    

class Puzzle_pixel_message(Pixel_message):

    def __init__(self, game, x, y, z = Z_GUI_OBJECT_LEVEL_5, wait = 3):
        Pixel_message.__init__(self, game, x, y, z, wait)
        # TODO
        #self.draw_strategy = "puzzle_pixel_message"



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
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.text = Text(
            self.game.core.media.fonts['puzzle_message'],
            self.x,
            self.y,
            TEXT_ALIGN_CENTER,
            text,
            )
        self.text.colour = (1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.3, .3, .3, .5)

        self.text.z = self.z
        self.do_fade = True
        self.iter = 0
        self.alpha = 0.0

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_width = self.text.text_width + 20.0
        self.primitive_square_height = self.text.text_height + 2.0
        self.primitive_square_x = self.x - (self.text.text_width/2) - 20.0
        self.primitive_square_y = self.y - (self.text.text_height/2) - 2.0
        self.primitive_square_colour = (0.0, 0.0, 0.0, 0.0)
        

    def Execute(self):
        if not self.do_fade:
            return
        self.iter += 1
        self.alpha = lerp(self.iter, 60, self.alpha, 1.0)
        self.text.alpha = self.alpha
        self.primitive_square_colour = (0.0, 0.0, 0.0, self.alpha - .7)
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

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_x = self.game.settings['screen_width'] - 300.0
        self.primitive_square_y = self.game.settings['screen_height'] - 74.0
        self.primitive_square_width = 300.0
        self.primitive_square_height = 74.0
        self.primitive_square_four_colours = True
        self.primitive_square_colour = (
            (1.0, 1.0, 1.0, 0.0),
            (.5, .7, .8, 1.0),
            (.5, .7, .8, 1.0),
            (1.0, 1.0, 1.0, 0.0)
            )


    def Execute(self):
        if self.game.lives < self.current_lives:
            self.lives_objs[self.current_lives - 1].die()
            del(self.lives_objs[self.current_lives - 1])
            if len(self.lives_objs):
                self.lives_objs[self.game.lives - 1].current = True
        self.current_lives = self.game.lives


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
        self.x = self.game.settings['screen_width'] - ((self.image.width * (num + 1)) + 15)
        self.y = self.game.settings['screen_height'] - self.image.height - 10
        self.z = Z_GUI_OBJECT_LEVEL_6 - 1
        self.scale_point = (self.image.width / 2, self.image.height / 2)
        self.scale = .8
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
            self.scale = lerp(self.iter, 60, .8 if self.scale_dir else 1.0, 1.0 if self.scale_dir else .8)
            if self.iter > 60:
                self.iter = 0
                self.scale_dir = not self.scale_dir


    def get_screen_draw_position(self):
        return self.x, self.y

    
    def die(self):
        self.dying = True
        self.init_y = self.y
        self.image_sequence = 2
        self.scale = 1.0



class Timer(Process):
    
    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.z = Z_GUI_OBJECT_LEVEL_6            
        self.text = Text(self.game.core.media.fonts['puzzle_timer'], self.game.settings['screen_width'] - 25, self.game.settings['screen_height'] - 100, TEXT_ALIGN_CENTER_RIGHT, "00:00:00")
        self.text.colour = (1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.3, .3, .3, .5)
        self.text.z = self.z - 1

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_x = self.game.settings['screen_width'] - 300.0
        self.primitive_square_y = self.text.y - 20.0
        self.primitive_square_width = 300.0
        self.primitive_square_height = 45
        self.primitive_square_four_colours = True
        self.primitive_square_colour = (
            (1.0, 1.0, 1.0, 0.0),
            (.5, .7, .8, 1.0),
            (.5, .7, .8, 1.0),
            (1.0, 1.0, 1.0, 0.0)
            )


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


    def get_screen_draw_position(self):
        return self.x, self.y


    def On_Exit(self):
        self.text.Kill()
