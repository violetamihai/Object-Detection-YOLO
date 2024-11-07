

#include <Stepper.h>

const int stepsPerRevolution = 300;  


Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
 
  myStepper.setSpeed(2);

  Serial.begin(9600);
}

void loop() {
 
  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  delay(500);


  Serial.println("counterclockwise");
  myStepper.step(-stepsPerRevolution);
  delay(500);
}

