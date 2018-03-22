#include "Timer.h"

Timer t;

//Serial communication variables.
int incomingByte = 0;
char incomingChar;
String incomingStr = "";

//LED settings and parameters.
int ledPin = 78;
int ledBlink = 0;

void setup() {
  //Set Red LED1 pin.
  pinMode(ledPin, OUTPUT);

  //Initiate Serial connection and wait untill it is established.
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  //Serial.println("Hello World");
  //delay(1000);
  
}

void loop() {
        t.update();
        
        // send data only when you receive data:
        if (Serial.available() > 0) {
                // read the incoming byte and character
                incomingByte = Serial.read();
                incomingChar = incomingByte;

                //If ; (0x3B) is sent, terminate the message, execute incoming command and print it.
                if (incomingByte == 0x3B){
                  Serial.println(incomingStr);
                  execCommand(incomingStr);

                  //Reset incoming string.
                  incomingStr = "";
                }
                
                else {
                  //Add incoming character to the incoming string
                  incomingStr += incomingChar;
                  //Serial.print("I received: ");
                  //Serial.println(incomingByte, HEX);
                }
        }

        
}

void execCommand(String input)
{
  //List of possible command.
  
  if (input == "LED ON"){
    t.stop(ledBlink);
    digitalWrite(ledPin, HIGH);
  }
  else if  (input == "LED OFF"){
    t.stop(ledBlink);
    digitalWrite(ledPin, LOW);
  }
  else if (input.substring(0, 9) == "LED BLINK"){
    t.stop(ledBlink);
    ledBlink = t.oscillate(ledPin, input.substring(10, 14).toInt(), LOW);
  }
}

