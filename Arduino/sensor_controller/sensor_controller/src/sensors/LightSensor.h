#ifndef LIGHTSENSOR_H
#define LIGHTSENSOR_H

class LightSensor {
public:
    LightSensor(int pin);
    int getLightLevel();

private:
    int pin;
};

#endif
