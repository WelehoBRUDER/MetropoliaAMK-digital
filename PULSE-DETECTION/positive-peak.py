from filefifo import Filefifo 
data = Filefifo(10, name = 'capture_250Hz_01.txt')
Fs = 250

peaks = []
current_slope = 0
interval_calculator = 0

prev_max = 0
curr_peak = 0

last_sample = 0
last_slope = 0

iterator = 0

while len(peaks) < 4:
    curr_sample = data.get()
    slope = curr_sample - last_sample
    if curr_sample > prev_max:
        prev_max = curr_sample
        curr_peak = iterator
    if slope <= 0 and last_slope > 0:
        peaks.append(curr_peak)
        prev_max = 0
        
    last_sample = curr_sample
    last_slope = slope
    iterator += 1


        
        
times = []
average_time = 0
for i in range(len(peaks) - 1):
    times.append((1 / 250) * (peaks[i + 1] - peaks[i]))
        
    average_time += times[i]
    
average_time = average_time / len(times)
        

print("Peaks", peaks)
print("Intervals (s)", times)
print("Frequency (Hz)", 1 / average_time)
        
        
    

        
    