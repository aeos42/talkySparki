#include <Sparki.h>
#include <stdio.h>
#include <string.h>

float pi = 3.1415926535897932384626;
int interval = 1000;
int cm = 0;
int loopCount = 0;
float maxspeed = 0.0285;    // [m/s] speed of the robot that you measured
float alength = 0.0851;     // [m] axle length
float phildotr = 0, phirdotr = 0; // wheel speeds that you sent to the motors
float Xi = 0, Yi = 0, Thetai = 0;
float Xrdot, Thetardot;

float rX; //robot coords
float rY;
float rT;
bool eC = false;
float Xg = 0.0;// = 0.2159;//goal coords
float Yg = 0.0;// = 0.2794;
float Thetag = 0.0;// = pi/2;

float a = 0.1;
float b = 1;
float c = 0.1;
float alpha, rho, eta; // error between positions in terms of angle to the goal, distance to the goal, and final angle

enum robotStates {
  SA,
  MTG,
  WFI,
  SendIdel
} state;

void setup() {
  // put your setup code here, to run once:
  sparki.servo(SERVO_CENTER);
  sparki.beep();
  Serial1.begin(9600);
  state = SA;
  rX = 0.3;
  rY = 0.4;
  rT = pi / 2;
}

void moveToGoal() {
  boolean move = true;
  while (move) {
    long int time_start = millis();
    int threshold = 700;

    // CALCULATE ERROR
    rho   = sqrt((Xi - Xg) * (Xi - Xg) + (Yi - Yg) * (Yi - Yg));
    //alpha = Thetai-atan2(Yi-Yg,Xi-Xg)-PI/2.0;
    alpha = atan2(Yg - Yi, Xg - Xi) - Thetai;
    eta   = Thetai - Thetag;

    // CALCULATE SPEED IN ROBOT COORDINATE SYSTEM
    Xrdot = a * rho;
    //Xrdot=0;
    Thetardot = b * alpha + c * eta;

    // CALCULATE WHEEL SPEED
    phildotr = ( 2 * Xrdot - Thetardot * alength) / (2.0);
    phirdotr = ( 2 * Xrdot + Thetardot * alength) / (2.0);

    // SET WHEELSPEED

    if (phildotr > maxspeed) {
      phildotr = maxspeed;
    }
    else if (phildotr < -maxspeed) {
      phildotr = -maxspeed;
    }
    if (phirdotr > maxspeed) {
      phirdotr = maxspeed;
    } else if (phirdotr < -maxspeed) {
      phirdotr = -maxspeed;
    }

    float leftspeed  = abs(phildotr);
    float rightspeed = abs(phirdotr);

    leftspeed = (leftspeed / maxspeed) * 100;//100
    rightspeed = (rightspeed / maxspeed) * 100;//100

    if (rho > 0.01) // if farther away than 1cm
    {
      if (phildotr > 0)
      {
        sparki.motorRotate(MOTOR_LEFT, DIR_CCW, leftspeed);
      }
      else
      {
        sparki.motorRotate(MOTOR_LEFT, DIR_CW, leftspeed);
      }
      if (phirdotr > 0)
      {
        sparki.motorRotate(MOTOR_RIGHT, DIR_CW, rightspeed);
      }
      else
      {
        sparki.motorRotate(MOTOR_RIGHT, DIR_CCW, rightspeed);
      }
    }
    else
    {
      float degs = Thetai * (180 / pi);
      float diff = (degs - Thetag);
      if (diff > 0) {
        sparki.moveRight(abs(diff));
      }
      if (diff < 0) {
        sparki.moveLeft(abs(diff));
      }
      Thetai = Thetag * (pi / 180);
      sparki.moveStop();
      state = SendIdel;
      move = false;
    }

    sparki.clearLCD(); // wipe the screen

    sparki.print(Xi);
    sparki.print("/");
    sparki.print(Yi);
    sparki.print("/");
    sparki.print(Thetai);
    sparki.println();
    sparki.print(alpha / PI * 180);
    sparki.println();

    sparki.updateLCD(); // display all of the information written to the screen

    // perform odometry
    Xrdot = phildotr / 2.0 + phirdotr / 2.0;
    Thetardot = phirdotr / alength - phildotr / alength;

    Xi = Xi + cos(Thetai) * Xrdot * 0.1;
    Yi = Yi + sin(Thetai) * Xrdot * 0.1;
    Thetai = Thetai + Thetardot * 0.1;

    while (millis() < time_start + 100);
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
      if (inByte == 32) //if it's a blank space
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
  if ((String) commArray[1] == "move")
  {
    Serial1.println("here!!");
    Yg = - (float) atof(commArray[2].c_str());
    Xg = (float) atof(commArray[3].c_str());
    Thetag = (float) atof(commArray[4].c_str());
    state = MTG;
  }
  else if ((String) commArray[1] == "scan") {
    state = SA;
  }
}

void updateSensorCM(int angle) {
  String XiS = (String)" " + Xi;
  String YiS = (String) XiS + " " + Yi;
  String ThetaiS = (String) YiS + " " + Thetai;
  String angleS = (String) "S scan" + ThetaiS + " " + angle + " " + sparki.ping() + " " + "E";
  //String thatS = (String) "S scan"+angleS+" "+sparki.ping()+" "+"E";
  Serial1.println(angleS);
  sparki.clearLCD();
  sparki.println(angleS);
  sparki.updateLCD();
  delay(100);
}

int scanDir() {
  // those angle ranges are the best for sparki spin his head, i.e. 180 degree
  for (int angle = -80; angle < 81; angle = angle + 10) {
    sparki.servo(angle);
    updateSensorCM(angle);
    //updateSensorRead();s
    if (angle >= 80) {
      sparki.servo(SERVO_CENTER);
      state = SendIdel;
      Serial1.println("I'm hitting angle 80");
      //eC = false;
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
    case SendIdel:
      Serial1.println("S Idle E");
      state = WFI;
      break;
    case WFI:
      eC = false;
      readComm();
      break;
  }
  delay(interval);
}
