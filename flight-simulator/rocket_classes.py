# Define Motor, Rocket, LaunchConditions, and Airbrakes classes
class Motor:
    """
    dry_mass: mass of the motor without fuel (kg)
    thrust_curve: dictionary of thrust (N) at time (s after ignition)
    mass_curve: dictionary of mass (kg) at time (s after ignition)
    burn_time: time it takes for the motor to burn all of its fuel (s)
    """

    def __init__(self, dry_mass, thrust_curve, fuel_mass_curve):
        self.dry_mass = dry_mass
        self.thrust_curve = thrust_curve
        self.mass_curve = fuel_mass_curve
        self.burn_time = max(thrust_curve.keys())


class Rocket:
    """
    L_rocket: length of the rocket (m)
    A_rocket: cross-sectional area of the rocket (m^2)
    rocket_mass: dry mass of the rocket without the motor (kg)
    motor: Motor object
    Cd_rocket_at_Re: coefficient of drag of the rocket as a function of Reynolds number
    h_second_rail_button: height of the second rail button from the bottom of the rocket (m). This is the upper button if there's only 2. Defaults to 0.69m, which is what Prometheus had. Doesn't matter much if it's not set as it changes apogee by less than 10ft when it's at 0.
    dry_mass: total mass of the rocket without fuel (kg)
    """

    def __init__(
        self,
        L_rocket,
        A_rocket,
        rocket_mass,
        motor,
        Cd_rocket_at_Re,
        h_second_rail_button=0.69,
    ):
        self.L_rocket = L_rocket
        self.A_rocket = A_rocket
        self.rocket_mass = rocket_mass
        self.motor = motor
        self.Cd_rocket_at_Re = Cd_rocket_at_Re
        self.h_second_rail_button = h_second_rail_button
        self.dry_mass = rocket_mass + motor.dry_mass


class LaunchConditions:
    """
    launchpad_pressure: pressure at the launchpad (Pa)
    launchpad_temp: temperature at the launchpad (°C)
    L_launch_rail: length of the launch rail (m). ESRA provides a 17ft (5.18m) launch rail
    launch_angle: launch angle from horizontal (deg). SAC comp rules say minimum of 6 deg off of vertical, but they pick it based on wind and pad location, so completely out of our control, and we just know it's between 6 and 15 deg
    """

    def __init__(self, launchpad_pressure, launchpad_temp, L_launch_rail, launch_angle):
        self.launchpad_pressure = launchpad_pressure
        self.launchpad_temp = launchpad_temp
        self.L_launch_rail = L_launch_rail
        self.launch_angle = launch_angle


class Airbrakes:
    """
    num_flaps: number of airbrakes flaps
    A_flap: cross-sectional area of each flap (m^2)
    Cd_brakes: coefficient of drag of the airbrakes
    max_deployment_speed: maximum speed at which the airbrakes can be deployed (deg/s)
    max_deployment_angle: maximum angle that the flaps can deploy to (deg)
    """

    def __init__(
        self, num_flaps, A_flap, Cd_brakes, max_deployment_speed, max_deployment_angle
    ):
        self.num_flaps = num_flaps
        self.A_flap = A_flap
        self.Cd_brakes = Cd_brakes
        self.max_deployment_speed = max_deployment_speed
        self.max_deployment_angle = max_deployment_angle