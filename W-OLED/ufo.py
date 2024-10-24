from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
screen_width = 128
screen_height = 64
screen = SSD1306_I2C(screen_width, screen_height, i2c)

class Ufo_controller:
    def __init__(self, width, left_pin, right_pin, height = 8):
        self.width = width
        self.height = height
        self.left = Pin(left_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.right = Pin(right_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.x = self.center() # initial x
        self.y = screen_height - 8  # the lowest point this sprite can be displayed at
    
    def render(self):
        screen.fill(0)
        sprite = "<" + "=" * (self.width - 2) + ">"
        screen.text(sprite, self.x, self.y, 1)
        screen.show()
        
    def center(self):
        return int((screen_width - self.width * self.height) / 2)
        
    def max_x(self):
        return screen_width - self.width * self.height # How far right the UFO can go
    
    def move(self, cord):
        # This could fit in one if statement, but it is split in two for clarity.
        if self.x + cord + self.width > self.max_x(): # return if UFO is trying to go TOO far right
            return
        elif self.x + cord < 0: # also return if UFO is trying to TOO far left
            return
        self.x += cord
        self.render() # refresh the screen
    
    def playing(self):
        self.render()
        while True:
            if(self.left.value() == 0): # Go left
                self.move(-1)
            elif (self.right.value() == 0): # Go right
                self.move(1)
            
            
        
# min width is 2, which results in <> as the sprite.
# width higher than 8 is not recommended.
# 9 and 7 are the control pins, SW_2 is left and SW_0 is right.
UFO = Ufo_controller(3, 7, 9) 
UFO.playing() # starts game loop