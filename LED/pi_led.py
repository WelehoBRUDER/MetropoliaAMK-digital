from machine import ADC, Pin
import time
led = Pin("LED", Pin.OUT)
adc = ADC(Pin(27))


while True:
    value = adc.read_u16()
    print(value)
    led.on()
    time.sleep_ms(50)
    led.off()
    time.sleep_ms(50)