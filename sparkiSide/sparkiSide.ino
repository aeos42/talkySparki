#include <sparki.h>
//#define START 0
//#define MOVE 1
//int state = START;

int interval = 1000;
int cm = 0;
int loopCount = 0;

void setup() {
  // put your setup code here, to run once:
  sparki.servo(SERVO_CENTER);
  Serial1.begin(9600);
}

void updateSensorCM() {
  sparki.clearLCD();
  sparki.print(sparki.ping());
  sparki.println(" cm");

  Serial1.print(sparki.ping());
  Serial1.println(" cm");
  sparki.updateLCD();
  delay(100);
}

int scanDir() {
  // those angle ranges are the best for sparki spin his head, i.e. 180 degree
  for (int angle = -85; angle < 81; angle = angle + 15){
    sparki.servo(angle);
    updateSensorCM();
    //updateSensorRead();
    if (angle == 80){
      sparki.servo(SERVO_CENTER);
    }
  }
}

void loop() {
  sparki.moveForward(10);
  scanDir();
  delay(interval);
}
