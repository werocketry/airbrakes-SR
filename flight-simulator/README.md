# airbrakes-prelim-analysis

Flight and airbrakes simulation, analysis of Prometheus' flight data

## Giorgio's Ideas

- **Alignment of Sim Data with Experimental Data:** 
  - About 1000 ft off around motor burnout.
  - try again with redone final Prometheus CFD, possibly check dry mass too
  - try taking data to motor burnout and simulating remainder of flight to see congruence with experimental data
    - just run sim as is and set deployment angle to 0 for the entire flight
  - think about other ways to/what would align sim data with experimental data if above doesn't work

- **Underestimation of Drag in Other Projects:** 
  - Observation: Other people are also experiencing underestimation of drag in their simulations.
  - Reference: [Discord Discussion](https://discord.com/channels/855522432945618965/855533557996453888/1017453223340150805).

- **Impact of Horizontal Velocity on Apogee Change Due to Airbrakes:** 
  - If actually wanting to simulate airbrakes on Prometheus using experimental data as the data till burnout, note that flight data has no vertical vs horizontal velocity data, so would need to use the speed and change of height with time to separate them out. Possibly use the velocity not being 0/the acceleration not being -g at apogee to help determine the horizontal motion

- **Useful Resources and Repositories:**
  - [ORBrake Repository](https://github.com/WPI-HPRC/ORBrake)
  - [RocketPy](https://github.com/RocketPy-Team/RocketPy)

- **Determining Landing Location and Animation:**
  - Goal: Determine how far from the launchpad the rocket lands.
  - Additional Idea: Create an animation of the flight for fun.

- **Incorporating Wind Effects:** 
  - Task: Add wind effects into the simulation.
  - Method: Perform CFD (Computational Fluid Dynamics) analysis under varying wind conditions to observe changes in the drag profile.

- **Simulation Use in Control Systems:**
  - Query: Explore the possibility of using the simulation on the controller.
  - Action: Consult with Cam for detailed requirements at specific waypoints.

- **Evaluating the Impact of Weathercocking:** 
  - Investigation: Determine the rough magnitude of change caused by weathercocking.
  - Focus: Is it a function of stability in tube calibers?