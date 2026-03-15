import numpy as np
import matplotlib.pyplot as plt
from .wobble_model import simulate_wobble


def plot_wobble_comparison(trail_val=0.1, c_mech=5.0, I_steer=1.5,
                           speeds=None, t_span=(0, 5), trigger_delta=0.1):
    """
    Single-call plot that simulates wobble at multiple speeds and annotates
    each curve as Stable / Critical / Unstable based on whether the
    oscillation amplitude grows or decays.
    """
    if speeds is None:
        speeds = [10, 25, 45]

    n = len(speeds)
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    fig, axes = plt.subplots(n, 1, figsize=(12, 3.5 * n), sharex=True)
    if n == 1:
        axes = [axes]

    y_limit = np.degrees(trigger_delta) * 4
    results = []

    for i, v in enumerate(speeds):
        t, delta = simulate_wobble(v=v, trail=trail_val, c_mech=c_mech,
                                   I_steer=I_steer, t_span=t_span,
                                   trigger_delta=trigger_delta)
        delta_deg = np.degrees(delta)
        delta_deg_clipped = np.clip(delta_deg, -y_limit, y_limit)

        peak_start = np.max(np.abs(delta_deg[:len(delta_deg) // 4]))
        peak_end = np.max(np.abs(delta_deg[3 * len(delta_deg) // 4:]))

        if peak_end < 0.3 * peak_start:
            tag = "Stable"
        elif peak_end > 1.2 * peak_start:
            tag = "Unstable"
        else:
            tag = "Critical"

        results.append((t, delta_deg_clipped, tag))

    for i, (t, delta_deg_clipped, tag) in enumerate(results):
        ax = axes[i]
        v = speeds[i]
        color = colors[i % len(colors)]
        ax.plot(t, delta_deg_clipped, color=color, linewidth=2)
        ax.axhline(0, color='black', linestyle='--', alpha=0.3)
        ax.set_ylim(-y_limit * 1.1, y_limit * 1.1)
        ax.set_ylabel('Steer Angle (°)')
        ax.set_title(f'{v} m/s ({v * 3.6:.0f} km/h) — {tag}',
                     fontsize=11, fontweight='bold', color=color)
        ax.grid(True, linestyle=':', alpha=0.6)

    axes[-1].set_xlabel('Time (s)')
    fig.suptitle('Steering Wobble Response at Different Speeds',
                 fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.show()
