# airbrakes-prelim-analysis

Analysis of Prometheus' flight data, flight simulation, and simplified airbrakes

## Giorgio's Ideas

- **Flight/Sim Main Differences in First 4/5 Seconds:** About 1000 ft off around motor burnout.

- **Simulating Prometheus Data Without Airbrakes Deployment:** 
  - Idea: Add an option to simulate Prometheus data from motor burnout without airbrakes deployment. 
  - Implementation: Set deployment angle to 0 for the entire flight.

- **Alignment of Sim Data with Experimental Data:** 
  - Objective: Make the simulation data converge towards the experimental data. 
  - Approach: Implement rotation (clockwise) adjustments.

- **Underestimation of Drag in Other Projects:** 
  - Observation: Other people are also experiencing underestimation of drag in their simulations.
  - Reference: [Discord Discussion](https://discord.com/channels/855522432945618965/855533557996453888/1017453223340150805).

- **Impact of Horizontal Velocity on Apogee Change Due to Airbrakes:** 
  - Hypothesis: The horizontal velocity significantly affects the apogee change, more than initially expected, due to airbrakes.

- **Utilizing Experimental Data for Horizontal Motion Analysis:** 
  - Focus: For the experimental datasets, consider the velocity not being 0 and the acceleration not being -g at apogee.
  - Purpose: This could be key in understanding the horizontal motion.

- **Useful Resources and Repositories:**
  - [ORBrake Repository](https://github.com/WPI-HPRC/ORBrake)
  - [RocketPy Branch with Air Brakes](https://github.com/RocketPy-Team/RocketPy/tree/enh/air-brakes)

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
  - Focus: Relate this to the function of stability in tube calibers.
