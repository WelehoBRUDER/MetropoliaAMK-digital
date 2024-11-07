from machine import Pin, I2C
from fifo import Fifo
import framebuf
from ssd1306 import SSD1306_I2C
import time

# Set OLED width and height in pixels
screen_width = 128
screen_height = 64

# Create OLED controller titled "screen".
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
screen = SSD1306_I2C(screen_width, screen_height, i2c)

# Adds a cute little LED sprite :)
bulb_bitmap = bytearray([0x00,0x00,0x1e,0x33,0xe9,0x89,0xe9,0x33,0x1e,0x00,0x00])
bulb = framebuf.FrameBuffer(bulb_bitmap, 11, 8, framebuf.MONO_VLSB)

# Class copied from lecture slides with 0 modifications
class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

rot = Encoder(10, 11)

# LED and menu controller class
class LED_Menu:
    def __init__(self, rot_click):
        self.click = Pin(rot_click, mode = Pin.IN, pull = Pin.PULL_UP)
        self.click.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        self.select = 0
        self.prev_tick = 0
        self.fifo = Fifo(10, typecode = "i")
        self.leds = [Pin(22, Pin.OUT), Pin(21, Pin.OUT), Pin(20, Pin.OUT)]
    
    def scroll(self, amnt):
        # Increment self.select by either +1 or -1
        self.select += amnt
        # Wrap the selector if it goes out of bounds
        if self.select >= len(self.leds):
            self.select = 0
        elif self.select < 0:
            self.select = len(self.leds) - 1
            
    def update(self):
        # Reset screen
        screen.fill(0)
        # Go through each LED
        for i in range(len(self.leds)):
            # Determine on/off text based on LED value
            on_off = "ON" if self.leds[i].value() else "OFF"
            text = f"LED{i + 1} - {on_off}"
            # Add extra effects if current LED is selected
            if i == self.select:
                text = f"[{text}]"
                # Draws a horizontal line below the text (looks fancy)
                screen.hline(0, i * 12 + 8, len(text) * 8, 1)
            # Print text, leaving a 4px vertical margin between each one.
            screen.text(text, 0, i * 12, 1)
        screen.show()
        
    def update_leds(self, data):
        if data > 0:
            # Toggle LEDs
            if(self.leds[self.select].value()):
                self.leds[self.select].off()
            else:
                self.leds[self.select].on()
        
    
    def handler(self, pin):
        # Get current time ticks in ms
        tick = time.ticks_ms()
        # Compare to previous stamp, if time between is below 50ms, return.
        if tick - self.prev_tick < 50:
            return
        if not self.click():
            self.fifo.put(1)
        else:
            self.fifo.put(0)

        # Update previous stamp
        self.prev_tick = tick
        



menu = LED_Menu(12)
        
# main loop
while True:
    while menu.fifo.has_data():
        menu.update_leds(menu.fifo.get())
    while rot.fifo.has_data():
        menu.scroll(rot.fifo.get())
    
    menu.update()

