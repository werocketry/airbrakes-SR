# a simulator that may be run during the flight to provide real-time apogee prediction based on the current airbrakes deployment angle being maintained
# as lightweight as possible, returning only the apogee prediction

import pandas as pd
import numpy as np
from configs import Hyperion, current_airbrakes_model
import helper_functions as hfunc
import rocket_classes as rktClass
import constants as con
import flight_simulation as fltSim

# wind
"""
Morning of launch, load wind forecasts for different times of day into the controller. Niall said wind forecasts are pretty accurate for the day of.
"""

# simulate the flight up to burnout
# real inputs would be fed from sensor data
dataset, liftoff_index, launch_rail_cleared_index, burnout_index, apogee_index = fltSim.simulate_flight(rocket=Hyperion, timestep=0.01)
pre_brake_flight = dataset.iloc[:burnout_index].copy()

input_height = pre_brake_flight["height"].iloc[-1]
input_speed = pre_brake_flight["speed"].iloc[-1]
input_v_y = pre_brake_flight["v_y"].iloc[-1]
input_v_x = pre_brake_flight["v_x"].iloc[-1]

# can be computed once at launchpad, then same value used each time a new sim is run
    # maybe incorporate this into the series of things the controller does during the burn based on what it read right before the burn (most recent launchpad pressure reading)
    # launchpad temperature could be something fed into it at the start of the day based on forecast temps at different times, and then it picks the one that is closest to the current time, as temp inside the rocket could vary from the outside
launchpad_temp = pre_brake_flight["temperature"].iloc[0]
launchpad_pressure = pre_brake_flight["air_density"].iloc[0] * con.R_specific_air * launchpad_temp
multiplier = launchpad_pressure / (con.R_specific_air * pow(launchpad_temp, con.F_g_over_R_spec_air_T_lapse_rate))
exponent_constant = con.F_g_over_R_spec_air_T_lapse_rate - 1


# TODO: opportunities to improve efficiency:
"""
- Dynamic viscosity only changes by about 5% over the flight, so can find a way to trade off some accuracy for speed here. Also it's only used in the reynolds number calculation, so it an optimized reynolds number calculation that uses len_characteristic/viscosity could be used for most of the timesteps
- Might be able to also look into not recalculating the reynolds number as often, because between 0 and 3e7, the drag coefficient doesn't change much
- Optimize Cd(Re) function to precombine the constants
- Look at helper_functions.py and note where np.interp might be faster
"""

def simulate_airbrakes_flight(input_height, input_speed, input_v_y, input_v_x, launchpad_temp, multiplier, exponent_constant, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle = 0, timestep=0.01):
    """
    Simulates the flight of the rocket with the airbrakes deployed at a constant angle to apogee, and returns the apogee height. To be used by the controller to predict apogee based on current deployment angle and adjust the airbrakes deployment angle accordingly.

    All arguments and return values are metric.

    Args:
    input_height (float): The height of the rocket at the start of the simulation
    input_speed (float): The speed of the rocket at the start of the simulation
    input_v_y (float): The vertical velocity of the rocket at the start of the simulation
    input_v_x (float): The horizontal velocity of the rocket at the start of the simulation
    launchpad_temp (float): The temperature at the launchpad
    multiplier (float): The multiplier used in the air density calculation
    exponent_constant (float): The exponent constant used in the air density calculation
    rocket (Rocket): The rocket object
    airbrakes (Airbrakes): The airbrakes object
    deployment_angle (float): The angle at which the airbrakes are deployed
    timestep (float): The timestep used in the simulation

    Returns:
    float: The predicted apogee height 
    """
    # Extract rocket parameters
    len_characteristic = rocket.L_rocket
    A_rocket = rocket.A_rocket
    mass = rocket.dry_mass
    Cd_rocket_at_Re = rocket.Cd_rocket_at_Re

    # Extract airbrakes parameters
    Cd_brakes = airbrakes.Cd_brakes
    A_brakes = airbrakes.num_flaps * airbrakes.A_flap
    max_deployment_speed = airbrakes.max_deployment_speed
    max_deployment_angle = airbrakes.max_deployment_angle
    t_full_deployment = max_deployment_angle / max_deployment_speed

    # Initialize simulation variables
    height = input_height
    speed = input_speed
    v_y = input_v_y
    v_x = input_v_x
    angle_to_vertical = np.arctan(v_x / v_y)

    # for efficiency, may be removed if/when the simulation is made more accurate by the cd of the brakes changing during the sim:
    A_Cd_brakes = A_brakes * Cd_brakes

    """
    TODO: Implement how closing the airbrakes at the end would be part of the simulation used for the controller

    t_to_apogee_min = v_y / a_y
        minimum time to apogee is if the current drag force remains all the way to apogee. Currently compared to time needed to close airbrakes completely if they're fully deployed
    t_to_apogee_max = v_y / con.F_gravity

    while t_to_apogee < t_full_deployment:
        run loop with same deployment angle as current
    
    rest of sim:
        run loop with deployment angle closing to 0
    """

    while v_y > 0:
        temperature = hfunc.temp_at_height(height, launchpad_temp)
        air_density = hfunc.air_density_optimized(temperature, multiplier, exponent_constant)
        dynamic_viscosity = hfunc.lookup_dynamic_viscosity(temperature)
        reynolds_num = hfunc.calculate_reynolds_number(air_density, speed, len_characteristic, dynamic_viscosity)
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)        

        F_drag = q * (np.sin(deployment_angle) * A_Cd_brakes + A_rocket * Cd_rocket)
        a_y = -F_drag * np.cos(angle_to_vertical) / mass - con.F_gravity
        a_x = -F_drag * np.sin(angle_to_vertical) / mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        height += v_y * timestep

        angle_to_vertical = np.arctan(v_x / v_y)

    return height

# TODO: going to need to put some work into picking a good timestep. maybe make it dynamic? for now using 0.1, which is small enough to cause less than a 1% error in the apogee prediction compared to a sim with a timestep of 0.001. Eventually do a proper analysis. Should also vary depending on how much of the flight is left

import numpy as np

thirty_deg_rad = np.deg2rad(30)
# print(thirty_deg_rad)

apogee = simulate_airbrakes_flight(input_height, input_speed, input_v_y, input_v_x, launchpad_temp, multiplier, exponent_constant, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=thirty_deg_rad, timestep=0.1)

print(apogee*3.28084)


if __name__ == "__main__":

    pass 
    # import time
    # time1 = time.time()
    # for i in range(10000):
    #     simulate_airbrakes_flight(input_height, input_speed, input_v_y, input_v_x, launchpad_temp, multiplier, exponent_constant, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=0.523599, timestep=0.1)
    #     if i % 100 == 0:
    #         print(i)
    # time2 = time.time()
    # print((time2 - time1)/10000)