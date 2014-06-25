"""
PixelPics - Nonograme game
Copyright (c) 2014 Stompy Blondie Games http://stompyblondie.com
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
    height = 620
    width = 420
    objs = {}
    widgets = {}

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        if self.game.manager.can_has_cat_mode():
            self.height = 700
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

        self.objs['title_graphics'] = GUI_options_title(self.game, self, "Graphics", 50)
        self.objs['title_sound'] = GUI_options_title(self.game, self, "Audio", 160)
        self.objs['title_gameplay'] = GUI_options_title(self.game, self, "Gameplay", 330)
        self.objs['mouse_image'] = GUI_options_mouse_image(self.game, self)

        self.widgets['resolution'] = GUI_options_resolution(self.game, self)
        self.widgets['full_screen'] = GUI_options_full_screen(self.game, self)
        self.widgets['music_on'] = GUI_options_music_on(self.game, self)
        self.widgets['music_vol'] = GUI_options_music_volume(self.game, self)
        self.widgets['sound_effects_on'] = GUI_options_sound_effects_on(self.game, self)
        self.widgets['sound_effects_vol'] = GUI_options_sound_effects_volume(self.game, self)
        self.widgets['bump_scroll'] = GUI_options_bump_scroll(self.game, self)
        self.widgets['lock_drawing'] = GUI_options_lock_drawing(self.game, self)
        self.widgets['cancel_button'] = GUI_options_cancel_button(self.game, self)
        self.widgets['apply_button'] = GUI_options_apply_button(self.game, self)

        if self.game.manager.can_has_cat_mode():
            self.objs['title_cat_mode'] = GUI_options_title(self.game, self, "Meow?", 570)
            self.widgets['cat_mode'] = GUI_options_cat_mode(self.game, self)

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
        self.game.core.settings.mouse_left_empty = bool(self.objs['mouse_image'].current_value)
        self.game.core.settings.bump_scroll = bool(self.widgets['bump_scroll'].current_value)
        self.game.core.settings.lock_drawing = bool(self.widgets['lock_drawing'].current_value)
        if self.game.manager.can_has_cat_mode():
            self.game.core.settings.cat_mode = bool(self.widgets['cat_mode'].current_value)
        else:
            self.game.core.settings.cat_mode = False
        self.game.core.settings.save()

        self.game.settings['mouse_left_empty'] = self.game.core.settings.mouse_left_empty
        self.game.settings['bump_scroll'] = self.game.core.settings.bump_scroll
        self.game.settings['lock_drawing'] = self.game.core.settings.lock_drawing

        if res_or_full_screen_changed:
            GUI_element_dialog_box(
                self.game,
                self.parent,
                "Notice",
                ["You will need to restart PixelPics before your", "settings will be applied."]
                )

        # alter music settings were appropriate
        self.game.set_music_volume(self.game.core.settings.music_vol)
        
        if not self.game.game_state in [GAME_STATE_PUZZLE, GAME_STATE_TEST]:
            if self.game.core.settings.music_on:
                self.game.ensure_correct_music_playing()
            else:
                self.game.fade_out_music()
        
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
        self.name_text = Text(self.game.core.media.fonts['window_subtitle'], self.x, self.y, TEXT_ALIGN_TOP_LEFT, str(title_text))
        self.name_text.z = self.z
        self.name_text.colour = (0.95, 0.58, 0.09)
        self.name_text.shadow = 1
        self.name_text.shadow_colour = (0.5, 0.5, 0.5)


    def On_Exit(self):
        self.name_text.Kill()



class GUI_options_cancel_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Cancel"

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + (self.parent.width / 2) + 13
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
        self.x = self.parent.x + (self.parent.width / 2) - 87
        self.y = self.parent.y + self.parent.height - 45
        self.z = self.parent.z - 2
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.apply_and_save()



class GUI_options_resolution(GUI_element_dropdown):
    display_width = 170

    dropdown_options = []

    selected_item = 0
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.display_x = self.parent.x + 180
        self.display_y = self.parent.y + 90
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

        self.name_text = Text(self.game.core.media.fonts["window_text"], self.parent.x + 30, self.display_y + 7, TEXT_ALIGN_TOP_LEFT, "Screen resolution")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.3, 0.3, 0.3)


    def On_Exit(self):
        GUI_element_dropdown.On_Exit(self)
        self.name_text.Kill()



class GUI_options_full_screen(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 180
        self.y = self.parent.y + 120
        self.z = self.parent.z - 3
        self.current_value = bool(self.game.core.settings.full_screen)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["window_text"], self.parent.x + 30, self.y + 7, TEXT_ALIGN_TOP_LEFT, "Full screen")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.3, 0.3, 0.3)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.name_text.Kill()


class GUI_options_music_on(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 180
        self.y = self.parent.y + 200
        self.z = self.parent.z - 3
        self.current_value = bool(self.game.core.settings.music_on)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["window_text"], self.parent.x + 30, self.y + 7, TEXT_ALIGN_TOP_LEFT, "Music on")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.3, 0.3, 0.3)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.name_text.Kill()


class GUI_options_sound_effects_on(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 180
        self.y = self.parent.y + 260
        self.z = self.parent.z - 3
        self.current_value = bool(self.game.core.settings.sound_effects_on)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["window_text"], self.parent.x + 30, self.y + 7, TEXT_ALIGN_TOP_LEFT, "Sound effects on")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.3, 0.3, 0.3)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.name_text.Kill()



class GUI_options_music_volume(GUI_element_slider):
    min_value = 0
    max_value = 128
    width = 170

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 180
        self.y = self.parent.y + 237
        self.z = self.parent.z - 3
        self.current_value = int(self.game.core.settings.music_vol)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["window_text"], self.parent.x + 30, self.y, TEXT_ALIGN_TOP_LEFT, "Music volume")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.3, 0.3, 0.3)


    def slider_dragged(self):
        self.game.set_music_volume(self.current_value)

    
    def On_Exit(self):
        GUI_element_slider.On_Exit(self)
        self.name_text.Kill()



class GUI_options_sound_effects_volume(GUI_element_slider):
    min_value = 0
    max_value = 128
    width = 170

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 180
        self.y = self.parent.y + 297
        self.z = self.parent.z - 3
        self.current_value = int(self.game.core.settings.sound_effects_vol)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["window_text"], self.parent.x + 30, self.y, TEXT_ALIGN_TOP_LEFT, "Sound volume")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.3, 0.3, 0.3)


    def On_Exit(self):
        GUI_element_slider.On_Exit(self)
        self.name_text.Kill()



class GUI_options_mouse_image(GUI_element):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.x = self.parent.x + (self.parent.width / 2)
        self.y = self.parent.y + 430
        self.z = self.parent.z - 2
        self.image = self.game.core.media.gfx['gui_mouse']
        self.mouse_key_left = GUI_options_mouse_key_left(self.game, self)
        self.mouse_key_right = GUI_options_mouse_key_right(self.game, self)
        self.current_value = self.game.core.settings.mouse_left_empty
        self.setting_button = GUI_options_mouse_setting_button(self.game, self)


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.mouse_key_left.Kill()
        self.mouse_key_right.Kill()


    def get_screen_draw_position(self):
        return (self.x - (self.image.width/2), self.y - (self.image.height/2))



class GUI_options_mouse_key_left(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x - 20
        self.y = self.parent.y - 20
        self.z = self.parent.z - 1
        self.text = Text(self.game.core.media.fonts['options_mouse_button'], self.x - 60, self.y - 20, TEXT_ALIGN_BOTTOM_RIGHT, "wub wub")
        self.text.z = self.z
        self.text.colour = (0.3, 0.3, 0.3)
        self.tile_image = None

        self.draw_strategy = "primitive_line"
        self.primitive_line_colour = ((.6, .6, .6, 1.0), (1.0, 1.0, 1.0, 0.3))
        self.primitive_line_position = ((self.x, self.y), ((self.x - 100, self.y - 20)))


    def Execute(self):
        if not self.tile_image is None:
            self.tile_image.Kill()
        
        if self.parent.current_value:
            self.text.text = "Mark empty"
            self.tile_image = GUI_options_mouse_tile_image_left(self.game, self, "gui_puzzle_cell_white")
        else:
            self.text.text = "Mark filled"
            self.tile_image = GUI_options_mouse_tile_image_left(self.game, self, "gui_puzzle_cell_black")


    def On_Exit(self):
        if not self.tile_image is None:
            self.tile_image.Kill()
        self.text.Kill()



class GUI_options_mouse_key_right(Process):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x - 20
        self.y = self.parent.y - 20
        self.z = self.parent.z - 1
        self.text = Text(self.game.core.media.fonts['options_mouse_button'], self.x + 94, self.y - 20, TEXT_ALIGN_BOTTOM_LEFT, "boom boom tish")
        self.text.z = self.z
        self.text.colour = (0.3, 0.3, 0.3)
        self.tile_image = None

        self.draw_strategy = "primitive_line"
        self.primitive_line_colour = ((.6, .6, .6, 1.0), (1.0, 1.0, 1.0, 0.3))
        self.primitive_line_position = ((self.x + 32, self.y), ((self.x + 132, self.y - 20)))


    def Execute(self):
        if not self.tile_image is None:
            self.tile_image.Kill()
        
        if self.parent.current_value:
            self.text.text = "Mark filled"
            self.tile_image = GUI_options_mouse_tile_image_right(self.game, self, "gui_puzzle_cell_black")
        else:
            self.text.text = "Mark empty"
            self.tile_image = GUI_options_mouse_tile_image_right(self.game, self, "gui_puzzle_cell_white")


    def On_Exit(self):
        if not self.tile_image is None:
            self.tile_image.Kill()        
        self.text.Kill()



class GUI_options_mouse_tile_image_left(Process):
    def __init__(self, game, parent, image):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x - 100
        self.y = self.parent.y
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx[image]
        self.scale = .75 if image == "gui_puzzle_cell_white" else .5


    def get_screen_draw_position(self):
        return (self.x - ((self.image.width/2) * self.scale), self.y - ((self.image.height/2) * self.scale))



class GUI_options_mouse_tile_image_right(Process):
    def __init__(self, game, parent, image):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 130
        self.y = self.parent.y
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx[image]
        self.scale = .75 if image == "gui_puzzle_cell_white" else .5


    def get_screen_draw_position(self):
        return (self.x - ((self.image.width/2) * self.scale), self.y - ((self.image.height/2) * self.scale))



class GUI_options_mouse_setting_button(GUI_element_button):
    generic_button = True
    generic_button_text = "Swap Buttons"

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 50
        self.y = self.parent.y + 16
        self.z = self.parent.z - 2
        self.gui_init()


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.current_value = True if not self.parent.current_value else False



class GUI_options_bump_scroll(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 260
        self.y = self.parent.y + 500
        self.z = self.parent.z - 3
        self.current_value = bool(self.game.core.settings.bump_scroll)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["window_text"], self.parent.x + 30, self.y + 7, TEXT_ALIGN_TOP_LEFT, "Enable bump scrolling")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.3, 0.3, 0.3)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.name_text.Kill()



class GUI_options_lock_drawing(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 260
        self.y = self.parent.y + 530
        self.z = self.parent.z - 3
        self.current_value = bool(self.game.core.settings.lock_drawing)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["window_text"], self.parent.x + 30, self.y + 7, TEXT_ALIGN_TOP_LEFT, "Lock drawing to row/column")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.3, 0.3, 0.3)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.name_text.Kill()



class GUI_options_cat_mode(GUI_element_yes_no_radios):
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 260
        self.y = self.parent.y + 610
        self.z = self.parent.z - 3
        self.current_value = bool(self.game.core.settings.cat_mode)
        self.gui_init()

        self.name_text = Text(self.game.core.media.fonts["window_text"], self.parent.x + 30, self.y + 7, TEXT_ALIGN_TOP_LEFT, "Cat mode")
        self.name_text.z = self.z - 1
        self.name_text.colour = (0.3, 0.3, 0.3)


    def On_Exit(self):
        GUI_element_yes_no_radios.On_Exit(self)
        self.name_text.Kill()
