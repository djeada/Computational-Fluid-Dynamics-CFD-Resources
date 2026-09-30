"""Free-particle 2D time-dependent Schrödinger equation.

A normalised Gaussian wavepacket is evolved with the Strang split-step
Fourier method (hbar = m = 1) on a periodic grid, and the probability density
|psi|^2 is animated as a 3D surface.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int, save_figure  # noqa: E402

# Parameters (dimensionless units with hbar = m = 1)
DOMAIN_LENGTH = 10.0  # side length L of the periodic square domain
N_POINTS = 100  # grid points per side
TIME_STEP = 0.01  # dt
FINAL_TIME = 1.0  # total simulated time for the default run
SPEED_FACTOR = 5  # time steps per animation frame
N_FRAMES = int(round(FINAL_TIME / TIME_STEP)) // SPEED_FACTOR


def make_grid(length=DOMAIN_LENGTH, n=N_POINTS):
    """Return the grid spacing and periodic coordinate arrays X, Y."""
    if length <= 0 or n < 2:
        raise ValueError("require positive length and at least two grid points")
    dx = length / n
    x = -length / 2 + dx * np.arange(n)  # periodic grid: no duplicated end point
    X, Y = np.meshgrid(x, x)
    return dx, X, Y


def potential(X, Y):
    """Potential energy V(x, y); zero everywhere for a free particle."""
    return np.zeros_like(X)


def initial_wavefunction(X, Y, dx):
    """Gaussian wavepacket exp(-(x^2 + y^2)/2), normalised so sum |psi|^2 dA = 1."""
    psi = np.exp(-(X**2 + Y**2) / 2).astype(complex)
    return psi / np.sqrt(probability_norm(psi, dx))


def squared_wavenumbers(n, dx):
    """Return k^2 = kx^2 + ky^2 on the FFT grid."""
    k = 2 * np.pi * np.fft.fftfreq(n, d=dx)
    KX, KY = np.meshgrid(k, k)
    return KX**2 + KY**2


def evolve(psi, dt, k2, V):
    """Advance psi by one Strang step: half kinetic, full potential, half kinetic."""
    half_kinetic = np.exp(-1j * k2 * dt / 4)  # exp(-i (k^2/2) (dt/2))
    psi = np.fft.ifft2(np.fft.fft2(psi) * half_kinetic)
    psi = psi * np.exp(-1j * V * dt)
    return np.fft.ifft2(np.fft.fft2(psi) * half_kinetic)


def probability_norm(psi, dx):
    """Total probability: sum of |psi|^2 times the cell area."""
    return float(np.sum(np.abs(psi) ** 2) * dx**2)


class SchrodingerSimulation:
    """Wavefunction state with FFT propagators cached for the chosen time step."""

    def __init__(self, length=DOMAIN_LENGTH, n=N_POINTS, dt=TIME_STEP):
        if dt <= 0:
            raise ValueError("time step must be positive")
        self.dx, self.X, self.Y = make_grid(length, n)
        self.dt = dt
        self.psi = initial_wavefunction(self.X, self.Y, self.dx)
        self.half_kinetic = np.exp(-1j * squared_wavenumbers(n, self.dx) * dt / 4)
        self.potential_phase = np.exp(-1j * potential(self.X, self.Y) * dt)
        self.steps = 0

    @property
    def time(self):
        return self.steps * self.dt

    @property
    def density(self):
        return np.abs(self.psi) ** 2

    @property
    def norm(self):
        return probability_norm(self.psi, self.dx)

    def advance(self, steps=1):
        """Advance Strang steps without rendering or rebuilding propagators."""
        if steps < 0:
            raise ValueError("steps must be nonnegative")
        for _ in range(steps):
            self.psi = np.fft.ifft2(np.fft.fft2(self.psi) * self.half_kinetic)
            self.psi *= self.potential_phase
            self.psi = np.fft.ifft2(np.fft.fft2(self.psi) * self.half_kinetic)
            self.steps += 1


def style_axes(ax, z_max, time):
    ax.set_facecolor("black")
    ax.set_xlim(-DOMAIN_LENGTH / 2, DOMAIN_LENGTH / 2)
    ax.set_ylim(-DOMAIN_LENGTH / 2, DOMAIN_LENGTH / 2)
    ax.set_zlim(0, z_max)
    ax.set_xlabel("x", color="white")
    ax.set_ylabel("y", color="white")
    ax.set_zlabel(r"$|\psi|^2$", color="white")
    ax.set_title(
        f"Time Evolution of Schrödinger Equation in 2D (t = {time:.2f})", color="white"
    )
    for axis in ("x", "y", "z"):
        ax.tick_params(axis=axis, colors="white")


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=N_FRAMES,
        help=f"animation frames, each {SPEED_FACTOR} time steps (default: {N_FRAMES})",
    )
    args = parser.parse_args(argv)

    simulation = SchrodingerSimulation()
    X, Y = simulation.X, simulation.Y
    initial_norm = simulation.norm
    density = simulation.density
    z_max = density.max()  # fixed colour and z range: the peak only decreases

    fig = plt.figure(facecolor="black")
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, density, cmap="viridis", vmin=0, vmax=z_max)
    style_axes(ax, z_max, simulation.time)

    cax = fig.add_axes([0.05, 0.15, 0.02, 0.7])  # [left, bottom, width, height]
    mappable = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(0, z_max))
    cbar = fig.colorbar(mappable, cax=cax)
    cbar.ax.tick_params(color="white", labelcolor="white")
    cbar.outline.set_edgecolor("white")

    def redraw():
        ax.clear()
        ax.plot_surface(X, Y, simulation.density, cmap="viridis", vmin=0, vmax=z_max)
        style_axes(ax, z_max, simulation.time)
        return ()

    def update(frame):
        simulation.advance(SPEED_FACTOR)
        return redraw()

    if args.no_show:
        simulation.advance(args.steps * SPEED_FACTOR)
        redraw()
    else:
        animation = FuncAnimation(  # noqa: F841 (keep a reference while showing)
            fig, update, frames=args.steps, init_func=lambda: (), repeat=False
        )
        plt.show()

    final_norm = simulation.norm
    print(
        f"t = {simulation.time:.2f}: total probability {final_norm:.15f} "
        f"(change {final_norm - initial_norm:+.2e})"
    )

    if args.output:
        save_figure(
            fig, args.output, "schroedinger_equation.png", facecolor=fig.get_facecolor()
        )
    plt.close(fig)


if __name__ == "__main__":
    main()
