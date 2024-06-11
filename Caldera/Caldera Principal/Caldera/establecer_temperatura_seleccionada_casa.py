#! /usr/bin/env python
# -*- coding: utf-8 -*-

#este programa recibe la temperatura por parametro y la ajusta al archivo
#temp_seleccionada_casa.py
import sys
import os

temperatura = str((sys.argv[1]))

if (os.path.exists("/home/pi/Caldera/datos/temp_seleccionada_casa.txt")):  #si el arvivo existe
    os.remove('/home/pi/Caldera/datos/temp_seleccionada_casa.txt')        #se borra
    os.system('touch /home/pi/Caldera/datos/temp_seleccionada_casa.txt')  #se crea vacio
    f = open("/home/pi/Caldera/datos/temp_seleccionada_casa.txt","a") #se abre para lectura
    f.write(temperatura)
    f.close()
    os.system('sudo chmod 777 /home/pi/Caldera/datos/temp_seleccionada_casa.txt')
else:                                                      #si no existe
    os.system('touch /home/pi/Caldera/datos/temp_seleccionada_casa.txt')  #se crea
    f = open("/home/pi/Caldera/datos/temp_seleccionada_casa.txt","a")     #se le pone True 
    f.write("21.0") #se inicia con 21 grados
    f.close()
    os.system('sudo chmod 777 /home/pi/Caldera/datos/temp_seleccionada_casa.txt')



