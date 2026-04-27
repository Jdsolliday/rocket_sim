import numpy as np
import os
import pandas as pd
import config

_motor_dir = os.path.join(os.path.dirname(__file__), "motors", "motors")
_motor_file = os.path.join(_motor_dir, "estes_e12.csv")
_motor_data = pd.read_csv(_motor_file)
_thrust_times = _motor_data["time_s"].values
_thrust_forces = _motor_data["thrust_n"].values
_burn_time = _thrust_times[-1]

def load_motor(filename):
    global _thrust_times, _thrust_forces, _burn_time
    path = os.path.join(_motor_dir, filename)
    data = pd.read_csv(path)
    _thrust_times = data["time_s"].values
    _thrust_forces = data["thrust_n"].values
    _burn_time = _thrust_times[-1]

def get_air_density(altitude):
    rho0 = 1.225
    scale_height = 8500.0
    return rho0 * np.exp(-(altitude + config.LAUNCH_ALTITUDE) / scale_height)

def get_thrust(t):
    if t >= _burn_time:
        return 0.0
    return float(np.interp(t, _thrust_times, _thrust_forces))

def get_mass(t):
    if t < _burn_time:
        burn_fraction = t / _burn_time
        burned = burn_fraction * config.PROPELLANT_MASS
        return config.TOTAL_MASS - burned
    return config.DRY_MASS

def calc_drag_2d(vx, vy, altitude, chute_deployed):
    rho = get_air_density(altitude)
    speed = np.sqrt(vx**2 + vy**2)
    if speed == 0:
        return 0.0, 0.0
    if chute_deployed:
        area = config.CHUTE_AREA
        cd = config.CHUTE_CD
    else:
        area = np.pi * (config.DIAMETER / 2) ** 2
        cd = config.CD
    drag_magnitude = 0.5 * rho * speed**2 * cd * area
    drag_x = -drag_magnitude * (vx / speed)
    drag_y = -drag_magnitude * (vy / speed)
    return drag_x, drag_y

def calc_acceleration_2d(t, vx, vy, altitude, chute_deployed):
    thrust = get_thrust(t)
    mass = get_mass(t)
    angle_rad = np.radians(config.LAUNCH_ANGLE)
    thrust_x = thrust * np.cos(angle_rad)
    thrust_y = thrust * np.sin(angle_rad)
    weight_y = mass * config.G
    wind_force_x = 0.0
    if t >= _burn_time:
        wind_force_x = mass * 0.1 * config.WIND_SPEED
    drag_x, drag_y = calc_drag_2d(vx, vy, altitude, chute_deployed)
    fx = thrust_x + drag_x + wind_force_x
    fy = thrust_y - weight_y + drag_y
    return fx / mass, fy / mass

def calc_dynamic_pressure(vx, vy, altitude):
    rho = get_air_density(altitude)
    speed = np.sqrt(vx**2 + vy**2)
    return 0.5 * rho * speed**2