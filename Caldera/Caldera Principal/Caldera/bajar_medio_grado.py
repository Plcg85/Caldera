#! /usr/bin/env python
# -*- coding: utf-8 -*-
#este escript sube medio grado la temperatura seleccionada de la casa

import os

if (os.path.exists("/home/pi/Caldera/datos/temp_seleccionada_casa.txt")):
    f = open("/home/pi/Caldera/datos/temp_seleccionada_casa.txt","r")
    temperatura_antigua = str(f.readline())
    f.close()
    temperatura_nueva = float(temperatura_antigua) - 0.5

    #se abre para escribir
    f = open("/home/pi/Caldera/datos/temp_seleccionada_casa.txt","w")
    f.write(str(temperatura_nueva))
    f.close()
