F_gravity = 9.791327  # m/s^2
T_lapse_rate = 0.00817  # K/m
R_universal = 8.3144598  # J/(mol*K)
MM_air = 0.0289644  # kg/mol
R_specific_air = R_universal / MM_air  # J/(kg*K)
m_to_ft_conversion = 3.28084  # ft/m
F_g_over_R_spec_air_T_lapse_rate = F_gravity / (R_specific_air * T_lapse_rate)

""" How F_gravity was calculated

https://en.wikipedia.org/wiki/Theoretical_gravity#International_gravity_formula_1980

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

h = 1401  # m, elevation of Spaceport America

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

""" How T_lapse_rate was determined

Only one source was found with the lapse rate for Spaceport America:
    - https://egusphere.copernicus.org/preprints/2023/egusphere-2023-633/egusphere-2023-633.pdf
    - luckily, they took their measurements in June
    - The lapse rates for the stratosphere for each of three flights were reported as follows:
        - June 1st 2021 8.4 K/km
        - June 4th 2021 7.9 K/km
        - June 6th 2021 8.2 K/km
    - An average of these is what was chosen for the simulation
    - The linear lapse rate was valid for the first 10 km AGL

For future reference, it should be noted that time of year has a large effect on the lapse rate, as reported in:
    - https://mdpi-res.com/d_attachment/remotesensing/remotesensing-14-00162/article_deploy/remotesensing-14-00162.pdf?version=1640917080
    - https://hwbdocs.env.nm.gov/Los%20Alamos%20National%20Labs/TA%2004/2733.PDF
        - states that the average lapse rate in NM is:
            - 4.0F/1000ft (7.3 K/km) in July
            - 2.5F/1000ft (4.6 K/km) in January
        - 8.2 K/km is higher than the summer average, but generally desert areas have higher-than-normal lapse rates

The following was the most comprehensive source found for temperature lapse rates in New Mexico: 
- https://pubs.usgs.gov/bul/1964/report.pdf
- No values were found for Spaceport itself, but values for other locations in New Mexico were found
- the report says that in the western conterminous United States, temperature lapse rates are generally significantly less than the standard 6.5 K/km
- the report didn't include the date (or month) of the measurements, so I'd assume that it happened in the winter due to the low lapse rates, and/or the data being several decades old means that it's no longer as accurate due to the changing global climate
- has values for many locations in New Mexico (search for n. mex), and they ranged from 1.4 to 3.9 K/km
    - the closest station to SC was Datil, which had a lapse rate of 3.1 K/km
"""