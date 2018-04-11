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
import RPi.GPIO as GPIO

channelID = "462038"
apiKey = "H412GOQL8NP0LRHS"
useSSLWebsockets = True
mqttHost = "mqtt.thingspeak.com"
tTransport = "websockets"
tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
tPort = 443
topic = "channels/" + channelID + "/publish/" + apiKey

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 23
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def iot():
    while True:

        try:            
            time.sleep(300)
            humidity, temperature = Adafruit_DHT.read_retry(11, 4)
            GPIO.output(GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)

            StartTime = time.time()
            StopTime = time.time ()

            while GPIO.input(GPIO_ECHO) == 0:
                StartTime = time.time()

            while GPIO.input(GPIO_ECHO) == 1:
                StopTime = time.time()

            TimeElapsed = StopTime - StartTime
            growth = (29.3 - (TimeElapsed * 34300) / 2)
            
            tPayload = "field1=" + str(temperature) + "&field2=" + str(humidity) + "&field3=" + str(growth)
            publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

        except BaseException:
            continue



def log(): 

    file = open("/home/pi/data_log.csv", "a")
    if os.stat("/home/pi/data_log.csv").st_size == 0:
        file.write("Tiempo,Temperatura,Humedad, Crecimiento\n")
                

    while True:
        humidity1, temperature1 = Adafruit_DHT.read_retry(11, 4)
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time ()

        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        growth1 = (29.3 - (TimeElapsed * 34300) / 2)
        now = datetime.now()
        file.write(str(now)+","+str(temperature1)+","+str(humidity1)+","+str(growth1)+"\n") #+str(now.year)+","+str(now.month)+","+str(now.day)+","+str(now.hour)+","+str(now.minute)+","
        file.flush()
        time.sleep(15)
                    

if __name__=="__main__":
    
    p1 = Process(target = iot)
    p1.start()
    p2 = Process(target = log)
    p2.start()


#except KeyboardInterrupt:
    #lcd.clear()
    #lcd.message("See you later\nalligator")  
    #print("keyboard interrupt detected, File closed")         
    #time.sleep(5)
    #lcd.clear()
    #file.close()
