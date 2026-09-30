"""Plot a NACA 2412 airfoil at several angles of attack.

Builds the NACA 4-digit airfoil geometry (camber line plus thickness
distribution), pitches it nose-up about the leading edge for each angle of
attack, and draws the chord lines and the free-stream direction.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

MAX_CAMBER = 0.02  # m: maximum camber as a fraction of chord
CAMBER_POSITION = 0.4  # p: chordwise position of maximum camber
THICKNESS = 0.12  # t: maximum thickness as a fraction of chord
CHORD = 2.0  # chord length (arbitrary length units)
N_POINTS = 200  # chordwise stations per surface
DEFAULT_ANGLES = [10.0, 60.0]  # angles of attack in degrees


def naca4_airfoil(m, p, t, c=1.0, n=100):
    """Upper and lower surface coordinates of a NACA 4-digit airfoil."""
    x = np.linspace(0, c, n)
    xc = x / c

    # Thickness distribution for NACA 4-digit airfoils
    yt = (
        (t / 0.2)
        * c
        * (
            0.2969 * np.sqrt(xc)
            - 0.1260 * xc
            - 0.3516 * xc**2
            + 0.2843 * xc**3
            - 0.1015 * xc**4
        )
    )

    # Camber line and its slope
    yc = c * np.where(
        xc < p,
        m / p**2 * (2 * p * xc - xc**2),
        m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * xc - xc**2),
    )
    dyc_dx = np.where(xc < p, 2 * m / p**2 * (p - xc), 2 * m / (1 - p) ** 2 * (p - xc))
    theta = np.arctan(dyc_dx)

    # Surfaces offset perpendicular to the camber line
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)
    return xu, yu, xl, yl


def pitch_airfoil(x, y, angle_of_attack):
    """Rotate points about the origin (leading edge) nose-up by angle_of_attack.

    The free stream flows in the +x direction, so a positive angle of attack
    is a clockwise rotation that moves the trailing edge below the leading
    edge.
    """
    alpha = np.radians(angle_of_attack)
    rotation_matrix = np.array(
        [[np.cos(alpha), np.sin(alpha)], [-np.sin(alpha), np.cos(alpha)]]
    )
    rotated = rotation_matrix @ np.vstack((x, y))
    return rotated[0], rotated[1]


def plot_multiple_airfoils(angles_of_attack):
    fig, ax = plt.subplots(figsize=(14, 7))

    xu, yu, xl, yl = naca4_airfoil(
        m=MAX_CAMBER, p=CAMBER_POSITION, t=THICKNESS, c=CHORD, n=N_POINTS
    )
    name = f"NACA {round(MAX_CAMBER * 100)}{round(CAMBER_POSITION * 10)}"
    name += f"{round(THICKNESS * 100):02d}"

    for angle in angles_of_attack:
        xu_rot, yu_rot = pitch_airfoil(xu, yu, angle)
        xl_rot, yl_rot = pitch_airfoil(xl, yl, angle)

        (line,) = ax.plot(
            xu_rot, yu_rot, linestyle="-", label=f"{name}, $\\alpha = {angle:g}^\\circ$"
        )
        ax.plot(xl_rot, yl_rot, linestyle="-", color=line.get_color())

        # Chord line from the leading edge to the trailing edge
        alpha = np.radians(angle)
        ax.annotate(
            "",
            xy=(CHORD * np.cos(alpha), -CHORD * np.sin(alpha)),
            xytext=(0, 0),
            arrowprops=dict(
                arrowstyle="->", linestyle="--", fill=False, color=line.get_color()
            ),
        )

    # Free-stream direction along +x
    ax.annotate(
        "",
        xy=(3.5, 0.5),
        xytext=(-1.5, 0.5),
        arrowprops=dict(arrowstyle="->", linestyle="--", fill=False),
    )
    ax.text(-1.5, 0.6, r"Free stream $V_\infty$")

    angle_text = " and ".join(f"{a:g}°" for a in angles_of_attack)
    ax.set_title(f"Comparison of Airfoils with Angles of Attack: {angle_text}")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    ax.legend(loc="upper right")
    ax.set_xlim(-2, 4)
    ax.set_ylim(-2, 1)
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--angles",
        type=float,
        nargs="+",
        default=DEFAULT_ANGLES,
        metavar="DEG",
        help="angles of attack in degrees (default: 10 60)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    fig = plot_multiple_airfoils(args.angles)

    finish_figures(
        {"airfoil_angle_attack.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
