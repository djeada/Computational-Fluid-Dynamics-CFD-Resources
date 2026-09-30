"""Animate the 2D wave equation on a square with an explicit leapfrog scheme.

A Gaussian pulse at rest in the centre of [-L, L]^2 spreads outward, reflects
from the fixed (u = 0) edges and interferes with itself. The field is shown as a
3D surface on a dark background.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int, save_figure  # noqa: E402

L = 5.0  # half-width of the square domain
NX = 100  # grid points in x
NY = 100  # grid points in y
C = 1.0  # wave speed
CFL_SAFETY = 0.5  # dt = CFL_SAFETY * min(dx, dy) / (c * sqrt(2))
T_END = 40.0  # simulated time of the default animation
SCALE_FACTOR = 5.0  # amplitude of the initial Gaussian pulse


def make_grid(length=L, nx=NX, ny=NY, c=C, cfl_safety=CFL_SAFETY):
    """Return X, Y, dx, dy, dt; axis 0 is y and axis 1 is x."""
    if nx < 3 or ny < 3 or length <= 0 or c <= 0 or not 0 < cfl_safety <= 1:
        raise ValueError(
            "require grids >= 3, positive length/speed, and 0 < CFL safety <= 1"
        )
    x = np.linspace(-length, length, nx)
    y = np.linspace(-length, length, ny)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    dt = cfl_safety * min(dx, dy) / (c * np.sqrt(2))
    X, Y = np.meshgrid(x, y)
    return X, Y, dx, dy, dt


def initial_condition(X, Y, dx, dy, dt, c=C, amplitude=SCALE_FACTOR):
    """Gaussian pulse with fixed edges and a second-order zero-velocity start."""
    u0 = amplitude * np.exp(-0.5 * (X**2 + Y**2))
    u0[[0, -1], :] = 0.0
    u0[:, [0, -1]] = 0.0
    _, first_order = leapfrog_step(u0, u0, dx, dy, dt, c)
    u_prev = u0 + 0.5 * (first_order - u0)
    return u_prev, u0


def leapfrog_step(u_prev, u, dx, dy, dt, c=C):
    """Return (u, u_new) after one leapfrog step with u = 0 on the boundary."""
    u_new = np.zeros_like(u)
    u_new[1:-1, 1:-1] = (
        2 * u[1:-1, 1:-1]
        - u_prev[1:-1, 1:-1]
        + (c * dt) ** 2
        * (
            (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) / dx**2  # axis 1 = x
            + (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]) / dy**2  # axis 0 = y
        )
    )
    return u, u_new


class WaveSimulation:
    """Wave state and time integration, independent of figure callbacks."""

    def __init__(self, length=L, nx=NX, ny=NY, c=C, cfl_safety=CFL_SAFETY):
        self.X, self.Y, self.dx, self.dy, self.dt = make_grid(
            length, nx, ny, c, cfl_safety
        )
        self.c = c
        self.u_prev, self.u = initial_condition(
            self.X, self.Y, self.dx, self.dy, self.dt, c
        )
        self.steps = 0

    @property
    def time(self):
        return self.steps * self.dt

    def advance(self, steps=1):
        """Advance exactly steps iterations without rendering intermediate fields."""
        if steps < 0:
            raise ValueError("steps must be nonnegative")
        for _ in range(steps):
            self.u_prev, self.u = leapfrog_step(
                self.u_prev, self.u, self.dx, self.dy, self.dt, self.c
            )
            self.steps += 1


def style_axes(ax):
    ax.set_zlim(-SCALE_FACTOR, SCALE_FACTOR)
    ax.set_title("2D Wave Equation Simulation Using Finite Differences", color="white")
    ax.set_xlabel("X", color="white")
    ax.set_ylabel("Y", color="white")
    ax.set_zlabel("U", color="white")
    for axis in ("x", "y", "z"):
        ax.tick_params(axis=axis, colors="white")


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=None,
        help="number of time steps (frames); default reaches t = 40",
    )
    args = parser.parse_args(argv)

    simulation = WaveSimulation()
    X, Y = simulation.X, simulation.Y
    n_steps = int(T_END / simulation.dt) if args.steps is None else args.steps

    # Fixed colour scale so the colour bar stays valid for every frame
    norm = Normalize(vmin=-SCALE_FACTOR, vmax=SCALE_FACTOR)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    surf = ax.plot_surface(X, Y, simulation.u, cmap="viridis", norm=norm)
    style_axes(ax)
    color_bar = fig.colorbar(
        surf, ax=ax, shrink=0.5, aspect=5, pad=0.1, location="left"
    )
    color_bar.set_label("Wave Amplitude", color="white")
    color_bar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(color_bar.ax.axes, "yticklabels"), color="white")
    artists = {"surf": surf}

    def redraw():
        artists["surf"].remove()
        artists["surf"] = ax.plot_surface(X, Y, simulation.u, cmap="viridis", norm=norm)
        style_axes(ax)
        return (artists["surf"],)

    def update(frame):
        simulation.advance()
        return redraw()

    if args.no_show:
        simulation.advance(n_steps)
        redraw()
    else:
        anim = FuncAnimation(
            fig, update, frames=n_steps, init_func=redraw, blit=False, repeat=False
        )
        plt.show()
        del anim

    print(
        f"dt = {simulation.dt:.4f}, steps = {simulation.steps}, t = {simulation.time:.2f}"
    )
    if args.output:
        save_figure(fig, args.output, "wave_2d.png", facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    main()
