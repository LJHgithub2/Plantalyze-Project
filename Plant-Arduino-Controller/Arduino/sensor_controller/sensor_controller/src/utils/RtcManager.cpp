#include "RtcManager.h"

RtcManager::RtcManager() : rtc(Wire) {}

void RtcManager::initialize() 
{
    Serial.print("compiled: ");
    Serial.print(__DATE__);
    Serial.println(__TIME__);

    rtc.Begin();

    RtcDateTime compiled = RtcDateTime(__DATE__, __TIME__);
    printDateTime(compiled);
    Serial.println();

    if (!rtc.IsDateTimeValid()) 
    {
        if (rtc.LastError() != 0)
        {
            Serial.print("RTC communications error = ");
            Serial.println(rtc.LastError());
        }
        else
        {
            Serial.println("RTC lost confidence in the DateTime!");
            rtc.SetDateTime(compiled);
        }
    }

    if (!rtc.GetIsRunning())
    {
        Serial.println("RTC was not actively running, starting now");
        rtc.SetIsRunning(true);
    }

    RtcDateTime now = rtc.GetDateTime();
    if (now < compiled) 
    {
        Serial.println("RTC is older than compile time!  (Updating DateTime)");
        rtc.SetDateTime(compiled);
    }
    else if (now > compiled) 
    {
        Serial.println("RTC is newer than compile time. (this is expected)");
    }
    else if (now == compiled) 
    {
        Serial.println("RTC is the same as compile time! (not expected but all is fine)");
    }

    rtc.SetSquareWavePin(DS1307SquareWaveOut_Low);
}

void RtcManager::updateDateTime()
{
    if (!rtc.IsDateTimeValid()) 
    {
        if (rtc.LastError() != 0)
        {
            Serial.print("RTC communications error = ");
            Serial.println(rtc.LastError());
        }
        else
        {
            Serial.println("RTC lost confidence in the DateTime!");
        }
    }

    RtcDateTime now = rtc.GetDateTime();
    printDateTime(now);
    Serial.println();
}

void RtcManager::printDateTime(const RtcDateTime& dt)
{
    char datestring[20];
    snprintf_P(datestring, 
               sizeof(datestring),
               PSTR("%02u/%02u/%04u %02u:%02u:%02u"),
               dt.Month(),
               dt.Day(),
               dt.Year(),
               dt.Hour(),
               dt.Minute(),
               dt.Second() );
    Serial.print(datestring);
}
