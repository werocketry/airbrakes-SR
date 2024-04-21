# Flight Analysis

Flight simulations, analysis of Prometheus' flight data

- **Alignment of Sim Data with Experimental Data:** 
  - About 1000 ft off around motor burnout.
  - try taking data to motor burnout and simulating remainder of flight to see congruence with experimental data
    - just run sim as is and set deployment angle to 0 for the entire flight
  - this isn't a real problem; it's caused by the delay in barometric sensor data. The rocket should have been just about where the sim says it would be at motor burnout, it's just the ~1 second delay in the pressure in the rocket getting to the pressure outside the rocket that causes the discrepancy.
