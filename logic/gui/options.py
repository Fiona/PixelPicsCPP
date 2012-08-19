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
        self.z = Z_GUI_OBJECT_LEVEL_10
        self.x = (self.game.settings['screen_width'] / 2) - (self.width / 2)
        self.y = (self.game.settings['screen_height'] / 2) - (self.height / 2)
        GUI_element_window.gui_init(self)

        self.objs['title_graphics'] = GUI_options_title(self.game, self, "Graphics", 30)
        self.objs['title_sound'] = GUI_options_title(self.game, self, "Audio", 120)
        self.objs['title_gameplay'] = GUI_options_title(self.game, self, "Gameplay", 275)

        self.widgets['resolution'] = GUI_options_resolution(self.game, self)
        self.widgets['full_screen'] = GUI_options_full_screen(self.game, self)
        self.widgets['music_on'] = GUI_options_music_on(self.game, self)
        self.widgets['music_vol'] = GUI_options_music_volume(self.game, self)
        self.widgets['sound_effects_on'] = GUI_options_sound_effects_on(self.game, self)
        self.widgets['sound_effects_vol'] = GUI_options_sound_effects_volume(self.game, self)
        self.widgets['cancel_button'] = GUI_options_cancel_button(self.game, self)
        self.widgets['apply_button'] = GUI_options_apply_button(self.game, self)
        
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


    def apply_and_save(self):
        selected_res = self.widgets['resolution'].dropdown_options[self.widgets['resolution'].selected_item]['data']
        res_or_full_screen_changed = False
        if float(self.game.core.settings.screen_width) != float(selected_res[0]) or float(self.game.core.settings.screen_height) != float(selected_res[1]):
            res_or_full_screen_changed = True
        
        if bool(self.game.core.settings.full_screen) != bool(self.widgets['full_screen'].current_value):
            res_or_full_screen_changed = True

        self.game.core.settings.screen_width = float(selected_res[0])
        self.game.core.settings.screen_height = float(selected_res[1])
        self.game.core.settings.full_screen = bool(self.widgets['full_screen'].current_value)
        self.game.core.settings.music_on = bool(self.widgets['music_on'].current_value)
        self.game.core.settings.sound_effects_on = bool(self.widgets['sound_effects_on'].current_value)
        self.game.core.settings.music_vol = int(self.widgets['music_vol'].current_value)
        self.game.core.settings.sound_effects_vol = int(self.widgets['sound_effects_vol'].current_value)
        self.game.core.settings.save()

        if res_or_full_screen_changed:
            GUI_element_dialog_box(
                self.game,
                self.parent,
                "Notice",
                ["You will need to restart PixelPics before your", "settings will be applied."]
                )
            
        self.Kill()
    

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
        self.name_text = Text(self.game.core.media.fonts['options_title'], self.x, self.y, TEXT_ALIGN_TOP_LEFT, str(title_text))
        self.name_text.z = self.z
        self.name_text.colour = (0.0, 0.0, 0.0)

        self.draw_strategy = "primitive_line"
        self.primitive_line_colour = ((.6, .6, .6, 1.0), (1.0, 1.0, 1.0, 0.0))
        self.primitive_line_position = ((self.x + 5, self.y + 20), ((self.x + self.parent.width - 30, self.y + 20)))


    def On_Exit(self):
        self.name_text.Kill()



class GUI_options_cancel_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Cancel"

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + self.parent.width - 160
        self.y = self.parent.y + self.parent.height - 45
        self.z = self.parent.z - 2
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.Kill()



class GUI_options_apply_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Apply"

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + self.parent.width - 80
        self.y = self.parent.y + self.parent.height - 45
        self.z = self.parent.z - 2
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.apply_and_save()



class GUI_options_resolution(GUI_element_dropdown):
    display_width = 170
    display_height = 25

    dropdown_options = []

    selected_item = 0
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.display_x = self.parent.x + 175
        self.display_y = self.parent.y + 55
        self.display_z = Z_GUI_OBJECT_LEVEL_11

        i = 0
        self.dropdown_options = []
        for x in self.game.core.allowed_screen_sizes:
            self.dropdown_options.append(
                  {
                    'text' : str(int(x[0])) + " x " + str(int(x[1])),
                    'data' : (x[0], x[1])
                  }
                )
            if self.game.core.settings.screen_width == x[0] and self.game.core.settings.screen_height == x[1]:
                self.selected_item = i
            i += 1
        
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.display_y, TEXT_ALIGN_TOP_LEFT, "Screen resolution")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_dropdown.On_Exit(self)
        self.name_text.Kill()



class GUI_options_full_screen(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 175
        self.y = self.parent.y + 85
        self.z = self.parent.z - 3
        self.current_value = bool(self.game.core.settings.full_screen)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.y, TEXT_ALIGN_TOP_LEFT, "Full screen")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.name_text.Kill()


class GUI_options_music_on(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 175
        self.y = self.parent.y + 150
        self.z = self.parent.z - 3
        self.current_value = bool(self.game.core.settings.music_on)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.y, TEXT_ALIGN_TOP_LEFT, "Music on")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.name_text.Kill()


class GUI_options_sound_effects_on(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 175
        self.y = self.parent.y + 210
        self.z = self.parent.z - 3
        self.current_value = bool(self.game.core.settings.sound_effects_on)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.y, TEXT_ALIGN_TOP_LEFT, "Sound effects on")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.name_text.Kill()



class GUI_options_music_volume(GUI_element_slider):
    min_value = 0
    max_value = 100
    width = 170

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 175
        self.y = self.parent.y + 180
        self.z = self.parent.z - 3
        self.current_value = int(self.game.core.settings.music_vol)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.y, TEXT_ALIGN_TOP_LEFT, "Music volume")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_slider.On_Exit(self)
        self.name_text.Kill()



class GUI_options_sound_effects_volume(GUI_element_slider):
    min_value = 0
    max_value = 100
    width = 170

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 175
        self.y = self.parent.y + 240
        self.z = self.parent.z - 3
        self.current_value = int(self.game.core.settings.sound_effects_vol)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["basic"], self.parent.x + 20, self.y, TEXT_ALIGN_TOP_LEFT, "Sound volume")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.0, 0.0, 0.0)


    def On_Exit(self):
        GUI_element_slider.On_Exit(self)
        self.name_text.Kill()
