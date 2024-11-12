#include <Arduino.h>
#include "src/sensors/DHTSensor.h"
#include "src/sensors/LightSensor.h"
#include "src/sensors/SoilMoistureSensor.h"
#include "src/utils/RtcManager.h"
#include "src/network/WebServerManage.h"
#include "include/Config.h"

#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial Serial1(BT_RXD, BT_TXD); // RX, TX
#endif

DHTSensor dhtSensor(DHTPIN, DHTTYPE);
SoilMoistureSensor soilSensor(SOILPIN);
LightSensor lightSensor(CDSPIN);

RtcManager rtcManager;
// Initialize Web Server Manager
WebServerManager webServer(ssid, pass, serverPort, maxRetries);

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  webServer.begin(Serial1);
  dhtSensor.begin();
  rtcManager.initialize();
}

void loop() {

    rtcManager.updateDateTime();
    
    int soilMoisture = soilSensor.getSoilMoisture();
    int lightLevel = lightSensor.getLightLevel();
    float humidity = dhtSensor.getHumidity();
    float temperature = dhtSensor.getTemperature();

    Serial.print("CDS_value: ");
    Serial.println(lightLevel);    
    Serial.print("Soil_moisture: ");
    Serial.println(soilMoisture);    
    Serial.print("Humidity: ");
    Serial.println(humidity);
    Serial.print("Temperature: ");
    Serial.println(temperature);   
    Serial.println(); 

  
    webServer.handleClients();

    delay(1000); // 1초마다
}
