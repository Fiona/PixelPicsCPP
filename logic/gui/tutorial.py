"""
PixelPics - Nonograme game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
#

# Game engine imports
from core import *

# Game imports
from consts import *
from gui.gui_elements import *
from gui.puzzle_view import GUI_puzzle, GUI_puzzle_container
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
        "logically deduce what's there."
        ]
    message_final_stage_wrong_cell_alt = [
        "Whoops! That's incorrect! Remember to use the LEFT mouse",
        "button to fill squares and the RIGHT mouse button to",
        "mark squares as empty. Only click a square when you can",
        "logically deduce what's there."
        ]
    message_final_stage_cell_filled = ["Whoops! That square has already been completed!"]
    message_tutorial_complete = ["Great work - you solved the puzzle and revealed the hidden", "picture!", "That's all I have to teach you!", "Have fun playing PixelPics!"]

    
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
            instructions = ["Hi there, I'm Chips!", "I'm going to show you how to solve PixelPics puzzles!"]
            )
        self.add_stage(
            instructions = ["The goal is to reveal the hidden picture in each puzzle.", "This is done by figuring out which squares are filled and", "which are empty."]
            )
        self.add_stage(
            instructions = ["Take a look at this one."]
            )
        self.add_stage(
            instructions = ["See the numbers along the edges?", "They tell you the lengths of the filled blocks that can be", "found on that row or column, in the order they", "appear."]
            )
        self.add_stage(
            instructions = ["This column has only one number, a 2!", "So somewhere in this column there's a single block of 2", "filled squares."],
            col_highlights = [[(0,0), (0,4)]]
            )
        self.add_stage(
            instructions = ["This row has two separate numbers, each being a 1.", "So somewhere in this row there are two separated filled", "squares."],
            row_highlights = [[(0,3), (4,3)]]
            )
        self.add_stage(
            instructions = ["Sounds tricky right? It's actually really easy!"]
            )
        self.add_stage(
            instructions = ["PixelPics puzzles never require any guesswork at all!", "They can always be solved by thinking logically. I'll show you!"]
            )
        self.add_stage(
            instructions = ["Let's start with this column.", "The clue says there's a single block of 5 squares here."],
            col_highlights = [[(2,0), (2,4)]]
            )
        self.add_stage(
            instructions = ["That's the whole height of the board! So we know for sure", "that they must all be filled in."],
            col_highlights = [[(2,0), (2,4)]]
            )
        self.add_stage(
            instructions = ["Go ahead and fill in those squares by clicking on them with", "your right mouse button!"],
            alt_instructions = ["Go ahead and fill in those squares by clicking on them with", "your left mouse button!"],
            col_highlights = [[(2, 0), (2, 4)]],
            cells_fill = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],
            wrong_cell = ["We'll get to the other squares in a second - let's focus on the", "highlighted ones for now!"],
            wrong_input = [
                "Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to fill in spaces!",
                "Whoops! That was a right click. Be sure to use the LEFT", "mouse button to fill in spaces!"
              ]
            )
        self.add_stage(
            instructions = ["Great!", "The squares that you figure out will help you solve more", "of the puzzle!"],
            mood = "happy"
            )
        self.add_stage(
            instructions = ["Take a look at this column.", "The clue is 0, that means there are no filled squares in this", "column at all!"],
            col_highlights = [[(4,0), (4,4)]]
            )
        self.add_stage(
            instructions = ["When we know for sure that a square isn't filled in,", "we can mark it with an 'X'."],
            col_highlights = [[(4,0), (4,4)]]
            )
        self.add_stage(
            instructions = ["Go ahead and mark those squares as empty with your", "left mouse button!"],
            alt_instructions = ["Go ahead and mark those squares as empty with your", "right mouse button!"],
            col_highlights = [[(4,0), (4,4)]],
            cells_empty = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)],
            wrong_cell = ["We'll get to the other squares in a second - let's focus on the", "highlighted ones for now!"],
            wrong_input = [
                "Whoops! That was a right click. Be sure to use the LEFT", "mouse button to mark spaces as empty!",
                "Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to mark spaces as empty!"
              ]
            )
        self.add_stage(
            instructions = ["Excellent!", "These will help us deduce more of the puzzle too."],
            mood = "happy"            
            )
        self.add_stage(
            instructions = ["Remember this row? The clue says there are 2 separated", "filled squares.", "Hey, we've already found one of them!"],
            row_highlights = [[(0,3), (4,3)]]
            )
        self.add_stage(
            instructions = ["Each block of squares must be separated by at least 1", "empty square.", "That means that the squares either side of the", "filled block must be empty!"],
            cell_highlights = [(1,3), (3,3)]
            )
        self.add_stage(
            instructions = ["Go ahead and mark those spaces as empty with your left", "mouse button."],
            alt_instructions = ["Go ahead and mark those spaces as empty with your right", "mouse button."],
            cell_highlights = [(1,3), (3,3)],
            cells_empty = [(3,1), (3,3)],
            wrong_cell = ["We'll get to the other squares in a second - let's focus on the", "highlighted ones for now!"],
            wrong_input = [
                "Whoops! That was a right click. Be sure to use the LEFT", "mouse button to mark spaces as empty!",
                "Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to mark spaces as empty!"
              ]            
            )
        self.add_stage(
            instructions = ["Fabulous!"],
            mood = "happy"            
            )        
        self.add_stage(
            instructions = ["Sometimes there is only 1 remaining place a block of squares", "could be.", "So the other filled square must be in the highlighted", "space!"],
            cell_highlights = [(0,3)]
            )
        self.add_stage(
            instructions = ["Go ahead and fill it!"],
            cell_highlights = [(0,3)],
            cells_fill = [(3,0)],
            wrong_cell = ["We'll get to the other squares in a second - let's focus on the", "highlighted ones for now!"],
            wrong_input = [
                "Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to fill in spaces!",
                "Whoops! That was a right click. Be sure to use the LEFT", "mouse button to fill in spaces!"
              ]            
            )
        self.add_stage(
            instructions = ["Bravo!"],
            mood = "happy"            
            )        
        self.add_stage(
            instructions = ["Check out this row. The clue says there's a single block of 3.", "But there are 4 spaces!", "So we don't know for sure exactly where the block", "starts and ends."],
            row_highlights = [[(0,0), (4,0)]]
            )
        self.add_stage(
            instructions = ["Maybe it's over here..."],
            row_highlights = [[(0,0), (2,0)]]
            )
        self.add_stage(
            instructions = ["Or maybe it's over here?"],
            row_highlights = [[(1,0), (3,0)]]
            )
        self.add_stage(
            instructions = ["Either way there's an overlap of two squares in the middle.", "So we know for sure that those squares must be filled!"],
            row_highlights = [[(1,0), (2,0)]]
            )
        self.add_stage(
            instructions = ["Go ahead and fill that middle square to complete the overlap!"],
            cell_highlights = [(1,0)],
            cells_fill = [(0, 1)],
            wrong_cell = ["We'll get to the other squares in a second - let's focus on the", "highlighted ones for now!"],
            wrong_input = [
                "Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to fill in spaces!",
                "Whoops! That was a right click. Be sure to use the LEFT", "mouse button to fill in spaces!"
              ]            
            )
        self.add_stage(
            instructions = ["You got it!"],
            mood = "happy"            
            )
        self.add_stage(
            instructions = ["Take a look at these rows. We've already found the blocks", "mentioned in the clues!", "Notice that the clues change colour when we've", "solved them."],
            row_highlights = [[(0,1), (4,1)], [(0,4), (4,4)]]
            )
        self.add_stage(
            instructions = ["That means we know for sure that the other squares on", "these rows must be empty."],
            row_highlights = [[(0,1), (4,1)], [(0,4), (4,4)]]
            )
        self.add_stage(
            instructions = ["Go ahead and mark those squares as empty!"],
            row_highlights = [[(0,1), (4,1)], [(0,4), (4,4)]],
            cells_empty = [(1,0), (1,1), (4,0), (4,1), (1,3), (4, 3)],
            wrong_cell = ["We'll get to the other squares in a second - let's focus on the", "highlighted ones for now!"],
            wrong_input = [
                "Whoops! That was a right click. Be sure to use the LEFT", "mouse button to mark spaces as empty!",
                "Whoops! That was a left click. Be sure to use the RIGHT", "mouse button to mark spaces as empty!"
              ]            
            )
        self.add_stage(
            instructions = ["Teriffic!"],
            mood = "happy"            
            )
        self.add_stage(
            instructions = ["Now there are only a few unfilled squares left.", "How about you take it from here?"]
            )
        self.add_stage(
            instructions = ["Remember, only mark squares that you know for sure.", "Good luck!"],
            mood = "happy"            
            )
        

    def add_stage(
          self, instructions = [""], alt_instructions = [""], row_highlights = [], col_highlights = [], cell_highlights = [], \
          cells_fill = [], cells_empty = [], wrong_cell = "", wrong_input = ["", ""], mood = "normal"
          ):
        empty_stage = {
            'instructions' : instructions,
            'alt_instructions' : alt_instructions,
            'row_highlights' : row_highlights,
            'col_highlights' : col_highlights,
            'cell_highlights' : cell_highlights,
            'cells_fill' : cells_fill,
            'cells_empty' : cells_empty,
            'wrong_cell' : wrong_cell,
            'wrong_input' : wrong_input,
            'mood' : mood
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
        self.reset_puzzle_obj()
       
        if self.current_stage == len(self.tutorial_stages):
            self.mascot.set_mood("normal")
            self.mascot.set_speech([])
            self.final_stage = True


    def next_stage(self):
        if self.display_message or not self.stage_object is None or self.final_stage:
            return
        self.game.cursor_tool_state = DRAWING_TOOL_STATE_NORMAL        
        self.mascot.set_mood(self.tutorial_stages[self.current_stage]['mood'])
        self.reset_puzzle_obj()
        self.stage_object = GUI_tutorial_stage(self.game, self, self.tutorial_stages[self.current_stage])
        

    def check_stage_completion(self):
        if len(self.tutorial_stages[self.current_stage]['cells_fill']):
            done = True
            for cell in self.tutorial_stages[self.current_stage]['cells_fill']:
                if not self.game.manager.current_puzzle_state[cell[0]][cell[1]] == True:
                    done = False
                    break

        if len(self.tutorial_stages[self.current_stage]['cells_empty']):
            done = True
            for cell in self.tutorial_stages[self.current_stage]['cells_empty']:
                if not self.game.manager.current_puzzle_state[cell[0]][cell[1]] == False:
                    done = False
                    break
        
        if done:
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
        self.show_message([message])
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


    def do_bump_scrolling(self):
        return
    

    def finish_cleared_anim(self):
        self.parent.puzzle_cleared = True
        self.mascot.set_speech(self.parent.message_tutorial_complete)
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
        if len(self.stage['col_highlights']):
            for column_highlight in self.stage['col_highlights']:
                self.objs.append(Tutorial_Line_Highlight(self.game, self, column_highlight[0], column_highlight[1], is_col = True))
        if len(self.stage['row_highlights']):
            for row_highlight in self.stage['row_highlights']:
                self.objs.append(Tutorial_Line_Highlight(self.game, self, row_highlight[0], row_highlight[1], is_col = False))
        if len(self.stage['cell_highlights']):
            for cell_highlight in self.stage['cell_highlights']:
                self.objs.append(Tutorial_Cell_Highlight(self.game, self, cell_highlight))

        
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
