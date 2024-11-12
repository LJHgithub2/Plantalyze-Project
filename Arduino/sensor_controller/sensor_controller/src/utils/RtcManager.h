#ifndef RTC_MANAGER_H
#define RTC_MANAGER_H

#include <Wire.h>
#include <RtcDS1307.h>

class RtcManager {
public:
    RtcManager();
    void initialize();
    void updateDateTime();
    void printDateTime(const RtcDateTime& dt);

private:
    RtcDS1307<TwoWire> rtc;
};

#endif
