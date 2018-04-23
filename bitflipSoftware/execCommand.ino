//Function to process messages from the serial port.
//input -> input message from serial port (excluding closing ';')
//Uses furst character in String as command
//All further additions are seen as 'values' (optional additional arguments)
void execCommand( String input )
{
  //List of possible command.
  String command = input.substring( 0, 1 );
  int value = (input.substring( 1, input.length() )).toInt();


  //Ping (return number from 'value')
  else if( command == "p" ){
    //Ping
    //Print 'value' to serial
    Serial.println( value );
  }

  
  //Move flipPointer to desired port (input in HEX with the 0x prefix) 
  //value -> target memory location
  else if( command == "m" ){
    // Assign hex address to pointer
    flipPointer = (unsigned int*)value; // Check if this works! Otherwise, use "reinterpret_cast<int*>"
    // Print address that the pointer contains to verify
    unsigned int address = (unsigned int)flipPointer;
    Serial.println(address);
   

  //Flip a bit at the current flipPointer location.
  //value -> bit number to flip: 0 is least significant
  else if( command == "f" ){
    flipBit( value );
  }


  //Set value at current flipPointer locationl.
  else if( command == "s" ){
    *flipPointer = value;
  }


  //Display test string
  else if( command == "t" ){
    Serial.println( testString );
  }


  //Output current memory value at flipPointer, and location
  else if( command == "o" ){
    Serial.print( "Val: " );
    Serial.print( *flipPointer );
    Serial.print( " at: " );
    Serial.print( (int)flipPointer);
    Serial.println();
  }


  //Count loop number through serial ouput
  //On for argument 1
  //Off for argument 0
  else if ( command == "c" ){
    if( value == 1 ){
      countOut = 1;
    }
    else if( value == 0 ){
      countOut = 0;
    }
  }

}
