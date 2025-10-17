""" CANSAT-BASE-V2 : Test the base board features
	
	- Init LCD & Keypad
	- Test the outputs with LEDs
	- wait 1 to be press 
	- test the radio


Test the radio
--------------
Emit message to the base station and wait for ACK (500ms max) over
RFM69HCW SPI module - EMITTER node
Must be tested togheter with test_receiver

Error-Code
----------
2 : SerLCD not detected on I2C
3 : Keypad not detected on I2C
4 : Error writing SerLCD
5 : Error accessing radio module

"""

from machine import SPI, I2C, Pin
from serlcd import SerLCD
from kpadi2c import Keypad_I2C
from rfm69 import RFM69
import time

led = Pin( 25, Pin.OUT, value=False )
i2c = I2C( 0, sda=Pin(8), scl=Pin(9), freq=20_000 )
lcd = None
kpad = None

def led_error( error_nr ):
	global led
	print( "led_error %i" % error_nr )
	while True:
		for i in range( 30 ):
			led.toggle()
			time.sleep_ms( 100 )
		led.off()
		time.sleep( 1 )
		for i in range( error_nr ):
			led.on()
			time.sleep_ms( 500 )
			led.off()
			time.sleep_ms( 500 )
		time.sleep( 1 )

def get_key():
	global kpad
	kpad.update_fifo()
	_btn = kpad.button # Retourne le code ASCII
	if _btn != 0: 
		# Flush the remaining
		_r = 1
		while _r != 0:
			kpad.update_fifo()
			_r = kpad.button # lecture du bouton suivant
	return _btn


def test_rfm():
	global lcd

	FREQ           = 433.1
	ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
	NODE_ID        = 120 # ID of this node
	BASESTATION_ID = 100 # ID of the node (base station) to be contacted

	spi = SPI(0, baudrate=50000, miso=Pin(4), mosi=Pin(7), sck=Pin(6), polarity=0, phase=0, firstbit=SPI.MSB)
	nss = Pin( 5, Pin.OUT, value=True )
	rst = Pin( 3, Pin.OUT, value=False )

	rfm = RFM69( spi=spi, nss=nss, reset=rst )
	rfm.frequency_mhz = FREQ
	rfm.tx_power = 20 # 20 dBm (maximum)

	# Optionally set an encryption key (16 byte AES key). MUST match both
	# on the transmitter and receiver (or be set to None to disable/the default).
	rfm.encryption_key = ( ENCRYPTION_KEY )
	rfm.node    = NODE_ID # This instance is the node 120

	print( 'Freq            :', rfm.frequency_mhz )
	print( 'NODE            :', rfm.node )
	print( 'BaseStation NODE:', BASESTATION_ID )

	# Send a packet and waits for its ACK.
	# Note you can only send a packet up to 60 bytes in length.
	counter = 1
	rfm.ack_retries = 3 # 3 attempt to receive ACK
	rfm.ack_wait    = 0.5 # 500ms, time to wait for ACK 
	rfm.destination = BASESTATION_ID # Send to specific node 100
	while True:
		led.toggle()
		print("Msg %i!" % counter )
		lcd.clear()
		lcd.print( "Msg %i!" % counter )
		ack = rfm.send_with_ack(bytes("Message %i!" % counter , "utf-8") )
		print("   +->", "ACK received" if ack else "ACK missing" )
		counter += 1
		time.sleep(1)


print( "starting..." )
# List will be empty if bus is not powered
led.on()
_scan = i2c.scan()
led.off()
if not( 0x72 in _scan ):
	led_error( 2 ) # SerLCD is missing
if not( 0x4B in _scan ):
	led_error( 3 ) # Keypad not detected

lcd = SerLCD( i2c, cols=16, rows=2 )

# Note: no error return when I2C bus not powered.
try:
	lcd.backlight( (0,255,0) ) # Vert
	lcd.clear()
	lcd.print( "Test outputs..." )
	print( "Test outputs..." )
except:
	led_error( 4 )

kpad = Keypad_I2C( i2c )

# Flush buffer
kpad.update_fifo()
_btn = kpad.button # Retourne le code ASCII
while _btn != 0:
	kpad.update_fifo()
	_btn = kpad.button # lecture du bouton suivant

# Blinking the LEDs
pins = [ 26, 27, 1, 0, 19, 18, 21, 20 ]
_outs = []
for pin in pins:
	_outs.append( Pin(pin, Pin.OUT, value=0) )
while get_key()==0: # No key pressed (retyurn ascii code)
	for p in _outs:
		p.on()
		time.sleep_ms( 50 )
		p.off()

for p in _outs:
	p.off()


lcd.clear()
lcd.print( "Test radio..." )
print( "Test radio..." )
try:
	test_rfm()
except:
	led_error( 5 )
