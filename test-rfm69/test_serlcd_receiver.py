""" CANSAT PICO SerLCD RECEIVER node

test_receiver but using a Sparkfun SerLCD + PICO-RFM69-433-BOOT + Pico

Receives message requiring ACK over RFM69HCW SPI module - RECEIVER node
Must be tested togheter with test_emitter

See Tutorial : https://wiki.mchobby.be/index.php?title=ENG-CANSAT-PICO-RFM69HCW-TEST
See GitHub : https://github.com/mchobby/cansat-belgium-micropython/tree/main/test-rfm69
see Github : https://github.com/mchobby/esp8266-upy/tree/master/qwiic-serlcd-i2c

PICO-RFM69-433-BOOT : https://shop.mchobby.be/product.php?id_product=2822
PICO                : https://shop.mchobby.be/product.php?id_product=2025
SERLCD-16x2-I2C-POS : https://shop.mchobby.be/product.php?id_product=2681
FIL-JSTSH4-TO-MALE-150mm : https://shop.mchobby.be/product.php?id_product=2429

"""

from machine import SPI, Pin, I2C
from rfm69 import RFM69
from serlcd import SerLCD
import time

led = Pin( 25, Pin.OUT)
led.off()

FREQ           = 433.1
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 100 # ID of this node

# Because of Pico-2-BB the SPI Bus must be relocated on SPI(1)
spi = SPI(0,  miso=Pin(4), mosi=Pin(7), sck=Pin(6), polarity=0, phase=0, firstbit=SPI.MSB) # baudrate=50000,
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )
i2c = I2C( 0, sda=Pin(8), scl=Pin(9), freq=100_000 )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = FREQ

lcd = SerLCD( i2c, cols=16, rows=2 )
lcd.splash( enable=False )
lcd.system_messages( enable=False )
lcd.clear()
lcd.backlight( (0,0,255) ) # Blue
lcd.contrast( 0 ) # Highest contrast. Value (0..255)

# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node = NODE_ID # This instance is the node 123

print( 'Freq            :', rfm.frequency_mhz )
print( 'NODE            :', rfm.node )
lcd.print( "%3.1fMhz"% (rfm.frequency_mhz), (0,0) )
time.sleep_ms( 10 )
lcd.print( 'Listening...', (0,1))
time.sleep_ms( 10 )


print("Waiting for packets...")
try:
	while True:
		packet = rfm.receive( with_ack=True )
		# Optionally change the receive timeout from its default of 0.5 seconds:
		# packet = rfm.receive(timeout=5.0)
		# If no packet was received during the timeout then None is returned.
		if packet is None:
			# Packet has not been received
			pass
		else:
			# Received a packet!
			print( "Received (raw bytes):", packet )
			# And decode to ASCII text
			packet_text = str(packet, "ascii")
			print("Received (ASCII):", packet_text)
			print("-"*40)
			lcd.print( packet_text[:16], (0,1) )
			time.sleep_ms( 10 )
			if rfm.rssi != None:
				lcd.print( "%3.2f"%rfm.rssi, (9,0) )
			else:
				lcd.print( "+++++", (9,0) )
except:
	# Somtetime we got error on lcd.print()
	#
	# OSError: [Errno 5] EIO
	while True:
		led.toggle() # Signal en ERROR
		time.sleep_ms( 500 )
