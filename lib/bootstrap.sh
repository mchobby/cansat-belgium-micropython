#!/bin/bash
# Collecter les pilotes nécessaires
rm bme280.py
rm rfm69.py
rm adafruit_gps.py
rm gps_config.py
wget https://raw.githubusercontent.com/mchobby/esp8266-upy/refs/heads/master/bme280-bmp280/lib/bme280.py
wget https://raw.githubusercontent.com/mchobby/esp8266-upy/refs/heads/master/rfm69/lib/rfm69.py
wget https://raw.githubusercontent.com/mchobby/esp8266-upy/refs/heads/master/gps-ultimate/lib/adafruit_gps.py
wget https://raw.githubusercontent.com/mchobby/esp8266-upy/refs/heads/master/gps-ultimate/lib/gps_config.py
