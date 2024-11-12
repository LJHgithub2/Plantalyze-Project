#include "SoilMoistureSensor.h"
#include <Arduino.h>
SoilMoistureSensor::SoilMoistureSensor(int pin) : pin(pin) {}
int SoilMoistureSensor::getSoilMoisture() {
    return analogRead(pin);
}
