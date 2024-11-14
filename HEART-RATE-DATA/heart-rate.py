from machine import Pin, I2C
from fifo import Fifo
import time
from filefifo import Filefifo

# Read the file
file = Filefifo(10, name = 'capture03_250Hz.txt')
# Set how many values should be read from the file
samples = 2000

peaks = []
current_slope = 0
interval_calculator = 0

values = []
prev_signal = 0
prev_max = 0
prev_slope = 0
peak = 0
prev_min = 9999999
_max = 0
i = 0
was_below = True
last_batch = []
threshold = 0
while len(peaks) < 40:
    signal = file.get()
    slope = signal - prev_signal
    if signal < prev_min:
        prev_min = signal
    #print("signal:",signal, "threshold:",threshold)
    if signal > threshold and signal > prev_max:
        peak = i
        prev_max = signal
    if signal > threshold and slope <= 0 and prev_slope > 0:
        if was_below:
            threshold = int((prev_max + prev_min) / 2)
            peaks.append(peak)
            prev_max = 0
            was_below = False
    if signal <= threshold:
        prev_max = 0
        was_below = True
    prev_signal = signal
    prev_slope = slope
    i += 1
        
        
hr = []
average_time = 0
for i in range(len(peaks) - 1):
    time = ((1 / 250) * (peaks[i + 1] - peaks[i]))
    hr.append(int(60 / time))
    
heart_rates = []
         
for i in range(len(hr)):
    time = hr[i]
    if i > 0:
        if not time > hr[i - 1] * 1.5 and not time < hr[i - 1] * 0.6 and not time > 240 and not time < 40:
             heart_rates.append(time)
    else:
         heart_rates.append(time)
        
    
   
print(heart_rates)