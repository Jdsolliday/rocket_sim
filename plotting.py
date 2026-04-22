import matplotlib.pyplot as plt
from config import THRUST_CURVE, BURN_TIME

def plot_thrust_curve():
    times = [p[0] for p in THRUST_CURVE]
    thrusts = [p[1] for p in THRUST_CURVE]

    plt.figure(figsize=(7, 3))
    plt.plot(times, thrusts, linewidth=2, marker='o', markersize=4)
    plt.title("Motor Thrust Curve")
    plt.xlabel("Time (s)")
    plt.ylabel("Thrust (N)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_flight(time_list, x_list, alt_list, speed_list, accel_list, dynpress_list, chute_list):
    chute_time = None
    for i, deployed in enumerate(chute_list):
        if deployed:
            chute_time = time_list[i]
            break

    fig1, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x_list, alt_list, linewidth=2)

    burnout_idx = next(i for i, t in enumerate(time_list) if t >= BURN_TIME)
    ax.plot(x_list[burnout_idx], alt_list[burnout_idx], 'o', markersize=8, label='Burnout')

    if chute_time is not None:
        chute_idx = next(i for i, t in enumerate(time_list) if t >= chute_time)
        ax.plot(x_list[chute_idx], alt_list[chute_idx], 'o', markersize=8, label='Chute Deploy')

    ax.plot(x_list[-1], alt_list[-1], 'o', markersize=8, label='Landing')

    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Altitude (m)")
    ax.set_title("2D Flight Trajectory")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.show()

    fig2, axes = plt.subplots(4, 1, figsize=(9, 13))
    fig2.suptitle("Rocket Flight Simulation — 2D", fontsize=13, fontweight='bold')

    axes[0].plot(time_list, alt_list, linewidth=2)
    axes[0].set_ylabel("Altitude (m)")
    axes[0].set_title("Altitude vs Time")
    axes[0].axvline(x=BURN_TIME, linestyle='--', label='Burnout')
    if chute_time is not None:
        axes[0].axvline(x=chute_time, linestyle='--', label='Chute Deploy')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(time_list, speed_list, linewidth=2)
    axes[1].set_ylabel("Speed (m/s)")
    axes[1].set_title("Total Speed vs Time")
    axes[1].axvline(x=BURN_TIME, linestyle='--', label='Burnout')
    if chute_time is not None:
        axes[1].axvline(x=chute_time, linestyle='--', label='Chute Deploy')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(time_list, accel_list, linewidth=2)
    axes[2].set_ylabel("Acceleration (m/s²)")
    axes[2].set_title("Acceleration vs Time")
    axes[2].axvline(x=BURN_TIME, linestyle='--', label='Burnout')
    if chute_time is not None:
        axes[2].axvline(x=chute_time, linestyle='--', label='Chute Deploy')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(time_list, dynpress_list, linewidth=2)
    axes[3].set_ylabel("Dynamic Pressure (Pa)")
    axes[3].set_xlabel("Time (s)")
    axes[3].set_title("Dynamic Pressure (Max Q) vs Time")
    axes[3].axvline(x=BURN_TIME, linestyle='--', label='Burnout')
    if chute_time is not None:
        axes[3].axvline(x=chute_time, linestyle='--', label='Chute Deploy')
    axes[3].legend()
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
