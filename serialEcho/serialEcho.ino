
const int BUFFER_SIZE = 30;
char sBuffer[BUFFER_SIZE];

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(57600);

}

void loop()
{

  String echo = "";

  
  if (Serial.available() > 0)
  {
    digitalWrite(LED_BUILTIN, HIGH);
    
    int packetEnd = Serial.readBytesUntil('E', sBuffer, BUFFER_SIZE);
    
    if (packetEnd == BUFFER_SIZE)
    {
      Serial.println("no end of packet char! discarding");
    }

    else
    {
      for (int i = 0; i < packetEnd; i++)
        {
          echo.concat(sBuffer[i]);
        }
      
      Serial.print(echo);
    }
    
    
   
  }
  
 

}

void clearBuffer()
{
 
  for (int i = 0; i < BUFFER_SIZE; i++)
  {
    sBuffer[i] = 0;
  }

  
}

