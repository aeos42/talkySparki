#include <Sparki.h>
#include <stdio.h>
#include <string.h>

static float pi = 3.1415926535897932384626;
int interval = 1000;
int loopCount = 0;
static float maxspeed = 0.0285;    // [m/s] speed of the robot that you measured
static float alength = 0.0851;     // [m] axle length
float phildotr = 0, phirdotr = 0; // wheel speeds that you sent to the motors
float Xi = 0, Yi = 0, Thetai = 0;
float Xrdot, Thetardot;


bool eC = false;
float Xg = 0.0;// = 0.2159;//goal coords
float Yg = 0.0;// = 0.2794;
float Thetag = 0.0;// = pi/2;

float alpha, rho, eta; // error between positions in terms of angle to the goal, distance to the goal, and final angle

float a = 0.1;
float b = 1;
float c = 0.1;



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
}

void moveToGoal() {
  boolean move = true;
  while (move) {
    long int time_start = millis();

    int lineL = sparki.lineLeft();
    int lineC = sparki.lineCenter();
    int lineR = sparki.lineRight();

    if (lineL > 700) {
      Serial1.println("S help " + String((-Yi) * 100) + " " + String(Xi * 100) + " E");
      sparki.moveStop();
      sparki.beep();
      state = WFI;
      break;
    }
  
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

  float normalization = max(phildotr, phirdotr);
  phildotr = phildotr * (maxspeed / normalization);
  phirdotr = phirdotr * (maxspeed / normalization);


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
    state = WFI;
    move = false;
  }

  // perform odometry
  Xrdot = phildotr / 2.0 + phirdotr / 2.0;
  Thetardot = phirdotr / alength - phildotr / alength;

  Xi = Xi + cos(Thetai) * Xrdot * 0.1;
  Yi = Yi + sin(Thetai) * Xrdot * 0.1;
  Thetai = Thetai + Thetardot * 0.1;
  
  displayInfo();
  while (millis() < time_start + 100);
}
}
void displayInfo() {

  sparki.clearLCD(); // wipe the screen

  sparki.print("X: ");
  sparki.print((-Yi));
  sparki.print("  G: ");
  sparki.println(Xg);

  sparki.print("Y: ");
  sparki.print(Xi);
  sparki.print("  G: ");
  sparki.println(Yg);

  sparki.print("T: ");
  sparki.print(Thetai);
  sparki.print("  G: ");
  sparki.println(Thetag);

  sparki.updateLCD(); // display all of the information written to the screen

}

void readComm()
{
  String commArray [10];
  int arrayCounter = 0;
  while (Serial1.available() && !eC)
  {
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
    Yg = - (float) atof(commArray[2].c_str()) / 100;
    Xg = (float) atof(commArray[3].c_str()) / 100;
    Thetag = (float) atof(commArray[4].c_str()) * pi / 180;
    sparki.clearLCD();
    sparki.print(commArray[3].c_str());
    sparki.updateLCD();
    delay(1000);
    state = MTG;
  }
  else if ((String) commArray[1] == "scan") {
    state = SA;
  }
}

void updateSensorCM(int angle) {
  String XiS = (String)" " + (-Yi) * 100;
  String YiS = (String) XiS + " " + Xi * 100;
  String ThetaiS = (String) YiS + " " + Thetai * 180 / pi;
  String angleS = (String) "S scan" + ThetaiS + " " + angle + " " + sparki.ping() + " " + "E";
  //String thatS = (String) "S scan"+angleS+" "+sparki.ping()+" "+"E";
  Serial1.println(angleS);

  sparki.clearLCD();
  sparki.print(angleS);
  sparki.updateLCD();
  delay(10);
}

int scanDir() {
  // those angle ranges are the best for sparki spin his head, i.e. 180 degree
  for (int angle = -45; angle < 45; angle = angle + 2) {
    sparki.servo(angle);
    updateSensorCM(angle);
    delay(100);
  }
  sparki.servo(SERVO_CENTER);
  state = SendIdle;

}

void loop() {
  displayInfo();
  switch ( state )
  {
    case SA:
      scanDir();
      break;
    case MTG:
      moveToGoal();
      break;
    case SendIdle:
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
