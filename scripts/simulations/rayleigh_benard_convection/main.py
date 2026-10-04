"""Rayleigh-Benard convection in a 2D Boussinesq fluid heated from below.

A layer heated from below (T = 1 at the bottom wall, T = 0 at the top wall,
periodic side boundaries) is solved in vorticity-streamfunction form in
free-fall units. Small seeded temperature noise grows into convection rolls,
shown as an animated temperature map with the hot wall at the bottom.
"""

import sys
from pathlib import Path

import numpy as np
from scipy import fft

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Physical parameters (dimensionless)
RAYLEIGH = 1.0e5  # Ra = g beta dT H^3 / (nu kappa)
PRANDTL = 1.0  # Pr = nu / kappa
DIFFUSIVITY = 1.0 / np.sqrt(RAYLEIGH * PRANDTL)  # kappa in free-fall units
VISCOSITY = np.sqrt(PRANDTL / RAYLEIGH)  # nu in free-fall units
T_BOTTOM, T_TOP = 1.0, 0.0  # wall temperatures (hot bottom, cold top)
NOISE_AMPLITUDE = 1e-2  # initial temperature perturbation
SEED = 0

# Numerical parameters
GRID_SIZE = 128  # nodes in x (periodic) and in z (walls included)
MAX_TIME_STEP = 2e-3  # free-fall time units; diffusion limit is about 2.4e-3
CFL = 0.4  # advective Courant number used to shrink dt when the flow is fast
STEPS_PER_FRAME = 40  # time steps between drawn frames (t += 0.08 at the largest dt)
N_FRAMES = 500  # frames of a headless run or reel: t = 40, rolls form near t = 13


def initialize_fields(rng, n=GRID_SIZE):
    """Conductive temperature profile plus noise; fluid at rest.

    Arrays are indexed [j, i] with j = 0 at the bottom wall and i along x.
    """
    z = np.linspace(0.0, 1.0, n)
    temperature = np.tile(T_BOTTOM + (T_TOP - T_BOTTOM) * z[:, None], (1, n))
    temperature[1:-1] += NOISE_AMPLITUDE * rng.standard_normal((n - 2, n))
    vorticity = np.zeros_like(temperature)
    return temperature, vorticity


def poisson_eigenvalues(dx, dz, n=GRID_SIZE):
    """Eigenvalues of the 5-point Laplacian for periodic x and psi = 0 walls."""
    m = np.arange(n)
    k = np.arange(1, n - 1)
    lam_x = -((2 * np.sin(np.pi * m / n) / dx) ** 2)
    lam_z = -((2 * np.sin(np.pi * k / (2 * (n - 1))) / dz) ** 2)
    return lam_z[:, None] + lam_x[None, :]


def solve_streamfunction(vorticity, eigenvalues):
    """Solve lap(psi) = -omega exactly (FFT in x, DST-I in z)."""
    rhs = -vorticity[1:-1]
    rhs_hat = fft.fft(fft.dst(rhs, type=1, axis=0), axis=1)
    psi_interior = fft.idst(
        np.real(fft.ifft(rhs_hat / eigenvalues, axis=1)), type=1, axis=0
    )
    psi = np.zeros_like(vorticity)
    psi[1:-1] = psi_interior
    return psi


def velocities(psi, dx, dz):
    """u = d(psi)/dz, w = -d(psi)/dx with central differences."""
    u = np.zeros_like(psi)
    u[1:-1] = (psi[2:] - psi[:-2]) / (2 * dz)
    w = -(np.roll(psi, -1, axis=1) - np.roll(psi, 1, axis=1)) / (2 * dx)
    return u, w


def upwind_advection(f, u, w, dx, dz):
    """First-order upwind approximation of u df/dx + w df/dz (interior rows)."""
    fx_minus = (f - np.roll(f, 1, axis=1)) / dx
    fx_plus = (np.roll(f, -1, axis=1) - f) / dx
    adv = np.zeros_like(f)
    fz_minus = (f[1:-1] - f[:-2]) / dz
    fz_plus = (f[2:] - f[1:-1]) / dz
    ui, wi = u[1:-1], w[1:-1]
    adv[1:-1] = (
        np.maximum(ui, 0) * fx_minus[1:-1]
        + np.minimum(ui, 0) * fx_plus[1:-1]
        + np.maximum(wi, 0) * fz_minus
        + np.minimum(wi, 0) * fz_plus
    )
    return adv


def laplacian(f, dx, dz):
    """5-point Laplacian on interior rows, periodic in x."""
    lap = np.zeros_like(f)
    lap[1:-1] = (np.roll(f, -1, axis=1) - 2 * f + np.roll(f, 1, axis=1))[
        1:-1
    ] / dx**2 + (f[2:] - 2 * f[1:-1] + f[:-2]) / dz**2
    return lap


def time_step(temperature, vorticity, eigenvalues, dx, dz):
    """Advance T and omega by one forward-Euler step; return the dt used."""
    psi = solve_streamfunction(vorticity, eigenvalues)
    u, w = velocities(psi, dx, dz)
    speed = np.abs(u).max() / dx + np.abs(w).max() / dz
    dt = MAX_TIME_STEP if speed == 0 else min(MAX_TIME_STEP, CFL / speed)

    # Thom's formula: no-slip walls with psi = 0 give omega_wall = -2 psi_1 / dz^2.
    vorticity[0] = -2 * psi[1] / dz**2
    vorticity[-1] = -2 * psi[-2] / dz**2

    dT_dx = (np.roll(temperature, -1, axis=1) - np.roll(temperature, 1, axis=1)) / (
        2 * dx
    )
    temperature += dt * (
        -upwind_advection(temperature, u, w, dx, dz)
        + DIFFUSIVITY * laplacian(temperature, dx, dz)
    )
    vorticity += dt * (
        -upwind_advection(vorticity, u, w, dx, dz)
        + VISCOSITY * laplacian(vorticity, dx, dz)
        + dT_dx
    )
    temperature[0], temperature[-1] = T_BOTTOM, T_TOP
    return dt


def nusselt_number(temperature, dz):
    """Mean conductive heat flux through the bottom wall, relative to conduction."""
    dT_dz = (-3 * temperature[0] + 4 * temperature[1] - temperature[2]) / (2 * dz)
    return float(np.mean(-dT_dz) / (T_BOTTOM - T_TOP))


class RayleighBenardSimulation(Simulation):
    """Temperature and vorticity on the periodic layer; adaptive time steps."""

    def __init__(self, n=GRID_SIZE, seed=SEED):
        super().__init__()
        self.dx = 1.0 / n  # periodic: n nodes span one unit
        self.dz = 1.0 / (n - 1)  # walls at z = 0 and z = 1
        self.eigenvalues = poisson_eigenvalues(self.dx, self.dz, n)
        self.temperature, self.vorticity = initialize_fields(
            np.random.default_rng(seed), n
        )
        self.elapsed = 0.0  # free-fall times; dt varies from step to step

    @property
    def time(self):
        return self.elapsed

    def step(self):
        self.elapsed += time_step(
            self.temperature, self.vorticity, self.eigenvalues, self.dx, self.dz
        )

    def nusselt(self):
        return nusselt_number(self.temperature, self.dz)


class RayleighBenardView(View):
    """Temperature map from blue (cold top wall) to red (hot bottom wall)."""

    figsize = (7.0, 6.2)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        ax = figure.subplots()
        self.image = ax.imshow(
            simulation.temperature, origin="lower", extent=(0.0, 1.0, 0.0, 1.0),
            cmap="turbo", vmin=T_TOP, vmax=T_BOTTOM, interpolation="bilinear",
        )  # fmt: skip
        figure.colorbar(self.image, ax=ax, label="temperature T")
        ax.set(xlabel="x (periodic)", ylabel="height z")

    def draw(self):
        self.image.set_data(self.simulation.temperature)

    def status(self):
        simulation = self.simulation
        return f"t = {simulation.time:.1f}   Nu = {simulation.nusselt():.2f}"


ANIMATION = Animation(
    title="Rayleigh-Bénard Convection",
    subtitle="Fluid heated from below overturns in rolls",
    filename="rayleigh_benard_convection.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of dt <= {MAX_TIME_STEP:g}",
    endless=True,
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, RayleighBenardSimulation(), RayleighBenardView)
    print(
        f"Ra = {RAYLEIGH:g}, Pr = {PRANDTL:g}: t = {simulation.time:.1f} free-fall "
        f"times, Nusselt number = {simulation.nusselt():.2f}"
    )


if __name__ == "__main__":
    main()
