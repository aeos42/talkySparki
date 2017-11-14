#include <sparki.h>  // include the sparki library
int loopCount = 0;

void setup()
{
  Serial1.begin(9600);
}

void loop()
{
  
    Serial1.print(loopCount);
    
    
    loopCount++;

    delay(1000);

}
