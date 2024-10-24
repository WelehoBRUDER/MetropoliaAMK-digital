from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
screen_width = 128
screen_height = 64
font_size = 8
screen = SSD1306_I2C(screen_width, screen_height, i2c)
screen.fill(0)

class Text_input:
    def __init__(self):
        self.line = 1 
        
    def start_typing(self):
        while True:
            new_text = input("Type something: ")
            self.write_text(new_text)
            self.line += 1
            
    def scroll_to_latest(self):
        # Scroll one line down
        screen.scroll(0, -font_size)
        # Draw black rectangle over the lowest row on the screen
        screen.fill_rect(0, screen_height - font_size, screen_width, font_size, 0)
    
    # Returns the maximum number of lines the screen can display
    def max_display(self):
        return int(screen.height / font_size)
    
    def write_text(self, text):
        # How many lines can be displayed at most
        limit = self.max_display()
        # Scroll by one line when at the bottom line
        if self.line > limit:
            self.line = limit
            self.scroll_to_latest()
        # Print text on screen
        screen.text(text, 0, (self.line - 1) * font_size)
        screen.show()

TEXT_INPUT = Text_input()
TEXT_INPUT.start_typing()