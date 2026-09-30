"""Maxwell-Boltzmann speed distribution of N2 molecules at several temperatures.

Plots f(v) for 300, 600, 900 and 1200 K and marks the most probable, mean and
root-mean-square speed of each curve.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

K_B = 1.380649e-23  # Boltzmann constant, J/K
M_N2 = 4.65e-26  # mass of one N2 molecule, kg (28.01 u)
TEMPERATURES = [300, 600, 900, 1200]  # K
MAX_SPEED = 3000.0  # m/s


def maxwell_boltzmann_distribution(v, T, m=M_N2):
    """Probability density f(v) (s/m) of molecular speed v (m/s) at temperature T (K)."""
    a = m / (2 * K_B * T)
    return 4 * np.pi * (a / np.pi) ** 1.5 * v**2 * np.exp(-a * v**2)


def characteristic_speeds(T, m=M_N2):
    """Return the most probable, mean and RMS speeds (m/s)."""
    v_p = np.sqrt(2 * K_B * T / m)
    v_mean = np.sqrt(8 * K_B * T / (np.pi * m))
    v_rms = np.sqrt(3 * K_B * T / m)
    return v_p, v_mean, v_rms


def plot_distributions(temperatures=TEMPERATURES, max_speed=MAX_SPEED):
    """Plot one distribution per temperature and return the figure."""
    velocities = np.linspace(0, max_speed, 500)
    speed_styles = [
        (":", "most probable $v_p$"),
        ("--", r"mean $\bar{v}$"),
        ("-.", "RMS $v_{rms}$"),
    ]

    fig = plt.figure(figsize=(12, 8))
    handles = []
    for T in temperatures:
        (line,) = plt.plot(
            velocities, maxwell_boltzmann_distribution(velocities, T), label=f"{T} K"
        )
        handles.append(line)
        for speed, (style, _) in zip(characteristic_speeds(T), speed_styles):
            plt.vlines(
                speed,
                0,
                maxwell_boltzmann_distribution(speed, T),
                colors=line.get_color(),
                linestyles=style,
            )

    handles += [
        Line2D([], [], color="black", linestyle=style, label=label)
        for style, label in speed_styles
    ]

    plt.xlabel("Speed $v$ (m/s)", fontsize=14)
    plt.ylabel("Probability density $f(v)$ (s/m)", fontsize=14)
    plt.legend(handles=handles, fontsize=12)
    plt.grid(True)
    plt.title(
        "Probability Distribution Function of N$_2$ Molecular Speeds", fontsize=16
    )
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlim(0, max_speed)
    plt.ylim(0, None)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for T in TEMPERATURES:
        v_p, v_mean, v_rms = characteristic_speeds(T)
        print(
            f"T = {T:5d} K: v_p = {v_p:6.1f}, mean = {v_mean:6.1f}, rms = {v_rms:6.1f} m/s"
        )

    fig = plot_distributions()

    finish_figures(
        {"probability_distribution_function.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
