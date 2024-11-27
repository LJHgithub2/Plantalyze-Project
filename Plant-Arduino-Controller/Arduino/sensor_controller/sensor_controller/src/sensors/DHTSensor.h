#ifndef DHTSENSOR_H
#define DHTSENSOR_H

#include <DHT.h>

class DHTSensor {
public:
    DHTSensor(int pin, int type);
    void begin();
    float getTemperature();
    float getHumidity();

private:
    DHT dht;
};

#endif
