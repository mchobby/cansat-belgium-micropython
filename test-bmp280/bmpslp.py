# Read Local pressure
# Calculate corresponding SLP pressure
#   (SLP: sea level pressure)
#
from machine import I2C, Pin
# BME280 aslo work for BMP280
from bme280 import BME280, BMP280_I2CADDR
from time import sleep

i2c = I2C(0, sda=>Pin(8), scl=Pin(9) )

# Sensor altitude required to
# calculate SLP (See Level Pressure)
altitude = 120.1 
bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )
while True:
    # returns a tuple with (temperature, pressure_hPa, humidity)
    p = bmp.raw_values[1]
    p_sea = p + (altitude/8.3)
    print( "Plocal: %6.1f hPa, Psea: %6.1f hPa" % (p,p_sea) )
    sleep(1) 


