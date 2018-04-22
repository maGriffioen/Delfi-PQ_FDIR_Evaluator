//Serial communication variables.
int incomingByte = 0;
char incomingChar;
String incomingStr = "";

//LED settings and parameters.
//int ledPin = 78;    
int counter = 0;        
int countOut = 1;

unsigned int pointerInitializationVariable = 0;
unsigned int *flipPointer = &pointerInitializationVariable;
String testString = "Hello World";

void setup() 
{
  //Set Red LED1 pin to ouput mode, and enable.
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  //Initiate Serial connection and wait untill it is established.
  Serial.begin(115200);
  while (!Serial) {
    ;
  }

  //Verify that the boot is complete.
  Serial.println("Boot sequence done");
  //Serial.println( (int)&testString );
}

void loop() {
        delay(100);
        counter ++;
        if( countOut == 1 ){
            Serial.print("LoopCount: ");
            Serial.println(counter);
        }
        
        // send data only when you receive data:
        if (Serial.available() > 0) {
                bool reading = true;
                while ( Serial.available() > 0 && reading )
                {
                    // read the incoming byte and character
                    incomingByte = Serial.read();
                    incomingChar = incomingByte;
    
                    //If ; (0x3B) is sent, terminate the message, execute incoming command and print it.
                    if (incomingByte == 0x3B){
                      reading = false;
                      execCommand(incomingStr);
                      Serial.println(incomingStr); 
    
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

        
}






