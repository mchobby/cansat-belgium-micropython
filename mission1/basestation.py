""" Mission 1 - BaseStation Receiver Module

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
BMP280 breakout   : https://shop.mchobby.be/product.php?id_product=1118
TMP36             : https://shop.mchobby.be/product.php?id_product=59
Raspberry-Pi PICO : https://shop.mchobby.be/product.php?id_product=2025

See Tutorial
   https://wiki.mchobby.be/index.php?title=ENG-CANSAT-PICO-BELGIUM

See GitHub
   https://github.com/mchobby/cansat-belgium-micropython/tree/main/mission1
"""

from machine import SPI, Pin
from rfm69 import RFM69
import time

FREQ           = 433.1
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 100 # ID of this node (BaseStation)

spi = SPI(0, polarity=0, phase=0, firstbit=SPI.MSB) # baudrate=50000,
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

led = Pin( 25, Pin.OUT )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = FREQ
rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node = NODE_ID # This instance is the node 123

print( 'Freq            :', rfm.frequency_mhz )
print( 'NODE            :', rfm.node )

print("Waiting for packets...")
while True:
	packet = rfm.receive( timeout=0.5 ) # Without ACK
	if packet is None: # No packet received
		print( "." )
		pass
	else: # Received a packet!
		led.on()
		print( "[DATA](len=%i,RSSI=%i)%s" % (len(packet),rfm.last_rssi,packet) )
		# And decode from ASCII text (to local utf-8)
		packet_text = str(packet, "ascii")
		print("[MSG]", packet_text)
		led.off()
