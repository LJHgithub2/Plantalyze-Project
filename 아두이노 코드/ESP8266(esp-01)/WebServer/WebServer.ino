
#include "WiFiEsp.h"
#include <ArduinoJson.h>

#ifndef HAVE_HWSERIAL1
#include <SoftwareSerial.h> 
#define BT_RXD 2 
#define BT_TXD 3 
SoftwareSerial Serial1(BT_RXD, BT_TXD); 
#endif


// char ssid[] = "jong";            // your network SSID (name)
// char pass[] = "dl994550";        // your network password
char ssid[] = "iptime_jong";            // your network SSID (name)
char pass[] = "ditlswlwhs3";        // your network password
int status = WL_IDLE_STATUS;     // wifi연결안된 상태
int retryCount = 0;             // wifi 연결시도 횟수
const int maxRetries = 10;  // wifi 최대 재시도 횟수

WiFiEspServer server(80);


// 함수 선언
void handleRoot(WiFiEspClient client);
void handleStatus(WiFiEspClient client);
void handleNotFound(WiFiEspClient client);


void setup()
{
  // initialize serial for debugging
  Serial.begin(115200);
  // initialize serial for ESP module
  Serial1.begin(9600);
  // initialize ESP module
  WiFi.init(&Serial1);

  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true);
  }

  // 해당 코드가 없으면 와이파이 연결이 안된다.
  // 원인 미상
  int numSsid = WiFi.scanNetworks();
  Serial.println(numSsid);
  // wifi 연결 시도
  while (status != WL_CONNECTED && retryCount < maxRetries) {
      // Serial.print("Attempting to connect to WPA SSID: ");
      Serial.println(ssid);
      status = WiFi.begin(ssid, pass);
      delay(100);  // 재시도 전 대기 시간
      retryCount++;
  }
  if (status != WL_CONNECTED) {
    Serial.println("Failed to connect to WiFi after maximum retries.");
    while (true);   // 다른 보드에서는 무한 루프를 통해 프로그램 멈춤
  }

  Serial.println("You're connected to the network");
  // 성공한 와이파이 이름 및 ip 출력
  printWifiStatus();
  
  // start the web server on port 80
  server.begin();
}

void loop() {
  WiFiEspClient client = server.available();
  
  if (client) {
    Serial.println("New client");
    boolean currentLineIsBlank = true;
    String request = "";
    String postData = "";
    int contentLength = 16;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        request += c;
        
        if (c == '\n' && currentLineIsBlank) {
            for (int i = 0; i < contentLength; i++) {
              if (client.available()) {
                postData += (char)client.read();
              }
            }
            processRequest(client, request, postData);
            break;
        }
        
        if (c == '\n') {
          currentLineIsBlank = true;
        } else if (c != '\r') {
          currentLineIsBlank = false;
        }
      }
    }
    delay(10);
    client.stop();
    Serial.println("Client disconnected");
  }
}
void processRequest(WiFiEspClient client, String request, String postData) {
  Serial.println("출력");
  Serial.println(request);
  Serial.println(postData);
  if (request.indexOf("GET /api/data") != -1) {
    StaticJsonDocument<200> doc;
    doc["sensor"] = "temperature";
    doc["value"] = 25.5;

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: application/json");
    client.println("Connection: close");
    client.println();
    
    String response;
    serializeJson(doc, response);
    client.println(response);
  } else {
    client.println("HTTP/1.1 404 Not Found");
    client.println("Content-Type: text/plain");
    client.println("Connection: close");
    client.println();
    client.println("404 Not Found");
  }
}
// void handleRoot(WiFiEspClient client) {
//   StaticJsonDocument<200> doc;
//   doc["message"] = "Welcome to the API server!";
//   doc["available_routes"] = "/status, /";

//   String response;
//   serializeJson(doc, response);
  
//   client.print("HTTP/1.1 200 OK\r\n");
//   client.print("Content-Type: application/json\r\n");
//   client.print("Connection: close\r\n");
//   client.print("\r\n");
//   client.print(response);
// }

// void handleStatus(WiFiEspClient client) {
//   StaticJsonDocument<200> doc;
//   doc["message"] = "Server is running";
//   doc["requests_received"] = ++reqCount;
//   doc["analog_A0"] = analogRead(0);

//   String response;
//   serializeJson(doc, response);
  
//   client.print("HTTP/1.1 200 OK\r\n");
//   client.print("Content-Type: application/json\r\n");
//   client.print("Connection: close\r\n");
//   client.print("\r\n");
//   client.print(response);
// }

// void handleNotFound(WiFiEspClient client) {
//   StaticJsonDocument<200> doc;
//   doc["error"] = "Route not found";

//   String response;
//   serializeJson(doc, response);
  
//   client.print("HTTP/1.1 404 Not Found\r\n");
//   client.print("Content-Type: application/json\r\n");
//   client.print("Connection: close\r\n");
//   client.print("\r\n");
//   client.print(response);
// }

void printWifiStatus()
{
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  
  // print where to go in the browser
  Serial.println();
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
  Serial.println();
}

