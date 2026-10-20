"""Finite-volume solution of steady 1D convection-diffusion with five face schemes.

Solves d(rho u phi)/dx = d/dx(Gamma dphi/dx) on 0 < x < L with phi(0) = 1 and
phi(L) = 0, the test problem of Versteeg and Malalasekera (2007, Examples 5.1
to 5.4), on uniform cell-centred grids. The convective face value is taken
from central differencing, first-order upwind, hybrid, power law or QUICK.
The first four are assembled directly in Patankar's A(|Pe|) form; QUICK is
applied by deferred correction around the upwind matrix. The figure compares
coarse and fine solutions with the exponential exact solution and plots the
error against the number of cells with the observed orders.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

LENGTH = 1.0  # domain length L (m)
DENSITY = 1.0  # rho (kg/m^3)
DIFFUSIVITY = 0.1  # Gamma (kg/(m s))
PHI_LEFT = 1.0  # phi at x = 0 [-]
PHI_RIGHT = 0.0  # phi at x = L [-]

# Cases of Versteeg and Malalasekera Example 5.1: (velocity m/s, cells).
CASES = ((0.1, 5), (2.5, 5), (2.5, 20))
VELOCITY_STUDY = 2.5  # u for the grid-convergence study (m/s), Pe_L = 25
N_STUDY = (5, 10, 20, 40, 80, 160, 320, 640, 1280)  # cells, refinement ratio 2

DC_TOLERANCE = 1e-12  # deferred-correction stop: max |phi^k - phi^(k-1)|
DC_MAX_ITER = 500

SCHEMES = ("central", "upwind", "hybrid", "power law", "QUICK")
COLORS = {
    "central": "tab:red",
    "upwind": "tab:blue",
    "hybrid": "tab:green",
    "power law": "tab:purple",
    "QUICK": "tab:orange",
}
MARKERS = {
    "central": "o",
    "upwind": "s",
    "hybrid": "^",
    "power law": "v",
    "QUICK": "D",
}


def a_function(scheme, peclet):
    """Patankar's A(|Pe|): the diffusive weight of a face coefficient.

    The neighbour coefficient of a face with mass flux F and diffusion
    conductance D is a_E = D A(|Pe|) + max(-F, 0), with Pe = F / D.
    """
    p = np.abs(peclet)
    if scheme == "central":
        return 1.0 - 0.5 * p
    if scheme in ("upwind", "QUICK"):  # QUICK uses the upwind matrix
        return np.ones_like(p)
    if scheme == "hybrid":
        return np.maximum(0.0, 1.0 - 0.5 * p)
    if scheme == "power law":
        return np.maximum(0.0, (1.0 - 0.1 * p) ** 5)
    raise ValueError(f"unknown scheme {scheme!r}")


def exact_solution(x, velocity, gamma=DIFFUSIVITY, rho=DENSITY, length=LENGTH):
    """phi(x) = phi_0 + (phi_L - phi_0)(exp(rho u x / Gamma) - 1)/(exp(Pe_L) - 1)."""
    pe_l = rho * velocity * length / gamma
    shape = np.expm1(pe_l * np.asarray(x) / length) / np.expm1(pe_l)
    return PHI_LEFT + (PHI_RIGHT - PHI_LEFT) * shape


def quick_face_values(phi, flux, phi_left, phi_right):
    """QUICK value at every face (N + 1 faces) for a uniform mass flux.

    Interior faces use 6/8 phi_U + 3/8 phi_D - 1/8 phi_UU. A mirror node
    phi_ghost = 2 phi_b - phi_1 supplies phi_UU next to the inflow boundary,
    and the boundary faces take the prescribed boundary value.
    """
    ext = np.concatenate(([2 * phi_left - phi[0]], phi, [2 * phi_right - phi[-1]]))
    faces = np.empty(phi.size + 1)
    faces[0], faces[-1] = phi_left, phi_right
    left, right = ext[1:-2], ext[2:-1]  # cells on either side of interior faces
    if flux >= 0:
        far = ext[:-3]  # the cell upstream of the left cell
        faces[1:-1] = 0.75 * left + 0.375 * right - 0.125 * far
    else:
        far = ext[3:]
        faces[1:-1] = 0.75 * right + 0.375 * left - 0.125 * far
    return faces


def assemble(n, velocity, scheme, gamma=DIFFUSIVITY, rho=DENSITY, length=LENGTH):
    """Coefficients a_W, a_E, a_P, b of a_P phi_P = a_W phi_W + a_E phi_E + b.

    Interior faces use Patankar's form. A boundary face lies half a cell from
    its node, so its diffusion conductance is 2 Gamma / dx. Its convective value
    is the boundary value at an inflow boundary; at an outflow boundary it is the
    boundary value for central and QUICK and the upstream node for the
    upwind-type schemes, as in Versteeg and Malalasekera.
    """
    dx = length / n
    flux = rho * velocity  # F, the same on every face
    cond = gamma / dx  # D on interior faces
    cond_b = 2.0 * gamma / dx  # D on boundary faces
    pe = flux / cond
    a_face = cond * float(a_function(scheme, np.array(pe))) + max(-flux, 0.0)
    a_e = np.full(n, a_face)
    a_w = np.full(n, a_face + flux)  # a_W = a_E + F on a uniform grid
    a_w[0] = a_e[-1] = 0.0
    # An interior east face adds F + a_E to a_P, an interior west face adds a_E.
    a_p = np.full(n, 2.0 * a_face + flux)
    a_p[0] -= a_face
    a_p[-1] -= a_face + flux
    b = np.zeros(n)
    upwind_type = scheme not in ("central", "QUICK")

    # West boundary face: flux in +x is F phi_conv - D_b (phi_1 - phi_left).
    if flux >= 0 or not upwind_type:
        a_p[0] += cond_b
        b[0] += (cond_b + flux) * PHI_LEFT
    else:  # outflow, upwind value phi_1
        a_p[0] += cond_b - flux
        b[0] += cond_b * PHI_LEFT
    # East boundary face: flux in +x is F phi_conv - D_b (phi_right - phi_N).
    if flux <= 0 or not upwind_type:
        a_p[-1] += cond_b
        b[-1] += (cond_b - flux) * PHI_RIGHT
    else:  # outflow, upwind value phi_N
        a_p[-1] += cond_b + flux
        b[-1] += cond_b * PHI_RIGHT
    return a_w, a_e, a_p, b, dx, flux


def tridiagonal_solve(a_w, a_e, a_p, b):
    """Solve a_P phi_P - a_W phi_W - a_E phi_E = b with a banded solver."""
    n = a_p.size
    ab = np.zeros((3, n))
    ab[0, 1:] = -a_e[:-1]
    ab[1, :] = a_p
    ab[2, :-1] = -a_w[1:]
    return solve_banded((1, 1), ab, b)


def solve(n, velocity, scheme, gamma=DIFFUSIVITY, rho=DENSITY, length=LENGTH):
    """Cell-centre coordinates, solution and deferred-correction iterations."""
    a_w, a_e, a_p, b, dx, flux = assemble(n, velocity, scheme, gamma, rho, length)
    x = (np.arange(n) + 0.5) * dx
    phi = tridiagonal_solve(a_w, a_e, a_p, b)
    if scheme != "QUICK":
        return x, phi, 0
    # Deferred correction: upwind implicit, (QUICK - upwind) face flux explicit.
    for k in range(1, DC_MAX_ITER + 1):
        faces_q = quick_face_values(phi, flux, PHI_LEFT, PHI_RIGHT)
        ext = np.concatenate(([PHI_LEFT], phi, [PHI_RIGHT]))
        faces_u = ext[:-1] if flux >= 0 else ext[1:]
        faces_u[0], faces_u[-1] = PHI_LEFT, PHI_RIGHT  # boundary faces are exact
        corr = flux * (faces_q - faces_u)  # correction flux in +x on every face
        rhs = b - (corr[1:] - corr[:-1])
        phi_new = tridiagonal_solve(a_w, a_e, a_p, rhs)
        change = np.max(np.abs(phi_new - phi))
        phi = phi_new
        if change < DC_TOLERANCE:
            return x, phi, k
    raise RuntimeError("deferred correction did not converge")


def face_fluxes(n, velocity, scheme, phi):
    """Total flux J (convective + diffusive, in +x) on all N + 1 faces.

    Uses exactly the face formulas of `assemble`, so a converged solution has
    the same J on every face: the discrete statement of conservation.
    """
    dx = LENGTH / n
    flux = DENSITY * velocity
    cond, cond_b = DIFFUSIVITY / dx, 2.0 * DIFFUSIVITY / dx
    left, right = phi[:-1], phi[1:]
    j = np.empty(n + 1)
    if scheme == "QUICK":
        faces = quick_face_values(phi, flux, PHI_LEFT, PHI_RIGHT)
        j[1:-1] = flux * faces[1:-1] - cond * (right - left)
    else:
        a_face = cond * float(a_function(scheme, np.array(flux / cond)))
        a_face += max(-flux, 0.0)
        j[1:-1] = flux * left + a_face * (left - right)
    upwind_type = scheme not in ("central", "QUICK")
    conv_w = PHI_LEFT if (flux >= 0 or not upwind_type) else phi[0]
    conv_e = PHI_RIGHT if (flux <= 0 or not upwind_type) else phi[-1]
    j[0] = flux * conv_w - cond_b * (phi[0] - PHI_LEFT)
    j[-1] = flux * conv_e - cond_b * (PHI_RIGHT - phi[-1])
    return j


def rms_error(n, velocity, scheme):
    x, phi, _ = solve(n, velocity, scheme)
    return np.sqrt(np.mean((phi - exact_solution(x, velocity)) ** 2))


def convergence_study(velocity=VELOCITY_STUDY, n_values=N_STUDY):
    """RMS error at cell centres for every scheme and grid."""
    n_values = np.array(n_values)
    return n_values, {
        s: np.array([rms_error(n, velocity, s) for n in n_values]) for s in SCHEMES
    }


def observed_orders(n_values, errors):
    """p = log2(e_k / e_(k+1)) for consecutive grids of ratio 2."""
    return np.log(errors[:-1] / errors[1:]) / np.log(n_values[1:] / n_values[:-1])


def _solution_panel(ax, velocity, n, title):
    xf = np.linspace(0.0, LENGTH, 400)
    ax.plot(xf, exact_solution(xf, velocity), "k-", linewidth=2, label="exact")
    for scheme in SCHEMES:
        if scheme == "power law":
            continue  # indistinguishable from hybrid on these grids
        x, phi, _ = solve(n, velocity, scheme)
        ax.plot(
            x,
            phi,
            linestyle="--",
            marker=MARKERS[scheme],
            color=COLORS[scheme],
            markersize=7,
            linewidth=1.2,
            label=scheme,
        )
    pe_cell = DENSITY * velocity * (LENGTH / n) / DIFFUSIVITY
    ax.set_title(
        f"{title}\nu = {velocity} m/s, N = {n}, " + r"$Pe_\Delta$" + f" = {pe_cell:g}",
        fontsize=12,
    )
    ax.set_xlabel("x [m]", fontsize=11)
    ax.set_ylabel(r"$\phi$ [-]", fontsize=11)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)


def make_figure(study):
    n_values, errors = study
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.2))
    _solution_panel(axes[0], 2.5, 5, "(a) Coarse grid")
    axes[0].legend(fontsize=9, loc="lower left")
    _solution_panel(axes[1], 2.5, 20, "(b) Refined grid, outlet layer")
    axes[1].set_xlim(0.5, 1.0)
    axes[1].legend(fontsize=9, loc="lower left")

    ax = axes[2]
    for scheme in SCHEMES:
        p = observed_orders(n_values, errors[scheme])[-1]
        ax.loglog(
            n_values,
            errors[scheme],
            marker=MARKERS[scheme],
            color=COLORS[scheme],
            label=f"{scheme} (p = {p:.2f})",
        )
    ref = errors["upwind"][-1]
    ax.loglog(
        n_values, ref * (n_values[-1] / n_values), "k:", linewidth=1, label="slope 1"
    )
    ref2 = errors["central"][-1]
    ax.loglog(
        n_values,
        ref2 * (n_values[-1] / n_values) ** 2,
        "k--",
        linewidth=1,
        label="slope 2",
    )
    ax.axvline(
        DENSITY * VELOCITY_STUDY * LENGTH / (2 * DIFFUSIVITY),
        color="gray",
        linewidth=1,
    )
    ax.text(13.5, 3e-1, r"$Pe_\Delta = 2$", color="gray", fontsize=10, ha="left")
    ax.set_xlabel("Number of cells N [-]", fontsize=11)
    ax.set_ylabel(r"RMS error of $\phi$ at cell centres [-]", fontsize=11)
    ax.set_title(
        f"(c) Error against N, u = {VELOCITY_STUDY} m/s\n(p from the two finest grids)",
        fontsize=12,
    )
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower left")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for velocity, n in CASES:
        pe = DENSITY * velocity * (LENGTH / n) / DIFFUSIVITY
        print(f"u = {velocity} m/s, N = {n}, Pe_cell = {pe:g}")
        x, _, _ = solve(n, velocity, "central")
        print("  x       " + " ".join(f"{xi:8.3f}" for xi in x))
        print("  exact   " + " ".join(f"{v:8.4f}" for v in exact_solution(x, velocity)))
        for scheme in SCHEMES:
            _, phi, iters = solve(n, velocity, scheme)
            extra = f"  ({iters} DC iterations)" if iters else ""
            print(f"  {scheme:8s}" + " ".join(f"{v:8.4f}" for v in phi) + extra)

    study = convergence_study()
    n_values, errors = study
    print(f"RMS error against N at u = {VELOCITY_STUDY} m/s (Pe_L = 25)")
    for scheme in SCHEMES:
        orders = observed_orders(n_values, errors[scheme])
        print(
            f"  {scheme:9s} e(N={n_values[-1]}) = {errors[scheme][-1]:.3e}, "
            "observed p: " + " ".join(f"{p:5.2f}" for p in orders)
        )

    fig = make_figure(study)
    finish_figures(
        {"fvm_convection_diffusion_1d.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
