"""
PixelPics - Nonograme game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# Game engine imports
from core import *

# Python imports
import pickle

# Game imports
from consts import *
from helpers  import *

# Consts
GUI_SCROLL_ELEMENT_SCROLL_AMOUNT = 20



class GUI_element(Process):
    """
    All GUI elements extend from this template.
    It must have a position and a width/height. This enables it to take mouse input.
    The handle_input() method must only be directly called by the overal parent element, all
    children will be polled and the correct response will be sent back up the chain.
    The Z order matters for how elements will be polled.
    """
    parent = None
    children = []
    width = 0
    height = 0
    disable = False
    _currently_hovered = False
    scroll_element = None


    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()


    def gui_init(self):
        """
        Must be called at the start of the execute method. Requres self.parent to be set though.
        """
        if not self.parent is None:
            self.parent.children.append(self)
        self.children = []
        self.priority = PRIORITY_GUI_ELEMENTS


    def Execute(self):
        self.update()


    def update(self):
        """
        Stub designed to be called every frame.
        """
        pass


    def mouse_over(self):
        """
        Override this method to respond to the mouse hovering.
        Called AFTER mouse_enter if that method gets called.
        """
        pass


    def mouse_not_over(self):
        """
        Override this method to respond to the mouse not being over the element.
        Called AFTER mouse_out if that method gets called.
        """
        pass


    def mouse_enter(self):
        """
        Override this method to respond to the mouse entering the element.
        """
        pass


    def mouse_out(self):
        """
        Override this method if to respond to the mouse leaving the element.
        """
        pass


    def mouse_left_down(self):
        """
        Override this method to respond to the left mouse button being held down over the element.
        """
        pass


    def mouse_left_up(self):
        """
        Override this method to respond to the left mouse button being released on the element.
        """
        pass


    def mouse_right_down(self):
        """
        Override this method to respond to the right mouse button being held down over the element.
        """
        pass


    def mouse_right_up(self):
        """
        Override this method to respond to the right mouse button being released on the element.
        """
        pass

    
    def mouse_middle_down(self):
        """
        Override this method to respond to the middle mouse button being held down over the element.
        """
        pass


    def mouse_middle_up(self):
        """
        Override this method to respond to the middle mouse button being released on the element.
        """
        pass


    def mouse_wheel_down(self):
        """
        Override this method to respond to the mouse wheel spinning when the mouse is being held down over the element.
        """
        if not self.scroll_element is None:
            self.scroll_element.mouse_wheel_down()


    def mouse_wheel_up(self):
        """
        Override this method to respond to the mouse wheel spinning when the mouse is being held down over the element.
        """
        if not self.scroll_element is None:
            self.scroll_element.mouse_wheel_up()


    def handle_input(self, coordinates, current_best = None):
        """
        Returns the pointer to the GUI object that is under the screen coordinates passed in to the coordinates parameter.
        current_best should be None unless called from this method.
        """
        if self.disable:
            return current_best
        
        if self.is_coords_in_bounds(coordinates):
            if current_best is None or self.z <= current_best.z:
                current_best = self
        else:
            if self._currently_hovered:
                self.mouse_out()
                self._currently_hovered = False
            self.mouse_not_over()
            
        for child in self.children:
            current_best = child.handle_input(coordinates, current_best)

        return current_best


    def is_coords_in_bounds(self, coordinates):
        if not self.scroll_element is None:
            if not (coordinates[0] > self.scroll_element.x and coordinates[0] < self.scroll_element.x + self.scroll_element.width and coordinates[1] > self.scroll_element.y and coordinates[1] < self.scroll_element.y + self.scroll_element.height):
                return False
            x = self.x + self.scroll_element.x
            y = self.y + self.scroll_element.y - self.scroll_element.contents_scroll_location
        else:
            x = self.x
            y = self.y
            
        return (coordinates[0] > x and coordinates[0] < x + self.width and coordinates[1] > y and coordinates[1] < y + self.height)


    def get_screen_draw_position(self):
        if not self.scroll_element is None:
            self.clip = (self.scroll_element.x, self.scroll_element.y, self.scroll_element.width, self.scroll_element.height)
            return (self.x + self.scroll_element.x, self.y + self.scroll_element.y - self.scroll_element.contents_scroll_location)
        else:
            self.clip = (0, 0, 0, 0)
            return (self.x, self.y)
        

    def On_Exit(self):
        kids = list(self.children)
        for child in kids:
            child.Kill()
        self.children = []

        if not self.parent is None and self in self.parent.children:
            self.parent.children.remove(self)



class GUI_element_button(GUI_element):
    """
    Button object. Does generic drawing and sequence frame switching.
    """
    # Set if this is a generic button, set to false if we're specifying an image
    generic_button = True

    # The text for the generic button 
    generic_button_text = ""

    # True if this is a togglable button. Make sure you call mouse_left_up_toggle when assigning a mouse_left_up event.
    toggle_button = False

    # Use this to change the initial toggle state, but try not to mess with it otherwise
    toggle_state = False

    # Set to True to disable. If not generic, image_seq 3 is used. Can be switched on and off at will.
    disabled = False

    # Set false to disable clicks and stuff 
    play_sound = True

    generic_button_text_object = None
    sequence_count = 0

    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
    

    def gui_init(self):
        """
        Must be called at the start of the execute method.
        Make sure that image has been set before calling this. A None image will draw a generic button.
        """
        GUI_element.gui_init(self)

        self.hover_sound = False
        
        if not self.image is None:
            self.generic_button = False
            self.width = self.image.width if self.width == 0 else self.width
            self.height = self.image.height if self.height == 0 else self.height
        else:
            # Set up a generic button
            self.generic_button = True
            self.image = self.game.core.media.gfx['gui_button_generic_background']
            self.draw_strategy = "gui_button"

            # fixed height
            self.height = 30
            
            # Create the text
            self.generic_button_text_object = Text(self.game.core.media.fonts["generic_buttons"], self.x, self.y + (self.height / 2), TEXT_ALIGN_CENTER, self.generic_button_text)
            self.generic_button_text_object.z = self.z - 1
            self.generic_button_text_object.colour = (1.0,1.0,1.0)
            
            # Set up the width, if we have a larger than normal width then we want to centre the text.
            if self.width < self.generic_button_text_object.text_width + 20:
                self.width = self.generic_button_text_object.text_width + 20
            self.generic_button_text_object.x += (self.width / 2)
            
        self.sequence_count = self.image.num_of_frames
        self.draw_strategy_call_parent = False
        

    def update(self):
        self.image_sequence = 1
        if self.generic_button:
            self.generic_button_text_object.colour = (1.0, 1.0, 1.0)
        GUI_element.update(self)
        if self.disabled:
            self.image_sequence = 4
            return
        if self.toggle_button and self.toggle_state:
            self.image_sequence = 3 if self.sequence_count > 3 else 0
        elif self.toggle_button:
            self.image_sequence = 1


    def mouse_left_up_toggle(self):
        if self.disabled:
            return
        self.toggle_state = True if self.toggle_state == False else False


    def mouse_left_up(self):
        if self.play_sound:
            self.game.core.media.sfx['button_click'].play(0)
        

    def mouse_over(self):
        if self.disabled:
            return
        if self.play_sound and not self.hover_sound:
            self.game.core.media.sfx['button_hover'].play(0)
            self.hover_sound = True
        if self.sequence_count > 1 and not (self.toggle_button and self.toggle_state):
            self.image_sequence = 2


    def mouse_out(self):
        self.hover_sound = False


    def mouse_left_down(self):
        if self.disabled:
            return
        if self.sequence_count > 2:
            self.image_sequence = 3
        if self.generic_button:
            self.generic_button_text_object.colour = (.84,.84,.84)


    def On_Exit(self):
        """
        Cleans up generic button text.
        """
        GUI_element.On_Exit(self)
        if self.generic_button:
            self.generic_button_text_object.Kill()



class GUI_element_window_frame(GUI_element):
    """
    Generic window frame.
    Used by GUI_Window to simply draw the background of it.
    """
    def __init__(self, game, parent, x, y, width, height):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.z = self.parent.z - 1
        self.draw_strategy = "gui_window_frame"



class GUI_element_window(GUI_element):
    """ Provides a window frame. Windows should subclass this. """
    # Set to the text that needs to appear as the title of the window    
    title = ""
    
    # Set to the desired pixel height of the window
    height = 0
    
    # Set to the desired width of the window
    width = 0

    frame = None
    text = None
    
    def gui_init(self):
        GUI_element.gui_init(self)
        self.frame = GUI_element_window_frame(self.game, self, self.x, self.y, self.width, self.height)
        self.text = Text(self.game.core.media.fonts['window_title'], self.x + self.width / 2, self.y + 5.0, TEXT_ALIGN_TOP,  self.title)
        self.text.colour = (0.95, 0.58, 0.09)
        self.text.shadow = 2
        self.text.shadow_colour = (0.5, 0.5, 0.5)
        self.text.z = self.z - 2

    
    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text.Kill()



class GUI_element_dialog_box(GUI_element):
    title = ""
    message = []
    caption_image = None
    
    frame = None
    title_text = None
    message_text = []
    caption_image_obj = None

    min_box_height = 100
    min_box_width = 300    
       
    def __init__(self, game, parent = None, title = "test", message = ["test message"], caption_image = None, callback = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.title = title
        self.message = message
        self.caption_image = caption_image
        self.callback = callback
        self.gui_init()
        

    def gui_init(self):
        GUI_element.gui_init(self)
        self.z = Z_GUI_OBJECT_LEVEL_9


        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']

        # Create the title text objects
        self.title_text = Text(self.game.core.media.fonts['window_title'], 0.0, 0.0, TEXT_ALIGN_TOP,  self.title)
        self.title_text.colour = (0.95, 0.58, 0.09)
        self.title_text.shadow = 2
        self.title_text.shadow_colour = (0.5, 0.5, 0.5)
        self.title_text.z = Z_GUI_OBJECT_LEVEL_10 - 1

        # Create all the message texts
        self.message_text = []

        y = 45.0
        max_text_width = None

        for msg in self.message:
            txt_obj = Text(self.game.core.media.fonts['window_text'], 0.0, y, TEXT_ALIGN_TOP_LEFT, str(msg))
            txt_obj.colour = (0.3,0.3,0.3)
            txt_obj.z = Z_GUI_OBJECT_LEVEL_10 - 1
            self.message_text.append(txt_obj)
            y += txt_obj.text_height + 2

            if max_text_width is None or txt_obj.text_width > max_text_width:
                max_text_width = txt_obj.text_width

        # Create the caption image
        if not self.caption_image is None:
            self.caption_image_obj = GUI_element_dialog_box_caption_image(self.game, self, self.caption_image)
            
        # Work out the width of the frame based on the max width of the text objects and captions
        if max_text_width + 60 > self.min_box_width:
            self.min_box_width = max_text_width + 60

        if not self.caption_image is None and self.caption_image_obj.image.width > self.min_box_width:
            self.min_box_width = self.caption_image_obj.image.width + 60

        # Work out the height of the frame based on the number of text objects and the height of any caption image
        self.min_box_height = self.min_box_height + (len(self.message_text) * self.message_text[0].text_height) + (0 if self.caption_image is None else (self.caption_image_obj.image.height + 20))

        # Work out where the frame should be (the middle of the screen)
        self.frame_location_y = (self.game.settings['screen_height'] / 2) - (self.min_box_height / 2)
        self.frame_location_x = (self.game.settings['screen_width'] / 2) - (self.min_box_width / 2)

        # Create the frame
        self.frame = GUI_element_window_frame(self.game, self, self.frame_location_x, self.frame_location_y, self.min_box_width, self.min_box_height)

        # Adjust the position of the text objects based on the final location of the frame
        self.title_text.x = self.frame_location_x + self.min_box_width / 2
        self.title_text.y = self.frame_location_y + 5.0

        for txt_obj in self.message_text:
            txt_obj.x = self.frame_location_x + 28
            txt_obj.y += self.frame_location_y + (0 if self.caption_image is None else (self.caption_image_obj.image.height + 20))

        # Put the caption image in the right place
        if not self.caption_image is None:
            self.caption_image_obj.x = (self.frame_location_x + (self.min_box_width / 2)) - (self.caption_image_obj.image.width / 2)
            self.caption_image_obj.y = self.frame_location_y + 35
            
        # Stop the user pressing keys and shit
        self.game.gui.block_gui_keyboard_input = True
        
        # Create the relevant buttons
        self.create_button_objects()        

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = False
        self.primitive_square_filled = True
        self.primitive_square_width = self.width
        self.primitive_square_height = self.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_colour = (0.0, 0.0, 0.0, .4)


    def create_button_objects(self):
        GUI_button_dialog_box_confirm(self.game, self, self.frame.x + (self.frame.width/2) - 27)

        
    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.title_text.Kill()
        for msg_obj in self.message_text:
            msg_obj.Kill()
        self.game.gui.block_gui_keyboard_input = False
            


class GUI_button_dialog_box_confirm(GUI_element_button):
    """ Button on dialogs boxes to confirm the message. """
    generic_button = True
    generic_button_text = "Okay"

    def __init__(self, game, parent = None, x = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.frame.z - 1
        self.x = x
        self.y = self.parent.frame.y + self.parent.frame.height - 45.0
        self.gui_init()

    
    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.parent.Kill()
        if not self.parent.callback is None:
            self.parent.callback()



class GUI_element_dialog_box_caption_image(GUI_element):
    def __init__(self, game, parent = None, type = 1):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.z - 2
        self.image = self.game.core.media.gfx['gui_dialog_caption_' + str(type)]
        self.gui_init()



class GUI_element_confirmation_box(GUI_element_dialog_box):
    def __init__(self, game, parent = None, title = "test", message = ["test message"], caption_image = None, confirm_callback = None, cancel_callback = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.title = title
        self.message = message
        self.caption_image = caption_image
        self.confirm_callback = confirm_callback
        self.cancel_callback = cancel_callback
        self.gui_init()


    def create_button_objects(self):
        GUI_button_confirmation_box_confirm(self.game, self, self.frame.x + (self.frame.width/2) - 49)
        GUI_button_confirmation_box_cancel(self.game, self, self.frame.x + (self.frame.width/2) + 11 )



class GUI_button_confirmation_box_confirm(GUI_element_button):
    """ Button on confirmation boxes to confirm the message. """
    generic_button = True
    generic_button_text = "Yes"

    def __init__(self, game, parent = None, x = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.frame.z - 1
        self.x = x
        self.y = self.parent.frame.y + self.parent.frame.height - 45.0
        self.gui_init()

    
    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if not self.parent.confirm_callback is None:
            self.parent.confirm_callback()
        self.parent.Kill()



class GUI_button_confirmation_box_cancel(GUI_element_button):
    """ Button on confirmation boxes to confirm the message. """
    generic_button = True
    generic_button_text = "No"

    def __init__(self, game, parent = None, x = 0):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.frame.z - 1
        self.x = x
        self.y = self.parent.frame.y + self.parent.frame.height - 45.0
        self.gui_init()

    
    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if not self.parent.cancel_callback is None:
            self.parent.cancel_callback()
        self.parent.Kill()



class Pixel_message(Process):

    pattern = [
        " XXX               XXX           ",
        "X   X           X X   X          ",
        "X   X           X X   X        XX",
        "X XX  X X X XXX X X XX  X XXX XX ",
        "X     X  X  XX  X X     X X     X",
        "X     X X X XXX X X     X XXX XX "
        ]

    objs = []
    dying = False
    pixel_message_state = 0
    
    def __init__(self, game, x, y, z = Z_GUI_OBJECT_LEVEL_5, wait = 3):
        Process.__init__(self)
        self.game = game
        self.width = (self.game.core.media.gfx['gui_main_menu_title_pixel'].width/2) * len(self.pattern[0])
        self.height = (self.game.core.media.gfx['gui_main_menu_title_pixel'].height/2) * len(self.pattern)
        self.x = x + (((self.game.settings['screen_width']/2) - (self.width/2)) - self.game.core.media.gfx['gui_main_menu_title_pixel'].width)
        self.y = y
        self.z = z
        self.wait = wait
        self.life = 0
        self.pixel_message_state = 0
        self.iter = 0
        

    def Execute(self):
        # waiting a bit
        if self.pixel_message_state == 0:
            self.iter += 1
            if self.iter >= 30:
                self.pixel_message_state = 1
                self.create_pixels()

        # doing stuff
        if self.pixel_message_state == 1:
            self.life += 1
            if self.dying:
                self.iter += 1
                self.alpha = lerp(self.iter, 30, self.alpha, 0.0)
                for x in self.objs:
                    x.alpha = self.alpha
                if self.iter == 30:
                    self.Kill()


    def finish(self):
        if self.pixel_message_state == 0:
            self.pixel_message_state = 1
            self.create_pixels()
        for x in self.objs:
            x.finish()
        

    def create_pixels(self):
        self.iter = 0

        pixel_y = self.y + self.height
        order = True
        self.objs = []

        wait_num = 0
        for i, row in enumerate(reversed(self.pattern)):
            pixel_x = self.x
            if not order:
                pixel_x = self.x + self.width + (self.game.core.media.gfx['gui_main_menu_title_pixel'].width/2)
                row = row[::-1]
            for j, char in enumerate(row):
                if order:
                    pixel_x += self.game.core.media.gfx['gui_main_menu_title_pixel'].width/2
                else:
                    pixel_x -= self.game.core.media.gfx['gui_main_menu_title_pixel'].width/2
                if char == " ":
                    continue
                self.objs.append(Pixel_message_pixel(self.game, pixel_x, pixel_y, self.z - i + j, self.wait * wait_num, ))
                wait_num += 1
            pixel_y -= (self.game.core.media.gfx['gui_main_menu_title_pixel'].height/2)
            order = not order

        
    def die(self):
        self.dying = True

    def On_Exit(self):
        for x in self.objs:
            x.Kill()
            


class Pixel_message_pixel(Process):
    pixel_message_pixel_state = 0
    
    def __init__(self, game, x, y, z, wait = 3):
        Process.__init__(self)
        self.game = game
        self.x = x
        self.y_to = y
        self.z = z - 50
        self.wait = wait
        self.image = self.game.core.media.gfx['gui_main_menu_title_pixel']
        self.y = -self.image.height
        self.pixel_message_pixel_state = 0
        self.iter = 0


    def Execute(self):
        # Waiting a bit
        if self.pixel_message_pixel_state == 0:
            self.iter += 1
            if self.iter > self.wait:
                self.pixel_message_pixel_state = 1
                self.iter = 0
        # Moving in
        if self.pixel_message_pixel_state == 1:
            self.iter += 1
            self.y = lerp(self.iter, 20, self.y, self.y_to)
            if self.iter == 20:
                self.pixel_message_pixel_state = 2


    def finish(self):
        self.y = self.y_to
        self.pixel_message_pixel_state = 2
        


class Puzzle_image(GUI_element):
    def __init__(self, game, parent, x, y, puzzle_object = None, puzzle_path = "", in_colour = True, fade_in_time = 60):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.fade_in_time = fade_in_time
        self.pos = (x, y)
        self.gui_init()
        self.in_colour = in_colour

        if not puzzle_path == "":
            f = open(puzzle_path, "r")
            self.puzzle = pickle.load(f)
            f.close()
        else:
            self.puzzle = puzzle_object
        
            if self.puzzle is None:
                self.puzzle = self.game.manager.current_puzzle
            
        self.width = self.puzzle.width
        self.height = self.puzzle.height

        self.create_image_from_puzzle()
        self.set_position_z_scale(*self.pos)

        if not self.fade_in_time is None:
            self.alpha = 0.0
            self.iter = 0
            

    def Execute(self):
        self.update()
        self.set_position_z_scale(*self.pos)
        # Fade in
        if not self.fade_in_time is None:
            self.iter += 1
            self.alpha = lerp(self.iter, 60, self.alpha, 1.0)
            if self.iter >= 60:
                self.fade_in_time = None


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.destroy_puzzle_image()


    def reload_image(self):
        self.destroy_puzzle_image()
        self.create_image_from_puzzle()


    def set_position_z_scale(self, x, y):
        self.x = 0
        self.y = 0
        self.z = Z_GUI_OBJECT_LEVEL_4
        self.scale = 1.0



class GUI_element_text_input(GUI_element):
    """
    This is a simple text input box.
    """
    # Set to relevant sizes
    width = 200
    height = 25

    # None will not add a label. Setting to a string will label the text input with a label.
    label = None

    # This is the maximum text length that this input will accept.
    max_length = 25

    # What the current text in the input element is.
    current_text = ""
    
    # text objects
    label_text_object = None
    text_object = None

    # If set to True then we are currently typing into the text input.
    active = False

    # Caret blinking related stuff
    blink = False
    blink_wait = 0
    
    # Whereever the blinking caret is at the time.
    caret_location = 0
       
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        

    def gui_init(self):
        GUI_element.gui_init(self)

        if not self.label is None:            
            self.label_text_object = Text(self.game.core.media.fonts['window_text'], self.x, self.y + 2, TEXT_ALIGN_TOP_LEFT, str(self.label + " "))
            self.label_text_object.z = self.z
            self.label_text_object.colour = (.3,.3,.3)
            self.width -= self.label_text_object.text_width
            
        self.x += self.label_text_object.text_width

        self.text_object = Text(self.game.core.media.fonts['text_input'], self.x + 5, self.y + 2, TEXT_ALIGN_TOP_LEFT, str(self.current_text))
        self.text_object.z = self.z - 1
        self.text_object.colour = (.2,.2,.2)

        self.draw_strategy = "gui_text_input"


    def update(self):
        GUI_element.update(self)
        
        if not self.active:
            return

        for input_key in self.game.core.Text_input:
            # Backspace
            if input_key == key.BACKSPACE:
                self.game.core.media.sfx['type'].play(0)                
                if len(self.current_text) > 0 and self.caret_location > 0:
                    self.current_text = self.current_text[0:self.caret_location-1] + self.current_text[self.caret_location:]
                    self.caret_location -= 1

            # Delete key
            elif input_key == key.DELETE:
                if len(self.current_text) > 0 and self.caret_location < len(self.current_text):            
                    self.current_text = self.current_text[0:self.caret_location] + self.current_text[self.caret_location+1:]
        
            # If we've input any normal key event that isn't quitting then add it to the text input
            if (
                input_key > 0 and input_key <= 127
                and not input_key == key.RETURN
                and not input_key == key.ESCAPE
                and not input_key == key.BACKSPACE
                and not input_key == key.DELETE
                ):
                self.game.core.media.sfx['type'].play(0)                
                if len(self.current_text) < self.max_length:
                    self.current_text = self.current_text[0:self.caret_location] + chr(input_key).decode('utf-8') + self.current_text[self.caret_location:]
                    self.caret_location += 1

        # Arrow keys move the caret
        if self.game.core.Keyboard_key_released(key.LEFT):
            if len(self.current_text) > 0 and self.caret_location > 0:
                self.caret_location -= 1
        elif self.game.core.Keyboard_key_released(key.RIGHT):
            if len(self.current_text) > 0 and self.caret_location < len(self.current_text):
                self.caret_location += 1

        # Update the display text, blinking if necessary
        if self.blink_wait == 10:
            self.blink_wait = 0
            self.blink = True if not self.blink else False
        self.blink_wait += 1

        if len(self.current_text) > 0:
            char_at_caret_location = "" if self.caret_location == len(self.current_text) else self.current_text[self.caret_location]
            self.text_object.text = str(self.current_text[0:self.caret_location] + ("_" if self.blink else char_at_caret_location) + self.current_text[self.caret_location+1:])
        else:
            self.text_object.text = str("_" if self.blink else "")

        # Get rid
        if self.game.core.mouse.left_up or self.game.core.Keyboard_key_released(key.RETURN) or self.game.core.Keyboard_key_released(key.ESCAPE):
            self.unfocus()


    def set_current_text_to(self, new_text):
        self.current_text = new_text
        self.text_object.text = str(new_text)
           

    def mouse_left_up(self):
        if self.active:
            return
        self.focus()


    def focus(self):
        if self.active:
            return
        if not self.game.gui.focussed_text_input is None:
            self.game.gui.focussed_text_input.unfocus()
        self.game.gui.focussed_text_input = self
        self.active = True
        self.caret_location = len(self.current_text)        
        self.game.core.Toggle_text_input()


    def unfocus(self):
        if not self.active:
            return
        self.game.focussed_text_input = None
        self.active = False
        self.text_object.text = str(self.current_text)
        self.game.core.Toggle_text_input()


    def On_Exit(self):
        GUI_element.On_Exit(self)
        if self.active:
            self.unfocus()
        if not self.label is None:
            self.label_text_object.Kill()
        self.text_object.Kill()



class GUI_element_dropdown(GUI_element):
    """
    A generic dropdown object.
    Instead of setting width,height,x,y,z as you normally would. Instead set
    display_width, display_height, display_x, display_y and display_z respectively.
    This is because the dropdown object uses a bunch of crazy things to make full
    use of the cascading GUI system.
    """
    # Set to the maximum length the currently selected text should be before being truncated
    max_selected_text_len = 20

    # Override these instead of the typical attributes
    display_width = 300
    display_height = 28
    display_x = 0
    display_y = 0
    display_z = Z_GUI_OBJECT_LEVEL_6

    # Override to set to your own dropdown options
    dropdown_options = [
        {'text' : "The first option", 'data' : 1},
        {'text' : "The second option", 'data' : 10},
        {'text' : "The third option", 'data' : 100}
        ]

    # Override to set what the initial selected item should be.
    selected_item = 0
    
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()        


    def on_selected_new_item(self, item):
        """
        Override this to hook into selection
        """
        pass
    
        
    def change_selected_item(self, selected_item):
        self.selected_item = selected_item
        self.set_visible_selected_text()
        self.on_selected_new_item(self.dropdown_options[self.selected_item])


    def change_selected_item_to_data(self, data):
        seq = 0
        for x in self.dropdown_options:
            if x['data'] == data:
                self.change_selected_item(seq)
                return
            seq += 1

        
    def set_visible_selected_text(self):
        if len(self.dropdown_options[self.selected_item]['text']) > self.max_selected_text_len:
            text = self.dropdown_options[self.selected_item]['text'][:self.max_selected_text_len] + "..."
        else:
            text = self.dropdown_options[self.selected_item]['text']

        self.currently_selected_object.set_text_to(text)


    def gui_init(self):
        GUI_element.gui_init(self)

        self.options_displayed = False

        self.z = Z_GUI_OBJECT_LEVEL_11
        
        self.currently_selected_object = GUI_element_dropdown_currently_selected(self.game, self)
        self.currently_selected_object.width = self.display_width
        self.currently_selected_object.height = self.display_height
        self.currently_selected_object.x = self.display_x
        self.currently_selected_object.y = self.display_y
        
        self.options_object = GUI_element_dropdown_options(self.game, self)
        self.options_object.width = self.display_width
        self.options_object.x = self.display_x
        self.options_object.y = self.display_y + self.display_height
        self.options_object.z = Z_GUI_OBJECT_LEVEL_11 - 1

        self.set_visible_selected_text()


    def mouse_left_up(self):
        self.game.core.media.sfx['button_click'].play(0)
        self.hide_all_options()

        
    def display_all_options(self):
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.options_object.show()
        self.options_displayed = True

        
    def hide_all_options(self):
        self.width = 0
        self.height = 0
        self.options_object.hide()        
        self.options_displayed = False
        

    
class GUI_element_dropdown_currently_selected(GUI_element):
    """
    -- Displays the currently selected option
    -- display z
    -- clicking makes the options display
    """
    text_object = None
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.z = self.parent.display_z
        self.draw_strategy = "gui_dropdown_currently_selected"
        self.image = self.game.core.media.gfx['gui_dropdown_arrow']
        self.hover_sound = False
        self.gui_init()


    def update(self):
        self.image_sequence = 1
        GUI_element.update(self)


    def set_text_to(self, text):
        if self.text_object is None:
            self.text_object = Text(self.game.core.media.fonts['dropdown_text'], self.x + 6, self.y + 6, TEXT_ALIGN_TOP_LEFT, text)
            self.text_object.z = self.z - 2
            self.text_object.colour = (0.3,0.3,0.3)
        else:
            self.text_object.text = text
            
        
    def mouse_over(self):
        if not self.hover_sound:
            self.game.core.media.sfx['button_hover'].play(0)
            self.hover_sound = True
        self.image_sequence = 2


    def mouse_out(self):
        self.hover_sound = False
        

    def mouse_left_down(self):
        self.image_sequence = 3


    def mouse_left_up(self):
        self.game.core.media.sfx['button_click'].play(0)        
        if self.parent.options_displayed:
            self.parent.hide_all_options()
        else:
            self.parent.display_all_options()


    def On_Exit(self):
        self.text_object.Kill()



class GUI_element_dropdown_options(GUI_element):
    """
    -- Displays all options
    -- clicking on changes the currently selected item in the dropdown
    """
    texts = []
    hovered_item = -1
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()
        self.draw_strategy = "gui_dropdown_options"
        self.display_height = self.parent.display_height - 4
        self.num_dropdown_options = len(self.parent.dropdown_options)
        self.hover_sound = False
        self.last_hovered_item = -1
        

    def Execute(self):
        self.hovered_item = -1
        self.update()
    

    def show(self):
        self.texts = []
        
        self.height = 0
        for item in self.parent.dropdown_options:
            new_text = Text(self.game.core.media.fonts['dropdown_text_options'], self.x + 2, self.y + 4 + self.height, TEXT_ALIGN_TOP_LEFT, item['text'])
            new_text.z = self.z - 2
            new_text.colour = (.3, .3, .3)
            self.texts.append(new_text)

            self.height += self.display_height

            if new_text.text_width > self.width:
                self.width = new_text.text_width

        if self.width < self.parent.display_width:
            self.width = self.parent.display_width
            

    def hide(self):
        for x in self.texts:
            x.Kill()
        self.width = 0
        self.height = 0        
        self.texts = []


    def mouse_over(self):
        self.hovered_item = int((self.game.gui.mouse.y - self.y) / (self.display_height))
        if self.hovered_item >= len(self.parent.dropdown_options):
            self.hovered_item = -1
        if not self.hover_sound and self.hovered_item > -1 and self.hovered_item != self.last_hovered_item:
            self.game.core.media.sfx['button_hover'].play(0)
            self.hover_sound = True
        if self.hovered_item != self.last_hovered_item:
            self.hover_sound = False            
        self.last_hovered_item = self.hovered_item


    def mouse_out(self):
        self.hover_sound = False
        
        
    def mouse_left_up(self):
        self.game.core.media.sfx['button_click'].play(0)
        if self.hovered_item > -1:
            self.parent.hide_all_options()
            self.parent.change_selected_item(self.hovered_item)
            

    def On_Exit(self):
        for x in self.texts:
            x.Kill()



class GUI_element_scroll_window(GUI_element):
    contents_height = 0
    contents_scroll_location = 0.0
    arrows = []

    def gui_init(self):
        GUI_element.gui_init(self)
        self.arrows = []
        self.arrows.append(GUI_element_button_scroll_window_arrow(self.game, self, up_arrow = True))
        self.arrows.append(GUI_element_button_scroll_window_arrow(self.game, self, up_arrow = False))
        self.draw_strategy = "gui_scroll_window"

        
    def update(self):
        GUI_element.update(self)
        
        # Make sure the scroll is not out of bounds
        self.normalise_scroll_location()


    def mouse_wheel_down(self):
        self.contents_scroll_location += GUI_SCROLL_ELEMENT_SCROLL_AMOUNT
        self.normalise_scroll_location()

        
    def mouse_wheel_up(self):
        self.contents_scroll_location -= GUI_SCROLL_ELEMENT_SCROLL_AMOUNT
        self.normalise_scroll_location()


    def normalise_scroll_location(self):
        if self.contents_height < self.height:
            self.contents_height = self.height
        if self.contents_scroll_location < 0:
            self.contents_scroll_location = 0
        if self.contents_scroll_location > self.contents_height - self.height:
            self.contents_scroll_location = self.contents_height - self.height

        for x in self.arrows:
            x.y = (64 if x.up_arrow else self.height - 128) + self.contents_scroll_location



class GUI_element_button_scroll_window_arrow(GUI_element_button):
    generic_button = False

    def __init__(self, game, parent, up_arrow):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.up_arrow = up_arrow
        self.scroll_element = self.parent
        self.x = self.parent.width - 64
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_scroll_button_up' if self.up_arrow else 'gui_scroll_button_down']
        self.gui_init()


    def mouse_left_down(self):
        GUI_element_button.mouse_left_down(self)
        if self.up_arrow:
            self.parent.mouse_wheel_up()
        else:
            self.parent.mouse_wheel_down()



class GUI_element_spinner(GUI_element):
    # Set to relevant sizes
    width = 75
    height = 25

    # None will not add a label. Setting to a string will label the spinner.
    label = None

    # Bounds
    max_value = 100
    min_value = -100

    # What the current value is.
    current_value = 1
    
    # text objects
    label_text_object = None
    text_object = None

    # Spinner button objects
    spinner_down = None
    spinner_up = None
    
    def __init__(self, game, parent = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()


    def gui_init(self):
        GUI_element.gui_init(self)
        
        if not self.label is None:            
            self.label_text_object = Text(self.game.core.media.fonts['basic'], self.x, self.y + 2, TEXT_ALIGN_TOP_LEFT, self.label + " ")
            self.label_text_object.z = self.z -1
            self.label_text_object.colour = (0,0,0)
            
        self.x += self.label_text_object.text_width

        self.text_object = Text(self.game.core.media.fonts['basic'], self.x + 5, self.y + 2, TEXT_ALIGN_TOP_LEFT, str(self.current_value))
        self.text_object.z = self.z - 1

        self.spinner_down = GUI_element_spinner_button_down(self.game, self)
        self.spinner_up = GUI_element_spinner_button_up(self.game, self)

        self.draw_strategy = "gui_spinner"
        

    def decrease_current_value(self):
        if self.current_value > self.min_value:
            self.set_current_value(self.current_value - 1)


    def increase_current_value(self):
        if self.current_value < self.max_value:
            self.set_current_value(self.current_value + 1)


    def set_current_value(self, new_val):
        self.current_value = int(new_val)
        self.text_object.text = str(self.current_value)


    def On_Exit(self):
        GUI_element.On_Exit(self)
        if not self.label is None:
            self.label_text_object.Kill()
        self.text_object.Kill()



class GUI_element_spinner_button_down(GUI_element_button):
    generic_button = False
    spinner_wait = 0
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.width = 19
        self.height = 12
        self.x = self.parent.x + self.parent.width - self.width - 1
        self.y = self.parent.y + 13
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_spinner_down']
        self.gui_init()


    def mouse_left_down(self):
        GUI_element_button.mouse_left_down(self)
        self.spinner_wait += 1
        if self.spinner_wait == 10:
            self.parent.decrease_current_value()
            self.spinner_wait = 0


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.spinner_wait = 0
        self.parent.decrease_current_value()



class GUI_element_spinner_button_up(GUI_element_button):
    generic_button = False
    spinner_wait = 0

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.width = 19
        self.height = 12
        self.x = self.parent.x + self.parent.width - self.width - 1
        self.y = self.parent.y + 1
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_button_spinner_up']
        self.gui_init()


    def mouse_left_down(self):
        GUI_element_button.mouse_left_down(self)
        self.spinner_wait += 1
        if self.spinner_wait == 10:
            self.parent.increase_current_value()
            self.spinner_wait = 0


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.spinner_wait = 0
        self.parent.increase_current_value()



class GUI_element_yes_no_radios(GUI_element):
    current_value = True
    yes_text = "Yes"
    no_text = "No"
    text = []
    buttons = []

    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()


    def gui_init(self):
        GUI_element.gui_init(self)
        self.width = 200
        self.height = 25
        self.buttons = {}
        self.text = []
    
        self.buttons['yes'] = GUI_element_single_radio_button(self.game, self, self.press_yes)
        self.buttons['yes'].x = self.x
        self.buttons['yes'].y = self.y
        self.buttons['yes'].on_press = self.press_yes
        text = Text(self.game.core.media.fonts["window_text"], self.x + 35.0, self.y + 16, TEXT_ALIGN_CENTER_LEFT, self.yes_text)
        text.z = self.z - 1
        text.colour = (0.3,0.3,0.3)
        self.text.append(text)

        self.buttons['no'] = GUI_element_single_radio_button(self.game, self, self.press_no)
        self.buttons['no'].x = self.x + 80
        self.buttons['no'].y = self.y
        self.buttons['no'].on_press = self.press_no
        text = Text(self.game.core.media.fonts["window_text"], self.x + 115.0, self.y + 16, TEXT_ALIGN_CENTER_LEFT, self.no_text)
        text.z = self.z - 1
        text.colour = (0.3,0.3,0.3)
        self.text.append(text)

        if self.current_value == True:
            self.buttons['yes'].toggle_state = True
        else:
            self.buttons['no'].toggle_state = True
        

    def press_yes(self):
        self.current_value = True
        self.buttons['yes'].toggle_state = True
        self.buttons['no'].toggle_state = False
    

    def press_no(self):
        self.current_value = False
        self.buttons['no'].toggle_state = True
        self.buttons['yes'].toggle_state = False
    

    def On_Exit(self):
        GUI_element.On_Exit(self)
        for x in self.text:
            x.Kill()



class GUI_element_single_radio_button(GUI_element_button):
    generic_button = False
    toggle_button = True
    width = 60
    height = 32

    def __init__(self, game, parent, action = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.action = action
        self.gui_init()


    def Execute(self):
        GUI_element_button.Execute(self)
        self.play_sound = False if self.toggle_state else True
        
        
    def gui_init(self):
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_radio_button']
        GUI_element_button.gui_init(self)


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if not self.action is None:
            self.action()



class GUI_element_slider(GUI_element):
    width = 300
    height = 16

    min_value = 0
    max_value = 100

    current_value = 50
    current_value_percentage = 50

    slider_handle = None
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()

        
    def gui_init(self):
        GUI_element.gui_init(self)
        self.hover_sound = False
        self.slider_handle = GUI_element_slider_handle(self.game, self)
        #self.draw_strategy = "gui_slider"
        self.set_value(self.current_value)

        self.draw_strategy = "gui_slider"


    def mouse_over(self):
        if not self.hover_sound:
            self.game.core.media.sfx['button_hover'].play(0)
            self.hover_sound = True        
        self.slider_handle.highlight = True


    def mouse_out(self):
        self.hover_sound = False
        self.slider_handle.highlight = False


    def mouse_left_down(self):
        self.current_value_percentage = int((float(self.game.gui.mouse.x - self.x) / self.width) * 100)
        if self.current_value_percentage < 0:
            self.current_value_percentage = 0
        elif self.current_value_percentage > 100:
            self.current_value_percentage = 100
        self.set_value(int(((self.max_value - self.min_value) * (float(self.current_value_percentage) / 100)) + self.min_value))
        self.slider_dragged()


    def set_value(self, new_value):
        self.current_value = new_value
        if self.current_value < self.min_value:
            self.current_value = self.min_value
        if self.current_value > self.max_value:
            self.current_value = self.max_value
        self.current_value_percentage = (float(self.current_value - self.min_value) / (self.max_value - self.min_value)) * 100


    def slider_dragged(self):
        """
        Called when the slider is dragged. Designed to be
        overridden to add custom behaviour.
        """
        pass


    def On_Exit(self):
        self.slider_handle.Kill()



class GUI_element_slider_handle(Process):
    
    def __init__(self, game, parent):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.y = self.parent.y + (self.parent.height / 2)
        self.z = self.parent.z - 1
        self.image = self.game.core.media.gfx['gui_slider_handle']
        self.highlight = False


    def Execute(self):
        self.image_sequence = 2 if self.highlight else 1
        self.x = self.parent.x + ((self.parent.width + 2) * (float(self.parent.current_value_percentage) / 100))



class GUI_element_network_container(GUI_element):

    def gui_init(self):
        GUI_element.gui_init(self)
        self.net_process = None
        self.net_callback = None
        self.loading_indicator = None


    def update(self):
        GUI_element.update(self)
        if not self.net_process is None:
            if self.net_process.is_complete():
                self.loading_indicator.Kill()
                self.loading_indicator = None                                
                if self.net_process.got_error:
                    GUI_element_dialog_box(
                        self.game,
                        self,
                        "Network error",
                        ["A network error occured!", "Please check your internet connection is functioning properly."],
                        callback = self.return_to_menu
                        )
                    self.net_process = None
                    return
                if 'error' in self.net_process.response:
                    GUI_element_dialog_box(
                        self.game,
                        self,
                        "Error",
                        ["The server returned an error:", str(self.net_process.response['error'])]
                        )
                    self.net_process = None
                elif not self.net_callback is None:
                    response = self.net_process.response
                    self.net_process = None
                    self.net_callback(response)
        


    def make_request_to_server(self, url, data = {}, callback = None, task_text = None):
        if not self.net_process is None:
            return

        self.net_process = Net_Process_POST(SHARING_ADDRESS + url, data)
        self.net_callback = callback
        self.loading_indicator = GUI_network_loading_indicator(self.game, self, task_text)


    def return_to_menu(self):
        self.game.gui.fade_toggle(lambda: self.game.switch_game_state_to(GAME_STATE_MENU), speed = 20)



class GUI_network_loading_indicator(GUI_element):
    def __init__(self, game, parent, task_text):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.gui_init()

        self.z = Z_GUI_OBJECT_LEVEL_11
        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']
        self.text = Text(self.game.core.media.fonts['puzzle_hint_numbers'], self.width / 2, (self.height / 2) - 16, TEXT_ALIGN_CENTER, "Loading . . . ")
        self.text.z = self.z - 1
        self.text.colour = (1.0, 1.0, 1.0, 1.0)
        self.text.shadow = 2
        self.text.shadow_colour = (.3, .3, .3, 1.0)

        self.task_text = None
        if not task_text is None:
            self.task_text = Text(self.game.core.media.fonts['menu_subtitles'], self.width / 2, (self.height / 2) + 20, TEXT_ALIGN_CENTER, str(task_text))
            self.task_text.z = self.z - 1
            self.task_text.colour = (.7, .7, .7, 1.0)
            self.task_text.shadow = 2
            self.task_text.shadow_colour = (.3, .3, .3, 1.0)
            
        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.primitive_square_width = self.width
        self.primitive_square_height = 100
        self.primitive_square_x = 0.0
        self.primitive_square_y = (self.height / 2) - 50
        self.primitive_square_colour = (0.0,0.0,0.0,.3)


    def On_Exit(self):
        GUI_element.On_Exit(self)
        self.text.Kill()
        if not self.task_text is None:
            self.task_text.Kill()
