from machine import ADC, Pin
from fifo import Fifo
from piotimer import Piotimer

class Forbidden_Zone:
    def __init__(self, dig, adc):
        self.dig = Pin(dig, Pin.IN)
        self.adc = ADC(Pin(adc, Pin.IN))
        self.prev = 0
        self.fifo = Fifo(size=50, typecode='i')
        self.tmr = Piotimer(freq=10, callback=self.callback)

    def callback(self, tmr):
        if self.dig.value() == 1:
            if self.prev == 0:
                self.fifo.put(1)
                #print("Triggered High", self.get_volts())
                self.prev = 1
        else:
            if self.prev == 1:
                self.fifo.put(0)
                #print("Triggered Low", self.get_volts())
                self.prev = 0
                
    def get_volts(self):
        adc_value = self.adc.read_u16()
        voltage = adc_value / ((1 << 16) - 1) * 3.3
        return "| VOLTAGE: {:1.3}V".format(voltage)
        
        

fz = Forbidden_Zone(26, 27)

while True:
    while fz.fifo.has_data():
        value = fz.fifo.get()
        if value == 1:
            print("Triggered High", fz.get_volts())
        else:
            print("Triggered Low", fz.get_volts())
    