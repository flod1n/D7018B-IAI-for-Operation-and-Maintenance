import machine
import ubinascii
import network
import ntptime
import random
from machine import Pin,I2C
from machine import ADC,Pin
import time
from time import sleep
import network
from umqtt.robust import MQTTClient
import time
import gc
import sys


def do_connect(WiFi_SSID, WiFi_PASSWORD, timeout=10):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connecting to network..')
        wlan.connect(WiFi_SSID, WiFi_PASSWORD)

        start_time = time.time()
        while not wlan.isconnected():
            if time.time() - start_time > timeout:
                print("Timeout: could not connect")
                return False
            time.sleep(1)
    
    print('Connected: ip info', wlan.ifconfig())
    return True

def get_temp_hum():

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
    # print("Temperature C: ", temp)

    # read Humidity
    data16 = read_HTU21D(0xE5)
    hum = -6 + (125.0 * data16) / 65536
    # print("Humidity: ", hum)
    return temp, hum

def get_moist():

    # Calibration will be required
    min_reading=1200
    max_reading=3110

    # create an ADC object acting on a pin
    moisture = ADC(Pin(0))
    # Full range: 3.3v
    moisture.atten(moisture.ATTN_11DB)

    # read a raw analog value in the range 0-4095
    reading = moisture.read()
    m = (max_reading-reading)*100/(max_reading-min_reading)
    moisture_value = '{:.1f} %'.format(m)
    
    return m

def get_lum():
    # Calibration will be required
    min_reading=0
    max_reading=5095
    # create an ADC object acting on a pin

    light = ADC(Pin(34))
    # Full range: 3.3v
    light.atten(ADC.ATTN_11DB)
    # read a raw analog value in the range 0-4095
    light_raw = light.read()
    li = (max_reading - light_raw )*100/(max_reading-min_reading)
    light_intensity = '{:.1f} %'.format(li)

    return li


def get_ntp_datetime(offset_hours=0):
    try:
        # Synka tid från NTP om inte redan gjort
        ntptime.settime()
    except:
        print("NTP failed")

    utc_time = time.time()

    local_time = utc_time + offset_hours * 3600

    tm = time.localtime(local_time)

    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        tm[0], tm[1], tm[2], tm[3], tm[4], tm[5]
    )
        
def collect_data():
    temp, hum = get_temp_hum()
    moist = get_moist()
    lum = get_lum()
    time = get_ntp_datetime(1)
    return temp, hum, moist, lum, time 
  
PUB_TIME_SEC = 15
SERVER = "mqtt.thingspeak.com"
client = MQTTClient("umqtt_client", SERVER)
# thingspeak creds
CHANNEL_ID = "2915692"
WRITE_API_KEY = "S0AXNQJR8IERE7B1"

#mqtt topic
topic = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY

# Configuration parameters
#=======================================================
WIFI_SSID = 'CasaDeSnopel'
WIFI_PASSWORD = 'ludvig1337'
THINGSPEAK_MQTT_CLIENT_ID = b"KiQkKAYoCAAfJDkqITAAMjo"
THINGSPEAK_MQTT_USERNAME = b"KiQkKAYoCAAfJDkqITAAMjo"
THINGSPEAK_MQTT_PASSWORD = b"pbMU4S9CoHQRy+X8h0qSHffA"
THINGSPEAK_CHANNEL_ID = b'2915692'
#=======================================================

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()
  
# connect to Thingspeak MQTT broker
# connection uses unsecure TCP (port 1883)
# 
# To use a secure connection (encrypted) with TLS: 
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses more heap space
THINGSPEAK_MQTT_USERNAME = THINGSPEAK_MQTT_CLIENT_ID

client = MQTTClient(server=b"mqtt3.thingspeak.com",
                    client_id=THINGSPEAK_MQTT_CLIENT_ID, 
                    user=THINGSPEAK_MQTT_USERNAME, 
                    password=THINGSPEAK_MQTT_PASSWORD, 
                    ssl=False)
                    
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

# continually publish two fields to a Thingspeak channel using MQTT


PUBLISH_PERIOD_IN_SEC = 20

while True:
    
    temp, hum, moist, lum, date = collect_data()
    freeHeapInBytes = gc.mem_free()

    credentials = bytes("channels/{:s}/publish".format(THINGSPEAK_CHANNEL_ID), 'utf-8') 

    payload_str = "field1={:.2f}&field2={:.2f}&field3={}&field4={}&field5={}".format(
        temp, hum, moist, lum, date
    )

    payload = bytes(payload_str, 'utf-8')

    client.connect()
    client.publish(credentials, payload)
    client.disconnect()
    time.sleep(PUBLISH_PERIOD_IN_SEC)

    
