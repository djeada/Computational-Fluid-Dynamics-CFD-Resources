"""Measure the viscosity of the D2Q9 BGK lattice Boltzmann scheme with a decaying Taylor-Green vortex.

A doubly periodic Taylor-Green vortex of wavenumber k = 2 pi / N decays as
exp(-2 nu k^2 t) in velocity and exp(-4 nu k^2 t) in kinetic energy. Fitting
the energy decay of the lattice Boltzmann solution gives a measured viscosity,
which is compared with nu = c_s^2 (tau - 1/2) and with the unshifted kinetic
value c_s^2 tau for several relaxation times. A resolution study shows that the
remaining discrepancy decreases as 1/N^2.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# D2Q9 lattice in lattice units (dx = dt = 1), counter-clockwise ordering.
VELOCITIES = np.array(
    [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
)
WEIGHTS = np.array([4 / 9] + [1 / 9] * 4 + [1 / 36] * 4)
CS2 = 1.0 / 3.0  # squared lattice speed of sound c_s^2 [-]

U0 = 0.005  # initial velocity amplitude (lattice units); Ma = U0 / c_s = 0.0087
GRID = 32  # nodes per side of the periodic box in the tau scan
TAUS = (0.51, 0.55, 0.6, 0.7, 0.8, 1.0, 1.25, 1.5, 2.0)
CURVE_TAUS = (0.55, 0.8, 1.5)  # energy histories drawn in panel (b)
RESOLUTION_TAUS = (1.0, 1.5)
RESOLUTIONS = (16, 32, 64, 128)
ENERGY_DROP = 2.0  # run until E / E0 = exp(-ENERGY_DROP) by the predicted decay
FIT_START = 0.2  # discard the first 20% of the run (start-up transient) in the fit


def viscosity(tau):
    """Lattice kinematic viscosity nu = c_s^2 (tau - 1/2) of the BGK scheme."""
    return CS2 * (np.asarray(tau) - 0.5)


def equilibrium(rho, u):
    """Second-order D2Q9 equilibrium for rho (nx, ny) and u (2, nx, ny)."""
    cu = np.einsum("qd,dxy->qxy", VELOCITIES, u)
    usq = np.sum(u**2, axis=0)
    return (
        WEIGHTS[:, None, None]
        * rho
        * (1.0 + cu / CS2 + cu**2 / (2 * CS2**2) - usq / (2 * CS2))
    )


def moments(f):
    """Density (nx, ny) and velocity (2, nx, ny) of populations f (9, nx, ny)."""
    rho = f.sum(axis=0)
    return rho, np.einsum("qd,qxy->dxy", VELOCITIES, f) / rho


def taylor_green_initial(n, u0=U0):
    """Velocity and density of the Taylor-Green vortex on an n x n periodic lattice.

    u = -u0 cos(kx) sin(ky), v = u0 sin(kx) cos(ky), and the density carries the
    pressure p - p0 = -rho0 u0^2 (cos 2kx + cos 2ky) / 4 through p = c_s^2 rho.
    """
    k = 2 * np.pi / n
    x, y = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    u = np.array(
        [-u0 * np.cos(k * x) * np.sin(k * y), u0 * np.sin(k * x) * np.cos(k * y)]
    )
    rho = 1.0 - u0**2 / (4 * CS2) * (np.cos(2 * k * x) + np.cos(2 * k * y))
    return rho, u


def collide_and_stream(f, tau):
    """One BGK collision followed by periodic streaming with np.roll."""
    rho, u = moments(f)
    f = f - (f - equilibrium(rho, u)) / tau
    for i, c in enumerate(VELOCITIES):
        f[i] = np.roll(f[i], shift=tuple(c), axis=(0, 1))
    return f


def run_decay(n, tau, u0=U0, energy_drop=ENERGY_DROP):
    """Run the vortex; return time steps, kinetic energy history and total mass.

    The run length is chosen so that the predicted energy falls by
    exp(-energy_drop): t_end = energy_drop / (4 nu k^2).
    """
    k = 2 * np.pi / n
    n_steps = int(np.ceil(energy_drop / (4 * viscosity(tau) * k**2)))
    rho, u = taylor_green_initial(n, u0)
    f = equilibrium(rho, u)
    energy = np.empty(n_steps + 1)
    mass = np.empty(n_steps + 1)
    for step in range(n_steps + 1):
        rho, u = moments(f)
        energy[step] = 0.5 * np.mean(rho * np.sum(u**2, axis=0))
        mass[step] = rho.sum()
        if step < n_steps:
            f = collide_and_stream(f, tau)
    return np.arange(n_steps + 1), energy, mass


def measured_viscosity(n, tau, u0=U0):
    """Viscosity from a least-squares fit of ln E(t) = ln E0 - 4 nu k^2 t."""
    t, energy, _ = run_decay(n, tau, u0)
    start = int(FIT_START * t[-1])
    slope = np.polyfit(t[start:], np.log(energy[start:]), 1)[0]
    return -slope / (4 * (2 * np.pi / n) ** 2)


def make_figure(histories, taus, nu_measured, resolution_errors):
    """Four panels: initial vorticity, energy decay, nu versus tau, error versus N."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9.5))
    colors = plt.cm.tab10.colors

    ax = axes[0, 0]
    rho, u = taylor_green_initial(GRID)
    vorticity = np.gradient(u[1], axis=0) - np.gradient(u[0], axis=1)
    image = ax.imshow(
        vorticity.T / (U0 * 2 * np.pi / GRID),
        origin="lower",
        cmap="RdBu_r",
        vmin=-2,
        vmax=2,
        extent=(-0.5, GRID - 0.5, -0.5, GRID - 0.5),
    )
    step = 2
    x = np.arange(GRID)
    ax.quiver(
        x[::step],
        x[::step],
        u[0, ::step, ::step].T,
        u[1, ::step, ::step].T,
        color="k",
        scale=U0 * 25,
        width=0.004,
    )
    fig.colorbar(image, ax=ax, label=r"Vorticity $\omega / (u_0 k)$ [-]")
    ax.set_xlabel("x [nodes]", fontsize=11)
    ax.set_ylabel("y [nodes]", fontsize=11)
    ax.set_title(f"(a) Initial vortex, {GRID} x {GRID} periodic lattice", fontsize=12)

    ax = axes[0, 1]
    k = 2 * np.pi / GRID
    for color, (tau, (t, energy)) in zip(colors, histories.items()):
        ax.semilogy(
            t[:: max(1, len(t) // 25)],
            (energy / energy[0])[:: max(1, len(t) // 25)],
            "o",
            color=color,
            markersize=5,
            label=rf"LBM, $\tau = {tau:g}$",
        )
        ax.semilogy(t, np.exp(-4 * viscosity(tau) * k**2 * t), "-", color=color)
    ax.plot([], [], "k-", label=r"$\exp(-4\nu k^2 t)$, $\nu = c_s^2(\tau - 1/2)$")
    ax.set_xlabel("Time step t [-]", fontsize=11)
    ax.set_ylabel(r"Kinetic energy $E / E_0$ [-]", fontsize=11)
    ax.set_title("(b) Energy decay", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 0]
    tau_line = np.linspace(0.5, max(taus), 50)
    ax.plot(tau_line, viscosity(tau_line), "k-", label=r"$c_s^2(\tau - 1/2)$")
    ax.plot(tau_line, CS2 * tau_line, "k--", label=r"$c_s^2 \tau$ (no shift)")
    ax.plot(taus, nu_measured, "o", color=colors[0], markersize=7, label="measured")
    ax.set_xlabel(r"Relaxation time $\tau$ [-]", fontsize=11)
    ax.set_ylabel(r"Kinematic viscosity $\nu$ [lattice units]", fontsize=11)
    ax.set_title(f"(c) Measured viscosity, N = {GRID}", fontsize=12)
    ax.set_xlim(0.45, max(taus) + 0.05)
    ax.set_ylim(0, None)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    grid = np.array(RESOLUTIONS, dtype=float)
    for color, tau, err in zip(colors, RESOLUTION_TAUS, resolution_errors):
        ax.loglog(grid, err, "o-", color=color, label=rf"$\tau = {tau:g}$")
    ax.loglog(
        grid,
        0.5 * resolution_errors[0][0] * (grid / grid[0]) ** -2,
        "k--",
        linewidth=1,
        label="slope $-2$",
    )
    ax.set_xlabel("Lattice size N [nodes per side]", fontsize=11)
    ax.set_ylabel(r"Relative viscosity error $|\nu_m / \nu - 1|$ [-]", fontsize=11)
    ax.set_title("(d) Convergence with resolution", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    histories = {}
    for tau in CURVE_TAUS:
        t, energy, _ = run_decay(GRID, tau)
        histories[tau] = (t, energy)

    nu_measured = np.array([measured_viscosity(GRID, tau) for tau in TAUS])
    print(f"N = {GRID}, u0 = {U0}:")
    for tau, nu_m in zip(TAUS, nu_measured):
        nu = viscosity(tau)
        print(
            f"  tau = {tau:5.2f}: nu predicted {nu:.5f}, measured {nu_m:.5f} "
            f"({100 * (nu_m / nu - 1):+.2f}%), c_s^2 tau = {CS2 * tau:.5f}"
        )

    resolution_errors = []
    for tau in RESOLUTION_TAUS:
        errors = [
            abs(measured_viscosity(n, tau) / viscosity(tau) - 1) for n in RESOLUTIONS
        ]
        resolution_errors.append(errors)
        print(
            f"tau = {tau:g}: relative viscosity error for N = {RESOLUTIONS}: "
            + ", ".join(f"{e:.2e}" for e in errors)
        )

    finish_figures(
        {
            "lbm_taylor_green_decay.png": make_figure(
                histories, TAUS, nu_measured, resolution_errors
            )
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
