from machine import Pin, I2C
from fifo import Fifo
import time
from filefifo import Filefifo
from ssd1306 import SSD1306_I2C

# Read the file
file = Filefifo(10, name = 'capture_250Hz_01.txt')
# Set how many values should be read from the file
values = 1000
# Init min and max values
min_val = file.get()
max_val = file.get()
# Create empty data list
data = []

# Set OLED width and height in pixels
screen_width = 128
screen_height = 64

# Create OLED controller titled "screen".
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
screen = SSD1306_I2C(screen_width, screen_height, i2c)

# Read values and insert to data while finding min and max
for _ in range(values):
    value = file.get()
    if value > max_val:
        # Prevent stupid pixel gap in the middle of the screen
        max_val = value + 1
    if value < min_val:
        min_val = value
        
    data.append(value)
    
class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-2)
        else:
            self.fifo.put(2)
            
            
rot = Encoder(10, 11)
            

class Sine_Controller:
    def __init__(self):
        self.x = 0
        self.lines = []
        
        self.convert_lines(data)
        
    # Converts raw data to list of values between 0-64
    def convert_lines(self, array):
        for item in array:
            self.lines.append(int((item - min_val) / (max_val - min_val) * 64))
            
    # Refresh the entire screen and draw every pixel currently visible from left to right
    def draw_screen(self):
        screen.fill(0)
        for i in range(0, 127):
            # Y axis of the pixel comes from the decoded values (0-64)
            screen.pixel(i, self.lines[i + self.x], 1)
        
        
    def update_screen(self):
        # Draw and show :D
        self.draw_screen()
        screen.show()
        
    def scroll_screen(self, amnt):
        # Set previous and current X cord
        prev = self.x
        self.x -= amnt
        # Prevent scrolling when at left or right edge
        if self.x < 0:
            self.x = 0
            return
        if self.x >= len(self.lines) - 127:
            self.x = len(self.lines) - 128
            return
        
    
    
    
sine = Sine_Controller()
sine.draw_screen()


while True:
    while rot.fifo.has_data():
        sine.scroll_screen(-rot.fifo.get())
        
    sine.update_screen()
            