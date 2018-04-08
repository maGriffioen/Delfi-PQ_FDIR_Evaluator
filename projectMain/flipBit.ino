//Function for flipping a bit at the location of the input pointer.
//*pointer -> Pointer to the address to be flipped.
//flipLocation -> Which bit to be flipped at the pointer.
//return -> None

void flipBit( unsigned int flipLocation )
{
  //Ensure the pointer is not pointing to itself, do not execute bitflip if it is [else].
  //  (int)pointer     --Pointer content
  //  (int)&pointer    --Pointer address
  
  if( *flipPointer != (int)flipPointer)
  {
      unsigned int flipmask = pow(2, flipLocation);
      *flipPointer = *flipPointer ^ flipmask;
  }
  else
  {
      //No bitflip when pointing points to itself.
      Serial.println( "Bad pointer" ); 
  }
}
