#include "Arduino.h"
#include "Arduino_BHY2Host.h"
//#include "DCMotorServo.h" // from https://github.com/CameronBrooks11/DCMotorServo

SensorXYZ accel(SENSOR_ID_ACC);
SensorOrientation ori(SENSOR_ID_ORI);
Sensor baro(SENSOR_ID_BARO);
SensorXYZ linaccel(SENSOR_ID_LACC);
SensorXYZ gyro(SENSOR_ID_GYRO);



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
}