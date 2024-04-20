# Perform sensitivity analysis using different environmental and launch conditions. Specifically:
# - temperature at launchpad
# - pressure at launchpad
# - launch rail angle
# - rocket mass

import numpy as np
import constants as con
import rocket_classes as rktClass
import flight_simulation as fsim
import helper_functions as hfunc
from configs import Hyperion

# Set type of analysis
analysis_type = 'gaussian' # options: 'linear' and 'gaussian'

# Outline of sensitivity analysis:
if analysis_type == 'linear':
    launch_rail_angles = 90 - np.linspace(5, 15, 6)
    launchpad_temps = np.linspace(20, 40, 3)
        # https://www.timeanddate.com/weather/@5492576/historic?month=6&year=2023
    launchpad_pressures = np.linspace(85000, 88000, 3)
        # 86400 2022/06/24   our 2022 data
        # 86405 2022/06/23   https://github.com/ISSUIUC/flight-data/tree/master/20220623
        # 86170 2023/06/21   https://github.com/ISSUIUC/flight-data/tree/master/20230621
        # Truth or Consequences, NM, USA, which has an elevation 90 m lower than Spaceport America
            # 84780 http://cms.ashrae.biz/weatherdata/STATIONS/722710_s.pdf
    rocket_dry_masses = [Hyperion.rocket_mass - 1, Hyperion.rocket_mass, Hyperion.rocket_mass + 1]
elif analysis_type == 'gaussian':
    num_sims = 20000
    mean_launch_rail_angle = 90-10
    std_launch_rail_angle = 3
    mean_launchpad_temp = 34
    std_launchpad_temp = 5
    mean_launchpad_pressure = 86300
    std_launchpad_pressure = 500
    mean_rocket_dry_mass = Hyperion.rocket_mass
    std_rocket_dry_mass = 0.5
else:
    raise ValueError("analysis_type must be either 'linear' or 'gaussian'")

# Run the simulations
def run_simulation(rocket, launch_condition):
    flight = fsim.simulate_flight(rocket, launch_condition, 0.01)[0]

    # correction for wind. For now, just a constant value of -300m (about what ork sims return as the average differences between sims with no wind and average windy sims), to be refined later
    wind_correction = -300

    apogee = flight['height'].iloc[-1] + wind_correction
    max_q = max(flight['q'])
    # max mach number is at max speed. Use that and the temperature at that point with the function mach_number_fn in helper_functions.py
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
                        5.18,
                        launch_rail_angle
                    )
                )

    # Create a list of all the different rocket objects to be simulated with
    rockets = []
    for rocket_dry_mass in rocket_dry_masses:
        rockets.append(
            rktClass.Rocket(
                Hyperion.L_rocket,
                Hyperion.A_rocket,
                rocket_dry_mass,
                Hyperion.motor,
                Hyperion.Cd_rocket_at_Re,
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
                85
            ),
            75
        )
        launchpad_temp = np.random.normal(mean_launchpad_temp, std_launchpad_temp)
        launchpad_pressure = np.random.normal(mean_launchpad_pressure, std_launchpad_pressure)
        rocket_dry_mass = np.random.normal(mean_rocket_dry_mass, std_rocket_dry_mass)
        launch_condition = rktClass.LaunchConditions(
            launchpad_pressure,
            launchpad_temp,
            5.18,
            launch_rail_angle
        )
        rocket = rktClass.Rocket(
            rocket_dry_mass,
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
plt.show()