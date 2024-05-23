# Flight Analysis

Flight simulations, analysis of Prometheus' flight data

- **Alignment of Sim Data with Experimental Data:** 
  - About 1000 ft off around motor burnout.
  - try taking data to motor burnout and simulating remainder of flight to see congruence with experimental data
    - just run sim as is and set deployment angle to 0 for the entire flight
  - this isn't a real problem; it's caused by the delay in barometric sensor data. The rocket should have been just about where the sim says it would be at motor burnout, it's just a delay on the order of 0.8s in the pressure in the rocket getting to equilibrate with the pressure outside the rocket that causes the discrepancy.
  - Note that if wanting to simulate airbrakes using Prometheus experimental data as the data till burnout, the flight data has no vertical vs horizontal velocity data, so would need to use the speed and change of height with time to separate them out. Possibly use the velocity not being 0/the acceleration not being -g at apogee to help determine the horizontal motion then too. Not a priority at all.
