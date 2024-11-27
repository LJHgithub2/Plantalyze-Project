#include "SensorManager.h"
#include <Arduino.h>

// Constructor
SensorManager::SensorManager(int dhtPin, int dhtType, int soilPin, int cdsPin)
    : dht(dhtPin, dhtType), soil(soilPin), cds(cdsPin) {}

// Initializes all sensors
void SensorManager::begin() {
    dht.begin();  // Initialize DHT sensor
    soil.begin();
    cds.begin();
}

// Reads temperature from DHT sensor
float SensorManager::getTemperature() {
    return dht.getTemperature();
}

// Reads humidity from DHT sensor
float SensorManager::getHumidity() {
    return dht.getHumidity();
}

// Reads light level from light sensor
float SensorManager::getLightLevel() {
    int lightVal = cds.getLightLevel();
    return lightVal; // Convert to percentage
}

// Reads soil moisture level from soil sensor
float SensorManager::getSoilMoisture() {
    int soilVal = soil.getSoilMoisture();
    return (soilVal / 1023.0) * 100.0; // Convert to percentage
}

// Prints all sensor readings to the serial monitor
void SensorManager::printAll() {
    Serial.println("---------------------");
    Serial.print("Temperature: ");
    Serial.print(getTemperature());
    Serial.println(" °C");

    Serial.print("Humidity: ");
    Serial.print(getHumidity());
    Serial.println(" %");

    Serial.print("Light Level: ");
    Serial.print(getLightLevel());
    Serial.println();

    Serial.print("Soil Moisture: ");
    Serial.print(getSoilMoisture());
    Serial.println(" %");

    Serial.println("---------------------");
}
