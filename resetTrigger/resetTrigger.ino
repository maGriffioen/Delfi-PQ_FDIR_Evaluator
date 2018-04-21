//Serial communication variables.
int incomingByte = 0;
char incomingChar;
String incomingStr = "";

//Pin parameters
int resetTriggerPin = 19; //HIGH -> No reset, LOW -> Reset triggered when set back to HIGH
int ledPin = 78;



void setup() {
  //Set resetTriggerPin to output mode and set it high -> prevents reset. 
  pinMode(resetTriggerPin, OUTPUT);
  digitalWrite(resetTriggerPin, HIGH);
  
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
  
  Serial.println("Boot sequence done (reset trigger)");
}

void loop() {
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
                }
        }
}
