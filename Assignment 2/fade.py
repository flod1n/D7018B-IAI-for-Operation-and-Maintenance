from machine import Pin,I2C
from machine import ADC,Pin

import time

def get_lum():
    # Calibration will be required
    min_reading = 4095
    max_reading = 0

    # create an ADC object acting on a pin

    light = ADC(Pin(34))
    # Full range: 3.3v
    light.atten(ADC.ATTN_11DB)
    # read a raw analog value in the range 0-4095
    light_raw = light.read()
    li = (max_reading - light_raw )*100/(max_reading-min_reading)
    light_intensity = '{:.1f}%'.format(li)

    return light_intensity, light_raw

while True:
    print(get_lum())
    time.sleep(2)