from machine import Pin
import time

class Circuit:
    def __init__(self, lamp, button):
        self.led = Pin(lamp, Pin.OUT)
        self.btn = Pin(button, mode = Pin.IN, pull = Pin.PULL_UP)
        self.prev_click = -300
        
    def click(self):
        tick = time.ticks_ms()
        if tick - self.prev_click >= 300:
            if self.led.value() == 1:
                self.led.off()
            else:
                self.led.on()
            self.prev_click = tick

        
    

circuit = Circuit(26, 12)

while True:
    if circuit.btn.value() == 0:
        circuit.click()