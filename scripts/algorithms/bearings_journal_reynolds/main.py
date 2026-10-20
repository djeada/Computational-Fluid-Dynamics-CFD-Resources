"""Pressure and load capacity of a hydrodynamic journal bearing from the Reynolds equation.

The steady Reynolds equation for an incompressible film between a journal
rotating at omega and a stationary bearing is written in the non-dimensional
form d/dtheta(H^3 dP/dtheta) + d/dzeta(H^3 dP/dzeta) = 6 dH/dtheta with
H = 1 + eps cos(theta) and P = p c^2 / (mu omega R^2). It is discretised with
conservative central differences on a grid periodic in theta.

Three cases are solved: the infinitely long bearing without cavitation (the
full-Sommerfeld solution, checked against its closed form); the long bearing
with the Reynolds (Swift-Stieber) cavitation condition, posed as the linear
complementarity problem P >= 0 and solved by a primal-dual active-set method;
and the finite bearing with L/D = 1 under the same condition. The script plots
pressure against angle for several eccentricity ratios, the Sommerfeld number
against eccentricity ratio for each model together with the short-bearing
(Ocvirk) formula and the Raimondi-Boyd design table, and the 2D pressure field.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_THETA = 144  # grid points around the bearing
N_AXIAL = 41  # grid points across the length of the finite bearing (incl. edges)
LENGTH_OVER_DIAMETER = 1.0  # L/D of the finite bearing
PROFILE_ECCENTRICITIES = (0.2, 0.4, 0.6, 0.8)  # eps = e/c of the pressure plots
CURVE_ECCENTRICITIES = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.97)
FIELD_ECCENTRICITY = 0.6  # eps of the 2D pressure field

# Raimondi and Boyd (1958), full 360 deg journal bearing, L/D = 1:
# eccentricity ratio, Sommerfeld number, attitude angle (deg).
RAIMONDI_BOYD_LD1 = np.array(
    [
        [0.1, 1.33, 79.5],
        [0.2, 0.631, 74.02],
        [0.4, 0.264, 63.10],
        [0.6, 0.121, 50.58],
        [0.8, 0.0446, 36.24],
        [0.9, 0.0188, 26.45],
        [0.97, 0.00474, 15.47],
    ]
)


def film(theta, eps):
    """Non-dimensional film thickness H = h/c, theta measured from h_max."""
    return 1.0 + eps * np.cos(theta)


def sommerfeld_pressure(theta, eps):
    """Closed-form full-Sommerfeld pressure P = p c^2 / (mu omega R^2), long bearing."""
    return (
        6 * eps * np.sin(theta) * (2 + eps * np.cos(theta))
        / ((2 + eps**2) * (1 + eps * np.cos(theta)) ** 2)
    )  # fmt: skip


def sommerfeld_number_full(eps):
    """S = (2 + eps^2) sqrt(1 - eps^2) / (12 pi^2 eps), full-Sommerfeld long bearing."""
    return (2 + eps**2) * np.sqrt(1 - eps**2) / (12 * np.pi**2 * eps)


def sommerfeld_number_short(eps, l_over_d):
    """Short-bearing (Ocvirk) Sommerfeld number with half-Sommerfeld cavitation.

    S (L/D)^2 = (1 - eps^2)^2 / (pi eps sqrt(pi^2 (1 - eps^2) + 16 eps^2)).
    """
    root = np.sqrt(np.pi**2 * (1 - eps**2) + 16 * eps**2)
    return (1 - eps**2) ** 2 / (np.pi * eps * root) / l_over_d**2


def assemble(eps, n_theta, n_axial=None, l_over_r=None):
    """Matrix A of -div(H^3 grad P) and right-hand side b = -6 dH/dtheta.

    Unknowns are ordered theta-fastest. In 1D (n_axial is None) the grid has
    n_theta points; in 2D it has n_theta x (n_axial - 2) interior points with
    P = 0 on the two bearing edges. Fluxes use H at the cell faces, so the
    scheme is conservative. Returns (A, b, theta, zeta).
    """
    dth = 2 * np.pi / n_theta
    theta = np.arange(n_theta) * dth
    h_east = film(theta + 0.5 * dth, eps) ** 3
    h_west = film(theta - 0.5 * dth, eps) ** 3
    # Source: 6 dH/dtheta integrated over the cell, divided by dtheta.
    source = 6 * (film(theta + 0.5 * dth, eps) - film(theta - 0.5 * dth, eps)) / dth
    if n_axial is None:
        n_z, zeta, dz = 1, np.zeros(1), None
    else:
        zeta_all = np.linspace(-0.5 * l_over_r, 0.5 * l_over_r, n_axial)
        zeta, dz = zeta_all[1:-1], zeta_all[1] - zeta_all[0]
        n_z = zeta.size
    rows, cols, vals = [], [], []
    idx = np.arange(n_theta * n_z).reshape(n_z, n_theta)
    for k in range(n_z):
        i = idx[k]
        ie, iw = np.roll(i, -1), np.roll(i, 1)
        diag = (h_east + h_west) / dth**2
        rows += [i, i, i]
        cols += [i, ie, iw]
        vals += [diag, -h_east / dth**2, -h_west / dth**2]
        if n_axial is not None:
            h3 = film(theta, eps) ** 3  # H does not vary along the axis
            rows.append(i)
            cols.append(i)
            vals.append(2 * h3 / dz**2)
            for kk in (k - 1, k + 1):
                if 0 <= kk < n_z:  # neighbours on the edges are P = 0
                    rows.append(i)
                    cols.append(idx[kk])
                    vals.append(-h3 / dz**2)
    n = n_theta * n_z
    a = coo_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(n, n),
    ).tocsr()
    b = -np.tile(source, n_z)
    return a, b, theta, zeta


def fix_supply_line(a, b, n_theta, n_z):
    """Impose P = 0 on the line theta = 0 (axial supply groove at h_max)."""
    a = a.tolil()
    for k in range(n_z):
        row = k * n_theta
        a.rows[row], a.data[row] = [row], [1.0]
        b[row] = 0.0
    return a.tocsr(), b


def solve_lcp(a, b, max_iter=500):
    """Solve A P = b with P >= 0, A P - b >= 0, P (A P - b) = 0 by primal-dual active set.

    Each iteration solves the linear system with P = 0 on the current
    cavitated set and moves points in or out of it by the sign of P and of the
    multiplier A P - b. The cavitation front moves by about one grid point per
    iteration, so the unconstrained (full-Sommerfeld) solution is used as the
    starting guess. Returns (P, iterations).
    """
    n = b.size
    tol = 1e-10 * np.abs(b).max()  # ignores round-off on the P = 0 supply line
    cavitated = spsolve(a.tocsc(), b) < -tol  # start from the unconstrained solution
    for it in range(1, max_iter + 1):
        free = ~cavitated
        p = np.zeros(n)
        p[free] = spsolve(a[free][:, free].tocsc(), b[free])
        multiplier = a @ p - b
        multiplier[free] = 0.0
        new = (multiplier - p) > tol
        if np.array_equal(new, cavitated):
            return p, it
        cavitated = new
    raise RuntimeError("active-set iteration did not converge")


def solve_long(eps, n_theta=N_THETA, cavitation=True):
    """Pressure P(theta) of the infinitely long bearing."""
    a, b, theta, _ = assemble(eps, n_theta)
    a, b = fix_supply_line(a, b, n_theta, 1)
    p = solve_lcp(a, b)[0] if cavitation else spsolve(a.tocsc(), b)
    return theta, p


def solve_finite(eps, l_over_d=LENGTH_OVER_DIAMETER, n_theta=N_THETA, n_axial=N_AXIAL):
    """Pressure P(theta, zeta) of a finite bearing with Reynolds cavitation."""
    l_over_r = 2 * l_over_d
    a, b, theta, zeta = assemble(eps, n_theta, n_axial, l_over_r)
    a, b = fix_supply_line(a, b, n_theta, zeta.size)
    p, _ = solve_lcp(a, b)
    return theta, zeta, p.reshape(zeta.size, n_theta)


def load_components(theta, p, dzeta=None):
    """Integrals of P cos(theta) and P sin(theta) over the film (trapezoid in zeta).

    For a 1D profile they are per unit length in units of mu omega R^3 / c^2;
    for a 2D field (rows = axial stations) in units of mu omega R^4 / c^2.
    """
    dth = theta[1] - theta[0]
    if p.ndim == 1:
        return np.sum(p * np.cos(theta)) * dth, np.sum(p * np.sin(theta)) * dth
    # Interior rows only; the edges have P = 0 and add nothing.
    return (
        np.sum(p * np.cos(theta)) * dth * dzeta,
        np.sum(p * np.sin(theta)) * dth * dzeta,
    )


def sommerfeld_and_attitude(theta, p, l_over_r=None, dzeta=None):
    """Sommerfeld number S = mu N L D / W (R/c)^2 and attitude angle (deg).

    With W = I mu omega R^3 / c^2 per unit length (1D) or I mu omega R^4 / c^2
    (2D), S = 1/(pi I) for the long bearing and S = (L/R)/(pi I) for the finite one.
    """
    wc, ws = load_components(theta, p, dzeta)
    total = np.hypot(wc, ws)
    s = 1 / (np.pi * total) if l_over_r is None else l_over_r / (np.pi * total)
    return s, np.degrees(np.arctan2(abs(ws), abs(wc)))


def curves():
    """Sommerfeld number and attitude angle against eps for every model."""
    eps = np.array(CURVE_ECCENTRICITIES)
    long_full = np.array(
        [sommerfeld_and_attitude(*solve_long(e, cavitation=False)) for e in eps]
    )
    long_rey = np.array([sommerfeld_and_attitude(*solve_long(e)) for e in eps])
    finite = []
    l_over_r = 2 * LENGTH_OVER_DIAMETER
    for e in eps:
        theta, zeta, p = solve_finite(e)
        finite.append(sommerfeld_and_attitude(theta, p, l_over_r, zeta[1] - zeta[0]))
    return eps, long_full, long_rey, np.array(finite)


def make_figure(curve_data):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), constrained_layout=True)
    colors = ("tab:blue", "tab:orange", "tab:green", "tab:red")
    fine = np.linspace(0, 2 * np.pi, 721)

    ax = axes[0, 0]
    for e, col in zip(PROFILE_ECCENTRICITIES, colors, strict=True):
        ax.plot(
            np.degrees(fine),
            sommerfeld_pressure(fine, e),
            color=col,
            label=rf"$\varepsilon$ = {e}",
        )
        theta, p = solve_long(e, cavitation=False)
        ax.plot(np.degrees(theta[::4]), p[::4], "o", color=col, ms=3.5)
    ax.plot([], [], "k-", label="closed form")
    ax.plot([], [], "ko", ms=3.5, label="finite differences")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.set_title("(a) Long bearing without cavitation (full Sommerfeld)")
    ax.set_ylabel(r"$P = p\,c^2/(\mu\omega R^2)$")

    ax = axes[0, 1]
    for e, col in zip(PROFILE_ECCENTRICITIES, colors, strict=True):
        theta, p = solve_long(e)
        ax.plot(np.degrees(theta), p, color=col, label=rf"$\varepsilon$ = {e}, long")
        theta, zeta, pf = solve_finite(e)
        ax.plot(np.degrees(theta), pf[zeta.size // 2], color=col, ls="--")
    ax.plot([], [], "k--", label="L/D = 1, mid-plane")
    ax.set_title("(b) Reynolds cavitation condition, P ≥ 0")
    ax.set_ylabel(r"$P = p\,c^2/(\mu\omega R^2)$")
    for ax in axes[0]:
        ax.set_xlabel(r"angle from maximum film $\theta$ (deg)")
        ax.set_xlim(0, 360)
        ax.set_xticks(range(0, 361, 60))
        ax.grid(alpha=0.3)
        ax.legend(fontsize=9, loc="upper left")

    ax = axes[1, 0]
    eps, long_full, long_rey, finite = curve_data
    e_fine = np.linspace(0.05, 0.97, 200)
    ax.semilogy(
        e_fine,
        sommerfeld_number_full(e_fine),
        color="tab:blue",
        label="long, full Sommerfeld (closed form)",
    )
    ax.semilogy(
        eps,
        long_full[:, 0],
        "o",
        color="tab:blue",
        ms=5,
        mfc="none",
        label="long, full Sommerfeld (FD)",
    )
    ax.semilogy(
        eps,
        long_rey[:, 0],
        "s-",
        color="tab:orange",
        ms=5,
        label="long, Reynolds condition (FD)",
    )
    ax.semilogy(
        eps,
        finite[:, 0],
        "^-",
        color="tab:green",
        ms=6,
        label="L/D = 1, Reynolds condition (FD)",
    )
    ax.semilogy(
        e_fine, sommerfeld_number_short(e_fine, LENGTH_OVER_DIAMETER),
        color="tab:purple", ls="--", label="short bearing (Ocvirk), L/D = 1",
    )  # fmt: skip
    rb = RAIMONDI_BOYD_LD1
    ax.semilogy(
        rb[:, 0], rb[:, 1], "kx", ms=8, mew=2, label="Raimondi–Boyd table, L/D = 1"
    )
    ax.set_xlabel(r"eccentricity ratio $\varepsilon = e/c$")
    ax.set_ylabel(r"Sommerfeld number $S = (\mu N / P)(R/c)^2$")
    ax.set_title("(c) Load capacity: lower S means more load at given speed")
    ax.set_xlim(0, 1)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8.5, loc="lower left")

    ax = axes[1, 1]
    theta, zeta, p = solve_finite(FIELD_ECCENTRICITY)
    th = np.degrees(np.append(theta, 2 * np.pi))
    z_all = np.concatenate(
        ([zeta[0] - (zeta[1] - zeta[0])], zeta, [zeta[-1] + (zeta[1] - zeta[0])])
    )
    p_all = np.zeros((z_all.size, th.size))
    p_all[1:-1, :-1] = np.maximum(p, 0.0)
    p_all[1:-1, -1] = p_all[1:-1, 0]
    levels = MaxNLocator(16).tick_values(0.0, p_all.max())
    cs = ax.contourf(
        th, z_all / (2 * LENGTH_OVER_DIAMETER), p_all, levels=levels, cmap="viridis"
    )
    fig.colorbar(cs, ax=ax, label=r"$P = p\,c^2/(\mu\omega R^2)$")
    ax.set_xlabel(r"angle from maximum film $\theta$ (deg)")
    ax.set_ylabel("axial position z / L")
    ax.set_xticks(range(0, 361, 60))
    ax.set_title(
        rf"(d) Pressure field, L/D = {LENGTH_OVER_DIAMETER:g}, $\varepsilon$ = {FIELD_ECCENTRICITY}"
    )
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for e in PROFILE_ECCENTRICITIES:
        theta, p = solve_long(e, cavitation=False)
        err = (
            np.abs(p - sommerfeld_pressure(theta, e)).max()
            / sommerfeld_pressure(theta, e).max()
        )
        print(f"eps = {e}: full-Sommerfeld FD max error {err:.1e} of peak pressure")
    data = curves()
    eps, long_full, long_rey, finite = data
    print(" eps   S_full  S_long_Rey  S_L/D=1  phi_L/D=1  S_short")
    for k, e in enumerate(eps):
        print(
            f"{e:4.2f}  {long_full[k, 0]:.4f}  {long_rey[k, 0]:.4f}      "
            f"{finite[k, 0]:.4f}   {finite[k, 1]:5.1f}     "
            f"{sommerfeld_number_short(e, LENGTH_OVER_DIAMETER):.4f}"
        )

    finish_figures(
        {"bearings_journal_reynolds.png": make_figure(data)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
