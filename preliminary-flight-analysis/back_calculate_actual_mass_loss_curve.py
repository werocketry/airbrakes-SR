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


dataset = pd.read_csv('preliminary-flight-analysis/2022-06-24-serial-5115-flight-0001.csv',skiprows=range(1,20)).iloc[:600].drop_duplicates().reset_index()
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

def tech_spec_thrust_at_time(time): 
    # as per https://www.csrocketry.com/rocket-motors/cesaroni/motors/pro-98/3g-reloads/cesaroni-m1520-blue-streak-rocket-motor.html
    if time < 0.1: return 1710*time/0.1
    elif time < 0.2: return 1710 - (time-0.1)*(1710-1626)/0.1
    elif time < 0.55: return 1626 + (time-0.2)*(1710-1626)/0.35
    elif time < 1.67: return 1710 + (time-0.55)*(1842-1710)/1.12
    elif time < 2.7: return 1842 - (time-1.67)*(1842-1722)/1.03
    elif time < 4.25: return 1722 - (time-2.7)*(1722-1389)/1.55
    elif time < 4.41: return 1389 + (time-4.25)*(1414-1389)/0.16
    elif time < 4.65: return 1414 - (time-4.41)*(1414-595)/0.24
    elif time < 4.9: return 595 - (time-4.65)*(595)/0.25
    else: return 0
def tech_spec_mass_at_time(time):
    if time <4.9: return 20.51-(time*(20.51-16.91)/4.9)
    else: return 16.91

dataset['thrust'] = dataset['time'].apply(lambda x: tech_spec_thrust_at_time(x))
dataset['mass'] = dataset['time'].apply(lambda x: tech_spec_mass_at_time(x))

dataset['accel_minus_g'] = dataset['acceleration'] - F_gravity
dataset['Cd_rocket'] = dataset['reynolds_num'].apply(Cd_rocket_at_Re)
dataset['accel_minus_g_minus_drag'] = dataset['accel_minus_g'] - (dataset['q']*A_rocket*dataset['Cd_rocket'])/dataset['mass']

dataset['thrust/mass'] = dataset['thrust']/dataset['mass']
dataset['thrust/mass_minus_g'] = dataset['thrust/mass'] - F_gravity
dataset['thrust/mass_minus_g_minus_drag'] = dataset['thrust/mass_minus_g'] - (dataset['q']*A_rocket*dataset['Cd_rocket'])/dataset['mass']
# plot thrust/mass_minus_g_minus_drag and acceleration_minus_g_minus_drag vs time on the same plot

fig, ax1 = plt.subplots()
ax1.plot(dataset['time'],dataset['thrust/mass_minus_g_minus_drag'],label='thrust/mass_minus_g_minus_drag')
ax1.plot(dataset['time'],dataset['accel_minus_g_minus_drag'],label='accel_minus_g_minus_drag')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('acceleration (m/s^2)')
ax1.legend()

plt.show()
