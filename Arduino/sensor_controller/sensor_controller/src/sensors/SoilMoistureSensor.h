#ifndef SOILMOISTURESENSOR_H
#define SOILMOISTURESENSOR_H

class SoilMoistureSensor {
public:
    SoilMoistureSensor(int pin);
    int getSoilMoisture();

private:
    int pin;
};
#endif
