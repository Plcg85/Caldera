#! /usr/bin/env python
# -*- coding: utf-8 -*-

#este script cambia al valor del archivo /home/pi/Caldera/datos/estado_script.txt
#a false para apagar la ejecucion del programa principal

import os

try:
    if (os.path.exists("/home/pi/Caldera/datos/estado_script.txt")):
        f = open("/home/pi/Caldera/datos/estado_script.txt","r")
        estado_script = str(f.readline())
        f.close()
        if (estado_script == "True"):
            f = open("/home/pi/Caldera/datos/estado_script.txt","w")
            f.write("False")
            f.close()
        else:
            print("ya esta apagado el programa principal, no hare nada")
    else:
        print("No existe /home/pi/Caldera/datos/estado_script.txt pues no hago nada")
except:
    print ("No se puede acceder a el archivo /home/pi/Caldera/datos/estado_script.txt")
