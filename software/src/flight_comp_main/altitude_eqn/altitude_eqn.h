// altitude_eqn.h

#ifndef ALTITUDE_EQN_H
#define ALTITUDE_EQN_H

#include <math.h>
// Source: https://www.weather.gov/media/epz/wxcalc/pressureAltitude.pdf

class AltBaro {
private:
    float currentPressureMillibars = 1013.25; // Default to sea level standard atmospheric pressure

public:
    AltBaro() {}

    // Update the current pressure
    void update(float pressureMillibars) {
        currentPressureMillibars = pressureMillibars;
    }

    // Get the current altitude in meters based on the latest pressure update
    float getAltitude() const {
        // Calculate altitude in feet first
        float altitudeFeet = (1 - pow(currentPressureMillibars / 1013.25, 0.190284)) * 145366.45;
        // Convert feet to meters
        return altitudeFeet * 0.3048;
    }
};

#endif // ALTITUDE_EQN_H
