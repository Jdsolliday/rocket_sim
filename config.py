import numpy as np

# Mass
DRY_MASS = 0.120
PROPELLANT_MASS = 0.015
TOTAL_MASS = DRY_MASS + PROPELLANT_MASS

# Aerodynamics
DIAMETER = 0.04
CD = 0.5

# Parachute
CHUTE_DIAMETER = 0.3
CHUTE_CD = 1.5
CHUTE_AREA = np.pi * (CHUTE_DIAMETER / 2) ** 2

# 2D parameters
LAUNCH_ANGLE = 85.0
WIND_SPEED = 2.0
LAUNCH_ALTITUDE = 1525.0  # Fort Collins, CO elevation in meters

# Simulation settings
DT = 0.01
MAX_TIME = 60.0

# Constants
G = 9.81