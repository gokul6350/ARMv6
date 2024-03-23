#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// https://github.com/90x-Development/Uno-arm
// version 9.87
//sudo chmod a+rw /dev/ttyACM0 
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// base> shoulder> elbow > fore arm > wrist > end effector / Gripper
// b>s>e>f>w>g
int currentAngles[8] = {90, 90, 90, 90, 90, 90, 90, 90};

void setup() {
  Serial.begin(9600);
  
  // Check if PCA9685 is connected
  if (!pwm.begin()) {
    Serial.println("Couldn't find PCA9685, check wiring!");
    while (1);
  }

  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(50);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    int angle;
    // base> shoulder> elbow > fore arm > wrist > end effector / Gripper
    // b>s>e>f>w>g

    
    switch (command) {
      case 'b':
        angle = Serial.parseInt();
        moveServo(0, angle);  // Servo 1
        break;
      case 's':
        angle = Serial.parseInt();
        moveServo(3, angle);  // Servo 2
        break;
      case 'e':
        angle = Serial.parseInt();
        moveServo(7, angle);  // Servo 3
        break;
      case 'f':
        angle = Serial.parseInt();
        moveServo(9, angle);  // Servo 4
        break;
      case 'w':
        angle = Serial.parseInt();
        moveServo(10, angle);  // Servo 5
        break;
      case 'g':
        angle = Serial.parseInt();
        moveServo(11, angle);  // Servo 6
        break;                
    }
  }
}

void moveServo(uint8_t servoNum, int degrees) {
  // Gradually move the servo to the desired angle
  for (int i = currentAngles[servoNum]; i != degrees; i += (degrees > currentAngles[servoNum]) ? 1 : -1) {
    pwm.setPWM(servoNum, 0, map(i, 0, 180, 102, 512));
    currentAngles[servoNum] = i; // Update current angle for this servo
    delay(20); // Adjust delay time for desired speed
  }
  
  Serial.print("==========");
  Serial.print(servoNum);
  Serial.print("==========");
  Serial.print(degrees);
  Serial.println(" degrees.");
  Serial.println(pwm.getPWM(servoNum));
 // Serial.println(currentAngles);
}

