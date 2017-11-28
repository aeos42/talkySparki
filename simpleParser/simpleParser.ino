#include <Sparki.h>
//#define START 0
//#define MOVE 1
//int state = START;

int interval = 1000;
int cm = 0;
int loopCount = 0;
float maxspeed=0.0285;    // [m/s] speed of the robot that you measured
float alength=0.0851;     // [m] axle length  
float phildotr=0, phirdotr=0; // wheel speeds that you sent to the motors
float Xi=0, Yi=0, Thetai=0;
float Xrdot, Thetardot;

void setup() {
  // put your setup code here, to run once:
  sparki.servo(SERVO_CENTER);
  Serial1.begin(9600);
}

void updateSensorCM(int angle) {
  
  String XiS = (String)" "+Xi;
  String YiS = (String) XiS+" "+Yi;
  String ThetaiS = (String) YiS+" "+Thetai;
  String angleS = (String) ThetaiS+" "+angle;
  String pingS = (String) angleS+" "+sparki.ping()+" ";
  String info = "S"+pingS+"E";
  sparki.clearLCD();
  sparki.print(info);
  Serial1.println(info);
  sparki.updateLCD();
  delay(100);
}

int scanDir() {
  // those angle ranges are the best for sparki spin his head, i.e. 180 degree
  for (int angle = -85; angle < 81; angle = angle + 15){
    sparki.servo(angle);
    updateSensorCM(angle);
    //updateSensorRead();
    if (angle == 80){
      sparki.servo(SERVO_CENTER);
    }
  }
}

void loop() {
  sparki.moveForward(10);
  Xrdot=phildotr/2.0+phirdotr/2.0;
  Thetardot=phirdotr/alength-phildotr/alength;
  Xi=Xi+cos(Thetai)*Xrdot*0.1;
  Yi=(Yi+sin(Thetai)*Xrdot*0.1)+10;
  Thetai=Thetai+Thetardot*0.1;
  scanDir();
  delay(interval);
}
