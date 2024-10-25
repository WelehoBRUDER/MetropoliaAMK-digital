from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
screen_width = 128
screen_height = 64
center = int((screen_height - 1) / 2) # Rough middle of the screen height
screen = SSD1306_I2C(screen_width, screen_height, i2c)
screen.fill(0)

class Draw_controller:
    def __init__(self, up_pin, down_pin, reset_pin):
        self.x = 0 # Starting x coordinate
        self.y = center # Set y to roughly middle of the screen
        self.up = Pin(up_pin, mode=Pin.IN, pull=Pin.PULL_UP) # SW_2
        self.down = Pin(down_pin, mode=Pin.IN, pull=Pin.PULL_UP) # SW_0
        self.reset = Pin(reset_pin, mode=Pin.IN, pull=Pin.PULL_UP) # SW_1
        
    # Draws pixel at current x and y position.
    # Also checks if the x position reaches edge of screen.
    def draw_pixel(self):
        if self.x > screen_width:
            return self.draw_reset(False)
        screen.pixel(self.x, self.y, 1)
        screen.show()
        
    # This function resets the x position, and optionally clears the screen and resets y.
    def draw_reset(self, clear = True):
        if clear:
            screen.fill(0)
            self.y = center
        self.x = 0
        screen.show()
    
    def draw_loop(self):
        while True:
            self.x += 1
            self.draw_pixel()
            if self.up.value() == 0 and self.y - 1 >= 0: # Go up (limited to 0)
                self.y -= 1
            elif self.down.value() == 0 and self.y + 1 <= screen_height - 1: # Go down (limited to max screen height) 
                self.y += 1
            elif self.reset.value() == 0: # Clears the screen and resets drawing
                self.draw_reset()
            
DRAW = Draw_controller(7, 9, 8)
DRAW.draw_loop()