from vpython import *
import json
import numpy as np

# Load data from file
with open("anim_data.json", "r") as f:
    data = json.load(f)

time_list = data["time"]
x_list = data["x"]
alt_list = data["alt"]
chute_list = data["chute"]

def run_animation():
    scene.title = "Rocket Flight Animation"
    scene.width = 1200
    scene.height = 700
    scene.background = vector(0.53, 0.81, 0.98)
    scene.up = vector(0, 1, 0)

    max_alt = max(alt_list)
    max_x = max(x_list)

    scale = max_alt * 0.04
    rocket_length = scale
    rocket_radius = scale * 0.18
    nose_length = scale * 0.5

    # Ground plane
    ground = box(
        pos=vector(max_x / 2, -scale * 0.3, 0),
        size=vector(max(max_x * 3, max_alt * 2), scale * 0.3, max_alt),
        color=vector(0.25, 0.52, 0.18),
        texture=textures.rough
    )

    # Launch rail
    rail = cylinder(
        pos=vector(0, 0, 0),
        axis=vector(0.05, scale * 1.2, 0),
        radius=rocket_radius * 0.3,
        color=vector(0.6, 0.6, 0.6)
    )

    # Rocket body
    rocket = cylinder(
        pos=vector(0, 0, 0),
        axis=vector(0, rocket_length, 0),
        radius=rocket_radius,
        color=vector(0.9, 0.1, 0.1)
    )

    # Nose cone
    nose = cone(
        pos=vector(0, rocket_length, 0),
        axis=vector(0, nose_length, 0),
        radius=rocket_radius,
        color=vector(0.95, 0.95, 0.95)
    )

    # Fins
    fin_size = rocket_length * 0.4
    fin_colors = vector(0.8, 0.1, 0.1)
    fins = []
    for angle in [0, 120, 240]:
        rad = np.radians(angle)
        fin = box(
            pos=vector(np.cos(rad) * rocket_radius, fin_size / 2, np.sin(rad) * rocket_radius),
            size=vector(rocket_radius * 0.3, fin_size, fin_size * 0.8),
            color=fin_colors
        )
        fins.append(fin)

    # Parachute
    chute = cone(
        pos=vector(0, 0, 0),
        axis=vector(0, -scale * 0.6, 0),
        radius=scale * 0.5,
        color=vector(1, 0.6, 0.0),
        opacity=0.7,
        visible=False
    )

    # Chute lines
    chute_lines = []
    for angle in [0, 90, 180, 270]:
        rad = np.radians(angle)
        line = cylinder(
            pos=vector(0, 0, 0),
            axis=vector(np.cos(rad) * scale * 0.4, -scale * 0.6, np.sin(rad) * scale * 0.4),
            radius=rocket_radius * 0.05,
            color=vector(0.8, 0.8, 0.8),
            visible=False
        )
        chute_lines.append(line)

    # Trail
    trail = curve(color=vector(0.4, 0.5, 0.9), radius=rocket_radius * 0.15)

    # Thin exhaust trail
    exhaust = curve(color=vector(1, 0.4, 0.0), radius=rocket_radius * 0.08)

    # Labels
    alt_label = label(
        pos=vector(0, 0, 0),
        text="Altitude: 0 m",
        height=16,
        color=color.white,
        box=False,
        opacity=0
    )
    status_label = label(
        pos=vector(0, 0, 0),
        text="Status: Powered flight",
        height=16,
        color=color.yellow,
        box=False,
        opacity=0
    )

    # Follow rocket but allow free zoom/pan
    scene.camera.follow(rocket)

    chute_deployed = False
    burn_time_index = next((i for i, t in enumerate(time_list) if chute_list[i]), len(time_list))

    for i in range(len(time_list)):
        rate(150)

        rx = x_list[i]
        ry = alt_list[i]
        pos = vector(rx, ry, 0)

        rocket.pos = pos
        nose.pos = vector(rx, ry + rocket_length, 0)

        for j, angle in enumerate([0, 120, 240]):
            rad = np.radians(angle)
            fins[j].pos = vector(
                rx + np.cos(rad) * rocket_radius,
                ry + fin_size / 2,
                np.sin(rad) * rocket_radius
            )

        trail.append(pos=vector(rx, ry, 0))

        if i < burn_time_index:
            exhaust.append(pos=vector(rx, ry, 0))

        alt_label.pos = vector(rx + scale * 1.5, ry + scale * 2, 0)
        alt_label.text = f"Altitude: {ry:.1f} m"
        status_label.pos = vector(rx + scale * 1.5, ry + scale * 0.5, 0)

        if chute_list[i] and not chute_deployed:
            chute_deployed = True
            chute.visible = True
            for line in chute_lines:
                line.visible = True
            rocket.color = vector(0.6, 0.6, 0.6)
            status_label.text = "Status: Chute deployed"
            status_label.color = color.cyan
        elif not chute_deployed:
            status_label.text = "Status: Powered flight" if i < burn_time_index else "Status: Coasting"

        if chute_deployed:
            chute.pos = vector(rx, ry + rocket_length + nose_length, 0)
            for j, angle in enumerate([0, 90, 180, 270]):
                rad = np.radians(angle)
                chute_lines[j].pos = vector(rx, ry + rocket_length, 0)
                chute_lines[j].axis = vector(
                    np.cos(rad) * scale * 0.4,
                    scale * 0.6,
                    np.sin(rad) * scale * 0.4
                )

    status_label.text = "Status: Landed"
    status_label.color = color.green

    # ✅ Return all objects so replay can hide them
    return [ground, rail, rocket, nose, chute, trail, exhaust, alt_label, status_label] + fins + chute_lines

# ✅ Replay hides old objects before redrawing
old_objects = []

def replay(b):
    global old_objects
    for obj in old_objects:
        obj.visible = False
    old_objects = run_animation()

old_objects = run_animation()
button(text="  Replay  ", bind=replay)

# Keep tab alive
while True:
    rate(10)