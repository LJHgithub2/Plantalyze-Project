#include <DHT.h>
#define SOILPIN A1
#define DHTPIN A2
#define CDSPIN A3
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  //1023(수분 없을때)  - 0 (수분 많을때)
  int Soil_moisture = analogRead(SOILPIN);  
  //0(빛이 완전 강할때) - 800(빛이 많을때) - 1000(빛이 없을때)
  int CDS_value = analogRead(CDSPIN);
  int h = dht.readHumidity();
  int t = dht.readTemperature();
  Serial.print("CDS_value: ");
  Serial.println(CDS_value);    
  Serial.print("Soil_moisture: ");
  Serial.println(Soil_moisture);    
  Serial.print("humidity: ");
  Serial.println(h);
  Serial.print("tempperature: ");
  Serial.println(t);    
  delay(1000); // 0.1초
}
