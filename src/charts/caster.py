import matplotlib.pyplot as plt
import numpy as np


def plot_caster_response(configs=None):
    """
    Time-domain steering response after a disturbance for different trail values.
    Demonstrates how lower trail weakens restoring torque and grows overshoot.

    configs: optional list of dicts with keys:
        label, trail_mm, zeta (damping ratio), omega (natural freq Hz), color
    """
    if configs is None:
        configs = [
            {'label': 'High trail (130 mm)',  'zeta':  0.35, 'omega': 6.0, 'color': '#2ecc71'},
            {'label': 'Medium trail (90 mm)', 'zeta':  0.10, 'omega': 7.5, 'color': '#f39c12'},
            {'label': 'Low trail (50 mm)',    'zeta': -0.05, 'omega': 9.0, 'color': '#e74c3c'},
        ]

    t = np.linspace(0, 1.5, 1000)
    A = 3.0  # initial disturbance in degrees

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])

    # --- Top: time-domain oscillation ---
    for cfg in configs:
        zeta = cfg['zeta']
        omega_n = 2 * np.pi * cfg['omega']
        envelope = A * np.exp(-zeta * omega_n * t)
        delta = envelope * np.sin(omega_n * t)

        ax1.plot(t, delta, color=cfg['color'], lw=2, label=cfg['label'])
        ax1.plot(t, envelope, color=cfg['color'], lw=1, ls='--', alpha=0.4)
        ax1.plot(t, -envelope, color=cfg['color'], lw=1, ls='--', alpha=0.4)

    ax1.axhline(0, color='black', lw=0.8)
    ax1.set_title("Steering Response After a Disturbance", fontsize=13, fontweight='bold')
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Steering Angle (°)")
    ax1.legend(fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.5)

    # --- Bottom: restoring torque vs trail ---
    trail_range = np.linspace(0, 160, 200)
    F_lateral = 500  # representative lateral force in N
    torque = F_lateral * (trail_range / 1000.0)

    ax2.plot(trail_range, torque, color='#3498db', lw=2.5)
    ax2.fill_between(trail_range, torque, alpha=0.1, color='#3498db')
    ax2.set_title(r"Restoring Torque vs Trail  ($T = F_{lateral} \times t$)", fontsize=13, fontweight='bold')
    ax2.set_xlabel("Mechanical Trail (mm)")
    ax2.set_ylabel("Torque (N·m)")
    ax2.grid(True, linestyle=':', alpha=0.5)

    for cfg in configs:
        trail_val = int(cfg['label'].split('(')[1].split(' ')[0])
        torque_val = F_lateral * trail_val / 1000.0
        ax2.plot(trail_val, torque_val, 'o', color=cfg['color'], markersize=10, zorder=5)
        ax2.annotate(f'{trail_val} mm', xy=(trail_val, torque_val),
                     xytext=(trail_val + 5, torque_val + 5),
                     fontsize=9, fontweight='bold', color=cfg['color'])

    plt.tight_layout()
    plt.show()
