#include "DHTSensor.h"

DHTSensor::DHTSensor(int pin, int type) : dht(pin, type) {}

void DHTSensor::begin() {
    dht.begin();
}

float DHTSensor::getTemperature() {
    return dht.readTemperature();
}

float DHTSensor::getHumidity() {
    return dht.readHumidity();
}
