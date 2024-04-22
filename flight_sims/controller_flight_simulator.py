# a simulator that may be run during the flight to provide real-time apogee prediction based on the current airbrakes deployment angle being maintained
# as lightweight as possible, returning only the apogee prediction

import pandas as pd
import numpy as np
from configs import Hyperion, current_airbrakes_model
import helper_functions as hfunc
import rocket_classes as rktClass
import constants as con
import flight_simulation as fsim

# wind
"""
Morning of launch, load wind forecasts for different times of day into the controller. Niall said wind forecasts are pretty accurate for the day of.

Might be nice to take a look at forecasts at SA in May and compare them to what the actual weather is the next day.
"""

# simulate the flight up to burnout
# real inputs would be fed from sensor data
dataset, liftoff_index, launch_rail_cleared_index, burnout_index, apogee_index = fsim.simulate_flight(rocket=Hyperion, timestep=0.01)
pre_brake_flight = dataset.iloc[:burnout_index].copy()

input_height = pre_brake_flight["height"].iloc[-1]
input_speed = pre_brake_flight["speed"].iloc[-1]
input_v_y = pre_brake_flight["v_y"].iloc[-1]
input_v_x = pre_brake_flight["v_x"].iloc[-1]

# can be computed once at launchpad, then same value used each time a new sim is run
    # maybe in the series of things the controller does during burn based on what it read right before the burn (most recent launchpad pressure reading)
    # launchpad temperature could be something fed into it at the start of the day based on forecast temps at different times, and then it picks the one that is closest to the current time, as temp inside the rocket could vary from the outside
launchpad_temp = pre_brake_flight["temperature"].iloc[0]
launchpad_pressure = pre_brake_flight["air_density"].iloc[0] * con.R_specific_air * launchpad_temp


# TODO: ways to improve efficiency:
"""
- Might be able to also look into not recalculating the Mach number as often, because for some parts of the Cd(Ma) curve, the drag coefficient doesn't change much
- Optimize Cd(Ma) function to precombine the constants
- all constants will be hardcoded
- multiplier can be calculated once and used in all the sims. Left inside the sim for now for the function's use in different scripts 
"""

def simulate_airbrakes_flight(input_height, input_speed, input_v_y, input_v_x, launchpad_temp, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle = 0, timestep=0.01):
    """
    Simulates the flight of the rocket from after motor burnout through to apogee with the airbrakes deployed at a constant angle, and returns the apogee height. To be used by the controller to predict apogee based on current deployment angle and adjust the airbrakes deployment angle accordingly.

    All arguments and return values are metric.

    Args:
    input_height (float): The height of the rocket at the start of the simulation
    input_speed (float): The speed of the rocket at the start of the simulation
    input_v_y (float): The vertical velocity of the rocket at the start of the simulation
    input_v_x (float): The horizontal velocity of the rocket at the start of the simulation
    launchpad_temp (float): The temperature at the launchpad
    rocket (Rocket): The rocket object
    airbrakes (Airbrakes): The airbrakes object
    deployment_angle (float): The angle at which the airbrakes are deployed
    timestep (float): The timestep used in the simulation

    Returns:
    float: The predicted apogee height 
    """
    # Extract rocket parameters
    mass = rocket.dry_mass
    Cd_A_rocket_fn = rocket.Cd_A_rocket

    # Extract airbrakes parameters
    Cd_brakes = airbrakes.Cd_brakes
    A_brakes = airbrakes.num_flaps * airbrakes.A_flap

    # Initialize simulation variables
    height = input_height
    speed = input_speed
    v_y = input_v_y
    v_x = input_v_x
    angle_to_vertical = np.arctan(v_x / v_y)
    
    multiplier = launchpad_pressure / (con.R_specific_air * pow(launchpad_temp, con.F_g_over_R_spec_air_T_lapse_rate))

    # for efficiency, may be removed if/when the simulation is made more accurate by the cd of the brakes changing during the sim:
    A_Cd_brakes = A_brakes * Cd_brakes

    """
    TODO: Implement how closing the airbrakes at the end would be part of the simulation used for the controller
        - wait till we test how fast retraction is (loaded and unloaded)

    t_to_apogee_min = v_y / a_y
        minimum time to apogee is if the current drag force remains all the way to apogee. Currently compared to time needed to close airbrakes completely if they're fully deployed
    t_to_apogee_max = v_y / con.F_gravity

    while t_to_apogee < t_full_retraction:
        run loop with same deployment angle as current
    
    rest of sim:
        run loop with deployment angle closing to 0
    """

    while v_y > 0:
        temperature = hfunc.temp_at_height(height, launchpad_temp)
        air_density = hfunc.air_density_optimized(temperature, multiplier)
        Ma = hfunc.mach_number_fn(speed, temperature)
        Cd_A_rocket = Cd_A_rocket_fn(Ma)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)        

        F_drag = q * (np.sin(deployment_angle) * A_Cd_brakes + Cd_A_rocket)
        a_y = -F_drag * np.cos(angle_to_vertical) / mass - con.F_gravity
        a_x = -F_drag * np.sin(angle_to_vertical) / mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        height += v_y * timestep

        angle_to_vertical = np.arctan(v_x / v_y)

    return height

# TODO: put some work into picking a good timestep. maybe make it dynamic? for now using 0.1, which is small enough to cause less than a 1% error in the apogee prediction compared to a sim with a timestep of 0.001. Eventually do a proper analysis. Should also vary depending on how much of the flight is left


if __name__ == "__main__":

    pass 

    # apogee = simulate_airbrakes_flight(input_height, input_speed, input_v_y, input_v_x, launchpad_temp, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=np.deg2rad(30), timestep=0.1)
    # print(apogee*3.28084)


    # import time
    # time1 = time.time()
    # for i in range(10000):
    #     simulate_airbrakes_flight(input_height, input_speed, input_v_y, input_v_x, launchpad_temp, rocket=Hyperion, airbrakes=current_airbrakes_model, deployment_angle=np.deg2rad(30), timestep=0.1)
    #     if i % 100 == 0:
    #         print(i)
    # time2 = time.time()
    # print((time2 - time1)/10000)