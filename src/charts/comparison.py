import matplotlib.pyplot as plt
import numpy as np


def _draw_fork(ax, rake_deg, offset_mm, wheel_radius_mm, title=None):
    """Draw fork geometry onto a given Axes."""
    rake_rad = np.radians(rake_deg)
    offset = offset_mm / 1000.0
    R = wheel_radius_mm / 1000.0

    trail = (R * np.sin(rake_rad) - offset) / np.cos(rake_rad)

    axle = np.array([0, R])
    x_pivot_ground = -trail

    wheel = plt.Circle(axle, R, color='gray', fill=False, lw=2, label='Front Wheel')
    ax.add_patch(wheel)
    ax.plot(0, R, 'ko', markersize=5)

    ax.axhline(0, color='black', lw=2)

    y_top = R * 2.2
    x_top = x_pivot_ground + y_top * np.tan(rake_rad)
    ax.plot([x_pivot_ground, x_top], [0, y_top], 'r--', lw=1.5, label='Steering Axis')

    fork_y_top = R * 2.1
    fork_x_top = (fork_y_top - R) * np.tan(rake_rad)
    ax.plot([0, fork_x_top], [R, fork_y_top], 'b-', lw=3, label='Fork Tubes')

    ax.annotate('', xy=(x_pivot_ground, -0.02), xytext=(0, -0.02),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax.text(x_pivot_ground / 2, 0.04, f'TRAIL: {trail * 1000:.1f} mm',
            color='green', fontweight='bold', ha='center', fontsize=10)

    ax.plot(0, 0, 'go', label='Contact Patch')
    ax.plot(x_pivot_ground, 0, 'ro', label='Pivot Point')

    label = title or f"{rake_deg}° Rake, {offset_mm}mm Offset"
    ax.set_title(label)
    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.legend(fontsize=8)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_aspect('equal')


def plot_fork_comparison(configs, suptitle="Fork Geometry Comparison"):
    """
    Side-by-side comparison of multiple fork geometries.
    configs: list of dicts, each with keys:
        rake_deg, offset_mm, wheel_radius_mm, title (optional)
    suptitle: overall figure title
    """
    n = len(configs)
    fig, axes = plt.subplots(1, n, figsize=(7 * n, 6))
    if n == 1:
        axes = [axes]
    for ax, cfg in zip(axes, configs):
        _draw_fork(
            ax,
            cfg.get('rake_deg', 25),
            cfg.get('offset_mm', 30),
            cfg.get('wheel_radius_mm', 315),
            title=cfg.get('title'),
        )
    fig.suptitle(suptitle, fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()
