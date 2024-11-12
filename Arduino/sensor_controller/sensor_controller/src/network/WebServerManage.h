#ifndef WEBSERVERMANAGER_H
#define WEBSERVERMANAGER_H

#include <WiFiEsp.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>

class WebServerManager {
public:
    WebServerManager(const char* ssid, const char* pass, int serverPort, int maxRetries = 10);
    void begin(SoftwareSerial& Serial1);
    void handleClients();
    
private:
    const char* ssid;
    const char* pass;
    WiFiEspServer server;
    int maxRetries;
    int retryCount;
    int status;
    
    void processRequest(WiFiEspClient client, String request);
    void printWifiStatus();
};

#endif // WEBSERVERMANAGER_H
