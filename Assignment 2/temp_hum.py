#https://www.i-programmer.info/programming/hardware/16441-esp32-in-micropython-i2c-htu21d-and-slow-reading-.html
#https://learn.adafruit.com/adafruit-htu21d-f-temperature-humidity-sensor/python-circuitpython
#https://github.com/peterhinch/micropython-async/tree/master/v3/as_drivers/htu21d
# https://cdn-shop.adafruit.com/datasheets/1899_HTU21D.pdf

from machine import Pin,I2C

def crcCheck(msb, lsb,check):
    data32 = (msb << 16)|(lsb <<8)| check
    divisor = 0x988000
    for i in range(16):
        if data32 & 1<<(23 - i):
             data32 ^= divisor
        divisor>>= 1
    return data32

i2c0=I2C(0,scl=Pin(18),sda=Pin(19),freq=100000)

def read_HTU21D(address):
    buf = bytearray([0xF3])
    i2c0.writeto( 0x40, buf, False)
    while True:
        try:
            read= i2c0.readfrom(0x40, 3, True)
            break
        except:
            continue
    msb = read[0]
    lsb = read[1]
    check = read[2]
    #print("msb lsb checksum =", msb, lsb, check)
    if crcCheck(msb,lsb,check):
        raise ValueError()
    data16= (msb << 8) |  (lsb & 0xFC)
    return data16

# read Temperature
data16 = read_HTU21D(0xE3)
temp = -46.85 + (175.72 * data16) / 65536
print("Temperature C: ", temp)

# read Humidity
data16 = read_HTU21D(0xE5)
hum = -6 + (125.0 * data16) / 65536
print("Humidity: ", hum)

