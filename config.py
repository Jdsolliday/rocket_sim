import numpy as np

# Mass
DRY_MASS = 0.5
PROPELLANT_MASS = 0.1
TOTAL_MASS = DRY_MASS + PROPELLANT_MASS

# Aerodynamics
DIAMETER = 0.04
CD = 0.5

# Thrust curve
THRUST_CURVE = [
    (0.000, 0.0),
    (0.050, 12.0),
    (0.100, 18.0),
    (0.200, 20.0),
    (0.500, 19.0),
    (1.000, 17.0),
    (1.500, 15.0),
    (1.800, 10.0),
    (1.900, 5.0),
    (2.000, 0.0),
]

BURN_TIME = THRUST_CURVE[-1][0]

# Parachute
CHUTE_DIAMETER = 0.3
CHUTE_CD = 1.5
CHUTE_AREA = np.pi * (CHUTE_DIAMETER / 2) ** 2

# 2D parameters
LAUNCH_ANGLE = 85.0
WIND_SPEED = 2.0

# Simulation settings
DT = 0.01
MAX_TIME = 60.0

# Constants
G = 9.81
