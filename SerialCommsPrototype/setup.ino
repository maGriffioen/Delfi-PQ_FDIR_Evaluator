// Setup function after reset of controller.
void setup() 
{
  //Set Red LED1 pin to ouput mode, and enable.
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  //Initiate Serial connection and wait untill it is established.
  Serial.begin(9600);
  while (!Serial) {
    ;
  }

  //Verify that the boot is complete.
  Serial.println("Boot sequence done");
  //delay(1000);
}
