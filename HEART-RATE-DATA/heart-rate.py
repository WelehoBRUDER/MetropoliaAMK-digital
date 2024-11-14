from machine import Pin, I2C
from fifo import Fifo
import time
from filefifo import Filefifo

# Read the file
file = Filefifo(10, name = 'capture03_250Hz.txt')

class HeartMaster:
    def __init__(self):
        self.min = 99999999
        self.max = 0
        self.peak = 0
        self.signal = 0
        self.thresh = 0
        self.peaks = []
        self.count = 1
        self.dipped = True
        
    def set_thresh(self):
        if self.signal > self.max:
            self.max = self.signal
        if self.signal < self.min:
            self.min = self.signal
        
    def calc_thresh(self):
        self.thresh = int((self.max + self.min) / 2)
        self.max = 0
        
    def measure(self):
        if(self.count % 250 == 0):
            self.calc_thresh()
            self.prev_max = 0
            
        self.set_thresh()
            
        #print("signal:",signal, "threshold:",threshold)
        if self.signal > self.thresh:
            self.peak = self.count
            
        if self.signal > self.thresh:
            if self.dipped:
                self.peaks.append(self.peak)
                self.dipped = False
        if self.signal <= self.thresh:
            self.dipped = True
        
        self.count += 1
        
    def get_heart_rates(self):
        hr = []
        average_time = 0
        for i in range(len(self.peaks) - 1):
            time = ((1 / 250) * (self.peaks[i + 1] - self.peaks[i]))
            hr.append(int(60 / time))
            
        heart_rates = []
                 
        for i in range(len(hr)):
            time = hr[i]
            if i > 0:
                if not time > hr[i - 1] * 1.5 and not time < hr[i - 1] * 0.5 and not time > 240 and not time < 40:
                     heart_rates.append(time)
            else:
                 heart_rates.append(time)
                 
        return heart_rates
        
heart_master = HeartMaster()

while len(heart_master.peaks) < 40:
    heart_master.signal = file.get()
    heart_master.measure()
    
        
heart_rate_values = heart_master.get_heart_rates()
print(heart_rate_values)