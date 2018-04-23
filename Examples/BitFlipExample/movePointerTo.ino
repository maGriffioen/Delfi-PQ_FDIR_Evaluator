

int *movePointerTo(int *pointer, int target )
{
  if( (int)pointer < target )
  {
    for( *pointer; (int)pointer < target; pointer++)
    {
      ;
    }
  }
  else if( (int)pointer > target)
  {
    for( *pointer; (int)pointer > target; pointer--)
    {
      ;
    }
  }
  else
  {
    ;
  }
  return pointer;
}

