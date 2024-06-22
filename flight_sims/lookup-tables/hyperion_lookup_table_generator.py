import numpy as np
import pandas as pd
from rocketflightsim import constants as con
from rocketflightsim import rocket_classes
from rocketflightsim import flight_simulation as fsim
from rocketflightsim import helper_functions as hfunc
from configs import Hyperion, current_airbrakes_model, Hyperion_launch_conditions

# define burnout states

dataset, _, _, burnout_index, _ = fsim.simulate_flight(rocket=Hyperion, timestep=0.001, launch_conditions=Hyperion_launch_conditions)
projected_conditions_burnout_state = dataset.iloc[burnout_index].copy()
time_to_apogee_no_deployment = projected_conditions_burnout_state['time']
projected_burnout_altitude = projected_conditions_burnout_state['height']
projected_burnout_vertical_speed = projected_conditions_burnout_state['v_z']

burnout_range_height = np.linspace(projected_burnout_altitude - projected_burnout_altitude * 0.25, projected_burnout_altitude + projected_burnout_altitude * 0.25, 100)
burnout_range_speed = np.linspace(projected_burnout_vertical_speed - projected_burnout_vertical_speed * 0.25, projected_burnout_vertical_speed + projected_burnout_vertical_speed * 0.25, 100)

print(f"Number of burnout states: {len(burnout_range_height) * len(burnout_range_speed)}")

"""
    time → don't care about initial, set to 0
    height → given
    speed → function of v_x, v_y, v_z
    a_y → can be calculated from angle to vertical, q, rocket parameters, environmental parameters
    a_x → can be calculated from angle to vertical, q, rocket parameters, environmental parameters
    v_z → given
    v_x → take as 8% of v_z
    v_y → take as 8% of v_z
    temperature → function of height, launch conditions
    air_density → function of height, launch conditions
    q → function of speed, air_density
    Ma → function of speed, temperature
    angle_to_vertical → function of velocities
"""

# make deployment functions

