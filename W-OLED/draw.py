from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
screen_width = 128
screen_height = 64
center = int((screen_height - 1) / 2)
screen = SSD1306_I2C(screen_width, screen_height, i2c)
screen.fill(0)

class Draw_controller:
    def __init__(self, up_pin, down_pin, reset_pin):
        self.x = 0
        self.y = center
        self.up = Pin(up_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.down = Pin(down_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.reset = Pin(reset_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        
    def draw_pixel(self):
        if self.x > screen_width:
            return self.draw_reset()
        screen.pixel(self.x, self.y, 1)
        screen.show()
        
    def draw_reset(self):
        screen.fill(0)
        self.x = 0
        self.y = center
        screen.show()
    
    def draw_loop(self):
        while True:
            self.x += 1
            self.draw_pixel()
            if self.up.value() == 0 and self.y - 1 >= 0: # Go up
                self.y -= 1
            elif self.down.value() == 0 and self.y + 1 <= screen_height - 1: # Go down
                self.y += 1
            
DRAW = Draw_controller(7, 9, 8)
DRAW.draw_loop()