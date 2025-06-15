// Pin configuration
const int trigPin = 8;
const int echoPin = 9;

const int motor1Pin1 = 4; // Motor 1 - IN1
const int motor1Pin2 = 5; // Motor 1 - IN2
const int motor2Pin1 = 7; // Motor 2 - IN3
const int motor2Pin2 = 6; // Motor 2 - IN4

// PID constants
float Kp = 6.0;  // Proportional gain
float Ki = 0.0001;  // Integral gain
float Kd = 1.0;  // Derivative gain

// Desired wall distance in cm
const int targetDistance = 10;

// PID variables
float error = 0, previousError = 0, integral = 0, derivative = 0;
int motorSpeed = 255;  // Default motor speed (maximum)

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Initialize motor control pins
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);

  // Initialize ultrasonic sensor pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  long duration, distance;

  // Trigger the ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure the duration of the echo pulse
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance from the sensor to the object
  distance = (duration / 2) * 0.0344;

  // Debugging: Print the distance value
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Calculate the PID error
  error = targetDistance - distance;
  integral += error;
  derivative = error - previousError;

  // Compute the PID output
  int pidOutput = (Kp * error) + (Ki * integral) + (Kd * derivative);

  // Apply the PID output to adjust motor speeds
  adjustMotors(pidOutput);

  // Store the current error as the previous error for next iteration
  previousError = error;

  delay(100); // Small delay for stability
}

// Function to adjust motor speeds based on PID output
void adjustMotors(int pidOutput) {
  int leftMotorSpeed = motorSpeed;
  int rightMotorSpeed = motorSpeed;

  // If PID output is positive, the robot needs to turn left
  if (pidOutput > 0) {
    leftMotorSpeed = motorSpeed - pidOutput;  // Slow down left motor
    rightMotorSpeed = motorSpeed;  // Keep right motor speed
  }
  // If PID output is negative, the robot needs to turn right
  else if (pidOutput < 0) {
    leftMotorSpeed = motorSpeed;  // Keep left motor speed
    rightMotorSpeed = motorSpeed + pidOutput;  // Slow down right motor
  }

  // Constrain motor speeds to valid range (0-255)
  leftMotorSpeed = constrain(leftMotorSpeed, 0, 255);
  rightMotorSpeed = constrain(rightMotorSpeed, 0, 255);

  // Set motor speeds
  setMotorSpeed(leftMotorSpeed, rightMotorSpeed);
}

// Function to control the motor direction and speed
void setMotorSpeed(int leftSpeed, int rightSpeed) {
  if (leftSpeed > 0) {
    analogWrite(motor1Pin1, leftSpeed);
    analogWrite(motor1Pin2, 0);
  } else {
    analogWrite(motor1Pin1, 0);
    analogWrite(motor1Pin2, -leftSpeed);
  }

  if (rightSpeed > 0) {
    analogWrite(motor2Pin1, rightSpeed);
    analogWrite(motor2Pin2, 0);
  } else {
    analogWrite(motor2Pin1, 0);
    analogWrite(motor2Pin2, -rightSpeed);
  }
}
