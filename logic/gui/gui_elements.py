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
        # IMPLEMENT
        # TODO
        # DO THIS
        return (self.x, self.y)
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
