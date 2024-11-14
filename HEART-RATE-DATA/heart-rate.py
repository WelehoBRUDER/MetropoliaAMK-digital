from machine import Pin, I2C
from fifo import Fifo
import time
from filefifo import Filefifo

# Read the file
file = Filefifo(10, name = 'capture02_250Hz.txt')
# Set how many values should be read from the file
samples = 2000

peaks = []
current_slope = 0
interval_calculator = 0

values = []
for _ in range(samples):
    val = file.get()
    values.append(val)
    
threshold = int((max(values) + min(values)) / 2)

prev_signal = 0
prev_max = 0
prev_slope = 0
peak = 0
i = 0
was_below = True
while len(peaks) < 20:
    signal = file.get()
    slope = signal - prev_signal
    if signal > threshold and signal > prev_max:
        peak = i
        prev_max = signal
    if signal > threshold and slope <= 0 and prev_slope > 0:
        if was_below:
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
print(hr)