# Perform analysis on max stopping power provided by different airbrakes. Specifically:
# - different areas
# - different deployment speeds
# TODO: - different coefficients of drag?

import numpy as np
import constants as con
import rocket_classes as rktClass
import flight_simulation as fs
from configs import Hyperion

# TODO: may want to do an updated version of this that incorporates other things outside of our control like launch angle, atmospheric conditions, etc similar to the other sensitivity analysis without airbrakes. Or just use worst case scenario (the one that leads to the highest apogee) for everything

# Outline of analysis:
individual_flap_areas = np.linspace(0.002, 0.007, 6) # m^2
deploy_speeds = np.linspace(1, 15, 8) # deg/s

# Create a list of all the different combinations of launch conditions to be simulated with
airbrakes_models = []
for area in individual_flap_areas:
    for speed in deploy_speeds:
        airbrakes_models.append(
            rktClass.Airbrakes(
                num_flaps = 3,
                A_flap = area,
                Cd_brakes = 1,
                max_deployment_speed = speed,
                max_deployment_angle = 41.35
            )
        )

# Get flight data for Hyperion through to motor burnout
pre_brake_flight, _, _, burnout_index, _ = fs.simulate_flight(Hyperion)
pre_brake_flight = pre_brake_flight.iloc[:burnout_index]

# Run the simulations
def run_simulation(pre_brake_flight, Hyperion, airbrakes_model):
    ascent = fs.simulate_airbrakes_flight(pre_brake_flight, Hyperion, airbrakes_model)[0]
    apogee = ascent['height'].iloc[-1]
    return apogee

num_sims = len(airbrakes_models)
print(f"Running {num_sims} simulations")
sim_num = 0
apogees = []
for airbrakes_model in airbrakes_models:
    sim_num += 1
    apogees.append(run_simulation(pre_brake_flight, Hyperion, airbrakes_model))
    if sim_num % 10 == 0:
        print(f"\tSimulation {sim_num} of {num_sims} complete")
print("All simulations complete")

# Plot the results with a heatmap with apogee as the z-axis, and the x and y axes as the airbrake area and deployment speed
import matplotlib.pyplot as plt
import seaborn as sns

apogees = np.array(apogees).reshape(len(individual_flap_areas), len(deploy_speeds))
apogees*=con.m_to_ft_conversion
apogees-=100 # wind correction, made smaller because worst case is low wind meaning greater need to bring down apogee 
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(apogees, annot=True, fmt=".0f", ax=ax, xticklabels=np.round(deploy_speeds, 4), yticklabels=np.round(individual_flap_areas*10000, 1))
ax.set_xlabel('Deployment Speed (deg/s)')
ax.set_ylabel('Individual Flap Area (cm^2)')
ax.set_title('Apogee (ft) vs Flap Area and Deployment Speed')
plt.show()