#include "LightSensor.h"
#include <Arduino.h>

LightSensor::LightSensor(int pin) : pin(pin) {}

void LightSensor::begin() {
    pinMode(pin, INPUT);
}

int LightSensor::getLightLevel() {
    return analogRead(pin);
}
