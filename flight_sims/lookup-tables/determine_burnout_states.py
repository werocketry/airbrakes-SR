"""
Start with:
    - v_z = np.linspace(200, 400, 10)
    - height = np.linspace(300, 600, 25)

Note, no need to make lookups for burnout states faster/higher than 0 drag theoretical max. Use that for upper limit, and construct table for heights and speeds below height and speed of that state.

Use a sensitivity analysis to determine plausible burnout states for the rocket: 
    - Motor total impulse: +/- 5%
    - C_d: +/- 10%
    - launch angle: +/- 3 degrees if not able to determine before launch
    - temps, pressures, etc can be fed in with the forecasted values right before launch
"""

import numpy as np
import pandas as pd
from rocketflightsim import constants as con
from rocketflightsim import rocket_classes
from rocketflightsim import flight_simulation as fsim
from rocketflightsim import helper_functions as hfunc
from configs import Hyperion, Hyperion_launch_conditions

# NOTE FROM RIGHT BEFORE HYPERION LAUNCH: this should be done properly in future years for the sake of completeness, but decent granularity and +/- 15% on hieght and speed at burnout is way more than the rocket will ever experience if it isn't in the middle of a CATO

num_sims = 100

mean_launchpad_temp = Hyperion_launch_conditions.launchpad_temp
std_launchpad_temp = 7
mean_launchpad_pressure = Hyperion_launch_conditions.launchpad_pressure
std_launchpad_pressure = 500
mean_rocket_mass = Hyperion.rocket_mass
std_rocket_mass = 3 # not that this is expected, but it should account for much more than the variation that unforseen error sources could cause

burnout_states = []
for i in range(num_sims):
    
    launch_condition = rocket_classes.LaunchConditions(
        launchpad_pressure = np.random.normal(mean_launchpad_pressure, std_launchpad_pressure),
        launchpad_temp = np.random.normal(mean_launchpad_temp, std_launchpad_temp),
        L_launch_rail=Hyperion_launch_conditions.L_launch_rail,
        launch_rail_elevation=Hyperion_launch_conditions.launch_rail_elevation,
        # add wind?
        local_T_lapse_rate=Hyperion_launch_conditions.local_T_lapse_rate,
        local_gravity=Hyperion_launch_conditions.local_gravity,
    )
    
    rocket_mass = np.random.normal(mean_rocket_mass, std_rocket_mass)
    rocket = rocket_classes.Rocket(
        rocket_mass,
        Hyperion.motor,
        Hyperion.A_rocket,
        Hyperion.Cd_rocket_at_Ma,
        Hyperion.h_second_rail_button
    )
    dataset, _, _, burnout_index, _ = fsim.simulate_flight(rocket=Hyperion, timestep=0.001, launch_conditions=launch_condition)
    burnout_states.append(dataset.iloc[burnout_index].copy())

    if i % 5 == 0:
        print(i)

burnout_states = sorted(burnout_states, key=lambda x: x["height"])









"""
launch angles: 5 7 9 11 13 15
sim with them and normal other conditions up to burnout
additional burnout states at: +/- np.linspace(0.01, 0.25, 25) * burnout_state of height, speed
    better ways to do this, but just want a first attempt
"""

# # extract launch conditions
# launchpad_pressure = Spaceport_America_avg_launch_conditions.launchpad_pressure
# launchpad_temp = Spaceport_America_avg_launch_conditions.launchpad_temp
# L_launch_rail = Spaceport_America_avg_launch_conditions.L_launch_rail
# launch_rail_elevations = [85, 83, 81, 79, 77, 75]

# # create a list of possible motor burnout states
# burnout_states = []
# for launch_rail_elevation in launch_rail_elevations:
#     launch_conditions = rocket_classes.LaunchConditions(launchpad_pressure, launchpad_temp, L_launch_rail, launch_rail_elevation)
#     dataset, _, _, burnout_index, _ = fsim.simulate_flight(rocket=Hyperion, timestep=0.001, launch_conditions=launch_conditions)
#     burnout_states.append(dataset.iloc[burnout_index].copy())

# # add additional burnout states
# for i in range(len(launch_rail_elevations)):
#     burnout_state = burnout_states[i]
#     for j in range(1, 25):
#         burnout_state_copy = burnout_state.copy()
#         burnout_state_copy["height"] *= 1 + j * 0.01
#         burnout_state_copy["speed"] *= 1 + j * 0.01
#         burnout_state_copy["v_x"] *= 1 + j * 0.01
#         burnout_state_copy["v_y"] *= 1 + j * 0.01
#         burnout_state_copy["angle_to_vertical"] = np.arctan(burnout_state_copy["v_x"] / burnout_state_copy["v_y"])
#         burnout_states.append(burnout_state_copy)
#         burnout_state_copy = burnout_state.copy()
#         burnout_state_copy["height"] *= 1 - j * 0.01
#         burnout_state_copy["speed"] *= 1 - j * 0.01
#         burnout_state_copy["v_x"] *= 1 - j * 0.01
#         burnout_state_copy["v_y"] *= 1 - j * 0.01
#         burnout_state_copy["angle_to_vertical"] = np.arctan(burnout_state_copy["v_x"] / burnout_state_copy["v_y"])
#         burnout_states.append(burnout_state_copy)

# # order them by height
# burnout_states = sorted(burnout_states, key=lambda x: x["height"])

# plot height and speed of different burnout states at burnout
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 1, figsize=(10, 10))

for i in range(len(burnout_states)):
    burnout_state = burnout_states[i]
    axs[0].scatter(i, burnout_state["height"], color='b')
    axs[1].scatter(i, burnout_state["v_z"], color='b')

axs[0].set_title("Height at burnout")
axs[0].set_xlabel("Burnout state")
axs[0].set_ylabel("Height (m)")

axs[1].set_title("Vertical velocity at burnout")
axs[1].set_xlabel("Burnout state")
axs[1].set_ylabel("Vertical velocity (m/s)")

plt.show()
