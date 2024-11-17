#ifndef WEBSERVERMANAGER_H
#define WEBSERVERMANAGER_H

#include <WiFiEsp.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include "../sensors/SensorManager.h"

class WebServerManager {
public:
    WebServerManager(const char* ssid, const char* pass, int serverPort, SensorManager sensormanager, int maxRetries = 10);
    void begin(SoftwareSerial& Serial1);
    void handleClients();
    
private:
    const char* ssid;
    const char* pass;
    WiFiEspServer server;
    int maxRetries;
    int retryCount;
    int status;
    SensorManager sensormanager;

    void processRequest(WiFiEspClient client);
    void printWifiStatus();
};

#endif // WEBSERVERMANAGER_H
