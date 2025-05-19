# Electronics and Water are Enemies
# Keep sufficient distance between the two
# https://www.mdpi.com/1424-8220/20/12/3585
# https://makersportal.com/blog/2020/5/26/capacitive-soil-moisture-calibration-with-arduino
# https://lastminuteengineers.com/capacitive-soil-moisture-sensor-arduino/
# https://github.com/KIT-HYD/ESP32-Soil-Moisture/tree/main
# https://community.dfrobot.com/makelog-313602.html

from machine import ADC,Pin
import time

# Calibration will be required
min_reading = 1484
max_reading = 3174

minimum = 2000
maximum = 2000

# create an ADC object acting on a pin
moisture = ADC(Pin(33))
# Full range: 3.3v
moisture.atten(moisture.ATTN_11DB)


while True:
    # read a raw analog value in the range 0-4095
    reading = moisture.read()
    print('Reading: ', reading)
    
    if reading < minimum:
        minimum = reading
    if reading > maximum:
        maximum = reading
    m = (max_reading-reading)/(max_reading-min_reading)
    m2 = m*100
    moisture_value = '{:.1f} %'.format(m2)
    
    print('Soil Moisture:', moisture_value)
    print("m:", m)
    print('min, max-reading: ', minimum, maximum)
    
    time.sleep(2)
