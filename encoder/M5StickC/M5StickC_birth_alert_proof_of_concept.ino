// M5 alert Proof of Concept
// Copyright (c) Over het paard
// First viable product demonstration june 2019

#define VERSION "0.13"

#include <arduino.h>
#include <M5StickC.h>
#include <math.h>

// Some variable definitions
String previousPosture, currentPosture = "Flying"; // Default value
int lastPostureChangeMillis = 0; // Time stamp so to be able to tell how long a posture change is in place
bool alert = false; // Set after a certain number of seconds in a laying posture
bool alertHasBeenSent = false; // Keep track to see if alert has been sent already
int birthingTreshold = 8; // Seconds to count down once 'Laying' has been 
double averageCurrentConsumption;
double totalCurrentConsumption = 0;
long numberOfCurrentConsumptionMeasurements = 0;
bool onBattery = true;

// Most important angle calculation: rotation over the width-axis
float getRoll() {
  int16_t accX = 0;
  int16_t accY = 0;
  int16_t accZ = 0;
  float angle;
  M5.IMU.getAccelData(&accX,&accY,&accZ);  
  angle = atan2(accY, accZ) * 180 / M_PI;
  return angle;
}

// Also usable angle calculation: rotation over the length-axis
float getPitch() {
  int16_t accX = 0;
  int16_t accY = 0;
  int16_t accZ = 0;
  float angle;
  M5.IMU.getAccelData(&accX,&accY,&accZ); // Get the raw accelerometer values
  angle = atan2(-accX, sqrt(accY * accY + accZ * accZ)) * 180/M_PI; // Calculate a degrees value
  return angle;
}

// Get the actual 80mAh battery voltage (only when not charging)
double getBatteryVoltage() {
  double vbat;
  vbat = M5.Axp.GetVbatData() * 1.1 / 1000;
  return vbat;
}

int getCurrentConsumption() {
  int disch;
  disch = M5.Axp.GetIdischargeData() / 2;
  return disch;
}

double getBatteryCapacity() {
  double bat_p;
  M5.Axp.GetPowerbatData() * 1.1 * 0.5 / 1000;
  return bat_p;
}

String getPosture() {
  String p = "Standing";
  float a = getRoll(); // Might want to experiment with getPitch()
  if (a < 0) {
    a = -a;
  } 
  if ((a > 2) && (a < 40)) {
    p = "Laying";
  }
  return p;
}

void updateScreen(String posture, bool alert, int current) {
  //M5.Lcd.fillScreen(BLACK); // Clear screen with black background
  M5.Lcd.setTextSize(2); // 1 is smallest, 2 is somewhat bigger
  M5.Lcd.setCursor(0, 0);
  M5.Lcd.printf("M5 ALERT %s", VERSION);
  M5.Lcd.setTextSize(1);
  M5.Lcd.setCursor(0, 25);
  M5.Lcd.printf("Roll %.0f degrees   ", (float) getRoll());
  M5.Lcd.println();
  if (onBattery) {
    M5.Lcd.printf("Iavg %.0f mA / Vbat %.2f V  ", (float) current, (float) getBatteryVoltage());  
  } else {
    M5.Lcd.printf("(%.0f mA) Charging..      ", (float) current);  
  }
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(0,45);
  if (posture == "Standing") {
    M5.Lcd.println("Standing  ");
  } else {
    if (alert == true) {
      M5.Lcd.println("Birthing  ");      
    } else {
      M5.Lcd.println("Laying    ");
    }
  }
  M5.Lcd.setCursor(0,65);
  M5.Lcd.setTextSize(1);
  if (posture != "Standing") {
    M5.Lcd.printf("For %.0f seconds", (float) ((millis() - lastPostureChangeMillis) / 1000));
  } else {
    M5.Lcd.println("                       ");
  }
}

int powernap(int millis) {
  esp_sleep_enable_timer_wakeup(millis * 1000);
  int reason = esp_light_sleep_start();
  return reason;
}

void sendAlert() {
}

void setup() {
  // This code runs once automagically after startup
  M5.begin();
  
  // Internal sensor initialisation
  M5.IMU.Init(); // Initialize the accelerometer and gyroscope
  M5.Axp.EnableCoulombcounter(); // Initialize the battery manager

  averageCurrentConsumption = getCurrentConsumption();

  // Digital pins
  pinMode(M5_LED, OUTPUT);
  digitalWrite(M5_LED, LOW);
  pinMode(M5_BUTTON_HOME, INPUT);

  // Internal lcd
  M5.Axp.ScreenBreath(15);
  M5.Lcd.setRotation(3); // Set display orientation
  //M5.Lcd.setTextColor(WHITE); // Using textcolor even once ruins the overprint
  M5.Lcd.fillScreen(BLACK); // Clear screen with black background
}

void loop() {
  // This code repeats endlessly
  if (alert == true) {
      digitalWrite(M5_LED, LOW);
      if (!alertHasBeenSent) {
        //sendAlert();
        alertHasBeenSent = true;
      }
      if (digitalRead(M5_BUTTON_HOME) == LOW) {
        alert = false;
      }
  }

  if (getCurrentConsumption() > 0) {
    if (!onBattery) {
      onBattery = true;
      M5.Axp.ScreenBreath(8);
    }
    totalCurrentConsumption += getCurrentConsumption();
    numberOfCurrentConsumptionMeasurements++;
    averageCurrentConsumption = totalCurrentConsumption / numberOfCurrentConsumptionMeasurements;
  } else {
    if (onBattery) {
      onBattery = false; 
      M5.Axp.ScreenBreath(15);
    }
  }  
  
  currentPosture = getPosture();
  if (currentPosture != previousPosture) {
    previousPosture = currentPosture;
    lastPostureChangeMillis = millis();
    // alert = false;
  }
  
  if ((alert == false) && ((millis() - lastPostureChangeMillis) / 1000 > birthingTreshold)) {
    if (currentPosture == "Laying") {
      alert = true; // Might want to act on this, now we're in alert state
      alertHasBeenSent = false;
      lastPostureChangeMillis = millis(); // Reset counter so we know how long in alert state
    }
  }

  updateScreen(currentPosture, alert, averageCurrentConsumption);
  digitalWrite(M5_LED, HIGH);

  if (onBattery) {
    powernap(1000); // Reduces power during a delay from 80 (with display set to brightness 15) to 40 (without display) to about 9 mA
  } else {
    delay(1000); // Powernapping 
  }
}