# Import libraries, define natural constants, helper functions
import pandas as pd
import numpy as np
from configs import Prometheus, Prometheus_launch_conditions, current_airbrakes_model
import helper_functions as hfunc
import rocket_classes as rktClass
import constants as con

# TODO: add consideration for wind

default_timestep = 0.02
""" Notes on timesteps:

The default for OpenRocket sims is 0.01s for the first while, and then somewhere between 0.02 and 0.05 for a while, and then 0.05 for most of the rest of the ascent. It simulates more complicated dynamics than we do

A timestep of 0.02s gives apogees a few feet different for a 10k launch compared to using 0.001s. 0.001s can still be used for one-off sims, but when running many sims, 0.02s is better.
"""
# Flight simulation function
def simulate_flight(rocket=Prometheus, launch_conditions=Prometheus_launch_conditions, timestep=default_timestep):
    """
    Simulate the flight of a rocket until its apogee given its specifications and launch conditions.

    Args:
    - rocket (Rocket): An instance of the Rocket class.
    - launch_conditions (LaunchConditions): An instance of the LaunchConditions class.
    - timestep (float): The time increment for the simulation in seconds.

    Returns:
    - tuple: A tuple containing the dataset of simulation results and indices of key flight events.
    """

    # Initialize rocket parameters and launch conditions
    dry_mass = rocket.dry_mass
    fuel_mass_lookup = rocket.motor.mass_curve
    engine_thrust_lookup = rocket.motor.thrust_curve
    Cd_A_rocket_fn = rocket.Cd_A_rocket
    burnout_time = rocket.motor.burn_time

    # Extract launch condition parameters
    launchpad_pressure = launch_conditions.launchpad_pressure
    launchpad_temp = launch_conditions.launchpad_temp + 273.15
    L_launch_rail = launch_conditions.L_launch_rail
    launch_angle = launch_conditions.launch_angle

    # Initialize simulation variables
    time, height, speed, a_y, a_x, v_y, v_x, Cd_A_rocket, Ma, q = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    angle_to_vertical = np.deg2rad(90 - launch_angle)

    # Calculate constants to be used in air density function
    multiplier = launchpad_pressure / (con.R_specific_air * pow(launchpad_temp, con.F_g_over_R_spec_air_T_lapse_rate))
    exponent_constant = con.F_g_over_R_spec_air_T_lapse_rate - 1

    # Initialize air density
    air_density = hfunc.air_density_optimized(launchpad_temp, multiplier, exponent_constant)

    # Store the initial state of the rocket
    simulated_values = [
        [
            time,
            height,
            speed,
            a_y,
            a_x,
            v_y,
            v_x,
            launchpad_temp,
            air_density,
            q,
            Ma,
            Cd_A_rocket, # why is this being saved?
            angle_to_vertical,
        ]
    ]

    # Simulate motor burn until liftoff
    while (
        hfunc.thrust_at_time(time, engine_thrust_lookup)
        / hfunc.mass_at_time(time, dry_mass, fuel_mass_lookup)
        <= con.F_gravity
    ):
        time += timestep
        # Append simulation values for each timestep
        simulated_values.append(
            [
                time,
                height, # 0
                speed, # 0
                a_y, # 0
                a_x, # 0
                v_y, # 0
                v_x, # 0
                launchpad_temp,
                air_density,
                q, # 0
                Ma, # 0
                Cd_A_rocket, # 0
                angle_to_vertical,
            ]
        )

    liftoff_index = len(simulated_values)

    # Liftoff until launch rail cleared
    time += timestep
    effective_L_launch_rail = L_launch_rail - rocket.h_second_rail_button
    effective_h_launch_rail = effective_L_launch_rail * np.cos(angle_to_vertical)

    # Simulate flight from liftoff until the launch rail is cleared
    while height < effective_h_launch_rail:
        # Update environmental conditions based on height
        temperature = hfunc.temp_at_height(height, launchpad_temp)
        air_density = hfunc.air_density_optimized(temperature, multiplier, exponent_constant)

        # Calculate Mach number, drag coefficient, and forces
        Ma = hfunc.mach_number_fn(speed, temperature)
        Cd_A_rocket = Cd_A_rocket_fn(Ma)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)
        F_drag = q * Cd_A_rocket

        # Update rocket's motion parameters
        mass = hfunc.mass_at_time(time, dry_mass, fuel_mass_lookup)
        thrust = hfunc.thrust_at_time(time, engine_thrust_lookup)
        a_y = (thrust - F_drag) * np.cos(angle_to_vertical) / mass - con.F_gravity
        a_x = (thrust - F_drag) * np.sin(angle_to_vertical) / mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        height += v_y * timestep

        # Append updated simulation values
        simulated_values.append(
            [
                time,
                height,
                speed,
                a_y,
                a_x,
                v_y,
                v_x,
                temperature,
                air_density,
                q,
                Ma,
                Cd_A_rocket,
                angle_to_vertical,
            ]
        )
        time += timestep

    launch_rail_cleared_index = len(simulated_values)

    # Flight from launch rail cleared until burnout
    while time < burnout_time:
        # Update environmental conditions based on height
        temperature = hfunc.temp_at_height(height, launchpad_temp)
        air_density = hfunc.air_density_optimized(temperature, multiplier, exponent_constant)

        # Calculate Mach number, Drag coefficient, and Forces
        Ma = hfunc.mach_number_fn(speed, temperature)
        Cd_A_rocket = Cd_A_rocket_fn(Ma)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)
        F_drag = q * Cd_A_rocket

        # Update rocket's motion parameters
        mass = hfunc.mass_at_time(time, dry_mass, fuel_mass_lookup)
        thrust = hfunc.thrust_at_time(time, engine_thrust_lookup)
        a_y = (thrust - F_drag) * np.cos(angle_to_vertical) / mass - con.F_gravity
        a_x = (thrust - F_drag) * np.sin(angle_to_vertical) / mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        height += v_y * timestep

        # Recalculate the angle to the veritcal
        angle_to_vertical = np.arctan(v_x / v_y)

        # Append updated simulation values
        simulated_values.append(
            [
                time,
                height,
                speed,
                a_y,
                a_x,
                v_y,
                v_x,
                temperature,
                air_density,
                q,
                Ma,
                Cd_A_rocket,
                angle_to_vertical,
            ]
        )

        time += timestep

    burnout_index = len(simulated_values)

    # Flight from burnout to apogee
    mass = dry_mass

    while v_y > 0:
        temperature = hfunc.temp_at_height(height, launchpad_temp)
        air_density = hfunc.air_density_optimized(temperature, multiplier, exponent_constant)

        # Calculate Mach number, Drag coefficient, and Forces
        Ma = hfunc.mach_number_fn(speed, temperature)
        Cd_A_rocket = Cd_A_rocket_fn(Ma)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)
        F_drag = q * Cd_A_rocket

        # Update rocket's motion parameters
        a_y = -F_drag * np.cos(angle_to_vertical) / mass - con.F_gravity
        a_x = -F_drag * np.sin(angle_to_vertical) / mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        height += v_y * timestep

        # Recalculate the angle to the veritcal
        angle_to_vertical = np.arctan(v_x / v_y)

        # Append updated simulation values
        simulated_values.append(
            [
                time,
                height,
                speed,
                a_y,
                a_x,
                v_y,
                v_x,
                temperature,
                air_density,
                q,
                Ma,
                Cd_A_rocket,
                angle_to_vertical,
            ]
        )

        time += timestep

    # Mark the index at apogee (highest point)
    apogee_index = len(simulated_values)
    simulated_values[-1][12] = simulated_values[-2][12]

    # Convert the list of simulation values to a DataFrame for easier analysis and visualization
    dataset = pd.DataFrame(
        {
            "time": [row[0] for row in simulated_values],
            "height": [row[1] for row in simulated_values],
            "speed": [row[2] for row in simulated_values],
            "a_y": [row[3] for row in simulated_values],
            "a_x": [row[4] for row in simulated_values],
            "v_y": [row[5] for row in simulated_values],
            "v_x": [row[6] for row in simulated_values],
            "temperature": [row[7] for row in simulated_values],
            "air_density": [row[8] for row in simulated_values],
            "q": [row[9] for row in simulated_values],
            "Ma": [row[10] for row in simulated_values],
            "Cd_A_rocket": [row[11] for row in simulated_values],
            "angle_to_vertical": [row[12] for row in simulated_values],
        }
    )

    return (
        dataset,
        liftoff_index,
        launch_rail_cleared_index,
        burnout_index,
        apogee_index
    )


# Flight with airbrakes simulation function
def simulate_airbrakes_flight(pre_brake_flight, rocket=Prometheus, airbrakes=current_airbrakes_model, timestep=default_timestep):
    # Extract rocket parameters
    mass = rocket.dry_mass
    Cd_A_rocket_fn = rocket.Cd_A_rocket

    # Extract launch condition parameters
    launchpad_temp = pre_brake_flight.temperature.iloc[0]
    launchpad_pressure = pre_brake_flight.air_density.iloc[0] * con.R_specific_air * launchpad_temp

    # Calculate constants to be used in air density function
    multiplier = launchpad_pressure / (con.R_specific_air * pow(launchpad_temp, con.F_g_over_R_spec_air_T_lapse_rate))
    exponent_constant = con.F_g_over_R_spec_air_T_lapse_rate - 1

    # Extract airbrakes parameters
    Cd_brakes = airbrakes.Cd_brakes
    max_deployment_speed = np.deg2rad(airbrakes.max_deployment_speed)
    max_deployment_angle = np.deg2rad(airbrakes.max_deployment_angle)
    A_brakes = airbrakes.num_flaps * airbrakes.A_flap

    pre_brake_flight["deployment_angle"] = 0

    # Initialize simulation variables
    height = pre_brake_flight["height"].iloc[-1]
    speed = pre_brake_flight["speed"].iloc[-1]
    v_y = pre_brake_flight["v_y"].iloc[-1]
    v_x = pre_brake_flight["v_x"].iloc[-1]
    time = pre_brake_flight["time"].iloc[-1]
    angle_to_vertical = np.arctan(v_x / v_y)

    deployment_angle = 0
    time_recorded = False

    # for efficiency, may be removed if/when the simulation is made more accurate by the cd of the brakes changing during the sim:
    A_Cd_brakes = A_brakes * Cd_brakes

    simulated_values = []
    while v_y > 0:
        time += timestep

        temperature = hfunc.temp_at_height(height, launchpad_temp)
        air_density = hfunc.air_density_optimized(temperature, multiplier, exponent_constant)
        Ma = hfunc.mach_number_fn(speed, temperature)
        Cd_A_rocket = Cd_A_rocket_fn(Ma)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)

        deployment_angle = min(max_deployment_angle, deployment_angle + max_deployment_speed * timestep)

        if deployment_angle >= max_deployment_angle and not time_recorded:
            time_of_max_deployment = time
            time_recorded = True


        F_drag = q * (np.sin(deployment_angle) * A_Cd_brakes + Cd_A_rocket)
        a_y = -F_drag * np.cos(angle_to_vertical) / mass - con.F_gravity
        a_x = -F_drag * np.sin(angle_to_vertical) / mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        height += v_y * timestep

        angle_to_vertical = np.arctan(v_x / v_y)

        simulated_values.append(
            [
                time,
                height,
                speed,
                a_y,
                a_x,
                v_y,
                v_x,
                temperature,
                air_density,
                q,
                Ma,
                Cd_A_rocket,
                angle_to_vertical,
                deployment_angle,
            ]
        )

    simulated_values[-1][12] = simulated_values[-2][12]

    data = {
        "time": [row[0] for row in simulated_values],
        "height": [row[1] for row in simulated_values],
        "speed": [row[2] for row in simulated_values],
        "a_y": [row[3] for row in simulated_values],
        "a_x": [row[4] for row in simulated_values],
        "v_y": [row[5] for row in simulated_values],
        "v_x": [row[6] for row in simulated_values],
        "temperature": [row[7] for row in simulated_values],
        "air_density": [row[8] for row in simulated_values],
        "q": [row[9] for row in simulated_values],
        "Ma": [row[10] for row in simulated_values],
        "Cd_A_rocket": [row[11] for row in simulated_values],
        "angle_to_vertical": [row[12] for row in simulated_values],
        "deployment_angle": [row[13] for row in simulated_values],
    }

    ascent = pd.concat([pre_brake_flight, pd.DataFrame(data)], ignore_index=True)

    if not time_recorded:
        time_of_max_deployment = time

    return ascent, time_of_max_deployment


if __name__ == "__main__":
    from configs import Hyperion
    
    dataset, liftoff_index, launch_rail_cleared_index, burnout_index, apogee_index = simulate_flight(rocket=Hyperion, timestep=0.001)
    
    print(dataset[["time", "height", "speed"]].iloc[apogee_index - 1]*3.28084)
    ascent, time_of_max_deployment = simulate_airbrakes_flight(dataset.iloc[:burnout_index].copy(), rocket=Hyperion, timestep=0.001)
    print(ascent[["time", "height", "speed"]].iloc[-1]*3.28084)

    # run a couple hundred different timesteps in logspace between 0.001 and 0.1 to see how it changes to help pick a good timestep
    
"""    apogees = []
    for timestep in np.logspace(-3, -1, 200):
        dataset, liftoff_index, launch_rail_cleared_index, burnout_index, apogee_index = simulate_flight(rocket=Hyperion, timestep=timestep)
        ascent, time_of_max_deployment = simulate_airbrakes_flight(dataset.iloc[:burnout_index].copy(), rocket=Hyperion, timestep=0.001)
        apogees.append(ascent["height"].iloc[-1]*3.28084)
        print(len(apogees))
    # plot them
    import matplotlib.pyplot as plt
    plt.plot(np.logspace(-3, -1, 200), apogees)
    plt.xscale("log")
    plt.xlabel("Timestep (s)")
    plt.ylabel("Apogee (ft)")
    plt.title("Apogee vs Timestep")
    plt.show()"""
    