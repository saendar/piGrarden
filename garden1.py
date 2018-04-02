#!/usr/bin/python
#Modulos a importar
import sys
import Adafruit_DHT
import os
import time 
from time import sleep
from datetime import datetime

try: 
# Configuracion del csv
        file = open("/home/pi/data_log.csv", "a")
        if os.stat("/home/pi/data_log.csv").st_size == 0:
                file.write("Tiempo, Anyo, Mes, Dia, Hora, Minuto, segundo, Temperatura,Humedad\n")
                
# Bucle principal para toma de datos y escritura en csv
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(11, 4)
            print("La temperatura es:", temperature,"C")
            print("La humedad es:", humidity,"%")
            now = datetime.now()
            file.write(str(now)+","+str(now.year)+","+str(now.month)+","+str(now.day)+","+str(now.hour)+","+str(now.minute)+","+str(now.second)+","+str(temperature)+","+str(humidity)+"\n")
            file.flush()
            time.sleep(1)
            
except KeyboardInterrupt:
        print("keyboard interrupt detected, File closed")       
        file.close()







    
    
