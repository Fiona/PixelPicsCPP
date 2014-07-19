"""
PixelPics - Nonograme game
Copyright (c) 2014 Stompy Blondie Games http://stompyblondie.com
"""

# python imports
#

# Game engine imports
from core import *

# Game imports
from consts import *
from gui.gui_elements import *
from gui.puzzle_view import GUI_puzzle, GUI_puzzle_container, Puzzle_marker
from gui.mascot import Mascot_Tutorial



class GUI_tutorial_container(GUI_puzzle_container):
    """
    All elements in the tutorial live inside this thing.
    """
    tutorial_stages = []
    current_stage = 0
    
    message_out_of_board = ["Whoops! Make sure you click on the board!"]
    message_final_stage_wrong_cell = [
        "Whoops! That's incorrect! Remember to use the RIGHT mouse",
        "button to fill squares and the LEFT mouse button to mark", 
        "squares as empty. Only click a square when you can",
        "definitely figure out what's there."
        ]
    message_final_stage_wrong_cell_alt = [
        "Whoops! That's incorrect! Remember to use the LEFT mouse",
        "button to fill squares and the RIGHT mouse button to",
        "squares as empty. Only click a square when you can",
        "definitely figure out what's there."
        ]
    message_final_stage_cell_filled = ["Whoops! That square has already been completed!"]
    message_tutorial_complete = ["Congratulations, you've solved the puzzle and", "revealed the hidden picture!", "Now try out the puzzles in the Beginner category.", "Have fun playing PixelPics!"]

    
    def __init__(self, game, parent = None):
        GUI_puzzle_container.__init__(self, game)
        self.tutorial_stages = []
        self.current_stage = 0
        self.display_message = False
        self.final_stage = False
        self.puzzle_cleared = False
        self.wait_one_left_click = False
        self.stage_object = None
        self.mascot = Mascot_Tutorial(self.game)

        self.add_stage(
            instructions = ["Hi there, I'm Chips!", "I'm going to show you how to solve PixelPics puzzles!"],
            no_hide_puzzle = True
            )
        self.add_stage(
            instructions = ["The goal is to reveal the hidden picture in each puzzle", "by figuring out which squares are filled."],
            no_hide_puzzle = True
            )
        self.add_stage(
            instructions = ["We solve rows and columns one at a time.", "I'm going to show you some rules for solving them."],
            no_hide_puzzle = True
            )
        self.add_stage(
            instructions = ["Each row and column has numbers that tell you how to solve it.", "This one just has a 0."],
            col_highlight = 4
            )
        self.add_stage(
            instructions = ["0 means that the row or column is completely empty.", "You should mark any squares you know are empty.", "Left click each square to mark them."],
            alt_instructions = ["0 means that the row or column is completely empty.", "You should mark any squares you know are empty.", "Right click each square to mark them."],
            col_highlight = 4,
            cells_empty = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)],
            wrong_cell = ["We'll get to the other squares in a second - let's focus on the", "highlighted column for now!"],
            wrong_input = [
                ["Whoops! That was a right click. Be sure to use the LEFT", "mouse button to mark squares as empty!"],
                ["Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to mark squares as empty!"]
              ]
            )
        self.add_stage(
            instructions = ["Numbers indicate how many connected filled squares are", "in that column or row."],
            row_highlight = 2,
            )
        self.add_stage(
            instructions = ["This 4 means there are 4 filled squares in that row.", "We've already solved one of the squares in this row.", "Right click the squares that are definitely filled."],
            alt_instructions = ["This 4 means there are 4 filled squares in that row.", "We've already solved one of the squares in this row.", "Left click the squares that are definitely filled."],
            wrong_cell = ["We'll get to the other squares in a second - let's focus on the", "highlighted row for now!"],
            wrong_input = [
                ["Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to fill in spaces!"],
                ["Whoops! That was a right click. Be sure to use the LEFT", "mouse button to fill in spaces!"]
              ],
            row_highlight = 2,
            cells_fill = [(2, 0), (2, 1), (2, 2), (2, 3)],
            )
        self.add_stage(
            instructions = ["This clue indicates a connected group of 3 squares.", "But there are two possible places they could be."],
            row_highlight = 0,
            )
        self.add_stage(
            instructions = ["We can determine that there is a two square OVERLAP", "which is filled.", "Right click the squares that are definitely filled."],
            alt_instructions = ["We can determine that there is a two square OVERLAP", "which is filled.", "Left click the squares that are definitely filled."],
            row_highlight = 0,
            cells_fill = [(0, 1), (0, 2)],
            wrong_cell = ["Try again! Remember to mark only the definite overlap."],
            wrong_input = [
                ["Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to fill in spaces!"],
                ["Whoops! That was a right click. Be sure to use the LEFT", "mouse button to fill in spaces!"]
              ],            
            )
        self.add_stage(
            instructions = ["Multiple numbers indicate groups of filled squares", "They are always in the order shown and separated", "by at least one empty square."],
            col_highlight = 3,
            )
        self.add_stage(
            instructions = ["Can you work out and mark which squares are filled", "and which are empty?", "Right click to mark filled, left click to mark empty."],
            alt_instructions = ["Can you work out and mark which squares are filled", "and which are empty?", "Left click to mark filled, right click to mark empty."],
            col_highlight = 3,
            cells_empty = [(1, 3)],
            cells_fill = [(0, 3), (2, 3), (3, 3), (4, 3)],
            wrong_cell = ["Try again! Remember, multiple numbers indicate groups of", "filled squares. They are always order shown and separated by", "at least one empty square"],
            )
        self.add_stage(
            instructions = ["Sometimes you can't solve all the squares at once.", "Here there's only ONE square we can work out.", "Can you mark which square you think is solvable?"],
            alt_instructions = ["Sometimes you can't solve all the squares at once.", "Here there's only ONE square we can work out.", "Can you mark which square you think is solvable?"],
            row_highlight = 3,
            cells_empty = [(3, 2)],
            wrong_cell = ["Try again! Remember that filled groups of squares must be", "separated by at least one empty square.", "We can't know for sure where the other filled", "square is - do we know which are definitely empty?"],
            wrong_input = [
                ["Are you sure you want to fill a square?", "Look carefully, can you know for certain that the", "other filled square is solvable?"],
                ["Are you sure you want to fill a square?", "Look carefully, can you know for certain that the", "other filled square is solvable?"],
              ],            
            )
        self.add_stage(
            instructions = ["Even though we've solved this column, it's a good", "idea to mark the rest of the empty squares to help", "us work out the rest of the puzzle."],
            alt_instructions = ["Even though we've solved this column, it's a good", "idea to mark the rest of the empty squares to help", "us work out the rest of the puzzle."],
            col_highlight = 1,
            cells_empty = [(1, 1), (3, 1), (4, 1)],
            wrong_cell = ["Whoops! We're marking the rest of this column as empty!"],
            wrong_input = [
                ["Whoops! That was a right click. Be sure to use the LEFT", "mouse button to mark squares as empty!"],
                ["Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to mark squares as empty!"]
              ],            
            )
        self.add_stage(
            instructions = ["Now try solving the rest of the puzzle on your", "own... Good luck!"],
            mood = "happy"
            )


    def add_stage(
          self, instructions = [""], alt_instructions = [""], row_highlight = -1, col_highlight = -1,  \
          cells_fill = [], cells_empty = [], wrong_cell = "", wrong_input = [[""], [""]], mood = "normal",
          no_hide_puzzle = False
          ):
        empty_stage = {
            'instructions' : instructions,
            'alt_instructions' : alt_instructions,
            'row_highlight' : row_highlight,
            'col_highlight' : col_highlight,
            'cells_fill' : cells_fill,
            'cells_empty' : cells_empty,
            'wrong_cell' : wrong_cell,
            'wrong_input' : wrong_input,
            'mood' : mood,
            'no_hide_puzzle' : no_hide_puzzle,
            }
        self.tutorial_stages.append(empty_stage)
        

    def create_puzzle_element(self):
        self.puzzle = GUI_tutorial_puzzle(self.game, self)


    def finish_stage(self):
        if self.stage_object is None:
            return
        if self.game.settings['mouse_left_empty']:        
            if len(self.tutorial_stages[self.current_stage]['cells_empty']):
                self.wait_one_left_click = True
            else:
                self.wait_one_left_click = False
        else:
            if len(self.tutorial_stages[self.current_stage]['cells_fill']):
                self.wait_one_left_click = True
            else:
                self.wait_one_left_click = False
        self.stage_object.Kill()
        self.stage_object = None
        self.current_stage += 1

        if self.current_stage == len(self.tutorial_stages) - 1:
            self.puzzle.hide_hint_numbers = False
            self.puzzle.markers_dont_die = False
            self.puzzle.tutorial = False
            self.puzzle.reset_drawing_all_blacks = False
            self.puzzle.reset_drawing_all_whites = False            

        if self.current_stage == len(self.tutorial_stages):
            self.mascot.set_mood("normal")
            self.mascot.set_speech([])
            self.final_stage = True

        self.reset_puzzle_obj()


    def next_stage(self):
        if self.display_message or not self.stage_object is None or self.final_stage:
            return
        self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL        
        self.mascot.set_mood(self.tutorial_stages[self.current_stage]['mood'])
        self.reset_puzzle_obj()
        self.stage_object = GUI_tutorial_stage(self.game, self, self.tutorial_stages[self.current_stage])
        self.puzzle.draw_strategy_tutorial_row_highlight = self.tutorial_stages[self.current_stage]['row_highlight']
        self.puzzle.draw_strategy_tutorial_col_highlight = self.tutorial_stages[self.current_stage]['col_highlight']

        if self.current_stage == len(self.tutorial_stages) - 1 or self.current_stage == len(self.tutorial_stages):
            self.puzzle.tutorial = False
        else:
            self.puzzle.tutorial = not self.tutorial_stages[self.current_stage]['no_hide_puzzle']

        self.puzzle.kill_all_visible_markers()

        # Create cell markers for all existing cells
        if self.puzzle.draw_strategy_tutorial_col_highlight > -1:
            cols = []
            for row in self.game.manager.current_puzzle_state:
                cols.append(row[self.puzzle.draw_strategy_tutorial_col_highlight])
            for i,state in enumerate(cols):
                if not state is None:
                    self.puzzle.cell_marker_objs[(i, self.puzzle.draw_strategy_tutorial_col_highlight)] = Puzzle_marker(
                        self.game, self.puzzle, i, self.puzzle.draw_strategy_tutorial_col_highlight, state, False
                        )

        if self.puzzle.draw_strategy_tutorial_row_highlight > -1:
            rows = self.game.manager.current_puzzle_state[self.puzzle.draw_strategy_tutorial_row_highlight]
            for i,state in enumerate(rows):
                if not state is None:
                    self.puzzle.cell_marker_objs[(self.puzzle.draw_strategy_tutorial_row_highlight, i)] = Puzzle_marker(
                        self.game, self.puzzle, self.puzzle.draw_strategy_tutorial_row_highlight, i, state, False
                        )
            

    def check_stage_completion(self):
        done_fill = False
        done_empty = False
        
        if len(self.tutorial_stages[self.current_stage]['cells_fill']):
            done_fill = True
            for cell in self.tutorial_stages[self.current_stage]['cells_fill']:
                if not self.game.manager.current_puzzle_state[cell[0]][cell[1]] == True:
                    done_fill = False
                    break

        if len(self.tutorial_stages[self.current_stage]['cells_empty']):
            done_empty = True
            for cell in self.tutorial_stages[self.current_stage]['cells_empty']:
                if not self.game.manager.current_puzzle_state[cell[0]][cell[1]] == False:
                    done_empty = False
                    break

        if len(self.tutorial_stages[self.current_stage]['cells_fill']) and len(self.tutorial_stages[self.current_stage]['cells_empty']):
            if done_fill and done_empty:
                self.finish_stage()                
        else:
            if done_fill or done_empty:
                self.finish_stage()


    def reset_puzzle_obj(self):
        self.puzzle.last_hovered_cell = (None, None)
        self.puzzle.hovered_column = -1
        self.puzzle.hovered_row = -1
        self.puzzle.last_state_set = "ignore"
        self.puzzle.current_locked_row = None
        self.puzzle.current_locked_col = None
        

    def wrong_input(self):
        if self.game.settings['mouse_left_empty']:
            message = self.tutorial_stages[self.current_stage]['wrong_input'][0]
        else:
            message = self.tutorial_stages[self.current_stage]['wrong_input'][1]        
        self.show_message(message)
        self.mascot.set_mood("sad")


    def wrong_cell(self):
        if not self.final_stage:
            self.show_message(self.tutorial_stages[self.current_stage]['wrong_cell'])
        else:
            if self.game.settings['mouse_left_empty']:
                message = self.message_final_stage_wrong_cell
            else:
                message = self.message_final_stage_wrong_cell_alt
            self.show_message(message)
        self.mascot.set_mood("sad")


    def final_stage_cell_already_filled(self):
        self.show_message(self.message_final_stage_cell_filled)
        self.mascot.set_mood("sad")
        

    def out_of_board(self):
        self.show_message(self.message_out_of_board)
        self.mascot.set_mood("sad")


    def show_message(self, message):
        if not self.stage_object is None:
            self.stage_object.Kill()
        self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL
        self.stage_object = GUI_tutorial_message(self.game, self, message)
        self.display_message = True


    def remove_message(self):
        self.stage_object.Kill()
        self.stage_object = None
        self.display_message = False
        self.mascot.set_mood("normal")
        self.mascot.set_speech([])        
        if self.puzzle_cleared:
            self.puzzle.close_puzzle()
        else:
            self.next_stage()
                

    def On_Exit(self):
        GUI_puzzle_container.On_Exit(self)
        self.mascot.Kill()



class GUI_tutorial_puzzle(GUI_puzzle):

    def __init__(self, game, parent = None):
        GUI_puzzle.__init__(self, game, parent)
        self.hide_hint_numbers = True
        self.markers_dont_die = True
        

    def Execute(self):
        GUI_puzzle.Execute(self)

        if self.state == PUZZLE_STATE_SOLVING:
            if self.parent.current_stage < len(self.parent.tutorial_stages):
                self.parent.next_stage()


    def mark_cell(self, state, cell, skip_animation = False):
        if not self.parent.stage_object is None and self.parent.stage_object.click_to_continue:
            return

        if -1 in cell:
            self.parent.out_of_board()
            return

        if not self.parent.final_stage:
            stage = self.parent.tutorial_stages[self.parent.current_stage]            

            # We have a hybrid stage        
            self.hybrid_stage = False
            if len(stage['cells_fill']) and len(stage['cells_empty']):
                self.hybrid_stage = True

            if self.hybrid_stage:
                if state == True and not cell in stage['cells_fill']:
                    self.parent.wrong_cell()
                    return
                elif state == False and not cell in stage['cells_empty']:
                    self.parent.wrong_cell()
                    return                
            else:
                # If we have cells that need filling
                if len(stage['cells_fill']):
                    if state == False:
                        self.parent.wrong_input()
                        return

                    if not cell in stage['cells_fill']:
                        self.parent.wrong_cell()
                        return

                # If we have cells that need emptying
                if len(stage['cells_empty']):
                    if state == True:
                        self.parent.wrong_input()
                        return
                    if not cell in stage['cells_empty']:
                        self.parent.wrong_cell()
                        return
                
        else:
            if not self.game.manager.current_puzzle_state[cell[0]][cell[1]] == None:
                self.parent.final_stage_cell_already_filled()
                return
            
            if state is True:
                if not self.game.manager.current_puzzle.cells[cell[0]][cell[1]][0] == True:
                    self.parent.wrong_cell()
                    return
            else:
                if not self.game.manager.current_puzzle.cells[cell[0]][cell[1]][0] in [False, None]:
                    self.parent.wrong_cell()
                    return

        GUI_puzzle.mark_cell(self, state, cell, skip_animation)

        if not self.parent.final_stage:
            self.parent.check_stage_completion()

        self.reset_drawing_blacks()
        self.reset_drawing_whites()


    def do_bump_scrolling(self):
        return
    

    def finish_cleared_anim(self):
        if self.parent.puzzle_cleared:
            return
        self.parent.puzzle_cleared = True
        self.parent.mascot.set_speech(self.parent.message_tutorial_complete, bubble = False)
        self.parent.show_message(self.parent.message_tutorial_complete)
        


class GUI_tutorial_stage(GUI_element):
    def __init__(self, game, parent, stage):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.stage = stage
        self.x = (self.game.settings['screen_width'] / 2) - 450
        self.y = (self.game.settings['screen_height'] / 2) - 395
        self.z = Z_GUI_OBJECT_LEVEL_7 - 1
        self.image = self.game.core.media.gfx['gui_tutorial_speech_bubble']
        self.gui_init()

        self.width, self.height = 0, 0
        self.click_to_continue = False
        
        if self.stage['cells_fill'] == [] and self.stage['cells_empty'] == []:
            self.width = self.game.settings['screen_width']
            self.height = self.game.settings['screen_height']
            self.click_to_continue = True
            GUI_tutorial_button_next(self.game, self, self.parent.finish_stage)

        self.objs = []

        ins = self.stage['instructions']
        if not self.stage['alt_instructions'] == [""] and not self.game.settings['mouse_left_empty']:
            ins = self.stage['alt_instructions']

        self.parent.mascot.set_speech(ins, bubble = False)

        text_y_pos = self.y + 40
        
        for text_string in ins:
            text = Text(self.game.core.media.fonts['tutorial_instructions'], self.x + 190, text_y_pos, TEXT_ALIGN_TOP_LEFT, text_string)
            text.colour = (.2, .2, .2)
            text.z = self.z - 1
            self.objs.append(text)
            text_y_pos += text.text_height + 5
        """
        if self.stage['col_highlights'] > -1:
            self.objs.append(Tutorial_Line_Highlight(self.game, self, column_highlight[0], column_highlight[1], is_col = True))
        if len(self.stage['row_highlight']):
            for row_highlight in self.stage['row_highlights']:
                self.objs.append(Tutorial_Line_Highlight(self.game, self, row_highlight[0], row_highlight[1], is_col = False))
        """        

        
    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.objs:
            x.Kill()
            


class GUI_tutorial_message(GUI_element):
    def __init__(self, game, parent, message):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = (self.game.settings['screen_width'] / 2) - 450
        self.y = (self.game.settings['screen_height'] / 2) - 395
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']        
        self.z = Z_GUI_OBJECT_LEVEL_7 - 1
        self.image = self.game.core.media.gfx['gui_tutorial_speech_bubble']
        self.gui_init()

        self.objs = []
        self.click_to_continue = True
        GUI_tutorial_button_next(self.game, self, self.parent.remove_message)

        self.parent.mascot.set_speech(message, bubble = False)

        text_y_pos = self.y + 40

        for text_string in message:
            text = Text(self.game.core.media.fonts['tutorial_instructions'], self.x + 190, text_y_pos, TEXT_ALIGN_TOP_LEFT, text_string)
            text.colour = (.2, .2, .2)
            text.z = self.z - 1
            self.objs.append(text)
            text_y_pos += text.text_height + 5
        

    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.objs:
            x.Kill()



class GUI_tutorial_button_next(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent = None, callback = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.callback = callback
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.image = self.game.core.media.gfx['gui_button_tutorial_next']
        self.gui_init()
        self.x = (self.game.settings['screen_width'] / 2) + 280
        self.y = (self.game.settings['screen_height'] / 2) - 285
        

    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if not self.callback is None:
            self.callback()



class Tutorial_Line_Highlight(Process):
    def __init__(self, game, parent, highlight_from, highlight_to, is_col):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.highlight_from = highlight_from
        self.highlight_to = highlight_to
        self.is_col = is_col
        self.z = Z_GUI_OBJECT_LEVEL_7 - 1
        self.strobe_dir = 1
        self.alpha = .6
        self.draw_strat()


    def Execute(self):
        if self.strobe_dir:
            if self.alpha >= .6:
                self.strobe_dir = 0
            else:
                self.alpha += .01
        else:
            if self.alpha <= .2:
                self.strobe_dir = 1
            else:
                self.alpha -= .01
        self.draw_strat()
        

    def draw_strat(self):        
        puzzle_obj = self.parent.parent.puzzle
        
        self.x = ((puzzle_obj.grid_x - puzzle_obj.camera_pos[0]) * self.game.current_zoom_level) + (self.game.settings['screen_width']/2)
        self.y = ((puzzle_obj.grid_y - puzzle_obj.camera_pos[1]) * self.game.current_zoom_level) + (self.game.settings['screen_height']/2)

        self.x += (self.highlight_from[0] * PUZZLE_CELL_WIDTH)
        self.y += (self.highlight_from[1] * PUZZLE_CELL_HEIGHT)

        if self.is_col:
            self.width = PUZZLE_CELL_WIDTH
            self.height = ((self.highlight_to[1] - self.highlight_from[1]) * PUZZLE_CELL_HEIGHT) + PUZZLE_CELL_HEIGHT
        else:
            self.width = ((self.highlight_to[0] - self.highlight_from[0]) * PUZZLE_CELL_WIDTH) + PUZZLE_CELL_WIDTH
            self.height = PUZZLE_CELL_HEIGHT

        pad = 5
        self.x -= pad
        self.y -= pad
        self.width += pad * 2
        self.height += pad * 2
        
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
        self.primitive_square_x = self.x
        self.primitive_square_y = self.y
        self.primitive_square_colour = (1.0, 0.0, 0.0, self.alpha)



class Tutorial_Cell_Highlight(Process):
    def __init__(self, game, parent, highlight):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.highlight = highlight
        self.z = Z_GUI_OBJECT_LEVEL_9
        self.strobe_dir = 1
        self.alpha = .6
        self.draw_strat()


    def Execute(self):
        if self.strobe_dir:
            if self.alpha >= .6:
                self.strobe_dir = 0
            else:
                self.alpha += .01
        else:
            if self.alpha <= .2:
                self.strobe_dir = 1
            else:
                self.alpha -= .01
        self.draw_strat()
        

    def draw_strat(self):        
        puzzle_obj = self.parent.parent.puzzle
        
        self.x = ((puzzle_obj.grid_x - puzzle_obj.camera_pos[0]) * self.game.current_zoom_level) + (self.game.settings['screen_width']/2)
        self.y = ((puzzle_obj.grid_y - puzzle_obj.camera_pos[1]) * self.game.current_zoom_level) + (self.game.settings['screen_height']/2)

        self.x += (self.highlight[0] * PUZZLE_CELL_WIDTH)
        self.y += (self.highlight[1] * PUZZLE_CELL_HEIGHT)

        self.width = PUZZLE_CELL_WIDTH
        self.height = PUZZLE_CELL_HEIGHT

        pad = 5
        self.x -= pad
        self.y -= pad
        self.width += pad * 2
        self.height += pad * 2
        
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
        self.primitive_square_x = self.x
        self.primitive_square_y = self.y
        self.primitive_square_colour = (1.0, 0.0, 0.0, self.alpha)
