#include <Servo.h>
#include <SoftwareSerial.h>

Servo hand;
Servo twist;
Servo shoulder;
Servo elbow;
Servo wrist;
Servo grip;

String Data = "";
int g, h, w, e, s, t;

void setup() {
  
  Serial.begin(9600);
  grip.attach(8);
  hand.attach(9);
  wrist.attach(10);
  elbow.attach(13);
  shoulder.attach(12);
  twist.attach(11);
  default_pos();
}

void loop() {

  while (Serial.available())
  {
    char character = Serial.read(); 
    Data.concat(character); 
    
    if (character == 'h')
    {
      h = Data.toInt();
      hand.write(h);
      Data = "";
    }
    
    else if (character == 't')
    {
      t = Data.toInt();
      twist.write(t);
      Data = "";

    }

    else if (character == 's')
    {
      s = Data.toInt();
      shoulder.write(s);
      Data = "";
    }
    
    else if (character == 'e')
    {
      e = Data.toInt();
      elbow.write(e);
      Data = "";

    }

    else if (character == 'w')
    {
      w = Data.toInt();
      wrist.write(w);
      Data = "";
    }

    else if (character == 'g')
    {
      g = Data.toInt();
      grip.write(g);
      Data = "";
    }
    
  }
}

void default_pos() {
  //origin position
  
  grip.write(90); 
  wrist.write(80); 
  hand.write(140); 
  elbow.write(135); 
  shoulder.write(120); 
  twist.write(0);
}



