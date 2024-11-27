#ifndef SENSORMANAGER_H
#define SENSORMANAGER_H

#include "DHTSensor.h"
#include "LightSensor.h"
#include "SoilMoistureSensor.h"

class SensorManager {
public:
    // Constructor
    SensorManager(int dhtPin, int dhtType, int soilPin, int cdsPin);

    // Initializes all sensors
    void begin();

    // Sensor reading methods
    float getTemperature();
    float getHumidity();
    float getLightLevel();
    float getSoilMoisture();

    // Prints all sensor readings to the serial monitor
    void printAll();

private:
    DHTSensor dht;               // DHT sensor object
    SoilMoistureSensor soil;       // Soil moisture sensor pin
    LightSensor cds;        // Light sensor pin
};

#endif
