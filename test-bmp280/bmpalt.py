# Read Local pressure then
# Calculate corresponding Altitude
#
from machine import I2C, Pin
# BME280 aslo work for BMP280
from bme280 import BME280, BMP280_I2CADDR
from time import sleep

i2c = I2C(0, sda=>Pin(8), scl=Pin(9) )

baseline = 1032.0 # Pressure at sea level
bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )
while True:
    # returns a tuple with (temperature, pressure_hPa, humidity)
    p = bmp.raw_values[1]
    altitude = (baseline - p)*8.3
    print( "Altitude: %f m" % altitude )
    sleep(1) 

