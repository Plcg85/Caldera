Hola!!. Este proyecto fue creado a medida para controlar la calefacción de casa por medio de raspberry pi, arduino y un relé que acciona la bomba del agua caliente de los radiadores (Ver esquema.jpg). Tiene 2 partes.
La primera parte es el programa principal que se ejecuta en una raspberry pi 3b. Este programa hace varias cosas que enumero a continuación:
      1. Se comunica con otra raspberry pi  que está en el salón principal de la casa a traves de ssh-paramiko para saber la temperatura del salón cada poco tiempo.
      2. Con un sensor de temperatura ds18b20 sumergido en agua caliente de la caldera conoce la temperatura de ésta y saber si está a la temperatura óptima.
      3. Cuando tiene los datos de temperatura necesarios comprueba la temperatura que el usuario quiere en el salón y dependiendo de varios factores activa el relé que acciona la bomba para que el agua caliente fluya a los radiadores.
      4. Cada cierto tiempo los datos se guardan en una base de datos local para ser utilizados por la segunda parte del proyecto.
La segunda parte del proyecto es una web alojada en la raspberry pi accesible a traves de un servidor apache (Accesible desde cualquier disposito y lugar con internet)(Ver web.jpg). Desde esta web se puede subir y bajar la temperatura deseada 
de la casa y se puede ver un gráfico histórico de 24 hora en el que tenemos la siguiente información:
      1. Temperatura actual de la casa y la media de las últimas 24 horas.
      2. La temperatura que tenemos seleccionada (temperatura deseada de la casa) y media de las últimas 24 horas.
      3. La temperatura actual de la caldera y la media de las últimas 24 horas.
      4. El estado actual del relé que controla la bomba del agua.
      5. Un gráfico con todo lo anterior en el que se puede visualizar rápidamente la información de las últimas 24 horas y seleccionar un momento exacto del día para ver la información de ese instante.
El programa dispone de protección contra sobretemperaturas de la caldera, es decir, cuando la caldera está mas alta de 80 grados ignora la temperatura deseada en casa para proteger la caldera.![web](https://github.com/Plcg85/Caldera/assets/168082799/fb68eeab-d5cd-4543-8456-3f4e16c60f4d)

      
