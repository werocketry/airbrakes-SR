# Perform sensitivity analysis using different environmental and launch conditions. Specifically:
# - temperature at launchpad
# - pressure at launchpad
# - launch rail angle
# - rocket mass

# TODO: move the mechanics of this to RFS (or at least the Monte Carlo method), have a notebook that uses it here

import numpy as np
from rocketflightsim import constants as con
from rocketflightsim import rocket_classes as rktClass
from rocketflightsim import flight_simulation as fsim
from rocketflightsim import helper_functions as hfunc
from configs import Hyperion, Spaceport_America_avg_launch_conditions

# Set type of analysis
analysis_type = 'gaussian' # options: 'linear' and 'gaussian'

# Outline of sensitivity analysis:
if analysis_type == 'linear':
    # TODO make the output of the linear analysis show the effect of each variable on the output
    launch_rail_angles = 90 - np.linspace(5, 15, 6)
    launchpad_temps = np.linspace(20, 40, 3)
        # https://www.timeanddate.com/weather/@5492576/historic?month=6&year=2023
    launchpad_pressures = np.linspace(85000, 88000, 3)
        # 86400 2022/06/24   our 2022 data
        # 86405 2022/06/23   https://github.com/ISSUIUC/flight-data/tree/master/20220623
        # 86170 2023/06/21   https://github.com/ISSUIUC/flight-data/tree/master/20230621
        # Truth or Consequences, NM, USA, which has an elevation 90 m lower than Spaceport America
            # 84780 http://cms.ashrae.biz/weatherdata/STATIONS/722710_s.pdf
    rocket_masses = [Hyperion.rocket_mass - 1, Hyperion.rocket_mass, Hyperion.rocket_mass + 1]
elif analysis_type == 'gaussian':
    # TODO: make the output of the gaussian analysis display more information about the input variables
        # either by colour coding the histogram stack to show how settings for one variable affect the output, and/or switching to a 3D heatmap with the x and y axes showing two different input variables, z showing apogee, and the colour showing the number of simulations in each bin. Extra important cause will help choose airbrake extension settings that are more resilient to variations in launch conditions
    num_sims = 20000
    mean_launch_rail_angle = Spaceport_America_avg_launch_conditions.launch_rail_elevation
    std_launch_rail_angle = 1
    mean_launchpad_temp = Spaceport_America_avg_launch_conditions.launchpad_temp
    std_launchpad_temp = 5
    mean_launchpad_pressure = Spaceport_America_avg_launch_conditions.launchpad_pressure
    std_launchpad_pressure = 500
    mean_rocket_mass = Hyperion.rocket_mass
    std_rocket_mass = 0.2
else:
    raise ValueError("analysis_type must be either 'linear' or 'gaussian'")

# Run the simulations
def run_simulation(rocket, launch_condition):
    flight = fsim.simulate_flight(rocket, launch_condition, 0.01)[0]

    # correction for wind. For now, just a constant value of -100m, TODO to be refined later
    wind_correction = -100

    apogee = flight['height'].iloc[-1] + wind_correction
    max_q = max(flight['q'])
    temp_at_max_speed = flight['temperature'].iloc[flight['speed'].idxmax()]
    max_mach = hfunc.mach_number_fn(flight['speed'].max(), temp_at_max_speed)
    return apogee, max_q, max_mach

sim_num = 0
apogees = []
max_qs = []
max_machs = []

if analysis_type == 'linear':
    # Create a list of all the different combinations of launch conditions to be simulated with
    launch_conditions = []
    for launch_rail_angle in launch_rail_angles:
        for launchpad_temp in launchpad_temps:
            for launchpad_pressure in launchpad_pressures:
                launch_conditions.append(
                    rktClass.LaunchConditions(
                        launchpad_pressure,
                        launchpad_temp,
                        Spaceport_America_avg_launch_conditions.L_launch_rail,
                        launch_rail_angle
                    )
                )

    # Create a list of all the different rocket objects to be simulated with
    rockets = []
    for rocket_mass in rocket_masses:
        rockets.append(
            rktClass.Rocket(
                rocket_mass,
                Hyperion.motor,
                Hyperion.A_rocket,
                Hyperion.Cd_rocket_at_Ma,
                Hyperion.h_second_rail_button
            )
        )
    
    # Run the simulations
    num_sims = len(launch_conditions) * len(rockets)
    print(f"Running {num_sims} simulations")

    for rocket in rockets:
        for launch_condition in launch_conditions:
            sim_num += 1
            apogee, max_q, max_mach = run_simulation(rocket, launch_condition)
            apogees.append(apogee)
            max_qs.append(max_q)
            max_machs.append(max_mach)
        print(f"Simulation {sim_num} of {num_sims} complete")
    print("All simulations complete")

elif analysis_type == 'gaussian':
    for _ in range(num_sims):
        launch_rail_angle = max(
            min(
                np.random.normal(mean_launch_rail_angle, std_launch_rail_angle),
                88
            ),
            78
        )
        launchpad_temp = np.random.normal(mean_launchpad_temp, std_launchpad_temp)
        launchpad_pressure = np.random.normal(mean_launchpad_pressure, std_launchpad_pressure)
        rocket_mass = np.random.normal(mean_rocket_mass, std_rocket_mass)
        launch_condition = Spaceport_America_avg_launch_conditions
        launch_condition.launch_rail_elevation = launch_rail_angle
        launch_condition.launchpad_temp = launchpad_temp
        launch_condition.launchpad_pressure = launchpad_pressure
        rocket = rktClass.Rocket(
            rocket_mass,
            Hyperion.motor,
            Hyperion.A_rocket,
            Hyperion.Cd_rocket_at_Ma,
            Hyperion.h_second_rail_button
        )
        apogee, max_q, max_mach = run_simulation(rocket, launch_condition)
        apogees.append(apogee)
        max_qs.append(max_q)
        max_machs.append(max_mach)
        sim_num += 1
        if sim_num % 100 == 0:
            print(f"Simulation {sim_num} of {num_sims} complete")
    print("All simulations complete")

# Print out the results
apogees = np.array(apogees)*con.m_to_ft_conversion
print('\nApogees (ft):')
print(f'Min: {min(apogees)}')
print(f'Max: {max(apogees)}')
print(f'Mean: {np.mean(apogees)}')
print(f'Std: {np.std(apogees)}')
proportion_above_10000 = sum(apogees > 10000) / len(apogees)
print(f'Proportion above 10000 ft: {proportion_above_10000}')

max_qs = np.array(max_qs)
print('\nMax-qs (Pa):')
print(f'Min: {min(max_qs)}')
print(f'Max: {max(max_qs)}')
print(f'Mean: {np.mean(max_qs)}')
print(f'Std: {np.std(max_qs)}')

max_machs = np.array(max_machs)
print('\nMax Mach numbers:')
print(f'Min: {min(max_machs)}')
print(f'Max: {max(max_machs)}')
print(f'Mean: {np.mean(max_machs)}')
print(f'Std: {np.std(max_machs)}')

# Plot the results
import matplotlib.pyplot as plt
# histogram of apogees, with bins of size 200
min_bin = int(min(apogees) // 200 * 200)
max_bin = int(max(apogees) // 200 * 200) + 200
plt.hist(apogees, bins=range(min_bin, max_bin, 200), edgecolor='black')
plt.xticks([400*x for x in range(min_bin//400, max_bin//400+1)])
plt.title('Apogee distribution')
plt.xlabel('Apogee (ft)')
plt.ylabel('Frequency')

# option to add annotations to the plot with the mean and std of the apogees, and the number of simulations
# maybe add mean and std of the input variables too
if 1:
    plt.annotate(f"n = {len(apogees)}\nσ = {np.std(apogees):.0f} ft\nμ = {np.mean(apogees):.0f} ft", xy=(0.98, 0.98), xycoords='axes fraction', ha='right', va='top')


plt.show()