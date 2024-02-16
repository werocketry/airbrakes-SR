F_gravity = 9.80665  # m/s^2
T_lapse_rate = 0.0065  # K/m
R_universal = 8.3144598  # J/(mol*K)
MM_air = 0.0289644  # kg/mol
R_specific_air = R_universal / MM_air  # J/(kg*K)
m_to_ft_conversion = 3.28084  # ft/m
F_g_over_R_spec_air_T_lapse_rate = F_gravity / (R_specific_air * T_lapse_rate)