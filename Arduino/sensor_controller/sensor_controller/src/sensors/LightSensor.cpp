#include "LightSensor.h"
#include <Arduino.h>

LightSensor::LightSensor(int pin) : pin(pin) {}

int LightSensor::getLightLevel() {
    return analogRead(pin);
}
