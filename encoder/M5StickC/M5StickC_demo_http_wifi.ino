// M5StickC WiFi/HTTP Proof of Concept
// Copyright (c) 2019 Testconsultancy Groep
// Demonstrate the use of wifi and http


//Nieuwe regel commentaar
#define INTERVAL_MS 60000
#define TIMEOUT_MS 5000

#include <M5StickC.h>
#include <WiFi.h>

// Some variables
double averageCurrentConsumption;
double totalCurrentConsumption = 0;
long numberOfCurrentConsumptionMeasurements = 0;
bool onBattery = true;
long timestampMillis;

// Change the values below to suit your needs
const char* ssid     = "ITPH-Gast"; 
const char* password = "itphgast";
const char* host = "maker.ifttt.com";
const char* my_ifttt_applet_name = "your applet name";
const char* my_ifttt_secret_key = "your ifttt long key";


int getCurrentConsumption() {
  int disch;
  disch = M5.Axp.GetIdischargeData() / 2;
  return disch;
}

int powernap(int millis) {
  esp_sleep_enable_timer_wakeup(millis * 1000);
  int reason = esp_light_sleep_start();
  return reason;
}

void updateDisplay() {
  
}

void setup() {
  M5.begin();
  // put your setup code here, to run once:
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // Internal sensor initialisation
  M5.IMU.Init(); // Initialize the accelerometer and gyroscope
  M5.Axp.EnableCoulombcounter(); // Initialize the battery manager

  averageCurrentConsumption = getCurrentConsumption();
  
   // Internal lcd
  M5.Axp.ScreenBreath(0); // Set brightness 7-15
  M5.Lcd.setRotation(3); // Set display orientation
  M5.Lcd.setTextColor(BLACK); // Using textcolor even once ruins  overprint
  M5.Lcd.fillScreen(BLACK); // Clear screen with black background
}

void loop() {
  // put your main code here, to run repeatedly:

  // Switch the display on
  M5.Axp.ScreenBreath(8); // Set brightness 7-15
 
  if (getCurrentConsumption() > 0) {
    if (!onBattery) {
      onBattery = true;
    }
    totalCurrentConsumption += getCurrentConsumption();
    numberOfCurrentConsumptionMeasurements++;
    averageCurrentConsumption = totalCurrentConsumption / numberOfCurrentConsumptionMeasurements;
  } else {
    if (onBattery) {
      onBattery = false; 
    }
  }  

  timestampMillis = millis();
  M5.Lcd.fillScreen(BLUE);
  WiFi.begin(ssid, password);

  while ( (WiFi.status() != WL_CONNECTED) && (millis() - timestampMillis < (TIMEOUT_MS * 2)) ) {
    delay(500);
    M5.Lcd.fillScreen(BLACK);
    delay(500);
    M5.Lcd.fillScreen(BLUE);
  }

  if (WiFi.status() != WL_CONNECTED) {
    M5.Lcd.fillScreen(RED);
  } else {
    M5.Lcd.fillScreen(GREEN);
    M5.Lcd.setTextSize(1); // 1 is smallest, 2 is somewhat bigger
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.printf("%.2f mA", averageCurrentConsumption);
    M5.Lcd.println();
    M5.Lcd.println(WiFi.localIP());
  }

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    M5.Lcd.fillScreen(RED);
    return;
  } else {
    M5.Lcd.println("Connected to host");
  }

  String url = "/trigger/" + String(my_ifttt_applet_name) + String("/with/key/") + String(my_ifttt_secret_key) + String("?value1=") + String(averageCurrentConsumption);

  // This will send the request to the server
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > TIMEOUT_MS) {
      M5.Lcd.fillScreen(RED);
      client.stop();
      return;
    }
  }
  M5.Lcd.println("GET request sent");

  // Read response from server
  int lines = 0;
  while (client.available()) {
    String line = client.readStringUntil('\r');
    lines ++;
    //Serial.print(line);
  }

  M5.Lcd.printf("Got %.0f lines returned\n", (float) lines);
  M5.Lcd.println("Disconnected");
  WiFi.disconnect();

  delay(1000); // Short delay to be able to deceipher messages

  // Switch the display off
  M5.Axp.ScreenBreath(0); // Set brightness 7-15
  M5.Lcd.fillScreen(BLACK); // Clear screen with blue background

  if (onBattery) {
    powernap(INTERVAL_MS); // Reduces power during a delay from 80 (with display set to brightness 15) to 40 (without display) to about 9 mA
  } else {
    delay(INTERVAL_MS); // Powernapping 
  }


}