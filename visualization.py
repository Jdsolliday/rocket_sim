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
    scene.forward = vector(1, -0.3, -1)

    max_alt = max(alt_list)
    max_x = max(x_list)

    # Ground plane
    ground = box(
        pos=vector(max_x / 2, -0.5, 0),
        size=vector(max(max_x * 2, 100), 1, 100),
        color=vector(0.3, 0.6, 0.2),
        texture=textures.rough
    )

    # Launch rail
    rail = cylinder(
        pos=vector(0, 0, 0),
        axis=vector(0.1, 1.5, 0),
        radius=0.02,
        color=vector(0.6, 0.6, 0.6)
    )

    # Rocket body
    rocket = cylinder(
        pos=vector(0, 0, 0),
        axis=vector(0, 0.4, 0),
        radius=0.04,
        color=vector(0.9, 0.1, 0.1)
    )

    # Nose cone
    nose = cone(
        pos=vector(0, 0.4, 0),
        axis=vector(0, 0.2, 0),
        radius=0.04,
        color=vector(0.9, 0.9, 0.9)
    )

    # Parachute marker
    chute_marker = sphere(
        pos=vector(0, 0, 0),
        radius=0.5,
        color=vector(1, 0.8, 0),
        opacity=0.5,
        visible=False
    )

    # Trail
    trail = curve(color=vector(0.5, 0.6, 0.8))

    # Labels
    alt_label = label(
        pos=vector(2, max_alt * 0.9, 0),
        text="Altitude: 0 m",
        height=14,
        color=color.white,
        box=False
    )
    status_label = label(
        pos=vector(2, max_alt * 0.8, 0),
        text="Status: Powered flight",
        height=14,
        color=color.white,
        box=False
    )

    scene.camera.follow(rocket)

    chute_deployed = False

    for i in range(len(time_list)):
        rate(100)

        rx = x_list[i]
        ry = alt_list[i]

        rocket.pos = vector(rx, ry, 0)
        nose.pos = vector(rx, ry + 0.4, 0)
        chute_marker.pos = vector(rx, ry + 0.6, 0)

        trail.append(pos=vector(rx, ry, 0))

        alt_label.pos = vector(rx + 2, ry + 5, 0)
        alt_label.text = f"Altitude: {ry:.1f} m"
        status_label.pos = vector(rx + 2, ry + 3, 0)

        if chute_list[i] and not chute_deployed:
            chute_deployed = True
            chute_marker.visible = True
            rocket.color = vector(1, 0.5, 0)
            status_label.text = "Status: Chute deployed"
        elif not chute_deployed:
            status_label.text = "Status: Powered flight"

    status_label.text = "Status: Landed"

run_animation()