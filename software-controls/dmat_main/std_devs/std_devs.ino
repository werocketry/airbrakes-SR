#include "Arduino.h"
#include "Arduino_BHY2Host.h"

SensorXYZ accel(SENSOR_ID_ACC);
Sensor baro(SENSOR_ID_BARO);
SensorXYZ gyro(SENSOR_ID_GYRO);

static void imuRead(float gyroData[3], float accelData[3])
{
  gyroData[0] = gyro.x() * PI / 180.0 / 4096.0; // radians/second
  gyroData[1] = gyro.y() * PI / 180.0 / 4096.0;
  gyroData[2] = gyro.z() * PI / 180.0 / 4096.0;
  // and acceleration values
  accelData[0] = accel.x() / 4096.0; // g-unit
  accelData[1] = accel.y() / 4096.0;
  accelData[2] = accel.z() / 4096.0;
}

// Number of readings from which standard deviations will be computed
uint16_t iterations = 1000;

// Function to compute barometer standard deviations
float getBarometerSigma(uint16_t numberOfIterations)
{
  // here we will store all pressure readings
  float history[numberOfIterations];
  float meanPressure = 0;
  for (uint16_t index = 0; index < numberOfIterations; index++)
  {
    BHY2Host.update();
    float readPressure = baro.value();
    history[index] = readPressure;
    // we will use pressureSum to compute the mean pressure
    meanPressure += readPressure;
  }
  meanPressure /= numberOfIterations;
  // Compute standard deviation
  float numerator = 0;
  for (uint16_t index = 0; index < numberOfIterations; index++)
  {
    numerator += pow(history[index] - meanPressure, 2);
  }
  return sqrt(numerator / (numberOfIterations - 1));
}

// Function to compute accelerometer and gyrometer standard deviations
void getAccelAndGyroSigmas(double *sigmaAccel, double *sigmaGyro, uint16_t numberOfIterations)
{
  // here we will store each accel axis' readings
  float accelHistoryX[numberOfIterations];
  float accelHistoryY[numberOfIterations];
  float accelHistoryZ[numberOfIterations];
  // here we will store each gyro axis' readings
  float gyroHistoryX[numberOfIterations];
  float gyroHistoryY[numberOfIterations];
  float gyroHistoryZ[numberOfIterations];
  float meanAccelX = 0;
  float meanAccelY = 0;
  float meanAccelZ = 0;
  float meanGyroX = 0;
  float meanGyroY = 0;
  float meanGyroZ = 0;

  for (uint16_t index = 0; index < numberOfIterations; index++)
  {
    BHY2Host.update();
    float readGyro[3];
    float readAccel[3];
    imuRead(readGyro, readAccel);
    // store gyro readings
    gyroHistoryX[index] = readGyro[0];
    gyroHistoryY[index] = readGyro[1];
    gyroHistoryZ[index] = readGyro[2];
    // store accel readings
    accelHistoryX[index] = readAccel[0];
    accelHistoryY[index] = readAccel[1];
    accelHistoryZ[index] = readAccel[2];
    // increase mean sums
    meanGyroX += readGyro[0];
    meanGyroY += readGyro[1];
    meanGyroZ += readGyro[2];

    meanAccelX += readAccel[0];
    meanAccelY += readAccel[1];
    meanAccelZ += readAccel[2];
  }
  // Compute means
  meanGyroX /= numberOfIterations;
  meanGyroY /= numberOfIterations;
  meanGyroZ /= numberOfIterations;

  meanAccelX /= numberOfIterations;
  meanAccelY /= numberOfIterations;
  meanAccelZ /= numberOfIterations;

  // Compute standard deviations
  double numeratorGyroX = 0;
  double numeratorGyroY = 0;
  double numeratorGyroZ = 0;

  double numeratorAccelX = 0;
  double numeratorAccelY = 0;
  double numeratorAccelZ = 0;

  for (uint16_t index = 0; index < numberOfIterations; index++)
  {
    numeratorGyroX += pow(gyroHistoryX[index] - meanGyroX, 2);
    numeratorGyroY += pow(gyroHistoryY[index] - meanGyroY, 2);
    numeratorGyroZ += pow(gyroHistoryZ[index] - meanGyroZ, 2);

    numeratorAccelX += pow(accelHistoryX[index] - meanAccelX, 2);
    numeratorAccelY += pow(accelHistoryY[index] - meanAccelY, 2);
    numeratorAccelZ += pow(accelHistoryZ[index] - meanAccelZ, 2);
  }
  // Now, to compute on single standard deviation value for each
  // sensor, Gyro and Accel, we will take the maximum of the standard
  // deviations of each axis.
  double gyroSigmaX = sqrt(numeratorGyroX / (numberOfIterations - 1));
  double gyroSigmaY = sqrt(numeratorGyroY / (numberOfIterations - 1));
  double gyroSigmaZ = sqrt(numeratorGyroZ / (numberOfIterations - 1));

  double accelSigmaX = sqrt(numeratorAccelX / (numberOfIterations - 1));
  double accelSigmaY = sqrt(numeratorAccelY / (numberOfIterations - 1));
  double accelSigmaZ = sqrt(numeratorAccelZ / (numberOfIterations - 1));

  double tmp = max(gyroSigmaX, gyroSigmaY);
  *sigmaGyro = max(tmp, gyroSigmaZ);
  tmp = max(accelSigmaX, accelSigmaY);
  *sigmaAccel = max(tmp, accelSigmaZ);
}

void setup()
{
  // debug port
  Serial.begin(115200);
  while (!Serial);

  // NOTE: if Nicla is used as a Shield on top of a MKR board we must use:
  BHY2Host.begin();

  accel.begin();
  baro.begin();
  gyro.begin();
}

void loop(void)
{
  static unsigned long lastRun = 0;
  unsigned long currentMillis = millis();

  if (currentMillis - lastRun >= 5000) { 
    lastRun = currentMillis; 
    Serial.println("Computing Barometer standard deviation");
    float baroSigma = getBarometerSigma(iterations);
    Serial.print("Barometer standard deviation: ");
    Serial.println(baroSigma, 30);
    Serial.println("Computing Accelerometer and Gyrometer standard deviations");
    double accelSigma;
    double gyroSigma;
    getAccelAndGyroSigmas(&accelSigma, &gyroSigma, iterations);
    Serial.print("Accelerometer standard deviation: ");
    Serial.println(accelSigma, 30);
    Serial.print("Gyrometer standard deviation: ");
    Serial.println(gyroSigma, 30);
  }
}
