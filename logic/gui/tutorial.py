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



class GUI_tutorial_container(GUI_puzzle_container):
    """
    All elements in the tutorial live inside this thing.
    """
    tutorial_stages = []
    current_stage = 0
    
    message_out_of_board = "Whoops! Make sure you click on the board!"
    message_final_stage_wrong_cell = [
        "Whoops! That's incorrect! Remember to use the RIGHT mouse button to fill squares",
        "and the LEFT mouse button to mark squares as empty.",
        "Only click a square when you can logically deduce what's there."
        ]
    message_final_stage_wrong_cell_alt = [
        "Whoops! That's incorrect! Remember to use the LEFT mouse button to fill squares",
        "and the RIGHT mouse button to mark squares as empty.",
        "Only click a square when you can logically deduce what's there."
        ]
    message_final_stage_cell_filled = "Whoops! That square has already been completed!"
    message_tutorial_complete = ["Great work - you solved the puzzle and revealed the hidden picture!", "That's all I have to teach you! Have fun playing PixelPics!"]
    
    def __init__(self, game, parent = None):
        GUI_puzzle_container.__init__(self, game)
        self.tutorial_stages = []
        self.current_stage = 0
        self.stage_object = None

        self.add_stage(
            instructions = ["Hi there!", "I'm Chips! I'm going to show you how to solve PixelPics puzzles!"]
            )
        self.add_stage(
            instructions = ["The goal is to reveal the hidden picture in each puzzle.", "This is done by figuring out which squares are filled and which are empty."]
            )
        self.add_stage(
            instructions = ["Take a look at this one."]
            )
        self.add_stage(
            instructions = ["See the numbers along the edges?", "They tell you the lengths of the filled blocks that can be found on that row or column,", "in the order they appear."]
            )
        self.add_stage(
            instructions = ["This column has only one number, a 2!", "So somewhere in this column there's a single block of 2 filled squares."],
            col_highlights = [[(0,0), (0,4)]]
            )
        self.add_stage(
            instructions = ["This row has two separate numbers, each being a 1.", "So somewhere in this row there are two separated filled squares."],
            row_highlights = [[(3,0), (3,4)]]
            )
        self.add_stage(
            instructions = ["Sounds tricky right? It's actually really easy!"]
            )
        self.add_stage(
            instructions = ["PixelPics puzzles never require any guesswork at all!", "They can always be solved by thinking logically. I'll show you!"]
            )
        self.add_stage(
            instructions = ["Let's start with this column.", "The clue says there's a single block of 5 squares here."],
            col_highlights = [[(0,2), (4,2)]]
            )
        self.add_stage(
            instructions = ["That's the whole height of the board! So we know for sure that they must all be filled in."],
            col_highlights = [[(0,2), (4,2)]]
            )
        self.add_stage(
            instructions = ["Go ahead and fill in those squares by clicking on them with your right mouse button!"],
            alt_instructions = ["Go ahead and fill in those squares by clicking on them with your left mouse button!"],
            col_highlights = [[(0,2), (4,2)]],
            cells_fill = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],
            wrong_cell = "We'll get to the other squares in a second - let's focus on the highlighted ones for now!",
            wrong_input = [
                "Whoops! That was a left click. Be sure to use the RIGHT mouse button to fill in spaces!",
                "Whoops! That was a right click. Be sure to use the LEFT mouse button to fill in spaces!"
              ]
            )
        self.add_stage(
            instructions = ["Great!", "The squares that you figure out will help you solve more of the puzzle!"]
            )
        self.add_stage(
            instructions = ["Take a look at this column.", "The clue is 0, that means there are no filled squares in this column at all!"],
            col_highlights = [[(0,4), (4,4)]]
            )
        self.add_stage(
            instructions = ["When we know for sure that a square isn't filled in,", "we can mark it with an 'X'."],
            col_highlights = [[(0,4), (4,4)]]
            )
        self.add_stage(
            instructions = ["Go ahead and mark those squares as empty with your left mouse button!"],
            alt_instructions = ["Go ahead and mark those squares as empty with your right mouse button!"],
            col_highlights = [[(0,4), (4,4)]],
            cells_empty = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)],
            wrong_cell = "We'll get to the other squares in a second - let's focus on the highlighted ones for now!",
            wrong_input = [
                "Whoops! That was a right click. Be sure to use the LEFT mouse button to mark spaces as empty!",
                "Whoops! That was a left click. Be sure to use the RIGHT mouse button to mark spaces as empty!"
              ]
            )
        self.add_stage(
            instructions = ["Excellent!", "These will help us deduce more of the puzzle too."]
            )
        self.add_stage(
            instructions = ["Remember this row? The clue says there are 2 separated filled squares.", "Hey, we've already found one of them!"],
            row_highlights = [[(3,0), (3,4)]]
            )
        self.add_stage(
            instructions = ["Each block of squares must be separated by at least 1 empty square.", "That means that the squares either side of the filled block must be empty!"],
            cell_highlights = [(3,1), (3,3)]
            )
        self.add_stage(
            instructions = ["Go ahead and mark those spaces as empty with your left mouse button."],
            alt_instructions = ["Go ahead and mark those spaces as empty with your right mouse button."],
            cell_highlights = [(3,1), (3,3)],
            cells_empty = [(3,1), (3,3)],
            wrong_cell = "We'll get to the other squares in a second - let's focus on the highlighted ones for now!",
            wrong_input = [
                "Whoops! That was a right click. Be sure to use the LEFT mouse button to mark spaces as empty!",
                "Whoops! That was a left click. Be sure to use the RIGHT mouse button to mark spaces as empty!"
              ]            
            )
        self.add_stage(
            instructions = ["Fabulous!"]
            )        
        self.add_stage(
            instructions = ["Sometimes there is only 1 remaining place a block of squares could be.", "So the other filled square must be in the highlighted space!"],
            cell_highlights = [(3,0)]
            )
        self.add_stage(
            instructions = ["Go ahead and fill it!"],
            cell_highlights = [(3,0)],
            cells_fill = [(3,0)],
            wrong_cell = "We'll get to the other squares in a second - let's focus on the highlighted one for now!",
            wrong_input = [
                "Whoops! That was a left click. Be sure to use the RIGHT mouse button to fill in spaces!",
                "Whoops! That was a right click. Be sure to use the LEFT mouse button to fill in spaces!"
              ]            
            )
        self.add_stage(
            instructions = ["Bravo!"]
            )        
        self.add_stage(
            instructions = ["Check out this row. The clue says there's a single block of 3. But there are 4 spaces!", "So we don't know for sure exactly where the block starts and ends."],
            row_highlights = [[(0,0), (0,4)]]
            )
        self.add_stage(
            instructions = ["Maybe it's over here..."],
            row_highlights = [[(0,0), (0,2)]]
            )
        self.add_stage(
            instructions = ["Or maybe it's over here?"],
            row_highlights = [[(0,1), (0,3)]]
            )
        self.add_stage(
            instructions = ["Either way there's an overlap of two squares in the middle.", "So we know for sure that those squares must be filled!"],
            row_highlights = [[(0,1), (0,2)]]
            )
        self.add_stage(
            instructions = ["Go ahead and fill that middle square to complete the overlap!"],
            cell_highlights = [(0,1)],
            cells_fill = [(0, 1)],
            wrong_cell = "We'll get to the other squares in a second - let's focus on the highlighted one for now!",
            wrong_input = [
                "Whoops! That was a left click. Be sure to use the RIGHT mouse button to fill in spaces!",
                "Whoops! That was a right click. Be sure to use the LEFT mouse button to fill in spaces!"
              ]            
            )
        self.add_stage(
            instructions = ["You got it!"]
            )
        self.add_stage(
            instructions = ["Take a look at these rows. We've already found the blocks mentioned in the clues!", "Notice that the clues change colour when we've solved them."],
            row_highlights = [[(1,0), (1,4)], [(4,0), (4,4)]]
            )
        self.add_stage(
            instructions = ["That means we know for sure that the other squares on these rows must be empty."],
            row_highlights = [[(1,0), (1,1)], [(4,0), (4,1)]],
            cell_highlights = [(1,3), (4, 3)]
            )
        self.add_stage(
            instructions = ["Go ahead and mark those squares as empty!"],
            row_highlights = [[(1,0), (1,1)], [(4,0), (4,1)]],
            cell_highlights = [(1,3), (4, 3)],
            cells_empty = [(1,0), (1,1), (4,0), (4,1), (1,3), (4, 3)],
            wrong_cell = "We'll get to the other squares in a second - let's focus on the highlighted ones for now!",
            wrong_input = [
                "Whoops! That was a right click. Be sure to use the LEFT mouse button to mark spaces as empty!",
                "Whoops! That was a left click. Be sure to use the RIGHT mouse button to mark spaces as empty!"
              ]            
            )
        self.add_stage(
            instructions = ["Teriffic!"]
            )
        self.add_stage(
            instructions = ["Now there are only a few unfilled squares left.", "How about you take it from here?"]
            )
        self.add_stage(
            instructions = ["Remember, only mark squares that you know for sure. Good luck!"]
            )
        

    def add_stage(
          self, instructions = [""], alt_instructions = [""], row_highlights = [], col_highlights = [], cell_highlights = [], \
          cells_fill = [], cells_empty = [], wrong_cell = "", wrong_input = ["", ""]
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
            'wrong_input' : wrong_input
            }
        self.tutorial_stages.append(empty_stage)
        

    def create_puzzle_element(self):
        self.puzzle = GUI_tutorial_puzzle(self.game, self)


    def finish_stage(self):
        if self.stage_object is None:
            return
        self.stage_object.Kill()
        self.stage_object = None
        self.current_stage += 1


    def next_stage(self):
        if not self.stage_object is None:
            return
        
        self.stage_object = GUI_tutorial_stage(self.game, self, self.tutorial_stages[self.current_stage])



class GUI_tutorial_puzzle(GUI_puzzle):

    def Execute(self):
        GUI_puzzle.Execute(self)
        
        if self.state == PUZZLE_STATE_SOLVING:
            if self.parent.current_stage < len(self.parent.tutorial_stages):
                self.parent.next_stage()



class GUI_tutorial_stage(GUI_element):
    def __init__(self, game, parent, stage):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.stage = stage
        self.x, self.y = 0, 0
        self.z = Z_GUI_OBJECT_LEVEL_7 - 1

        self.width, self.height = 0, 0
        self.click_to_continue = False
        
        if self.stage['cells_fill'] == [] and self.stage['cells_empty'] == []:
            self.width = self.game.settings['screen_width']
            self.height = self.game.settings['screen_height']
            self.click_to_continue = True

        self.objs = []

        text_y_pos = 50
        for text_string in self.stage['instructions']:
            text = Text(self.game.core.media.fonts['tutorial_instructions'], 20, text_y_pos, TEXT_ALIGN_TOP_LEFT, text_string)
            text.colour = (1.0, .5, 0.0)
            text.shadow = 1
            text.shadow_colour = (.6, .4, .2, .5)
            text.z = self.z
            self.objs.append(text)
            text_y_pos += text.text_height + 5

        if self.click_to_continue:
            text = Text(self.game.core.media.fonts['tutorial_click_to_continue'], self.game.settings['screen_width'] / 2, text_y_pos + 20, TEXT_ALIGN_TOP, "[ Click to continue ]")
            text.colour = (.8, .3, 0.0)
            text.shadow = 2
            text.shadow_colour = (.5, .3, .1, .5)
            text.z = self.z
            self.objs.append(text)
            
        self.gui_init()


    def mouse_left_up(self):
        if self.click_to_continue:
            self.parent.finish_stage()


    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.objs:
            x.Kill()
