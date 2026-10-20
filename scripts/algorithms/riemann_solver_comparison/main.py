"""First-order Godunov schemes with five Riemann solvers on two shock-tube problems.

The 1D Euler equations are solved with the first-order finite-volume Godunov
scheme, using the exact Riemann solver of Toro (2009, chapter 4) and the
approximate Rusanov, HLL, HLLC and Roe fluxes at the cell faces. The results
for Sod's shock tube and Toro's test 3 (a strong blast wave) are compared with
the exact solution, with zooms on the rarefaction and the contact, and the L1
error in density is plotted against the number of cells.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GAMMA = 1.4  # ratio of specific heats [-]
CFL = 0.9  # Courant number of the first-order scheme
START_CFL = 0.2  # Courant number of the first START_STEPS steps
START_STEPS = 5  # cell speeds underestimate the waves of the initial jump

# Shock-tube problems on [0, 1]: (rho, u, p) left and right of x0, end time.
PROBLEMS = {
    "sod": {
        "title": "Sod shock tube",
        "left": (1.0, 0.0, 1.0),
        "right": (0.125, 0.0, 0.1),
        "x0": 0.5,
        "t_end": 0.2,
    },
    "toro3": {
        "title": "Toro test 3 (blast wave)",
        "left": (1.0, 0.0, 1000.0),
        "right": (1.0, 0.0, 0.01),
        "x0": 0.5,
        "t_end": 0.012,
    },
}
N_CELLS = 100  # cells in the solution plots
N_REFINEMENT = (50, 100, 200, 400, 800, 1600)  # cells in the convergence study
N_EXACT = 2000  # sample points of the exact solution in the plots
SOLVERS = ("exact", "rusanov", "hll", "hllc", "roe")
LABELS = {
    "exact": "Godunov (exact)",
    "rusanov": "Rusanov",
    "hll": "HLL",
    "hllc": "HLLC",
    "roe": "Roe",
}
ROE_ENTROPY_FIX = 0.1  # Harten's delta as a fraction of |u~| + c~


# ---------------------------------------------------------------- gas state
def conservative(rho, u, p, gamma=GAMMA):
    """Conservative variables (rho, rho u, E) from primitive ones."""
    rho, u, p = np.broadcast_arrays(*map(np.asarray, (rho, u, p)))
    return np.array([rho, rho * u, p / (gamma - 1.0) + 0.5 * rho * u**2])


def primitive(U, gamma=GAMMA):
    """Density, velocity and pressure from conservative variables."""
    rho = U[0]
    u = U[1] / rho
    p = (gamma - 1.0) * (U[2] - 0.5 * rho * u**2)
    return rho, u, p


def physical_flux(U, gamma=GAMMA):
    """Euler flux F(U) = (rho u, rho u^2 + p, (E + p) u)."""
    rho, u, p = primitive(U, gamma)
    return np.array([rho * u, rho * u**2 + p, (U[2] + p) * u])


def sound_speed(rho, p, gamma=GAMMA):
    return np.sqrt(gamma * p / rho)


# ------------------------------------------------------ exact Riemann solver
def pressure_function(p, rho_k, p_k, c_k, gamma=GAMMA):
    """Toro's f_K(p) and its derivative: velocity change across wave K.

    A shock (p > p_K) follows the Rankine-Hugoniot relations, a rarefaction
    (p <= p_K) the isentropic Riemann invariant.
    """
    a_k = 2.0 / ((gamma + 1.0) * rho_k)
    b_k = (gamma - 1.0) / (gamma + 1.0) * p_k
    shock = p > p_k
    root = np.sqrt(a_k / (p + b_k))
    f_shock = (p - p_k) * root
    d_shock = root * (1.0 - 0.5 * (p - p_k) / (p + b_k))
    ratio = p / p_k
    f_fan = 2.0 * c_k / (gamma - 1.0) * (ratio ** ((gamma - 1.0) / (2.0 * gamma)) - 1)
    d_fan = ratio ** (-(gamma + 1.0) / (2.0 * gamma)) / (rho_k * c_k)
    return np.where(shock, f_shock, f_fan), np.where(shock, d_shock, d_fan)


def star_state(left, right, gamma=GAMMA, tol=1e-14, max_iter=100):
    """Pressure p* and velocity u* between the outer waves (Newton iteration).

    ``left`` and ``right`` are (rho, u, p) tuples of scalars or arrays. The
    initial guess is the primitive-variable (PVRS) estimate of Toro (2009),
    eq. 4.47, kept positive. Returns (p_star, u_star, iterations).
    """
    rl, ul, pl = (np.asarray(v, dtype=float) for v in left)
    rr, ur, pr = (np.asarray(v, dtype=float) for v in right)
    cl, cr = sound_speed(rl, pl, gamma), sound_speed(rr, pr, gamma)
    if np.any(2.0 * (cl + cr) / (gamma - 1.0) <= ur - ul):
        raise ValueError("the initial data generate a vacuum")
    guess = 0.5 * (pl + pr) - 0.125 * (ur - ul) * (rl + rr) * (cl + cr)
    p = np.maximum(guess, 1e-8 * np.minimum(pl, pr))
    for iteration in range(1, max_iter + 1):
        fl, dl = pressure_function(p, rl, pl, cl, gamma)
        fr, dr = pressure_function(p, rr, pr, cr, gamma)
        p_new = np.maximum(p - (fl + fr + ur - ul) / (dl + dr), 1e-3 * p)
        change = np.max(2.0 * np.abs(p_new - p) / (p_new + p))
        p = p_new
        if change < tol:
            break
    fl, _ = pressure_function(p, rl, pl, cl, gamma)
    fr, _ = pressure_function(p, rr, pr, cr, gamma)
    return p, 0.5 * (ul + ur) + 0.5 * (fr - fl), iteration


def sample_riemann(left, right, xi, gamma=GAMMA):
    """Exact (rho, u, p) at similarity coordinates xi = (x - x0) / t.

    Works elementwise: left/right may be arrays of states (one per face) with
    xi a scalar or an array of matching shape. Follows Toro (2009), sec. 4.5.
    """
    rl, ul, pl = (np.asarray(v, dtype=float) for v in left)
    rr, ur, pr = (np.asarray(v, dtype=float) for v in right)
    p_star, u_star, _ = star_state((rl, ul, pl), (rr, ur, pr), gamma)
    xi = np.asarray(xi, dtype=float)
    on_left = xi <= u_star
    sign = np.where(on_left, -1.0, 1.0)  # -1: left wave, +1: right wave
    rho = np.where(on_left, rl, rr)
    u = np.where(on_left, ul, ur)
    p = np.where(on_left, pl, pr)
    c = sound_speed(rho, p, gamma)
    g1 = (gamma - 1.0) / (gamma + 1.0)
    ratio = p_star / p

    # Shock: speed and the density behind it.
    shock_speed = u + sign * c * np.sqrt(
        (gamma + 1.0) / (2.0 * gamma) * ratio + (gamma - 1.0) / (2.0 * gamma)
    )
    rho_shock = rho * (ratio + g1) / (g1 * ratio + 1.0)
    # Rarefaction: head and tail speeds, the isentropic star density and the fan.
    c_star = c * ratio ** ((gamma - 1.0) / (2.0 * gamma))
    head = u + sign * c
    tail = u_star + sign * c_star
    rho_fan_star = rho * ratio ** (1.0 / gamma)
    u_fan = 2.0 / (gamma + 1.0) * (-sign * c + 0.5 * (gamma - 1.0) * u + xi)
    c_fan = 2.0 / (gamma + 1.0) * (c - sign * 0.5 * (gamma - 1.0) * (u - xi))
    rho_fan = rho * (c_fan / c) ** (2.0 / (gamma - 1.0))
    p_fan = p * (c_fan / c) ** (2.0 * gamma / (gamma - 1.0))

    is_shock = p_star > p
    ahead = np.where(is_shock, sign * (xi - shock_speed) > 0, sign * (xi - head) > 0)
    in_fan = ~is_shock & ~ahead & (sign * (xi - tail) > 0)
    behind = ~ahead & ~in_fan
    rho_behind = np.where(is_shock, rho_shock, rho_fan_star)
    out_rho = np.select([ahead, in_fan, behind], [rho, rho_fan, rho_behind])
    out_u = np.select([ahead, in_fan, behind], [u, u_fan, u_star * np.ones_like(u)])
    out_p = np.select([ahead, in_fan, behind], [p, p_fan, p_star * np.ones_like(p)])
    return out_rho, out_u, out_p


def exact_solution(problem, x, t, gamma=GAMMA):
    """Exact density, velocity and pressure of a shock-tube problem at time t."""
    xi = (np.asarray(x) - problem["x0"]) / max(t, 1e-300)
    n = np.size(xi)
    left = [np.full(n, v) for v in problem["left"]]
    right = [np.full(n, v) for v in problem["right"]]
    return sample_riemann(left, right, np.reshape(xi, n), gamma)


# ----------------------------------------------------------- numerical fluxes
def exact_flux(UL, UR, gamma=GAMMA):
    """Godunov flux: the physical flux of the exact solution at x/t = 0."""
    state = sample_riemann(primitive(UL, gamma), primitive(UR, gamma), 0.0, gamma)
    return physical_flux(conservative(*state, gamma), gamma)


def davis_speeds(UL, UR, gamma=GAMMA):
    """Outer wave-speed estimates S_L, S_R of Davis (1988)."""
    rl, ul, pl = primitive(UL, gamma)
    rr, ur, pr = primitive(UR, gamma)
    cl, cr = sound_speed(rl, pl, gamma), sound_speed(rr, pr, gamma)
    return np.minimum(ul - cl, ur - cr), np.maximum(ul + cl, ur + cr)


def rusanov_flux(UL, UR, gamma=GAMMA):
    """Rusanov (local Lax-Friedrichs): central flux plus S_max/2 (U_R - U_L)."""
    s_left, s_right = davis_speeds(UL, UR, gamma)
    s_max = np.maximum(np.abs(s_left), np.abs(s_right))
    return 0.5 * (physical_flux(UL, gamma) + physical_flux(UR, gamma)) - 0.5 * s_max * (
        UR - UL
    )


def hll_flux(UL, UR, gamma=GAMMA):
    """HLL flux of Harten, Lax and van Leer (1983) with Davis wave speeds."""
    s_left, s_right = davis_speeds(UL, UR, gamma)
    FL, FR = physical_flux(UL, gamma), physical_flux(UR, gamma)
    middle = (s_right * FL - s_left * FR + s_left * s_right * (UR - UL)) / (
        s_right - s_left
    )
    return np.where(s_left >= 0, FL, np.where(s_right <= 0, FR, middle))


def hllc_flux(UL, UR, gamma=GAMMA):
    """HLLC flux of Toro, Spruce and Speares (1994) with Davis wave speeds."""
    s_left, s_right = davis_speeds(UL, UR, gamma)
    rl, ul, pl = primitive(UL, gamma)
    rr, ur, pr = primitive(UR, gamma)
    s_star = (pr - pl + rl * ul * (s_left - ul) - rr * ur * (s_right - ur)) / (
        rl * (s_left - ul) - rr * (s_right - ur)
    )

    def star(U, rho, u, p, s):
        factor = rho * (s - u) / (s - s_star)
        energy = U[2] / rho + (s_star - u) * (s_star + p / (rho * (s - u)))
        return factor * np.array([np.ones_like(rho), s_star, energy])

    FL, FR = physical_flux(UL, gamma), physical_flux(UR, gamma)
    F_star_left = FL + s_left * (star(UL, rl, ul, pl, s_left) - UL)
    F_star_right = FR + s_right * (star(UR, rr, ur, pr, s_right) - UR)
    return np.where(
        s_left >= 0,
        FL,
        np.where(s_star >= 0, F_star_left, np.where(s_right > 0, F_star_right, FR)),
    )


def roe_flux(UL, UR, gamma=GAMMA, entropy_fix=ROE_ENTROPY_FIX):
    """Roe (1981) flux with Harten's entropy fix on the acoustic waves.

    F = (F_L + F_R)/2 - 1/2 sum_k alpha_k |lambda_k| K_k with Roe-averaged
    eigenvalues lambda_k, eigenvectors K_k and wave strengths alpha_k.
    """
    rl, ul, pl = primitive(UL, gamma)
    rr, ur, pr = primitive(UR, gamma)
    hl = (UL[2] + pl) / rl
    hr = (UR[2] + pr) / rr
    wl, wr = np.sqrt(rl), np.sqrt(rr)
    u = (wl * ul + wr * ur) / (wl + wr)
    h = (wl * hl + wr * hr) / (wl + wr)
    c = np.sqrt((gamma - 1.0) * (h - 0.5 * u**2))
    dU = UR - UL
    alpha2 = (gamma - 1.0) / c**2 * (dU[0] * (h - u**2) + u * dU[1] - dU[2])
    alpha1 = (dU[0] * (u + c) - dU[1] - c * alpha2) / (2.0 * c)
    alpha3 = dU[0] - alpha1 - alpha2
    eigen = [u - c, u, u + c]
    vectors = [
        np.array([np.ones_like(u), u - c, h - u * c]),
        np.array([np.ones_like(u), u, 0.5 * u**2]),
        np.array([np.ones_like(u), u + c, h + u * c]),
    ]
    delta = entropy_fix * (np.abs(u) + c)
    dissipation = 0.0
    for k, (lam, alpha, vector) in enumerate(
        zip(eigen, (alpha1, alpha2, alpha3), vectors, strict=True)
    ):
        speed = np.abs(lam)
        if k != 1:  # Harten (1983): smooth |lambda| near zero for the acoustic waves
            speed = np.where(speed < delta, (lam**2 + delta**2) / (2 * delta), speed)
        dissipation = dissipation + alpha * speed * vector
    return (
        0.5 * (physical_flux(UL, gamma) + physical_flux(UR, gamma)) - 0.5 * dissipation
    )


FLUXES = {
    "exact": exact_flux,
    "rusanov": rusanov_flux,
    "hll": hll_flux,
    "hllc": hllc_flux,
    "roe": roe_flux,
}


# ------------------------------------------------------------ Godunov scheme
def max_wave_speed(U, gamma=GAMMA):
    rho, u, p = primitive(U, gamma)
    return float(np.max(np.abs(u) + sound_speed(rho, p, gamma)))


def godunov_step(U, flux, dt, dx, boundary="transmissive", gamma=GAMMA):
    """One first-order Godunov step; returns the new cell averages.

    Each face flux is added to one cell and subtracted from its neighbour, so
    the update conserves mass, momentum and energy up to boundary fluxes.
    """
    if boundary == "transmissive":  # zero-gradient ghost cells
        padded = np.concatenate([U[:, :1], U, U[:, -1:]], axis=1)
    elif boundary == "periodic":
        padded = np.concatenate([U[:, -1:], U, U[:, :1]], axis=1)
    else:
        raise ValueError(f"unknown boundary {boundary!r}")
    F = flux(padded[:, :-1], padded[:, 1:], gamma)  # faces i - 1/2, i = 0..n
    return U - dt / dx * (F[:, 1:] - F[:, :-1])


def initial_state(problem, n_cells, gamma=GAMMA):
    """Cell centres and cell averages of the shock-tube initial data on [0, 1]."""
    x = (np.arange(n_cells) + 0.5) / n_cells
    left = x < problem["x0"]
    prim = [np.where(left, a, b) for a, b in zip(problem["left"], problem["right"])]
    return x, conservative(*prim, gamma)


def solve(problem, solver, n_cells, cfl=CFL, gamma=GAMMA):
    """Run the first-order Godunov scheme to t_end; return x, U and step count."""
    x, U = initial_state(problem, n_cells, gamma)
    dx = 1.0 / n_cells
    flux = FLUXES[solver]
    t, steps, t_end = 0.0, 0, problem["t_end"]
    while t < t_end * (1 - 1e-12):
        courant = START_CFL if steps < START_STEPS else cfl
        dt = min(courant * dx / max_wave_speed(U, gamma), t_end - t)
        U = godunov_step(U, flux, dt, dx, gamma=gamma)
        if not np.all(np.isfinite(U)) or np.any(primitive(U, gamma)[2] <= 0):
            raise FloatingPointError(f"{solver} produced a non-physical state")
        t += dt
        steps += 1
    return x, U, steps


def l1_density_error(problem, solver, n_cells, gamma=GAMMA):
    """Mean |rho - rho_exact| over the cells (exact solution at cell centres)."""
    x, U, _ = solve(problem, solver, n_cells, gamma=gamma)
    rho_exact = exact_solution(problem, x, problem["t_end"], gamma)[0]
    return float(np.mean(np.abs(U[0] - rho_exact)))


def observed_rate(cells, errors):
    """Least-squares slope of log(error) against log(1/N)."""
    return float(-np.polyfit(np.log(cells), np.log(errors), 1)[0])


# ------------------------------------------------------------------ figures
def solution_figure(results, gamma=GAMMA):
    """Density and velocity for both problems, plus zooms on the Sod waves."""
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.5), constrained_layout=True)
    colors = dict(zip(SOLVERS, plt.cm.tab10.colors, strict=False))
    markers = dict(zip(SOLVERS, "osD^v", strict=True))
    x_exact = np.linspace(0.0, 1.0, N_EXACT)
    panels = [
        (axes[0, 0], "sod", 0, None, "Density"),
        (axes[0, 1], "sod", 0, (0.22, 0.52), "Density, rarefaction"),
        (axes[0, 2], "sod", 0, (0.62, 0.78), "Density, contact"),
        (axes[1, 0], "toro3", 0, None, "Density"),
        (axes[1, 1], "toro3", 0, (0.62, 0.84), "Density, contact and shock"),
        (axes[1, 2], "toro3", 1, None, "Velocity"),
    ]
    for ax, name, var, window, title in panels:
        problem = PROBLEMS[name]
        exact = exact_solution(problem, x_exact, problem["t_end"], gamma)
        ax.plot(x_exact, exact[var], color="black", lw=1.5, label="exact", zorder=5)
        for solver in SOLVERS:
            x, U = results[name][solver]
            q = primitive(U, gamma)[var]
            zoomed = window is not None
            ax.plot(
                x, q, marker=markers[solver] if zoomed else None, ms=4,
                lw=1.0, color=colors[solver], label=LABELS[solver],
            )  # fmt: skip
        if window is not None:
            ax.set_xlim(window)
            inside = (x_exact >= window[0]) & (x_exact <= window[1])
            low, high = exact[var][inside].min(), exact[var][inside].max()
            pad = 0.12 * (high - low)
            ax.set_ylim(low - pad, high + pad)
        ax.set_title(f"{problem['title']}: {title}")
        ax.set_xlabel("x [-]")
        ax.set_ylabel(r"$\rho$ [-]" if var == 0 else "u [-]")
        ax.grid(alpha=0.3)
    axes[0, 0].legend(loc="lower left", fontsize=9)
    fig.suptitle(
        f"First-order Godunov scheme, {N_CELLS} cells, CFL = {CFL}", fontsize=13
    )
    return fig


def convergence_figure(errors):
    """L1 density error against cell count for both problems."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    colors = dict(zip(SOLVERS, plt.cm.tab10.colors, strict=False))
    cells = np.array(N_REFINEMENT)
    for ax, name in zip(axes, PROBLEMS, strict=True):
        for solver in SOLVERS:
            e = errors[name][solver]
            rate = observed_rate(cells, e)
            ax.loglog(
                cells, e, "o-", color=colors[solver],
                label=f"{LABELS[solver]} (slope {rate:.2f})",
            )  # fmt: skip
        reference = errors[name]["hllc"][0] * (cells / cells[0]) ** -0.5
        ax.loglog(cells, reference, "k--", lw=1, label=r"$N^{-1/2}$")
        ax.set_title(f"{PROBLEMS[name]['title']}: L1 error in density")
        ax.set_xlabel("number of cells N [-]")
        ax.set_ylabel(r"$\|\rho - \rho_{exact}\|_1$ [-]")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=9)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for name, problem in PROBLEMS.items():
        p_star, u_star, iterations = star_state(problem["left"], problem["right"])
        print(
            f"{problem['title']}: p* = {float(p_star):.5f}, u* = {float(u_star):.5f} "
            f"({iterations} Newton iterations)"
        )
    results = {name: {} for name in PROBLEMS}
    errors = {name: {} for name in PROBLEMS}
    for name, problem in PROBLEMS.items():
        for solver in SOLVERS:
            x, U, _ = solve(problem, solver, N_CELLS)
            results[name][solver] = (x, U)
            errors[name][solver] = [
                l1_density_error(problem, solver, n) for n in N_REFINEMENT
            ]
    print(f"L1 density error, N = {N_REFINEMENT[0]} ... {N_REFINEMENT[-1]}:")
    for name in PROBLEMS:
        for solver in SOLVERS:
            e = errors[name][solver]
            print(
                f"  {name:6s} {LABELS[solver]:16s} N={N_CELLS}: "
                f"{e[N_REFINEMENT.index(N_CELLS)]:.4e}  "
                f"N={N_REFINEMENT[-1]}: {e[-1]:.4e}  "
                f"slope {observed_rate(N_REFINEMENT, e):.2f}"
            )
    finish_figures(
        {
            "riemann_solver_comparison.png": solution_figure(results),
            "riemann_solver_convergence.png": convergence_figure(errors),
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
