from filefifo import Filefifo 
data = Filefifo(10, name = 'capture_250Hz_01.txt')

time = 10 * 250

min_value = data.get()
max_value = data.get()

for _ in range(time):
    value = data.get()
    if value > max_value:
        max_value = value
    if value < min_value:
        min_value = value
        
print(max_value, min_value)
        
for _ in range(time):
    value = data.get()
    percentage = (value - min_value) / (max_value - min_value) * 100
    print(percentage)
    
    