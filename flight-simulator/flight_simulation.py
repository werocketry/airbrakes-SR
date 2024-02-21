# Import libraries, define natural constants, helper functions
import pandas as pd
import numpy as np
from configs import Prometheus, Prometheus_launch_conditions, current_airbrakes_model
import helper_functions as hfunc
import rocket_classes as rktClass
import constants as con


"""
Note on timesteps:
The default for OpenRocket sims is 0.01s for the first while, and then somewhere between 0.02 and 0.05 for a while, and then 0.05 for most of the rest of the ascent. It simulates more complicated dynamics than we do, so a timestep of 0.01s is good enough for us. That timestep gives apogees about 2m different for a 10k launch compared to using 0.001s. 0.001s can still be used for one-off sims, but when running many sims, 0.01s is better.
"""
# Flight simulation function
def simulate_flight(rocket=Prometheus, launch_conditions=Prometheus_launch_conditions, timestep=0.01):
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
    len_characteristic = rocket.L_rocket
    A_rocket = rocket.A_rocket
    dry_mass = rocket.dry_mass
    fuel_mass_lookup = rocket.motor.mass_curve
    engine_thrust_lookup = rocket.motor.thrust_curve
    Cd_rocket_at_Re = rocket.Cd_rocket_at_Re
    burnout_time = rocket.motor.burn_time

    # Extract launch condition parameters
    launchpad_pressure = launch_conditions.launchpad_pressure
    launchpad_temp = launch_conditions.launchpad_temp + 273.15
    L_launch_rail = launch_conditions.L_launch_rail
    launch_angle = launch_conditions.launch_angle

    # Initialize simulation variables
    time, height, speed, a_y, a_x, v_y, v_x, Cd_rocket = 0, 0, 0, 0, 0, 0, 0, 0
    angle_to_vertical = np.deg2rad(90 - launch_angle)

    # Calculate constants to be used in air density function
    multiplier = launchpad_pressure / (con.R_specific_air * pow(launchpad_temp, con.F_g_over_R_spec_air_T_lapse_rate))
    exponent_constant = con.F_g_over_R_spec_air_T_lapse_rate - 1

    # Calculate initial air density and dynamic viscosity
    air_density = hfunc.air_density_optimized(launchpad_temp, multiplier, exponent_constant)
    dynamic_viscosity = hfunc.lookup_dynamic_viscosity(launchpad_temp)
    reynolds_num = hfunc.calculate_reynolds_number(air_density, speed, len_characteristic, dynamic_viscosity) # 0
    q = hfunc.calculate_dynamic_pressure(air_density, speed)

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
            dynamic_viscosity,
            reynolds_num,
            Cd_rocket,
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
                dynamic_viscosity,
                reynolds_num, # 0
                Cd_rocket, # 0
                angle_to_vertical,
            ]
        )

    liftoff_index = len(simulated_values)

    # Liftoff until launch rail cleared
    time += timestep
    effective_L_launch_rail = L_launch_rail - rocket.h_second_rail_button

    # Simulate flight from liftoff until the launch rail is cleared
    while height < effective_L_launch_rail * np.cos(angle_to_vertical):
        # Update environmental conditions based on height
        temperature = hfunc.temp_at_height(height, launchpad_temp)
        air_density = hfunc.air_density_optimized(temperature, multiplier, exponent_constant)
        dynamic_viscosity = hfunc.lookup_dynamic_viscosity(temperature)

        # Calculate Reynolds number, drag coefficient, and forces
        reynolds_num = (air_density * speed * len_characteristic) / dynamic_viscosity
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)
        F_drag = q * Cd_rocket * A_rocket

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
                dynamic_viscosity,
                reynolds_num,
                Cd_rocket,
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
        dynamic_viscosity = hfunc.lookup_dynamic_viscosity(temperature)

        # Calculate Reynolds number, Drag coefficient, and Forces
        reynolds_num = hfunc.calculate_reynolds_number(air_density, speed, len_characteristic, dynamic_viscosity)
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)
        F_drag = q * Cd_rocket * A_rocket

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
                dynamic_viscosity,
                reynolds_num,
                Cd_rocket,
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
        dynamic_viscosity = hfunc.lookup_dynamic_viscosity(temperature)

        # Calculate Reynolds number, Drag coefficient, and Forces
        reynolds_num = hfunc.calculate_reynolds_number(air_density, speed, len_characteristic, dynamic_viscosity)
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)
        F_drag = q * Cd_rocket * A_rocket

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
                dynamic_viscosity,
                reynolds_num,
                Cd_rocket,
                angle_to_vertical,
            ]
        )

        time += timestep

    # Mark the index at apogee (highest point)
    apogee_index = len(simulated_values)

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
            "dynamic_viscosity": [row[10] for row in simulated_values],
            "reynolds_num": [row[11] for row in simulated_values],
            "Cd_rocket": [row[12] for row in simulated_values],
            "angle_to_vertical": [row[13] for row in simulated_values],
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
def simulate_airbrakes_flight(pre_brake_flight, rocket=Prometheus, airbrakes=current_airbrakes_model, timestep=0.01):
    # Extract rocket parameters
    len_characteristic = rocket.L_rocket
    A_rocket = rocket.A_rocket
    mass = rocket.dry_mass
    Cd_rocket_at_Re = rocket.Cd_rocket_at_Re

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

    # for efficiency, may be removed when the simulation is made more accurate by the cd of the brakes changing during the sim:
    A_Cd_brakes = A_brakes * Cd_brakes

    simulated_values = []
    while v_y > 0:
        time += timestep

        temperature = hfunc.temp_at_height(height, launchpad_temp)
        air_density = hfunc.air_density_optimized(temperature, multiplier, exponent_constant)
        dynamic_viscosity = hfunc.lookup_dynamic_viscosity(temperature)
        reynolds_num = hfunc.calculate_reynolds_number(air_density, speed, len_characteristic, dynamic_viscosity)
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)        

        deployment_angle = min(max_deployment_angle, deployment_angle + max_deployment_speed * timestep)

        if deployment_angle >= max_deployment_angle and not time_recorded:
            time_of_max_deployment = time
            time_recorded = True


        F_drag = q * (np.sin(deployment_angle) * A_Cd_brakes + A_rocket * Cd_rocket)
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
                dynamic_viscosity,
                reynolds_num,
                Cd_rocket,
                angle_to_vertical,
                deployment_angle,
            ]
        )

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
        "dynamic_viscosity": [row[10] for row in simulated_values],
        "reynolds_num": [row[11] for row in simulated_values],
        "Cd_rocket": [row[12] for row in simulated_values],
        "angle_to_vertical": [row[13] for row in simulated_values],
        "deployment_angle": [row[14] for row in simulated_values],
    }

    ascent = pd.concat([pre_brake_flight, pd.DataFrame(data)], ignore_index=True)

    if not time_recorded:
        time_of_max_deployment = time

    return ascent, time_of_max_deployment


if __name__ == "__main__":
    from configs import Hyperion
    
    dataset, liftoff_index, launch_rail_cleared_index, burnout_index, apogee_index = simulate_flight(rocket=Hyperion, timestep=0.01)
    
    print(dataset[["time", "height", "speed"]].iloc[apogee_index - 1]*3.28084)
    ascent, time_of_max_deployment = simulate_airbrakes_flight(dataset.iloc[:burnout_index].copy(), rocket=Hyperion, timestep=0.01)
    print(ascent[["time", "height", "speed"]].iloc[-1]*3.28084)