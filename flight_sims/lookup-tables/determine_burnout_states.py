"""
Start with:
    - v_y = np.linspace(200, 400, 10)
    - height = np.linspace(300, 600, 25)

Note, no need to make lookups for burnout states faster/higher than 0 drag theoretical max. Use that for upper limit, and construct table for heights and speeds below height and speed of that state.

Use a sensitivity analysis to determine plausible burnout states for the rocket: 
    - Motor total impulse: +/- 5%
    - C_d: +/- 10%
    - launch angle: +/- 3 degrees if not able to determine before launch
    - temps, pressures, etc can be fed in with the forecasted values right before launch

Old code below:
"""

import numpy as np
import pandas as pd
from rocketflightsim import constants as con
from rocketflightsim import rocket_classes
from rocketflightsim import flight_simulation as fsim
from rocketflightsim import helper_functions as hfunc
from configs import Hyperion, Spaceport_America_avg_launch_conditions

"""
launch angles: 5 7 9 11 13 15
sim with them and normal other conditions up to burnout
additional burnout states at: +/- np.linspace(0.01, 0.25, 25) * burnout_state of height, speed
    better ways to do this, but just want a first attempt
"""

# extract launch conditions
launchpad_pressure = Spaceport_America_avg_launch_conditions.launchpad_pressure
launchpad_temp = Spaceport_America_avg_launch_conditions.launchpad_temp
L_launch_rail = Spaceport_America_avg_launch_conditions.L_launch_rail
launch_angles = [85, 83, 81, 79, 77, 75]

# create a list of possible motor burnout states
burnout_states = []
for launch_angle in launch_angles:
    launch_conditions = rocket_classes.LaunchConditions(launchpad_pressure, launchpad_temp, L_launch_rail, launch_angle)
    dataset, _, _, burnout_index, _ = fsim.simulate_flight(rocket=Hyperion, timestep=0.001, launch_conditions=launch_conditions)
    burnout_states.append(dataset.iloc[burnout_index].copy())

# add additional burnout states
for i in range(len(launch_angles)):
    burnout_state = burnout_states[i]
    for j in range(1, 25):
        burnout_state_copy = burnout_state.copy()
        burnout_state_copy["height"] *= 1 + j * 0.01
        burnout_state_copy["speed"] *= 1 + j * 0.01
        burnout_state_copy["v_x"] *= 1 + j * 0.01
        burnout_state_copy["v_y"] *= 1 + j * 0.01
        burnout_state_copy["angle_to_vertical"] = np.arctan(burnout_state_copy["v_x"] / burnout_state_copy["v_y"])
        burnout_states.append(burnout_state_copy)
        burnout_state_copy = burnout_state.copy()
        burnout_state_copy["height"] *= 1 - j * 0.01
        burnout_state_copy["speed"] *= 1 - j * 0.01
        burnout_state_copy["v_x"] *= 1 - j * 0.01
        burnout_state_copy["v_y"] *= 1 - j * 0.01
        burnout_state_copy["angle_to_vertical"] = np.arctan(burnout_state_copy["v_x"] / burnout_state_copy["v_y"])
        burnout_states.append(burnout_state_copy)

# order them by height
burnout_states = sorted(burnout_states, key=lambda x: x["height"])

# plot height and speed of different burnout states at burnout
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 1, figsize=(10, 10))

for i in range(len(burnout_states)):
    burnout_state = burnout_states[i]
    axs[0].scatter(i, burnout_state["height"], color='b')
    axs[1].scatter(i, burnout_state["v_y"], color='b')

axs[0].set_title("Height at burnout")
axs[0].set_xlabel("Burnout state")
axs[0].set_ylabel("Height (m)")

axs[1].set_title("Vertical velocity at burnout")
axs[1].set_xlabel("Burnout state")
axs[1].set_ylabel("Vertical velocity (m/s)")

plt.show()
