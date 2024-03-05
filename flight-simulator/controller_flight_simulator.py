# a simulator that may be run during the flight to provide real-time apogee prediction
# as lightweight as possible, returning only the apogee prediction

import pandas as pd
import numpy as np
from configs import Hyperion, current_airbrakes_model
import helper_functions as hfunc
import rocket_classes as rktClass
import constants as con
import flight_simulation as fltSim

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
    # should temperature be something fed into it at the start of the day based on forecast temps at different times, and then it picks the one that is closest to the current time? temp inside the rocket could vary from the outside
launchpad_temp = pre_brake_flight["temperature"].iloc[0]
launchpad_pressure = pre_brake_flight["air_density"].iloc[0] * con.R_specific_air * launchpad_temp
multiplier = launchpad_pressure / (con.R_specific_air * pow(launchpad_temp, con.F_g_over_R_spec_air_T_lapse_rate))
exponent_constant = con.F_g_over_R_spec_air_T_lapse_rate - 1

# when used on controller, the current deployment angle would be fed in, and the deployment angle will remain constant for a given sim
def simulate_airbrakes_flight(input_height, input_speed, input_v_y, input_v_x, launchpad_temp, multiplier, exponent_constant, rocket=Hyperion, airbrakes=current_airbrakes_model, timestep=0.01):
    # Extract rocket parameters
    len_characteristic = rocket.L_rocket
    A_rocket = rocket.A_rocket
    mass = rocket.dry_mass
    Cd_rocket_at_Re = rocket.Cd_rocket_at_Re

    # Extract airbrakes parameters
    Cd_brakes = airbrakes.Cd_brakes
    max_deployment_speed = np.deg2rad(airbrakes.max_deployment_speed)
    max_deployment_angle = np.deg2rad(airbrakes.max_deployment_angle)
    A_brakes = airbrakes.num_flaps * airbrakes.A_flap

    # Initialize simulation variables
    height = input_height
    speed = input_speed
    v_y = input_v_y
    v_x = input_v_x
    angle_to_vertical = np.arctan(v_x / v_y)

    deployment_angle = 0

    # for efficiency, may be removed when the simulation is made more accurate by the cd of the brakes changing during the sim:
    A_Cd_brakes = A_brakes * Cd_brakes
    
    while v_y > 0:
        temperature = hfunc.temp_at_height(height, launchpad_temp)
        air_density = hfunc.air_density_optimized(temperature, multiplier, exponent_constant)
        dynamic_viscosity = hfunc.lookup_dynamic_viscosity(temperature)
        reynolds_num = hfunc.calculate_reynolds_number(air_density, speed, len_characteristic, dynamic_viscosity)
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)        

        deployment_angle = min(max_deployment_angle, deployment_angle + max_deployment_speed * timestep)

        F_drag = q * (np.sin(deployment_angle) * A_Cd_brakes + A_rocket * Cd_rocket)
        a_y = -F_drag * np.cos(angle_to_vertical) / mass - con.F_gravity
        a_x = -F_drag * np.sin(angle_to_vertical) / mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        height += v_y * timestep

        angle_to_vertical = np.arctan(v_x / v_y)

    return height

apogee = simulate_airbrakes_flight(input_height, input_speed, input_v_y, input_v_x, launchpad_temp, multiplier, exponent_constant, rocket=Hyperion, airbrakes=current_airbrakes_model, timestep=0.01)

print(apogee*3.28084)

import time
time1 = time.time()
for i in range(10000):
    simulate_airbrakes_flight(input_height, input_speed, input_v_y, input_v_x, launchpad_temp, multiplier, exponent_constant, rocket=Hyperion, airbrakes=current_airbrakes_model, timestep=0.01)
    if i % 100 == 0:
        print(i)
time2 = time.time()
print((time2 - time1)/10000)