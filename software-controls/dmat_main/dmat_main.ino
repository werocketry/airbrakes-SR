//#define ARDUINO_PORTENTA_H7_M7
//#define CORE_NUM_INTERRUPT 21

#include "Arduino.h"
#include "Arduino_BHY2Host.h"

#include "altitude.h"

#include "altitude_eqn/altitude_eqn.h"

#include <Encoder.h>
#include <PID_v1.h>
#include "DCMotorServo.h" // from https://github.com/CameronBrooks11/DCMotorServo

#define pin_dcmoto_encode1 0
#define pin_dcmoto_encode2 1
#define pin_dcmoto_dir1 2
#define pin_dcmoto_dir2 3
#define pin_dcmoto_pwm_out 4

// ESLOV - DO NOT USE
#define FORBIDDEN_PH8_I2C3_SDA 11
#define FORBIDDEN_PH7_I2C3_SCL 12
#define FORBIDDEN_PI0_SPI1_CS 7


// Encoder specifications
#define PPR 11 // Pulses per revolution (PPR) of the encoder
#define GEAR_RATIO 29 // Gear ratio of the gearbox. Change this according to your motor's gear ratio.

// Calculate Counts Per Revolution (CPR) for quadrature encoders
#define CPR (PPR * 4 * GEAR_RATIO)

DCMotorServo servo = DCMotorServo(pin_dcmoto_dir1, pin_dcmoto_dir2, pin_dcmoto_pwm_out, pin_dcmoto_encode1, pin_dcmoto_encode2);

// Define PID parameters as variables for easy adjustment
float KP = 0.1;
float KI = 0.15;
float KD = 0.05;


SensorXYZ accel(SENSOR_ID_ACC);
SensorOrientation ori(SENSOR_ID_ORI);
Sensor baro(SENSOR_ID_BARO);
SensorXYZ linaccel(SENSOR_ID_LACC);
SensorXYZ gyro(SENSOR_ID_GYRO);

AltBaro altBaro; // Barometer altitude estimator

struct vec3_t {
  float x;
  float y;
  float z;
};

// Altitude estimator
static AltitudeEstimator altitude = AltitudeEstimator(
        0.0005, // sigma Accel
        0.0005, // sigma Gyro
        0.018,   // sigma Baro
        0.5, // ca
        0.1);// accelThreshold

static void imuRead(float gyroData[3], float accelData[3])
{
      gyroData[0] = gyro.x()*PI/180.0/4096.0; // radians/second
      gyroData[1] = gyro.y()*PI/180.0/4096.0;
      gyroData[2] = gyro.z()*PI/180.0/4096.0;
      // and acceleration values
      accelData[0] = accel.x()/4096.0; // g-unit
      accelData[1] = accel.y()/4096.0;
      accelData[2] = accel.z()/4096.0;
}

float pastTime = millis();
float currentTime = millis();

bool printFlag = false;



void setup() {
  // debug port
  Serial.begin(115200);
  while(!Serial);

  pinMode(pin_dcmoto_dir1, OUTPUT);
  pinMode(pin_dcmoto_dir2, OUTPUT);
  pinMode(pin_dcmoto_pwm_out, OUTPUT);
  pinMode(pin_dcmoto_encode1, INPUT);
  pinMode(pin_dcmoto_encode2, INPUT);

  servo.myPID->SetTunings(KP, KI, KD);
  servo.setPWMSkip(50);
  servo.setAccuracy(14); // Accuracy based on encoder specifics

 // NOTE: if Nicla is used as a Shield on top of a MKR board we must use:
  BHY2Host.begin();


  accel.begin();
  ori.begin();
  baro.begin();
  linaccel.begin();
  gyro.begin();
}


void loop()
{

  static unsigned long debug_timeout = millis();
  
  servo.run();
  
  if (millis() - debug_timeout > 1000) { // Every 1000ms, print debug info
    debug_timeout = millis();
    Serial.println(servo.getDebugInfo());
  }

  // Check if data is available to read
  while (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command until a newline character
    command.trim(); // Remove any whitespace or newlines

    // Parse PID tuning commands
    if (command.startsWith("KP=")) {
      KP = command.substring(3).toFloat();
      servo.myPID->SetTunings(KP, KI, KD);
      Serial.print("KP set to: ");
      Serial.println(KP);
    }
    else if (command.startsWith("KI=")) {
      KI = command.substring(3).toFloat();
      servo.myPID->SetTunings(KP, KI, KD);
      Serial.print("KI set to: ");
      Serial.println(KI);
    }
    else if (command.startsWith("KD=")) {
      KD = command.substring(3).toFloat();
      servo.myPID->SetTunings(KP, KI, KD);
      Serial.print("KD set to: ");
      Serial.println(KD);
    }else if (command.startsWith("MOVE=")) {
      String value = command.substring(5); // Extract the command value
      if (value == "1R") {
        // If the command is to rotate one full revolution
        servo.move(CPR); // Move the motor by one full revolution based on CPR
        Serial.println("Rotating one full revolution");
      } else {
        int newPosition = value.toInt(); // Try to convert to integer for custom moves
        if (newPosition != 0) {
          servo.move(newPosition); // Move the motor to the new position
          Serial.print("Moving to: ");
          Serial.println(newPosition);
        } else {
          Serial.println("Invalid MOVE command");
        }
      }
    }
    else if (command.startsWith("MAXPWM=")) {
      int maxPWM = command.substring(7).toInt(); // Extract and convert max PWM value to integer
      if (maxPWM >= 0 && maxPWM <= 255) {
        servo.setMaxPWM(maxPWM); // Set the maximum PWM value
        Serial.print("Setting MAXPWM to: ");
        Serial.println(maxPWM);
      } else {
        Serial.println("Invalid MAXPWM command");
      }
    } else {
      Serial.println("Invalid command");
    }
  }


// --------------------------

  BHY2Host.update();

  // Check for serial input to toggle printFlag
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command until a newline character.
    command.trim(); // Trim any whitespace.

    if (command.equals("toggle")) { // If the command is "toggle", invert the printFlag state.
      printFlag = !printFlag;
      Serial.println(printFlag ? "Printing Enabled" : "Printing Disabled"); // Feedback.
    }
  }  

  currentTime = millis();
  

  if ((currentTime - pastTime) > 50 && !printFlag)
  {
    // get all necessary data
    float pressure = baro.value();
    altBaro.update(pressure);
    float baroHeight =  altBaro.getAltitude();
    uint32_t timestamp = micros();
    float accelData[3];
    float gyroData[3];
    imuRead(gyroData, accelData);
    altitude.estimate(accelData, gyroData, baroHeight, timestamp);
    Serial.print("Altitude Estimator: ");
    Serial.print(baroHeight);
    Serial.print(",");
    Serial.print(altitude.getAltitude());
    Serial.print(",");
    Serial.print(altitude.getVerticalVelocity());
    Serial.print(",");
    Serial.println(altitude.getVerticalAcceleration());
    pastTime = currentTime;
  }



  static auto printTime = millis();
  if (millis() - printTime >= 500 && printFlag) {
    printTime = millis();
    Serial.println(String("Acceleration values: ") + accel.toString());
    Serial.println(String("Orientation values: ") + ori.toString());
    Serial.println(String("Barometer value: ") + baro.toString());
    Serial.println(String("Linear Acceleration: ") + linaccel.toString());
    printSerialwUnits();
  }


}


void printSerialwUnits()
{
    // Measure state:  
  vec3_t linaccel_data = { linaccel.x()/4096.0, linaccel.y()/4096.0, linaccel.z()/4096.0};    // g-unit
  vec3_t gyro_data = { gyro.x()*PI/180.0/4096.0, gyro.y()*PI/180.0/4096.0, gyro.z()*PI/180.0/4096.0};     // radians/second

  // Print linear acceleration data with units
  Serial.print("Linear Acceleration X: ");
  Serial.print(linaccel_data.x, 6); // Assuming 6 decimal places for precision
  Serial.print(" g, Y: ");
  Serial.print(linaccel_data.y, 6);
  Serial.print(" g, Z: ");
  Serial.print(linaccel_data.z, 6);
  Serial.println(" g");

  // Print gyro data with units
  Serial.print("Gyro Data X: ");
  Serial.print(gyro_data.x, 6); // Assuming 6 decimal places for precision
  Serial.print(" rad/s, Y: ");
  Serial.print(gyro_data.y, 6);
  Serial.print(" rad/s, Z: ");
  Serial.print(gyro_data.z, 6);
  Serial.println(" rad/s");

}
