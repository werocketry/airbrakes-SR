# contains parameters for instances of these classes: Rocket, LaunchConditions, Airbrakes
# also contains the functions that give the Cd of a rocket as a function of Re
import rocket_classes
import constants as con
import numpy as np

# Motor class configurations
Cesaroni_7579M1520_P = rocket_classes.Motor( 
    # source: https://www.thrustcurve.org/simfiles/5f4294d20002e900000006b1/
    dry_mass = 2.981,
    thrust_curve = {
        0: 0,
        0.04: 1427.8,
        0.082: 1706.39,
        0.176: 1620.49,
        0.748: 1734.25,
        1.652: 1827.11,
        2.676: 1715.68,
        3.89: 1423.15,
        4.399: 1404.58,
        4.616: 661.661,
        4.877: 69.649,
        4.897: 0
    },
    fuel_mass_curve = {
        0: 3.737,
        0.04: 3.72292,
        0.082: 3.69047,
        0.176: 3.61337,
        0.748: 3.14029,
        1.652: 2.34658,
        2.676: 1.45221,
        3.89: 0.512779,
        4.399: 0.157939,
        4.616: 0.0473998,
        4.877: 0.000343417,
        4.897: 0
    }
)

Cesaroni_7450M2505_P = rocket_classes.Motor(
    dry_mass = 2.866, # source: http://www.pro38.com/products/pro98/motor/MotorData.php?prodid=7450M2505-P
    thrust_curve = { # source: https://www.thrustcurve.org/simfiles/5f4294d20002e900000005a0/
        0: 0,
        0.12: 2600,
        0.21: 2482,
        0.6: 2715,
        0.9: 2876,
        1.2: 2938,
        1.5: 2889,
        1.8: 2785,
        2.1: 2573,
        2.4: 2349,
        2.7: 2182,
        2.99: 85,
        3: 0
    },
    fuel_mass_curve = { # source: https://www.thrustcurve.org/simfiles/5f4294d20002e900000005a0/
        0: 3.423,
        0.12: 3.35069,
        0.21: 3.24469,
        0.6: 2.77495,
        0.9: 2.38622,
        1.2: 1.98198,
        1.5: 1.57684,
        1.8: 1.18234,
        2.1: 0.809811,
        2.4: 0.467594,
        2.7: 0.152563,
        2.99: 0.000196996,
        3: 0
    }
)

our_Cesaroni_7450M2505_P = rocket_classes.Motor(
    dry_mass = 2.762, # from massing our dry parts
    # TODO: mass the tube once cleaned, as well as the thrust plate, and update the mass budget and this value
    thrust_curve = { # source: https://www.thrustcurve.org/simfiles/5f4294d20002e900000005a0/
        0: 0,
        0.12: 2600,
        0.21: 2482,
        0.6: 2715,
        0.9: 2876,
        1.2: 2938,
        1.5: 2889,
        1.8: 2785,
        2.1: 2573,
        2.4: 2349,
        2.7: 2182,
        2.99: 85,
        3: 0
    },
    fuel_mass_curve = { # source: https://www.thrustcurve.org/simfiles/5f4294d20002e900000005a0/
        0: 3.423,
        0.12: 3.35069,
        0.21: 3.24469,
        0.6: 2.77495,
        0.9: 2.38622,
        1.2: 1.98198,
        1.5: 1.57684,
        1.8: 1.18234,
        2.1: 0.809811,
        2.4: 0.467594,
        2.7: 0.152563,
        2.99: 0.000196996,
        3: 0
    }
)

# Cd functions


# TODO: see if I can get a proper Cd(Ma) for Prometheus instead of this conversion from the Cd(Re) function. Clean this whole thing up
def Prometheus_Cd_at_Re(Re):
    """
    CFD done by Niall in early 2021 using the Prometheus CAD as it was at that time. k-ω model.
    """
    if Re <= 1e7:
        return 0.42
    elif Re <= 2.8e7:
        return 0.42 - (Re - 1e7) * (0.42 - 0.4) / (2.8e7 - 1e7)
    elif Re <= 5e7:
        return 0.4 - (Re - 2.8e7) * (0.4 - 0.31) / (5e7 - 2.8e7)
    else:
        return 0.31

# rough translation of Cd(Re) into a Cd(mach) function
# assumptions:
air_temp_for_mach = 20 + 273.15 # assumed constant at 20C (temp about halfway through flight)
dynamic_viscosity_for_mach = 1.85e-5 # assumed constant at 1.85e-5 (dynamic viscosity at 20C)
air_density_for_mach = 0.85 # assumed constant at 0.85 kg/m^3 (air density about halfway through flight)
L_Prometheus = 2.229  # length of Prometheus in m # TODO: measure to double check
# mach = speed / np.sqrt(1.4 * con.R_specific_air * temp)
# Re = air_density * speed * len_characteristic / dynamic_viscosity
# Re = air_density * mach * len_characteristic * np.sqrt(1.4 * con.R_specific_air * temp) / dynamic_viscosity

def Prometheus_Cd_at_Ma(mach):
    Re = air_density_for_mach * mach * L_Prometheus * np.sqrt(1.4 * con.R_specific_air * air_temp_for_mach) / dynamic_viscosity_for_mach
    return Prometheus_Cd_at_Re(Re)

# OpenRocket Cd functions TODO: update to take Ma
"""
For demonstrative purposes, here's the Cd function from the ork files for Prometheus and Hyperion. They are basically indistinguishable.

Using the Prometheus one to project the Prometheus flight gives terrible results, doubling the error to about 2000 ft (at least as the sim and ork outputs stood on March 26th). 
"""
def Prometheus_Cd_function_orkPrometheus_V3_CADUPD(Re):
    """
    Drag coefficient curve given by Prometheus_V3_CADUPD.ork, on flight with Prometheus' launch conditions, but no wind (ascent only). Far less accurate than simply using the Prometheus Cd function.
    """
    if Re <= 2.2e6:
        return 0.436
    elif Re <= 5.01e6:
        return 0.436 + (Re - 2.2e6) * (0.438 - 0.436) / (5.01e6 - 2.2e6)
    elif Re <= 1.12e7:
        return 0.438 + (Re - 5.01e6) * (0.445 - 0.438) / (1.12e7 - 5.01e6)
    elif Re <= 1.83e7:
        return 0.445 + (Re - 1.12e7) * (0.47 - 0.445) / (1.83e7 - 1.12e7)
    elif Re <= 2.46e7:
        return 0.47 + (Re - 1.83e7) * (0.496 - 0.47) / (2.46e7 - 1.83e7)
    elif Re <= 3.02e7:
        return 0.496 + (Re - 2.46e7) * (0.528 - 0.496) / (3.02e7 - 2.46e7)
    elif Re <= 3.61e7:
        return 0.528 + (Re - 3.02e7) * (0.576 - 0.528) / (3.61e7 - 3.02e7)
    elif Re <= 3.88e7:
        return 0.576 + (Re - 3.61e7) * (0.61 - 0.576) / (3.88e7 - 3.61e7)
    elif Re <= 4.14e7:
        return 0.61 + (Re - 3.88e7) * (0.657 - 0.61) / (4.14e7 - 3.88e7)
    elif Re <= 4.42e7:
        return 0.657 + (Re - 4.14e7) * (0.652 - 0.657) / (4.42e7 - 4.14e7)
    else:
        return 0.65
def Hyperion_Cd_function_orkV7(Re):
    """
    Drag coefficient curve given by HyperionV7.ork, on flight with Prometheus' launch conditions, but no wind (ascent only). Likely far less accurate than simply using the Prometheus Cd function.
    """
    if Re <= 2.2e6:
        return 0.436
    elif Re <= 7.64e6:
        return 0.436 + (Re - 2.2e6) * (0.44 - 0.436) / (7.64e6 - 2.2e6)
    elif Re <= 1.75e7:
        return 0.44 + (Re - 7.64e6) * (0.467 - 0.44) / (1.75e7 - 7.64e6)
    elif Re <= 2.76e7:
        return 0.467 + (Re - 1.75e7) * (0.512 - 0.467) / (2.76e7 - 1.75e7)
    elif Re <= 3.41e7:
        return 0.512 + (Re - 2.76e7) * (0.557 - 0.512) / (3.41e7 - 2.76e7)
    elif Re <= 3.86e7:
        return 0.557 + (Re - 3.41e7) * (0.606 - 0.557) / (3.86e7 - 3.41e7)
    elif Re <= 4.14e7:
        return 0.606 + (Re - 3.86e7) * (0.657 - 0.606) / (4.14e7 - 3.86e7)
    elif Re <= 4.48e7:
        return 0.657 + (Re - 4.14e7) * (0.651 - 0.657) / (4.48e7 - 4.14e7)
    else:
        return 0.65

# Hyperion Cd function

# TODO: add Hyperion Cd function(s) here when Shelby's done CFD
# TODO: add a Cd function from some other team's CFD, see how different it actually is to get an idea of how important it is to have a very accurate Cd function


# Rocket class configurations
# TODO: add another team's rocket and Cd function, test our sim with it
Hyperion_2024_03_20 = {
    # "L_rocket": 2.71,
    # TODO: when more parts finished, update L_rocket
    "A_rocket": 0.015326,# + 0.13 * 0.012 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 1.2cm (thickness of Sapphire fins, span as planned)
        # as best I can tell, it was only the area of the body tube that was fed to Star-CCM+ for the Cd calculation
    # TODO: when fins made, update A_rocket
    # TODO: when body tubes sanded, update A_rocket
    "rocket_mass": 13.462+2,
    # TODO: continuous refinement of mass budget and updating of the first value. second value is guess at additional mass we'll add to it (heavier infills, coatings, literal weights, etc.) to bring our pre-airbrakes apogee down to ~11k ft
    "motor": our_Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69 # m, distance from bottom of rocket to second rail button, was what Prometheus had
    # TODO: switch to Hyperion's once aero has a final design
}

Hyperion_2024_03_19 = {
    # "L_rocket": 2.70,
    "A_rocket": 0.015326 + 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
    "rocket_mass": 13.449,
    "motor": our_Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69 # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Hyperion_2024_03_05 = {
    # "L_rocket": 2.70,
    "A_rocket": 0.015326 + 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
    "rocket_mass": 13.917,
    "motor": our_Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69 # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Hyperion_2024_02_20 = {
    # "L_rocket": 2.70,
    "A_rocket": 0.015326 + 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
    "rocket_mass": 14.29,
    "motor": Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69 # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Hyperion_2024_02_04 = {
    # "L_rocket": 2.59,
    "A_rocket": 0.015326 + 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
    "rocket_mass": 14.24,
    "motor": Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69  # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Hyperion_2024_01_24 = {
    # "L_rocket": 2.59,
    "A_rocket": 0.015326 + 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
    "rocket_mass": 14.54,
    "motor": Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69  # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Prometheus = rocket_classes.Rocket(
    # L_rocket = 2.229,  # length of Prometheus in m # TODO: measure to double check
    A_rocket = 0.015326, #+ 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
        # as best I can tell, it was only the area of the body tube that was fed to Star-CCM+ for the Cd calculation
    rocket_mass = 13.93,  # kg, from (TODO: CAD? final physical rocket mass? were they the same at the end?)
    motor = Cesaroni_7579M1520_P,
    Cd_rocket_at_Ma = Prometheus_Cd_at_Ma,
    h_second_rail_button = 0.69  # m
)

# LaunchConditions class configurations
Prometheus_launch_conditions = rocket_classes.LaunchConditions(
    launchpad_pressure = 86400,  # Pa, what it was at Prometheus' launch
    launchpad_temp = 34,  # deg C, what it was at Prometheus' launch
    L_launch_rail = 5.18,  # m, ESRA provides a 5.18m rail
    launch_angle = 80  # deg from horizontal. Niall said Prometheus was set up at 10 deg off of the vertical
)

# Airbrakes class configurations
airbrakes_model_2024_01_14 = rocket_classes.Airbrakes(
    num_flaps = 3,
    A_flap = 0.0022505,  # current area in CAD. Maryland's last year was 0.0064516, which we'll probably have a similar configuration to
    Cd_brakes = 1,  # about what other teams had. rough
    max_deployment_speed = 7.5,  # deg/s
    max_deployment_angle = 41.35  # deg
)

airbrakes_model_2024_03_10 = rocket_classes.Airbrakes(
    num_flaps = 3,
    A_flap = 0.0045,  # m^2  current estimate. Maryland's last year was 0.0064516, which we'll probably have a similar configuration to
    Cd_brakes = 1,  # about what other teams had. rough
    max_deployment_speed = 5.5,  # deg/s
    max_deployment_angle = 41.35  # deg
)

airbrakes_model_2024_03_20 = rocket_classes.Airbrakes(
    num_flaps = 3,
    A_flap = 0.00395,  # m^2  flap area
    # TODO: still needs final sanding, so check again later, but should be super close
    # TODO: look at how some being covered by the tube affects the area (will be incredibly minor)
    Cd_brakes = 1,  # about what other teams had. rough
    # TODO: verify Cd by checking other teams' values again
    max_deployment_speed = 5.5,  # deg/s
    # TODO: check with Cam on how to make more accurate (likely not to be exactly linear?)
    max_deployment_angle = 45  # deg
)

# Set the default Hyperion configuration
Hyperion = rocket_classes.Rocket(**Hyperion_2024_03_20)
current_airbrakes_model = airbrakes_model_2024_03_20