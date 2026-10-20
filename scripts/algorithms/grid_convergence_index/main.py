"""Richardson extrapolation and the grid convergence index (GCI) on three meshes.

Implements the three-grid procedure of Celik et al. (2008): observed order p
by fixed-point iteration (valid for unequal refinement ratios), the
Richardson-extrapolated value and the fine-grid GCI with safety factor 1.25.
It is demonstrated on a computable case, the wall
gradient of a 1D advection-diffusion boundary-value problem solved with
second-order central differences (exact answer known), and on an illustrative
set of drag coefficients from three car meshes.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# 1D model problem: a u' = eps u'' on (0, 1), u(0) = 0, u(1) = 1.
ADVECTION_SPEED = 1.0  # a (m/s)
DIFFUSIVITY = 0.1  # eps (m^2/s); Peclet number a L / eps = 10
N_SEQUENCE = (4, 8, 16, 32, 64, 128, 256, 512, 1024)  # cells, refinement ratio 2
N_GCI = (16, 32, 64)  # coarse, medium, fine cells for the GCI triple

SAFETY_FACTOR = 1.25  # Fs for three-grid studies (Roache 1994)

# Illustrative drag study: cell counts and C_d on three meshes (fine first).
# These are example numbers of the kind a refinement study produces, not data
# from a specific vehicle.
CD_CELLS = (20.0e6, 7.5e6, 3.0e6)  # cells on fine, medium, coarse mesh
CD_VALUES = (0.3205, 0.3238, 0.3290)  # C_d on fine, medium, coarse mesh


def solve_advection_diffusion(n, a=ADVECTION_SPEED, eps=DIFFUSIVITY):
    """Solve a u' = eps u'' with central differences on n uniform cells.

    Returns the node coordinates and the discrete solution (n + 1 values).
    """
    h = 1.0 / n
    lower = -eps / h**2 - a / (2 * h)  # coefficient of u_{i-1}
    diag = 2 * eps / h**2  # coefficient of u_i
    upper = -eps / h**2 + a / (2 * h)  # coefficient of u_{i+1}
    m = n - 1  # interior unknowns
    ab = np.zeros((3, m))
    ab[0, 1:] = upper
    ab[1, :] = diag
    ab[2, :-1] = lower
    rhs = np.zeros(m)
    rhs[-1] = -upper * 1.0  # u(1) = 1 moved to the right-hand side
    u = np.concatenate(([0.0], solve_banded((1, 1), ab, rhs), [1.0]))
    return np.linspace(0.0, 1.0, n + 1), u


def wall_gradient(n, a=ADVECTION_SPEED, eps=DIFFUSIVITY):
    """Second-order one-sided estimate of du/dx at x = 1 (a skin-friction analogue)."""
    _, u = solve_advection_diffusion(n, a, eps)
    h = 1.0 / n
    return (3 * u[-1] - 4 * u[-2] + u[-3]) / (2 * h)


def exact_wall_gradient(a=ADVECTION_SPEED, eps=DIFFUSIVITY):
    """du/dx at x = 1 of u = (exp(a x / eps) - 1) / (exp(a / eps) - 1)."""
    pe = a / eps
    return pe / (1.0 - np.exp(-pe))


def observed_order(phi1, phi2, phi3, r21, r32, tol=1e-12, max_iter=200):
    """Observed order p from three solutions (1 = fine), Celik et al. (2008).

    Solves p = |ln|eps32 / eps21| + q(p)| / ln r21 with
    q(p) = ln((r21^p - s) / (r32^p - s)) and s = sign(eps32 / eps21) by
    fixed-point iteration. Returns (p, s); s = -1 means oscillatory convergence.
    """
    eps21 = phi2 - phi1
    eps32 = phi3 - phi2
    if eps21 == 0 or eps32 == 0:
        raise ValueError("two meshes give identical values; p is undefined")
    ratio = eps32 / eps21
    s = 1.0 if ratio > 0 else -1.0
    p = abs(np.log(abs(ratio))) / np.log(r21)
    for _ in range(max_iter):
        q = np.log((r21**p - s) / (r32**p - s))
        p_new = abs(np.log(abs(ratio)) + q) / np.log(r21)
        if abs(p_new - p) < tol:
            return p_new, s
        p = p_new
    return p, s


def richardson_extrapolate(phi1, phi2, r21, p):
    """Extrapolated value phi_ext = (r21^p phi1 - phi2) / (r21^p - 1)."""
    return (r21**p * phi1 - phi2) / (r21**p - 1.0)


def gci(phi_fine, phi_coarse, r, p, safety_factor=SAFETY_FACTOR):
    """Relative GCI of the finer of two meshes: Fs |e_a| / (r^p - 1)."""
    e_a = abs((phi_fine - phi_coarse) / phi_fine)
    return safety_factor * e_a / (r**p - 1.0)


def gci_study(phi, h, safety_factor=SAFETY_FACTOR):
    """Full three-grid study. ``phi`` and ``h`` are ordered fine, medium, coarse.

    Returns a dict with r21, r32, p, s, phi_ext, the approximate and
    extrapolated relative errors e_a21 and e_ext21, and GCI_fine (GCI_21).
    """
    phi1, phi2, phi3 = phi
    h1, h2, h3 = h
    r21, r32 = h2 / h1, h3 / h2
    p, s = observed_order(phi1, phi2, phi3, r21, r32)
    phi_ext = richardson_extrapolate(phi1, phi2, r21, p)
    gci21 = gci(phi1, phi2, r21, p, safety_factor)
    return {
        "r21": r21,
        "r32": r32,
        "p": p,
        "s": s,
        "phi_ext": phi_ext,
        "e_a21": abs((phi1 - phi2) / phi1),
        "e_ext21": abs((phi_ext - phi1) / phi_ext),
        "gci_fine": gci21,
    }


def representative_size(cells, dimension=3, volume=1.0):
    """Representative cell size h = (volume / cells)^(1/dimension)."""
    return (volume / np.asarray(cells, dtype=float)) ** (1.0 / dimension)


def local_orders(values, h):
    """Observed order of every consecutive triple of a refinement sequence.

    ``values`` and ``h`` run from coarse to fine; entry k uses meshes k, k+1, k+2
    and is plotted against the finest h of the triple.
    """
    return np.array(
        [
            observed_order(
                values[k + 2],
                values[k + 1],
                values[k],
                h[k + 1] / h[k + 2],
                h[k] / h[k + 1],
            )[0]
            for k in range(len(values) - 2)
        ]
    )


def bvp_study():
    """Convergence sequence plus the GCI triple for the model problem."""
    n_seq = np.array(N_SEQUENCE)
    g_seq = np.array([wall_gradient(n) for n in n_seq])
    n_fine_first = N_GCI[::-1]
    phi = [wall_gradient(n) for n in n_fine_first]
    h = [1.0 / n for n in n_fine_first]
    return n_seq, g_seq, phi, h, gci_study(phi, h)


def cd_study():
    """GCI for the illustrative drag coefficients."""
    h = representative_size(CD_CELLS)
    return h, gci_study(CD_VALUES, h)


def _gci_panel(ax, h, phi, res, exact=None, ylabel=""):
    """Solution against h with the extrapolated value and the fine-grid GCI band."""
    h = np.asarray(h)
    ax.plot(h / h[0], phi, "o-", color="tab:blue", markersize=8, label="three meshes")
    band = res["gci_fine"] * abs(phi[0])
    ax.errorbar(
        [1.0],
        [phi[0]],
        yerr=[band],
        color="tab:red",
        capsize=6,
        linewidth=2,
        label=f"fine value $\\pm$ GCI ({100 * res['gci_fine']:.2f}%)",
    )
    ax.plot(
        [0.0],
        [res["phi_ext"]],
        "*",
        color="tab:orange",
        markersize=16,
        label="Richardson extrapolation",
    )
    hh = np.linspace(0.0, h[-1] / h[0], 50)
    phi_fit = res["phi_ext"] + (phi[0] - res["phi_ext"]) * hh ** res["p"]
    ax.plot(
        hh, phi_fit, ":", color="tab:orange", label=f"$h^p$ fit, p = {res['p']:.2f}"
    )
    if exact is not None:
        ax.axhline(exact, color="k", linestyle="--", linewidth=1, label="exact value")
    ax.set_xlabel("Cell size relative to fine mesh $h / h_1$", fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="upper left")


def make_figure(bvp, cd):
    n_seq, g_seq, phi_b, h_b, res_b = bvp
    h_c, res_c = cd
    exact = exact_wall_gradient()
    fig, axes = plt.subplots(2, 2, figsize=(13, 10.5))

    _gci_panel(
        axes[0, 0],
        h_b,
        phi_b,
        res_b,
        exact=exact,
        ylabel="Wall gradient $du/dx$ at $x = 1$",
    )
    axes[0, 0].set_title(
        f"(a) Model problem, GCI on N = {N_GCI[0]}, {N_GCI[1]}, {N_GCI[2]} cells",
        fontsize=12,
    )
    axes[0, 0].legend(fontsize=9, loc="lower left")

    h_seq = 1.0 / n_seq
    err = np.abs(g_seq - exact)
    ax = axes[0, 1]
    ax.loglog(h_seq, err, "o-", color="tab:blue", label="|computed - exact|")
    ax.loglog(
        h_seq, err[-1] * (h_seq / h_seq[-1]) ** 2, "k--", label="slope 2 (formal order)"
    )
    gci_idx = [list(n_seq).index(n) for n in N_GCI]
    ax.loglog(
        h_seq[gci_idx],
        err[gci_idx],
        "s",
        color="tab:red",
        markersize=11,
        fillstyle="none",
        markeredgewidth=2,
        label="meshes used in (a)",
    )
    ax.set_xlabel("Cell size $h$ (domain length 1)", fontsize=11)
    ax.set_ylabel("Error in wall gradient", fontsize=11)
    ax.set_title("(b) Model problem, error against cell size", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower right")

    ax = axes[1, 0]
    p_local = local_orders(g_seq, h_seq)
    ax.semilogx(
        h_seq[2:],
        p_local,
        "o-",
        color="tab:blue",
        label="observed p, consecutive triples",
    )
    ax.axhline(2.0, color="k", linestyle="--", linewidth=1, label="formal order 2")
    ax.plot(
        [h_b[0]],
        [res_b["p"]],
        "s",
        color="tab:red",
        markersize=11,
        fillstyle="none",
        markeredgewidth=2,
        label=f"triple used in (a): p = {res_b['p']:.2f}",
    )
    ax.invert_xaxis()
    ax.set_xlabel(
        "Finest cell size of the triple $h_1$ (refining to the right)", fontsize=11
    )
    ax.set_ylabel("Observed order $p$", fontsize=11)
    ax.set_title("(c) Observed order approaches the formal order", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower right")

    _gci_panel(axes[1, 1], h_c, CD_VALUES, res_c, ylabel="Drag coefficient $C_d$")
    axes[1, 1].set_title(
        "(d) Illustrative $C_d$ on 20M, 7.5M and 3.0M cells", fontsize=12
    )
    axes[1, 1].legend(fontsize=9, loc="upper left")
    fig.tight_layout()
    return fig


def report(name, res):
    print(
        f"{name}: r21 = {res['r21']:.3f}, r32 = {res['r32']:.3f}, p = {res['p']:.3f}, "
        f"{'monotone' if res['s'] > 0 else 'oscillatory'}, phi_ext = {res['phi_ext']:.6f}, "
        f"e_a21 = {100 * res['e_a21']:.3f}%, e_ext21 = {100 * res['e_ext21']:.3f}%, "
        f"GCI_fine = {100 * res['gci_fine']:.3f}%"
    )


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    bvp = bvp_study()
    cd = cd_study()
    exact = exact_wall_gradient()
    print(f"Exact wall gradient: {exact:.6f}")
    for n, g in zip(bvp[0], bvp[1]):
        print(f"  N = {n:4d}: du/dx(1) = {g:.6f}, error = {abs(g - exact):.3e}")
    report("Model BVP", bvp[4])
    p_local = local_orders(bvp[1], 1.0 / bvp[0])
    print("  observed p of consecutive triples:", " ".join(f"{p:.3f}" for p in p_local))
    print(
        f"  true relative error of fine mesh = {100 * abs(bvp[2][0] - exact) / exact:.3f}%"
    )
    print(
        f"  true relative error of extrapolation = {100 * abs(bvp[4]['phi_ext'] - exact) / exact:.4f}%"
    )
    report("Illustrative C_d", cd[1])

    fig = make_figure(bvp, cd)
    finish_figures(
        {"grid_convergence_index.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
