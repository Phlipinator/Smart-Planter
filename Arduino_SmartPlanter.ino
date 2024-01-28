#include "Arduino.h"
#include "DFRobotDFPlayerMini.h"
#include <HardwareSerial.h>

HardwareSerial FPSerial(1);

DFRobotDFPlayerMini myDFPlayer;

// define the Pins for motion sensor and moisture sensor
#define MoistureSensor 12
#define MotionSensor 5


void setup() {
  FPSerial.begin(9600, SERIAL_8N1, 16, 17); // RX, TX
  Serial.begin(115200);

  Serial.println(F("DFRobot DFPlayer Mini Demo"));
  Serial.println(F("Initializing DFPlayer ..."));

  if (!myDFPlayer.begin(FPSerial)) {
    Serial.println(F("Unable to begin: Check connection and SD card."));
    while (true) {
      delay(0); // Prevent WDT reset on ESP
    }
  }
  Serial.println(F("DFPlayer Mini online."));
  myDFPlayer.volume(15);
  myDFPlayer.playFolder(2, 1);     // Play startup sound

  randomSeed(analogRead(0));

  pinMode(MotionSensor, INPUT); // Set the PIR sensor pin as an input
}

void loop() {
  // Change number of sound files here
  int randomNumber = random(1, 9);

  int moisture = analogRead(MoistureSensor); // read the analog value from sensor
  Serial.println(moisture);

  int sensorValue = digitalRead(MotionSensor); // read the motion sensor value

  if (sensorValue == HIGH && moisture < 1000) { // Check if the sensor is HIGH

    myDFPlayer.playFolder(1, randomNumber);

    delay(100000); // Wait for a second to avoid multiple detections
  }

  delay(1000);
}
