# Import libraries, define natural constants, helper functions
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

R_universal = 8.3144598 # J/(mol*K)
R_specific_air = 287.058 # J/(kg*K)
MM_air = 0.0289644 # kg/mol
F_gravity = 9.80665 # m/s^2
T_lapse_rate = 0.0065 # K/m

def temp_at_height(h, temp_at_launchpad):
    return temp_at_launchpad - (h*T_lapse_rate)

def pressure_at_height(h, temp_at_launchpad, pressure_at_launchpad):
    return pressure_at_launchpad*(pow((1-(h*T_lapse_rate/(temp_at_launchpad+273.15))),(F_gravity*MM_air/(R_universal*T_lapse_rate)))) 
    # Pressure at the launch site was around 87 kPa for Prometheus' launch

def air_density_fn(pressure, temp):
    return pressure/(R_specific_air*(temp+273.15))

one_atm_air_dynamic_viscosity_lookup = { # https://www.me.psu.edu/cimbala/me433/Links/Table_A_9_CC_Properties_of_Air.pdf
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

def lookup_dynamic_viscosity(temp, one_atm_air_dynamic_viscosity_lookup):
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
    
def Cd_rocket_at_Re(Re): 
    # taken from looking at Prometheus' simulated Reynold's number vc Cd graphs
    if Re < 1e7: return 0.4
    elif Re < 4e7: return 0.4 - (Re-1e7)*(0.4-0.32)/(4e7-1e7)
    elif Re < 5.8e7: return 0.32 - (Re-4e7)*(0.32-0.3)/(5.8e7-4e7)

A_rocket = 0.015326 # 5.5" diameter circle's area in m^2


dataset = pd.read_csv('preliminary-flight-analysis/2022-06-24-serial-5115-flight-0001.csv',skiprows=range(1,20)).iloc[:2000].drop_duplicates().reset_index()
dataset['time'] = dataset['time'] - dataset['time'][0]
timestep = 0.01

L_rocket = 2.229 # length of Prometheus in m
len_characteristic = L_rocket
# correct temperatures to what the temperature would be on the outside of the rocket using the standard temperature lapse rate
dataset['temperature'] = dataset['height'].apply(lambda x: temp_at_height(x,dataset['temperature'][0]))
# calculate pressure, air density, dynamic viscosity, Reynolds number, and drag coefficient
pressure_at_launchpad = dataset['pressure'][0]
dataset['pressure'] = dataset['height'].apply(lambda x: pressure_at_height(x,dataset['temperature'][0], pressure_at_launchpad))
dataset['air_density'] = dataset.apply(lambda x: air_density_fn(x['pressure'],x['temperature']), axis=1)
dataset['q'] = dataset.apply(lambda x: 0.5*x['air_density']*pow(x['speed'],2), axis=1)
dataset['dynamic_viscosity'] = dataset['temperature'].apply(lambda x: lookup_dynamic_viscosity(x,one_atm_air_dynamic_viscosity_lookup))
dataset['reynolds_num'] = dataset.apply(lambda x: x['air_density']*x['speed']*len_characteristic/x['dynamic_viscosity'], axis=1)
dataset['Cd_rocket'] = dataset['reynolds_num'].apply(Cd_rocket_at_Re)


dry_mass = 16.91 # kg
engine_mass_lookup = { # source: https://www.thrustcurve.org/simfiles/5f4294d20002e900000006b1/
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
}
def tech_spec_mass_at_time(time, dry_mass, engine_mass_lookup):
    time_list = list(engine_mass_lookup.keys())
    if time >= time_list[-1]:
        return dry_mass
    else:
        lower_time = max([t for t in time_list if t <= time])
        upper_time = min([t for t in time_list if t > time])
        lower_mass = engine_mass_lookup[lower_time]
        upper_mass = engine_mass_lookup[upper_time]
        return dry_mass + lower_mass + (time - lower_time) * (upper_mass - lower_mass) / (upper_time - lower_time)
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
}
def tech_spec_thrust_at_time(time, engine_thrust_lookup):
    time_list = list(engine_thrust_lookup.keys())
    if time >= time_list[-1]:
        return 0
    else:
        lower_time = max([t for t in time_list if t <= time])
        upper_time = min([t for t in time_list if t > time])
        lower_thrust = engine_thrust_lookup[lower_time]
        upper_thrust = engine_thrust_lookup[upper_time]
        return lower_thrust + (time - lower_time) * (upper_thrust - lower_thrust) / (upper_time - lower_time)

dataset['thrust'] = dataset['time'].apply(lambda x: tech_spec_thrust_at_time(x, engine_thrust_lookup))
dataset['mass'] = dataset['time'].apply(lambda x: tech_spec_mass_at_time(x, dry_mass, engine_mass_lookup))

dataset['accel_minus_g'] = dataset['acceleration'] - F_gravity
dataset['accel_minus_g_minus_drag'] = dataset['accel_minus_g'] - (dataset['q']*A_rocket*dataset['Cd_rocket'])/dataset['mass']


# plot thrust/mass_minus_g_minus_drag and acceleration_minus_g_minus_drag vs time on the same plot

fig, ax1 = plt.subplots()
ax1.plot(dataset['time'],dataset['accel_minus_g_minus_drag'],label='accel_minus_g_minus_drag')

def Cd_rocket_at_Re(Re): 
    # new version, just k-ω model
    if Re < 1e7: return 0.42
    elif Re < 2.8e7: return 0.42 - (Re-1e7)*(0.42-0.4)/(2.8e7-1e7)
    elif Re < 5e7: return 0.4 - (Re-2.8e7)*(0.4-0.31)/(5e7-2.8e7)
    else: return 0.31
dataset['Cd_rocket'] = dataset['reynolds_num'].apply(Cd_rocket_at_Re)


dataset['thrust/mass'] = dataset['thrust']/dataset['mass']
dataset['thrust/mass_minus_g'] = dataset['thrust/mass'] - F_gravity
dataset['thrust/mass_minus_g_minus_drag'] = dataset['thrust/mass_minus_g'] - (dataset['q']*A_rocket*dataset['Cd_rocket'])/dataset['mass']

ax1.plot(dataset['time'],dataset['thrust/mass_minus_g_minus_drag'],label='thrust/mass_minus_g_minus_drag')

ax1.set_xlabel('time (s)')
ax1.set_ylabel('acceleration (m/s^2)')
ax1.legend()

# plot Re on the same graph
ax2 = ax1.twinx()
ax2.plot(dataset['time'],dataset['reynolds_num'],label='Re', color='black')
ax2.set_ylabel('Re')
ax2.legend()

plt.show()

# # determine what the coefficient of drag would need to be to slow the rocket down the same amount as it was slowed in the expermental data

# dataset['Fd_experimental'] = dataset['thrust']-(dataset['acceleration']-F_gravity)*(dataset['mass'])
# dataset['Cd_experimental'] = dataset['Fd_experimental']/(dataset['q']*A_rocket)

# # plot Cd_experimental vs time
# fig, ax1 = plt.subplots()
# ax1.plot(dataset['time'].iloc[100:],dataset['Cd_experimental'].iloc[100:],label='Cd_experimental')
# ax1.set_xlabel('time (s)')
# ax1.set_ylabel('Cd_experimental')
# ax1.legend()

# # plot Re on the same graph
# ax2 = ax1.twinx()
# ax2.plot(dataset['time'].iloc[100:],dataset['reynolds_num'].iloc[100:],label='Re', color='orange')
# ax2.set_ylabel('Re')
# ax2.legend()

# plt.show()

# # plot Fd_experimental and q vs time on the same graph

# fig, ax1 = plt.subplots()
# ax1.plot(dataset['time'].iloc[100:],dataset['Fd_experimental'].iloc[100:],label='Fd_experimental')
# ax1.set_xlabel('time (s)')
# ax1.set_ylabel('Fd_experimental')
# ax1.legend()

# ax2 = ax1.twinx()
# ax2.plot(dataset['time'].iloc[100:],dataset['q'].iloc[100:],label='q', color='orange')
# ax2.set_ylabel('q')
# ax2.legend()

# plt.show()

# # plot Fd_experimental/Re vs time

# fig, ax1 = plt.subplots()
# ax1.plot(dataset['time'].iloc[100:],dataset['Fd_experimental'].iloc[100:]/dataset['reynolds_num'].iloc[100:],label='Fd_experimental/Re')
# ax1.set_xlabel('time (s)')
# ax1.set_ylabel('Fd_experimental/Re')
# ax1.legend()

# plt.show()