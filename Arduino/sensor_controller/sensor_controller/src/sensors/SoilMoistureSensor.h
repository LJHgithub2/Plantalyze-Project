#ifndef SOILMOISTURESENSOR_H
#define SOILMOISTURESENSOR_H

class SoilMoistureSensor {
public:
    SoilMoistureSensor(int pin);
    void begin();
    int getSoilMoisture();

private:
    int pin;
};
#endif
