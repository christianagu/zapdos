#include <Servo.h>

Servo servo;

void setup() {
  servo.attach(2);  // Assumes servo is connected to pin 2
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String posString = Serial.readStringUntil('\n');  // Read the string until a newline character
    int pos = posString.toInt();  // Convert the string to integer
    servo.write(pos);  // Set the servo position
  }
}
