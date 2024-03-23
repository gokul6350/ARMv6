#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// https://github.com/90x-Development/Uno-arm
// version 9.87

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

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
    
    switch (command) {
      case 'b':
        angle = Serial.parseInt();
        moveServo(0, angle);  // Servo 1
        break;
      case 'a':
        angle = Serial.parseInt();
        moveServo(2, angle);  // Servo 2
        break;
      case 'h':
        angle = Serial.parseInt();
        moveServo(3, angle);  // Servo 3
        break;
      case 'f':
        angle = Serial.parseInt();
        moveServo(4, angle);  // Servo 4
        break;
    }
  }
}

void moveServo(uint8_t servoNum, int degrees) {
  int pulse = map(degrees, 0, 180, 102, 512);
  pwm.setPWM(servoNum, 0, pulse);
}
