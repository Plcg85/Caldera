#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

#este script es llamado desde la pagina web de la calefaccion y
#cambia el valor del archivo homepi/Caldera/datos/encendido_forzoso.txt a
#forzoso_off

try:
    if (os.path.exists("/home/pi/Caldera/datos/encendido_forzoso.txt")):
        f = open("/home/pi/Caldera/datos/encendido_forzoso.txt","r")
        estado_forzoso = str(f.readline())
        f.close()
        if (estado_forzoso == "forzoso_on"):
            f = open("/home/pi/Caldera/datos/encendido_forzoso.txt","w")
            f.write("forzoso_off")
            f.close()
        else:
            print("estado_forzoso esta en off, no hare nada")
    else:
        print("No existe /home/pi/Caldera/datos/encendido_forzoso.txt pues no hago nada")
except:
    print ("No se puede acceder a el archivo /home/pi/Caldera/datos/encendido_forzoso.txt")
