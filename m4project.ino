/*

  Arduino LSM6DS3 - Accelerometer Application
  This example reads the acceleration values as relative direction and degrees,
  from the LSM6DS3 sensor and prints them to the Serial Monitor or Serial Plotter.

  The circuit:
  - Arduino Nano 33 IoT
  Created by Riccardo Rizzo
  Modified by Jose García
  27 Nov 2020
  This example code is in the public domain.

*/


#include <Arduino_LSM6DS3.h>

float ax, ay, az, gx, gy, gz;
int degreesX = 0;
int degreesY = 0;

void setup() {

  Serial.begin(9600);

  while (!Serial);

  //Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // Serial.print("Accelerometer sample rate = ");
  // Serial.print(IMU.accelerationSampleRate());
  // Serial.println("Hz");
  // Serial.print("Gyroscope sample rate = ");
  // Serial.print(IMU.gyroscopeSampleRate());
  // Serial.println(" Hz");

}


void loop() {

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);
  }
  
  // Serial.print("ax: ");
  // Serial.print(ax);
  // Serial.print(" ay: ");
  // Serial.print(ay);
  // Serial.print(" az: ");
  // Serial.print(az);
  // Serial.print(" gx: ");
  // Serial.print(gx);
  // Serial.print(" gy: ");
  // Serial.print(gy);
  // Serial.print(" gz: ");
  // Serial.println(gz);

  // print the data in CSV format

  //Serial.print(gx, 3);
  // Serial.print(',');
  Serial.print(ay, 3);
  //Serial.print(',');
  //Serial.print(gz, 3);
  Serial.println();


  delay(10);

}