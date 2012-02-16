"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# Debug values
DEBUG_SHOW_FPS = True

# States
GAME_STATE_LOGO = 1
GAME_STATE_MENU = 2
GAME_STATE_PUZZLE = 3
GAME_STATE_DESIGNER = 4
GAME_STATE_TEST = 5

# GUI states
GUI_STATE_LOGO = 1
GUI_STATE_MENU = 2
GUI_STATE_PUZZLE = 3
GUI_STATE_DESIGNER_PACKS = 4
GUI_STATE_DESIGNER_PUZZLES = 5
GUI_STATE_DESIGNER_DESIGNER = 6

# Puzzle states
PUZZLE_STATE_READY_MESSAGE = 1
PUZZLE_STATE_SOLVING = 2
PUZZLE_STATE_FAILED = 3
PUZZLE_STATE_CLEARED = 4

# Drawing tool states
DRAWING_TOOL_STATE_NORMAL = 1
DRAWING_TOOL_STATE_DRAW = 2
DRAWING_TOOL_STATE_FILL = 3
DRAWING_TOOL_STATE_RECTANGLE = 4
DRAWING_TOOL_STATE_CIRCLE = 5
DRAWING_TOOL_STATE_PIPETTE = 6

# Z vals
Z_STOMPYBLONDIE_LOGO = 1000
Z_GUI = -500
Z_GUI_CONTAINERS = -550
Z_GUI_OBJECT_LEVEL_1 = -560
Z_GUI_OBJECT_LEVEL_2 = -570
Z_GUI_OBJECT_LEVEL_3 = -580
Z_GUI_OBJECT_LEVEL_4 = -590
Z_GUI_OBJECT_LEVEL_5 = -600
Z_GUI_OBJECT_LEVEL_6 = -650
Z_GUI_OBJECT_LEVEL_7 = -660
Z_GUI_OBJECT_LEVEL_8 = -670
Z_GUI_OBJECT_LEVEL_9 = -680
Z_GUI_OBJECT_LEVEL_10 = -690
Z_MOUSE = -1000

# Process priorities
PRIORITY_MAIN_GAME = 1000
PRIORITY_GUI_ELEMENTS = 900
PRIORITY_GUI = 800
PRIORITY_MARKERS = 700

# Backgrounds
BACKGROUND_TYPE_COLOUR = 1
BACKGROUND_TYPE_IMAGE = 2

BACKGROUNDS = {
    'blue' : {
        'type' : BACKGROUND_TYPE_COLOUR,
        'data' : (.7,1.0,1.0,1.0)
        },
    'green' : {
        'type' : BACKGROUND_TYPE_COLOUR,
        'data' : (.5,1.0,.5,1.0)
        },
    'red' : {
        'type' : BACKGROUND_TYPE_COLOUR,
        'data' : (1.0,.5,.5,1.0)
        },
    'purple' : {
        'type' : BACKGROUND_TYPE_COLOUR,
        'data' : (.7,.6,.7,1.0)
        },    
    'yellow' : {
        'type' : BACKGROUND_TYPE_COLOUR,
        'data' : (1.0,1.0,.5,1.0)
        },
    }

# Game related consts
PUZZLE_HINT_GRADIENT_COLOURS_HORISONTAL = (
    (1.0, 1.0, 1.0, 0.0),
    (.5, .7, .8, 1.0),
    (.5, .7, .8, 1.0),
    (1.0, 1.0, 1.0, 0.0)
    )
PUZZLE_HINT_GRADIENT_COLOURS_VERTICAL = (
    (1.0, 1.0, 1.0, 0.0),
    (1.0, 1.0, 1.0, 0.0),
    (.5, .7, .8, 1.0),
    (.5, .7, .8, 1.0)
    )
PUZZLE_HINT_COMPLETED_COLOUR = (.8, .8, .8)
PUZZLE_HINT_COLOUR = (1.0, 1.0, 1.0)

INITIAL_LIVES = 5

DESIGNER_PUZZLE_ICON_HEIGHT = 43.0

PUZZLE_VERIFIER_ITERATIONS = 10
PUZZLE_VERIFIER_MAX_ITERATIONS = 200

MAX_UNDO_STACK = 100
