#!/usr/bin/env python3
"""Solve steady 2D laminar flow over a backward-facing step with SIMPLE.

The incompressible Navier-Stokes equations are discretised with the finite
volume method on a staggered (MAC) grid using first-order upwind convection
and central diffusion. Pressure and velocity are coupled with Patankar's SIMPLE
algorithm; every linear system is relaxed with Gauss-Seidel/SOR sweeps
compiled with Numba. A live figure shows the velocity magnitude with arrows,
the residual history and the global mass imbalance. The reattachment length of
the recirculation zone behind the step is printed at the end.
"""

import sys
import time
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
from numba import njit

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int, save_figure  # noqa: E402

DTYPE = np.float32


@dataclass
class Params:
    nx: int = 240  # pressure cells in x
    ny: int = 80  # pressure cells in y
    Re: float = 200.0  # Reynolds number rho*U_avg*H/mu
    H: float = 1.0  # inlet channel height
    h: float = 0.5  # step height
    step_length: float = 4.0  # length of the inlet channel above the step
    Lx: float = 24.0  # domain length
    Ly: float = 1.5  # domain height (= H + h)
    rho: float = 1.0  # density
    U_avg: float = 1.0  # mean inlet velocity
    alpha_u: float = 0.7  # momentum under-relaxation
    alpha_p: float = 0.3  # pressure under-relaxation
    omega_mom: float = 1.0  # SOR factor for the momentum sweeps
    omega_p: float = 1.7  # SOR factor for the pressure-correction sweeps
    mom_sweeps: int = 2
    pcor_sweeps: int = 40
    max_iters: int = 3000
    plot_interval: int = 20
    quiver_ds: int = 3  # plot every quiver_ds-th arrow


def build_geometry_masks(prm):
    """Return fluid masks for pressure cells, u faces and v faces plus grid."""
    nx, ny = prm.nx, prm.ny
    dx = DTYPE(prm.Lx / nx)
    dy = DTYPE(prm.Ly / ny)
    xP = (np.arange(nx, dtype=DTYPE) + DTYPE(0.5)) * dx
    yP = (np.arange(ny, dtype=DTYPE) + DTYPE(0.5)) * dy
    XP, YP = np.meshgrid(xP, yP, indexing="ij")
    fluid_P = np.ones((nx, ny), dtype=bool)
    fluid_P[(XP < prm.step_length) & (YP < prm.h)] = False
    fluid_u = np.zeros((nx + 1, ny), dtype=bool)
    fluid_u[1:nx, :] = fluid_P[:-1, :] & fluid_P[1:, :]
    fluid_u[0, :] = fluid_P[0, :]
    fluid_u[nx, :] = fluid_P[nx - 1, :]
    fluid_v = np.zeros((nx, ny + 1), dtype=bool)
    fluid_v[:, 1:ny] = fluid_P[:, :-1] & fluid_P[:, 1:]
    fluid_v[:, 0] = fluid_P[:, 0]
    fluid_v[:, ny] = fluid_P[:, ny - 1]
    return fluid_P, fluid_u, fluid_v, dx, dy, XP, YP


def inlet_parabolic_profile(y, h, H, U_avg=1.0):
    """Fully developed channel profile between y = h and y = h + H."""
    eta = (y - h) / H
    return (6.0 * U_avg * eta * (1.0 - eta)).astype(DTYPE)


def precompute_indices(mask):
    idx = np.argwhere(mask)
    return idx[:, 0].astype(np.int32), idx[:, 1].astype(np.int32)


@njit(cache=True)
def gs_sor_scalar(AW, AE, AS, AN, AP, b, phi, idx_i, idx_j, omega, sweeps):
    """SOR sweeps for AP*phi = AW*phi_W + AE*phi_E + AS*phi_S + AN*phi_N + b."""
    nx, ny = phi.shape
    for _ in range(sweeps):
        for k in range(idx_i.size):
            i = idx_i[k]
            j = idx_j[k]
            ap = AP[i, j]
            if ap == 0.0:
                continue
            nb = 0.0
            if i > 0:
                nb += AW[i, j] * phi[i - 1, j]
            if i < nx - 1:
                nb += AE[i, j] * phi[i + 1, j]
            if j > 0:
                nb += AS[i, j] * phi[i, j - 1]
            if j < ny - 1:
                nb += AN[i, j] * phi[i, j + 1]
            phi[i, j] += omega * ((b[i, j] + nb) / ap - phi[i, j])


@njit(cache=True)
def build_momentum_u(
    u, v, p, mu, rho, dx, dy, fluid_P, alpha_u, AW, AE, AS, AN, AP, b, idx_i, idx_j
):
    """Assemble the under-relaxed x-momentum equations on the u faces."""
    nxp1, ny = u.shape
    nx = nxp1 - 1
    De = mu * dy / dx
    Dn = mu * dx / dy
    AW[:] = 0.0
    AE[:] = 0.0
    AS[:] = 0.0
    AN[:] = 0.0
    AP[:] = 0.0
    b[:] = 0.0
    for k in range(idx_i.size):
        i = idx_i[k]
        j = idx_j[k]
        if i == 0 or i == nx:  # inlet / outlet faces are set by the BCs
            continue
        if (not fluid_P[i - 1, j]) or (not fluid_P[i, j]):
            AP[i, j] = 1.0  # face touches a solid cell: u = 0
            continue
        # mass fluxes through the faces of the u control volume
        fe = rho * 0.5 * (u[i, j] + u[i + 1, j]) * dy
        fw = rho * 0.5 * (u[i - 1, j] + u[i, j]) * dy
        fn = rho * 0.5 * (v[i - 1, j + 1] + v[i, j + 1]) * dx
        fs = rho * 0.5 * (v[i - 1, j] + v[i, j]) * dx
        aE = De + max(-fe, 0.0)
        aW = De + max(fw, 0.0)
        aN = Dn + max(-fn, 0.0)
        aS = Dn + max(fs, 0.0)
        aP = aE + aW + aN + aS + (fe - fw + fn - fs)
        # no-slip wall half a cell above/below: double the diffusion conductance
        if j == ny - 1 or ((not fluid_P[i - 1, j + 1]) and (not fluid_P[i, j + 1])):
            aP += Dn
            aN = 0.0
        if j == 0 or ((not fluid_P[i - 1, j - 1]) and (not fluid_P[i, j - 1])):
            aP += Dn
            aS = 0.0
        AP[i, j] = aP / alpha_u
        AW[i, j] = aW
        AE[i, j] = aE
        AS[i, j] = aS
        AN[i, j] = aN
        b[i, j] = (p[i - 1, j] - p[i, j]) * dy + (1.0 - alpha_u) / alpha_u * aP * u[
            i, j
        ]


@njit(cache=True)
def build_momentum_v(
    u, v, p, mu, rho, dx, dy, fluid_P, alpha_u, AW, AE, AS, AN, AP, b, idx_i, idx_j
):
    """Assemble the under-relaxed y-momentum equations on the v faces."""
    nx, nyp1 = v.shape
    ny = nyp1 - 1
    De = mu * dy / dx
    Dn = mu * dx / dy
    AW[:] = 0.0
    AE[:] = 0.0
    AS[:] = 0.0
    AN[:] = 0.0
    AP[:] = 0.0
    b[:] = 0.0
    for k in range(idx_i.size):
        i = idx_i[k]
        j = idx_j[k]
        if j == 0 or j == ny:  # bottom / top walls: v = 0
            continue
        if (not fluid_P[i, j - 1]) or (not fluid_P[i, j]):
            AP[i, j] = 1.0
            continue
        fe = rho * 0.5 * (u[i + 1, j - 1] + u[i + 1, j]) * dy
        fw = rho * 0.5 * (u[i, j - 1] + u[i, j]) * dy
        fn = rho * 0.5 * (v[i, j] + v[i, j + 1]) * dx
        fs = rho * 0.5 * (v[i, j - 1] + v[i, j]) * dx
        aE = De + max(-fe, 0.0)
        aW = De + max(fw, 0.0)
        aN = Dn + max(-fn, 0.0)
        aS = Dn + max(fs, 0.0)
        aP = aE + aW + aN + aS + (fe - fw + fn - fs)
        # inlet plane (v = 0) or vertical step face half a cell to the west
        if i == 0 or ((not fluid_P[i - 1, j - 1]) and (not fluid_P[i - 1, j])):
            aP += De
            aW = 0.0
        if i == nx - 1:  # outlet: zero normal gradient, v_E = v_P
            aP -= aE
            aE = 0.0
        AP[i, j] = aP / alpha_u
        AW[i, j] = aW
        AE[i, j] = aE
        AS[i, j] = aS
        AN[i, j] = aN
        b[i, j] = (p[i, j - 1] - p[i, j]) * dx + (1.0 - alpha_u) / alpha_u * aP * v[
            i, j
        ]


@njit(cache=True)
def momentum_residual(AW, AE, AS, AN, AP, b, phi, idx_i, idx_j):
    """Mean absolute residual of the assembled momentum equations."""
    nx, ny = phi.shape
    s = 0.0
    c = 0
    for k in range(idx_i.size):
        i = idx_i[k]
        j = idx_j[k]
        if AP[i, j] == 0.0 or AP[i, j] == 1.0 and b[i, j] == 0.0 and AE[i, j] == 0.0:
            continue
        r = b[i, j] - AP[i, j] * phi[i, j]
        if i > 0:
            r += AW[i, j] * phi[i - 1, j]
        if i < nx - 1:
            r += AE[i, j] * phi[i + 1, j]
        if j > 0:
            r += AS[i, j] * phi[i, j - 1]
        if j < ny - 1:
            r += AN[i, j] * phi[i, j + 1]
        s += abs(r)
        c += 1
    return s / max(c, 1)


def apply_velocity_bcs(u, v, prm, fluid_u, fluid_v, dy):
    """Inlet profile, zero-gradient outlet, no-slip walls, zero velocity in solids."""
    nx = u.shape[0] - 1
    ny = u.shape[1]
    y_c = (np.arange(ny, dtype=DTYPE) + DTYPE(0.5)) * dy
    open_rows = fluid_u[0, :]
    u[0, :] = 0.0
    u[0, open_rows] = inlet_parabolic_profile(y_c[open_rows], prm.h, prm.H, prm.U_avg)
    u[nx, :] = u[nx - 1, :]  # outlet: du/dx = 0
    v[:, 0] = 0.0  # bottom wall
    v[:, ny] = 0.0  # top wall
    u[~fluid_u] = 0.0
    v[~fluid_v] = 0.0
    np.clip(u, -5.0, 5.0, out=u)  # safety clamp against divergence
    np.clip(v, -5.0, 5.0, out=v)


def build_pressure_correction(
    u_star, v_star, APu, APv, prm, fluid_P, fluid_u, fluid_v, dx, dy
):
    """Assemble the SIMPLE pressure-correction equation.

    Returns (AW, AE, AS, AN, AP, b, du, dv) where du = dy/a_u and dv = dx/a_v
    are the velocity-correction coefficients (zero on boundary and solid faces).
    """
    nx, ny = fluid_P.shape
    rho = DTYPE(prm.rho)
    du = np.zeros_like(u_star)
    dv = np.zeros_like(v_star)
    mu_ = fluid_u.copy()
    mu_[0, :] = mu_[nx, :] = False
    mv_ = fluid_v.copy()
    mv_[:, 0] = mv_[:, ny] = False
    du[mu_] = dy / APu[mu_]
    dv[mv_] = dx / APv[mv_]

    AE = rho * dy * du[1:, :]
    AW = rho * dy * du[:-1, :]
    AN = rho * dx * dv[:, 1:]
    AS = rho * dx * dv[:, :-1]
    AP = AE + AW + AN + AS
    # b = mass imbalance of the predicted velocity field (inflow - outflow)
    b = -rho * (
        (u_star[1:, :] - u_star[:-1, :]) * dy + (v_star[:, 1:] - v_star[:, :-1]) * dx
    )
    for arr in (AW, AE, AS, AN, AP, b):
        arr[~fluid_P] = 0.0
    # pressure outlet: p' = 0 in the last column
    AW[-1, :] = AE[-1, :] = AS[-1, :] = AN[-1, :] = 0.0
    AP[-1, :] = 1.0
    b[-1, :] = 0.0
    return AW, AE, AS, AN, AP, b, du, dv


def correct_uvp(u, v, p, pcor, du, dv, alpha_p):
    """Apply the SIMPLE velocity and (under-relaxed) pressure corrections."""
    u[1:-1, :] += du[1:-1, :] * (pcor[:-1, :] - pcor[1:, :])
    v[:, 1:-1] += dv[:, 1:-1] * (pcor[:, :-1] - pcor[:, 1:])
    p += DTYPE(alpha_p) * pcor


def global_mass_imbalance(u, fluid_P, dy):
    nx = fluid_P.shape[0]
    inlet_flux = float(np.sum(u[0, :][fluid_P[0, :]]) * dy)
    outlet_flux = float(np.sum(u[nx, :][fluid_P[nx - 1, :]]) * dy)
    denom = abs(inlet_flux) if abs(inlet_flux) > 1e-12 else 1.0
    return abs(inlet_flux - outlet_flux) / denom, inlet_flux, outlet_flux


def reattachment_length(u, prm, dx):
    """Distance from the step to where the bottom-wall recirculation ends (in h).

    Looks at u in the first cell row (y = dy/2) downstream of the step and
    returns the first sign change from negative to positive, or None.
    """
    x_faces = np.arange(u.shape[0]) * dx
    row = u[:, 0].astype(float)
    down = x_faces > prm.step_length
    xs, us = x_faces[down], row[down]
    neg = np.nonzero(us < 0)[0]
    if neg.size == 0:
        return None
    for k in range(neg[0], len(us) - 1):
        if us[k] < 0 <= us[k + 1]:
            x_r = xs[k] - us[k] * (xs[k + 1] - xs[k]) / (us[k + 1] - us[k])
            return (x_r - prm.step_length) / prm.h
    return None


def cell_centre_velocity(u, v):
    Uc = DTYPE(0.5) * (u[:-1, :] + u[1:, :])
    Vc = DTYPE(0.5) * (v[:, :-1] + v[:, 1:])
    return Uc, Vc


def quiver_component(comp, fac, fluid_P, ds):
    """Scaled, subsampled velocity component with arrows hidden inside solids."""
    return np.where(fluid_P, comp * fac, np.nan)[::ds, ::ds]


def setup_plot(XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, params, interactive=True):
    if interactive:
        plt.ion()
    fig = plt.figure(figsize=(11, 8))
    gs = fig.add_gridspec(2, 2, height_ratios=[2.0, 1.0])
    ax0 = fig.add_subplot(gs[0, :])  # field
    ax1 = fig.add_subplot(gs[1, 0])  # residuals
    ax2 = fig.add_subplot(gs[1, 1])  # mass imbalance

    speed = np.sqrt(Uc**2 + Vc**2, dtype=DTYPE)
    speed_masked = ma.array(speed.T, mask=~fluid_P.T)
    dx_cell = float(XP[1, 0] - XP[0, 0])
    dy_cell = float(YP[0, 1] - YP[0, 0])
    im = ax0.imshow(
        speed_masked,
        origin="lower",
        extent=[0.0, float(XP.max()) + dx_cell / 2, 0.0, float(YP.max()) + dy_cell / 2],
        aspect="auto",
        cmap="viridis",
    )
    cbar = fig.colorbar(im, ax=ax0, fraction=0.046, pad=0.04)
    cbar.set_label("|U|")

    ds = params.quiver_ds
    # pre-scale velocities so the 95th percentile arrow is ~0.7 of a cell
    cell = min(dx_cell, dy_cell)
    ref = float(np.nanpercentile(speed[fluid_P], 95)) if np.any(fluid_P) else 1.0
    fac = min(max((0.7 * cell) / max(ref, 1e-6), 0.1), 1.5)  # same clamp as updates
    qv = ax0.quiver(
        XP[::ds, ::ds],
        YP[::ds, ::ds],
        quiver_component(Uc, fac, fluid_P, ds),
        quiver_component(Vc, fac, fluid_P, ds),
        color="white",
        scale=1.0,
        scale_units="xy",
        angles="xy",
        pivot="mid",
        width=0.0025,
        zorder=3,
    )
    ax0._qfac = fac  # remembered for the smoothed updates in update_plot

    ax0.set_title("Velocity magnitude with quiver (Backward-Facing Step)")
    ax0.set_xlabel("x")
    ax0.set_ylabel("y")
    ax0.set_xlim([0.0, params.Lx])
    ax0.set_ylim([0.0, params.Ly])
    im_vmax = max(1.0, float(speed_masked.max()))
    im.set_clim(vmin=0.0, vmax=im_vmax)
    ax0._im_vmax = im_vmax

    ax1.set_title("Residuals")
    ax1.set_yscale("log")
    (line_ru,) = ax1.plot(res_hist["u"], label="u-momentum")
    (line_rv,) = ax1.plot(res_hist["v"], label="v-momentum")
    (line_rp,) = ax1.plot(res_hist["p"], label="continuity")
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Mean |residual|")
    ax1.legend(loc="best")

    ax2.set_title("Global mass imbalance")
    imb_percent = np.clip(np.array(imb_hist, dtype=float), 1e-12, None) * 100.0
    (line_imb,) = ax2.plot(imb_percent)
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Imbalance (% of inlet)")
    ax2.set_yscale("log")
    set_imbalance_limits(ax2, imb_percent)

    fig.tight_layout()
    if interactive:
        fig.canvas.draw()
        plt.show(block=False)
        plt.pause(0.001)
    return fig, (ax0, ax1, ax2), im, qv, (line_ru, line_rv, line_rp), line_imb, ds


def set_imbalance_limits(ax, imb_percent):
    finite = imb_percent[np.isfinite(imb_percent)]
    if finite.size:
        ax.set_ylim(max(1e-6, 0.5 * finite.min()), max(1e-2, 2.0 * finite.max()))
    else:
        ax.set_ylim(1e-6, 1e2)


def update_plot(
    axs, im, qv, lines_res, line_imb, XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, ds
):
    speed = np.sqrt(Uc**2 + Vc**2, dtype=DTYPE)
    speed_masked = ma.array(speed.T, mask=~fluid_P.T)
    im.set_data(speed_masked)

    # smoothed (exponential moving average) colour limit
    ax0 = axs[0]
    new_max = max(1.0, float(speed_masked.max()))
    ax0._im_vmax = 0.9 * ax0._im_vmax + 0.1 * new_max
    im.set_clim(vmin=0.0, vmax=ax0._im_vmax)

    cell = min(float(XP[1, 0] - XP[0, 0]), float(YP[0, 1] - YP[0, 0]))
    ref = float(np.nanpercentile(speed[fluid_P], 95)) if np.any(fluid_P) else 1.0
    fac_new = (0.7 * cell) / max(ref, 1e-6)
    fac = min(max(0.9 * ax0._qfac + 0.1 * fac_new, 0.1 * cell), 1.5)
    ax0._qfac = fac
    qv.set_UVC(
        quiver_component(Uc, fac, fluid_P, ds), quiver_component(Vc, fac, fluid_P, ds)
    )

    for line, key in zip(lines_res, ("u", "v", "p")):
        line.set_data(np.arange(len(res_hist[key])), res_hist[key])
    axs[1].relim()
    axs[1].autoscale_view()

    imb_percent = np.clip(np.array(imb_hist, dtype=float), 1e-12, None) * 100.0
    line_imb.set_data(np.arange(len(imb_percent)), imb_percent)
    axs[2].relim()
    axs[2].autoscale_view()
    set_imbalance_limits(axs[2], imb_percent)


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument("--nx", type=int, default=240)
    parser.add_argument("--ny", type=int, default=80)
    parser.add_argument("--max-iters", type=int, default=3000)
    parser.add_argument("--plot-interval", type=int, default=20)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=None,
        help="run at most this many SIMPLE iterations (overrides --max-iters)",
    )
    parser.add_argument(
        "--throttle-ms",
        type=int,
        default=0,
        help="sleep this many ms every 5 iterations",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="quick demo: 120x40 grid, 400 iterations, plot every 5",
    )
    args = parser.parse_args(argv)

    plt.style.use("dark_background")
    if args.demo:
        nx, ny, max_iters, plot_interval = 120, 40, 400, 5
    else:
        nx, ny = args.nx, args.ny
        max_iters, plot_interval = args.max_iters, args.plot_interval
    if args.steps is not None:
        max_iters = args.steps
    interactive = not args.no_show

    prm = Params(nx=nx, ny=ny, max_iters=max_iters, plot_interval=plot_interval)
    fluid_P, fluid_u, fluid_v, dx, dy, XP, YP = build_geometry_masks(prm)

    p = np.zeros((prm.nx, prm.ny), dtype=DTYPE)
    u = np.zeros((prm.nx + 1, prm.ny), dtype=DTYPE)
    v = np.zeros((prm.nx, prm.ny + 1), dtype=DTYPE)
    mu = prm.rho * prm.U_avg * prm.H / prm.Re
    apply_velocity_bcs(u, v, prm, fluid_u, fluid_v, dy)

    res_hist = {"u": [], "v": [], "p": []}
    imb_hist = []
    if interactive:
        Uc, Vc = cell_centre_velocity(u, v)
        fig, axs, im, qv, lines_res, line_imb, ds = setup_plot(
            XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, prm
        )

    idx_u_i, idx_u_j = precompute_indices(fluid_u)
    idx_v_i, idx_v_j = precompute_indices(fluid_v)
    idx_p_i, idx_p_j = precompute_indices(fluid_P)

    AWu, AEu, ASu, ANu, APu, bu = (np.zeros_like(u) for _ in range(6))
    AWv, AEv, ASv, ANv, APv, bv = (np.zeros_like(v) for _ in range(6))
    u_star = u.copy()
    v_star = v.copy()
    pcor = np.zeros_like(p)
    ref_res = None
    start = time.time()
    it = 0

    for it in range(1, prm.max_iters + 1):
        # --- predictor: momentum equations with the current pressure ---
        build_momentum_u(
            u,
            v,
            p,
            mu,
            prm.rho,
            dx,
            dy,
            fluid_P,
            prm.alpha_u,
            AWu,
            AEu,
            ASu,
            ANu,
            APu,
            bu,
            idx_u_i,
            idx_u_j,
        )
        build_momentum_v(
            u,
            v,
            p,
            mu,
            prm.rho,
            dx,
            dy,
            fluid_P,
            prm.alpha_u,
            AWv,
            AEv,
            ASv,
            ANv,
            APv,
            bv,
            idx_v_i,
            idx_v_j,
        )
        ru = momentum_residual(AWu, AEu, ASu, ANu, APu, bu, u, idx_u_i, idx_u_j)
        rv = momentum_residual(AWv, AEv, ASv, ANv, APv, bv, v, idx_v_i, idx_v_j)
        np.copyto(u_star, u)
        np.copyto(v_star, v)
        gs_sor_scalar(
            AWu,
            AEu,
            ASu,
            ANu,
            APu,
            bu,
            u_star,
            idx_u_i,
            idx_u_j,
            prm.omega_mom,
            prm.mom_sweeps,
        )
        gs_sor_scalar(
            AWv,
            AEv,
            ASv,
            ANv,
            APv,
            bv,
            v_star,
            idx_v_i,
            idx_v_j,
            prm.omega_mom,
            prm.mom_sweeps,
        )
        apply_velocity_bcs(u_star, v_star, prm, fluid_u, fluid_v, dy)

        # --- pressure correction (p' = 0 at the outlet) ---
        AWp, AEp, ASp, ANp, APp, bp, du, dv = build_pressure_correction(
            u_star, v_star, APu, APv, prm, fluid_P, fluid_u, fluid_v, dx, dy
        )
        rp = float(np.mean(np.abs(bp[fluid_P])))  # continuity residual of u*
        pcor.fill(0.0)
        gs_sor_scalar(
            AWp,
            AEp,
            ASp,
            ANp,
            APp,
            bp,
            pcor,
            idx_p_i,
            idx_p_j,
            prm.omega_p,
            prm.pcor_sweeps,
        )

        # --- corrector ---
        np.copyto(u, u_star)
        np.copyto(v, v_star)
        correct_uvp(u, v, p, pcor, du, dv, prm.alpha_p)
        apply_velocity_bcs(u, v, prm, fluid_u, fluid_v, dy)

        # --- monitors ---
        res_hist["u"].append(ru)
        res_hist["v"].append(rv)
        res_hist["p"].append(rp)
        imb, _, _ = global_mass_imbalance(u, fluid_P, dy)
        imb_hist.append(imb)

        if it == 10:
            ref_res = [max(res_hist[k]) for k in ("u", "v", "p")]

        if it % 10 == 0 or it == 1:
            print(
                f"Iter {it:5d}: Ru={ru:.3e}, Rv={rv:.3e}, Rp={rp:.3e}, "
                f"MassImb={imb * 100:.2f}%"
            )

        if interactive and (it % prm.plot_interval == 0 or it == 1):
            Uc, Vc = cell_centre_velocity(u, v)
            update_plot(
                axs,
                im,
                qv,
                lines_res,
                line_imb,
                XP,
                YP,
                fluid_P,
                Uc,
                Vc,
                res_hist,
                imb_hist,
                ds,
            )
            fig.canvas.draw_idle()
            plt.pause(0.001)

        if ref_res is not None:
            drops = [
                res_hist[k][-1] / (r + 1e-30) for k, r in zip(("u", "v", "p"), ref_res)
            ]
            if max(drops) <= 1e-3 and imb <= 5e-3:
                print(
                    "Converged: residuals dropped >= 3 orders below their early "
                    "maximum and mass imbalance <= 0.5%."
                )
                break

        if args.throttle_ms > 0 and it % 5 == 0:
            time.sleep(args.throttle_ms / 1000.0)

    print(f"Finished at iter {it} in {time.time() - start:.1f}s.")
    x_r = reattachment_length(u, prm, dx)
    if x_r is None:
        print("No recirculation zone found on the bottom wall.")
    else:
        print(f"Bottom-wall reattachment length: x_r/h = {x_r:.2f} step heights")

    Uc, Vc = cell_centre_velocity(u, v)
    if interactive:
        update_plot(
            axs,
            im,
            qv,
            lines_res,
            line_imb,
            XP,
            YP,
            fluid_P,
            Uc,
            Vc,
            res_hist,
            imb_hist,
            ds,
        )
    else:
        fig, axs, im, qv, lines_res, line_imb, ds = setup_plot(
            XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, prm, interactive=False
        )

    if args.output:
        save_figure(fig, args.output, "backward_facing_step.png")
    if interactive:
        plt.ioff()
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
