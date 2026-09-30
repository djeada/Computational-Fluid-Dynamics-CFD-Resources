"""Quasi-one-dimensional isentropic flow through a converging-diverging nozzle.

The nozzle has a linear converging wall (height 0.8 -> 0.4) followed by a
linear diverging wall (0.4 -> 0.7). At the design condition the flow is
subsonic upstream of the throat, sonic at the throat and supersonic
downstream. The local Mach number follows from the isentropic area-Mach
relation A/A* = f(M), and streamlines that follow the walls (y/h = const) are
drawn and coloured by Mach number.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GAMMA = 1.4  # ratio of specific heats (air) [-]
X_MIN, X_MAX = 0.0, 2.0  # nozzle length [arbitrary units]
Y_MIN, Y_MAX = 0.0, 1.0  # plotting window height [arbitrary units]
X_THROAT = 1.0  # throat location [arbitrary units]
H_INLET, H_THROAT, H_EXIT = (
    0.8,
    0.4,
    0.7,
)  # wall heights (unit depth => area) [arbitrary units]
NX, NY = 100, 50  # grid points for the streamline plot


def nozzle_top(x):
    """Height of the top wall; linear converging then linear diverging."""
    x = np.asarray(x, dtype=float)
    converging = H_INLET + (H_THROAT - H_INLET) * (x - X_MIN) / (X_THROAT - X_MIN)
    diverging = H_THROAT + (H_EXIT - H_THROAT) * (x - X_THROAT) / (X_MAX - X_THROAT)
    return np.where(x <= X_THROAT, converging, diverging)


def nozzle_slope(x):
    """Derivative dh/dx of the top wall."""
    x = np.asarray(x, dtype=float)
    return np.where(
        x <= X_THROAT,
        (H_THROAT - H_INLET) / (X_THROAT - X_MIN),
        (H_EXIT - H_THROAT) / (X_MAX - X_THROAT),
    )


def area_ratio(mach, gamma=GAMMA):
    """Isentropic area ratio A/A* as a function of Mach number."""
    term = 2.0 / (gamma + 1.0) * (1.0 + 0.5 * (gamma - 1.0) * mach**2)
    return term ** ((gamma + 1.0) / (2.0 * (gamma - 1.0))) / mach


def mach_from_area_ratio(ratio, supersonic, gamma=GAMMA, iterations=60):
    """Invert A/A* = f(M) by bisection on the subsonic or supersonic branch.

    ``ratio`` and ``supersonic`` are broadcast element-wise. f(M) decreases on
    0 < M < 1 and increases on M > 1, so each branch has one root for
    ratio >= 1.
    """
    ratio = np.asarray(ratio, dtype=float)
    supersonic = np.broadcast_to(supersonic, ratio.shape)
    lo = np.where(supersonic, 1.0, 1e-6)
    hi = np.where(supersonic, 50.0, 1.0)
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        too_big = area_ratio(mid, gamma) > ratio
        # Subsonic branch: f too big means M too small. Supersonic: M too big.
        move_lo = np.where(supersonic, ~too_big, too_big)
        lo = np.where(move_lo, mid, lo)
        hi = np.where(move_lo, hi, mid)
    return 0.5 * (lo + hi)


def solve_nozzle(X, Y, gamma=GAMMA):
    """Return u, v (scaled by the stagnation speed of sound a0) and Mach number on a grid.

    Points above the top wall are set to NaN so the streamlines stop at the wall.
    """
    h = nozzle_top(X)
    mach = mach_from_area_ratio(h / H_THROAT, X > X_THROAT, gamma)
    a_over_a0 = 1.0 / np.sqrt(1.0 + 0.5 * (gamma - 1.0) * mach**2)
    u = mach * a_over_a0
    # Streamlines follow y/h = const, so dy/dx = v/u = y h'(x) / h(x)
    v = u * Y * nozzle_slope(X) / h
    inside = Y <= h
    return (
        np.where(inside, u, np.nan),
        np.where(inside, v, np.nan),
        np.where(inside, mach, np.nan),
    )


def plot_nozzle(x, y, u, v, mach):
    """Plot walls and Mach-coloured streamlines; return the figure."""
    X, Y = np.meshgrid(x, y)
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.plot(x, nozzle_top(x), "k", lw=2, label="Nozzle top boundary")
    ax.plot(x, np.zeros_like(x), "k", lw=2, label="Nozzle bottom boundary")
    strm = ax.streamplot(X, Y, u, v, color=mach, cmap="jet", density=1.4, linewidth=1.2)
    fig.colorbar(strm.lines, ax=ax, label="Mach Number")
    ax.axvline(X_THROAT, color="grey", ls=":", lw=1)
    ax.set_aspect("equal", "box")
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_xlabel("x (arbitrary units)")
    ax.set_ylabel("y (arbitrary units)")
    ax.set_title(
        "Isentropic Flow Through a Converging-Diverging Nozzle (design condition)"
    )
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    x = np.linspace(X_MIN, X_MAX, NX)
    y = np.linspace(Y_MIN, Y_MAX, NY)
    X, Y = np.meshgrid(x, y)
    u, v, mach = solve_nozzle(X, Y)

    for xp in (X_MIN, X_THROAT, X_MAX):
        m = mach_from_area_ratio(nozzle_top(xp) / H_THROAT, xp > X_THROAT)
        print(
            f"x = {xp:.1f}: A/A* = {nozzle_top(xp) / H_THROAT:.3f}, M = {float(m):.3f}"
        )

    fig = plot_nozzle(x, y, u, v, mach)

    finish_figures({"nozzle_flow.png": fig}, output=args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
