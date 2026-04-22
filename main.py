from simulation import run_simulation
from plotting import plot_thrust_curve, plot_flight
from config import TOTAL_MASS, LAUNCH_ANGLE, WIND_SPEED, CHUTE_DIAMETER

def main():
    print("✅ Rocket configuration loaded!")
    print(f"   Total mass    : {TOTAL_MASS} kg")
    print(f"   Launch angle  : {LAUNCH_ANGLE}°")
    print(f"   Wind speed    : {WIND_SPEED} m/s")
    print(f"   Chute diameter: {CHUTE_DIAMETER * 100} cm")

    print("\n" + "=" * 40)
    print("   ROCKET FLIGHT SIMULATOR - 2D")
    print("=" * 40 + "\n")

    plot_thrust_curve()
    results = run_simulation()
    plot_flight(*results)

if __name__ == "__main__":
    main()
