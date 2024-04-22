import numpy as np
import pandas as pd
import constants as con
import rocket_classes as rktClass
import flight_simulation as fsim
import helper_functions as hfunc
from configs import Hyperion, current_airbrakes_model, Prometheus_launch_conditions
import controller_flight_simulator as cfsim
# should I be siming with different Cds?

"""
launch angles: 5 7 9 11 13 15
sim with them and normal other conditions up to burnout
additional burnout states at: +/- np.linspace(0.01, 0.25, 25) * burnout_state of height, speed
    better ways to do this, but just want a first attempt
calcs on those of what specific angle would need to be maintained to hit 10k
"""

# extract launch conditions
launchpad_pressure = Prometheus_launch_conditions.launchpad_pressure
launchpad_temp = Prometheus_launch_conditions.launchpad_temp + 273.15
L_launch_rail = Prometheus_launch_conditions.L_launch_rail
launch_angles = [85, 83, 81, 79, 77, 75]

# create a list of possible motor burnout states
burnout_states = []
for launch_angle in launch_angles:
    launch_conditions = rktClass.LaunchConditions(launchpad_pressure, launchpad_temp, L_launch_rail, launch_angle)
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

# calculate the angles needed to hit 10k
multiplier = launchpad_pressure / (con.R_specific_air * pow(launchpad_temp, con.F_g_over_R_spec_air_T_lapse_rate))

deployment_angles = []
tracker = 0

for burnout_state in burnout_states:
    apogee_no_braking = cfsim.simulate_airbrakes_flight(burnout_state["height"], burnout_state["speed"], burnout_state["v_y"], burnout_state["v_x"], launchpad_temp, multiplier, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=0, timestep=0.01)
    if apogee_no_braking * 3.28084 < 10000:
        deployment_angles.append(0)
        tracker += 1
        print(f'{tracker} of {len(burnout_states)} deployment angles found')
    else:
        apogee_max_braking = cfsim.simulate_airbrakes_flight(burnout_state["height"], burnout_state["speed"], burnout_state["v_y"], burnout_state["v_x"], launchpad_temp, multiplier, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=np.pi / 4, timestep=0.01)
        if apogee_max_braking * 3.28084 > 10000:
            deployment_angles.append(np.pi / 4)
            tracker += 1
            print(f'{tracker} of {len(burnout_states)} deployment angles found')
        else:
            lower_bound = 0
            upper_bound = np.pi / 4
            while upper_bound - lower_bound > 0.0001:
                deployment_angle = (upper_bound + lower_bound) / 2
                apogee = cfsim.simulate_airbrakes_flight(burnout_state["height"], burnout_state["speed"], burnout_state["v_y"], burnout_state["v_x"], launchpad_temp, multiplier, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=deployment_angle, timestep=0.01)
                if apogee * 3.28084 > 10000:
                    lower_bound = deployment_angle
                else:
                    upper_bound = deployment_angle
            deployment_angles.append(deployment_angle)
            tracker += 1
            print(f'{tracker} of {len(burnout_states)} deployment angles found')

# plot the deployment angles
plt.scatter(range(len(deployment_angles)), np.rad2deg(deployment_angles))
plt.title("Deployment angles needed to hit 10k")
plt.xlabel("Burnout state")
plt.ylabel("Deployment angle (degrees)")
plt.show()

# save to a csv
for i in range(len(deployment_angles)):
    burnout_states[i]["deployment_angle_needed"] = deployment_angles[i]

burnout_states_df = pd.DataFrame(burnout_states)
burnout_states_df.drop(columns=["a_y", "a_x", "temperature","air_density","q"], inplace=True)
burnout_states_df.to_csv("flight-simulator/lookup-tables/burnout_states.csv", index=False)