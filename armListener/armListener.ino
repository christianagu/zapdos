#include <Servo.h>

Servo baseJointServo;
Servo joint2Servo;
Servo joint3Servo;
Servo endeffector;

#define TRIG_PIN 6  // Change this according to your connection
#define ECHO_PIN 7  // Change this according to your connection
long duration;
int distance;

void setup() {

  endeffector.attach(2);    // Connect endeffector servo to pin 2
  baseJointServo.attach(3);    // Connect first joint servo to pin 3
  joint2Servo.attach(4);    // Connect second joint servo to pin 4
  joint3Servo.attach(5);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
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
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    duration = pulseIn(ECHO_PIN, HIGH);
    distance = duration * 0.034 / 2;  // Convert to cm

    // Optionally send distance to Python for logging or other purposes
    Serial.print("Distance: ");
    Serial.println(distance);
}
