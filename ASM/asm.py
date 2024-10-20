from machine import ADC, Pin
import time
    
class Light_asm:
    def __init__(self, pin_button, pin_lamp, delay):
        self.button = Pin(pin_button, mode=Pin.IN, pull=Pin.PULL_UP)
        self.lamp = Pin(pin_lamp, Pin.OUT)
        self.delay = delay
        self.state = self.reset
        
    def execute(self):
        print(self.state.__name__)
        self.state()

    def reset(self):
        self.lamp.off()
        time.sleep_ms(self.delay)
        if not self.button.value():
            self.state = self.light
        else:
            self.state = self.reset
    
    def light(self):
        self.lamp.on()
        time.sleep_ms(self.delay)
        if self.button.value():
            self.state = self.held
        else:
            self.state = self.light

            
    def held(self):
        self.lamp.on()
        time.sleep_ms(self.delay)
        if self.button.value():
            self.state = self.held
        else:
            self.state = self.shut_down
    
    def shut_down(self):
        self.lamp.off()
        time.sleep_ms(self.delay)
        if self.button.value():
            self.state = self.reset
        else:
            self.state = self.shut_down 

LIGHT_ASM = Light_asm(7, 20, 50)

def Start_light_asm():
    while(True):
        LIGHT_ASM.execute()
        
        
class Alarm_system:
    def __init__(self, pin_button, pin_alarm, pin_lamp, pin_siren, delay):
        self.button = Pin(pin_button, mode=Pin.IN, pull=Pin.PULL_UP)
        self.alarm = Pin(pin_alarm, mode=Pin.IN, pull=Pin.PULL_UP)
        self.lamp = Pin(pin_lamp, Pin.OUT)
        self.siren = Pin(pin_siren, Pin.OUT)
        self.delay = delay
        self.state = self.reset
        
    def execute(self):
        print(self.state.__name__)
        self.state()
    
    def reset(self):
        self.lamp.off()
        self.siren.off()
        time.sleep_ms(self.delay)
        self.state = self.check_alarm
        
    def check_alarm(self):
        print("LAMP", self.lamp.value())
        if not self.alarm.value():
            if not self.lamp.value():
                self.state = self.activate
            else:
                self.state = self.blink
        else:
            if self.siren.value():  
               self.state = self.lamp_on
            else:
                self.state = self.reset
        time.sleep_ms(self.delay)
        
    def activate(self):
        self.lamp.on()
        self.siren.on()
        time.sleep_ms(self.delay)
        print(self.button.value())
        if not self.button.value():
            self.state = self.blink
        else:
            self.state = self.check_alarm
            
    def lamp_on(self):
        self.siren.off()
        self.lamp.on()
        time.sleep_ms(self.delay)
        self.state = self.check_alarm
            
    def blink(self):
        self.siren.off()
        self.lamp.on()
        time.sleep_ms(int(self.delay / 2))
        self.lamp.off()
        time.sleep_ms(int(self.delay / 2))
        self.state = self.blink
        
ALARM_SYSTEM = Alarm_system(7, 9, 22, 20, 100)

def Start_alarm_system():
    while(True):
        ALARM_SYSTEM.execute()
        
# Did this to keep both in the same file.
Start_light_asm()
# Start_alarm_system()
# Alarm system is not finished because I couldn't figure it out.

