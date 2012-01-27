"""
PixelPics - Nonograme game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# Game engine imports
from core import *

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
            self.clip = ((self.scroll_element.x, self.scroll_element.y), (self.scroll_element.width, self.scroll_element.height))
            return (self.x + self.scroll_element.x, self.y + self.scroll_element.y - self.scroll_element.contents_scroll_location)
        else:
            self.clip = None
            return (self.x, self.y)
    

    def On_Exit(self):
        kids = list(self.children)
        for child in kids:
            child.Kill()

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

        if not self.image is None:
            self.generic_button = False
            self.width = self.image.width if self.width == 0 else self.width
            self.height = self.image.height if self.height == 0 else self.height
        else:
            # Set up a generic button
            self.generic_button = True
            self.image = self.game.core.media.gfx['gui_button_generic_background']
            self.draw_strategy = "gui_button"
            
            # Create the text
            self.generic_button_text_object = Text(self.game.core.media.fonts["basic"], self.x + 9.0, self.y + 4.0, TEXT_ALIGN_TOP_LEFT, self.generic_button_text)
            self.generic_button_text_object.z = self.z - 1
            self.generic_button_text_object.colour = (0.0,0.0,0.0)
            
            # Set up the width, if we have a larger than normal width then we want to centre the text.
            if self.width > self.generic_button_text_object.text_width + 20:
                self.generic_button_text_object.x += (self.width / 2) - (self.generic_button_text_object.text_width/2) - 9
            else:
                self.width = self.generic_button_text_object.text_width + 20

            # Fixed height, a little bit taller than the text
            self.height = self.generic_button_text_object.text_height + 10
            
        self.sequence_count = self.image.num_of_frames
        self.draw_strategy_call_parent = False
        

    def update(self):
        self.image_sequence = 1
        GUI_element.update(self)
        if self.toggle_button and self.toggle_state:
            self.image_sequence = 3 if self.sequence_count > 3 else 0
        elif self.toggle_button:
            self.image_sequence = 1


    def mouse_left_up_toggle(self):
        self.toggle_state = True if self.toggle_state == False else False


    def mouse_over(self):
        if self.sequence_count > 1:
            self.image_sequence = 2


    def mouse_left_down(self):
        if self.sequence_count > 2:
            self.image_sequence = 3


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
        self.text = Text(self.game.core.media.fonts['small'], self.x+16.0, self.y+4.0, TEXT_ALIGN_TOP_LEFT,  self.title)
        self.text.colour = (0.0,0.0,0.0)
        self.text.z = self.z - 1

    
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

    min_box_height = 95
    min_box_width = 300    
       
    def __init__(self, game, parent = None, title = "test", message = ["test message"], caption_image = None):
        Process.__init__(self)
        self.game = game
        self.parent = parent
        self.title = title
        self.message = message
        self.caption_image = caption_image
        self.gui_init()
        

    def gui_init(self):
        GUI_element.gui_init(self)
        self.z = Z_GUI_OBJECT_LEVEL_9

        self.width = self.game.settings['screen_width']
        self.height = self.game.settings['screen_height']

        # Create the title text objects
        self.title_text = Text(self.game.core.media.fonts['small'], 0.0, 0.0, TEXT_ALIGN_TOP_LEFT, self.title)
        self.title_text.colour = (0.0,0.0,0.0)
        self.title_text.z = Z_GUI_OBJECT_LEVEL_10 - 1

        # Create all the message texts
        self.message_text = []

        y = 30.0
        max_text_width = None

        for msg in self.message:
            txt_obj = Text(self.game.core.media.fonts['basic'], 0.0, y, TEXT_ALIGN_TOP_LEFT, msg)
            txt_obj.colour = (0.0,0.0,0.0)
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
        self.title_text.x = self.frame_location_x + 16
        self.title_text.y = self.frame_location_y + 4

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
        self.y = self.parent.frame.y + self.parent.frame.height - 50.0
        self.gui_init()

    
    def mouse_left_up(self):
        self.parent.Kill()



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
        GUI_button_confirmation_box_confirm(self.game, self, self.frame.x + (self.frame.width/2) - 50)
        GUI_button_confirmation_box_cancel(self.game, self, self.frame.x + (self.frame.width/2) + 20)



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
        self.y = self.parent.frame.y + self.parent.frame.height - 50.0
        self.gui_init()

    
    def mouse_left_up(self):
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
        self.y = self.parent.frame.y + self.parent.frame.height - 50.0
        self.gui_init()

    
    def mouse_left_up(self):
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
        self.width = self.game.core.media.gfx['gui_main_menu_title_pixel'].width * len(self.pattern[0])
        self.height = self.game.core.media.gfx['gui_main_menu_title_pixel'].height * len(self.pattern)
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
                self.iter = 0

                pixel_y = self.y + self.height
                order = True
                self.objs = []

                wait_num = 0
                for i, row in enumerate(reversed(self.pattern)):
                    pixel_x = self.x
                    if not order:
                        pixel_x = self.x + self.width + self.game.core.media.gfx['gui_main_menu_title_pixel'].width
                        row = row[::-1]
                    for char in row:
                        if order:
                            pixel_x += self.game.core.media.gfx['gui_main_menu_title_pixel'].width
                        else:
                            pixel_x -= self.game.core.media.gfx['gui_main_menu_title_pixel'].width
                        if char == " ":
                            continue
                        self.objs.append(Pixel_message_pixel(self.game, pixel_x, pixel_y, self.z, self.wait * wait_num))
                        wait_num += 1
                    pixel_y -= self.game.core.media.gfx['gui_main_menu_title_pixel'].height
                    order = not order

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
        self.z = z
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



class Puzzle_image(GUI_element):
    pass
