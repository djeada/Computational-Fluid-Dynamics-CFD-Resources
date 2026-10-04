"""1D heat equation (Crank-Nicolson) next to the 1D wave equation (leapfrog).

Both equations start from the same Gaussian pulse on 0 <= x <= L with
homogeneous Dirichlet boundaries. The heat equation is advanced with the
implicit Crank-Nicolson scheme (unconditionally stable), the wave equation with
the explicit second-order leapfrog scheme, whose Courant number c*dt/dx must
not exceed 1. Both share one time step, set by the wave CFL limit. Two stacked
panels show the pulse diffusing away and the pulse splitting into two waves
that reflect from the fixed ends.
"""

import math
import sys
from pathlib import Path

import numpy as np
from scipy.sparse import diags, identity
from scipy.sparse.linalg import splu

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

L = 10.0  # domain length (nondimensional)
C = 1.0  # wave speed
D = 1.0  # diffusivity of the heat equation
PULSE_WIDTH = 5.0  # initial condition exp(-PULSE_WIDTH * (x - L/2)^2)
T = 2 * L / C  # total simulated time: one wave period, the pulse is back at x = L/2
NX = 500  # number of grid points
COURANT = 0.9  # c*dt/dx for the leapfrog scheme (must be <= 1)
STEPS_PER_FRAME = 1  # time steps per animation frame
# Steps that reach t = T, as counted by make_grid (1109 for the defaults)
N_FRAMES = math.ceil(T / (COURANT * (L / (NX - 1)) / C))


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


class HeatWaveSimulation(Simulation):
    """Heat and wave fields on one grid, with the Crank-Nicolson LU cached."""

    def __init__(
        self, length=L, nx=NX, c=C, diffusivity=D, courant=COURANT, total_time=T
    ):
        super().__init__()
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
        self.initial_pulse = self.wave.copy()  # both equations start from it

    def step(self):
        heat_step(self.heat, self.lu, self.b)
        wave_step(self.wave_prev, self.wave, self.courant2)


class HeatWaveView(View):
    """Heat solution above the wave solution, with the initial pulse dashed."""

    figsize = (10.0, 7.0)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        x = simulation.x
        heat_ax, wave_ax = figure.subplots(2, 1, sharex=True)
        dashed = dict(color="0.5", lw=1.5, ls="--", label="initial pulse")
        for ax in (heat_ax, wave_ax):
            ax.plot(x, simulation.initial_pulse, **dashed)
            ax.set(xlim=(x[0], x[-1]), ylabel="u")
        (self.heat_line,) = heat_ax.plot(x, simulation.heat, color="cyan")
        (self.wave_line,) = wave_ax.plot(x, simulation.wave, color="magenta")
        heat_ax.set(ylim=(-0.1, 1.1), title="Heat equation (Crank-Nicolson)")
        wave_ax.set(ylim=(-1.1, 1.1), title="Wave equation (leapfrog)", xlabel="x")
        heat_ax.legend(loc="upper right")

    def draw(self):
        self.heat_line.set_ydata(self.simulation.heat)
        self.wave_line.set_ydata(self.simulation.wave)

    def status(self):
        return f"t = {self.simulation.time:.2f}"


ANIMATION = Animation(
    title="Heat vs Wave Equation",
    subtitle="One pulse diffuses, the other travels",
    filename="heat_and_wave_1d.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label="time steps",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, HeatWaveSimulation(), HeatWaveView)
    print(
        f"t = {simulation.time:.2f} after {simulation.steps} steps of "
        f"dt = {simulation.dt:.4f} (Courant {np.sqrt(simulation.courant2):.3f}, "
        f"r = D dt/dx^2 = {simulation.r:.1f}): heat peak "
        f"{simulation.heat.max():.3f}, wave peak {simulation.wave.max():.3f}"
    )


if __name__ == "__main__":
    main()
