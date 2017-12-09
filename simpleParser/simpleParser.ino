#include <Sparki.h>
#include <stdio.h>
#include <string.h>

float pi = 3.1415926535897932384626;
int interval = 1000;
int cm = 0;
int loopCount = 0;
float maxspeed=0.0285;    // [m/s] speed of the robot that you measured
float alength=0.0851;     // [m] axle length  
float phildotr=0, phirdotr=0; // wheel speeds that you sent to the motors
float Xi=0, Yi=0, Thetai=0;
float Xrdot, Thetardot;

float rX; //robot coords
float rY;
float rT;
bool eC = false;
float gX = 0.0;// = 0.2159;//goal coords
float gY = 0.0;// = 0.2794;
float gT= 0.0;// = pi/2;

float a = 0.05;
float b = 0.9;
float c = 0.01;

float d = 0.0851; //axel_length_m = 0.0851
float r = 0.025;  //wheel_diameter_m = 0.05
float maxWheelSpeed = 0.0285;

enum robotStates {
  SA,
  MTG,
  WFI,
  SendIdle
} state;

void setup() {
  // put your setup code here, to run once:
  sparki.servo(SERVO_CENTER);
  Serial1.begin(9600);
  state = SA;
  rX = 0.3;
  rY = 0.4;
  rT = pi / 2;
}

void moveToGoal() {
  
  sparki.clearLCD();
  float t1 = millis();
  //figure out how to drive
  
  float dX = (gX - rX);
  float dY = (gY - rY);
  
  sparki.print(dX);
  sparki.print(" ");
  
  sparki.print(dY);
  sparki.print(" ");
  
  float rho = sqrt(pow(dX, 2) + pow(dY, 2)); //distance to point
  sparki.println(rho);

  float at2 = atan2(dY,dX);//returns bearing

  float aFromX = pi/2 - at2;
   
  float dT = aFromX - rT; //how far we have to turn
  sparki.print("dT ");
  sparki.println(dT*180/pi);
  
  float nu = gT - rT;
  //sparki.println(nu);
  
  float x_rp = a*rho; //our desired movement speed
  float theta_rp = b*dT + c*nu; //our desired rotation speed
  
  //sparki.println("speeds:");
  //sparki.println(2*x_rp);
  //sparki.println(d*theta_rp);
  
  float leftWheelSpeed = ((2 * x_rp) - (theta_rp * d)) / (2*r); //max 0.0285
  float rightWheelSpeed = ((2 * x_rp) + (theta_rp * d)) / (2*r); //max 0.0285
  
  //sparki.println((leftWheelSpeed));
  //sparki.println((rightWheelSpeed));
  
  float scaleFactor = max(abs(leftWheelSpeed), abs(rightWheelSpeed));
  
  leftWheelSpeed = leftWheelSpeed * (0.0285 / scaleFactor);
  rightWheelSpeed = rightWheelSpeed * (0.0285 / scaleFactor);
  
  sparki.println((leftWheelSpeed / maxWheelSpeed) * 100);
  sparki.println((rightWheelSpeed / maxWheelSpeed) * 100);
  
  //rotate while moving towards the point
  //eventually, get on the correct trajectory. keep traveling forward,
  //eventually get to the objective point. then rotate to your desired
  //orientation

  if(leftWheelSpeed > 0)
    {
    sparki.motorRotate(MOTOR_LEFT, DIR_CCW, (leftWheelSpeed / maxWheelSpeed) * 100); // rotate(which motor, which direction, percent)  
  }
  else{
    sparki.motorRotate(MOTOR_LEFT, DIR_CW, abs((leftWheelSpeed / maxWheelSpeed) * 100)); // rotate(which motor, which direction, percent)  
  
    }
  if(rightWheelSpeed > 0)
    {
     sparki.motorRotate(MOTOR_RIGHT, DIR_CW, (rightWheelSpeed / maxWheelSpeed) * 100);  
    }
  else{
    sparki.motorRotate(MOTOR_RIGHT, DIR_CCW, abs((rightWheelSpeed / maxWheelSpeed) * 100));  
  }
  
  //UPDATE MY POS
//   sparki.motorRotate(MOTOR_LEFT, DIR_CCW, 100); // rotate(which motor, which direction, percent)  
//   sparki.motorRotate(MOTOR_RIGHT, DIR_CW, 100); // rotate(which motor, which direction, percent)  

  delay(100);
  
  float t2 = millis();
  float totalTime = (t2-t1) / 1000;
  
  float Xdot = (leftWheelSpeed / 2.0) + (rightWheelSpeed / 2.0);
  float Thetadot = (rightWheelSpeed / d) - (leftWheelSpeed / d);
  
  rX = rX + sin(rT) * Xdot * totalTime;
  rY = rY + cos(rT) * Xdot * totalTime;
  rT = rT + Thetadot * totalTime;

  if (rT > ( 2 * pi)){rT = rT - ( 2 * pi);}
  if (rT < 0){rT = rT + (2 * pi);}
  
  sparki.print("x: ");
  sparki.print(rX);
  
  sparki.print("  y: ");
  sparki.print(rY);
  
  sparki.print("  T: ");
  sparki.println(dT * (180 / pi));

  sparki.print("spin:");
  sparki.print(Thetadot);

  sparki.print(" sp:");
  sparki.print(Xdot);

  sparki.updateLCD();
    if(rho < 0.02){

    sparki.moveForward(0.02);
//    sparki.println(nu);
//    leftWheelSpeed = -nu;
//    rightWheelSpeed = nu;
//    if(abs(nu) < (5 * pi/180)){
      leftWheelSpeed = 0;
      rightWheelSpeed = 0;
//    }
    state = SendIdle;
  }
}

void readComm()
{
 String commArray [10];
 int arrayCounter = 0;
 while (Serial1.available() && !eC)
 {
 Serial1.println("Hello");
 int inByte = Serial1.read();
 if ((char)inByte == 'S')
 {
  arrayCounter = 0;
 }
 else if ((char)inByte == 'E')
 {
   eC = true;
   break;
 }
 else
 {
 //here is where the code differs a lot from the previous code
 if(inByte == 32) //if it's a blank space
 {
 arrayCounter ++; //increment array counter to store in new array space
 }
 else
 {
 //add the character to the arrayCounter space in commArray
 commArray[arrayCounter] += (char)inByte;
 }
 }
 }
 if((String) commArray[1] == "move")
 {
  Serial1.println("here!!");
  gX = (float) atof(commArray[2].c_str());
  gY = (float) atof(commArray[3].c_str());
  state = MTG;
 }
 else if ((String) commArray[1] == "scan"){
  state = SA;
 }
}


void updateSensorCM(int angle) {
  String XiS = (String)" "+rX;
  String YiS = (String) XiS+" "+rY;
  String ThetaiS = (String) YiS+" "+rT;  
  String angleS = (String) ThetaiS+" "+angle;
  String pingS = (String) "S scan"+angleS+" "+sparki.ping()+" "+"E";
  Serial1.println(pingS);
  sparki.clearLCD();
  sparki.print(pingS);
  sparki.updateLCD();
  delay(100);
}

int scanDir() {
  // those angle ranges are the best for sparki spin his head, i.e. 180 degree
  for (int angle = -80; angle < 81; angle = angle + 1){
    sparki.servo(angle);
    updateSensorCM(angle);
    //updateSensorRead();s
    if (angle >= 80){
      sparki.servo(SERVO_CENTER);
      state = SendIdle;
      Serial1.println("I'm hitting angle 80");
      eC = false;
    }
  }
}

void loop() {
switch ( state )
{
  case SA:
      scanDir();
      break;
  case MTG:
      moveToGoal();
      break;
  case SendIdle:
      Serial1.println("S idle E");
      state = WFI;
      break;
  case WFI:
      readComm();
      break;
}
  
//  sparki.moveForward(10);
//  Xrdot=phildotr/2.0+phirdotr/2.0;
//  Thetardot=phirdotr/alength-phildotr/alength;
//  Xi=Xi+cos(Thetai)*Xrdot*0.1;
//  Yi=(Yi+sin(Thetai)*Xrdot*0.1)+10;
//  Thetai=Thetai+Thetardot*0.1;
//  scanDir();
  delay(interval);
}
