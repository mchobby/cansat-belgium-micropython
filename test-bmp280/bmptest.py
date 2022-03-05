# Read the sensor values:
#    (temperature_celcius, pressure_hpa, humidity_percent)
#    Humidity only applies to BME280 only, not BMP280. 
#
from machine import I2C
# BME280 aslo work for BMP280
from bme280 import BME280, BMP280_I2CADDR
from time import sleep
i2c = I2C(1)
bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )
while True:
    # returns a tuple with (temperature, pressure_hPa, humidity)
    print( bmp.raw_values )
    sleep(1) # 60*30 
