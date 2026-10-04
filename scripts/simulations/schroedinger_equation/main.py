"""Free-particle 2D time-dependent Schrödinger equation, split-step Fourier.

A normalised Gaussian wavepacket at rest is evolved with the Strang split-step
Fourier method (hbar = m = 1) on a periodic grid. The probability density
|psi|^2 is shown as a 3D surface on fixed height and colour scales, so the
packet visibly spreads and its peak falls while the total probability stays 1.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Parameters (dimensionless units with hbar = m = 1)
DOMAIN_LENGTH = 10.0  # side length L of the periodic square domain
N_POINTS = 100  # grid points per side
TIME_STEP = 0.001  # dt; for V = 0 the result does not depend on it
FINAL_TIME = 1.0  # total simulated time for the default run
STEPS_PER_FRAME = 10  # time steps per animation frame
SPEED_FACTOR = STEPS_PER_FRAME  # former name of STEPS_PER_FRAME
N_FRAMES = int(round(FINAL_TIME / TIME_STEP)) // STEPS_PER_FRAME  # 100 frames
COLORMAP = "viridis"


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


class SchrodingerSimulation(Simulation):
    """Wavefunction state with FFT propagators cached for the chosen time step."""

    def __init__(self, length=DOMAIN_LENGTH, n=N_POINTS, dt=TIME_STEP):
        super().__init__()
        if dt <= 0:
            raise ValueError("time step must be positive")
        self.dx, self.X, self.Y = make_grid(length, n)
        self.length = length
        self.dt = dt
        self.psi = initial_wavefunction(self.X, self.Y, self.dx)
        self.half_kinetic = np.exp(-1j * squared_wavenumbers(n, self.dx) * dt / 4)
        self.potential_phase = np.exp(-1j * potential(self.X, self.Y) * dt)
        self.initial_norm = self.norm
        self.initial_peak = float(self.density.max())  # fixes the plot scales

    @property
    def density(self):
        return np.abs(self.psi) ** 2

    @property
    def norm(self):
        return probability_norm(self.psi, self.dx)

    def step(self):
        """One Strang step with the cached propagators (same as ``evolve``)."""
        self.psi = np.fft.ifft2(np.fft.fft2(self.psi) * self.half_kinetic)
        self.psi *= self.potential_phase
        self.psi = np.fft.ifft2(np.fft.fft2(self.psi) * self.half_kinetic)


class SchrodingerView(View):
    """Surface of |psi|^2 scaled to the initial peak, re-plotted every frame.

    Fixed height and colour scales show the peak falling as the packet
    spreads. In a reel the colour bar sits below the surface.
    """

    figsize = (8.0, 6.5)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        self.ax = figure.add_subplot(projection="3d")
        peak = simulation.initial_peak
        self.norm = Normalize(0.0, peak)
        figure.colorbar(
            ScalarMappable(self.norm, COLORMAP), ax=self.ax, shrink=0.6,
            label=r"probability density $|\psi|^2$",
            location="bottom" if portrait else "right",
        )  # fmt: skip
        half = simulation.length / 2
        self.ax.set(
            xlim=(-half, half), ylim=(-half, half), zlim=(0.0, peak),
            xlabel="x", ylabel="y", zlabel=r"$|\psi|^2$",
        )  # fmt: skip
        # Zoom into the margin the 3D axes leaves around the box. The reel panel
        # is nearly square, so a taller box fills it.
        self.ax.set_box_aspect((4, 4, 4) if portrait else None, zoom=1.1)
        if portrait:  # keep the large axis labels clear of the tick labels
            for axis in (self.ax.xaxis, self.ax.yaxis, self.ax.zaxis):
                axis.labelpad = 18
        self.surface = None

    def draw(self):
        if self.surface is not None:
            self.surface.remove()
        simulation = self.simulation
        self.surface = self.ax.plot_surface(
            simulation.X, simulation.Y, simulation.density, cmap=COLORMAP,
            norm=self.norm,
        )  # fmt: skip

    def status(self):
        peak = self.simulation.density.max()
        return f"t = {self.simulation.time:.2f}   peak |ψ|² = {peak:.3f}"


ANIMATION = Animation(
    title="2D Schrödinger Equation",
    subtitle="A free quantum wavepacket spreads out",
    filename="schroedinger_equation.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"split-step time steps of dt = {TIME_STEP:g}",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, SchrodingerSimulation(), SchrodingerView)
    norm = simulation.norm
    print(
        f"t = {simulation.time:.2f}: total probability {norm:.15f} "
        f"(change {norm - simulation.initial_norm:+.2e})"
    )


if __name__ == "__main__":
    main()
