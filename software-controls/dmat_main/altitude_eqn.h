// altitude_eqn.h

#ifndef ALTITUDE_EQN_H
#define ALTITUDE_EQN_H

#include <math.h>

class AltitudeEquation {
public:
    // Convert pressure in millibars to altitude in meters
    static float pressureToAltitudeMeters(float pressureMillibars) {
        // Calculate altitude in feet first
        float altitudeFeet = (1 - pow(pressureMillibars / 1013.25, 0.190284)) * 145366.45;
        // Convert feet to meters
        return altitudeFeet * 0.3048;
    }
};

#endif // ALTITUDE_EQN_H
