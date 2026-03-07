import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def trail_mm(rake_deg, offset_mm=30, wheel_radius_mm=315):
    """Return mechanical trail in mm for given rake (degrees)."""
    rake_rad = np.radians(rake_deg)
    return (wheel_radius_mm * np.sin(rake_rad) - offset_mm) / np.cos(rake_rad)


def plot_trail_vs_rake(
    rake_range=(20, 35),
    offsets_mm=(20, 30, 40),
    wheel_radius_mm=315,
):
    """
    Parametric sweep: mechanical trail vs. rake angle for several fork offsets.

    Highlights the typical sport-bike and cruiser operating windows so the
    reader can see how geometry choices map to trail values.
    """
    rakes = np.linspace(rake_range[0], rake_range[1], 200)

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = plt.cm.viridis(np.linspace(0.2, 0.85, len(offsets_mm)))

    for offset, color in zip(offsets_mm, colors):
        trails = trail_mm(rakes, offset_mm=offset, wheel_radius_mm=wheel_radius_mm)
        ax.plot(rakes, trails, lw=2.5, color=color,
                label=f'Offset = {offset} mm')

    ax.axvspan(23, 27, alpha=0.10, color='blue', label='Sport-bike zone')
    ax.axvspan(30, 34, alpha=0.10, color='red', label='Cruiser zone')

    ax.set_xlabel('Rake Angle (degrees)', fontsize=12)
    ax.set_ylabel('Mechanical Trail (mm)', fontsize=12)
    ax.set_title('Mechanical Trail vs. Rake Angle', fontsize=14)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.legend(fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.5)
    fig.tight_layout()
    plt.show()
