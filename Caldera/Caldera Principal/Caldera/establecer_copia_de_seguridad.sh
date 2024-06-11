#!/bin/bash
#este script es activado por cron todas las noches a las 23:59 y lo que hace es 
#poner un archivo dentro de la carpeta datos escribir true("home/pi/caldera/datos/copia.txt")

file=/home/pi/Caldera/datos/copia.txt
	if [ -e $file ]; then
		#el fichero existe, se borra y se crea y rellena a true
		rm -r /home/pi/Caldera/datos/copia.txt
		echo "True" >> /home/pi/Caldera/datos/copia.txt
	else
		#el fichero no existe,se crea y se pone a true
		echo "True" >> /home/pi/Caldera/datos/copia.txt
	fi