# https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
# https://electrocredible.com/micropython-web-server-tutorial-examples/
# https://github.com/micropython/micropython/blob/master/examples/network/http_server.py

from machine import Pin
import time
import network
import socket

myLED = Pin(2, Pin.OUT)
myLED.value(0)

CONTENT = b"""\
HTTP/1.0 200 OK

Hello #%d from MicroPython!
"""

#WiFi credentials
ssid = 'No_Spoon'
password = 'morethan8'

wlan = network.WLAN(network.STA_IF)

#function to connect to Wi-Fi network
def cnctWifi():
    wlan.active(True)
    print('Attempting to connect to the network...')
    wlan.connect(ssid, password)        
    max_wait = 10
    while max_wait > 0 and not wlan.isconnected():
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    
    # Manage connection errors
    if not wlan.isconnected():
        print('Network Connection has failed')
    else:
        print('Connected to the network successfully.')
        status = wlan.ifconfig()
        print( 'Enter this address in browser = ' + status[0] )




def server():
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    counter = 0
    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        led_on = request.find('/?ledon') > 0
        if led_on:
            myLED.value(1)
        
        led_off = request.find('/?ledoff') > 0
        if led_off:
            myLED.value(0)
        
        conn.write(CONTENT % counter)

        conn.close()
        counter += 1
        print()

cnctWifi()
server()

