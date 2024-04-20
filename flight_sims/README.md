# airbrakes-prelim-analysis

Flight and airbrakes simulations, analysis of Prometheus' flight data

## Giorgio's Ideas
- convert these to issues. I don't want to keep comitting every time I have an idea. Also this keeps getting out of date because I have my ideas in several different places

- **Alignment of Sim Data with Experimental Data:** 
  - About 1000 ft off around motor burnout.
  - try taking data to motor burnout and simulating remainder of flight to see congruence with experimental data
    - just run sim as is and set deployment angle to 0 for the entire flight
  - this isn't a real problem; it's caused by the delay in barometric sensor data. The rocket should have been just about where the sim says it would be at motor burnout, it's just the ~1 second delay in the pressure in the rocket getting to the pressure outside the rocket that causes the discrepancy.

- **ORK Underestimation of Drag:** 
  - Others are also experiencing underestimation of drag in their OpenRocket simulations: [Discord Discussion](https://discord.com/channels/855522432945618965/855533557996453888/1017453223340150805)

- **Evaluating the Impact of Weathercocking:** 
  - Investigation: Determine the rough magnitude of change caused by weathercocking.
  - Focus: Is it a function of stability in tube calibers?