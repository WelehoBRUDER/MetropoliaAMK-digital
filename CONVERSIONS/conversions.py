from machine import Pin
import time
import math

sw = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
LEDs = [Pin(22, Pin.OUT), Pin(21, Pin.OUT), Pin(20, Pin.OUT)]
b0 = Pin(22, Pin.OUT)
b1 = Pin(21, Pin.OUT)
b2 = Pin(20, Pin.OUT)
count = 0
i = 0

for led in LEDs:
    led.off()
    
while True:
    if not sw.value():
        time.sleep_ms(100)
        if not sw.value():
            count += 1
            if count > 7:
                count = 0

        print("CURRENT COUNT", count)
        for i in range(len(LEDs)):
             LEDs[i].value(count & 2 ** i)
             # I first tried using count << i & 4, but this lead to mirrored LEDs lighting


            

