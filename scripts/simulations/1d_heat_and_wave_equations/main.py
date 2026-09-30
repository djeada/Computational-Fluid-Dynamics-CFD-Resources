"""Animate the 1D heat equation (Crank-Nicolson) and 1D wave equation (leapfrog).

Both equations start from the same Gaussian pulse on 0 <= x <= L with
homogeneous Dirichlet boundaries. The heat equation is advanced with the
implicit Crank-Nicolson scheme (unconditionally stable), the wave equation with
the explicit second-order leapfrog scheme, whose Courant number c*dt/dx must
not exceed 1. Both share one time step, set by the wave CFL limit.
"""

import sys
from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags, identity
from scipy.sparse.linalg import splu

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int, save_figure  # noqa: E402

L = 10.0  # domain length (nondimensional)
T = 500.0  # total simulated time
NX = 500  # number of grid points
C = 1.0  # wave speed
D = 1.0  # diffusivity of the heat equation
COURANT = 0.9  # c*dt/dx for the leapfrog scheme (must be <= 1)
PULSE_WIDTH = 5.0  # initial condition exp(-PULSE_WIDTH * (x - L/2)^2)


def make_grid(length=L, nx=NX, c=C, courant=COURANT, total_time=T):
    """Return x, dx, dt and the number of steps needed to reach total_time."""
    if nx < 3 or min(length, c, total_time) <= 0 or not 0 < courant <= 1:
        raise ValueError(
            "require nx >= 3, positive length/speed/time, and 0 < Courant <= 1"
        )
    x = np.linspace(0.0, length, nx)
    dx = x[1] - x[0]
    nt = int(np.ceil(total_time / (courant * dx / c)))
    dt = total_time / nt  # fits exactly into total_time, Courant <= courant
    return x, dx, dt, nt


def crank_nicolson_operators(nx, r):
    """Return (LU of A, B) for (I - r/2 L) u^{n+1} = (I + r/2 L) u^n.

    L is the second-difference matrix; the first and last rows are identity
    rows so that u = 0 is kept on both boundaries. r = D*dt/dx^2.
    """
    lap = diags([1.0, -2.0, 1.0], [-1, 0, 1], shape=(nx, nx)).tolil()
    lap[0, :] = 0.0
    lap[-1, :] = 0.0
    lap = lap.tocsc()
    eye = identity(nx, format="csc")
    a = (eye - 0.5 * r * lap).tocsc()
    b = (eye + 0.5 * r * lap).tocsc()
    return splu(a), b


def heat_step(u, lu, b):
    """Advance the heat solution one Crank-Nicolson step (in place)."""
    u[:] = lu.solve(b @ u)
    u[0] = u[-1] = 0.0


def wave_step(u_prev, u, courant2):
    """Advance the wave solution one leapfrog step (in place)."""
    u_new = np.empty_like(u)
    u_new[1:-1] = (
        2.0 * u[1:-1] - u_prev[1:-1] + courant2 * (u[2:] - 2.0 * u[1:-1] + u[:-2])
    )
    u_new[0] = u_new[-1] = 0.0
    u_prev[:] = u
    u[:] = u_new


def initial_state(x, dx, dt, c=C, pulse_width=PULSE_WIDTH):
    """Return (heat, wave_prev, wave) for a Gaussian pulse at rest."""
    u0 = np.exp(-pulse_width * (x - (x[0] + x[-1]) / 2) ** 2)
    u0[0] = u0[-1] = 0.0
    courant2 = (c * dt / dx) ** 2
    # Zero initial velocity: u^{-1} = u^0 + (C^2/2) * delta^2 u^0 (second order)
    u_prev = u0.copy()
    u_prev[1:-1] += 0.5 * courant2 * (u0[2:] - 2.0 * u0[1:-1] + u0[:-2])
    return u0.copy(), u_prev, u0.copy()


class HeatWaveSimulation:
    """Coupled heat/wave state with cached Crank-Nicolson factorization."""

    def __init__(
        self, length=L, nx=NX, c=C, diffusivity=D, courant=COURANT, total_time=T
    ):
        if diffusivity < 0:
            raise ValueError("diffusivity must be nonnegative")
        self.x, self.dx, self.dt, self.default_steps = make_grid(
            length, nx, c, courant, total_time
        )
        self.r = diffusivity * self.dt / self.dx**2
        self.courant2 = (c * self.dt / self.dx) ** 2
        self.lu, self.b = crank_nicolson_operators(nx, self.r)
        self.heat, self.wave_prev, self.wave = initial_state(
            self.x, self.dx, self.dt, c
        )
        self.steps = 0

    @property
    def time(self):
        return self.steps * self.dt

    def advance(self, steps=1):
        """Advance both equations exactly steps iterations, without plotting."""
        if steps < 0:
            raise ValueError("steps must be nonnegative")
        for _ in range(steps):
            heat_step(self.heat, self.lu, self.b)
            wave_step(self.wave_prev, self.wave, self.courant2)
            self.steps += 1


def setup_figure(x):
    """Create the two-panel dark figure; return (fig, artists)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), facecolor="black")
    for ax in (ax1, ax2):
        ax.set_facecolor("black")
        ax.set_xlim(x[0], x[-1])
        ax.grid(False)
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")
        ax.set_ylabel("Amplitude", fontsize=14, color="white")
    (line_heat,) = ax1.plot(x, np.zeros_like(x), color="cyan", lw=2)
    (line_wave,) = ax2.plot(x, np.zeros_like(x), color="magenta", lw=2)
    ax1.set_title("Heat Equation (Crank-Nicolson)", fontsize=16, color="white")
    ax2.set_title("Wave Equation (Leapfrog)", fontsize=16, color="white")
    ax2.set_xlabel("Spatial Coordinate $x$", fontsize=14, color="white")
    ax1.set_ylim(-0.1, 1.1)
    ax2.set_ylim(-1.1, 1.1)
    text_kw = dict(fontsize=14, color="white", bbox=dict(facecolor="black", alpha=0.5))
    time_text1 = ax1.text(0.75, 0.85, "", transform=ax1.transAxes, **text_kw)
    time_text2 = ax2.text(0.75, 0.85, "", transform=ax2.transAxes, **text_kw)
    fig.tight_layout()
    return fig, (line_heat, line_wave, time_text1, time_text2)


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=None,
        help="number of time steps (animation frames); default reaches t = T",
    )
    args = parser.parse_args(argv)

    simulation = HeatWaveSimulation()
    n_steps = simulation.default_steps if args.steps is None else args.steps
    print(
        f"dx = {simulation.dx:.4f}, dt = {simulation.dt:.4f}, "
        f"Courant = {np.sqrt(simulation.courant2):.3f}, "
        f"r = D dt/dx^2 = {simulation.r:.2f} (Crank-Nicolson: stable for any r)"
    )

    fig, (line_heat, line_wave, text1, text2) = setup_figure(simulation.x)

    def draw():
        line_heat.set_ydata(simulation.heat)
        line_wave.set_ydata(simulation.wave)
        label = f"Time = {simulation.time:.4f} s"
        text1.set_text(label)
        text2.set_text(label)
        return [line_heat, line_wave, text1, text2]

    def animate(i):
        simulation.advance()
        return draw()

    draw()
    if args.no_show:
        simulation.advance(n_steps)
        draw()
    else:
        ani = animation.FuncAnimation(
            fig,
            animate,
            frames=n_steps,
            init_func=draw,
            interval=20,
            blit=True,
            repeat=False,
        )
        plt.show()  # after the window closes, the figure holds the last frame
        del ani

    if args.output:
        save_figure(
            fig, args.output, "heat_and_wave_1d.png", facecolor=fig.get_facecolor()
        )
    plt.close(fig)


if __name__ == "__main__":
    main()
