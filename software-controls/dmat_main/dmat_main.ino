#include "Arduino.h"
#include "Arduino_BHY2Host.h"



//#include <Servo.h>


SensorXYZ accel(SENSOR_ID_ACC);
SensorOrientation ori(SENSOR_ID_ORI);
Sensor baro(SENSOR_ID_BARO);
SensorXYZ linaccel(SENSOR_ID_LACC);
SensorXYZ gyro(SENSOR_ID_GYRO);

const int targetApogee = 10000; // Target apogee in feet
const int safetyFloor = 5000; // Safety altitude floor in feet
const int maxVelocity = 80; // Maximum velocity in m/s

//int servoPin = 9;

//Servo airbrakeServo;

// Velocity estimation
#include <accIntegral.h>
// =========== Settings ===========
accIntegral fusion;

// Filter coefficients                       //  Unit           
constexpr float GRAVITY = 9.81e3;            //  mm/s^2             Magnitude of gravity at rest. Determines units of velocity. [UNITS MUST MATCH ACCELERATION]
constexpr float SD_ACC  = 1000 / GRAVITY;    //  mm/s^2 / g-force   Standard deviation of acceleration. Deviations from zero are suppressed.
constexpr float SD_VEL  = 200  / GRAVITY;    //  mm/s   / g-force   Standard deviation of velocity. Deviations from target value are suppressed.
constexpr float ALPHA   = 0.5;                /* Fusion gain, value between 0 and 1 - Determines orientation correction with respect to gravity vector. 
                                 If set to 1 the gyroscope is dissabled. If set to 0 the accelerometer is dissabled (equivant to gyro-only) */


void setup() {
  // debug port
  Serial.begin(115200);
  while(!Serial);

 // NOTE: if Nicla is used as a Shield on top of a MKR board we must use:
  BHY2Host.begin(false, NICLA_AS_SHIELD);


  accel.begin();
  ori.begin();
  baro.begin();
  linaccel.begin();
  gyro.begin();

  fusion.reset();

  // Initialize servo
  //airbrakeServo.attach(servoPin);


}


void loop()
{
  static auto printTime = millis();
  BHY2Host.update();

  if (millis() - printTime >= 500) {
    printTime = millis();
    Serial.println(String("Acceleration values: ") + accel.toString());
    Serial.println(String("Orientation values: ") + ori.toString());
    Serial.println(String("Barometer value: ") + baro.toString());
    Serial.println(String("Linear Acceleration: ") + linaccel.toString());
    printVelocity();
  }
}


void printVelocity()
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

  // Update heading and velocity estimate:
  
  // known measured velocity (target state). Estimate will be forced towards this vector
  vec3_t vel_t = {0.0,0.0,0.0};

  vel_t /= GRAVITY;                         // must have unit: g-force * second
  
      /* note: all coefficients are optional and have default values */
  fusion.update( gyro_data, linaccel_data, vel_t, ALPHA ); 

      // obtain velocity estimate
  vec3_t vel = fusion.getVel() * GRAVITY;   // scale by gravity for desired units
  
  // Display velocity components: [view with serial plotter]
  Serial.print("Velocity X: ");
  Serial.print(vel.x, 5);
  Serial.print(" mm/s, Y: ");
  Serial.print(vel.y, 5);
  Serial.print(" mm/s, Z: ");
  Serial.print(vel.z, 5);
  Serial.println(" mm/s");
}
