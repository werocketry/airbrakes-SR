# Perform sensitivity analysis using different environmental and launch conditions. Specifically:
# - temperature at launchpad
# - pressure at launchpad
# - launch rail angle
# - rocket mass

import numpy as np
import constants as con
import rocket_classes as rktClass
import flight_simulation as fs
import helper_functions as hfunc
from configs import Hyperion

# Outline of sensitivity analysis:
launch_rail_angles = 90 - np.linspace(5, 15, 6)
launchpad_temps = np.linspace(25, 45, 3)
launchpad_pressures = np.linspace(80000, 90000, 3) # [86400]
rocket_dry_masses = np.linspace(16, 19, 4)

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
            Hyperion["L_rocket"],
            Hyperion["A_rocket"],
            rocket_dry_mass,
            Hyperion["fuel_mass_lookup"],
            Hyperion["engine_thrust_lookup"],
            Hyperion["Cd_rocket_at_Re"],
            Hyperion["h_second_rail_button"]
        )
    )

# Run the simulations
num_sims = len(launch_conditions) * len(rockets)
print(f"Running {num_sims} simulations")
sim_num = 0
apogees = []
max_qs = []
max_machs = []
for rocket in rockets:
    for launch_condition in launch_conditions:
        sim_num += 1
        flight = fs.simulate_flight(rocket, launch_condition, 0.01)[0]
        apogee = flight['height'].iloc[-1]
        apogees.append(apogee)
        max_qs.append(max(flight['q']))
        # max mach number is at max speed. Use that and the temperature at that point with the function mach_number_fn in helper_functions.py
        temp_at_max_speed = flight['temperature'].iloc[flight['speed'].idxmax()]
        max_machs.append(hfunc.mach_number_fn(flight['speed'].max(), temp_at_max_speed))
    print(f"Simulation {sim_num} of {num_sims} complete")

# Print out the results
apogees = np.array(apogees)*con.m_to_ft_conversion
print('\nApogees (ft):')
print(f'Min: {min(apogees)}')
print(f'Max: {max(apogees)}')
print(f'Mean: {np.mean(apogees)}')
print(f'Std: {np.std(apogees)}')

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
# histogram of apogees
plt.hist(apogees, bins=20)
plt.title('Apogee distribution')
plt.xlabel('Apogee (ft)')
plt.ylabel('Frequency')
plt.show()