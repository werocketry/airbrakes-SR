# Import libraries, define natural constants, helper functions
import pandas as pd
import numpy as np

F_gravity = 9.80665 # m/s^2
R_universal = 8.3144598 # J/(mol*K)
MM_air = 0.0289644 # kg/mol
R_specific_air = R_universal/MM_air # J/(kg*K)
T_lapse_rate = 0.0065 # K/m

def temp_at_height(h, launchpad_temp):
    return launchpad_temp - (h*T_lapse_rate)
def pressure_at_height(h, launchpad_temp, launchpad_pressure):
    return launchpad_pressure*pow((1-(h*T_lapse_rate/(launchpad_temp+273.15))),(F_gravity/(R_specific_air*T_lapse_rate)))
def air_density_fn(pressure, temp):
    return pressure/(R_specific_air*(temp+273.15))
def lookup_dynamic_viscosity(temp):
    """
    temp: temperature in C
    returns dynamic viscosity in kg/m·s
    source of lookup table: https://www.me.psu.edu/cimbala/me433/Links/Table_A_9_CC_Properties_of_Air.pdf
    """
    one_atm_air_dynamic_viscosity_lookup = {
    -150:8.636*pow(10,-6),
    -100:1.189*pow(10,-6),
    -50:1.474*pow(10,-5),
    -40:1.527*pow(10,-5),
    -30:1.579*pow(10,-5),
    -20:1.630*pow(10,-5),
    -10:1.680*pow(10,-5),
    0:1.729*pow(10,-5),
    5:1.754*pow(10,-5),
    10:1.778*pow(10,-5),
    15:1.802*pow(10,-5),
    20:1.825*pow(10,-5),
    25:1.849*pow(10,-5),
    30:1.872*pow(10,-5),
    35:1.895*pow(10,-5),
    40:1.918*pow(10,-5),
    45:1.941*pow(10,-5),
    50:1.963*pow(10,-5),
    60:2.008*pow(10,-5),
    70:2.052*pow(10,-5),
    }
    temp_list = list(one_atm_air_dynamic_viscosity_lookup.keys())
    if temp <= temp_list[0]:
        return one_atm_air_dynamic_viscosity_lookup[temp_list[0]]
    elif temp >= temp_list[-1]:
        return one_atm_air_dynamic_viscosity_lookup[temp_list[-1]]
    else:
        lower_temp = max([t for t in temp_list if t < temp])
        upper_temp = min([t for t in temp_list if t > temp])
        lower_viscosity = one_atm_air_dynamic_viscosity_lookup[lower_temp]
        upper_viscosity = one_atm_air_dynamic_viscosity_lookup[upper_temp]
        return lower_viscosity + (temp - lower_temp) * (upper_viscosity - lower_viscosity) / (upper_temp - lower_temp)

def mass_at_time(time, dry_mass, fuel_mass_lookup):
    time_list = list(fuel_mass_lookup.keys())
    if time >= time_list[-1]:
        return dry_mass
    else:
        lower_time = max([t for t in time_list if t <= time])
        upper_time = min([t for t in time_list if t > time])
        lower_mass = fuel_mass_lookup[lower_time]
        upper_mass = fuel_mass_lookup[upper_time]
        return dry_mass + lower_mass + (time - lower_time) * (upper_mass - lower_mass) / (upper_time - lower_time)
def thrust_at_time(time, engine_thrust_lookup):
    time_list = list(engine_thrust_lookup.keys())
    if time >= time_list[-1]:
        return 0
    else:
        lower_time = max([t for t in time_list if t <= time])
        upper_time = min([t for t in time_list if t > time])
        lower_thrust = engine_thrust_lookup[lower_time]
        upper_thrust = engine_thrust_lookup[upper_time]
        return lower_thrust + (time - lower_time) * (upper_thrust - lower_thrust) / (upper_time - lower_time)

# Define rocket, launch condition, and airbrake classes
class Rocket:
    """
    L_rocket: length of the rocket (m)
    A_rocket: cross-sectional area of the rocket (m^2)
    dry_mass: dry mass of the rocket (kg)
    fuel_mass_lookup: dictionary of fuel mass at time (kg)
    engine_thrust_lookup: dictionary of thrust at time (N)
    Cd_rocket_at_Re: coefficient of drag of the rocket at Re
    """
    def __init__(self, dry_mass, fuel_mass_lookup, engine_thrust_lookup, Cd_rocket_at_Re, A_rocket, L_rocket):
        self.L_rocket = L_rocket
        self.A_rocket = A_rocket
        self.dry_mass = dry_mass
        self.fuel_mass_lookup = fuel_mass_lookup
        self.engine_thrust_lookup = engine_thrust_lookup
        self.Cd_rocket_at_Re = Cd_rocket_at_Re
class LaunchConditions:
    """
    launchpad_pressure: pressure at the launchpad (Pa)
    launchpad_temp: temperature at the launchpad (C)
    L_launch_rail: length of the launch rail (m)
    launch_angle: launch angle (deg)
    """
    def __init__(self, launchpad_pressure, launchpad_temp, L_launch_rail, launch_angle):
        self.launchpad_pressure = launchpad_pressure
        self.launchpad_temp = launchpad_temp
        self.L_launch_rail = L_launch_rail
        self.launch_angle = launch_angle
class Airbrakes:
    """
    num_flaps: number of flaps on the airbrakes
    A_flap: cross-sectional area of each flap (m^2)
    Cd_brakes: coefficient of drag of the airbrakes
    max_deployment_speed: maximum speed at which the airbrakes can be deployed (deg/s)
    """
    def __init__(self, num_flaps, A_flap, Cd_brakes, max_deployment_speed):
        self.num_flaps = num_flaps
        self.A_flap = A_flap
        self.Cd_brakes = Cd_brakes
        self.max_deployment_speed = max_deployment_speed

# Create instances of rocket, launch conditions, airbrakes
def Prometheus_Cd_function(Re):
    # use k-ω model from Prometheus CFD sims
    if Re < 1e7: return 0.42
    elif Re < 2.8e7: return 0.42 - (Re-1e7)*(0.42-0.4)/(2.8e7-1e7)
    elif Re < 5e7: return 0.4 - (Re-2.8e7)*(0.4-0.31)/(5e7-2.8e7)
    else: return 0.31
Prometheus = Rocket(
    L_rocket = 2.229, # length of Prometheus in m
    A_rocket = 0.015326, # 5.5" diameter circle's area in m^2
    dry_mass = 16.91, # kg, from (CAD? final physical rocket mass? were they the same at the end?)
    fuel_mass_lookup = { # source: https://www.thrustcurve.org/simfiles/5f4294d20002e900000006b1/
    # note we took there to be 3.6kg of propellant
    0:3.737,
    0.04:3.72292,
    0.082:3.69047,
    0.176:3.61337,
    0.748:3.14029,
    1.652:2.34658,
    2.676:1.45221,
    3.89:0.512779,
    4.399:0.157939,
    4.616:0.0473998,
    4.877:0.000343417,
    4.897:0
    },
    engine_thrust_lookup = { # source: https://www.thrustcurve.org/simfiles/5f4294d20002e900000006b1/
    0:0,
    0.04:1427.8,
    0.082:1706.39,
    0.176:1620.49,
    0.748:1734.25,
    1.652:1827.11,
    2.676:1715.68,
    3.89:1423.15,
    4.399:1404.58,
    4.616:661.661,
    4.877:69.649,
    4.897:0
    }, 
    Cd_rocket_at_Re = Prometheus_Cd_function
)
Prometheus_launch_conditions = LaunchConditions(
    launchpad_pressure = 86400, # Pa, what it was at Prometheus' launch
    launchpad_temp = 34, # deg C, what it was at Prometheus' launch
    L_launch_rail = 5.2, # m, what ESRA provides
    launch_angle = 84 # deg, SAC comp rules
)
example_airbrakes = Airbrakes(
    num_flaps = 4,
    A_flap = 0.0064516, # 0.011408 is the current area in CAD, likely to decrease. 0.0064516 from Maryland's last year, which we'll probably have a similar configuration to
    Cd_brakes = 1, # about what other teams had, super rough
    max_deployment_speed = 10 # deg/s
)

# Flight simulation function
def simulate_flight(rocket = Prometheus, launch_conditions = Prometheus_launch_conditions, timestep = 0.001):
    # Initializations
    len_characteristic = rocket.L_rocket
    A_rocket = rocket.A_rocket
    dry_mass = rocket.dry_mass
    fuel_mass_lookup = rocket.fuel_mass_lookup
    engine_thrust_lookup = rocket.engine_thrust_lookup
    Cd_rocket_at_Re = rocket.Cd_rocket_at_Re
    burnout_time = max(list(engine_thrust_lookup.keys()))

    launchpad_pressure = launch_conditions.launchpad_pressure
    launchpad_temp = launch_conditions.launchpad_temp
    L_launch_rail = launch_conditions.L_launch_rail
    launch_angle = launch_conditions.launch_angle

    time, height, speed, v_y, v_x = 0, 0, 0, 0, 0
    angle_to_vertical = np.deg2rad(90 - launch_angle)
    air_density = air_density_fn(launchpad_pressure, launchpad_temp)
    dynamic_viscosity = lookup_dynamic_viscosity(launchpad_temp)

    simulated_values = [[0, 0, 0, 0, 0, 0, 0, launchpad_temp, launchpad_pressure, air_density, 0, dynamic_viscosity, 0, 0, angle_to_vertical]]

    # Motor burn until liftoff
    while thrust_at_time(time, engine_thrust_lookup)/mass_at_time(time, dry_mass, fuel_mass_lookup) <= F_gravity:
        time += timestep
        simulated_values.append([time, 0, 0, 0, 0, 0, 0, launchpad_temp, launchpad_pressure, air_density, 0, dynamic_viscosity, 0, 0, angle_to_vertical])
    liftoff_index = len(simulated_values)

    # Liftoff until launch rail cleared
    while height < L_launch_rail*np.cos(angle_to_vertical):
        time += timestep
        temperature = temp_at_height(height,launchpad_temp)        
        pressure = pressure_at_height(height,launchpad_temp, launchpad_pressure)
        air_density = air_density_fn(pressure, temperature)
        dynamic_viscosity = lookup_dynamic_viscosity(temperature)
        reynolds_num = (air_density*speed*len_characteristic)/dynamic_viscosity
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = 0.5 * (air_density) * (speed**2)
        F_drag = q * Cd_rocket * A_rocket
        mass = mass_at_time(time,dry_mass,fuel_mass_lookup)
        thrust = thrust_at_time(time, engine_thrust_lookup)
        a_y = (thrust-F_drag)*np.cos(angle_to_vertical)/mass - F_gravity
        a_x = (thrust-F_drag)*np.sin(angle_to_vertical)/mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        height += v_y * timestep
    
        simulated_values.append([time, height, speed, a_y, a_x, v_y, v_x, temperature, pressure, air_density, q, dynamic_viscosity, reynolds_num, Cd_rocket, angle_to_vertical])
    launch_rail_cleared_index = len(simulated_values)
    
    # Flight from launch rail cleared until burnout
    while time < burnout_time:
        time += timestep
        
        temperature = temp_at_height(height, launchpad_temp)        
        pressure = pressure_at_height(height, launchpad_temp, launchpad_pressure)
        air_density = air_density_fn(pressure, temperature)
        dynamic_viscosity = lookup_dynamic_viscosity(temperature)
        reynolds_num = air_density * speed * len_characteristic / dynamic_viscosity
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = 0.5 * air_density * (speed**2)
        F_drag = q * Cd_rocket * A_rocket
        mass = mass_at_time(time, dry_mass, fuel_mass_lookup)
        thrust = thrust_at_time(time, engine_thrust_lookup)
        a_y = (thrust-F_drag)*np.cos(angle_to_vertical)/mass - F_gravity
        a_x = (thrust-F_drag)*np.sin(angle_to_vertical)/mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        height += v_y * timestep

        angle_to_vertical = np.arctan(v_x/v_y)
        
        
        simulated_values.append([time, height, speed, a_y, a_x, v_y, v_x, temperature, pressure, air_density, q, dynamic_viscosity, reynolds_num, Cd_rocket, angle_to_vertical])
    burnout_index = len(simulated_values)

    # Flight from burnout to apogee
    previous_height = height
    mass = dry_mass
    while height >= previous_height:
        time += timestep
        
        temperature = temp_at_height(height, launchpad_temp)        
        pressure = pressure_at_height(height, launchpad_temp, launchpad_pressure)
        air_density = air_density_fn(pressure, temperature)
        dynamic_viscosity = lookup_dynamic_viscosity(temperature)
        reynolds_num = (air_density*speed*len_characteristic)/dynamic_viscosity
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = 0.5 * air_density * (speed**2)
        F_drag = q * Cd_rocket * A_rocket
        a_y = -F_drag*np.cos(angle_to_vertical)/mass - F_gravity
        a_x = -F_drag*np.sin(angle_to_vertical)/mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        previous_height = height
        height += v_y * timestep

        angle_to_vertical = np.arctan(v_x/v_y)
        
        simulated_values.append([time, height, speed, a_y, a_x, v_y, v_x, temperature, pressure, air_density, q, dynamic_viscosity, reynolds_num, Cd_rocket, angle_to_vertical])
    apogee_index = len(simulated_values)
    dataset = pd.DataFrame({
        'time': [row[0] for row in simulated_values],
        'height': [row[1] for row in simulated_values],
        'speed': [row[2] for row in simulated_values],
        'a_y': [row[3] for row in simulated_values],
        'a_x': [row[4] for row in simulated_values],
        'v_y': [row[5] for row in simulated_values],
        'v_x': [row[6] for row in simulated_values],
        'temperature': [row[7] for row in simulated_values],
        'pressure': [row[8] for row in simulated_values],
        'air_density': [row[9] for row in simulated_values],
        'q': [row[10] for row in simulated_values],
        'dynamic_viscosity': [row[11] for row in simulated_values],
        'reynolds_num': [row[12] for row in simulated_values],
        'Cd_rocket': [row[13] for row in simulated_values],
        'angle_to_vertical': [row[14] for row in simulated_values],
        })
    return dataset, liftoff_index, launch_rail_cleared_index, burnout_index, apogee_index

# Flight with airbrakes simulation function
def simulate_airbrakes_flight(pre_brake_flight, rocket = Prometheus, airbrakes = example_airbrakes, timestep = 0.001):
    # Initializations
    len_characteristic = rocket.L_rocket
    A_rocket = rocket.A_rocket
    mass = rocket.dry_mass
    Cd_rocket_at_Re = rocket.Cd_rocket_at_Re

    launchpad_pressure = pre_brake_flight.pressure.iloc[0]
    launchpad_temp = pre_brake_flight.temperature.iloc[0]
    
    num_flaps = airbrakes.num_flaps
    A_flap = airbrakes.A_flap
    Cd_brakes = airbrakes.Cd_brakes
    max_deployment_speed = airbrakes.max_deployment_speed
    A_brakes = num_flaps * A_flap

    pre_brake_flight['deployment_angle']=0

    height = pre_brake_flight['height'].iloc[-1]
    speed = pre_brake_flight['speed'].iloc[-1]
    v_y = pre_brake_flight['v_y'].iloc[-1]
    v_x = pre_brake_flight['v_x'].iloc[-1]
    time = pre_brake_flight['time'].iloc[-1]
    angle_to_vertical = np.arctan(v_x/v_y)

    deployment_angle = 0

    # for efficiency, may be removed when the simulation is made more accurate by the cd changing during the sim:
    A_Cd_brakes = A_brakes*Cd_brakes

    simulated_values = []
    previous_height = height
    while height >= previous_height:
        time += timestep

        temperature = temp_at_height(height,launchpad_temp)
        pressure = pressure_at_height(height,launchpad_temp, launchpad_pressure)
        air_density = air_density_fn(pressure, temperature)
        dynamic_viscosity = lookup_dynamic_viscosity(temperature)
        reynolds_num = (air_density*speed*len_characteristic)/dynamic_viscosity
        Cd_rocket = Cd_rocket_at_Re(reynolds_num)
        q = 0.5 * air_density * (speed**2)
        
        deployment_angle = min(45, deployment_angle + max_deployment_speed*timestep) 
        
        F_drag = q * (np.sin(np.deg2rad(deployment_angle))*A_Cd_brakes + A_rocket*Cd_rocket)
        a_y = -F_drag*np.cos(angle_to_vertical)/mass - F_gravity
        a_x = -F_drag*np.sin(angle_to_vertical)/mass
        v_y += a_y * timestep
        v_x += a_x * timestep
        speed = np.sqrt(v_y**2 + v_x**2)
        previous_height = height
        height += v_y * timestep

        angle_to_vertical = np.arctan(v_x/v_y)

        simulated_values.append([time, height, speed, a_y, a_x, v_y, v_x, temperature, pressure, air_density, q, dynamic_viscosity, reynolds_num, Cd_rocket, angle_to_vertical, deployment_angle])

    data = {
    'time': [row[0] for row in simulated_values],
    'height': [row[1] for row in simulated_values],
    'speed': [row[2] for row in simulated_values],
    'a_y': [row[3] for row in simulated_values],
    'a_x': [row[4] for row in simulated_values],
    'v_y': [row[5] for row in simulated_values],
    'v_x': [row[6] for row in simulated_values],
    'temperature': [row[7] for row in simulated_values],
    'pressure': [row[8] for row in simulated_values],
    'air_density': [row[9] for row in simulated_values],
    'q': [row[10] for row in simulated_values],
    'dynamic_viscosity': [row[11] for row in simulated_values],
    'reynolds_num': [row[12] for row in simulated_values],
    'Cd_rocket': [row[13] for row in simulated_values],
    'angle_to_vertical': [row[14] for row in simulated_values],
    'deployment_angle': [row[15] for row in simulated_values],
    }

    ascent = pd.concat([pre_brake_flight, pd.DataFrame(data)], ignore_index=True)
    ascent['q'] = 0.5 * air_density_fn(ascent['pressure'], ascent['temperature']) * (ascent['speed']**2)
    
    return ascent


if __name__ == "__main__":
    dataset, liftoff_index, launch_rail_cleared_index, burnout_index, apogee_index = simulate_flight()