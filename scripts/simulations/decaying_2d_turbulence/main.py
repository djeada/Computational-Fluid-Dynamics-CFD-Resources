"""Decaying two-dimensional turbulence in a doubly periodic box.

A random vorticity field whose energy sits in a narrow band of wavenumbers is
evolved with a pseudo-spectral solver of the 2D vorticity equation: 2/3-rule
dealiasing and a fourth-order Runge-Kutta scheme with an integrating factor
for the viscous terms. Like-signed vortices merge, energy moves to ever larger
scales (the inverse energy cascade) while enstrophy cascades to small scales
and is dissipated, until a few large vortices remain. The vorticity is
animated next to its energy spectrum E(k).
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import AsinhNorm
from scipy import fft, ndimage

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Physical parameters (dimensionless: box side 2 pi, initial rms velocity 1)
BOX_SIZE = 2 * np.pi  # L, side of the periodic square; wavenumbers are integers
INITIAL_ENERGY = 0.5  # E = <|u|^2> / 2 at t = 0
PEAK_WAVENUMBER = 7.0  # k0, centre of the initial energy band
BAND_WIDTH = 1.5  # standard deviation of the band around k0
VISCOSITY = 1e-4  # nu, multiplies k^2 in the dissipation
HYPERVISCOSITY = 2e-7  # nu_4, multiplies k^4: damps the grid scale, spares vortices
SEED = 0

# Numerical parameters
GRID_SIZE = 256  # collocation points per side
TIME_STEP = 5e-3  # dt; max |u| |k| dt = 2.0 here, RK4 needs < 2.83
STEPS_PER_FRAME = 10  # time steps between drawn frames
N_FRAMES = 835  # frames of a run (t = 41.75); a 30 s reel shows each one
VORTICITY_SCALE = 20.0  # colour limits +-omega
VORTICITY_LINEAR_WIDTH = 4.0  # colours are linear for |omega| below this, asinh above


def wavenumbers(n, length=BOX_SIZE):
    """kx (rfft half plane) and ky arrays for an n x n grid, shaped to broadcast."""
    scale = 2 * np.pi / length
    kx = scale * np.fft.rfftfreq(n, 1.0 / n)[None, :]
    ky = scale * np.fft.fftfreq(n, 1.0 / n)[:, None]
    return kx, ky


def dealias_mask(n):
    """2/3 rule: keep modes with |kx|, |ky| < n/3 (in units of 2 pi / L).

    A product of two kept modes has wavenumbers below 2n/3; whatever of it
    wraps around the grid lands above n/3, where it is removed again.
    """
    mx = np.abs(np.fft.rfftfreq(n, 1.0 / n))[None, :]
    my = np.abs(np.fft.fftfreq(n, 1.0 / n))[:, None]
    return (mx < n / 3) & (my < n / 3)


def spectral_weights(n):
    """Weights that turn sums over the rfft half plane into full-plane sums."""
    weights = np.full((n, n // 2 + 1), 2.0)
    weights[:, 0] = 1.0
    if n % 2 == 0:
        weights[:, -1] = 1.0
    return weights


def initial_vorticity(n, rng, k0=PEAK_WAVENUMBER, width=BAND_WIDTH,
                      energy=INITIAL_ENERGY):  # fmt: skip
    """Random-phase vorticity field with E(k) ~ exp(-(k - k0)^2 / (2 width^2)).

    White noise gives random phases; its Fourier amplitudes are rescaled so
    that the shell energy follows the band, and the field is normalised to
    the requested kinetic energy. Returns the Fourier coefficients.
    """
    kx, ky = wavenumbers(n)
    k = np.hypot(kx, ky)
    noise_hat = fft.rfft2(rng.standard_normal((n, n)))
    noise_hat /= np.maximum(np.abs(noise_hat), 1e-30)  # unit amplitude, random phase
    # A shell of radius k holds about 2 pi k modes with |u_hat|^2 = |omega_hat|^2 / k^2,
    # so |omega_hat|^2 ~ k E(k).
    band = np.exp(-((k - k0) ** 2) / (2 * width**2))
    omega_hat = noise_hat * np.sqrt(band * k)
    omega_hat[0, 0] = 0.0
    omega_hat *= dealias_mask(n)
    return omega_hat * np.sqrt(energy / kinetic_energy(omega_hat))


def kinetic_energy(omega_hat):
    """E = <|u|^2> / 2, from |u_hat|^2 = |omega_hat|^2 / k^2 (Parseval)."""
    n = omega_hat.shape[0]
    kx, ky = wavenumbers(n)
    k2 = kx**2 + ky**2
    k2[0, 0] = 1.0
    return float(np.sum(spectral_weights(n) * np.abs(omega_hat) ** 2 / k2) / (2 * n**4))


def enstrophy(omega_hat):
    """Z = <omega^2> / 2 (Parseval)."""
    n = omega_hat.shape[0]
    return float(np.sum(spectral_weights(n) * np.abs(omega_hat) ** 2) / (2 * n**4))


def energy_spectrum(omega_hat):
    """Shell-summed E(k) for k = 1, 2, ... up to the dealiasing limit."""
    n = omega_hat.shape[0]
    kx, ky = wavenumbers(n)
    k2 = kx**2 + ky**2
    shell = np.rint(np.sqrt(k2)).astype(int)
    k2[0, 0] = 1.0
    density = spectral_weights(n) * np.abs(omega_hat) ** 2 / k2 / (2 * n**4)
    spectrum = np.bincount(shell.ravel(), density.ravel())
    k_max = int(np.ceil(n / 3)) - 1
    return np.arange(1, k_max + 1), spectrum[1 : k_max + 1]


class SpectralVorticitySolver:
    """d(omega)/dt + u . grad(omega) = -(nu k^2 + nu_4 k^4) omega in Fourier space."""

    def __init__(self, n, viscosity=VISCOSITY, hyperviscosity=HYPERVISCOSITY):
        self.n = n
        self.kx, self.ky = wavenumbers(n)
        k2 = self.kx**2 + self.ky**2
        self.mask = dealias_mask(n)
        self.inverse_k2 = np.where(k2 > 0, 1.0 / np.where(k2 > 0, k2, 1.0), 0.0)
        self.damping = viscosity * k2 + hyperviscosity * k2**2

    def velocity(self, omega_hat):
        """u = d(psi)/dy, v = -d(psi)/dx with psi_hat = omega_hat / k^2."""
        psi_hat = omega_hat * self.inverse_k2
        u = fft.irfft2(1j * self.ky * psi_hat, s=(self.n, self.n), workers=-1)
        v = fft.irfft2(-1j * self.kx * psi_hat, s=(self.n, self.n), workers=-1)
        return u, v

    def nonlinear(self, omega_hat):
        """-(u . grad omega) evaluated on the grid, transformed back and dealiased."""
        u, v = self.velocity(omega_hat)
        shape = (self.n, self.n)
        omega_x = fft.irfft2(1j * self.kx * omega_hat, s=shape, workers=-1)
        omega_y = fft.irfft2(1j * self.ky * omega_hat, s=shape, workers=-1)
        return -fft.rfft2(u * omega_x + v * omega_y, workers=-1) * self.mask

    def step(self, omega_hat, dt):
        """Integrating-factor RK4 (Lawson, 1967): the damping is integrated exactly.

        Classical RK4 applied to exp(D t) omega_hat with D = nu k^2 + nu_4 k^4;
        ``half`` = exp(-D dt / 2) carries values across half a step.
        """
        half = np.exp(-self.damping * dt / 2)
        k1 = self.nonlinear(omega_hat)
        k2 = self.nonlinear(half * (omega_hat + 0.5 * dt * k1))
        k3 = self.nonlinear(half * omega_hat + 0.5 * dt * k2)
        k4 = self.nonlinear(half**2 * omega_hat + dt * half * k3)
        return half**2 * (omega_hat + dt / 6 * k1) + dt / 6 * (
            half * (2 * k2 + 2 * k3) + k4
        )


class TurbulenceSimulation(Simulation):
    """Vorticity Fourier coefficients with energy and enstrophy after every step.

    ``energy[k]`` and ``enstrophy[k]`` belong to step ``k`` (0 = start).
    """

    dt = TIME_STEP

    def __init__(self, n=GRID_SIZE, seed=SEED, viscosity=VISCOSITY,
                 hyperviscosity=HYPERVISCOSITY, dt=TIME_STEP, omega_hat=None):  # fmt: skip
        super().__init__()
        if n < 8:
            raise ValueError("at least 8 points per side are required")
        self.n, self.dt = n, dt
        self.solver = SpectralVorticitySolver(n, viscosity, hyperviscosity)
        if omega_hat is None:
            omega_hat = initial_vorticity(n, np.random.default_rng(seed))
        self.omega_hat = omega_hat * self.solver.mask
        self.initial_spectrum = energy_spectrum(self.omega_hat)
        self.energy, self.enstrophy = [], []
        self.record()

    def record(self):
        self.energy.append(kinetic_energy(self.omega_hat))
        self.enstrophy.append(enstrophy(self.omega_hat))

    def step(self):
        self.omega_hat = self.solver.step(self.omega_hat, self.dt)
        self.record()

    @property
    def vorticity(self):
        return fft.irfft2(self.omega_hat, s=(self.n, self.n), workers=-1)

    def spectrum(self):
        return energy_spectrum(self.omega_hat)

    def count_vortices(self, threshold=VORTICITY_SCALE / 2):
        """Connected regions with |omega| above ``threshold``, joined across edges."""
        omega = self.vorticity
        count = 0
        for sign in (1, -1):
            labels, _ = ndimage.label(sign * omega > threshold)
            # Periodic box: regions touching across opposite edges are one vortex.
            parent = {}

            def find(a):
                while parent.get(a, a) != a:
                    a = parent[a]
                return a

            for first, last in ((labels[0], labels[-1]), (labels[:, 0], labels[:, -1])):
                for a, b in zip(first, last):
                    if a and b and find(a) != find(b):
                        parent[find(a)] = find(b)
            roots = {find(label) for label in np.unique(labels) if label}
            count += len(roots)
        return count


class TurbulenceView(View):
    """Vorticity map and energy spectrum.

    Side by side in the window; in a reel the spectrum is a strip below the
    vorticity. The spectrum shows the initial E(k) (grey) and a k^-3 line.
    """

    figsize = (12.0, 5.6)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        if portrait:
            axes = figure.subplot_mosaic(
                [["omega"], ["spectrum"]], height_ratios=[3.2, 1]
            )
        else:
            axes = figure.subplot_mosaic([["omega", "spectrum"]])
        ax = axes["omega"]
        self.image = ax.imshow(
            simulation.vorticity, extent=(0, BOX_SIZE, 0, BOX_SIZE), cmap="berlin",
            norm=AsinhNorm(VORTICITY_LINEAR_WIDTH, -VORTICITY_SCALE, VORTICITY_SCALE),
            interpolation="bilinear",
        )  # fmt: skip
        ticks = [-VORTICITY_SCALE, -10, -VORTICITY_LINEAR_WIDTH, 0,
                 VORTICITY_LINEAR_WIDTH, 10, VORTICITY_SCALE]  # fmt: skip
        figure.colorbar(
            self.image, ax=ax, ticks=ticks, format="%g", label=r"vorticity $\omega$",
            aspect=30,
        )  # fmt: skip
        ax.set(xticks=[], yticks=[])
        ax = axes["spectrum"]
        k, initial = simulation.initial_spectrum
        ax.loglog(k, initial, color="0.55", lw=1.5, label="t = 0")
        (self.line,) = ax.loglog(k, initial, color="#ffb000", label="now")
        inertial = k >= 2 * PEAK_WAVENUMBER
        ax.loglog(k[inertial], 3 * k[inertial] ** -3.0, "--", color="#4cc9f0",
                  label=r"$k^{-3}$")  # fmt: skip
        ax.set(xlim=(1, k[-1]), ylim=(1e-9, 1), xlabel="wavenumber k", ylabel="E(k)")
        if portrait:  # the empty corner of a short, wide strip
            ax.legend(loc="lower left", ncols=3, borderaxespad=0.3)
        else:
            ax.legend(loc="upper right")

    def draw(self):
        self.image.set_data(self.simulation.vorticity)
        self.line.set_ydata(self.simulation.spectrum()[1])

    def status(self):
        simulation = self.simulation
        return f"t = {simulation.time:.1f}   vortices {simulation.count_vortices()}"


ANIMATION = Animation(
    title="2D Turbulence",
    subtitle="Vortices merge into ever larger ones",
    filename="decaying_2d_turbulence.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of dt = {TIME_STEP:g}",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, TurbulenceSimulation(), TurbulenceView)
    print(
        f"t = {simulation.time:.1f}: energy {simulation.energy[-1]:.4f} "
        f"(from {simulation.energy[0]:.4f}), enstrophy {simulation.enstrophy[-1]:.2f} "
        f"(from {simulation.enstrophy[0]:.2f}), {simulation.count_vortices()} vortices"
    )


if __name__ == "__main__":
    main()
