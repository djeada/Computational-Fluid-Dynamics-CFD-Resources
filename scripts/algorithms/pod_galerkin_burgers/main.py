"""POD-Galerkin reduced-order model of the 1D viscous Burgers equation.

The full-order model (FOM) is u_t + u u_x = nu u_xx on (0, 1) with u = 0 at
both ends, discretized by second-order central differences on 2000 interior
points and advanced with an IMEX Euler scheme (implicit diffusion, explicit
convection). Snapshots from the first half of the run are compressed by POD,
and the semi-discrete equations are projected onto r modes. Because the
convection term is quadratic, the reduced constant, linear and quadratic
operators are computed once offline, so an online time step costs O(r^3)
operations instead of O(N). The figure compares the FOM with ROMs of size
r = 2, 5 and 10, plots the error against r inside the training window, in a
later time window and at a new viscosity, and reports the wall-clock times.
"""

import sys
import time
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import compute_pod  # noqa: E402

N_POINTS = 2000  # interior grid points on (0, 1) m
NU_TRAIN = 0.005  # kinematic viscosity of the training run (m^2/s)
NU_TEST = 0.004  # viscosity of the parameter test (m^2/s)
DT = 2.5e-4  # time step (s); convective CFL u dt / dx = 0.5 for u = 1 m/s
T_TRAIN = 0.5  # snapshots are collected for 0 <= t <= T_TRAIN (s)
T_END = 1.0  # the FOM and ROMs run to T_END; (T_TRAIN, T_END] is the test window
SNAPSHOT_EVERY = 10  # store every 10th time step (every 2.5 ms)
PULSE_CENTER = 0.25  # initial Gaussian pulse centre (m)
PULSE_WIDTH = 0.08  # initial pulse width (m)
SHOWN_RANKS = (2, 5, 10)  # ROM sizes drawn in the solution panels
SWEEP_RANKS = (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30)  # error-vs-r sweep
PROFILE_TIME = T_TRAIN  # time of the profile panel (s)
TIMING_REPEATS = 3  # wall-clock times are the best of this many runs


@dataclass(frozen=True)
class Grid:
    """Uniform grid of interior points with homogeneous Dirichlet ends."""

    n: int

    @property
    def dx(self) -> float:
        return 1.0 / (self.n + 1)

    @property
    def x(self) -> np.ndarray:
        return np.arange(1, self.n + 1) * self.dx


def first_derivative(u: np.ndarray, dx: float) -> np.ndarray:
    """Central difference du/dx along axis 0 with u = 0 outside the grid.

    Works on a vector (one field) or on a matrix whose columns are fields.
    """
    du = np.zeros_like(u)
    du[1:-1] = u[2:] - u[:-2]
    du[0] = u[1]
    du[-1] = -u[-2]
    return du / (2.0 * dx)


def second_derivative(u: np.ndarray, dx: float) -> np.ndarray:
    """Central difference d^2u/dx^2 along axis 0 with u = 0 outside the grid."""
    d2u = -2.0 * u
    d2u[1:] += u[:-1]
    d2u[:-1] += u[1:]
    return d2u / dx**2


def initial_condition(grid: Grid) -> np.ndarray:
    """Gaussian pulse that steepens into a moving front."""
    return np.exp(-(((grid.x - PULSE_CENTER) / PULSE_WIDTH) ** 2))


def solve_fom(u0, grid, nu, dt, n_steps, every=1):
    """Advance the FOM with IMEX Euler and return the stored states as columns.

    (I - dt nu D2) u^{n+1} = u^n - dt u^n * (D1 u^n). Column 0 is u0, and column
    k holds the state after k * every steps.
    """
    d = nu * dt / grid.dx**2
    banded = np.zeros((3, grid.n))
    banded[0, 1:] = -d
    banded[1, :] = 1.0 + 2.0 * d
    banded[2, :-1] = -d
    u = np.array(u0, dtype=float)
    states = [u.copy()]
    for step in range(1, n_steps + 1):
        u = solve_banded((1, 1), banded, u - dt * u * first_derivative(u, grid.dx))
        if step % every == 0:
            states.append(u.copy())
    return np.column_stack(states)


@dataclass(frozen=True)
class ReducedOperators:
    """Offline POD-Galerkin operators for u = mean + V a.

    da/dt = nu (d + D a) - (c + L a + Q(a, a)), with Q(a, a)_i = Q_ijk a_j a_k.
    The diffusion terms are kept apart because they are linear in nu.
    """

    mean: np.ndarray
    modes: np.ndarray
    diffusion: np.ndarray  # D = V^T D2 V
    diffusion_mean: np.ndarray  # d = V^T D2 mean
    convection_mean: np.ndarray  # c = V^T (mean * D1 mean)
    convection_linear: np.ndarray  # L
    convection_quadratic: np.ndarray  # Q reshaped to (r, r * r)

    @property
    def rank(self) -> int:
        return self.modes.shape[1]


def build_rom(mean, modes, grid) -> ReducedOperators:
    """Project the semi-discrete Burgers operators onto the POD modes.

    N(mean + V a) = mean*D1 mean + (mean*D1 V + (D1 mean)*V) a + (V a)*(D1 V a),
    so the quadratic tensor is Q_ijk = sum_n V_ni V_nj (D1 V)_nk.
    """
    mean = np.asarray(mean, dtype=float).ravel()
    dx = grid.dx
    d_modes = first_derivative(modes, dx)
    d_mean = first_derivative(mean, dx)
    quadratic = np.einsum("ni,nj,nk->ijk", modes, modes, d_modes, optimize=True)
    return ReducedOperators(
        mean=mean,
        modes=modes,
        diffusion=modes.T @ second_derivative(modes, dx),
        diffusion_mean=modes.T @ second_derivative(mean, dx),
        convection_mean=modes.T @ (mean * d_mean),
        convection_linear=modes.T @ (mean[:, None] * d_modes + d_mean[:, None] * modes),
        convection_quadratic=quadratic.reshape(modes.shape[1], -1),
    )


def solve_rom(ops: ReducedOperators, u0, nu, dt, n_steps, every=1):
    """Advance the ROM with the same IMEX Euler scheme as the FOM.

    (I - dt nu D) a^{n+1} = a^n + dt (nu d - c - L a^n - Q(a^n, a^n)).
    Returns the reduced coefficients of the stored states as columns.
    """
    r = ops.rank
    step_matrix = np.linalg.inv(np.eye(r) - dt * nu * ops.diffusion)
    forcing = nu * ops.diffusion_mean - ops.convection_mean
    linear = ops.convection_linear
    quadratic = ops.convection_quadratic
    a = ops.modes.T @ (np.asarray(u0, dtype=float) - ops.mean)
    coefficients = [a.copy()]
    for step in range(1, n_steps + 1):
        rhs = forcing - linear @ a - quadratic @ np.outer(a, a).ravel()
        a = step_matrix @ (a + dt * rhs)
        if step % every == 0:
            coefficients.append(a.copy())
    return np.column_stack(coefficients)


def reconstruct(ops: ReducedOperators, coefficients) -> np.ndarray:
    """Full fields mean + V a for coefficient columns a."""
    return ops.mean[:, None] + ops.modes @ coefficients


def relative_errors(approx, reference) -> np.ndarray:
    """Relative 2-norm error of each column."""
    return np.linalg.norm(approx - reference, axis=0) / np.linalg.norm(
        reference, axis=0
    )


def window_error(errors) -> float:
    """Root-mean-square of per-snapshot relative errors over a window."""
    return float(np.sqrt(np.mean(np.square(errors))))


def best_time(function, repeats=TIMING_REPEATS):
    """Return the result of function() and its best wall-clock time in s."""
    best = np.inf
    for _ in range(repeats):
        start = time.perf_counter()
        result = function()
        best = min(best, time.perf_counter() - start)
    return result, best


def run_study():
    """Run the FOMs, build the POD basis, and sweep the ROM size."""
    grid = Grid(N_POINTS)
    u0 = initial_condition(grid)
    n_steps = round(T_END / DT)
    n_train = round(T_TRAIN / DT) // SNAPSHOT_EVERY + 1  # stored states in training
    times = np.arange(n_steps // SNAPSHOT_EVERY + 1) * DT * SNAPSHOT_EVERY

    fom, fom_time = best_time(
        lambda: solve_fom(u0, grid, NU_TRAIN, DT, n_steps, SNAPSHOT_EVERY)
    )
    fom_test = solve_fom(u0, grid, NU_TEST, DT, n_steps, SNAPSHOT_EVERY)

    offline_start = time.perf_counter()
    pod = compute_pod(fom[:, :n_train])
    pod_time = time.perf_counter() - offline_start

    sweep = {}
    for r in sorted(set(SWEEP_RANKS) | set(SHOWN_RANKS)):
        start = time.perf_counter()
        ops = build_rom(pod.mean, pod.modes[:, :r], grid)
        build_time = time.perf_counter() - start
        coefficients, rom_time = best_time(
            lambda ops=ops: solve_rom(ops, u0, NU_TRAIN, DT, n_steps, SNAPSHOT_EVERY)
        )
        fields = reconstruct(ops, coefficients)
        errors = relative_errors(fields, fom)
        test_fields = reconstruct(
            ops, solve_rom(ops, u0, NU_TEST, DT, n_steps, SNAPSHOT_EVERY)
        )
        test_errors = relative_errors(test_fields[:, :n_train], fom_test[:, :n_train])
        modes = pod.modes[:, :r]
        fluctuations = fom[:, :n_train] - pod.mean
        projected = pod.mean + modes @ (modes.T @ fluctuations)
        sweep[r] = {
            "fields": fields,
            "projection": window_error(relative_errors(projected, fom[:, :n_train])),
            "errors": errors,
            "train": window_error(errors[:n_train]),
            "later": window_error(errors[n_train:]),
            "new_nu": window_error(test_errors),
            "energy": np.linalg.norm(fields, axis=0) / np.linalg.norm(fom, axis=0),
            "build_time": build_time,
            "rom_time": rom_time,
        }
    return {
        "grid": grid,
        "times": times,
        "n_train": n_train,
        "fom": fom,
        "fom_time": fom_time,
        "pod": pod,
        "pod_time": pod_time,
        "sweep": sweep,
    }


def plot_study(study):
    """Six panels: field, profiles, POD spectrum, energy, error vs r, timing."""
    grid, times = study["grid"], study["times"]
    fom, sweep, pod = study["fom"], study["sweep"], study["pod"]
    colors = dict(zip(SHOWN_RANKS, plt.cm.tab10.colors[:3], strict=True))

    fig, axes = plt.subplots(2, 3, figsize=(13, 7.6), constrained_layout=True)
    ax = axes[0, 0]
    mesh = ax.pcolormesh(grid.x, times, fom.T, shading="auto", cmap="viridis")
    ax.axhline(T_TRAIN, color="white", ls="--", lw=1.2)
    ax.text(0.97, T_TRAIN + 0.02, "end of snapshots", color="white", ha="right")
    fig.colorbar(mesh, ax=ax, label="u [m/s]")
    ax.set(xlabel="x [m]", ylabel="t [s]", title="(a) FOM solution u(x, t)")

    ax = axes[0, 1]
    k = int(np.argmin(np.abs(times - PROFILE_TIME)))
    ax.plot(grid.x, fom[:, 0], color="0.6", lw=1.5, label="initial condition")
    ax.plot(grid.x, fom[:, k], "k", lw=2.6, label="FOM")
    for r in SHOWN_RANKS:
        ax.plot(
            grid.x,
            sweep[r]["fields"][:, k],
            color=colors[r],
            lw=1.4,
            label=f"ROM r = {r}",
        )
    ax.set(
        xlim=(0, 0.8),
        xlabel="x [m]",
        ylabel="u [m/s]",
        title=f"(b) Profiles at t = {times[k]:.2f} s",
    )
    ax.legend(fontsize=9, loc="upper right")

    ax = axes[0, 2]
    energy = np.cumsum(pod.energy_fractions)
    ranks = np.arange(1, pod.singular_values.size + 1)
    ax.semilogy(
        ranks,
        pod.singular_values / pod.singular_values[0],
        "o-",
        ms=3,
        color="tab:blue",
        label=r"$\sigma_r / \sigma_1$",
    )
    ax.semilogy(
        ranks,
        1.0 - energy + 1e-17,
        "s-",
        ms=3,
        color="tab:orange",
        label="unresolved energy fraction",
    )
    ax.set(
        xlim=(0, 40),
        ylim=(1e-8, 2),
        xlabel="mode number r [-]",
        ylabel="[-]",
        title="(c) POD spectrum of the snapshots",
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=9)

    ax = axes[1, 0]
    for r in SHOWN_RANKS:
        ax.plot(times, sweep[r]["energy"], color=colors[r], label=f"ROM r = {r}")
    ax.axhline(1.0, color="k", lw=1)
    ax.axvspan(0, T_TRAIN, color="0.9", zorder=0)
    ax.set(
        xlabel="t [s]",
        ylabel=r"$\|u_{ROM}\| / \|u_{FOM}\|$ [-]",
        title="(d) Norm of the ROM solution relative to the FOM",
    )
    ax.text(0.03, 0.95, "training window", transform=ax.transAxes, va="top")
    ax.legend(fontsize=9, loc="lower right")

    ax = axes[1, 1]
    sweep_r = np.array(SWEEP_RANKS)
    for key, label, marker in (
        ("train", rf"training window, $\nu$ = {NU_TRAIN}", "o"),
        ("new_nu", rf"training window, new $\nu$ = {NU_TEST}", "^"),
        ("later", f"later window {T_TRAIN} < t <= {T_END} s", "s"),
    ):
        ax.semilogy(
            sweep_r,
            [sweep[r][key] for r in SWEEP_RANKS],
            marker=marker,
            ms=4,
            label=label,
        )
    ax.semilogy(
        sweep_r,
        [sweep[r]["projection"] for r in SWEEP_RANKS],
        "k:",
        lw=1.5,
        label="best fit: projection of the snapshots",
    )
    ax.set(
        xlim=(0, max(SWEEP_RANKS) + 1),
        ylim=(1e-6, 2),
        xlabel="r [-]",
        ylabel="RMS relative error [-]",
        title="(e) ROM error against basis size",
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=9, loc="lower left")

    ax = axes[1, 2]
    rom_times = [sweep[r]["rom_time"] for r in SWEEP_RANKS]
    ax.plot(sweep_r, rom_times, "o-", ms=4, color="tab:blue", label="ROM online run")
    ax.axhline(study["fom_time"], color="k", ls="--", label=f"FOM run (N = {grid.n})")
    ax.set(
        ylim=(0, 1.15 * study["fom_time"]),
        xlabel="r [-]",
        ylabel="wall-clock time [s]",
        title=f"(f) Cost of the run to t = {T_END} s",
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=9, loc="center right")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    study = run_study()
    sweep = study["sweep"]
    print(
        f"FOM: N = {N_POINTS}, {round(T_END / DT)} steps, "
        f"{study['fom_time']:.3f} s; POD of {study['n_train']} snapshots "
        f"in {study['pod_time']:.3f} s"
    )
    print(
        "   r   train err   new-nu err   later err   max norm ratio   ROM time [s]"
        "   speed-up"
    )
    for r in SWEEP_RANKS:
        s = sweep[r]
        print(
            f"{r:4d}   {s['train']:.3e}   {s['new_nu']:.3e}    {s['later']:.3e}"
            f"   {s['energy'][: study['n_train']].max():.3f}"
            f"            {s['rom_time']:.4f}       {study['fom_time'] / s['rom_time']:.1f}"
        )
    figure = plot_study(study)
    finish_figures(
        {"pod_galerkin_burgers.png": figure}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
