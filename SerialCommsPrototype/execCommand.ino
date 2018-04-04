//Function to process messages from the serial port.
//input -> input message from serial port (excluding closing ';')
//Uses furst character in String as command
//All further additions are seen as 'values' (optional additional arguments)
void execCommand( String input )
{
  //List of possible command.
  String command = input.substring( 0, 1 );
  int value = (input.substring( 1, input.length() )).toInt();

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


  //Blink LED (input ->3 half period)
  else if ( command == "B" ){
    t.stop(ledBlink);
    ledBlink = t.oscillate(ledPin, value, LOW);
  }

  //Ping (return number from 'value')
  else if( command == "p" ){
    //Ping
    //Print 'value' to serial
    Serial.println( outputValue );
  }

  //Count loop number through serial ouput
  //On for argument 1
  //Off for argument 0
  else if ( command == "C" ){
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
