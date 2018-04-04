#include "Timer.h"

Timer t;

//Serial communication variables.
int incomingByte = 0;
char incomingChar;
String incomingStr = "";

//LED settings and parameters.
int ledPin = 78; 
int ledBlink = 0;    
int counter = 0;        
int countOut = 0;



void loop() {
        delay(50);
        t.update();
        counter ++;
        if( countOut == 1 ){
            Serial.print("LoopCount: ");
            Serial.println(counter);
        }
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






