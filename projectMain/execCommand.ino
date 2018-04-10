//Function to process messages from the serial port.
//input -> input message from serial port (excluding closing ';')
//Uses furst character in String as command
//All further additions are seen as 'values' (optional additional arguments)
void execCommand( String input )
{
  //List of possible command.
  String command = input.substring( 0, 1 );
  int value = (input.substring( 1, input.length() )).toInt();

  /*
  //Turn LED on
  if( command == "L" ){
    t.stop(ledBlink);
    digitalWrite(ledPin, HIGH);
  }

  //Turn LED off
  else if( command == "l" ){
    t.stop(ledBlink);
    digitalWrite(ledPin, LOW);
  }


  //Ping (return number from 'value')
  else*/ if( command == "p" ){
    //Ping
    //Print 'value' to serial
    Serial.println( value );
  }

  //TODO: current bug - only bits 0-31 work, the 32nd bit cannot be flipped
  //Move flipPointer to desired port (input in DEC) 
  //value -> target memory location
  else if( command == "m" ){
    //move pointer
    if( (int)flipPointer < value ){ //Move forward
      for( *flipPointer; (int)flipPointer < value; flipPointer++ ){
        ;
      }
    }
    else if( (int)flipPointer > value ){ // Move backwards
      for( *flipPointer; (int)flipPointer > value; flipPointer-- ){
        ;
      }
    }
    else {  // Do nothing if no pointer is already at the correct position
      ;
    }
  }

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

  //Output current memory value at flipPointer
  else if( command == "o" ){
    Serial.print( "Val: " );
    Serial.print( *flipPointer );
    Serial.print( " at: " );
    Serial.println( (int)flipPointer );
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

  //Reset
  //Currently not operational
  else if ( command == "R" ){
    //Reset controller?? -Is this even possible from the software? -
    Serial.println( "ERROR" );
  }
}
