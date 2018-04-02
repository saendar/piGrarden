#!/usr/bin/python
from __future__ import print_function
import sys
import Adafruit_DHT
import os
import time 
from time import sleep
from datetime import datetime
import Adafruit_CharLCD as LCD
from multiprocessing import Process
import paho.mqtt.publish as publish
import psutil
import ssl

channelID = "462038"
apiKey = "H412GOQL8NP0LRHS"
useSSLWebsockets = True
mqttHost = "mqtt.thingspeak.com"
tTransport = "websockets"
tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
tPort = 443
topic = "channels/" + channelID + "/publish/" + apiKey

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

def iot():
    while True:

        try:            
            time.sleep(15)
            humidity2, temperature2 = Adafruit_DHT.read_retry(11, 4)
            tPayload = "field1=" + str(temperature2) + "&field2=" + str(humidity2)        
            publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

        except BaseException as e:
            print ("e")
            continue

def log(): 

    file = open("/home/pi/data_log.csv", "a")
    if os.stat("/home/pi/data_log.csv").st_size == 0:
        file.write("Tiempo, Anyo, Mes, Dia, Hora, Minuto, Temperatura,Humedad\n")
                

    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        now = datetime.now()
        file.write(str(now)+","+str(now.year)+","+str(now.month)+","+str(now.day)+","+str(now.hour)+","+str(now.minute)+","+str(temperature)+","+str(humidity)+"\n")
        file.flush()
        time.sleep(5)
        
            

def display():
    while True:
        humidity1, temperature1 = Adafruit_DHT.read_retry(11, 4)
        lcd.message("Temp is: ")
        lcd.message(str(temperature1))
        lcd.message(" C\n")
        lcd.message("Hum is: ")
        lcd.message(str(humidity1))
        lcd.message(" %")
        time.sleep(5)
        lcd.clear()

if __name__=="__main__":
    
    p1 = Process(target = iot)
    p1.start()
    p2 = Process(target = log)
    p2.start()
    p3 = Process(target = display)
    p3.start()

#""except KeyboardInterrupt:
    #lcd.clear()
    #lcd.message("See you later\nalligator")  
    #print("keyboard interrupt detected, File closed")         
    #time.sleep(5)
    #lcd.clear()
    #file.close()
