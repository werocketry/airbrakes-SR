import numpy as np
import constants as con
import rocket_classes as rktClass
import flight_simulation as fsim
import helper_functions as hfunc
from configs import Hyperion, current_airbrakes_model, Prometheus_launch_conditions

# should I be siming with different Cds?

"""
launch angles: 5 7 9 11 13 15
sim with them and normal other conditions up to burnout
additional burnout states at +/- 5%, 10%, 15%, 20%, and 25% of height, speed
calcs on those of what specific angle would need to be maintained to hit 10k
"""

# extract launch conditions
launchpad_pressure = Prometheus_launch_conditions.launchpad_pressure
launchpad_temp = Prometheus_launch_conditions.launchpad_temp
L_launch_rail = Prometheus_launch_conditions.L_launch_rail
launch_angles = [85, 83, 81, 79, 77, 75]

# create a list of possible motor burnout states
burnout_states = []
for launch_angle in launch_angles:
    launch_conditions = rktClass.LaunchConditions(launchpad_pressure, launchpad_temp, L_launch_rail, launch_angle)
    dataset, _, _, burnout_index, _ = fsim.simulate_flight(rocket=Hyperion, timestep=0.001, launch_conditions=launch_conditions)
    burnout_states.append(dataset.iloc[burnout_index].copy())

print(burnout_states[0])

# add additional burnout states at +/- 5%, 10%, 15%, 20%, and 25% of height, speed
    # better ways to do this, but just want a first attempt
for i in range(len(launch_angles)):
    burnout_state = burnout_states[i]
    for j in range(1, 6):
        burnout_state_copy = burnout_state.copy()
        burnout_state_copy["height"] *= 1 + j * 0.05
        burnout_state_copy["speed"] *= 1 + j * 0.05
        burnout_state_copy["v_x"] *= 1 + j * 0.05
        burnout_state_copy["v_y"] *= 1 + j * 0.05
        burnout_state_copy["angle_to_vertical"] = np.arctan(burnout_state_copy["v_x"] / burnout_state_copy["v_y"])
        burnout_states.append(burnout_state_copy)
        burnout_state_copy = burnout_state.copy()
        burnout_state_copy["height"] *= 1 - j * 0.05
        burnout_state_copy["speed"] *= 1 - j * 0.05
        burnout_state_copy["v_x"] *= 1 - j * 0.05
        burnout_state_copy["v_y"] *= 1 - j * 0.05
        burnout_state_copy["angle_to_vertical"] = np.arctan(burnout_state_copy["v_x"] / burnout_state_copy["v_y"])
        burnout_states.append(burnout_state_copy)

# order them by height
burnout_states = sorted(burnout_states, key=lambda x: x["height"])

# plot height and speed of different burnout states at burnout
import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
colors = ['b', 'g', 'r', 'c', 'm', 'y']  # Add more colors if needed
labels = []
for i in range(len(burnout_states)):
    burnout_state = burnout_states[i]
    launch_angle = launch_angles[i % len(launch_angles)]
    if launch_angle not in labels:
        labels.append(launch_angle)
        axs[0].scatter(i, burnout_state["height"], color=colors[i % len(colors)], label=f'launch angle = {launch_angle} deg')
        axs[1].scatter(i, burnout_state["speed"], color=colors[i % len(colors)], label=f'launch angle = {launch_angle} deg')
    else:
        axs[0].scatter(i, burnout_state["height"], color=colors[i % len(colors)])
        axs[1].scatter(i, burnout_state["speed"], color=colors[i % len(colors)])
axs[0].set_title("Height at burnout")
axs[0].set_xlabel("Burnout state")
axs[0].set_ylabel("Height (m)")
axs[0].legend()
axs[1].set_title("Speed at burnout")
axs[1].set_xlabel("Burnout state")
axs[1].set_ylabel("Speed (m/s)")
axs[1].legend()
plt.show()

# calculate the angle needed to hit 10k
