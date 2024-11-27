#include "SoilMoistureSensor.h"
#include <Arduino.h>

SoilMoistureSensor::SoilMoistureSensor(int pin) : pin(pin) {}

void SoilMoistureSensor::begin() {
    pinMode(pin, INPUT);   // Set light sensor pin as input
}

int SoilMoistureSensor::getSoilMoisture() {
    return analogRead(pin);
}
