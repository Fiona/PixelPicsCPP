"""
PixelPics - Nonograme game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports

# Game engine imports
from core import *

# Game imports
from consts import *
from helpers  import *
from gui.gui_elements import *



class GUI_options(GUI_element_window):
    title = "Options"
    height = 400
    width = 400
    objs = {}
    widgets = {}

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()


    def Execute(self):
        GUI_element_window.Execute(self)
        if self.game.core.Keyboard_key_released(key.ESCAPE):
            self.Kill()
            

    def gui_init(self):
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.x = (self.game.settings['screen_width'] / 2) - (self.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) - (self.height / 2)
        GUI_element_window.gui_init(self)

        self.objs['title_graphics'] = GUI_options_title(self.game, self, "Graphics", 30)
        self.objs['title_sound'] = GUI_options_title(self.game, self, "Audio", 120)
        self.objs['title_gameplay'] = GUI_options_title(self.game, self, "Gameplay", 250)

        self.widgets['resolution'] = GUI_options_resolution(self.game, self)
        self.widgets['full_screen'] = GUI_options_full_screen(self.game, self)
        #self.widgets['music_on'] = GUI_options_music_on(self.game, self)
        #self.widgets['sound_effects_on'] = GUI_options_sound_effects_on(self.game, self)

        self.game.gui.block_gui_keyboard_input = True
        self.x = 0
        self.y = 0
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']

        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_width = self.x + self.width
        self.primitive_square_height = self.y + self.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_colour = (0.0, 0.0, 0.0, .4)


    def On_Exit(self):
        GUI_element_window.On_Exit(self)
        self.game.gui.block_gui_keyboard_input = False
        for x in self.objs:
            self.objs[x].Kill()



class GUI_options_title(Process):
    def __init__(self, game, parent, title_text, y_offset):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 20
        self.y = self.parent.y + y_offset
        self.z = self.parent.z - 2
        self.text = Text(self.game.core.media.fonts['options_title'], self.x, self.y, TEXT_ALIGN_TOP_LEFT, str(title_text))
        self.text.z = self.z
        self.text.colour = (0.0, 0.0, 0.0)

        self.draw_strategy = "primitive_line"
        self.primitive_line_colour = ((.6, .6, .6, 1.0), (1.0, 1.0, 1.0, 0.0))
        self.primitive_line_position = ((self.x + 5, self.y + 20), ((self.x + self.parent.width - 30, self.y + 20)))


    def On_Exit(self):
        self.text.Kill()



class GUI_options_resolution(GUI_element_dropdown):
    display_width = 170
    display_height = 25

    dropdown_options = [
        {'text' : "1024 x 768", 'data' : (1024, 768)},
        {'text' : "1920 x 1080", 'data' : (1920, 1080)},
        ]

    selected_item = 0
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.display_x = self.parent.x + 175
        self.display_y = self.parent.y + 55
        self.display_z = self.parent.z - 3
        self.gui_init()

        self.text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.display_y, TEXT_ALIGN_TOP_LEFT, "Screen resolution")
        self.text.z = self.z - 1
        self.text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_dropdown.On_Exit(self)
        self.text.Kill()



class GUI_options_full_screen(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 175
        self.y = self.parent.y + 85
        self.z = self.parent.z - 3
        self.gui_init()

        self.text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.y, TEXT_ALIGN_TOP_LEFT, "Full screen?")
        self.text.z = self.z - 1
        self.text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.text.Kill()


"""
class GUI_options_music_on(GUI_element_checkbox):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 175
        self.y = self.parent.y + 160
        self.z = self.parent.z - 3
        self.gui_init()

        self.text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.y, TEXT_ALIGN_TOP_LEFT, "Music")
        self.text.z = self.z - 1
        self.text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_checkbox.On_Exit(self)
        self.text.Kill()



class GUI_options_sound_effects_on(GUI_element_checkbox):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 175
        self.y = self.parent.y + 175
        self.z = self.parent.z - 3
        self.gui_init()

        self.text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.y, TEXT_ALIGN_TOP_LEFT, "Sound effects")
        self.text.z = self.z - 1
        self.text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_checkbox.On_Exit(self)
        self.text.Kill()


"""
