""" Mission 1 - Cansat Emitter Module (error reinforced)

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
BMP280 breakout   : https://shop.mchobby.be/product.php?id_product=1118
TMP36             : https://shop.mchobby.be/product.php?id_product=59
Raspberry-Pi PICO : https://shop.mchobby.be/product.php?id_product=2025

See Tutorial
   https://wiki.mchobby.be/index.php?title=ENG-CANSAT-PICO-BELGIUM

See GitHub
   https://github.com/mchobby/cansat-belgium-micropython/tree/main/mission1
"""

from machine import SPI, I2C, Pin, ADC
from rfm69 import RFM69
from bme280 import BME280, BMP280_I2CADDR
import time

# Onboard LED
led = Pin(25, Pin.OUT)
def led_error( count ):
    global led
    while True:
        for i in range(10):
            led.on()
            time.sleep_ms(40)
            led.off()
            time.sleep_ms(40)
        time.sleep(0.6)
        for i in range( count ):
            led.on()
            time.sleep(0.6)
            led.off()
            time.sleep(0.6)

FREQ           = 433.1
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 120 # ID of this node
BASESTATION_ID = 100 # ID of the node (base station) to be contacted

# Buses & Pins
spi = SPI(0, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )
i2c = I2C(0)

# RFM Module
try:
    rfm = RFM69( spi=spi, nss=nss, reset=rst )
except Exception as err:
	print( '[ERROR] ', err )
	led_error(1)

rfm.frequency_mhz  = FREQ
rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node           = NODE_ID # This instance is the node 120
rfm.destination    = BASESTATION_ID # Send to specific node 100
# BMP280 (uses the BME280)
try:
    bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )
except Exception as err:
	print( '[ERROR] ', err )
	led_error(2)

# TMP36 analog pin
adc = ADC(Pin(26))

# Main Loop
print( 'Frequency     :', rfm.frequency_mhz )
print( 'encryption    :', rfm.encryption_key )
print( 'NODE_ID       :', NODE_ID )
print( 'BASESTATION_ID:', BASESTATION_ID )
print( '***HEADER***' )
print( ":iteration_count,time_sec,pressure_hpa,tmp36_temp,bmp280_temp;" )
print( '***DATA***' )
counter = 1
ctime = time.time() # Now

try:
	while True:
		# read BMP280
		try:
			t,hpa,rh =  bmp.raw_values # Temp, press_hPa, humidity
		except Exception as err:
			print( '[ERROR] ', err )
			led_error(3)
		# Read tmp36
		value = adc.read_u16()
		mv = 3300.0 * value / 65535
		temp = (mv-500)/10
		# message: iteration_count,time_sec,pressure_hpa,tmp36_temp,bmp280_temp (coma separated)
		msg = ":%i,%i,%6.2f,%5.2f,%5.2f;" % (counter,time.time()-ctime,hpa,temp,t)
		led.on() # Led ON while sending data
		print( msg )
		# Send a packet without ACK - Send it, don't care if it is received or not
		rfm.send(bytes(msg , "utf-8") )
		led.off()
		counter += 1
		time.sleep(0.4) # wait 0.4 second
except Exception as err:
	print( '[ERROR] ', err )
	led_error(4)
