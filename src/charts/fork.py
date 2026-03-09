import matplotlib.pyplot as plt
import numpy as np


def plot_fork_geometry(rake_deg=25, offset_mm=30, wheel_radius_mm=315):
    """
    Plots the steering geometry of a motorcycle front end.
    rake_deg: Angle of the steering head from vertical (degrees)
    offset_mm: Distance from steering axis to fork center (mm)
    wheel_radius_mm: Radius of the front wheel + tire (mm)
    """
    rake_rad = np.radians(rake_deg)
    offset = offset_mm / 1000.0
    R = wheel_radius_mm / 1000.0

    trail = (R * np.sin(rake_rad) - offset) / np.cos(rake_rad)

    axle = np.array([0, R])
    x_pivot_ground = -trail

    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    wheel = plt.Circle(axle, R, color='gray', fill=False, lw=2, label='Front Wheel')
    ax.add_patch(wheel)
    plt.plot(0, R, 'ko')

    plt.axhline(0, color='black', lw=2)

    y_top = R * 2.2
    x_top = x_pivot_ground + y_top * np.tan(rake_rad)
    plt.plot([x_pivot_ground, x_top], [0, y_top], 'r--', lw=1.5, label='Steering Axis')

    fork_y_top = R * 2.1
    fork_x_top = (fork_y_top - R) * np.tan(rake_rad)
    plt.plot([0, fork_x_top], [R, fork_y_top], 'b-', lw=3, label='Fork Tubes')

    plt.annotate('', xy=(x_pivot_ground, -0.02), xytext=(0, -0.02),
                 arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    plt.text(x_pivot_ground / 2, 0.04, f'TRAIL: {trail * 1000:.1f} mm',
             color='green', fontweight='bold', ha='center', fontsize=10)

    plt.plot(0, 0, 'go', label='Contact Patch')
    plt.plot(x_pivot_ground, 0, 'ro', label='Pivot Point')

    plt.title(f"Motorcycle Geometry: {rake_deg}° Rake, {offset_mm}mm Offset")
    plt.xlabel("Horizontal Distance (m)")
    plt.ylabel("Height (m)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.axis('equal')
    plt.show()
