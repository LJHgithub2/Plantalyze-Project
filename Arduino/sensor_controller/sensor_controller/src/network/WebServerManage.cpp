#include "WebServerManage.h"

RingBuffer buf(8); // 요청 데이터를 저장할 버퍼

WebServerManager::WebServerManager(const char* ssid, const char* pass, int serverPort, SensorManager sensormanager, int maxRetries = 10)
    : ssid(ssid), pass(pass), maxRetries(maxRetries), server(serverPort), retryCount(0), status(WL_IDLE_STATUS), sensormanager(sensormanager) {
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
  // listen for incoming clients
  WiFiEspClient client = server.available();
  if (client) {
    Serial.println("New client");
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) {
            Serial.println("Sending response");
            // send a standard http response header
            // use \r\n instead of many println statements to speedup data send
            client.print(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                "Connection: close\r\n"
                "\r\n"
            );

            client.print("{");
            client.print("\"temperature\": " + String(sensormanager.getTemperature(), 2) + ",");
            client.print("\"humidity\": " + String(sensormanager.getHumidity(), 2) + ",");
            client.print("\"light\": " + String(sensormanager.getLightLevel(), 0) + ",");
            client.print("\"soil_moisture\": " + String(sensormanager.getSoilMoisture(), 2));
            client.print("}");
            break;
        }
        if (c == '\n') {
          // you're starting a new line
          currentLineIsBlank = true;
        }
        else if (c != '\r') {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
        }
      }
    }
    // give the web browser time to receive the data
    delay(10);

    // close the connection:
    client.stop();
    Serial.println("Client disconnected");
  }
}

void WebServerManager::processRequest(WiFiEspClient client) {
    Serial.println("Processing request...");
    sensormanager.printAll();
    
    // 센서 데이터 가져오기 및 검증
    String temperature = isnan(sensormanager.getTemperature()) ? "null" : String(sensormanager.getTemperature(), 2);
    String humidity = isnan(sensormanager.getHumidity()) ? "null" : String(sensormanager.getHumidity(), 2);
    String lightVal = isnan(sensormanager.getLightLevel()) ? "null" : String(sensormanager.getLightLevel(), 2);
    String soilVal = isnan(sensormanager.getSoilMoisture()) ? "null" : String(sensormanager.getSoilMoisture(), 2);

    // JSON 데이터 생성
    String data = "{";
    data += "\"status\": \"success\",";
    data += "\"message\": \"Sensor data retrieved successfully\",";
    data += "\"data\": {";
    data += "\"temperature\": " + temperature + ",";
    data += "\"humidity\": " + humidity + ",";
    data += "\"light\": " + lightVal + ",";
    data += "\"soilMoisture\": " + soilVal;
    data += "}";
    data += "}";

    Serial.println(data);

    // HTTP 응답 전송
    client.print(
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        "Connection: close\r\n"
        "\r\n");
    client.print(data);
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
