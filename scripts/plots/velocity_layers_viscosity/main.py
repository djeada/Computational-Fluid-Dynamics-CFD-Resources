"""Schematic of three fluid layers sliding at different speeds, illustrating tau = mu du/dy.

Each layer is drawn as a bar whose length is the layer velocity, so the bars
form a stepped velocity profile. The velocity gradient between adjacent layers
is annotated at each interface.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

LAYERS = ["Slow layer (bottom)", "Medium layer (middle)", "Fast layer (top)"]
VELOCITIES = [0, 5, 10]  # arbitrary units
LAYER_BOUNDARIES = [0, 1, 2, 3]  # layer positions, arbitrary units
COLORS = ["lightblue", "skyblue", "dodgerblue"]


def interface_gradients(velocities, boundaries):
    """Velocity gradient du/dy between the centres of adjacent layers."""
    centres = [(lo + hi) / 2 for lo, hi in zip(boundaries[:-1], boundaries[1:])]
    return [
        (velocities[i + 1] - velocities[i]) / (centres[i + 1] - centres[i])
        for i in range(len(velocities) - 1)
    ]


def draw_layers(layers=LAYERS, velocities=VELOCITIES, boundaries=LAYER_BOUNDARIES):
    """Draw the layer schematic and return the figure."""
    fig, ax = plt.subplots(figsize=(8, 6))
    v_max = max(velocities)

    for i, layer in enumerate(layers):
        ax.fill_betweenx(
            [boundaries[i], boundaries[i + 1]],
            0,
            velocities[i],
            color=COLORS[i],
            alpha=0.7,
            label=f"{layer} (V = {velocities[i]})",
        )

    # Layer velocity labels
    for i, velocity in enumerate(velocities):
        mid = (boundaries[i] + boundaries[i + 1]) / 2
        ax.annotate(
            f"V = {velocity}",
            xy=(velocity, mid),
            xytext=(velocity + 1, mid),
            va="center",
            arrowprops=dict(arrowstyle="->"),
        )

    # Interfaces between layers, where adjacent layers exert shear on each other
    for i, gradient in enumerate(interface_gradients(velocities, boundaries)):
        y = boundaries[i + 1]
        ax.axhline(y, color="gray", linestyle="--", linewidth=1)
        ax.text(
            v_max + 0.5,
            y,
            f"$\\Delta V/\\Delta y$ = {gradient:g}\n$\\tau = \\mu\\, du/dy$",
            va="center",
            fontsize=10,
            color="red",
        )

    ax.annotate(
        "Velocity gradient\n(viscous forces)",
        xy=(velocities[1], boundaries[2]),
        xytext=(7.5, 1.7),
        arrowprops=dict(arrowstyle="->", color="red"),
        fontsize=10,
        color="red",
        va="center",
    )

    ax.set_xlim(-0.5, v_max + 3.5)
    ax.set_ylim(boundaries[0], boundaries[-1])
    ax.set_xlabel("Velocity (arbitrary units)")
    ax.set_ylabel("Layer Position")
    ax.set_title("Velocity Gradient and Viscous Forces in Fluid Layers")
    ax.set_yticks([])
    ax.legend(loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.6)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = draw_layers()

    finish_figures(
        {"velocity_layers_viscosity.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
