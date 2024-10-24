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
        self.history = []
        
    def start_typing(self):
        while True:
            new_text = input("Type something: ")
            self.history.append(new_text)
            self.display_text()
            
    def scroll_to_latest(self):
        min_index = 0
        # How many lines can fit on the screen, assuming the font size is accurate
        max_display = int(screen.height / font_size)
        # If the history has more lines than can be displayed, we need to adjust
        if len(self.history) > max_display:
            # If history is for example 9, then this will yield 9 - 8 = 1
            min_index = len(self.history) - max_display
        return min_index
            
            
    def display_text(self):
        # Clear the screen
        screen.fill(0)
        # Set starting y value to scrolll
        y = self.scroll_to_latest()
        # this starts at y, which is at first 0 but then adjusts to fit the latest text in the screen
        for i in range(y, len(self.history)):
            txt = self.history[i]
            screen.text(txt, 0, font_size * (i - y), 1) # Since i = y at first, subtracting y from it gives us a starting height of 0
            i += 1
        screen.show()

TEXT_INPUT = Text_input()
TEXT_INPUT.start_typing()