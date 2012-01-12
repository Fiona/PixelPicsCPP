from game_core import *


class Game(Process):
    def Init(self):
        self.current_rotation = 0
        self.current_rotation_2 = 0
        Ship()

        self.current_fps_display = Text(game.media.fonts["basic"], 0, 0, TEXT_ALIGN_TOP_LEFT, "TESTING")
        self.current_process_count_display = Text(game.media.fonts["basic"], 0, 20.0, TEXT_ALIGN_TOP_LEFT, "")


    def Execute(self):
        if game.Keyboard_key_down(key.ESCAPE):
            game.Quit()

        self.create_vorticies(200.0, 300.0, 1)
        self.create_vorticies(400.0, 300.0, 1)

        self.current_fps_display.text = "FPS: " + str(game.current_fps)
        self.current_process_count_display.text = "Num processes: " + str(game.process_count)


    def create_vorticies(self, x, y, type):
        _range = 1
        amount = 3

        if game.Keyboard_key_down(key.SPACE):
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

            Shot(x, y, self.current_rotation_2  if type else self.current_rotation)



class Ship(Process):

    def Init(self):
        self.x = 500.0
        self.y = 300.0
        self.z = -100
        self.image = game.media.gfx['ship']

        # Draw strategy data
        self.draw_strategy = "primitive_square"
        self.primitive_square_width = 100.0
        self.primitive_square_height = 200.0
        
    def Execute(self):
        if game.Keyboard_key_down(key.LEFT):
            self.x -= 10.0
        if game.Keyboard_key_down(key.RIGHT):
            self.x += 10.0
        if game.Keyboard_key_down(key.UP):
            self.y -= 10.0
        if game.Keyboard_key_down(key.DOWN):
            self.y += 10.0
        self.colour = (.5, .1, 0)
        if game.Keyboard_key_down(key.a):
            self.alpha -= .05
        if game.Keyboard_key_down(key.o):
            self.alpha += .05
        if game.Keyboard_key_down(key.QUOTE):
            self.scale -= .05
        if game.Keyboard_key_down(key.COMMA):
            self.scale += .05
        if game.Keyboard_key_down(key.q):
            self.rotation -= 10
        if game.Keyboard_key_down(key.j):
            self.rotation += 10


        


class Shot(Process):
    def __init__(self, x, y, angle):
        Process.__init__(self)
        self.angle = angle
        self.x = x
        self.y = y
        self.image = game.media.gfx['shot']
        self.z = 512
        
    def Execute(self):
        self.move_forward(3.0, self.angle)

        if self.x < 50.0 or self.x > 590.0 or self.y < 0.0 or self.y > 480.0:
            self.Kill()
        

Game()
