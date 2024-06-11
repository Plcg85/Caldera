#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -version 2.0  22 noviembre 2018
# temperatura funcionamiento 60 temperatura maxima 72

# NOTAS DE LA VERSION 1.23
# 1.Añadido soporte para subir y bajar 0.5 grados la temperatura seleccionada
#------------------------------------------------------------------------------------------------------------------------------------------
# NOTAS DE LA VERSION 1.22
# 1.Corregido el bug por el que la temperatura minima de rele no volvia a su estado despues de la temperatura de consigna
#------------------------------------------------------------------------------------------------------------------------------------------
# NOTAS DE LA VERSION 1.21
# 1.Añadidas nuevas variables para controlar el rele y su funcionamiento. Cuando lleva mucho tiempo sin conseguir la temperatura de consigna
#   la temperatura de corte del rele se baja para que haya paso continuo de agua.
# 2.Añadida proteccion contra temperaturas superiores a 80 grados en la caldera
#-------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
# NOTAS DE LA VERSION 2.0
# 1.Ahora el accionador del rele es el arduino 
# 2.Anadida la libreria serial
# 3.Cambiado el modo de accion del rele
# 4.Modulo nuevo iniciar_serial
# 5.Modulo nuevo apagar_serial
#-------------------------------------------------------------------
#*abierto
#-cerrado
#              **- corta pasillo1(mas cerca del salon) baño
#              *-* corta dos del salon y cocina
#              -** corta dormitorio inma dormitorio matrim. y pasillo2 
#-------------------------------------------------------------------
import time
import serial
import os
import commands
import paramiko
#import RPi.GPIO as GPIO
from datetime import datetime

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(21, GPIO.OUT,initial=GPIO.LOW)

#******************************************************************#
#******************************************************************#
#*************************** FUNCIONES ****************************#
def hora_actual_sin_puntos():
    #devuelve la hora en string 'HHMMSS'
    hora = time.strftime("%H%M%S")
    return hora
def hora_actual():
    #devuelve la hora en string 'HH:MM:SS'
    hora = time.strftime("%H:%M:%S")
    return hora
def fecha():
    #devuelve dia_mes_ano__dia del anio (001-366)
    fecha = time.strftime("%d_%m_%Y__%j")
    return fecha
def enciende_bomba():
    print("encendiendo la bomba")
    #encender la bomba del agua
    #cambiar a encendida en archivo /home/pi/Caldera/estado_bomba.txt
    
    #os.system('echo out > /sys/class/gpio/gpio21/direction')
    #os.system("gpio -g mode 21 out")
    arduino.write("1")
    
    if (os.path.exists("/home/pi/Caldera/datos/estado_bomba.txt")):  #si el arvivo existe
        os.remove('/home/pi/Caldera/datos/estado_bomba.txt')        #se borra
        os.system('touch /home/pi/Caldera/datos/estado_bomba.txt')  #se crea vacio
        f = open("/home/pi/Caldera/datos/estado_bomba.txt","a")      
        f.write("encendida")
        f.close()
    else:                                                      #si no existe
        os.system('touch /home/pi/Caldera/datos/estado_bomba.txt')  #se crea
        f = open("/home/pi/Caldera/datos/estado_bomba.txt","a")     #se le pone True 
        f.write("encendida")
        f.close()
    return 0
def parar_la_bomba():
    print("parando la bomba")
    #asegurarse de que el relé esta en off
    #modificar archivo estado_bomba.txt a apagada
    #/home/pi/Caldera/estado_bomba.txt

    #os.system('echo in > /sys/class/gpio/gpio21/direction')
    #os.system("gpio -g mode 21 in")
    arduino.write("0")
    
    if (os.path.exists("/home/pi/Caldera/datos/estado_bomba.txt")):  #si el arvivo existe
        os.remove('/home/pi/Caldera/datos/estado_bomba.txt')        #se borra
        os.system('touch /home/pi/Caldera/datos/estado_bomba.txt')  #se crea vacio
        f = open("/home/pi/Caldera/datos/estado_bomba.txt","a")      
        f.write("apagada")
        f.close()
    else:                                                      #si no existe
        os.system('touch /home/pi/Caldera/datos/estado_bomba.txt')  #se crea
        f = open("/home/pi/Caldera/datos/estado_bomba.txt","a")     #se le pone True 
        f.write("apagada")
        f.close()
    return 0
def comprobar_estado_bomba():
    #comprobar y devolver estado bomba del archivo
    #/home/pi/Caldera/estado_bomba.txt
    #Hay dos estados ------encendida------apagada
    #devolver estado
    f = open("/home/pi/Caldera/datos/estado_bomba.txt","r")
    estado_bomba = f.readline()
    f.close()
    return estado_bomba
def setear_estado_script_a_true():
    #modificar a true el archivo que indica que este script esta
    #funcionando para poder pararlo
    #/home/pi/Caldera/estado_script.txt
    if (os.path.exists("/home/pi/Caldera/datos/estado_script.txt")):  #si el arvivo existe
        os.remove('/home/pi/Caldera/datos/estado_script.txt')        #se borra
        os.system('touch /home/pi/Caldera/datos/estado_script.txt')  #se vuelve a crear
        f = open("/home/pi/Caldera/datos/estado_script.txt","a")     #se le pone True 
        f.write("True")
        f.close()
    else:                                                      #si no existe
        os.system('touch /home/pi/Caldera/datos/estado_script.txt')  #se crea
        f = open("/home/pi/Caldera/datos/estado_script.txt","a")     #se le pone True 
        f.write("True")
        f.close()
        
def comprobar_estado_script():
    #comprobar estado en el archivo /home/pi/Caldera/estado_script.txt
    #devolver estado
    f = open("/home/pi/Caldera/datos/estado_script.txt","r")
    estado_script = f.readline()
    f.close()
    return estado_script
def apuntar_error_conexiones():
    print "apuntando error conexiones"
    hora = hora_actual()
    #guarda todas las conexiones fallidas en el archivo /Caldera/conexiones_fallidas.txt
    if (os.path.exists("/home/pi/Caldera/datos/conexiones_fallidas.txt")): #si el arvivo existe
        f = open("/home/pi/Caldera/datos/conexiones_fallidas.txt","a")      #se abre
        f.write(hora + '\n')         
        f.close()
    else:                                                  #si no existe
        os.system('touch /home/pi/Caldera/datos/conexiones_fallidas.txt')  #se crea
        f = open("/home/pi/Caldera/datos/conexiones_fallidas.txt","a")
        f.write(hora + '\n')
        f.close()
def apuntar_error_sensor_retorno():
    print "apuntando error_sensor retorno"
    hora = hora_actual()
    #guarda todos los errores de lectura del sensor del retorno en /Caldera/datos/errores_sensor_caldera
    if (os.path.exists("/home/pi/Caldera/datos/error_sensor_retorno.txt")):
        f = open("/home/pi/Caldera/datos/error_sensor_retorno.txt","a")
        f.write(hora + '\n')
        f.close()
    else:                                                  #si no existe
        os.system('touch /home/pi/Caldera/datos/error_sensor_retorno.txt')  #se crea
        f = open("/home/pi/Caldera/datos/error_sensor_retorno.txt","a")
        f.write(hora + '\n')
        f.close()
def apuntar_error_sensor_caldera():
    print "apuntando error sensor caldera"
    hora = hora_actual()
    #guarda todos los errores de lectura del sensor de la caldera en /Caldera/datos/errores_sensor_caldera
    if (os.path.exists("/home/pi/Caldera/datos/error_sensor_caldera.txt")):
        f = open("/home/pi/Caldera/datos/error_sensor_caldera.txt","a")
        f.write(hora + '\n')
        f.close()
    else:                                                  #si no existe
        os.system('touch /home/pi/Caldera/datos/error_sensor_caldera.txt')  #se crea
        f = open("/home/pi/Caldera/datos/error_sensor_caldera.txt","a")
        f.write(hora + '\n')
        f.close()
def guardar_hum_casa(hum_casa):
    print "guardar humedad casa"
    hora = hora_actual()
    #guarda todas la humedad capturadas a lo largo del dia de la casa
    if (os.path.exists("/home/pi/Caldera/datos/hum_casa.txt")): #si el arvivo existe
        f = open("/home/pi/Caldera/datos/hum_casa.txt","a")      #se abre
        f.write(str(hum_casa) + "     " + hora + '\n')         #se guarda la temp
        f.close()
    else:                                                  #si no existe
        os.system('touch /home/pi/Caldera/datos/hum_casa.txt')  #se crea
        f = open("/home/pi/Caldera/datos/hum_casa.txt","a")     #se le pone True 
        f.write(str(hum_casa) + "     " + hora + '\n')
        f.close()
def guardar_temp_casa(temp_casa):
    print "guardar temperatura casa"
    hora = hora_actual()
    #guarda todas las temperaturas capturadas a lo largo del dia de la casa
    if (os.path.exists("/home/pi/Caldera/datos/temp_casa.txt")): #si el arvivo existe
        f = open("/home/pi/Caldera/datos/temp_casa.txt","a")      #se abre
        f.write(str(temp_casa) + "     " + hora + '\n')         #se guarda la temp
        f.close()
    else:                                                  #si no existe
        os.system('touch /home/pi/Caldera/datos/temp_casa.txt')  #se crea
        f = open("/home/pi/Caldera/datos/temp_casa.txt","a")     #se le pone True 
        f.write(str(temp_casa) + "     " + hora + '\n')
        f.close()
def comprobar_ultima_temperatura_casa():
    print "comprobando la ultima temp porque ha fallado la lectura"
    #se lee el archivo temp_casa y se coge la ultima temperatura
    #primero hay que saber el numero de lineas
    with open('/home/pi/Caldera/datos/temp_casa.txt') as f:
        last = None
        for line in (line for line in f if line.rstrip('\n')):
            last = line
            
    ultima_temperatura_valida = last[0] + last[1] + last[2] + last[3] + last[4]
    print str(ultima_temperatura_valida)
    return (float(ultima_temperatura_valida))
def comprobar_ultima_hum_casa():
    print "comprobar ultima humedad casa"
    #se lee el archivo hum_casa y se coge la ultima hum
    #primero hay que saber el numero de lineas
    with open('/home/pi/Caldera/datos/hum_casa.txt') as f:
        last = None
        for line in (line for line in f if line.rstrip('\n')):
            last = line
            
    ultima_hum_valida = last[0] + last[1] + last[2] + last[3] 
    return (float(ultima_hum_valida))
def comprobar_temperatura_casa():
    print "comprobar temperatura casa"
    #con paramiko coger y delvolver temperatura casa
    try:
        paramiko.util.log_to_file("/home/pi/Caldera/datos/log_paramiko.log")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('192.168.1.101', port = 4564 , username = 'pi', password="jj2hkr7g9kekeet6")

        stdin,stdout,stderr = client.exec_command('grep "t=" /sys/bus/w1/devices/28-0000072aaf0f/w1_slave | cut -d\= -f2')
        temp_casa = stdout.read()
        temp_casa = float(temp_casa)
        temp_casa = temp_casa / 1000

        guardar_temp_casa(temp_casa)
        #print stderr.read() parece que aqui se guarda el error en caso de haberlo

        stdout.close()
        stdin.close()
        stderr.close()

        client.close
        return temp_casa
    except:
        print "error conexion capturado temperatura"
        apuntar_error_conexiones()
        #aqui se podia leer la ultima temperatura valida del archivo /Caldera/temp_casa.txt
        #y devolverla
        ultima_temp = comprobar_ultima_temperatura_casa()
        guardar_temp_casa(ultima_temp)
        return ultima_temp
        
def comprobar_humedad_casa():
    print "comprobar humedad casa"
    #con paramiko coger y delvolver humedad casa
    try:
        paramiko.util.log_to_file("/home/pi/Caldera/datos/log_paramiko.log")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('192.168.1.39', port = 4564 , username = 'pi', password="jj2hkr7g9kekeet6")

        stdin,stdout,stderr = client.exec_command('sudo /home/pi/sources/Adafruit_Python_DHT/examples/AdafruitDHT.py 2302 9 | cut -c 22-25')
        hum_casa = stdout.read()

        hum_casa = float(hum_casa)  # estad dos lineas parecen una tonteria pero con esto se elimina
        hum_casa = str(hum_casa)    # el retorno de carro que tiene la variable hum_casa

        guardar_hum_casa(hum_casa)
        #print stderr.read() parece que aqui se guarda el error en caso de haberlo

        stdout.close()
        stdin.close()
        stderr.close()

        client.close
        return hum_casa
    except:
        print "error conexion capturado humedad"
        #aqui se podia leer la ultima humedad validad del archivo y devolverla
        #y devolverla
        ultima_hum = comprobar_ultima_hum_casa()
        guardar_hum_casa(ultima_hum)
        return ultima_hum

def temperatura_sensor_caldera():
    #coger la temperatura sensor de la caldera y devolverla
    try:
        tfile = open("/sys/bus/w1/devices/28-800000034cec/w1_slave")
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return float(temperature - 0.2)
    except:
        apuntar_error_sensor_caldera()
        return 80
def temperatura_sensor_ida():
    #esta desactivado
    #coger la temperatura sensor de ida y devolverla
    temperatura_ida = 10.0
    return temperatura_ida
def temperatura_sensor_retorno():
    #coger la temperatura sensor del retorno y devolverla
    try:
        tfile = open("/sys/bus/w1/devices/28-800000035116/w1_slave")
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return float(temperature)
    except:
        apuntar_error_sensor_retorno()
        return 30
def comprobar_temperatura_seleccionada_casa():
    #coger y devolver la temperatura deseada para la casa del archivo
    #/home/pi/Caldera/temp_seleccionada_casa.txt+
    #si el archivo no existe se creara con 21.0 grados
    try:
        if (os.path.exists("/home/pi/Caldera/datos/temp_seleccionada_casa.txt")):  #si el arvivo existe
            f = open("/home/pi/Caldera/datos/temp_seleccionada_casa.txt","r") #se abre para lectura
            temp_seleccionada = f.readline()#se lee la temperatura
            f.close()
            return temp_seleccionada #se devuelve la temperatura
        else:                                                      #si no existe
            os.system('touch /home/pi/Caldera/datos/temp_seleccionada_casa.txt')  #se crea
            f = open("/home/pi/Caldera/datos/temp_seleccionada_casa.txt","a")     #se le pone True 
            f.write("22.0") #se inicia con 21 grados
            f.close()
            return "22.0"
    except:
        print "error leyendo temperatura seleccionada"
        print "devolviendo 21 por defecto"
        return "22.0"
def guardar_datos_para_grafica(temp_casa,temp_seleccionada_casa,temp_caldera,estado_bomba):
    #se guardan los datos para crear la grafica al final del dia con cron
    #en el archivo /home/pi/Caldera/datos.txt
    #el orden de escritura es hora,temp_casa,temp_seleccionada_casa,temp_caldera,bomba
    hora = hora_actual_sin_puntos()
    if (estado_bomba == "encendida"):
        bomba = "50"
    else:
        bomba = "0"
        
    if (os.path.exists("/home/pi/Caldera/datos/datos.txt")):  #si el arvivo existe
        f = open("/home/pi/Caldera/datos/datos.txt","a") #se abre para escritura
        f.write(str(hora) + " " + str(temp_casa) + " " +  str(temp_seleccionada_casa) + " " + str(temp_caldera) + " " + str(bomba) + '\n')
        f.close()
    else:                                                      #si no existe
        os.system('touch /home/pi/Caldera/datos/datos.txt')  #se crea
        f = open("/home/pi/Caldera/datos/datos.txt","a")     
        f.write(str(hora) + " " + str(temp_casa) + " " +  str(temp_seleccionada_casa) + " " + str(temp_caldera) + " " + str(bomba) + '\n')       
        f.close()
    return 0
def guardar_datos_base_mysql(temp_casa,temp_seleccionada_casa,temp_caldera,estado_bomba):
    #se guardan los datos en la base de datos
    if (estado_bomba == "encendida"):
        bomba = 40.0
    else:
        bomba = 30.0

    import MySQLdb
    db = MySQLdb.connect("localhost","root","jj2hkr7g","Temperaturas")
    cursor = db.cursor()
    cursor.execute("""INSERT INTO temps (temp1,temp2,temp3,temp4) VALUES (%s,%s,%s,%s) """,(temp_casa,temp_seleccionada_casa,temp_caldera,bomba))
    db.commit()
	
def apagar_serial():
	arduino.close()
def iniciar_archivo_copia_seguridad():
    #se crea el archivo ("home/pi/Caldera/datos/copia.txt") y se escribe a false
    if (os.path.exists("/home/pi/Caldera/datos/copia.txt")):  #si el arvivo existe
         os.remove('/home/pi/Caldera/datos/copia.txt')
         os.system('touch /home/pi/Caldera/datos/copia.txt')  #se vuelve a crear
         f = open("/home/pi/Caldera/datos/copia.txt","a")     #se le pone False 
         f.write("False")
         f.close()
    else:                                                      #si no existe
        os.system('touch /home/pi/Caldera/datos/copia.txt')  #se crea
        f = open("/home/pi/Caldera/datos/copia.txt","a")     #se le pone False 
        f.write("False")
        f.close()
    return 0
def comprobar_si_copia_de_seguridad():
    #aqui se comprueba si el archivo copia.txt esta a True
    #si esta a True se realiza la copia de seguridad
    f = open("/home/pi/Caldera/datos/copia.txt","r")
    lectura = str(f.readline())
    lectura = lectura.rstrip('\n')
    if (lectura == "True"):
        realizar_copia_de_seguridad()
    else:
        time.sleep(0.1)
def realizar_copia_de_seguridad():
    try:
        #se ejecuta el programa en bash que realiza la copia
        #os.system('sudo source /home/pi/Caldera/realizar_copia_seguridad.sh')
        res=commands.getoutput('sudo /home/pi/Caldera/realizar_copia_seguridad.sh')
        print("Haciendo copia de seguridad")
        print (str(res))
    except:
        print("Error al hacer la copia de seguridad")
    #se reinicia el archivo de copia de seguridad
    iniciar_archivo_copia_seguridad()
def apuntar_encendidos_de_bomba(tiempo_desde_ultimo_encendido):
    #aqui se guardan los encendidos de la bomba en el archivo /home/pi/Caldera/datos/encendidos_bomba.txt
    hora = hora_actual()
    tiempo_en_minutos = tiempo_desde_ultimo_encendido / 60
    if (os.path.exists("/home/pi/Caldera/datos/encendidos_bomba.txt")):  #si el arvivo existe
         f = open("/home/pi/Caldera/datos/encendidos_bomba.txt","a")    
         f.write(hora + "   " + str(tiempo_en_minutos) + '\n')
         f.close()
    else:                                                      #si no existe
        os.system('touch /home/pi/Caldera/datos/encendidos_bomba.txt')  #se crea
        f = open("/home/pi/Caldera/datos/encendidos_bomba.txt","a")     
        f.write(hora + "   " + str(tiempo_en_minutos) + '\n')
        f.close()
    return 0
def apuntar_apagados_de_bomba(tiempo_desde_ultimo_apagado):
    #aqui se guardan los encendidos de la bomba en el archivo /home/pi/Caldera/datos/encendidos_bomba.txt
    hora = hora_actual()
    tiempo_en_minutos = tiempo_desde_ultimo_apagado / 60
    if (os.path.exists("/home/pi/Caldera/datos/apagados_bomba.txt")):  #si el arvivo existe
         f = open("/home/pi/Caldera/datos/apagados_bomba.txt","a")    
         f.write(hora + "   " + str(tiempo_en_minutos) + '\n')
         f.close()
    else:                                                      #si no existe
        os.system('touch /home/pi/Caldera/datos/apagados_bomba.txt')  #se crea
        f = open("/home/pi/Caldera/datos/apagados_bomba.txt","a")     
        f.write(hora + "   " + str(tiempo_en_minutos) + '\n')
        f.close()
    return 0
def apuntar_tiempo_quemando(tiempo_de_quemado):
    #aqui se guardan el tiempo de quemado de la caldera
    hora = hora_actual()
    tiempo_en_minutos = tiempo_de_quemado / 60
    if (os.path.exists("/home/pi/Caldera/datos/tiempo_quemando.txt")):  #si el arvivo existe
         f = open("/home/pi/Caldera/datos/tiempo_quemando.txt","a")    
         #f.write(hora + "   " + str(tiempo_en_minutos) + '\n')
         f.write(str(tiempo_en_minutos) + "   " + hora + '\n')
         f.close()
    else:                                                      #si no existe
        os.system('touch /home/pi/Caldera/datos/tiempo_quemando.txt')  #se crea
        f = open("/home/pi/Caldera/datos/tiempo_quemando.txt","a")     
        #f.write(hora + "   " + str(tiempo_en_minutos) + '\n')
        f.write(str(tiempo_en_minutos) + "   " + hora + '\n')
        f.close()
    return 0
def comprueba_encendido_bomba_forzoso():
    #aqui se comprueba si la bomba debe estar encendida forzosamente
    #los estados son forzoso_on forzoso_off
    estado = "forzoso_off"
    try:
        if (os.path.exists("/home/pi/Caldera/datos/encendido_forzoso.txt")):
            f = open("/home/pi/Caldera/datos/encendido_forzoso.txt","r")
            estado = str(f.readline())
            f.close()
            return estado
        else :
            os.system('touch /home/pi/Caldera/datos/encendido_forzoso.txt')
            f = open("/home/pi/Caldera/datos/encendido_forzoso.txt","a")
            f.write("forzoso_off")
            f.close()
            return estado
    except:
        return estado
def apagar_encendido_bomba_forzoso():
    #esta funcion es llamada cuando encendido_bomba_forzoso esta on y
    #ademas la temperatura de la casa ha superado a la temperatura seleccionada
    #de la casa para cortar el encendido forzoso
    try:
        if (os.path.exists("/home/pi/Caldera/datos/encendido_forzoso.txt")):
            f = open("/home/pi/Caldera/datos/encendido_forzoso.txt","w")
            f.write("forzoso_off")
            f.close()
            print("Estado forzoso_off temperatura de consigna ok")
        else:
            print("No existe el archivo de encendido forzoso, no se hace nada")
    except:
        print ("no se puece acceder a el archivo /home/pi/Caldera/datos/encendido_forzoso.txt")
def encender_encendido_bomba_forzoso():
    #esta funcion es llamado cuando hay que encender encendido forzoso a on
    try:
        if (os.path.exists("/home/pi/Caldera/datos/encendido_forzoso.txt")):
            f = open("/home/pi/Caldera/datos/encendido_forzoso.txt","w")
            f.write("forzoso_on")
            f.close()
            print ("Estado_forzoso_on")
        else:
            print("No existe el archivo de encendido forzoso, no se hace nada")
    except:
        print("No se puede acceder a el archivo /home/pi/Caldera/datos/encendido_forzoso.txt")

#******************************************************************#
#******************************************************************#
#***************************** MAIN *******************************#
arduino = serial.Serial('/dev/ttyACM0',baudrate=9600,timeout = 3)

iniciar_archivo_copia_seguridad()
time.sleep(2) #la bomba se encendio al princio y hay que esperar un poco
              #para pararla
parar_la_bomba()
apagar_encendido_bomba_forzoso()# por si la ultima vez se qued en on
setear_estado_script_a_true() 

temperatura_seteo_caldera = 60 #esta es la temperatura a la que esta seteada la caldera

temperatura_corte_rele = temperatura_seteo_caldera # al principio el rele corta a la temperatura de seteo
temperatura_minima_rele = temperatura_seteo_caldera -6 # la temperatura de corte cuando entra en forzoso_on

temperatura_quemado_caldera = temperatura_seteo_caldera - 3 #temperatura a la que empieza a quemar la caldera

temperatura_maxima_caldera = 70 #temperatura maxima que no debe sobrepasar la caldera, sera usada para encender la bomba si esta es sobrepasada

encendido = comprobar_estado_script()
temp_casa = comprobar_temperatura_casa()
temp_seleccionada_casa = float(comprobar_temperatura_seleccionada_casa())
ultimo_encendido = time.time() #se actualiza cada vez que la bomba se enciende
ultimo_apagado = time.time() #se actualiza cada vez que la bomba se apaga
tiempo_desde_ultimo_encendido = 0#el tiempo que tarda desde un encendido a otro
tiempo_desde_ultimo_apagado = 0#el tiempo que tarda desde el ultimo apagado
temperatura_progresion_1 = 0 #para calcular si la temperatura esta subiendo o baj
estado_combustion = "no_quemando" #iniciar la variable para que no de problemas
tiempo_desde_temperatura_conseguida1 = time.time() #el tiempo que hace desde que la temperatura de la casa supera la de consigna
tiempo_desde_temperatura_conseguida2 = time.time()
tiempo_maximo_sin_conseguir_temperatura_de_consigna = 3600 # en segundos (1 hora)


#hum_casa = comprobar_humedad_casa() #no necesario

#*****************************************************************
                                                                 
tiempo_entre_comprobaciones_casa = 150
tiempo_parada_bucle = 0.5
tiempo_escribir_en_archivo = 30 # tiempo que pasa hasta que se escribe archivo datos.txt para grafica
t_progresion = 8 #tiempo que tiene que pasar para comprobar el progreso de la temp
tiempo_para_comprobar_temperatura_seleccionada_casa = 30 # tiempo que tiene que pasar para comprobar la temperatura seleccionada en la casa
progresion = "mantenida" #la progresion de la temperatura (mantenida,ascenso,descenso)

tiempo_para_archivo = time.time() #tiempo que pasa para escribir en el archivo
tiempo1 = time.time()#para las comprobaciones de temperatura en la casa                                         
tiempo_progresion_temp_1 = time.time() #para saber si la temp asciende o desciende
tiempo_temp_seleccionada1 = time.time()#tiempo que pasa para comprobar la temperatura seleccionada

entrado = False # para controlar tiempo de quemado

while (encendido == "True"):
    tiempo_para_archivo2 = time.time()
    tiempo2 = time.time()
    tiempo_progresion_temp_2 = time.time()
    tiempo_temp_seleccionada2 = time.time()
    tiempo_desde_temperatura_conseguida2 = time.time()
    
    if ((tiempo2 - tiempo1)>tiempo_entre_comprobaciones_casa):   
        tiempo1 = time.time()
        print "*************************"
        temp_casa = comprobar_temperatura_casa()
        print "Temperatura casa = " + str(temp_casa)
        #hum_casa = comprobar_humedad_casa()                      

    encendido = comprobar_estado_script()
    
    temp_caldera = temperatura_sensor_caldera()
    #temp_ida = temperatura_sensor_ida()
    #temp_retorno = temperatura_sensor_retorno()

    #comprobar temperatura seleccionada casa (cada 30 segundos)
    if ((tiempo_temp_seleccionada2 - tiempo_temp_seleccionada1)>tiempo_para_comprobar_temperatura_seleccionada_casa):
        temp_seleccionada_casa = float(comprobar_temperatura_seleccionada_casa())
        tiempo_temp_seleccionada1 = time.time()
        
    #comprobar el estado bomba
    estado_bomba = comprobar_estado_bomba()

    #condiciones de si debe encenderse la bomba 
    if (temp_casa < temp_seleccionada_casa):
        if (temp_caldera > temperatura_corte_rele):
            if (estado_bomba == "apagada"):
                enciende_bomba()
                tiempo_desde_ultimo_encendido = time.time() - ultimo_encendido
                ultimo_encendido = time.time()
                apuntar_encendidos_de_bomba(tiempo_desde_ultimo_encendido)

    #condiciones de si debe apagarse la bomba
    if (temp_casa > temp_seleccionada_casa):
        tiempo_desde_temperatura_conseguida1 = time.time()
        if (estado_bomba == "encendida"):
            if (temp_caldera > temperatura_maxima_caldera):
                print ("No se puede parar la bomba por altas temperaturas de la caldera")
            else:
                parar_la_bomba()
                tiempo_desde_ultimo_apagado = time.time() - ultimo_apagado
                ultimo_apagado = time.time()
                apuntar_apagados_de_bomba(tiempo_desde_ultimo_apagado)
        elif ((estado_bomba == "apagada") and (temp_caldera > temperatura_maxima_caldera)):
            enciende_bomba()
            tiempo_desde_ultimo_encendido = time.time() - ultimo_encendido
            ultimo_encendido = time.time()
            apuntar_encendidos_de_bomba(tiempo_desde_ultimo_encendido)
    if (temp_caldera < temperatura_corte_rele):
        if (estado_bomba == "encendida"):
            parar_la_bomba()
            tiempo_desde_ultimo_apagado = time.time() - ultimo_apagado
            ultimo_apagado = time.time()
            apuntar_apagados_de_bomba(tiempo_desde_ultimo_apagado)

    #rellenar datos para graficas        
    if (tiempo_para_archivo2 - tiempo_para_archivo > tiempo_escribir_en_archivo):
        tiempo_para_archivo = time.time()#se reinicia el tiempo
        guardar_datos_para_grafica(temp_casa,temp_seleccionada_casa,temp_caldera,estado_bomba)
        guardar_datos_base_mysql(temp_casa,temp_seleccionada_casa,temp_caldera,estado_bomba)

    #--Comprobar si la temperatura esta en ascenso o descenso--#
    if (tiempo_progresion_temp_2 - tiempo_progresion_temp_1 > t_progresion):
        tiempo_progresion_temp_1 = time.time()# se reinicia el contador
        if (temp_caldera > temperatura_progresion_1):
            progresion = "ascenso"
        if (temp_caldera < temperatura_progresion_1):
            progresion = "descenso"
        if (temp_caldera == temperatura_progresion_1):
            progresion = progresion

        print str(temp_caldera) + " --> " + progresion + " " + str(temp_caldera - temperatura_progresion_1)
        temperatura_progresion_1 = temp_caldera
        
    #--Estado de combustion ("quemando" ó "no_quemando")--#
    if (temp_caldera <= temperatura_quemado_caldera):
        estado_combustion = "quemando"
    elif (temp_caldera >= temperatura_seteo_caldera):
        estado_combustion = "no_quemando"
    elif ((temp_caldera > temperatura_quemado_caldera) & (temp_caldera < temperatura_seteo_caldera)):
        if (progresion == "ascenso"):
            estado_combustion = "quemando"
        if (progresion == "descenso"):
            estado_combustion = "no_quemando"
    #print "estado combustion =  " + str(estado_combustion)

    #--Tiempo que esta la llama encendida--#
    if (estado_combustion == "quemando") & (not entrado):
        tiempo_inicio_quemado = time.time()
        entrado = True
        print "ha empezado a quemar"
    if (estado_combustion == "no_quemando") & (entrado):
        tiempo_quemado = time.time() - tiempo_inicio_quemado
        if (tiempo_quemado < 60):
            print "nada porque ha quemado menos de 10 seg"
        if (tiempo_quemado > 600):
            print "No se apunta porque ha quemado mas de 10 minutos"
        if (tiempo_quemado >=60) and (tiempo_quemado <=720):
            apuntar_tiempo_quemando(tiempo_quemado)
        entrado = False
        print "Ha terminado de quemar"
        print "El tiempo de quemado ha sido de:" + str(tiempo_quemado/60)

    #--Comprobar si esta puesto el encendido forzoso
    encendido_bomba_forzoso = comprueba_encendido_bomba_forzoso()
    #print encendido_bomba_forzoso

    #--si la casa llega a la temperatura de consigna se apaga estado_forzoso
    if ((encendido_bomba_forzoso == "forzoso_on") and (temp_casa > temp_seleccionada_casa)):
        apagar_encendido_bomba_forzoso()
        temperatura_corte_rele = temperatura_seteo_caldera # la temperatura de corte del rele vuelve a ser la misma 
        
        
    #--Comprobar si hay que activar el modo forzoso-on por tiempo sin llegar a la temperatura
    tiempo_sin_conseguir_temperatura_de_consigna = tiempo_desde_temperatura_conseguida2 - tiempo_desde_temperatura_conseguida1
    if (tiempo_sin_conseguir_temperatura_de_consigna > tiempo_maximo_sin_conseguir_temperatura_de_consigna):
        print "Encendido forzoso on por demasiado tiempo sin consigna"
        if (encendido_bomba_forzoso == "forzoso_off"):
            temperatura_corte_rele = temperatura_minima_rele
            encender_encendido_bomba_forzoso()

    #comprobar si hay que hacer copia de seguridad
    comprobar_si_copia_de_seguridad()
    
    time.sleep(tiempo_parada_bucle)

#de aqui hacia abajo queda fuera del while si se para la ejecucion por el script
print "parando ejecucion por script"
#os.system('echo 21 > /sys/class/gpio/unexport')
parar_la_bomba()#si se para el script por el usuario hay que parar la bomba

#aqui entra si por medio hay algun problema
#parar_la_bomba()

#datos que sirven para servidor
#    temp_casa(float)
#    temp_seleccionada_casa(float)
#    temp_caldera(float)
#    estado_bomba(encendida-apagada convertir a float)
