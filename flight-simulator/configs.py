# contains parameters for instances of these classes: Rocket, LaunchConditions, Airbrakes
# also contains the functions that give the Cd of a rocket as a function of Re
import rocket_classes

# Motor class configurations
Cesaroni_7579M1520_P = rocket_classes.Motor( # source: https://www.thrustcurve.org/simfiles/5f4294d20002e900000006b1/
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

# Cd functions
def Prometheus_Cd_function(Re):
    """
    THIS IS FROM THE OLD 2020-2021 CFD. Get Shelby's new CFD based on the final Promtheus CAD and see if it's different. Likely switch to that if it is (keep this as legacy here because why not).
    """
    # use k-ω model from Prometheus CFD sims
    if Re < 1e7:
        return 0.42
    elif Re < 2.8e7:
        return 0.42 - (Re - 1e7) * (0.42 - 0.4) / (2.8e7 - 1e7)
    elif Re < 5e7:
        return 0.4 - (Re - 2.8e7) * (0.4 - 0.31) / (5e7 - 2.8e7)
    else:
        return 0.31

# add Hyperion Cd function(s) here when Shelby's done CFD


# Rocket class configurations
Hyperion_2024_02_20 = {
    "L_rocket": 2.70, # CHECK WITH UPDATED CAD
    "A_rocket": 0.015326 + 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
    "rocket_mass": 14.29,
    "motor": Cesaroni_7450M2505_P,
    "Cd_rocket_at_Re": Prometheus_Cd_function,
    "h_second_rail_button": 0.69  # TBU # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Hyperion_2024_02_04 = {
    "L_rocket": 2.59,
    "A_rocket": 0.015326 + 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
    "rocket_mass": 14.24,
    "motor": Cesaroni_7450M2505_P,
    "Cd_rocket_at_Re": Prometheus_Cd_function,
    "h_second_rail_button": 0.69  # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Hyperion_2024_01_24 = {
    "L_rocket": 2.59,
    "A_rocket": 0.015326 + 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
    "rocket_mass": 14.54,
    "motor": Cesaroni_7450M2505_P,
    "Cd_rocket_at_Re": Prometheus_Cd_function,
    "h_second_rail_button": 0.69  # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Prometheus = rocket_classes.Rocket(
    L_rocket = 2.229,  # length of Prometheus in m # measure to double check
    A_rocket = 0.015326 + 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
    rocket_mass = 13.93,  # kg, from (CAD? final physical rocket mass? were they the same at the end?)
    motor = Cesaroni_7579M1520_P,
    Cd_rocket_at_Re = Prometheus_Cd_function,
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

# Set the default Hyperion configuration
Hyperion = rocket_classes.Rocket(**Hyperion_2024_02_20)
current_airbrakes_model = airbrakes_model_2024_01_14