"""New:
- use real simulator instead of controller simulator
- table with height and vertical velocity at burnout
    - each entry in the table is a function that outputs deployment angle as a function of height for a flightpath reaching 10k (function will be a series of points)
        - choose paths that are the most resistant to changes expected via Monte Carlo
            - if highly sensitive to another variable, a third dimension could be added to the table
    - controller will use PID ontop of this to adjust for errors in deployment angle, trying to keep the flightpath as close as possible to that of the flightpath specified by the function chosen at burnout
    - incorporate having the brakes closed for apogee into the recommended flightpaths
        - t_to_apogee_min = v_y / a_y
        - minimum time to apogee is if the current drag force remains all the way to apogee. Currently compared to time needed to close airbrakes completely if they're fully deployed
        - t_to_apogee_max = v_y / F_gravity
        - now doing it with this method, can just check at each timestep (after some cutoff) if the breaks need to be closed more to get closed for apogee, don't need efficiency anymore. Can also use extra small timesteps now
- things to update closer to launch (incomplete list):
    - temperature at launchpad
        - launchpad temperature could be something fed into it at the start of the day based on forecast temps at different times, and then it picks the one that is closest to the current time, as temp inside the rocket could vary from the outside 
    - pressure at launchpad
    - rocket mass
    - loaded motor mass
    - launch angle would be great to have, maybe ask during initial safety if there's a way to find out about what it would be for our rocket
        - could this and launch direction be found out day-of? Could make a series of tables for different launch angles and directions earlier in the day, then choose the one that is closest to the actual launch conditions to plug into the flight controller
        - https://www.herox.com/SpaceportAmericaCup2024/forum/thread/11118
    - wind
    - launch direction
- ask Cam granularity of the lookup tables the controller can handle. every m in height and every m/s in vertical velocity at burnout?
- how to deal with angle to vertical? 
- wait for now, but look into simulating with different Cd curves

- remember that increasing drag increases proportionally less drag in the vertical direction as the angle to vertical increases
"""

import numpy as np
import pandas as pd
from rocketflightsim import constants as con
from rocketflightsim import rocket_classes
from rocketflightsim import flight_simulation as fsim
from rocketflightsim import helper_functions as hfunc
from configs import Hyperion, current_airbrakes_model, Spaceport_America_avg_launch_conditions

# step 1: use determine_burnout_states.py to get the burnout states
"""for now, just use:
    - v_ys_at_burnout = np.linspace(200, 400, 10)
    - heights_at_burnout = np.linspace(300, 600, 25)
    - launch conditions: Spaceport_America_avg_launch_conditions
With the above:
    time → don't care about initial, set to 0
    height → given
    speed → function of v_x, v_y
    a_y → can be calculated from angle to vertical, q, rocket parameters, environmental parameters
    a_x → can be calculated from angle to vertical, q, rocket parameters, environmental parameters
    v_y → given
    v_x → for now, take as 10% of v_y
    temperature → function of height, launch conditions
    air_density → function of height, launch conditions
    q → function of speed, air_density
    Ma → function of speed, temperature
    angle_to_vertical → function of v_x, v_y (and later, v_wind)
"""

# step 2: define a function that will return the flightpath for a given burnout state by choosing deployment angles needed to hit 10k. 
""" Definition of the function:
- input: height
- output: deployment angle
- ideal function will be the one that:
    - ideally doesn't get too close to the max deployment angle
    - is closed a bit before apogee
    - is the most resistant to changes in launch conditions and total impulse (cap effect of changes in total impulse to a reasonable maximum plausible)
"""
""" Properties of the function:
- f(h = h_0) = 0
    - airbrakes are closed at burnout
- f(h = 10 000) = 0
    - airbrakes are closed at apogee
- max(f(h)) = 40 degrees
    - keep the airbrakes from deploying too far. This could be played with slightly, but stick with this for now
- min(f(h)) = 0 degrees
    - airbrakes can't have negative deployment angles
- f(h) is continuous
    - airbrakes can't deploy or retract instantly
- max(f'(t)) = airbrakes.max_deployment_rate
    - airbrakes can't deploy faster than their max rate
        - this could be played with, but stick with this for now
- min(f'(t)) = -airbrakes.max_retraction_rate
    - airbrakes can't retract faster than their max rate
"""
""" Other constraints:
h'(h = 10 000) = 0
    - apogee occurs at 10k
If want more, can add things like must be increasing then one switch to non-increasing
"""

v_y = 280
height_initial = 440
airbrakes = current_airbrakes_model
tenkft_in_m = 10000/3.28084

from rocketflightsim.flight_simulation import simulate_airbrakes_flight_deployment_function_of_height

# def deployment_fn(h): 
#     return 0.75 * np.deg2rad(airbrakes.max_deployment_angle) * np.sin(np.pi * (h - height_initial) / (tenkft_in_m - height_initial))

"""
1) Get time to apogee without airbrake deployment, discretize time space, map to height space
2) Define in time space, respecting deployment rates plus some margin
3) Switch to height space to make the next sim
4) Run sim, get new time to apogee, make adjustments to deployment function, repeat 2-4
"""

# 1
def deployment_fn_null(h): return 0
ascent = simulate_airbrakes_flight_deployment_function_of_height(
    [height_initial, v_y, v_y * 0.1],
    Hyperion,
    Spaceport_America_avg_launch_conditions,
    airbrakes,
    deployment_fn_null
)
t_to_apogee = ascent["time"].iloc[-1]

num_iterations = 10
num_intervals = 100
deployment_function_values = np.zeros(num_intervals)
for i in range(num_iterations):
    time_intervals = np.linspace(0, t_to_apogee, num_intervals) # switch to some kind of altered log space?
    
    # use ascent["height"] to map times to heights
    height_intervals = [height_initial]
    for j in range(1, num_intervals):
        height_intervals.append(ascent["height"].iloc[ascent["time"].sub(time_intervals[i]).abs().idxmin()])

    # # plot height_intervals to see if it's working
    # import matplotlib.pyplot as plt
    # plt.plot(ascent["time"], ascent["height"])
    # print(time_intervals[0:5])
    # print(height_intervals[0:5])
    # plt.scatter(time_intervals, height_intervals)
    # plt.show()

    def deployment_fn_simulator(h):
        # index is which interval the height h is in in the height_intervals list
        index = min(range(len(height_intervals)), key=lambda i: abs(height_intervals[i]-h))
        return deployment_function_values[index]

    ascent = simulate_airbrakes_flight_deployment_function_of_height(
        [height_initial, v_y, v_y * 0.01],
        Hyperion,
        Spaceport_America_avg_launch_conditions,
        airbrakes,
        deployment_fn_simulator
    )

    # 2
    for j in range(num_intervals - i - 1):
        deployment_function_values[j] += np.deg2rad(airbrakes.max_deployment_rate)
    print(num_intervals - i - 10)


    # 3

    # 4
    t_to_apogee = ascent["time"].iloc[-1]
    apogee = ascent["height"].iloc[-1]

""" next step: test and score functions that look at ascent and check:
Test:
- closed at start
- closed at apogee
- max deployment angle = airbrakes.max_deployment_angle
- min deployment angle = 0
- max deployment rate = airbrakes.max_deployment_rate
- min deployment rate = -airbrakes.max_retraction_rate
- continuous
- continuous first derivative
- continuous second derivative

Score:
- how close it gets to 10k
- how close it gets to the max deployment angle
- how close to apogee it is before fully closing the airbrakes
    - maybe let the criteria be 0.1 deg so that fun functions can be used
- how close it gets to the max deployment rate?
"""


ascent = simulate_airbrakes_flight_deployment_function_of_height(
    [height_initial, v_y, v_y * 0.01],
    Hyperion,
    Spaceport_America_avg_launch_conditions,
    airbrakes,
    deployment_fn_simulator
)

# plot the ascent. include time, height, speed, a_y, deployment angle on the same plot
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()

ax1.plot(ascent["time"], ascent['height']*3.28084, color="b")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel(f"Height (ft)", color="b")
ax1.tick_params(axis="y", labelcolor="b")
ax1.axhline(y=10000, color='gray', linestyle='--')

ax2 = ax1.twinx()
ax2.plot(ascent["time"], ascent["speed"], color="r")
ax2.set_ylabel(f"Speed (m/s)", color="r")
ax2.tick_params(axis="y", labelcolor="r")

ax3 = ax1.twinx()
ax3.spines["right"].set_position(("outward", 60))
ax3.plot(ascent["time"], ascent['a_y'], color="g")
ax3.set_ylabel(f"Vertical Acceleration (m/s^2)", color="g")
ax3.tick_params(axis="y", labelcolor="g")

ax4 = ax1.twinx()
ax4.spines["right"].set_position(("outward", 120))
ax4.plot(ascent["time"], np.rad2deg(ascent["deployment_angle"]), color="y")
ax4.set_ylabel(f"Deployment Angle (deg)", color="y")
ax4.tick_params(axis="y", labelcolor="y")
ax4.set_yticks(range(0, 46, 15))

plt.title("Ascent with airbrakes deployed")
plt.show()




# step 3: use the function to generate flightpaths for each burnout state

# calculate the angles needed to hit 10k
# multiplier = launchpad_pressure / (con.R_specific_air * pow(launchpad_temp, con.F_g_over_R_spec_air_T_lapse_rate))

# deployment_angles = []
# tracker = 0

# for burnout_state in burnout_states:
#     apogee_no_braking = cfsim.simulate_airbrakes_flight(burnout_state["height"], burnout_state["speed"], burnout_state["v_y"], burnout_state["v_x"], launchpad_temp, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=0, timestep=0.01)
#     if apogee_no_braking * 3.28084 < 10000:
#         deployment_angles.append(0)
#         tracker += 1
#         print(f'{tracker} of {len(burnout_states)} deployment angles found')
#     else:
#         apogee_max_braking = cfsim.simulate_airbrakes_flight(burnout_state["height"], burnout_state["speed"], burnout_state["v_y"], burnout_state["v_x"], launchpad_temp, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=np.pi / 4, timestep=0.01)
#         if apogee_max_braking * 3.28084 > 10000:
#             deployment_angles.append(np.pi / 4)
#             tracker += 1
#             print(f'{tracker} of {len(burnout_states)} deployment angles found')
#         else:
#             lower_bound = 0
#             upper_bound = np.pi / 4
#             while upper_bound - lower_bound > 0.0001:
#                 deployment_angle = (upper_bound + lower_bound) / 2
#                 apogee = cfsim.simulate_airbrakes_flight(burnout_state["height"], burnout_state["speed"], burnout_state["v_y"], burnout_state["v_x"], launchpad_temp, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=deployment_angle, timestep=0.01)
#                 if apogee * 3.28084 > 10000:
#                     lower_bound = deployment_angle
#                 else:
#                     upper_bound = deployment_angle
#             deployment_angles.append(deployment_angle)
#             tracker += 1
#             print(f'{tracker} of {len(burnout_states)} deployment angles found')

# # plot the deployment angles
# plt.scatter(range(len(deployment_angles)), np.rad2deg(deployment_angles))
# plt.title("Deployment angles needed to hit 10k")
# plt.xlabel("Burnout state")
# plt.ylabel("Deployment angle (degrees)")
# plt.show()

# # save to a csv
# for i in range(len(deployment_angles)):
#     burnout_states[i]["deployment_angle_needed"] = deployment_angles[i]

# burnout_states_df = pd.DataFrame(burnout_states)
# burnout_states_df.drop(columns=["a_y", "a_x", "temperature","air_density","q"], inplace=True)
# # burnout_states_df.to_csv("flight-simulator/lookup-tables/burnout_states.csv", index=False)