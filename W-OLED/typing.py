from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
screen_width = 128
screen_height = 64
screen = SSD1306_I2C(screen_width, screen_height, i2c)

