#include <Servo.h>

Servo baseJointServo;
Servo joint2Servo;
Servo joint3Servo;
Servo endeffector;

void setup() {

  endeffector.attach(2);    // Connect endeffector servo to pin 2
  baseJointServo.attach(3);    // Connect first joint servo to pin 3
  joint2Servo.attach(4);    // Connect second joint servo to pin 4
  joint3Servo.attach(5);
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');  // Read the command string until a newline character

    char servoId = command.charAt(0);  // First character identifies the servo
    int pos = command.substring(1).toInt();  // Rest of the string is converted to integer for position

    switch(servoId) {
      case 'J':
        baseJointServo.write(pos);
        break;
      case 'K':
        joint2Servo.write(pos);
        break;
      case 'B':
        joint3Servo.write(pos);
        break;  
      case 'E':
        endeffector.write(pos);
        break;
      default:
        // Handle invalid commands or ignore
        break;
    }
    Serial.print("Received: ");
    Serial.println(command);
  }
}
