import numpy as np
from config import (
    G,
    BURN_TIME,
    THRUST_CURVE,
    PROPELLANT_MASS,
    TOTAL_MASS,
    DRY_MASS,
    LAUNCH_ANGLE,
    WIND_SPEED,
    CHUTE_AREA,
    CHUTE_CD,
    DIAMETER,
    CD,
)

def get_air_density(altitude):
    rho0 = 1.225
    scale_height = 8500.0
    return rho0 * np.exp(-altitude / scale_height)

def get_thrust(t):
    if t >= BURN_TIME:
        return 0.0

    for i in range(len(THRUST_CURVE) - 1):
        t0, f0 = THRUST_CURVE[i]
        t1, f1 = THRUST_CURVE[i + 1]
        if t0 <= t <= t1:
            fraction = (t - t0) / (t1 - t0)
            return f0 + fraction * (f1 - f0)

    return 0.0

def get_mass(t):
    if t < BURN_TIME:
        burn_fraction = t / BURN_TIME
        burned = burn_fraction * PROPELLANT_MASS
        return TOTAL_MASS - burned
    return DRY_MASS

def calc_drag_2d(vx, vy, altitude, chute_deployed):
    rho = get_air_density(altitude)
    speed = np.sqrt(vx**2 + vy**2)

    if speed == 0:
        return 0.0, 0.0

    if chute_deployed:
        area = CHUTE_AREA
        cd = CHUTE_CD
    else:
        area = np.pi * (DIAMETER / 2) ** 2
        cd = CD

    drag_magnitude = 0.5 * rho * speed**2 * cd * area
    drag_x = -drag_magnitude * (vx / speed)
    drag_y = -drag_magnitude * (vy / speed)

    return drag_x, drag_y

def calc_acceleration_2d(t, vx, vy, altitude, chute_deployed):
    thrust = get_thrust(t)
    mass = get_mass(t)

    angle_rad = np.radians(LAUNCH_ANGLE)
    thrust_x = thrust * np.cos(angle_rad)
    thrust_y = thrust * np.sin(angle_rad)

    weight_y = mass * G

    wind_force_x = 0.0
    if t >= BURN_TIME:
        wind_force_x = mass * 0.1 * WIND_SPEED

    drag_x, drag_y = calc_drag_2d(vx, vy, altitude, chute_deployed)

    fx = thrust_x + drag_x + wind_force_x
    fy = thrust_y - weight_y + drag_y

    return fx / mass, fy / mass

def calc_dynamic_pressure(vx, vy, altitude):
    rho = get_air_density(altitude)
    speed = np.sqrt(vx**2 + vy**2)
    return 0.5 * rho * speed**2
