# contains parameters for instances of these classes: Rocket, LaunchConditions, Airbrakes
# also contains the functions that give the Cd of a rocket as a function of Re
from rocketflightsim import rocket_classes
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

our_Cesaroni_7450M2505_P = Cesaroni_7450M2505_P
our_Cesaroni_7450M2505_P.dry_mass = 2.310 # NOT including thrust plate, which is included in the rocket mass

# Rocket Cd functions
def Prometheus_Cd_at_Ma(mach):
    """CFD done by Niall in early 2021 using the Prometheus CAD as it was at that time in Star-CCM+. k-ω model."""
    if mach <= 0.15:
        return 0.422
    elif mach <= 0.45:
        return 0.422 + (mach - 0.15) * (0.38 - 0.422) / (0.45 - 0.15)
    elif mach <= 0.77:
        return 0.38 + (mach - 0.45) * (0.32 - 0.38) / (0.77 - 0.45)
    elif mach <= 0.82:
        return 0.32 + (mach - 0.77) * (0.3 - 0.32) / (0.82 - 0.77)
    elif mach <= 0.88:
        return 0.3 + (mach - 0.82) * (0.3 - 0.3) / (0.88 - 0.82)
    elif mach <= 0.94:
        return 0.3 + (mach - 0.88) * (0.32 - 0.3) / (0.94 - 0.88)
    elif mach <= 0.99:
        return 0.32 + (mach - 0.94) * (0.37 - 0.32) / (0.99 - 0.94)
    elif mach <= 1.04:
        return 0.37 + (mach - 0.99) * (0.44 - 0.37) / (1.04 - 0.99)
    elif mach <= 1.24:
        return 0.44 + (mach - 1.04) * (0.43 - 0.44) / (1.24 - 1.04)
    elif mach <= 1.33:
        return 0.43 + (mach - 1.24) * (0.42 - 0.43) / (1.33 - 1.24)
    elif mach <= 1.49:
        return 0.42 + (mach - 1.33) * (0.39 - 0.42) / (1.49 - 1.33)
    else:
        return 0.39

""" ORK Cd functions
For demonstrative purposes, here's the Cd functions from the ork files for Prometheus and Hyperion. They are basically indistinguishable.

Using the Prometheus one to project the Prometheus flight gives terrible results, doubling the error to about 2000 ft (at least as the sim and ork outputs stood on March 26th). 

Others are also experiencing underestimation of drag in their OpenRocket simulations: 
    - https://discord.com/channels/855522432945618965/855533557996453888/1017453223340150805
"""
def Prometheus_Cd_function_orkPrometheus_V3_CADUPD(Ma):
    """
    Drag coefficient curve given by Prometheus_V3_CADUPD.ork, on flight with Prometheus' launch conditions, but no wind (ascent only). Far less accurate than simply using the Prometheus Cd function.
    """
    if Ma <= 0.033:
        return 0.422
    elif Ma <= 0.048:
        return 0.422 + (Ma - 0.033) * (0.405 - 0.422) / (0.048 - 0.033)
    elif Ma <= 0.1:
        return 0.405 + (Ma - 0.048) * (0.406 - 0.405) / (0.1 - 0.048)
    elif Ma <= 0.205:
        return 0.406 + (Ma - 0.1) * (0.411 - 0.406) / (0.205 - 0.1)
    elif Ma <= 0.314:
        return 0.411 + (Ma - 0.205) * (0.421 - 0.411) / (0.314 - 0.205)
    elif Ma <= 0.451:
        return 0.421 + (Ma - 0.314) * (0.44 - 0.421) / (0.451 - 0.314)
    elif Ma <= 0.602:
        return 0.44 + (Ma - 0.451) * (0.472 - 0.44) / (0.602 - 0.451)
    elif Ma <= 0.687:
        return 0.472 + (Ma - 0.602) * (0.499 - 0.472) / (0.687 - 0.602)
    elif Ma <= 0.803:
        return 0.499 + (Ma - 0.687) * (0.552 - 0.499) / (0.803 - 0.687)
    elif Ma <= 0.824:
        return 0.552 + (Ma - 0.803) * (0.565 - 0.552) / (0.824 - 0.803)
    elif Ma <= 0.864:
        return 0.565 + (Ma - 0.824) * (0.596 - 0.565) / (0.864 - 0.824)
    elif Ma <= 0.891:
        return 0.596 + (Ma - 0.864) * (0.625 - 0.596) / (0.891 - 0.864)
    elif Ma <= 0.904:
        return 0.625 + (Ma - 0.891) * (0.637 - 0.625) / (0.904 - 0.891)
    elif Ma <= 0.959:
        return 0.637 + (Ma - 0.904) * (0.631 - 0.637) / (0.959 - 0.904)
    else:
        return 0.63
def Hyperion_Cd_function_orkV7(Ma):
    """
    Drag coefficient curve given by HyperionV7.ork, on flight with Prometheus' launch conditions, but no wind (ascent only). Likely far less accurate than simply using the Prometheus Cd function.
    """
    if Ma <= 0.019:
        return 0.494
    elif Ma <= 0.049:
        return 0.494 + (Ma - 0.019) * (0.436 - 0.494) / (0.049 - 0.019)
    elif Ma <= 0.104:
        return 0.436 + (Ma - 0.049) * (0.438 - 0.436) / (0.104 - 0.049)
    elif Ma <= 0.26:
        return 0.438 + (Ma - 0.104) * (0.447 - 0.438) / (0.26 - 0.104)
    elif Ma <= 0.435:
        return 0.447 + (Ma - 0.26) * (0.468 - 0.447) / (0.435 - 0.26)
    elif Ma <= 0.568:
        return 0.468 + (Ma - 0.435) * (0.497 - 0.468) / (0.568 - 0.435)
    elif Ma <= 0.714:
        return 0.497 + (Ma - 0.568) * (0.535 - 0.497) / (0.714 - 0.568)
    elif Ma <= 0.81:
        return 0.535 + (Ma - 0.714) * (0.58 - 0.535) / (0.81 - 0.714)
    elif Ma <= 0.857:
        return 0.58 + (Ma - 0.81) * (0.612 - 0.58) / (0.857 - 0.81)
    elif Ma <= 0.9:
        return 0.612 + (Ma - 0.857) * (0.657 - 0.612) / (0.9 - 0.857)
    elif Ma <= 0.969:
        return 0.657 + (Ma - 0.9) * (0.65 - 0.657) / (0.969 - 0.9)
    else:
        return 0.65

# Hyperion Cd functions
def Hyperion_Cd_function_RASAeroII_2024_06_10(Ma):
    if Ma <= 0.01:
        return 0.41
    elif Ma <= 0.02:
        return 0.41 + (Ma - 0.01) * (0.415 - 0.41) / (0.02 - 0.01)
    elif Ma <= 0.03:
        return 0.415 + (Ma - 0.02) * (0.406 - 0.415) / (0.03 - 0.02)
    elif Ma <= 0.04:
        return 0.406 + (Ma - 0.03) * (0.403 - 0.406) / (0.04 - 0.03)
    elif Ma <= 0.05:
        return 0.403 + (Ma - 0.04) * (0.402 - 0.403) / (0.05 - 0.04)
    elif Ma <= 0.1:
        return 0.402 + (Ma - 0.05) * (0.393 - 0.402) / (0.1 - 0.05)
    elif Ma <= 0.15:
        return 0.393 + (Ma - 0.1) * (0.386 - 0.393) / (0.15 - 0.1)
    elif Ma <= 0.2:
        return 0.386 + (Ma - 0.15) * (0.38 - 0.386) / (0.2 - 0.15)
    elif Ma <= 0.25:
        return 0.38 + (Ma - 0.2) * (0.375 - 0.38) / (0.25 - 0.2)
    elif Ma <= 0.3:
        return 0.375 + (Ma - 0.25) * (0.372 - 0.375) / (0.3 - 0.25)
    elif Ma <= 0.35:
        return 0.372 + (Ma - 0.3) * (0.37 - 0.372) / (0.35 - 0.3)
    elif Ma <= 0.4:
        return 0.37 + (Ma - 0.35) * (0.368 - 0.37) / (0.4 - 0.35)
    elif Ma <= 0.45:
        return 0.368 + (Ma - 0.4) * (0.366 - 0.368) / (0.45 - 0.4)
    elif Ma <= 0.5:
        return 0.366 + (Ma - 0.45) * (0.365 - 0.366) / (0.5 - 0.45)
    elif Ma <= 0.55:
        return 0.365 + (Ma - 0.5) * (0.364 - 0.365) / (0.55 - 0.5)
    elif Ma <= 0.6:
        return 0.364 + (Ma - 0.55) * (0.365 - 0.364) / (0.6 - 0.55)
    elif Ma <= 0.65:
        return 0.365 + (Ma - 0.6) * (0.367 - 0.365) / (0.65 - 0.6)
    elif Ma <= 0.7:
        return 0.367 + (Ma - 0.65) * (0.369 - 0.367) / (0.7 - 0.65)
    elif Ma <= 0.75:
        return 0.369 + (Ma - 0.7) * (0.371 - 0.369) / (0.75 - 0.7)
    elif Ma <= 0.8:
        return 0.371 + (Ma - 0.75) * (0.373 - 0.371) / (0.8 - 0.75)
    elif Ma <= 0.85:
        return 0.373 + (Ma - 0.8) * (0.376 - 0.373) / (0.85 - 0.8)
    elif Ma <= 0.9:
        return 0.376 + (Ma - 0.85) * (0.378 - 0.376) / (0.9 - 0.85)
    elif Ma <= 0.91:
        return 0.378 + (Ma - 0.9) * (0.38 - 0.378) / (0.91 - 0.9)
    elif Ma <= 0.92:
        return 0.38 + (Ma - 0.91) * (0.388 - 0.38) / (0.92 - 0.91)
    elif Ma <= 0.93:
        return 0.388 + (Ma - 0.92) * (0.403 - 0.388) / (0.93 - 0.92)
    elif Ma <= 0.94:
        return 0.403 + (Ma - 0.93) * (0.422 - 0.403) / (0.94 - 0.93)
    elif Ma <= 0.95:
        return 0.422 + (Ma - 0.94) * (0.441 - 0.422) / (0.95 - 0.94)
    elif Ma <= 0.96:
        return 0.441 + (Ma - 0.95) * (0.46 - 0.441) / (0.96 - 0.95)
    elif Ma <= 0.97:
        return 0.46 + (Ma - 0.96) * (0.479 - 0.46) / (0.97 - 0.96)
    elif Ma <= 0.98:
        return 0.479 + (Ma - 0.97) * (0.498 - 0.479) / (0.98 - 0.97)
    elif Ma <= 0.99:
        return 0.498 + (Ma - 0.98) * (0.517 - 0.498) / (0.99 - 0.98)
    elif Ma <= 1:
        return 0.517 + (Ma - 0.99) * (0.536 - 0.517) / (1 - 0.99)
    elif Ma <= 1.01:
        return 0.536 + (Ma - 1) * (0.555 - 0.536) / (1.01 - 1)
    elif Ma <= 1.02:
        return 0.555 + (Ma - 1.01) * (0.574 - 0.555) / (1.02 - 1.01)
    elif Ma <= 1.03:
        return 0.574 + (Ma - 1.02) * (0.593 - 0.574) / (1.03 - 1.02)
    elif Ma <= 1.04:
        return 0.593 + (Ma - 1.03) * (0.612 - 0.593) / (1.04 - 1.03)
    elif Ma <= 1.05:
        return 0.612 + (Ma - 1.04) * (0.631 - 0.612) / (1.05 - 1.04)
    elif Ma <= 1.06:
        return 0.631 + (Ma - 1.05) * (0.633 - 0.631) / (1.06 - 1.05)
    elif Ma <= 1.07:
        return 0.633 + (Ma - 1.06) * (0.634 - 0.633) / (1.07 - 1.06)
    else:
        return 0.634

# Rocket class configurations
Hyperion_2024_06_17_1900 = {
    "A_rocket": 0.015326, # 5.5" diameter circle's area in m^2
    # TODO: calculate actual area with final tube OD
    "rocket_mass": 18.261, # a bit off at the moment
    # TODO: final massing soon
    "motor": our_Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Hyperion_Cd_function_RASAeroII_2024_06_10,
    # TODO: further refinement of Cd function
    "h_second_rail_button": 1.13 # m, distance from bottom of rocket to second rail button
}

Prometheus = rocket_classes.Rocket(
    A_rocket = 0.015326, #+ 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
        # I think it was only the area of the body tube that was fed to Star-CCM+ for the Cd calculation
            # but maybe not?? TODO: look into more
    rocket_mass = 13.93,  # kg, from (TODO: CAD? final physical rocket mass? were they the same at the end?)
    motor = Cesaroni_7579M1520_P,
    Cd_rocket_at_Ma = Prometheus_Cd_at_Ma,
    h_second_rail_button = 0.69  # m
)

# LaunchConditions class configuration for Spaceport America Cup
    # See RFS for how the following values were determined
    # TODO: have this read from RFS instead of defined here
T_lapse_rate_SA = -0.00817  # K/m
L_launch_rail_ESRA_provided_SAC = 5.18  # m
launchpad_pressure_SAC = 86400  # Pa
launchpad_temp_SAC = 35  # deg C
latitude_SA = 32.99  # deg, Spaceport America's latitude
altitude_SA = 1401  # m, Spaceport America's elevation
launch_rail_elevation_SAC = 86  # deg from horizontal

Spaceport_America_avg_launch_conditions = rocket_classes.LaunchConditions(
    launchpad_pressure = launchpad_pressure_SAC,
    launchpad_temp = launchpad_temp_SAC,
    L_launch_rail = L_launch_rail_ESRA_provided_SAC,
    launch_rail_elevation = launch_rail_elevation_SAC,
    local_T_lapse_rate = T_lapse_rate_SA,
    latitude = latitude_SA,
    altitude = altitude_SA
)

Prometheus_launch_conditions = rocket_classes.LaunchConditions(
    launchpad_pressure = launchpad_pressure_SAC,  # Pa
    launchpad_temp = 34,  # deg C, from https://www.timeanddate.com/weather/@5492576/historic?month=6&year=2023
    L_launch_rail = L_launch_rail_ESRA_provided_SAC,
    launch_rail_elevation = 80,  # deg from horizontal. Niall said Prometheus was set up at 10 deg off of the vertical
    local_T_lapse_rate = T_lapse_rate_SA,
    latitude = latitude_SA,
    altitude = altitude_SA
)

# LaunchConditions for Hyperion for SAC 2024
Hyperion_launch_conditions = rocket_classes.LaunchConditions(
    launchpad_pressure = launchpad_pressure_SAC, # TODO: update on Tues
    launchpad_temp = launchpad_temp_SAC, # TODO: update on Tues
    L_launch_rail = L_launch_rail_ESRA_provided_SAC,
    launch_rail_elevation = launch_rail_elevation_SAC,
    launch_rail_direction = 0, # TODO: update
    local_T_lapse_rate = T_lapse_rate_SA,
    latitude = latitude_SA,
    altitude = altitude_SA,
    mean_wind_speed = 0,# TODO: update
    wind_heading = 0# TODO: update
)

# Airbrakes class configurations
airbrakes_model_2024_06_17_1900 = rocket_classes.Airbrakes(
    num_flaps = 3,
    A_flap = 0.004215,  # m^2  flap area (47.1 mm * 89.5 mm)
    Cd_brakes = 1,  # flat plate, TODO: TBC
    max_deployment_rate = 5.5,  # deg/s
    # TODO: update rate after loaded testing
    # TODO: consider retraction speed being significantly faster than deployment speed, incorporate being closed for apogee into sims
    max_deployment_angle = 45  # deg
)
# Set the default Hyperion configuration
Hyperion = rocket_classes.Rocket(**Hyperion_2024_06_17_1900)
current_airbrakes_model = airbrakes_model_2024_06_17_1900