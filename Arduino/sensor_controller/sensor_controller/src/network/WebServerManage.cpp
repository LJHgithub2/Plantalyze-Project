#include "WebServerManage.h"

WebServerManager::WebServerManager(const char* ssid, const char* pass, int serverPort, int maxRetries = 10)
    : ssid(ssid), pass(pass), maxRetries(maxRetries), server(serverPort), retryCount(0), status(WL_IDLE_STATUS) {
    // 초기화 코드
}

void WebServerManager::begin(SoftwareSerial& Serial1) {
    // initialize ESP module
    WiFi.init(&Serial1);

    // check for the presence of the shield
    if (WiFi.status() == WL_NO_SHIELD) {
        Serial.println("WiFi shield not present");
        // don't continue
        while (true);
    }

    // Necessary code to scan networks
    int numSsid = WiFi.scanNetworks();
    Serial.println(numSsid);

    // attempt to connect to WiFi network
    while ( status != WL_CONNECTED) {
        Serial.print("Attempting to connect to WPA SSID: ");
        Serial.println(ssid);
        // Connect to WPA/WPA2 network
        status = WiFi.begin(ssid, pass);
    }

    if (status != WL_CONNECTED) {
        Serial.println("Failed to connect to WiFi after maximum retries.");
        while (true); // Halt execution
    }

    Serial.println("You're connected to the network");
    printWifiStatus();
    server.begin();
}

void WebServerManager::handleClients() {
    WiFiEspClient client = server.available();
    if (client) {
        Serial.println("New client");
        // an http request ends with a blank line
        boolean currentLineIsBlank = true;
        String request = "";
        while (client.connected()) {
            if (client.available()) {
                char c = client.read();
                Serial.print(c);
                request += c;
                
                if (c == '\n' && currentLineIsBlank) {
                    // Serial.println(request);
                    processRequest(client, request);
                    break;
                }
                
                if (c == '\n') {
                    currentLineIsBlank = true;
                } else if (c != '\r') {
                    currentLineIsBlank = false;
                }
            }
        }
        client.stop();
        Serial.println("Client disconnected");
    }
}

void WebServerManager::processRequest(WiFiEspClient client, String request) {
    Serial.println("Request Received:");
    Serial.println(request);
    
    client.print(
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Connection: close\r\n"  // the connection will be closed after completion of the response
    "Refresh: 20\r\n"        // refresh the page automatically every 20 sec
    "\r\n");
    client.print("<!DOCTYPE HTML>\r\n");
    client.print("<html>\r\n");
    client.print("<h1>Hello World!</h1>\r\n");
    client.print("<br>\r\n");
    client.print("<h1>수신 성공</h1>\r\n");
    client.print("</html>\r\n");

}

void WebServerManager::printWifiStatus() {
    // Print the SSID of the network you're attached to
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());

    // Print your WiFi shield's IP address
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);
    
    // Print where to go in the browser
    Serial.println();
    Serial.print("To see this page in action, open a browser to http://");
    Serial.println(ip);
    Serial.println();
}
