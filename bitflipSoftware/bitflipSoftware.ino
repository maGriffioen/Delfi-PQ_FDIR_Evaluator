//Serial communication variables.
int incomingByte = 0;
char incomingChar;
String incomingStr = "";

//Loop-counter settings
int counter = 0;        
int countOut = 1;

//Bitflip dummy variable (unused) and pointer to it.
unsigned int pointerInitializationVariable = 0;
unsigned int *flipPointer = &pointerInitializationVariable;
//String for data verification / detecting corruption
String testString = "Hello World";

void setup() 
{
  //Initiate Serial connection and wait untill it is established.
  //Ensure that only the FDIR-verification software uses the serial port
  Serial.begin(115200);
  while (!Serial) {
    ;
  }

  //Verify that the system booted is complete.
  Serial.println("Boot sequence done");
}

//Main loop function of the flightcontroller.
//The content present in the examplesoftware need to be included to the flight software
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






