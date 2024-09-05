from machine import ADC, Pin
import time
led = Pin("LED", Pin.OUT)
adc = ADC(Pin(26))

while True:
    value = adc.read_u16()
    print(value)
    led.on()
    time.sleep_ms(int(value / 131.07)) # 131.07 is 65.535x2
    led.off()
    time.sleep_ms(int(value / 131.07))
    