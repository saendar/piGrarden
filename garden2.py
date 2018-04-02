#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi
import time
import Adafruit_CharLCD as LCD
import sys
import Adafruit_DHT

# Raspberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        lcd.message("Temp is: ")
        lcd.message(str(temperature))
        lcd.message(" C\n")
        lcd.message("Hum is: ")
        lcd.message(str(humidity))
        lcd.message(" %")
        time.sleep(5.0)

except KeyboardInterrupt:
    lcd.clear()

