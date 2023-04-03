from machine import I2C, Pin, SPI
from bmp280 import *
from utime import sleep, sleep_ms
import ahtx0
from bh1750 import BH1750
from ssd1306 import SSD1306_SPI
import framebuf


sclPin = Pin(1)
sdaPin = Pin(0)

sclPin_2 = Pin(15)
sdaPin_2 = Pin(14)

sclPin_3 = Pin(17)
sdaPin_3 = Pin(16)

WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

i2c = I2C(0,scl=sclPin,sda=sdaPin, freq=200000) # la freq cannot rise above 100K, for the BMP280
i2c_2 = I2C(1,scl=sclPin_2, sda=sdaPin_2, freq=100000)

logo = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

spi = SPI(0,100000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
rst=Pin(20)
dc=Pin(17)
cs=Pin(2) # Not used in the display

addresses = i2c.scan()
addresses2 = i2c_2.scan()
print(i2c.scan())
print(i2c_2.scan())
# print(i2c_3.scan())

for i in addresses:
    print("Canal 0",hex(i))
for i in addresses2:
    print("Canal 1:",hex(i))    
bmp = BMP280(i2c_bus=i2c_2)
sleep_ms(100)
bmp.use_case(BMP280_CASE_INDOOR)

aht10 = ahtx0.AHT10(i2c) #0x38
bh1750 = BH1750(0x23, i2c) #0x23
# oled = SSD1306_I2C(WIDTH, HEIGHT, i2c_2)
oled=SSD1306_SPI(WIDTH,HEIGHT, spi,dc,rst,cs)

print("OK")

oled.text("joseDev", 38,0)
oled.blit(logo, 48, 18)
oled.show()
sleep(2)
oled.fill(0)

oled.rect(0,0,127,15,1)
oled.rect(0,16,127,47,1)
oled.text("ENVIRONMENT", 19, 4)

def getLuminity():
    return str(bh1750.measurement)

def getTemperatureHumidity():
    return str(aht10.temperature), str(aht10.relative_humidity)

def getPressure():
    return str(bmp.pressure)

while True:

    tempHum = getTemperatureHumidity()
    temp = tempHum[0]
    hum = tempHum[1]
    lux = getLuminity()
    pres=getPressure()
    print("Pres: {}".format(pres))
    print("Lum: {}".format(lux))
    print("Temp: {}".format(temp))
    print("Hum: {}".format(hum))
    oled.fill_rect(1, 17, 125, 40,0)
    oled.text("Hum: ",3,19)
    oled.text(hum,45, 19)
    oled.text("Temp: ",3,29)
    oled.text(temp,45, 29)
    oled.text("Lum: ",3,39)
    oled.text(lux,45, 39)
    oled.text("Pres: ",3,49)
    oled.text(pres,45, 49)
    oled.show()
    sleep_ms(200)



