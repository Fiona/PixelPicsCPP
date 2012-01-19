from core import *


class Game(Process):
    def Init(self):
        self.current_rotation = 0
        self.current_rotation_2 = 0
        Ship(self)

        self.current_fps_display = Text(core.media.fonts["basic"], 0, 0, TEXT_ALIGN_TOP_LEFT, "TESTING")
        self.current_process_count_display = Text(core.media.fonts["basic"], 0, 20.0, TEXT_ALIGN_TOP_LEFT, "")


    def Execute(self):
        if core.Keyboard_key_down(key.ESCAPE):
            core.Quit()

        self.create_vorticies(200.0, 300.0, 1)
        self.create_vorticies(400.0, 300.0, 1)

        self.current_fps_display.text = "FPS: " + str(core.current_fps)
        self.current_process_count_display.text = "Num processes: " + str(core.process_count)


    def create_vorticies(self, x, y, type):
        _range = 1
        amount = 3

        if core.Keyboard_key_down(key.SPACE):
            _range = 20
            amount = 10

        for c in range(_range):
            if type == 1:
                self.current_rotation_2 -= amount
            else:
                self.current_rotation += amount

            if type == 1:
                if self.current_rotation_2 < -360:
                    self.current_rotation_2 = 0
            else:
                if self.current_rotation > 360:
                    self.current_rotation = 0

            Shot(self, x, y, self.current_rotation_2  if type else self.current_rotation)



class Ship(Process):

    def __init__(self, game):
        Process.__init__(self)
        self.game = game
        self.image_sequence = 2
        self.x = 500.0
        self.y = 300.0
        self.z = -100
        self.image = core.media.gfx['ship']

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.draw_strategy_call_parent = True
        self.primitive_square_filled = False
        self.primitive_square_width = self.image.width
        self.primitive_square_height = self.image.height
        self.primitive_square_x = 0.0
        self.primitive_square_y = 0.0
        self.primitive_square_line_width = 1.0
        self.primitive_square_colour = (0.0, 1.0, 0.0, 1.0)

        
    def Execute(self):

        self.primitive_square_x = self.x - (self.image.width/2)
        self.primitive_square_y = self.y - (self.image.height/2)
        
        if core.Keyboard_key_down(key.LEFT):
            self.x -= 10.0
        if core.Keyboard_key_down(key.RIGHT):
            self.x += 10.0
        if core.Keyboard_key_down(key.UP):
            self.y -= 10.0
        if core.Keyboard_key_down(key.DOWN):
            self.y += 10.0
        if core.Keyboard_key_down(key.a):
            self.alpha -= .05
        if core.Keyboard_key_down(key.o):
            self.alpha += .05
        if core.Keyboard_key_down(key.QUOTE):
            self.scale -= .05
        if core.Keyboard_key_down(key.COMMA):
            self.scale += .05
        if core.Keyboard_key_down(key.q):
            self.rotation -= 10
        if core.Keyboard_key_down(key.j):
            self.rotation += 10
        


class Shot(Process):
    def __init__(self, game, x, y, angle):
        Process.__init__(self)
        self.game = game
        self.angle = angle
        self.x = x
        self.y = y
        self.image = core.media.gfx['shot']
        self.z = 512
        
    def Execute(self):
        self.move_forward(3.0, self.angle)

        if self.x < 50.0 or self.x > 590.0 or self.y < 0.0 or self.y > 480.0:
            self.Kill()



Game()
