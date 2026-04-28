#  Rocket Flight Simulator & Design Optimization Platform

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![UI](https://img.shields.io/badge/UI-Tkinter-blueviolet)
![Visualization](https://img.shields.io/badge/3D-VPython-green)
![Simulation](https://img.shields.io/badge/Simulation-Physics%20Based-red)
![Focus](https://img.shields.io/badge/Focus-Aerospace%20Optimization-blue)

---

##  Overview

This project is a **physics-based rocket flight simulator** designed as a **baseline platform for rocket design and performance optimization**.

The goal is not just to simulate a rocket — but to beat it.

> Build a baseline rocket → simulate performance → redesign → compare → outperform.

This mirrors real aerospace engineering workflows where iterative design is used to optimize performance.

The long-term goal is to use this simulator as the baseline for a **physically built model rocket**, optimized aerodynamically beyond what the simulation predicts — then fly it to prove it.

---

##  Features

- 2D physics-based flight simulation
- 3D trajectory visualization using VPython in the browser
- Real motor thrust curve integration via CSV (Estes C6, D12, E12)
- Motor selector dropdown — swap motors without touching code
- Full parameter UI — edit dry mass, propellant mass, diameter, drag coefficient, parachute settings, launch angle, wind speed, and launch altitude
- 4 real-time performance plots:
  - Flight trajectory (downrange vs altitude)
  - Velocity vs time
  - Acceleration vs time
  - Dynamic pressure (Max Q)
- Fort Collins CO launch altitude (1525m) for realistic air density
- Replay button in 3D animation

---

##  Simulation Model

The simulator models:

- **Thrust** — time-dependent, loaded from real motor CSV data
- **Drag** — D = 0.5 × ρ × v² × Cd × A
- **Air density** — exponential atmosphere model offset by launch altitude: ρ = ρ₀ × e^(-(alt + launch_alt) / 8500)
- **Gravity** — F = m × g
- **Variable mass** — decreases linearly as propellant burns
- **Parachute deployment** — triggered at apogee, switches to chute drag area
- **Wind effects** — applied as lateral force after burnout

---

##  3D Visualization

The simulation includes a **3D visualization layer using VPython**, which:

- Animates the rocket trajectory in a browser tab
- Renders rocket body, nose cone, fins, and parachute deployment
- Displays flight trail and engine exhaust
- Supports free zoom, pan, and rotation during playback
- Includes a replay button to rewatch without rerunning the simulation

> Note: Physics is currently 2D, with 3D used for visualization. Full 3D dynamics are planned.

---

##  Project Structure

- app.py — Main Tkinter UI
- simulation.py — 2D flight simulation loop
- physics.py — Thrust, drag, mass, acceleration calculations
- config.py — Default rocket parameters
- visualization.py — 3D VPython browser animation
- motors/motors/ — Motor CSV files (estes_c6, estes_d12, estes_e12)
- run.bat — Quick Windows launch script

---

##  Installation

git clone https://github.com/jdsolliday/rocket_sim.git
cd rocket_sim
py -3.12 -m pip install numpy matplotlib pandas vpython

---

##  Usage

py -3.12 app.py

Or use the quick launch script:
.\run.bat

1. Set rocket parameters in the UI
2. Select a motor from the dropdown
3. Click Run Simulation to generate graphs and flight stats
4. Click View 3D Animation to watch the 3D playback in your browser

---

##  Adding New Motors

Drop any CSV into motors/motors/ with columns time_s and thrust_n.
It will automatically appear in the motor selector dropdown.
Real thrust curve data available at thrustcurve.org

---

##  Project Goal

This simulator is designed to support:

- Baseline rocket performance modeling
- Iterative design improvements
- Aerodynamic optimization
- Performance comparison between configurations

Typical workflow:
Baseline Rocket → Simulation → Design Changes → Re-simulate → Compare → Improve

---

##  Current Limitations

- Physics is currently 2D (visualized in 3D)
- Simplified aerodynamic model (constant Cd)
- Limited wind modeling
- No stability analysis (CP/CG) yet

---

##  Roadmap

- [x] Physics engine — thrust, drag, gravity, variable mass
- [x] 2D flight simulation loop
- [x] Real motor thrust curve integration via CSV
- [x] Motor selector dropdown
- [x] Full parameter UI — mass, diameter, CD, parachute, wind, altitude
- [x] 4 real-time performance plots
- [x] Fort Collins launch altitude and air density correction
- [x] 3D VPython flight animation
- [x] Rocket body, nose cone, fins, and parachute in 3D
- [x] Camera tracking with free zoom and pan
- [x] Replay button
- [ ] Full 3D physics (x, y, z motion)
- [ ] Mach-dependent drag modeling
- [ ] Stability analysis — center of pressure vs center of mass
- [ ] Advanced wind modeling
- [ ] Save/load rocket configurations
- [ ] Export results and graphs to PNG/PDF
- [ ] Parameter sweep — compare multiple configs on one plot
- [ ] Build a physical rocket optimized beyond the simulation baseline
- [ ] Launch at Fort Collins and validate against real flight data

---

##  Long-Term Vision

This project aims to evolve into a full rocket design and analysis tool capable of predicting real-world flight performance, guiding physical rocket builds, and validating simulation results against experimental data.

---

##  Screenshots

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/5d543a22-52cd-4ea8-b3ea-0c8ec3209301" />
<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/f31e488d-5e19-4cc6-a6fd-4f076412e38d" />
<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/f12b9b66-2166-4765-aea3-ff034e069c77" />

---

##  Author

**Johnny Solliday** — Aerospace Missions and System Design student at MSU Denver
github.com/jdsolliday

---

## ⭐ Notes

This project is actively being developed as both a learning platform and a foundation for more advanced aerospace simulation work.
