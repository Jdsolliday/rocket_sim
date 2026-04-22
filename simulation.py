import numpy as np
from config import DT, MAX_TIME, BURN_TIME
from physics import calc_acceleration_2d, calc_dynamic_pressure

def run_simulation():
    t = 0.0
    x = 0.0
    y = 0.0
    vx = 0.0
    vy = 0.0

    time_list = []
    x_list = []
    alt_list = []
    vx_list = []
    vy_list = []
    speed_list = []
    accel_list = []
    dynpress_list = []
    chute_list = []

    burnout_reported = False
    apogee_reported = False
    chute_deployed = False
    prev_vy = 0.0

    print("Running 2D simulation...\n")

    while t <= MAX_TIME:
        if y < 0 and t > 0.5:
            print(f"  Landed   at t = {t:.2f} s  |  downrange = {x:.1f} m")
            break

        if not chute_deployed and prev_vy > 0 and vy <= 0 and t > 0.5:
            chute_deployed = True

        ax, ay = calc_acceleration_2d(t, vx, vy, y, chute_deployed)
        q = calc_dynamic_pressure(vx, vy, y)
        speed = np.sqrt(vx**2 + vy**2)
        a_mag = np.sqrt(ax**2 + ay**2)

        time_list.append(t)
        x_list.append(x)
        alt_list.append(y)
        vx_list.append(vx)
        vy_list.append(vy)
        speed_list.append(speed)
        accel_list.append(a_mag)
        dynpress_list.append(q)
        chute_list.append(chute_deployed)

        if not burnout_reported and t >= BURN_TIME:
            print(f"  Burnout  at t = {t:.2f} s  |  alt = {y:.1f} m  |  speed = {speed:.1f} m/s")
            burnout_reported = True

        if not apogee_reported and prev_vy > 0 and vy <= 0 and t > 0.5:
            print(f"  Apogee   at t = {t:.2f} s  |  alt = {y:.1f} m  ← chute deploys here!")
            apogee_reported = True

        prev_vy = vy
        vx = vx + ax * DT
        vy = vy + ay * DT
        x = x + vx * DT
        y = y + vy * DT
        t = t + DT

    print(f"\n  Max altitude  : {max(alt_list):.1f} m")
    print(f"  Max speed     : {max(speed_list):.1f} m/s")
    print(f"  Downrange dist: {max(x_list):.1f} m")
    print(f"  Landing speed : {speed_list[-1]:.1f} m/s")

    max_q = max(dynpress_list)
    max_q_time = time_list[dynpress_list.index(max_q)]
    print(f"  Max Q         : {max_q:.2f} Pa  at t = {max_q_time:.2f} s")

    return time_list, x_list, alt_list, speed_list, accel_list, dynpress_list, chute_list
