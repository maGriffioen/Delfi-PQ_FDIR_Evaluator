int testVar = 12;
int *testPointer = &testVar;
String testString = "Hello World";
String *stringPointer = &testString;

void setup() {
  //Initiate Serial connection and wait untill it is established.
  Serial.begin(9600);
  while (!Serial) {
    ;
  }

  //Verify that the boot is complete.
  Serial.println("Boot sequence done");


  //BitFlip on testVar
  Serial.println( (int)testPointer );
  Serial.println( *testPointer );
  flipBit( testPointer, 2 );
  Serial.println( *testPointer );

  Serial.println( "" );
  Serial.println( "Before bitflip" );
  Serial.println( testString );
  Serial.println( "" );
  //Move testPointer to stringPoitner to influence the testString.
  for( testPointer; (int)testPointer < (int)stringPointer; testPointer++)
  {
    ;
  }
  //Serial.println( (int)testPointer );
  //Serial.println( *testPointer );
  flipBit( testPointer, 2 );
  //Serial.println( *testPointer );
  Serial.println( "" );
  Serial.println( "After bitflip" );
  Serial.println( testString );

  
}

void loop() {
  // put your main code here, to run repeatedly: 
  ;
}
