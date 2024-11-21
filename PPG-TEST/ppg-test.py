from machine import ADC, Pin
from fifo import Fifo
from piotimer import Piotimer
from time import sleep_ms
import micropython
micropython.alloc_emergency_exception_buf(200)


class HeartMaster:
    def __init__(self):
        self.min = 99999999
        self.max = 0
        self.peak = 0
        self.signal = 0
        self.thresh = 0
        self.peaks = []
        self.count = 0
        self.loops = 0
        self.fifo = Fifo(30, typecode = "i")
        self.dipped = True
        self.ppg = ADC(Pin(27))
        self.tmr = Piotimer(period=4, mode=Piotimer.PERIODIC, callback=self.adc_callback)
        
    def adc_callback(self, ms):
        value = self.ppg.read_u16()
        self.fifo.put(value)
        
    def set_thresh(self):
        if self.signal > self.max:
            self.max = self.signal
        if self.signal < self.min:
            self.min = self.signal
        
    def calc_thresh(self):
        self.thresh = int((self.max - self.min) * 0.8 + self.min)
        self.max = 0
        
    def measure(self):
        if(self.count % 1000 == 0):
            self.calc_thresh()
            self.loops += 1
            self.prev_max = 0
            
        self.set_thresh()
            
        #print("signal:",self.signal, "threshold:",self.thresh)
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
        for i in range(0, len(self.peaks) - 1):
            time = ((1 / 250) * (self.peaks[i + 1] - self.peaks[i]))
            hr.append(int(60 / time))
            
        heart_rates = []
        median = hr[int(len(hr) / 2)]
            
        for i in range(len(hr)):
            # median boundaries
            size = 7
            start = i
            end = min(len(hr), i + size)
            if end < i + size:
                diff = i + size - end
                start = i - diff
            
            # segment
            window = hr[start:end]
            
            # median
            sorted_window = sorted(window)
            window_size = len(sorted_window)
        
            
            heart_rates.append(int(sorted_window[window_size // 2]))
                 
        return heart_rates
        
heart_master = HeartMaster()

while True:
    while heart_master.fifo.has_data():
        heart_master.signal = heart_master.fifo.get()
        heart_master.measure()
        
    if len(heart_master.peaks) > 1:
        time = ((1 / 250) * (heart_master.peaks[1] - heart_master.peaks[0]))
        print(int(60 / time))
        heart_master.peaks = []

