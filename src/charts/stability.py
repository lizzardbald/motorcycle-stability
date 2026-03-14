import matplotlib.pyplot as plt
import numpy as np


def plot_eigenvalue_vs_speed(I_steer=0.6, c0=12.0, c1=0.07, k0=80.0, k1=0.002):
    """
    Plots eigenvalue real/imaginary parts vs forward speed to show
    the stability boundary (Hopf bifurcation) of the wobble mode.

    Simplified model:
        c_eff(v) = c0 - c1 * v^2   (damping decreases with speed)
        k_eff(v) = k0 + k1 * v^2   (stiffness mildly increases with speed)
    """
    speeds_kmh = np.linspace(0, 300, 500)
    speeds_ms = speeds_kmh / 3.6

    c_eff = c0 - c1 * speeds_ms ** 2
    k_eff = k0 + k1 * speeds_ms ** 2

    discriminant = c_eff ** 2 - 4 * I_steer * k_eff

    sigma = np.zeros_like(speeds_ms)
    omega = np.zeros_like(speeds_ms)

    for i in range(len(speeds_ms)):
        disc = discriminant[i]
        if disc >= 0:
            s1 = (-c_eff[i] + np.sqrt(disc)) / (2 * I_steer)
            sigma[i] = s1
            omega[i] = 0.0
        else:
            sigma[i] = -c_eff[i] / (2 * I_steer)
            omega[i] = np.sqrt(-disc) / (2 * I_steer)

    # Find critical speed (where sigma crosses zero)
    sign_changes = np.where(np.diff(np.sign(sigma)))[0]
    v_critical = None
    if len(sign_changes) > 0:
        idx = sign_changes[0]
        v_critical = np.interp(0, [sigma[idx], sigma[idx + 1]],
                               [speeds_kmh[idx], speeds_kmh[idx + 1]])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # --- Real part (stability) ---
    ax1.plot(speeds_kmh, sigma, color='#e74c3c', lw=2.5)
    ax1.axhline(0, color='black', lw=1, ls='--')
    ax1.fill_between(speeds_kmh, sigma, 0, where=(sigma < 0),
                     alpha=0.1, color='#2ecc71', label='Stable (damped)')
    ax1.fill_between(speeds_kmh, sigma, 0, where=(sigma >= 0),
                     alpha=0.15, color='#e74c3c', label='Unstable (growing)')
    if v_critical is not None:
        ax1.axvline(v_critical, color='#f39c12', lw=2, ls='--',
                    label=f'Critical speed $v_c$ = {v_critical:.0f} km/h')
    ax1.set_ylabel(r"Real part $\sigma$ (1/s)")
    ax1.set_title("Eigenvalue Analysis: Wobble Mode Stability vs Speed",
                  fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.5)

    # --- Imaginary part (frequency) ---
    freq_hz = omega / (2 * np.pi)
    ax2.plot(speeds_kmh, freq_hz, color='#3498db', lw=2.5)
    if v_critical is not None:
        ax2.axvline(v_critical, color='#f39c12', lw=2, ls='--')
    ax2.set_xlabel("Forward Speed (km/h)")
    ax2.set_ylabel("Wobble Frequency (Hz)")
    ax2.set_title("Oscillation Frequency vs Speed", fontsize=13, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.5)

    typical_band = ax2.axhspan(7, 10, alpha=0.1, color='#e74c3c',
                               label='Typical tank slapper range (7–10 Hz)')
    ax2.legend(handles=[typical_band], fontsize=10)

    plt.tight_layout()
    plt.show()

    if v_critical is not None:
        print(f"  Critical speed (Hopf bifurcation): {v_critical:.0f} km/h")
        idx_c = np.argmin(np.abs(speeds_kmh - v_critical))
        print(f"  Wobble frequency at critical speed: {freq_hz[idx_c]:.1f} Hz")


def plot_time_domain_wobble(I_steer=0.6, c0=12.0, c1=0.07, k0=80.0, k1=0.002):
    """
    Shows steering angle over time at three speeds:
    below critical, at critical, and above critical.
    """
    speeds_ms_all = np.linspace(0, 300 / 3.6, 500)
    c_eff_all = c0 - c1 * speeds_ms_all ** 2
    sign_changes = np.where(np.diff(np.sign(c_eff_all)))[0]
    if len(sign_changes) > 0:
        idx = sign_changes[0]
        vc_ms = np.interp(0, [c_eff_all[idx], c_eff_all[idx + 1]],
                          [speeds_ms_all[idx], speeds_ms_all[idx + 1]])
    else:
        vc_ms = 50.0

    cases = [
        {'v_ms': vc_ms * 0.7, 'color': '#2ecc71', 'label': 'Below $v_c$'},
        {'v_ms': vc_ms,        'color': '#f39c12', 'label': 'At $v_c$ (critical)'},
        {'v_ms': vc_ms * 1.15, 'color': '#e74c3c', 'label': 'Above $v_c$'},
    ]

    t = np.linspace(0, 1.5, 2000)
    A = 2.0  # initial perturbation in degrees

    fig, ax = plt.subplots(figsize=(12, 5))

    for case in cases:
        v = case['v_ms']
        c_eff = c0 - c1 * v ** 2
        k_eff = k0 + k1 * v ** 2

        sigma_val = -c_eff / (2 * I_steer)
        disc = c_eff ** 2 - 4 * I_steer * k_eff
        if disc < 0:
            omega_val = np.sqrt(-disc) / (2 * I_steer)
        else:
            omega_val = 8.0 * 2 * np.pi

        delta = A * np.exp(sigma_val * t) * np.sin(omega_val * t)

        ax.plot(t, delta, color=case['color'], lw=2, label=f"{case['label']} ({v * 3.6:.0f} km/h)")

    ax.axhline(0, color='black', lw=0.8)
    ax.set_title("Steering Response to a Disturbance at Different Speeds",
                fontsize=13, fontweight='bold')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Steering Angle (°)")
    ax.legend(fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.show()


def _compute_sigma(speeds_ms, I_steer, c0, c1, k0, k1):
    """Compute real part of eigenvalue across speed range."""
    c_eff = c0 - c1 * speeds_ms ** 2
    k_eff = k0 + k1 * speeds_ms ** 2
    discriminant = c_eff ** 2 - 4 * I_steer * k_eff
    sigma = np.zeros_like(speeds_ms)
    for i in range(len(speeds_ms)):
        if discriminant[i] >= 0:
            sigma[i] = (-c_eff[i] + np.sqrt(discriminant[i])) / (2 * I_steer)
        else:
            sigma[i] = -c_eff[i] / (2 * I_steer)
    return sigma


def _find_critical_speed(speeds_kmh, sigma):
    """Find speed where sigma crosses zero."""
    sign_changes = np.where(np.diff(np.sign(sigma)))[0]
    if len(sign_changes) > 0:
        idx = sign_changes[0]
        return np.interp(0, [sigma[idx], sigma[idx + 1]],
                         [speeds_kmh[idx], speeds_kmh[idx + 1]])
    return None


def plot_damper_effect(I_steer=0.6, c0=12.0, c1=0.07, k0=80.0, k1=0.002,
                       damper_values=None):
    """
    Overlays eigenvalue real-part curves with and without steering damper
    to show how added damping shifts the critical speed.
    """
    if damper_values is None:
        damper_values = [0, 4, 8]

    speeds_kmh = np.linspace(0, 350, 500)
    speeds_ms = speeds_kmh / 3.6

    colors = ['#e74c3c', '#f39c12', '#2ecc71']
    labels = ['No damper', 'Light damper', 'Heavy damper']

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axhline(0, color='black', lw=1, ls='--')

    for i, c_damper in enumerate(damper_values):
        sigma = _compute_sigma(speeds_ms, I_steer, c0 + c_damper, c1, k0, k1)
        vc = _find_critical_speed(speeds_kmh, sigma)

        lbl = labels[i] if i < len(labels) else f'$c_{{damper}}$ = {c_damper}'
        if vc is not None:
            lbl += f'  ($v_c$ = {vc:.0f} km/h)'
        else:
            lbl += '  (stable across range)'

        ax.plot(speeds_kmh, sigma, color=colors[i % len(colors)], lw=2.5, label=lbl)

        if vc is not None:
            ax.axvline(vc, color=colors[i % len(colors)], lw=1.5, ls=':', alpha=0.6)

    ax.fill_between(speeds_kmh, ax.get_ylim()[0], 0, alpha=0.04, color='#2ecc71')
    ax.fill_between(speeds_kmh, 0, ax.get_ylim()[1], alpha=0.04, color='#e74c3c')

    ax.set_xlabel("Forward Speed (km/h)")
    ax.set_ylabel(r"Real part $\sigma$ (1/s)")
    ax.set_title("Effect of Steering Damper on Wobble Stability",
                fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.show()
