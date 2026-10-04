"""Rayleigh-Taylor instability: heavy fluid sinking into light fluid below it.

A tall periodic box (1 m wide, 2 m high) holds heavy fluid above light fluid,
separated by a thin tanh interface with a single-mode ripple and a little
seeded noise. The 2D Boussinesq equations are solved in vorticity-streamfunction
form: the density is advected in flux form with fifth-order WENO
reconstruction, an exact FFT/sine-transform Poisson solve gives the
streamfunction, and SSP Runge-Kutta steps advance both fields. The ripple grows,
a rising bubble and a falling spike form, and their edges roll up into
mushroom caps through secondary Kelvin-Helmholtz instabilities before the
fluids mix. Density and vorticity are animated side by side.
"""

import sys
from pathlib import Path

import numpy as np
from numba import njit, prange
from scipy import fft

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Physical parameters (SI units)
WIDTH = 1.0  # L, periodic box width [m]
HEIGHT = 2.0  # H, distance between the free-slip walls [m]
GRAVITY = 9.81  # g [m/s^2]
ATWOOD = 0.1  # A = (rho_heavy - rho_light) / (rho_heavy + rho_light)
VISCOSITY = 2e-4  # nu, kinematic viscosity [m^2/s]
DIFFUSIVITY = 2e-5  # kappa, mass diffusivity of the density field [m^2/s]
INTERFACE_THICKNESS = 0.015  # delta in rho = rho0 (1 + A tanh(z / delta)) [m]
PERTURBATION_AMPLITUDE = 0.01  # a, interface displacement of the seeded mode [m]
PERTURBATION_MODE = 1  # wavelengths across the box: lambda = L / mode
NOISE_AMPLITUDE = 1e-5  # rms interface displacement of the seeded noise [m]
NOISE_MODES = (2, 32)  # wavelengths across the box carrying the noise
SEED = 0

# Numerical parameters
NX, NZ = 256, 512  # cells across and up; dx = dz = 3.9 mm
CFL = 0.6  # (|u|/dx + |w|/dz) dt, with SSP-RK3 and WENO5
MAX_TIME_STEP = 5e-3  # dt while the flow is slow [s]
STEPS_PER_FRAME = 4  # time steps between drawn frames
N_FRAMES = 835  # frames of a run (t = 4.4 s); a 30 s reel shows each one
WENO_EPSILON = 1e-12  # keeps the WENO weights finite in uniform regions
VORTICITY_SCALE = 30.0  # colour limits +-omega [1/s]


def initial_fields(nx=NX, nz=NZ, rng=None, atwood=ATWOOD,
                   amplitude=PERTURBATION_AMPLITUDE, mode=PERTURBATION_MODE,
                   noise=NOISE_AMPLITUDE):  # fmt: skip
    """Density rho/rho0 in cells and vorticity on nodes of a fluid at rest.

    The interface sits at mid-height, displaced by a cos(2 pi mode x / L) so
    that heavy fluid dips at x = L/2, plus random modes of rms height
    ``noise``. A negative ``atwood`` puts the light fluid on top (stable).
    """
    rng = np.random.default_rng(SEED) if rng is None else rng
    dx, dz = WIDTH / nx, HEIGHT / nz
    x = (np.arange(nx) + 0.5) * dx
    z = (np.arange(nz) + 0.5) * dz
    height = amplitude * np.cos(2 * np.pi * mode * x / WIDTH)
    modes = np.arange(NOISE_MODES[0], NOISE_MODES[1] + 1)
    if noise > 0:
        coefficients = (
            rng.standard_normal((2, modes.size)) * noise / np.sqrt(modes.size / 2)
        )
        phase = 2 * np.pi * modes[:, None] * x[None, :] / WIDTH
        height += coefficients[0] @ np.cos(phase) + coefficients[1] @ np.sin(phase)
    interface = 0.5 * HEIGHT + height
    density = 1.0 + atwood * np.tanh(
        (z[:, None] - interface[None, :]) / INTERFACE_THICKNESS
    )
    vorticity = np.zeros((nz + 1, nx))
    return density, vorticity


def poisson_eigenvalues(nx, nz, dx, dz):
    """Eigenvalues of the 5-point Laplacian on nodes: periodic x, psi = 0 walls.

    Rows are the sine modes 1..nz-1 in z, columns the rfft wavenumbers in x.
    """
    m = np.arange(nx // 2 + 1)
    k = np.arange(1, nz)
    lam_x = -((2 * np.sin(np.pi * m / nx) / dx) ** 2)
    lam_z = -((2 * np.sin(np.pi * k / (2 * nz)) / dz) ** 2)
    return lam_z[:, None] + lam_x[None, :]


def solve_streamfunction(vorticity, eigenvalues):
    """Solve lap(psi) = -omega exactly on the nodes (rfft in x, DST-I in z)."""
    nx = vorticity.shape[1]
    rhs = -vorticity[1:-1]
    rhs_hat = fft.rfft(fft.dst(rhs, type=1, axis=0, workers=-1), axis=1, workers=-1)
    psi = np.zeros_like(vorticity)
    psi[1:-1] = fft.idst(
        fft.irfft(rhs_hat / eigenvalues, n=nx, axis=1, workers=-1),
        type=1, axis=0, workers=-1,
    )  # fmt: skip
    return psi


def vertical_velocity(psi, dx):
    """w = -d(psi)/dx on the horizontal cell faces (zero on both walls) [m/s]."""
    return -(np.roll(psi, -1, axis=1) - psi) / dx


@njit(cache=False)
def weno5(a, b, c, d, e):
    """Fifth-order WENO value at the face between c and d, upwind side a, b, c.

    Jiang & Shu (1996): three third-order candidates weighted by their
    smoothness, so smooth regions get the fifth-order upwind value and
    steep fronts the candidate that does not cross them.
    """
    q0 = (2.0 * a - 7.0 * b + 11.0 * c) / 6.0
    q1 = (-b + 5.0 * c + 2.0 * d) / 6.0
    q2 = (2.0 * c + 5.0 * d - e) / 6.0
    s0 = 13.0 / 12.0 * (a - 2.0 * b + c) ** 2 + 0.25 * (a - 4.0 * b + 3.0 * c) ** 2
    s1 = 13.0 / 12.0 * (b - 2.0 * c + d) ** 2 + 0.25 * (b - d) ** 2
    s2 = 13.0 / 12.0 * (c - 2.0 * d + e) ** 2 + 0.25 * (3.0 * c - 4.0 * d + e) ** 2
    w0 = 0.1 / (WENO_EPSILON + s0) ** 2
    w1 = 0.6 / (WENO_EPSILON + s1) ** 2
    w2 = 0.3 / (WENO_EPSILON + s2) ** 2
    return (w0 * q0 + w1 * q1 + w2 * q2) / (w0 + w1 + w2)


@njit(cache=False, parallel=True)
def advection_tendency(padded, u, w, dx, dz):
    """-div(q u) in flux form for q with three ghost cells on every side.

    ``padded[j + 3, i + 3]`` is q[j, i]; ``u[j, i]`` is the velocity on the face
    left of q[j, i] (periodic in x) and ``w[j, i]`` the one below it, with one
    more row of faces above the last row.
    """
    m, n = u.shape
    flux_x = np.empty((m, n + 1))
    flux_z = np.empty((m + 1, n))
    for j in prange(m):
        r = j + 3
        for i in range(n + 1):
            c = i + 3
            velocity = u[j, i % n]
            if velocity >= 0.0:
                face = weno5(padded[r, c - 3], padded[r, c - 2], padded[r, c - 1],
                             padded[r, c], padded[r, c + 1])  # fmt: skip
            else:
                face = weno5(padded[r, c + 2], padded[r, c + 1], padded[r, c],
                             padded[r, c - 1], padded[r, c - 2])  # fmt: skip
            flux_x[j, i] = velocity * face
    for j in prange(m + 1):
        r = j + 3
        for i in range(n):
            c = i + 3
            velocity = w[j, i]
            if velocity >= 0.0:
                face = weno5(padded[r - 3, c], padded[r - 2, c], padded[r - 1, c],
                             padded[r, c], padded[r + 1, c])  # fmt: skip
            else:
                face = weno5(padded[r + 2, c], padded[r + 1, c], padded[r, c],
                             padded[r - 1, c], padded[r - 2, c])  # fmt: skip
            flux_z[j, i] = velocity * face
    tendency = np.empty((m, n))
    for j in prange(m):
        for i in range(n):
            tendency[j, i] = (
                -(flux_x[j, i + 1] - flux_x[j, i]) / dx
                - (flux_z[j + 1, i] - flux_z[j, i]) / dz
            )
    return tendency


@njit(cache=False, parallel=True)
def tendencies(density, vorticity, psi, dx, dz, gravity, viscosity, diffusivity):
    """Time derivatives of the cell densities and of the interior vorticity.

    d(rho)/dt = -div(rho u) + kappa lap(rho), with no flux through the walls;
    d(omega)/dt = -div(omega u) - g d(rho/rho0)/dx + nu lap(omega), with
    omega = 0 on the free-slip walls. Each velocity is a difference of one
    streamfunction across a face, so its discrete divergence is exactly zero:
    psi itself for the cells, and psi averaged to the cell centres for the
    cells around the nodes.
    """
    nz, nx = density.shape
    # Ghost cells: density mirrored at the walls, vorticity odd about them.
    rho = np.empty((nz + 6, nx + 6))
    omega = np.empty((nz + 5, nx + 6))  # row r holds node r - 2
    for r in prange(nz + 6):
        j = r - 3
        if j < 0:
            j = -1 - j
        elif j >= nz:
            j = 2 * nz - 1 - j
        for c in range(nx + 6):
            rho[r, c] = density[j, (c - 3) % nx]
    for r in prange(nz + 5):
        j, sign = r - 2, 1.0
        if j < 0:
            j, sign = -j, -1.0
        elif j > nz:
            j, sign = 2 * nz - j, -1.0
        for c in range(nx + 6):
            omega[r, c] = sign * vorticity[j, (c - 3) % nx]
    # Face velocities of the cells (u left, w below) and of the node cells.
    u = np.empty((nz, nx))
    w = np.empty((nz + 1, nx))
    centre = np.empty((nz, nx))  # psi at the cell centres
    for j in prange(nz + 1):
        for i in range(nx):
            right = (i + 1) % nx
            w[j, i] = -(psi[j, right] - psi[j, i]) / dx
            if j < nz:
                u[j, i] = (psi[j + 1, i] - psi[j, i]) / dz
                corners = psi[j, i] + psi[j, right] + psi[j + 1, i] + psi[j + 1, right]
                centre[j, i] = 0.25 * corners
    u_node = np.empty((nz - 1, nx))
    w_node = np.empty((nz, nx))
    for j in prange(nz):
        for i in range(nx):
            w_node[j, i] = -(centre[j, i] - centre[j, i - 1]) / dx
            if j < nz - 1:
                u_node[j, i] = (centre[j + 1, i - 1] - centre[j, i - 1]) / dz
    d_density = advection_tendency(rho, u, w, dx, dz)
    d_vorticity = advection_tendency(omega, u_node, w_node, dx, dz)
    for j in prange(nz):
        for i in range(nx):
            r, c = j + 3, i + 3
            d_density[j, i] += diffusivity * (
                (rho[r, c - 1] - 2.0 * rho[r, c] + rho[r, c + 1]) / dx**2
                + (rho[r - 1, c] - 2.0 * rho[r, c] + rho[r + 1, c]) / dz**2
            )
            if j < nz - 1:  # interior node j + 1, between cell rows j and j + 1
                # Differences row by row: exactly zero for a stratified fluid.
                drho_dx = (
                    rho[r, c] - rho[r, c - 1] + (rho[r + 1, c] - rho[r + 1, c - 1])
                ) / (2.0 * dx)
                lap = (
                    omega[r, c - 1] - 2.0 * omega[r, c] + omega[r, c + 1]
                ) / dx**2 + (
                    omega[r - 1, c] - 2.0 * omega[r, c] + omega[r + 1, c]
                ) / dz**2
                d_vorticity[j, i] += -gravity * drho_dx + viscosity * lap
    return d_density, d_vorticity


class RayleighTaylorSimulation(Simulation):
    """Density and vorticity of the Boussinesq fluid; adaptive time steps.

    ``density`` is rho/rho0 at the cell centres, ``vorticity`` and ``psi`` live
    on the nodes (cell corners), with the wall rows 0 and ``nz``.
    """

    def __init__(self, nx=NX, nz=NZ, seed=SEED, atwood=ATWOOD, gravity=GRAVITY,
                 viscosity=VISCOSITY, diffusivity=DIFFUSIVITY,
                 amplitude=PERTURBATION_AMPLITUDE, mode=PERTURBATION_MODE,
                 noise=NOISE_AMPLITUDE, max_time_step=MAX_TIME_STEP):  # fmt: skip
        super().__init__()
        if nx < 4 or nz < 4:
            raise ValueError("at least four cells per direction are required")
        self.dx, self.dz = WIDTH / nx, HEIGHT / nz
        self.atwood, self.gravity = atwood, gravity
        self.viscosity, self.diffusivity = viscosity, diffusivity
        self.max_time_step = max_time_step
        self.eigenvalues = poisson_eigenvalues(nx, nz, self.dx, self.dz)
        self.density, self.vorticity = initial_fields(
            nx, nz, np.random.default_rng(seed), atwood, amplitude, mode, noise
        )
        self.psi = solve_streamfunction(self.vorticity, self.eigenvalues)
        self.elapsed = 0.0  # [s]; dt changes from step to step

    @property
    def time(self):
        return self.elapsed

    def time_step(self):
        """dt [s] from the CFL limit of the current velocity, at most max_time_step."""
        u = np.diff(self.psi, axis=0) / self.dz
        w = vertical_velocity(self.psi, self.dx)
        rate = np.abs(u).max() / self.dx + np.abs(w).max() / self.dz
        return min(self.max_time_step, CFL / rate) if rate > 0 else self.max_time_step

    def rates(self, density, vorticity, psi):
        return tendencies(
            density, vorticity, psi, self.dx, self.dz, self.gravity,
            self.viscosity, self.diffusivity,
        )  # fmt: skip

    def step(self):
        """One three-stage SSP Runge-Kutta step (Shu & Osher, 1988)."""
        dt = self.time_step()
        rho0, omega0 = self.density, self.vorticity
        rho, omega, psi = rho0, omega0, self.psi
        for weight in (1.0, 0.25, 2.0 / 3.0):
            d_rho, d_omega = self.rates(rho, omega, psi)
            rho_stage = rho + dt * d_rho
            omega_stage = omega.copy()
            omega_stage[1:-1] += dt * d_omega
            rho = (1 - weight) * rho0 + weight * rho_stage
            omega = (1 - weight) * omega0 + weight * omega_stage
            psi = solve_streamfunction(omega, self.eigenvalues)
        self.density, self.vorticity, self.psi = rho, omega, psi
        self.elapsed += dt

    def heavy_fraction(self):
        """Horizontal mean of the heavy-fluid fraction (rho - rho_light) / (2 A)."""
        return (self.density.mean(axis=1) - 1 + abs(self.atwood)) / (
            2 * abs(self.atwood)
        )

    def mixing_width(self, threshold=0.01):
        """Height [m] of the layer where the mean heavy fraction is mixed.

        Mixed means between ``threshold`` and 1 - ``threshold`` (1 % and 99 %).
        """
        fraction = self.heavy_fraction()
        mixed = (fraction > threshold) & (fraction < 1 - threshold)
        return mixed.sum() * self.dz

    def mode_velocity(self, mode=PERTURBATION_MODE):
        """Amplitude of the seeded mode in the vertical velocity at mid-height [m/s]."""
        row = vertical_velocity(self.psi, self.dx)[self.psi.shape[0] // 2]
        return 2 * np.abs(np.fft.rfft(row)[mode]) / row.size


class RayleighTaylorView(View):
    """Density (left) and vorticity (right) of the tall box, side by side.

    The two 1:2 panels fill the window and the nearly square reel panel
    alike; in a reel their colour bars sit below them.
    """

    figsize = (8.4, 8.0)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        axes = figure.subplots(1, 2, sharey=True)
        extent = (0.0, WIDTH, 0.0, HEIGHT)
        atwood = abs(simulation.atwood)
        self.density = axes[0].imshow(
            simulation.density, extent=extent, cmap="inferno", vmin=1 - atwood,
            vmax=1 + atwood, interpolation="bilinear",
        )  # fmt: skip
        self.vorticity = axes[1].imshow(
            simulation.vorticity, extent=extent, cmap="berlin",
            vmin=-VORTICITY_SCALE, vmax=VORTICITY_SCALE, interpolation="bilinear",
        )  # fmt: skip
        location = "bottom" if portrait else "right"
        figure.colorbar(self.density, ax=axes[0], location=location)
        figure.colorbar(self.vorticity, ax=axes[1], location=location)
        axes[0].set(title=r"Density $\rho/\rho_0$", xlabel="x [m]", ylabel="z [m]")
        axes[1].set(title=r"Vorticity $\omega$ [1/s]", xlabel="x [m]")

    def draw(self):
        self.density.set_data(self.simulation.density)
        self.vorticity.set_data(self.simulation.vorticity)

    def status(self):
        simulation = self.simulation
        return (
            f"t = {simulation.time:.2f} s   mixing layer "
            f"{simulation.mixing_width():.2f} m"
        )


ANIMATION = Animation(
    title="Rayleigh-Taylor Instability",
    subtitle="Heavy fluid on top falls in mushroom plumes",
    filename="rayleigh_taylor_instability.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of dt <= {MAX_TIME_STEP:g} s",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, RayleighTaylorSimulation(), RayleighTaylorView)
    print(
        f"A = {ATWOOD:g}: t = {simulation.time:.2f} s after {simulation.steps} "
        f"steps, mixing layer {simulation.mixing_width():.2f} m"
    )


if __name__ == "__main__":
    main()
