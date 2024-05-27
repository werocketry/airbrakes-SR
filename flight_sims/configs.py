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

our_Cesaroni_7450M2505_P = rocket_classes.Motor(
    dry_mass = 2.761, # from massing our dry parts
    # TODO: mass fabricated thrust plate, and update the mass budget and this value
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

# TODO: when Shelby's done redoing Prometheus CFD, add her function here, and maybe try to verify A_rocket that should be used when using Niall's function

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

# TODO: maybe try a RASAero II Cd function, see https://www.reddit.com/r/rocketry/comments/18si1ws/comment/kf8iq38/

# Hyperion Cd function

# TODO: add Hyperion Cd function(s) here when Shelby's done CFD
# TODO: add a Cd function from some other team's CFD, see how different from ours it actually is to get an idea of how important it is to have a very accurate Cd function


# Rocket class configurations
Hyperion_2024_05_26 = {
    "A_rocket": 0.015326,# + 0.13 * 0.012 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 1.2cm (thickness of Sapphire fins, span as planned)
        # I think it was only the area of the body tube that was fed to Star-CCM+ for the Cd calculation
        # once using Shelby's CFD model, ensure that the area used here is the same as plugged into Ansys Fluent for its conversion of drag force to Cd
    "rocket_mass": 17.772,
    # TODO: continuous refinement of mass budget and updating of value
    "motor": our_Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69 # m, distance from bottom of rocket to second rail button, was what Prometheus had
    # TODO: switch to Hyperion's once installed on rocket and measured
}

Hyperion_2024_05_25 = {
    "A_rocket": 0.015326,# + 0.13 * 0.012 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 1.2cm (thickness of Sapphire fins, span as planned)
        # I think it was only the area of the body tube that was fed to Star-CCM+ for the Cd calculation
        # once using Shelby's CFD model, ensure that the area used here is the same as plugged into Ansys Fluent for its conversion of drag force to Cd
    "rocket_mass": 17.149,
    "motor": our_Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69 # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Hyperion_2024_05_08 = {
    "A_rocket": 0.015326,# + 0.13 * 0.012 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 1.2cm (thickness of Sapphire fins, span as planned)
        # I think it was only the area of the body tube that was fed to Star-CCM+ for the Cd calculation
        # once using Shelby's CFD model, ensure that the area used here is the same as plugged into Ansys Fluent for its conversion of drag force to Cd
    "rocket_mass": 14.763+1, # first value is expected mass of all planned components, second is guess at additional mass to add to it (heavier infills, coatings, literal weights, etc.) to bring our pre-airbrakes apogee down to ~11k ft
    "motor": our_Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69 # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Hyperion_2024_04_13 = {
    "A_rocket": 0.015326,# + 0.13 * 0.012 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 1.2cm (thickness of Sapphire fins, span as planned)
        # I think it was only the area of the body tube that was fed to Star-CCM+ for the Cd calculation
        # once using Shelby's CFD model, ensure that the area used here is the same as plugged into Ansys Fluent for its conversion of drag force to Cd
    "rocket_mass": 13.222+3, # first value is expected mass of all planned components, second is guess at additional mass to add to it (heavier infills, coatings, literal weights, etc.) to bring our pre-airbrakes apogee down to ~11k ft
    "motor": our_Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69 # m, distance from bottom of rocket to second rail button, was what Prometheus had
}

Hyperion_2024_03_20 = {
    # "L_rocket": 2.71, # when more parts finished, update L_rocket
    "A_rocket": 0.015326,# + 0.13 * 0.012 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 1.2cm (thickness of Sapphire fins, span as planned)
        # I think it was only the area of the body tube that was fed to Star-CCM+ for the Cd calculation
        # once using Shelby's CFD model, ensure that the area used here is the same as plugged into Ansys Fluent for its conversion of drag force to Cd
    "rocket_mass": 13.462+2, # first value is expected mass of all planned components, second is guess at additional mass to add to it (heavier infills, coatings, literal weights, etc.) to bring our pre-airbrakes apogee down to ~11k ft
    "motor": our_Cesaroni_7450M2505_P,
    "Cd_rocket_at_Ma": Prometheus_Cd_at_Ma,
    "h_second_rail_button": 0.69 # m, distance from bottom of rocket to second rail button, was what Prometheus had
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
    # L_rocket = 2.229,  # length of Prometheus in m # measure to double check
    A_rocket = 0.015326, #+ 0.13 * 0.008 * 3,  # 5.5" diameter circle's area in m^2, plus 3 fins with span of 13cm and thickness of 0.8cm
        # I think it was only the area of the body tube that was fed to Star-CCM+ for the Cd calculation
            # but maybe not?? TODO: look into more
    rocket_mass = 13.93,  # kg, from (TODO: CAD? final physical rocket mass? were they the same at the end?)
    motor = Cesaroni_7579M1520_P,
    Cd_rocket_at_Ma = Prometheus_Cd_at_Ma,
    h_second_rail_button = 0.69  # m
)

# LaunchConditions class configuration for Spaceport America Cup
T_lapse_rate_SA = -0.00817  # K/m
""" How T_lapse_rate at Spaceport America was determined

Only one source was found with the lapse rate for Spaceport America:
    - https://egusphere.copernicus.org/preprints/2023/egusphere-2023-633/egusphere-2023-633.pdf
    - luckily, they took their measurements in June
    - The lapse rates for the stratosphere for each of three flights were reported as follows:
        - June 1st 2021 -8.4 K/km
        - June 4th 2021 -7.9 K/km
        - June 6th 2021 -8.2 K/km
    - An average of these is what was chosen for the simulation
    - The linear lapse rate was valid for the first 10 km AGL

For future reference, it should be noted that time of year has a large effect on the lapse rate, as reported in:
    - https://mdpi-res.com/d_attachment/remotesensing/remotesensing-14-00162/article_deploy/remotesensing-14-00162.pdf?version=1640917080
    - https://hwbdocs.env.nm.gov/Los%20Alamos%20National%20Labs/TA%2004/2733.PDF
        - states that the average lapse rate in NM is:
            - -4.0F/1000ft (-7.3 K/km) in July
            - -2.5F/1000ft (-4.6 K/km) in January
        - -8.2 K/km is higher than the summer average, but generally desert areas have higher-than-normal lapse rates

The following was the most comprehensive source found for temperature lapse rates in New Mexico: 
- https://pubs.usgs.gov/bul/1964/report.pdf
- No values were found for Spaceport itself, but values for other locations in New Mexico were found
- the report says that in the western conterminous United States, temperature lapse rates are generally significantly less than the standard -6.5 K/km
- the report didn't include the date (or month) of the measurements, so I'd assume that it happened in the winter due to the low lapse rates, and/or the data being several decades old means that it's no longer as accurate due to the changing global climate
- has values for many locations in New Mexico (search for n. mex), and they ranged from -1.4 to -3.9 K/km
    - the closest station to SC was Datil, which had a lapse rate of -3.1 K/km
"""
L_launch_rail_ESRA_provided_SAC = 5.18  # m, 
""" ESRA provides teams with a 5.18m rail at competition """
launchpad_pressure_SAC = 86400  # Pa
""" How the launchpad pressure at Spaceport America was determined

- 86400 2022/06/24   WE Rocketry 2022 TeleMega/TeleMetrum data
- 86405 2022/06/23   https://github.com/ISSUIUC/flight-data/tree/master/20220623
- 86170 2023/06/21   https://github.com/ISSUIUC/flight-data/tree/master/20230621
"""
launchpad_temp_SAC = 35  # deg C
""" Ground-level temperature at Spaceport America Cup note

Flights can occur between about 07:00 and 16:30 local time, so the temperature at the time of launch can vary significantly. 35 C is about what it has been historically during the competition in mid-late June. Getting closer to launch day, it would be more accurate to use a weather forecast to get a value for expected temperature(s).

You can also consider running simulations with a range of temperatures that have been seen on launch days in the past (normally between 25 and 45 C) to see how different ground-level temperatures could affect a rocket's flight.
"""
latitude_SA = 32.99  # deg, Spaceport America's latitude
""" https://maps.app.goo.gl/rZT6MRLqHneA7wNX7 """
altitude_SA = 1401  # m, Spaceport America's elevation
""" https://www.spaceportamerica.com/faq/#toggle-id-15 """
launch_angle_SAC = 84  # deg from horizontal
""" How the standard launch angle at Spaceport America Cup was determined
DTEG 10.1.1: 
    > Launch vehicles will nominally launch at an elevation angle of 84° ±1°
DTEG 10.1.2:
    > Range Safety Officers reserve the right to require certain vehicles’ launch elevation be 
lower or higher if flight safety issues are identified during pre-launch activities

Teams have noted that they've been told to use angles at least as low as 80°. The Range Safety Officer picks the angle based on various factors, including the rocket being launched, the weather, and the location of the launch pad. In the design, simulation, and testing phases, use the nominal angle of 84°, but consider the possibility of the launch angle being more or less than that on competition day.
"""

Spaceport_America_avg_launch_conditions = rocket_classes.LaunchConditions(
    launchpad_pressure = launchpad_pressure_SAC,
    launchpad_temp = launchpad_temp_SAC,
    L_launch_rail = L_launch_rail_ESRA_provided_SAC,
    launch_angle = launch_angle_SAC,
    local_T_lapse_rate = T_lapse_rate_SA,
    latitude = latitude_SA,
    altitude = altitude_SA
)


Prometheus_launch_conditions = rocket_classes.LaunchConditions(
    launchpad_pressure = launchpad_pressure_SAC,  # Pa
    launchpad_temp = 34,  # deg C, from https://www.timeanddate.com/weather/@5492576/historic?month=6&year=2023
    L_launch_rail = L_launch_rail_ESRA_provided_SAC,
    launch_angle = 80,  # deg from horizontal. Niall said Prometheus was set up at 10 deg off of the vertical
    local_T_lapse_rate = T_lapse_rate_SA,
    latitude = latitude_SA,
    altitude = altitude_SA
)
# TODO: have this read from RFS instead of defined here
Spaceport_America_avg_launch_conditions = rocket_classes.LaunchConditions(
    launchpad_pressure = launchpad_pressure_SAC,
    launchpad_temp = launchpad_temp_SAC,
    L_launch_rail = L_launch_rail_ESRA_provided_SAC,
    launch_angle = launch_angle_SAC,
    local_T_lapse_rate = T_lapse_rate_SA,
    latitude = latitude_SA,
    altitude = altitude_SA
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
    # TODO: consider retraction speed being significantly faster than deployment speed, incorporate being closed for apogee into sims
    max_deployment_angle = 45  # deg
)

# Set the default Hyperion configuration
Hyperion = rocket_classes.Rocket(**Hyperion_2024_05_26)
current_airbrakes_model = airbrakes_model_2024_03_20