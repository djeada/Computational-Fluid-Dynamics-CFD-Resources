"""SIMPLE and SIMPLEC on a staggered grid for inviscid flow in a converging nozzle.

The steady 1D continuity and momentum equations for incompressible,
frictionless flow through a nozzle of linearly varying area are solved with
the finite volume method on a backward-staggered grid, following Example 6.2
of Versteeg and Malalasekera (2007): first-order upwind convection, a
stagnation-pressure inlet and a fixed static pressure at the outlet. The
converged mass flow and pressure are compared with Bernoulli's equation, and
the residual histories of SIMPLE and SIMPLEC are compared for several
under-relaxation factors.
"""

import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

LENGTH = 2.0  # nozzle length L [m]
AREA_IN = 0.5  # inlet area [m^2]
AREA_OUT = 0.1  # outlet area [m^2]
DENSITY = 1.0  # rho [kg/m^3]
P_STAGNATION = 10.0  # stagnation pressure at the inlet p0 [Pa]
P_EXIT = 0.0  # static pressure at the outlet [Pa]
INITIAL_MASS_FLOW = 1.0  # initial guess for m [kg/s], as in the textbook
TOLERANCE = 1e-6  # stop when the continuity residual drops below this [kg/s]
MAX_ITERATIONS = 2000
DIVERGED = 1e3  # a continuity residual above this [kg/s] counts as divergence
N_NODES_DEMO = (5, 9, 17, 33)  # pressure nodes shown in the profile panel
N_NODES_STUDY = (5, 9, 17, 33, 65, 129, 257)  # grid study of the mass flow
# (algorithm, alpha_u, alpha_p) runs compared in the residual panel
RELAXATION_RUNS = (
    ("SIMPLE", 0.8, 0.8),
    ("SIMPLE", 0.8, 0.2),
    ("SIMPLE", 0.7, 0.3),
    ("SIMPLE", 0.5, 0.5),
    ("SIMPLEC", 0.7, 1.0),
)
N_NODES_RELAXATION = 33  # pressure nodes of the relaxation study
ALPHA_U_SCAN = np.round(np.arange(0.2, 0.96, 0.05), 2)  # momentum factors scanned
ALPHA_P_SCAN = np.round(np.arange(0.1, 1.01, 0.1), 2)  # pressure factors scanned


def area(x):
    """Cross-sectional area A(x), linear from the inlet to the outlet [m^2]."""
    return AREA_IN + (AREA_OUT - AREA_IN) * x / LENGTH


def exact_mass_flow():
    """Bernoulli: p0 = p_exit + m^2 / (2 rho A_out^2)."""
    return AREA_OUT * np.sqrt(2.0 * DENSITY * (P_STAGNATION - P_EXIT))


def exact_pressure(x, mass_flow=None):
    """Static pressure p(x) = p0 - m^2 / (2 rho A(x)^2) for a given mass flow."""
    m = exact_mass_flow() if mass_flow is None else mass_flow
    return P_STAGNATION - 0.5 * m**2 / (DENSITY * area(x) ** 2)


@dataclass
class Result:
    x_p: np.ndarray  # pressure nodes [m]
    x_u: np.ndarray  # velocity nodes [m]
    p: np.ndarray  # pressure at the pressure nodes [Pa]
    u: np.ndarray  # velocity at the velocity nodes [m/s]
    mass_flow: np.ndarray  # rho u A at each velocity node [kg/s]
    residuals: list  # continuity residual sum |b| per iteration [kg/s]
    converged: bool

    @property
    def iterations(self):
        return len(self.residuals)


def solve_nozzle(n_nodes, alpha_u=0.7, alpha_p=0.3, variant="SIMPLE",
                 tol=TOLERANCE, max_iter=MAX_ITERATIONS):  # fmt: skip
    """Run SIMPLE or SIMPLEC on n_nodes pressure nodes (n_nodes - 1 velocity nodes).

    Pressure nodes I = 0..n-1 sit at x_I = I dx; velocity node i = 0..n-2 sits
    halfway between pressure nodes i and i+1 (a backward-staggered grid).
    """
    if n_nodes < 3:
        raise ValueError("need at least three pressure nodes")
    if variant not in ("SIMPLE", "SIMPLEC"):
        raise ValueError(f"unknown variant {variant!r}")
    n_u = n_nodes - 1
    dx = LENGTH / n_u
    x_p = np.arange(n_nodes) * dx
    x_u = x_p[:-1] + 0.5 * dx
    A_p, A_u = area(x_p), area(x_u)

    u = INITIAL_MASS_FLOW / (DENSITY * A_u)
    p = P_STAGNATION + (P_EXIT - P_STAGNATION) * x_p / LENGTH
    residuals = []
    converged = False
    with np.errstate(over="ignore", invalid="ignore"):  # diverging runs overflow
        for _ in range(max_iter):
            u, p, residual = simple_iteration(u, p, A_u, A_p, alpha_u, alpha_p, variant)
            residuals.append(residual)
            if not residual < DIVERGED:  # also catches NaN
                break
            if residual < tol:
                converged = True
                break
    return Result(x_p, x_u, p, u, DENSITY * u * A_u, residuals, converged)


def simple_iteration(u, p, A_u, A_p, alpha_u, alpha_p, variant):
    """One SIMPLE or SIMPLEC outer iteration; returns new u, p and the residual.

    The residual is sum |b|, the mass imbalance of the pressure cells after
    the momentum predictor, the source of the pressure-correction equation.
    """
    n_nodes = len(p)
    n_u = n_nodes - 1
    # Face mass fluxes of the velocity control volumes (cell i spans
    # pressure nodes i and i+1): F_I = rho u_I A_I at pressure node I,
    # with the nodal velocity the average of the neighbouring u.
    F = np.empty(n_nodes)
    F[1:-1] = DENSITY * 0.5 * (u[:-1] * A_u[:-1] + u[1:] * A_u[1:])
    F[0] = DENSITY * u[0] * A_u[0]  # inlet: continuity with the first node
    F[-1] = DENSITY * u[-1] * A_u[-1]  # outlet: upwind (flow is outward)
    F_w, F_e = F[:-1], F[1:]

    # Momentum: a_P u_i = a_W u_{i-1} + (p_I - p_{I+1}) A_i + S (upwind, F > 0)
    a_W = np.concatenate(([0.0], F_w[1:]))
    a_P = F_e.copy()
    source = (p[:-1] - p[1:]) * A_u
    # Inlet node: p_0 = p0 - rho u_A^2 / 2 with u_A = u_0 A_0 / A_in, which
    # is linearised as in Versteeg & Malalasekera (2007), Example 6.2.
    ratio = A_u[0] / A_p[0]
    a_P[0] = F_e[0] + 0.5 * F_w[0] * ratio**2
    source[0] = (P_STAGNATION - p[1]) * A_u[0] + F_w[0] * ratio * u[0]
    # Under-relaxation, then solve the bidiagonal system.
    a_P_relaxed = a_P / alpha_u
    source = source + (1.0 - alpha_u) * a_P_relaxed * u
    bands = np.zeros((2, n_u))
    bands[0] = a_P_relaxed
    bands[1, :-1] = -a_W[1:]
    u_star = solve_banded((1, 0), bands, source, check_finite=False)

    # Velocity-correction coefficients: SIMPLE drops sum(a_nb u'_nb),
    # SIMPLEC subtracts sum(a_nb) from a_P instead.
    denominator = a_P_relaxed - (a_W if variant == "SIMPLEC" else 0.0)
    d = A_u / denominator

    # Pressure correction at the interior pressure nodes 1..n-2; p' = 0 at
    # the inlet node (p_0 follows from p0) and at the outlet (fixed p).
    flux_star = DENSITY * u_star * A_u
    b = flux_star[:-1] - flux_star[1:]  # mass imbalance of each p cell
    a_west = DENSITY * d[:-1] * A_u[:-1]
    a_east = DENSITY * d[1:] * A_u[1:]
    diag = a_west + a_east
    m = n_nodes - 2
    bands = np.zeros((3, m))
    bands[0, 1:] = -a_east[:-1]
    bands[1] = diag
    bands[2, :-1] = -a_west[1:]
    p_corr = np.zeros(n_nodes)
    p_corr[1:-1] = solve_banded((1, 1), bands, b, check_finite=False)

    u = u_star + d * (p_corr[:-1] - p_corr[1:])
    p = p + alpha_p * p_corr
    u_inlet = u[0] * A_u[0] / A_p[0]
    p[0] = P_STAGNATION - 0.5 * DENSITY * u_inlet**2
    p[-1] = P_EXIT
    return u, p, float(np.sum(np.abs(b)))


def iteration_map(n_nodes=N_NODES_RELAXATION):
    """SIMPLE iterations to convergence over the (alpha_p, alpha_u) grid, NaN if not."""
    counts = np.full((len(ALPHA_U_SCAN), len(ALPHA_P_SCAN)), np.nan)
    for i, alpha_u in enumerate(ALPHA_U_SCAN):
        for j, alpha_p in enumerate(ALPHA_P_SCAN):
            result = solve_nozzle(n_nodes, alpha_u, alpha_p)
            if result.converged:
                counts[i, j] = result.iterations
    return counts


def plot_results(demo, study, runs, counts):
    fig, axes = plt.subplots(2, 3, figsize=(16, 9), constrained_layout=True)
    colors = plt.cm.viridis(np.linspace(0.0, 0.85, len(demo)))
    x = np.linspace(0.0, LENGTH, 400)
    m_exact = exact_mass_flow()

    ax = axes[0, 0]
    ax.plot(x, m_exact / (DENSITY * area(x)), "k-", lw=2, label="Bernoulli")
    for color, result in zip(colors, demo, strict=True):
        ax.plot(result.x_u, result.u, "o-", color=color, ms=4,
                label=f"{len(result.x_p)} p nodes")  # fmt: skip
    ax.set(title="Velocity at the velocity nodes", xlabel="x [m]", ylabel="u [m/s]")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(x, exact_pressure(x), "k-", lw=2, label="Bernoulli")
    for color, result in zip(colors, demo, strict=True):
        ax.plot(result.x_p, result.p, "s-", color=color, ms=4,
                label=f"{len(result.x_p)} p nodes")  # fmt: skip
    ax.set(title="Pressure at the pressure nodes", xlabel="x [m]", ylabel="p [Pa]")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    ax = axes[0, 2]
    n = np.array([len(r.x_p) for r in study])
    error = np.array([abs(r.mass_flow.mean() - m_exact) / m_exact for r in study])
    h = LENGTH / (n - 1)
    slope = np.polyfit(np.log(h), np.log(error), 1)[0]
    ax.loglog(
        h, error, "o-", color="tab:blue", label=f"converged SIMPLE (slope {slope:.2f})"
    )
    ax.loglog(h, error[0] * h / h[0], "k--", lw=1, label=r"$\propto \Delta x$")
    ax.set(
        title="Mass-flow error against grid spacing",
        xlabel=r"$\Delta x$ [m]",
        ylabel=r"$|\dot m - \dot m_{\mathrm{exact}}|\,/\,\dot m_{\mathrm{exact}}$ [-]",
    )  # fmt: skip
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 0]
    for (variant, alpha_u, alpha_p), result in zip(RELAXATION_RUNS, runs, strict=True):
        status = f"{result.iterations} it." if result.converged else "diverges"
        ax.semilogy(
            np.arange(1, result.iterations + 1), result.residuals,
            label=rf"{variant} $\alpha_u$ = {alpha_u}, $\alpha_p$ = {alpha_p} ({status})",
        )  # fmt: skip
    ax.axhline(TOLERANCE, color="0.4", ls=":", lw=1)
    ax.set(
        title=f"Continuity residual, {N_NODES_RELAXATION} p nodes",
        xlabel="outer iteration [-]", ylabel=r"$\sum |b|$ [kg/s]", ylim=(1e-7, 1e3),
    )  # fmt: skip
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 1]
    du = ALPHA_U_SCAN[1] - ALPHA_U_SCAN[0]
    dp = ALPHA_P_SCAN[1] - ALPHA_P_SCAN[0]
    extent = (
        ALPHA_P_SCAN[0] - dp / 2, ALPHA_P_SCAN[-1] + dp / 2,
        ALPHA_U_SCAN[0] - du / 2, ALPHA_U_SCAN[-1] + du / 2,
    )  # fmt: skip
    cmap = plt.cm.viridis.with_extremes(bad="0.85")
    image = ax.imshow(
        counts, origin="lower", extent=extent, aspect="auto", cmap=cmap,
        norm=plt.matplotlib.colors.LogNorm(vmin=np.nanmin(counts), vmax=np.nanmax(counts)),
    )  # fmt: skip
    fig.colorbar(image, ax=ax, label="iterations [-]")
    line = np.linspace(0.0, 1.0, 50)
    ax.plot(line, 1.0 - line, "w--", lw=1.5, label=r"$\alpha_u + \alpha_p = 1$")
    ax.set(
        xlim=extent[:2], ylim=extent[2:],
        title=f"SIMPLE iterations, {N_NODES_RELAXATION} p nodes (grey: no convergence)",
        xlabel=r"pressure under-relaxation $\alpha_p$ [-]",
        ylabel=r"momentum under-relaxation $\alpha_u$ [-]",
    )  # fmt: skip
    ax.legend(loc="lower left", fontsize=10)

    ax = axes[1, 2]
    simple = [solve_nozzle(N_NODES_RELAXATION, a, 1.0 - a) for a in ALPHA_U_SCAN]
    simplec = [
        solve_nozzle(N_NODES_RELAXATION, a, 1.0, "SIMPLEC") for a in ALPHA_U_SCAN
    ]
    for results, label, marker in (
        (simple, r"SIMPLE, $\alpha_p = 1 - \alpha_u$", "o-"),
        (simplec, r"SIMPLEC, $\alpha_p = 1$", "s-"),
    ):
        its = [r.iterations if r.converged else np.nan for r in results]
        ax.plot(ALPHA_U_SCAN, its, marker, label=label)
    ax.set(
        title="Iterations against momentum under-relaxation",
        xlabel=r"$\alpha_u$ [-]", ylabel="iterations to converge [-]", yscale="log",
    )  # fmt: skip
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, which="both")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    m_exact = exact_mass_flow()
    print(f"Bernoulli mass flow: {m_exact:.5f} kg/s")
    demo = [solve_nozzle(n) for n in N_NODES_DEMO]
    study = [solve_nozzle(n) for n in N_NODES_STUDY]
    for result in study:
        m = result.mass_flow.mean()
        print(
            f"  {len(result.x_p):4d} p nodes: m = {m:.5f} kg/s "
            f"(error {100 * (m - m_exact) / m_exact:+.2f} %), "
            f"{result.iterations} iterations"
        )
    runs = [
        solve_nozzle(N_NODES_RELAXATION, alpha_u, alpha_p, variant)
        for variant, alpha_u, alpha_p in RELAXATION_RUNS
    ]
    for (variant, alpha_u, alpha_p), result in zip(RELAXATION_RUNS, runs, strict=True):
        outcome = f"{result.iterations} iterations" if result.converged else "diverges"
        print(f"  {variant:7s} alpha_u = {alpha_u}, alpha_p = {alpha_p}: {outcome}")
    counts = iteration_map()
    print(
        f"  SIMPLE converges for {np.sum(np.isfinite(counts))} of {counts.size} "
        f"(alpha_u, alpha_p) pairs; fewest iterations {int(np.nanmin(counts))}"
    )
    finish_figures(
        {"simple_1d_nozzle.png": plot_results(demo, study, runs, counts)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
