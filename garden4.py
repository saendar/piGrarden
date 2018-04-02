#!/usr/bin/python

from __future__ import print_function
import paho.mqtt.publish as publish
import psutil

import sys
import Adafruit_DHT
import os
import time 
from time import sleep
from datetime import datetime
import Adafruit_CharLCD as LCD

channelID = "462038"
apiKey = "H412GOQL8NP0LRHS"
useSSLWebsockets = True
mqttHost = "mqtt.thingspeak.com"

lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)



if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443
        
topic = "channels/" + channelID + "/publish/" + apiKey

try:
    file = open("/home/pi/data_log.csv", "a")
    if os.stat("/home/pi/data_log.csv").st_size == 0:
        file.write("Tiempo, Anyo, Mes, Dia, Hora, Minuto, Temperatura,Humedad\n")

    while(True):
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        now = datetime.now()  

        file.write(str(now)+","+str(now.year)+","+str(now.month)+","+str(now.day)+","+str(now.hour)+","+str(now.minute)+","+str(temperature)+","+str(humidity)+"\n")
        file.flush()

        tPayload = "field1=" + str(temperature) + "&field2=" + str(humidity)
        lcd.message("Temp is: ")
        lcd.message(str(temperature))
        lcd.message(" C\n")
        lcd.message("Hum is: ")
        lcd.message(str(humidity))
        lcd.message(" %")

        time.sleep(5)
        lcd.clear()       

    
        try:
            publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
            
        except:
            lcd.message ("Error")
            time.sleep(20)
            lcd.clear()

except KeyboardInterrupt:
        lcd.clear()
        print("keyboard interrupt detected, File closed")  
        lcd.message("See you later\nalligator")
        time.sleep(5)
        lcd.clear()    
        file.close()
