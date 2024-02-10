# Import libraries, define natural constants, helper functions
import pandas as pd
import numpy as np
from configs import Prometheus, Prometheus_launch_conditions, current_airbrakes_model
import helper_functions as hfunc
import rocket_classes as rktClass
import constants as con

# Create default instances of rocket, launch conditions, airbrakes
Prometheus = rktClass.Rocket(**Prometheus)
Prometheus_launch_conditions = rktClass.LaunchConditions(**Prometheus_launch_conditions)
airbrakes_model = rktClass.Airbrakes(**current_airbrakes_model)


# Flight simulation function
def simulate_flight(rocket=Prometheus, launch_conditions=Prometheus_launch_conditions, timestep=0.001):
    """
    Simulate the flight of a rocket until its apogee given its specifications and launch conditions.

    Args:
    - rocket (Rocket): An instance of the Rocket class.
    - launch_conditions (LaunchConditions): An instance of the LaunchConditions class.
    - timestep (float): The time increment for the simulation in seconds.

    Returns:
    - tuple: A tuple containing the dataset of simulation results and indices of key flight events.
    """

    # Initializations
    # Initialize essential parameters from rocket and launch conditions    
    len_characteristic = rocket.L_rocket
    A_rocket = rocket.A_rocket
    dry_mass = rocket.dry_mass
    fuel_mass_lookup = rocket.fuel_mass_lookup
    engine_thrust_lookup = rocket.engine_thrust_lookup
    Cd_rocket_at_Re = rocket.Cd_rocket_at_Re
    burnout_time = max(list(engine_thrust_lookup.keys()))

    # Extract launch condition parameters
    launchpad_pressure = launch_conditions.launchpad_pressure
    launchpad_temp = launch_conditions.launchpad_temp
    L_launch_rail = launch_conditions.L_launch_rail
    launch_angle = launch_conditions.launch_angle

    # Initialize simulation variables
    time, height, speed, a_y, a_x, v_y, v_x, Cd_rocket = 0, 0, 0, 0, 0, 0, 0, 0
    angle_to_vertical = np.deg2rad(90 - launch_angle)

    # Calculate initial air density and dynamic viscosity
    air_density = hfunc.air_density_fn(launchpad_pressure, launchpad_temp)
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
            launchpad_pressure,
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
                launchpad_pressure,
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
        pressure = hfunc.pressure_at_height(height, launchpad_temp, launchpad_pressure)
        air_density = hfunc.air_density_fn(pressure, temperature)
        dynamic_viscosity = hfunc.lookup_dynamic_viscosity(temperature)

        # Calculate Reynolds number, Drag coefficient, and Forces
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
                pressure,
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
        pressure = hfunc.pressure_at_height(height, launchpad_temp, launchpad_pressure)
        air_density = hfunc.air_density_fn(pressure, temperature)
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
                pressure,
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
    previous_height = height
    mass = dry_mass

    while height >= previous_height:
        temperature = hfunc.temp_at_height(height, launchpad_temp)
        pressure = hfunc.pressure_at_height(height, launchpad_temp, launchpad_pressure)
        air_density = hfunc.air_density_fn(pressure, temperature)
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
        previous_height = height
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
                pressure,
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
            "pressure": [row[8] for row in simulated_values],
            "air_density": [row[9] for row in simulated_values],
            "q": [row[10] for row in simulated_values],
            "dynamic_viscosity": [row[11] for row in simulated_values],
            "reynolds_num": [row[12] for row in simulated_values],
            "Cd_rocket": [row[13] for row in simulated_values],
            "angle_to_vertical": [row[14] for row in simulated_values],
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
def simulate_airbrakes_flight(pre_brake_flight, rocket=Prometheus, airbrakes=airbrakes_model, timestep=0.001):
    # Initializations
    len_characteristic = rocket.L_rocket
    A_rocket = rocket.A_rocket
    mass = rocket.dry_mass
    Cd_rocket_at_Re = rocket.Cd_rocket_at_Re

    launchpad_pressure = pre_brake_flight.pressure.iloc[0]
    launchpad_temp = pre_brake_flight.temperature.iloc[0]

    Cd_brakes = airbrakes.Cd_brakes
    max_deployment_speed = airbrakes.max_deployment_speed
    max_deployment_angle = airbrakes.max_deployment_angle
    A_brakes = airbrakes.num_flaps * airbrakes.A_flap

    pre_brake_flight["deployment_angle"] = 0

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
    previous_height = height
    while height >= previous_height:
        time += timestep

        temperature = hfunc.temp_at_height(height, launchpad_temp)
        pressure = hfunc.pressure_at_height(height, launchpad_temp, launchpad_pressure)
        air_density = hfunc.air_density_fn(pressure, temperature)
        dynamic_viscosity = hfunc.lookup_dynamic_viscosity(temperature)
        reynolds_num = hfunc.calculate_reynolds_number(air_density, speed, len_characteristic, dynamic_viscosity)
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = hfunc.calculate_dynamic_pressure(air_density, speed)        

        deployment_angle = min(max_deployment_angle, deployment_angle + max_deployment_speed * timestep)

        if deployment_angle >= max_deployment_angle and not time_recorded:
            time_of_max_deployment = time
            time_recorded = True


        F_drag = q * (np.sin(np.deg2rad(deployment_angle)) * A_Cd_brakes + A_rocket * Cd_rocket)
        a_y = -F_drag * np.cos(angle_to_vertical) / mass - con.F_gravity
        a_x = -F_drag * np.sin(angle_to_vertical) / mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        previous_height = height
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
                pressure,
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
        "pressure": [row[8] for row in simulated_values],
        "air_density": [row[9] for row in simulated_values],
        "q": [row[10] for row in simulated_values],
        "dynamic_viscosity": [row[11] for row in simulated_values],
        "reynolds_num": [row[12] for row in simulated_values],
        "Cd_rocket": [row[13] for row in simulated_values],
        "angle_to_vertical": [row[14] for row in simulated_values],
        "deployment_angle": [row[15] for row in simulated_values],
    }

    ascent = pd.concat([pre_brake_flight, pd.DataFrame(data)], ignore_index=True)

    if not time_recorded:
        time_of_max_deployment = time

    return ascent, time_of_max_deployment

# Execution Guard
if __name__ == "__main__":
    from configs import Hyperion

    Hyperion = rktClass.Rocket(**Hyperion)

    dataset, liftoff_index, launch_rail_cleared_index, burnout_index, apogee_index = simulate_flight(rocket=Hyperion)
    ascent, time_of_max_deployment = simulate_airbrakes_flight(dataset.iloc[:burnout_index].copy(), rocket=Hyperion)