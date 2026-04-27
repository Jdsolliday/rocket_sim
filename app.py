from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import os
import config
import simulation

class RocketSimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rocket Simulation")
        self.root.minsize(800, 900)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

        frame = ttk.Frame(root, padding=10)
        frame.grid(row=0, column=0, sticky="ew")

        ttk.Label(frame, text="Launch Angle").grid(column=0, row=0)
        self.angle = ttk.Entry(frame)
        self.angle.insert(0, str(config.LAUNCH_ANGLE))
        self.angle.grid(column=1, row=0)

        ttk.Label(frame, text="Wind Speed").grid(column=0, row=1)
        self.wind = ttk.Entry(frame)
        self.wind.insert(0, str(config.WIND_SPEED))
        self.wind.grid(column=1, row=1)

        # ✅ Motor selector
        ttk.Label(frame, text="Motor").grid(column=0, row=2)
        self.motor_var = tk.StringVar()
        motor_dir = os.path.join(os.path.dirname(__file__), "motors", "motors")
        motors = [f for f in os.listdir(motor_dir) if f.endswith(".csv")]
        self.motor_dropdown = ttk.Combobox(frame, textvariable=self.motor_var, values=motors, state="readonly")
        self.motor_dropdown.set(motors[0])
        self.motor_dropdown.grid(column=1, row=2)

        ttk.Button(frame, text="Run Simulation", command=self.run).grid(column=0, row=3, columnspan=2)

        self.output = tk.Text(frame, height=6, width=50)
        self.output.grid(column=0, row=4, columnspan=2)

        self.chart_frame = ttk.Frame(root)
        self.chart_frame.grid(row=1, column=0, sticky="nsew")
        self.chart_frame.columnconfigure(0, weight=1)
        self.chart_frame.rowconfigure(0, weight=1)

        self.canvas = None

    def run(self):
        config.LAUNCH_ANGLE = float(self.angle.get())
        config.WIND_SPEED = float(self.wind.get())

        # ✅ Load selected motor before running
        simulation.load_motor(self.motor_var.get())

        results = simulation.run_simulation()
        time     = results[0]
        x        = results[1]
        altitude = results[2]
        speed    = results[3]
        accel    = results[4]
        dynpress = results[5]
        chute    = results[6]

        chute_time = next((time[i] for i, c in enumerate(chute) if c), None)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"Max altitude  : {max(altitude):.2f} m\n")
        self.output.insert(tk.END, f"Max speed     : {max(speed):.2f} m/s\n")
        self.output.insert(tk.END, f"Downrange dist: {max(x):.2f} m\n")
        self.output.insert(tk.END, f"Landing speed : {speed[-1]:.2f} m/s\n")

        if self.canvas is not None:
            plt.close(self.canvas.figure)
            self.canvas.get_tk_widget().destroy()

        fig, axes = plt.subplots(2, 2, figsize=(10, 7))
        fig.suptitle("Rocket Simulation Results", fontsize=13)

        ax1 = axes[0, 0]
        ax1.plot(x, altitude, color="royalblue")
        ax1.set_xlabel("Downrange Distance (m)")
        ax1.set_ylabel("Altitude (m)")
        ax1.set_title("Flight Trajectory")
        ax1.grid(True)

        ax2 = axes[0, 1]
        ax2.plot(time, speed, color="tomato")
        if chute_time:
            ax2.axvline(chute_time, color="gray", linestyle="--", label="Chute deploy")
            ax2.legend()
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Speed (m/s)")
        ax2.set_title("Speed vs Time")
        ax2.grid(True)

        ax3 = axes[1, 0]
        ax3.plot(time, accel, color="seagreen")
        if chute_time:
            ax3.axvline(chute_time, color="gray", linestyle="--", label="Chute deploy")
            ax3.legend()
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Acceleration (m/s²)")
        ax3.set_title("Acceleration vs Time")
        ax3.grid(True)

        ax4 = axes[1, 1]
        ax4.plot(time, dynpress, color="darkorange")
        if chute_time:
            ax4.axvline(chute_time, color="gray", linestyle="--", label="Chute deploy")
            ax4.legend()
        ax4.set_xlabel("Time (s)")
        ax4.set_ylabel("Dynamic Pressure (Pa)")
        ax4.set_title("Dynamic Pressure vs Time")
        ax4.grid(True)

        fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

root = tk.Tk()
app = RocketSimApp(root)
root.mainloop()