"""Compare prescribed incompressible and compressible velocity fields in a 2D duct.

The incompressible case is a fully developed parabolic profile that is the same
at every streamwise station. The compressible case is a schematic, prescribed
field whose parabolic profile grows linearly in amplitude along the duct, as it
would in a flow whose density falls downstream (steady continuity requires
rho * U = const in a constant-area duct). Both fields are drawn as colour maps
of speed on a shared colour scale with velocity arrows on top.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Domain (non-dimensional length units)
NX, NY = 40, 10  # grid points in x and y
X_MAX, Y_MAX = 10.0, 2.0  # duct length and height

# Velocity scales (non-dimensional velocity units)
U_MAX_INCOMP = 2.0  # centreline speed of the incompressible profile
U_INLET = 1.0  # centreline speed of the compressible profile at x = 0
U_OUTLET = 4.0  # centreline speed of the compressible profile at x = X_MAX


def make_grid(nx=NX, ny=NY, x_max=X_MAX, y_max=Y_MAX):
    """Return the meshgrid arrays X, Y covering [0, x_max] x [0, y_max]."""
    x = np.linspace(0.0, x_max, nx)
    y = np.linspace(0.0, y_max, ny)
    return np.meshgrid(x, y)


def parabolic_shape(Y, y_max=Y_MAX):
    """Parabola equal to 1 on the centreline and 0 on the walls y = 0, y_max."""
    y_mid = y_max / 2.0
    return np.clip(1.0 - ((Y - y_mid) / y_mid) ** 2, 0.0, None)


def incompressible_field(X, Y, u_max=U_MAX_INCOMP, y_max=Y_MAX):
    """Fully developed profile u = u_max * [1 - ((y - y_mid)/y_mid)^2], v = 0."""
    u = u_max * parabolic_shape(Y, y_max)
    return u, np.zeros_like(u)


def compressible_field(
    X, Y, u_inlet=U_INLET, u_outlet=U_OUTLET, x_max=X_MAX, y_max=Y_MAX
):
    """Accelerating profile u = (u_inlet + slope * x) * parabola(y), v = 0."""
    slope = (u_outlet - u_inlet) / x_max
    u = (u_inlet + slope * X) * parabolic_shape(Y, y_max)
    return u, np.zeros_like(u)


def plot_panel(ax, fig, X, Y, u, v, title, vmax, x_max=X_MAX, y_max=Y_MAX):
    """Draw the speed colour map, velocity arrows, and duct outline on ax."""
    speed = np.hypot(u, v)
    ax.add_patch(Rectangle((0, 0), x_max, y_max, fill=False, linewidth=1))
    mesh = ax.pcolormesh(X, Y, speed, shading="auto", vmin=0.0, vmax=vmax)
    fig.colorbar(mesh, ax=ax, label="Velocity Magnitude")
    ax.quiver(X, Y, u, v, color="white", scale=15)
    ax.set_xlim([0, x_max])
    ax.set_ylim([0, y_max])
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)


def make_figure():
    """Build the two-panel comparison figure."""
    X, Y = make_grid()
    u_inc, v_inc = incompressible_field(X, Y)
    u_comp, v_comp = compressible_field(X, Y)
    vmax = max(np.hypot(u_inc, v_inc).max(), np.hypot(u_comp, v_comp).max())

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    plot_panel(
        axes[0],
        fig,
        X,
        Y,
        u_inc,
        v_inc,
        "Incompressible Flow (Laminar Parabolic)",
        vmax,
    )
    plot_panel(
        axes[1], fig, X, Y, u_comp, v_comp, "Compressible Flow (Increasing Speed)", vmax
    )
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = make_figure()

    finish_figures(
        {"compressible_vs_incompressible.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
