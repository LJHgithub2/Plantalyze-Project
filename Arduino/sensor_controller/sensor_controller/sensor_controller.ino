#include <Arduino.h>
#include "src/utils/RtcManager.h"
#include "src/network/WebServerManage.h"
#include "src/sensors/SensorManager.h"
#include "include/Config.h"

#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial Serial1(BT_RXD, BT_TXD); // RX, TX
#endif

SensorManager sensorManager(DHTPIN, DHTTYPE, SOILPIN, CDSPIN);

// RtcManager rtcManager;

// Initialize Web Server Manager
WebServerManager webServer(ssid, pass, serverPort, sensorManager, maxRetries);

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  sensorManager.begin();
  webServer.begin(Serial1);
  // rtcManager.initialize();
}

void loop() {

    // rtcManager.updateDateTime();
    webServer.handleClients();

    delay(1000); // 10초마다
}
