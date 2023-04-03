import urequests as request
import ujson
import network
from time import sleep

SSID = 'CHATO'
PASSWORD = '35509837@'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)

while wlan.isconnected() != True:
    print("Trying to connect to: {}".format(SSID))
    sleep(1)
print(wlan.isconnected())