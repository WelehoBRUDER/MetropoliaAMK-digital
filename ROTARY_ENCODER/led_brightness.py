from machine import Pin, PWM
from fifo import Fifo
import time
from led import Led

class Encoder:
    def __init__(self, rot_a, rot_b, rot_c):
        # A, B relate to the rotation of the encoder
        # C is the click action
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.c = Pin(rot_c, mode = Pin.IN, pull = Pin.PULL_UP)
        self.led = PWM(Pin(22, Pin.OUT))
        self.fifo = Fifo(30, typecode = 'i')
        self.prev_click = -200
        # Set starting and max brightness to brightest possible
        self.brightness = 65535
        self.brightness_limit = 65535
        # Booleans used because I'm unsure about my coding practices
        self.led_on = False
        self.held = False
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
        self.led.freq(self.brightness)
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
    
    def click(self):
        # Prevent holding down the toggle button
        if not self.held:
            self.held = True
            tick = time.ticks_ms()
            # Long delay between clicks to prevent jankiness
            if tick - self.prev_click >= 200:
                # Toggle LED on or off, setting brightness to 0 or max.
                if not self.led_on:
                    self.led_on = True
                    self.led.duty_u16(self.brightness_limit)
                else:
                    self.led_on = False
                    self.led.duty_u16(0)
                self.prev_click = tick
            
    def change_brightness(self, value):
        # Brightness increment is multiplied by 650 because the total value is massive
        self.brightness += value * 650
        # Check if brightness is outside of limits
        # and reset it if it is.
        if self.brightness > self.brightness_limit:
            self.brightness = self.brightness_limit
        elif self.brightness < 0:
            self.brightness = 0
        # Update brightness in the led.
        self.led.duty_u16(self.brightness)
    

rot = Encoder(10, 11, 12)

while True:
    while rot.fifo.has_data():
        rot.change_brightness(rot.fifo.get())
    
    if not rot.c():
        rot.click()
    else:
        rot.held = False