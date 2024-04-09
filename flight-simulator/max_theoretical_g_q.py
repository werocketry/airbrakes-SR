import numpy as np
import constants as con
import rocket_classes as rktClass
import flight_simulation as fsim
import helper_functions as hfunc
from configs import Hyperion, Prometheus_launch_conditions

# max g, given no drag, and no parts of the rocket fall off
max_thrust = max(Hyperion.motor.thrust_curve.values())
print(f"Max thrust (N): {max_thrust}")
time_of_max_thrust = max(Hyperion.motor.thrust_curve, key=Hyperion.motor.thrust_curve.get)
mass_at_max_thrust = hfunc.mass_at_time(1.2, Hyperion.dry_mass, Hyperion.motor.mass_curve)
print(f"Mass at max thrust (kg): {mass_at_max_thrust}")
max_acceleration = max_thrust / mass_at_max_thrust - con.F_gravity
max_g = max_acceleration / con.F_gravity
print(f"Max g: {max_g}\n")

# max q, given no drag, and no parts of the rocket fall off, air density is that at the launchpad
air_density = hfunc.air_density_fn(Prometheus_launch_conditions.launchpad_pressure, Prometheus_launch_conditions.launchpad_temp + 273.15)
timestep = 0.0001
t = 0
v = 0
v_max = 0
while t < Hyperion.motor.burn_time:
    mass = hfunc.mass_at_time(t, Hyperion.dry_mass, Hyperion.motor.mass_curve)
    thrust = hfunc.thrust_at_time(t, Hyperion.motor.thrust_curve)
    acceleration = thrust / mass - con.F_gravity
    if acceleration < 0:
        acceleration = 0
    v += acceleration * timestep
    if v > v_max:
        v_max = v
    t += timestep
print(f"Max velocity (m/s): {v_max}")
max_q = hfunc.calculate_dynamic_pressure(air_density, v_max)/1000
print(f"Max q (kPa): {max_q}")