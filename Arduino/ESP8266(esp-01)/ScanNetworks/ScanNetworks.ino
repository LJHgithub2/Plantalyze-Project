/*
 WiFiEsp example: ScanNetworks

 This example  prints the Wifi shield's MAC address, and
 scans for available Wifi networks using the Wifi shield.
 Every ten seconds, it scans again. It doesn't actually
 connect to any network, so no encryption scheme is specified.

 For more details see: http://yaab-arduino.blogspot.com/p/wifiesp.html
*/
// wifiesp라이브러리는 네트워크 통신을 쉽게 해주는 라이브러리이다.
#include "WiFiEsp.h"

// serial1통신이 이미 연결되어있지 않다면 소프트웨어로 연결하라
#ifndef HAVE_HWSERIAL1
#include <SoftwareSerial.h> 
#define BT_RXD 2 
#define BT_TXD 3 
SoftwareSerial Serial1(BT_RXD, BT_TXD); 
#endif

void setup() {
  // initialize serial for debugging
  Serial.begin(115200);
  // initialize serial for ESP module
  Serial1.begin(9600);
  // initialize ESP module
  WiFi.init(&Serial1);

  // 와이파이 쉴드가 있냐없냐 -> 별로 안중요
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true);
  }

  // Print WiFi MAC address
  printMacAddress();
}

void loop()
{
  // scan for existing networks
  Serial.println();
  // 모든 네트워크 목록 출력
  Serial.println("Scanning available networks...");
  // 정의한 network list 보여주는 함수이다.
  listNetworks();
  delay(10000);
}


void printMacAddress()
{
  // get your MAC address
  byte mac[6];
  WiFi.macAddress(mac);
  
  // print MAC address
  char buf[20];
  sprintf(buf, "%02X:%02X:%02X:%02X:%02X:%02X", mac[5], mac[4], mac[3], mac[2], mac[1], mac[0]);
  Serial.print("MAC address: ");
  Serial.println(buf);
}

void listNetworks()
{
  // Wifi.scanNetworks()함수는 찾은 와이파이의 총 개수를 반환한다.
  int numSsid = WiFi.scanNetworks();
  // 못찾았을경우 -1 반환
  if (numSsid == -1) {
    Serial.println("Couldn't get a wifi connection");
    while (true);
  }

  // print the list of networks seen
  Serial.print("Number of available networks:");
  Serial.println(numSsid);

  // 아까 찾은 네트워크 개수만큼 반복하여 정보출력
  // 찾은 와이파이는 0~numSsid로 인덱싱 되어있다.
  for (int thisNet = 0; thisNet < numSsid; thisNet++) {
    Serial.print(thisNet); // 몇번째
    Serial.print(") ");
    Serial.print(WiFi.SSID(thisNet)); // 네트워크 아이디 이름
    Serial.print("\tSignal: "); 
    Serial.print(WiFi.RSSI(thisNet)); // 신호 세기
    Serial.print(" dBm");
    Serial.print("\tEncryption: ");
    printEncryptionType(WiFi.encryptionType(thisNet)); // 해당 네트워크 보안정보
  }
}

// 사람이 보기 쉽게 보안방식을 출력해줌
void printEncryptionType(int thisType) {
  // read the encryption type and print out the name
  switch (thisType) {
    case ENC_TYPE_WEP:
      Serial.print("WEP");
      break;
    case ENC_TYPE_WPA_PSK:
      Serial.print("WPA_PSK");
      break;
    case ENC_TYPE_WPA2_PSK:
      Serial.print("WPA2_PSK");
      break;
    case ENC_TYPE_WPA_WPA2_PSK:
      Serial.print("WPA_WPA2_PSK");
      break;
    case ENC_TYPE_NONE:
      Serial.print("None");
      break;
  }
  Serial.println();
}

