import numpy as np
import constants as con


def temp_at_height(h, launchpad_temp):
    """
    Calculate the temperature at a given height above the launchpad.

    Args:
    - h (float): Height above the launchpad in meters.
    - launchpad_temp (float): Temperature at the launchpad in Celsius.

    Returns:
    - float: Temperature at the given height in Celsius.
    """
    return launchpad_temp - (h * con.T_lapse_rate)
def pressure_at_height(h, launchpad_temp, launchpad_pressure):
    """
    Calculate the air pressure at a given height above the launchpad.

    Args:
    - h (float): Height above the launchpad in meters.
    - launchpad_temp (float): Temperature at the launchpad in Celsius.
    - launchpad_pressure (float): Air pressure at the launchpad in Pascals.

    Returns:
    - float: Air pressure at the given height in Pascals.
    """
    return launchpad_pressure * pow(
        (1 - (h * con.T_lapse_rate / (launchpad_temp + 273.15))),
        (con.F_gravity / (con.R_specific_air * con.T_lapse_rate))
    )
def air_density_fn(pressure, temp):
    """
    Calculate the density of air at a given pressure and temperature.

    Args:
    - pressure (float): Pressure in Pascals.
    - temp (float): Temperature in Celsius.

    Returns:
    - float: Air density in kilograms per cubic meter.
    """
    return pressure / (con.R_specific_air * (temp + 273.15))
def lookup_dynamic_viscosity(temp):
    """
    Look up the dynamic viscosity of air at a given temperature.

    Args:
    - temp (float): Temperature in Celsius.

    Returns:
    - float: Dynamic viscosity in kilograms per meter-second.

    Source of lookup table: https://www.me.psu.edu/cimbala/me433/Links/Table_A_9_CC_Properties_of_Air.pdf
    """
    one_atm_air_dynamic_viscosity_lookup = {
        -150: 8.636 * pow(10, -6),
        -100: 1.189 * pow(10, -6),
        -50: 1.474 * pow(10, -5),
        -40: 1.527 * pow(10, -5),
        -30: 1.579 * pow(10, -5),
        -20: 1.630 * pow(10, -5),
        -10: 1.680 * pow(10, -5),
        0: 1.729 * pow(10, -5),
        5: 1.754 * pow(10, -5),
        10: 1.778 * pow(10, -5),
        15: 1.802 * pow(10, -5),
        20: 1.825 * pow(10, -5),
        25: 1.849 * pow(10, -5),
        30: 1.872 * pow(10, -5),
        35: 1.895 * pow(10, -5),
        40: 1.918 * pow(10, -5),
        45: 1.941 * pow(10, -5),
        50: 1.963 * pow(10, -5),
        60: 2.008 * pow(10, -5),
        70: 2.052 * pow(10, -5),
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
def mach_number_fn(v, temp):
    """
    Calculate the Mach number of an object moving in air at a given temperature.

    Args:
    - v (float): Velocity in meters per second.
    - temp (float): Temperature in Celsius.

    Returns:
    - float: Mach number (dimensionless).
    """
    return v / np.sqrt(1.4 * con.R_specific_air * (temp + 273.15))


def mass_at_time(time, dry_mass, fuel_mass_lookup):
    """
    Calculate the total mass of the rocket at a given time during motor burn.

    Args:
    - time (float): Time in seconds since motor ignition.
    - dry_mass (float): Dry mass of the rocket in kilograms.
    - fuel_mass_lookup (dict): Dictionary mapping times to fuel masses.

    Returns:
    - float: Total mass of the rocket at the specified time.
    """
    time_list = list(fuel_mass_lookup.keys())
    lower_time = max([t for t in time_list if t <= time])
    upper_time = min([t for t in time_list if t > time])
    lower_mass = fuel_mass_lookup[lower_time]
    upper_mass = fuel_mass_lookup[upper_time]
    return (dry_mass + lower_mass + (time - lower_time) * (upper_mass - lower_mass) / (upper_time - lower_time))
def thrust_at_time(time, engine_thrust_lookup):
    """
    Calculate the thrust of the rocket engine at a given time during motor burn.

    Args:
    - time (float): Time in seconds since motor ignition.
    - engine_thrust_lookup (dict): Dictionary mapping times to thrust values.

    Returns:
    - float: Thrust of the engine at the specified time.
    """
    time_list = list(engine_thrust_lookup.keys())
    lower_time = max([t for t in time_list if t <= time])
    upper_time = min([t for t in time_list if t > time])
    lower_thrust = engine_thrust_lookup[lower_time]
    upper_thrust = engine_thrust_lookup[upper_time]
    return lower_thrust + (time - lower_time) * (upper_thrust - lower_thrust) / (upper_time - lower_time)

# turn into function
def calculate_reynolds_number(air_density, speed, len_characteristic, dynamic_viscosity):
    """
    Calculate the Reynolds number of a solid moving through air.

    Args:
    - air_density (float): The density of the air.
    - speed (float): The relative speed of the solid and the air.
    - len_characteristic (float): The characteristic length of the solid.
    - dynamic_viscosity (float): The dynamic viscosity of the air.

    Returns:
    - float: The Reynolds number of the solid.
    """
    return (air_density * speed * len_characteristic) / dynamic_viscosity


def calculate_dynamic_pressure(air_density, speed):
    """
    Calculate the dynamic pressure imparted on a solid moving through a fluid.

    Args:
    - air_density (float): The density of the fluid.
    - speed (float): The relative speed of the solid and the fluid.

    Returns:
    - float: The dynamic pressure on the solid.
    """
    return 0.5 * air_density * (speed ** 2)
