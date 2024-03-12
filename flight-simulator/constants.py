F_gravity = 9.791327  # m/s^2
T_lapse_rate = 0.0065  # K/m
# TODO: can we get a more accurate value for T_lapse_rate?
R_universal = 8.3144598  # J/(mol*K)
MM_air = 0.0289644  # kg/mol
R_specific_air = R_universal / MM_air  # J/(kg*K)
m_to_ft_conversion = 3.28084  # ft/m
F_g_over_R_spec_air_T_lapse_rate = F_gravity / (R_specific_air * T_lapse_rate)

"""
How F_gravity was calculated:

# https://en.wikipedia.org/wiki/Theoretical_gravity#International_gravity_formula_1980
import numpy as np
gamma_a = 9.780327  # m/s^2
beta = 0.0053024  # 1/m
beta_1 = -0.0000058  # 1/m
c1 = 0.0052790414
c2 = 0.0000232718
c3 = 0.0000001262
c4 = 0.0000000007

phi = 32.99 # latitude at Spaceport America
phi = np.deg2rad(phi)

gamma_0 =gamma_a * (1 + c1 * np.sin(phi)**2 + c2 * np.sin(phi)**4 + c3 * np.sin(phi)**6 + c4 * np.sin(phi)**8)

print(gamma_0)

h = 1401  # m

k1 = 3.15704e-07  # 1/m
k2 = 2.10269e-09  # 1/m
k3 = 7.37452e-14  # 1/m^2

g_launchpad = gamma_0 * (1 - (k1 - k2 * np.sin(phi)**2) * h + k3 * h**2)
print(g_launchpad)

h_10kft = h + 10 * 0.3048  # m
g_10kft = gamma_0 * (1 - (k1 - k2 * np.sin(phi)**2) * h_10kft + k3 * h_10kft**2)
print(g_10kft)

print((g_launchpad + g_10kft) / 2)

Standard gravity: 9.80665 m/s^2
RocketPy: 9.7913 m/s^2
IGF 1980 (with height at launchpad): 9.791331465 m/s^2
IGF 1980 (with height at 10kft): 9.791322064 m/s^2
Going to use average height between launchpad and 10kft: 9.791327 m/s^2
"""