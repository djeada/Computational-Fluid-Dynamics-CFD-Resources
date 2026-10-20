"""Plot a NACA 2412 airfoil at several angles of attack.

Builds the NACA 4-digit airfoil geometry (camber line plus thickness
distribution), pitches it nose-up about the leading edge for each angle of
attack, and draws one panel per angle with the free-stream direction, the
extended chord line, the angle-of-attack arc and the thin-airfoil estimate
c_l = 2 pi (alpha - alpha_L0).
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
CHORD = 1.0  # chord length (arbitrary length units)
N_POINTS = 200  # chordwise stations per surface
DEFAULT_ANGLES = [0.0, 8.0, 16.0]  # angles of attack in degrees
ALPHA_ZERO_LIFT = -2.08  # deg, thin-airfoil zero-lift angle of NACA 2412


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
    """One panel per angle: pitched airfoil, free stream, chord line and alpha."""
    xu, yu, xl, yl = naca4_airfoil(
        m=MAX_CAMBER, p=CAMBER_POSITION, t=THICKNESS, c=CHORD, n=N_POINTS
    )
    name = f"NACA {round(MAX_CAMBER * 100)}{round(CAMBER_POSITION * 10)}"
    name += f"{round(THICKNESS * 100):02d}"

    n = len(angles_of_attack)
    fig, axes = plt.subplots(1, n, figsize=(4.3 * n, 3.4), squeeze=False)
    colours = plt.cm.tab10(np.arange(n))
    for ax, angle, colour in zip(axes[0], angles_of_attack, colours, strict=True):
        xu_rot, yu_rot = pitch_airfoil(xu, yu, angle)
        xl_rot, yl_rot = pitch_airfoil(xl, yl, angle)
        ax.fill(
            np.r_[xu_rot, xl_rot[::-1]],
            np.r_[yu_rot, yl_rot[::-1]],
            color=colour,
            alpha=0.25,
        )
        ax.plot(xu_rot, yu_rot, color=colour, lw=1.5)
        ax.plot(xl_rot, yl_rot, color=colour, lw=1.5)

        # Chord line, extended ahead of the nose, and the free-stream direction.
        alpha = np.radians(angle)
        ext = np.array([-0.6 * CHORD, CHORD])
        ax.plot(ext * np.cos(alpha), -ext * np.sin(alpha), "--", color="0.2", lw=1)
        ax.plot([-0.6 * CHORD, 0], [0, 0], color="0.2", lw=1)
        for y0 in (0.38, 0.52):
            ax.annotate(
                "",
                xy=(-0.3 * CHORD, y0 * CHORD),
                xytext=(-0.75 * CHORD, y0 * CHORD),
                arrowprops=dict(arrowstyle="-|>", color="0.3"),
            )
        ax.text(-0.75 * CHORD, 0.58 * CHORD, r"$V_\infty$ (free stream)", fontsize=10)

        # Angle arc between the free stream and the chord line, ahead of the nose.
        if angle != 0:
            arc = np.linspace(np.pi, np.pi - alpha, 30)
            radius = 0.45 * CHORD
            ax.plot(radius * np.cos(arc), radius * np.sin(arc), color="tab:red", lw=1.5)
            ax.text(
                -0.8 * CHORD,
                -0.13 * CHORD,
                rf"$\alpha = {angle:g}^\circ$",
                color="tab:red",
                fontsize=11,
            )
        else:
            ax.text(
                -0.8 * CHORD,
                -0.13 * CHORD,
                r"$\alpha = 0^\circ$",
                color="tab:red",
                fontsize=11,
            )
        cl = 2 * np.pi * (alpha - np.radians(ALPHA_ZERO_LIFT))
        ax.set_title(
            f"{name}, $\\alpha = {angle:g}^\\circ$\nthin-airfoil $c_l$ = {cl:.2f}"
        )
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-0.85 * CHORD, 1.1 * CHORD)
        ax.set_ylim(-0.45 * CHORD, 0.7 * CHORD)
        ax.set_xlabel("x (chord units)")
        ax.grid(alpha=0.3)
    axes[0][0].set_ylabel("y (chord units)")
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--angles",
        type=float,
        nargs="+",
        default=DEFAULT_ANGLES,
        metavar="DEG",
        help="angles of attack in degrees (default: 0 8 16)",
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
