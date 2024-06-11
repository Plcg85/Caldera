const int rele = 13;
int iniciado = 0;

void setup(){
  Serial.begin(9600);
  pinMode(rele,OUTPUT);
}

void loop(){
  if (iniciado == 0)
    {
      digitalWrite(rele,HIGH);
    }
  
  //digitalWrite(rele,HIGH);
  //delay(500);
  //digitalWrite(rele,HIGH);
  //delay(5000);
  
  if(Serial.available()>0)
    
    {
      int dato = Serial.read();
      //Serial.print(dato);
      if (dato == 49)
        {
          iniciado = 1;
          //Serial.println("Nivel alto recibido");
          digitalWrite(rele,LOW);
        }
      else if (dato == 48)
        {
          //Serial.println("Nivel bajo recibido");
          digitalWrite(rele,HIGH);
        }
    }
}
