#!/bin/bash
fecha=$(date +%d_%B_%Y) 
mkdir /home/pi/Caldera/copias_de_seguridad
mkdir /home/pi/Caldera/copias_de_seguridad/$fecha

file=/home/pi/Caldera/datos/datos.txt 
if [ -e $file ]; then
	mv /home/pi/Caldera/datos/datos.txt /home/pi/Caldera/copias_de_seguridad/$fecha/datos.txt
fi

file=/home/pi/Caldera/datos/apagados_bomba.txt 
if [ -e $file ]; then
	mv /home/pi/Caldera/datos/apagados_bomba.txt /home/pi/Caldera/copias_de_seguridad/$fecha/apagados_bomba.txt
fi

file=/home/pi/Caldera/datos/conexiones_fallidas.txt 
if [ -e $file ]; then
	mv /home/pi/Caldera/datos/conexiones_fallidas.txt /home/pi/Caldera/copias_de_seguridad/$fecha/conexiones_fallidas.txt
fi

file=/home/pi/Caldera/datos/encendidos_bomba.txt 
if [ -e $file ]; then
	mv /home/pi/Caldera/datos/encendidos_bomba.txt /home/pi/Caldera/copias_de_seguridad/$fecha/encendidos_bomba.txt
fi

file=/home/pi/Caldera/datos/error_sensor_caldera.txt 
if [ -e $file ]; then
	mv /home/pi/Caldera/datos/error_sensor_caldera.txt /home/pi/Caldera/copias_de_seguridad/$fecha/error_sensor_caldera.txt
fi

file=/home/pi/Caldera/datos/log_paramiko.log 
if [ -e $file ]; then
	mv /home/pi/Caldera/datos/log_paramiko.log /home/pi/Caldera/copias_de_seguridad/$fecha/log_paramiko.log
fi

file=/home/pi/Caldera/datos/temp_casa.txt 
if [ -e $file ]; then
	mv /home/pi/Caldera/datos/temp_casa.txt /home/pi/Caldera/copias_de_seguridad/$fecha/temp_casa.txt
fi

file=/home/pi/Caldera/datos/tiempo_quemando.txt 
if [ -e $file ]; then
	mv /home/pi/Caldera/datos/tiempo_quemando.txt /home/pi/Caldera/copias_de_seguridad/$fecha/tiempo_quemando.txt
fi

