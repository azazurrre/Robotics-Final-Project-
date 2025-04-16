int laserPin = 8;

#include <Servo.h>

Servo servo1;  // Servo for X-axis (left-right)
Servo servo2;  // Servo for Y-axis (up-down)

int current_pos1 = 90;  // Initial position for servo1
int current_pos2 = 90;  // Initial position for servo2



void setup() {
  // Initialize the servos
  pinMode(laserPin, OUTPUT);    // Set pin 8 as output
  digitalWrite(laserPin, LOW);  // Turn laser OFF at start
  servo1.attach(10);  // Servo 1 connected to pin 9
  servo2.attach(9); // Servo 2 connected to pin 10

  // Start serial communication
  Serial.begin(9600);

  //servo1.write(90);
  delay(500);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the input data from the serial port (dx, dy)
    String input = Serial.readStringUntil('\n');  // Read until newline

    if (input == "L"){
      digitalWrite(laserPin, LOW); 
    }
    else if (input == "H"){
      digitalWrite(laserPin, HIGH); 
    }
    else{
    int commaIndex = input.indexOf(',');
    int dx = input.substring(0, commaIndex).toInt();
    int dy = input.substring(commaIndex + 1).toInt();

    // Apply small steps for servo movement
    current_pos1 += dx;  // Update servo1 position based on dx
    current_pos2 += dy;  // Update servo2 position based on dy

    // Constrain the servo position to the valid range (0-180 degrees)
    current_pos1 = constrain(current_pos1, -360, 360);
    current_pos2 = constrain(current_pos2, -360, 360);

    // Control the servos based on the updated positions
    //servo1.write(180);
    //servo2.write(current_pos2);
    //servo1.attach(10);
    //servo1.write(current_pos1);
    servo1.write(current_pos1);
    servo2.write(current_pos2);

    delay(100);  // Add delay to avoid rapid movement
    }
  }
}
// #include <Servo.
