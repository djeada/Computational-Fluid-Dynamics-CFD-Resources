#!/usr/bin/env python3
import argparse, time, os
from dataclasses import dataclass
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

# limit NumPy BLAS threads (keeps CPU from pegging all cores)
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
plt.style.use("dark_background")

# ---- use float32 everywhere ----
DTYPE = np.float32
FZERO = DTYPE(0.0)
FONE = DTYPE(1.0)
FBIG = DTYPE(1e10)  # safe "infinity" for float32
FSIX = DTYPE(6.0)
FHALF = DTYPE(0.5)
FMINUS_FIVE = DTYPE(-5.0)
FFIVE = DTYPE(5.0)


@dataclass
class Params:
    nx: int = 240
    ny: int = 80
    Re: float = 200.0
    H: float = 1.0
    h: float = 0.5
    Lx: float = 24.0
    Ly: float = 1.5
    rho: float = 1.0
    alpha_u: float = 0.2
    alpha_p: float = 0.3
    omega_mom: float = 1.0
    omega_p: float = 1.5
    mom_sweeps: int = 1
    pcor_sweeps: int = 40
    max_iters: int = 3000
    plot_interval: int = 20
    quiver_ds: int = 3
    seed: int = 0


def build_geometry_masks(nx, ny, Lx, Ly, H, h):
    dx = DTYPE(Lx / nx)
    dy = DTYPE(Ly / ny)
    xP = (np.arange(nx, dtype=DTYPE) + DTYPE(0.5)) * dx
    yP = (np.arange(ny, dtype=DTYPE) + DTYPE(0.5)) * dy
    XP, YP = np.meshgrid(xP, yP, indexing="ij")
    fluid_P = np.ones((nx, ny), dtype=bool)
    fluid_P[(XP < DTYPE(4.0)) & (YP < DTYPE(h))] = False
    fluid_u = np.zeros((nx + 1, ny), dtype=bool)
    fluid_u[1:nx, :] = fluid_P[:-1, :] & fluid_P[1:, :]
    fluid_u[0, :] = fluid_P[0, :]
    fluid_u[nx, :] = fluid_P[nx - 1, :]
    fluid_v = np.zeros((nx, ny + 1), dtype=bool)
    fluid_v[:, 1:ny] = fluid_P[:, :-1] & fluid_P[:, 1:]
    fluid_v[:, 0] = fluid_P[:, 0]
    fluid_v[:, ny] = fluid_P[:, ny - 1]
    return fluid_P, fluid_u, fluid_v, dx, dy, XP, YP


def inlet_parabolic_profile(y, H, Uavg=1.0):
    y = y.astype(DTYPE, copy=False)
    H = DTYPE(H)
    Uavg = DTYPE(Uavg)
    y_prime = y - FHALF * H
    return FSIX * Uavg * (y_prime / H) * (FONE - y_prime / H)


def precompute_indices(mask):
    idx = np.argwhere(mask)
    return idx[:, 0].astype(np.int32), idx[:, 1].astype(np.int32)


def gs_sor_scalar(AW, AE, AS, AN, AP, b, phi, idx_i, idx_j, omega, sweeps):
    nx, ny = phi.shape
    omega = DTYPE(omega)
    for _ in range(sweeps):
        for i, j in zip(idx_i, idx_j):
            ap = AP[i, j]
            if ap == FZERO:
                continue
            nb = FZERO
            if i > 0:
                nb += AW[i, j] * phi[i - 1, j]
            if i < nx - 1:
                nb += AE[i, j] * phi[i + 1, j]
            if j > 0:
                nb += AS[i, j] * phi[i, j - 1]
            if j < ny - 1:
                nb += AN[i, j] * phi[i, j + 1]
            phi[i, j] += omega * (((b[i, j] + nb) / ap) - phi[i, j])
    return phi


def compute_face_fluxes_u(u, v, dx, dy, Fe, Fw, Fn, Fs):
    rho = DTYPE(1.0)
    nxp1, ny = u.shape
    nx = nxp1 - 1
    Fe[:, :] = rho * u[2 : nx + 1, :] * dy
    Fw[:, :] = rho * u[0 : nx - 1, :] * dy
    Fn[:, :] = rho * DTYPE(0.5) * (v[0 : nx - 1, 1 : ny + 1] + v[1:nx, 1 : ny + 1]) * dx
    Fs[:, :] = rho * DTYPE(0.5) * (v[0 : nx - 1, 0:ny] + v[1:nx, 0:ny]) * dx


def compute_face_fluxes_v(u, v, dx, dy, Fe, Fw, Fn, Fs):
    rho = DTYPE(1.0)
    nx, nyp1 = v.shape
    ny = nyp1 - 1
    Fe[:, :] = rho * DTYPE(0.5) * (u[1 : nx + 1, 1:ny] + u[1 : nx + 1, 0 : ny - 1]) * dy
    Fw[:, :] = rho * DTYPE(0.5) * (u[0:nx, 1:ny] + u[0:nx, 0 : ny - 1]) * dy
    Fn[:, :] = rho * v[:, 2 : ny + 1] * dx
    Fs[:, :] = rho * v[:, 0 : ny - 1] * dx


def build_momentum_u(
    u,
    v,
    p,
    mu,
    dx,
    dy,
    fluid_u,
    fluid_P,
    alpha_u,
    AW,
    AE,
    AS,
    AN,
    AP,
    b,
    Fe,
    Fw,
    Fn,
    Fs,
    idx_i,
    idx_j,
):
    nxp1, ny = u.shape
    nx = nxp1 - 1
    De = DTYPE(mu * dy / dx)
    Dw = De
    Dn = DTYPE(mu * dx / dy)
    Ds = Dn
    AW.fill(FZERO)
    AE.fill(FZERO)
    AS.fill(FZERO)
    AN.fill(FZERO)
    AP.fill(FZERO)
    b.fill(FZERO)
    compute_face_fluxes_u(u, v, dx, dy, Fe, Fw, Fn, Fs)
    for i, j in zip(idx_i, idx_j):
        if i == 0 or i == nx:  # BCs
            continue
        if (not fluid_P[i - 1, j]) or (not fluid_P[i, j]):
            AP[i, j] = FONE
            b[i, j] = FZERO
            continue
        aE = De + max(-Fe[i - 1, j], FZERO)
        aW = Dw + max(Fw[i - 1, j], FZERO)
        aN = Dn + max(-Fn[i - 1, j], FZERO)
        aS = Ds + max(Fs[i - 1, j], FZERO)
        aP = (
            aE
            + aW
            + aN
            + aS
            + (Fe[i - 1, j] - Fw[i - 1, j] + Fn[i - 1, j] - Fs[i - 1, j])
        )
        bsrc = (p[i - 1, j] - p[i, j]) * dy
        AP[i, j] = aP / DTYPE(alpha_u)
        AW[i, j] = aW
        AE[i, j] = aE
        AS[i, j] = aS
        AN[i, j] = aN
        b[i, j] = bsrc + (FONE - DTYPE(alpha_u)) / DTYPE(alpha_u) * aP * u[i, j]


def build_momentum_v(
    u,
    v,
    p,
    mu,
    dx,
    dy,
    fluid_v,
    fluid_P,
    alpha_u,
    AW,
    AE,
    AS,
    AN,
    AP,
    b,
    Fe,
    Fw,
    Fn,
    Fs,
    idx_i,
    idx_j,
):
    nx, nyp1 = v.shape
    ny = nyp1 - 1
    De = DTYPE(mu * dy / dx)
    Dw = De
    Dn = DTYPE(mu * dx / dy)
    Ds = Dn
    AW.fill(FZERO)
    AE.fill(FZERO)
    AS.fill(FZERO)
    AN.fill(FZERO)
    AP.fill(FZERO)
    b.fill(FZERO)
    compute_face_fluxes_v(u, v, dx, dy, Fe, Fw, Fn, Fs)
    for i, j in zip(idx_i, idx_j):
        if j == 0 or j == ny:
            continue
        if (not fluid_P[i, j - 1]) or (not fluid_P[i, j]):
            AP[i, j] = FONE
            b[i, j] = FZERO
            continue
        aE = De + max(-Fe[i, j - 1], FZERO)
        aW = Dw + max(Fw[i, j - 1], FZERO)
        aN = Dn + max(-Fn[i, j - 1], FZERO)
        aS = Ds + max(Fs[i, j - 1], FZERO)
        aP = (
            aE
            + aW
            + aN
            + aS
            + (Fe[i, j - 1] - Fw[i, j - 1] + Fn[i, j - 1] - Fs[i, j - 1])
        )
        bsrc = (p[i, j - 1] - p[i, j]) * dx
        AP[i, j] = aP / DTYPE(alpha_u)
        AW[i, j] = aW
        AE[i, j] = aE
        AS[i, j] = aS
        AN[i, j] = aN
        b[i, j] = bsrc + (FONE - DTYPE(alpha_u)) / DTYPE(alpha_u) * aP * v[i, j]


def apply_velocity_bcs(u, v, params, fluid_u, fluid_v, dy, *, stage="pre"):
    """
    stage="pre":  enforce all BCs (including outlet zero-grad for u)
    stage="post": enforce BCs EXCEPT outlet u, so pressure-correction can set the outflow.
    """
    H = DTYPE(params.H)
    Ly = DTYPE(params.Ly)
    nxp1, ny = u.shape
    nx = nxp1 - 1
    nyp1 = v.shape[1]
    ny_v = nyp1 - 1

    # ---- inlet: parabolic u on open portion, zero-grad v ----
    y_vc = (np.arange(ny, dtype=DTYPE) + DTYPE(0.5)) * (Ly / DTYPE(ny))
    u_in = np.zeros(ny, dtype=DTYPE)
    mask_open = y_vc >= FHALF * H
    u_in[mask_open] = inlet_parabolic_profile(y_vc[mask_open], H, Uavg=1.0)

    u[0, :].fill(FZERO)
    m = fluid_u[0, :]
    u[0, m] = u_in[m]
    # inlet: no penetration, only on open faces
    v[0, fluid_v[0, :]] = FZERO

    # ---- outlet ----
    if stage == "pre":
        # before pressure correction, keep usual zero-gradient
        u[nx, :] = u[nx - 1, :]
    # always zero-grad for v at outlet
    v[nx - 1, :] = v[nx - 2, :]

    # ---- walls (no-slip) ----
    v[:, ny_v].fill(FZERO)  # top wall
    v[:, 0].fill(FZERO)  # bottom wall
    u[:, 0].fill(FZERO)
    u[:, ny - 1].fill(FZERO)

    # ---- obstacles ----
    u[~fluid_u] = FZERO
    v[~fluid_v] = FZERO

    # ---- safety clamp ----
    np.clip(u, FMINUS_FIVE, FFIVE, out=u)
    np.clip(v, FMINUS_FIVE, FFIVE, out=v)


def build_pressure_correction(
    u_star, v_star, APu, APv, fluid_P, dx, dy, AW, AE, AS, AN, AP, b, d_e, d_w, d_n, d_s
):
    nx, ny = fluid_P.shape
    Ae = dy
    Aw = dy
    An = dx
    As = dx

    # Clear/output arrays (keep dtypes)
    np.copyto(d_e, FZERO)
    np.copyto(d_w, FZERO)
    np.copyto(d_n, FZERO)
    np.copyto(d_s, FZERO)
    AW.fill(FZERO)
    AE.fill(FZERO)
    AS.fill(FZERO)
    AN.fill(FZERO)
    AP.fill(FZERO)
    b.fill(FZERO)

    # Safe denominators (avoid 1/0) for momentum AP*
    APu_safe = np.where(APu == FZERO, FBIG, APu)
    APv_safe = np.where(APv == FZERO, FBIG, APv)

    # Face "d" coefficients (Rhie–Chow-like) on the collocated pressure grid
    d_e[0 : nx - 1, :] = Ae / APu_safe[1:nx, :]
    d_w[1:nx, :] = Aw / APu_safe[0 : nx - 1, :]
    d_n[:, 0 : ny - 1] = An / APv_safe[:, 1:ny]
    d_s[:, 1:ny] = As / APv_safe[:, 0 : ny - 1]

    # Discrete divergence of predictor field (RHS)
    b[:, :] = (
        -(u_star[1 : nx + 1, :] - u_star[0:nx, :]) * dy
        - (v_star[:, 1 : ny + 1] - v_star[:, 0:ny]) * dx
    )

    # Cell coefficients (interior)
    AE[:, :] = d_e
    AW[:, :] = d_w
    AN[:, :] = d_n
    AS[:, :] = d_s
    AP[:, :] = AE + AW + AN + AS

    # Mask out solids
    mask = fluid_P
    AW[~mask] = AE[~mask] = AS[~mask] = AN[~mask] = FZERO
    AP[~mask] = FZERO
    b[~mask] = FZERO

    # ---- Pressure-outlet for the correction on the right boundary: p' = 0 ----
    i_out = nx - 1
    AW[i_out, :] = AE[i_out, :] = AS[i_out, :] = AN[i_out, :] = FZERO
    AP[i_out, :] = FONE
    b[i_out, :] = FZERO


def correct_uvp(u, v, p, pcor, fluid_P, dx, dy, d_e, d_w, d_n, d_s, alpha_p):
    # vectorized corrections (same as loop but slice-wise)
    nx, ny = fluid_P.shape

    # u faces i=1..nx-1
    dp_u = pcor[0 : nx - 1, :] - pcor[1:nx, :]
    dface_u = DTYPE(0.5) * (d_e[0 : nx - 1, :] + d_w[1:nx, :])
    u[1:nx, :] += dface_u * dp_u

    # v faces j=1..ny-1
    dp_v = pcor[:, 0 : ny - 1] - pcor[:, 1:ny]
    dface_v = DTYPE(0.5) * (d_n[:, 0 : ny - 1] + d_s[:, 1:ny])
    v[:, 1:ny] += dface_v * dp_v

    p += DTYPE(alpha_p) * pcor


def compute_residuals_u(AW, AE, AS, AN, AP, b, u, idx_i, idx_j):
    nxp1, ny = u.shape
    s = DTYPE(0.0)
    c = 0
    for i, j in zip(idx_i, idx_j):
        if i == 0 or i == nxp1 - 1:
            continue
        r = b[i, j]
        if i > 0:
            r += AW[i, j] * u[i - 1, j]
        if i < nxp1 - 1:
            r += AE[i, j] * u[i + 1, j]
        if j > 0:
            r += AS[i, j] * u[i, j - 1]
        if j < ny - 1:
            r += AN[i, j] * u[i, j + 1]
        r -= AP[i, j] * u[i, j]
        s += abs(r)
        c += 1
    return (s / DTYPE(max(c, 1))).astype(DTYPE)


def compute_residuals_v(AW, AE, AS, AN, AP, b, v, idx_i, idx_j):
    nx, nyp1 = v.shape
    s = DTYPE(0.0)
    c = 0
    for i, j in zip(idx_i, idx_j):
        if j == 0 or j == nyp1 - 1:
            continue
        r = b[i, j]
        if i > 0:
            r += AW[i, j] * v[i - 1, j]
        if i < nx - 1:
            r += AE[i, j] * v[i + 1, j]
        if j > 0:
            r += AS[i, j] * v[i, j - 1]
        if j < nyp1 - 1:
            r += AN[i, j] * v[i, j + 1]
        r -= AP[i, j] * v[i, j]
        s += abs(r)
        c += 1
    return (s / DTYPE(max(c, 1))).astype(DTYPE)


def global_mass_imbalance(u, v, fluid_P, dx, dy):
    nx, ny = fluid_P.shape
    inlet_flux = DTYPE(np.sum(u[0, :][fluid_P[0, :]] * dy))
    outlet_flux = DTYPE(np.sum(u[nx, :][fluid_P[nx - 1, :]] * dy))
    net = inlet_flux - outlet_flux
    denom = abs(inlet_flux) if abs(inlet_flux) > DTYPE(1e-12) else FONE
    return DTYPE(abs(net) / denom), inlet_flux, outlet_flux


def setup_plot(XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, params):
    plt.ion()
    fig = plt.figure(figsize=(11, 8))
    gs = fig.add_gridspec(2, 2, height_ratios=[2.0, 1.0])
    ax0 = fig.add_subplot(gs[0, :])  # field
    ax1 = fig.add_subplot(gs[1, 0])  # residuals
    ax2 = fig.add_subplot(gs[1, 1])  # mass imbalance

    # --- field (imshow + quiver) ---
    speed = np.sqrt(Uc**2 + Vc**2, dtype=DTYPE)
    speed_masked = ma.array(speed.T, mask=~fluid_P.T)
    im = ax0.imshow(
        speed_masked,
        origin="lower",
        extent=[float(XP.min()), float(XP.max()), float(YP.min()), float(YP.max())],
        aspect="auto",
        cmap="viridis",
    )
    cbar = fig.colorbar(im, ax=ax0, fraction=0.046, pad=0.04)
    cbar.set_label("|U|")

    ds = params.quiver_ds
    Xc = XP[::ds, ::ds]
    Yc = YP[::ds, ::ds]

    # --- pre-scale velocities so the 95th percentile vector ≈ 0.7 * smallest cell ---
    dx_cell = float(XP[1, 0] - XP[0, 0])
    dy_cell = float(YP[0, 1] - YP[0, 0])
    cell = min(dx_cell, dy_cell)
    ref = float(np.nanpercentile(speed[fluid_P], 95)) if np.any(fluid_P) else 1.0
    ref = max(ref, 1e-6)  # guard against tiny/zero fields
    fac = (0.7 * cell) / ref  # scale factor in data units
    Uq = Uc * fac
    Vq = Vc * fac

    qv = ax0.quiver(
        Xc,
        Yc,
        Uq[::ds, ::ds],
        Vq[::ds, ::ds],
        color="white",
        scale=1.0,  # we pre-scaled U,V; keep quiver scale = 1
        scale_units="xy",
        angles="xy",
        pivot="mid",
        width=0.0025,
        zorder=3,
    )
    ax0._qfac = fac  # remember scale for EMA updates

    ax0.set_title("Velocity magnitude with quiver (Backward-Facing Step)")
    ax0.set_xlim([float(XP.min()), float(XP.max())])
    ax0.set_ylim([float(YP.min()), float(YP.max())])

    # store vmax for gentle EMA updates in update_plot
    im_vmax = max(1.0, float(speed_masked.max()))
    im.set_clim(vmin=0.0, vmax=im_vmax)
    ax0._im_vmax = im_vmax

    # --- residuals ---
    ax1.set_title("Residuals")
    ax1.set_yscale("log")
    (line_ru,) = ax1.plot(res_hist["u"], label="u")
    (line_rv,) = ax1.plot(res_hist["v"], label="v")
    (line_rp,) = ax1.plot(res_hist["p"], label="p")
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Residual")
    ax1.legend(loc="best")

    # --- mass imbalance (adaptive log axis) ---
    ax2.set_title("Global mass imbalance")
    imb_percent = np.clip(np.array(imb_hist, dtype=float), 1e-12, None) * 100.0
    (line_imb,) = ax2.plot(imb_percent)
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Imbalance (% of inlet)")
    ax2.set_yscale("log")
    if np.isfinite(imb_percent).any():
        lo = max(1e-6, 0.5 * np.nanmin(imb_percent[np.isfinite(imb_percent)]))
        hi = max(1e-2, 2.0 * np.nanmax(imb_percent[np.isfinite(imb_percent)]))
        ax2.set_ylim(lo, hi)
    else:
        ax2.set_ylim(1e-6, 1e2)

    fig.tight_layout()
    fig.canvas.draw()
    try:
        plt.show(block=False)
    except TypeError:
        plt.show()
    plt.pause(0.001)

    return fig, (ax0, ax1, ax2), im, qv, (line_ru, line_rv, line_rp), line_imb, ds


def update_plot(
    axs, im, qv, lines_res, line_imb, XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, ds
):
    # --- field ---
    speed = np.sqrt(Uc**2 + Vc**2, dtype=DTYPE)
    speed_masked = ma.array(speed.T, mask=~fluid_P.T)
    im.set_data(speed_masked)

    # gentle color scaling (EMA)
    ax0 = axs[0]
    new_max = float(speed_masked.max())
    ax0._im_vmax = 0.9 * getattr(ax0, "_im_vmax", max(1.0, new_max)) + 0.1 * max(
        1.0, new_max
    )
    im.set_clim(vmin=0.0, vmax=ax0._im_vmax)

    # --- quiver: recompute scale factor gently (EMA) and pre-scale U,V ---
    dx_cell = float(XP[1, 0] - XP[0, 0])
    dy_cell = float(YP[0, 1] - YP[0, 0])
    cell = min(dx_cell, dy_cell)
    ref = float(np.nanpercentile(speed[fluid_P], 95)) if np.any(fluid_P) else 1.0
    ref = max(ref, 1e-6)
    fac_new = (0.7 * cell) / ref
    fac = 0.9 * getattr(ax0, "_qfac", fac_new) + 0.1 * fac_new
    fac = min(fac, 1.5)
    fac = max(fac, 0.1)

    ax0._qfac = fac

    Uq = Uc * fac
    Vq = Vc * fac
    qv.set_UVC(Uq[::ds, ::ds], Vq[::ds, ::ds])

    # --- residuals ---
    lines_res[0].set_data(np.arange(len(res_hist["u"])), res_hist["u"])
    lines_res[1].set_data(np.arange(len(res_hist["v"])), res_hist["v"])
    lines_res[2].set_data(np.arange(len(res_hist["p"])), res_hist["p"])
    axs[1].relim()
    axs[1].autoscale_view()

    # --- mass imbalance (adaptive limits) ---
    imb_percent = np.clip(np.array(imb_hist, dtype=float), 1e-12, None) * 100.0
    line_imb.set_data(np.arange(len(imb_percent)), imb_percent)
    if np.isfinite(imb_percent).any():
        lo = max(1e-6, 0.5 * np.nanmin(imb_percent[np.isfinite(imb_percent)]))
        hi = max(1e-2, 2.0 * np.nanmax(imb_percent[np.isfinite(imb_percent)]))
        axs[2].set_ylim(lo, hi)
    axs[2].relim()
    axs[2].autoscale_view()

    # draw
    fig = axs[0].figure
    fig.canvas.draw_idle()
    try:
        fig.canvas.flush_events()
    except Exception:
        pass
    plt.pause(0.001)


def main():
    parser = argparse.ArgumentParser(
        description="2D BFS SIMPLE (NumPy, float32, throttled)"
    )
    parser.add_argument("--nx", type=int, default=240)
    parser.add_argument("--ny", type=int, default=80)
    parser.add_argument("--max-iters", type=int, default=3000)
    parser.add_argument("--plot-interval", type=int, default=20)
    parser.add_argument(
        "--throttle-ms",
        type=int,
        default=0,
        help="Sleep this many ms every 5 iterations",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a quick demo (smaller grid, fewer iterations)",
    )
    args = parser.parse_args()

    if args.demo:
        nx, ny = 120, 40
        max_iters = 400
        plot_interval = 5
    else:
        nx, ny = args.nx, args.ny
        max_iters = args.max_iters
        plot_interval = args.plot_interval

    prm = Params(nx=nx, ny=ny, max_iters=max_iters, plot_interval=plot_interval)
    np.random.seed(prm.seed)

    fluid_P, fluid_u, fluid_v, dx, dy, XP, YP = build_geometry_masks(
        prm.nx, prm.ny, prm.Lx, prm.Ly, prm.H, prm.h
    )

    # state arrays as float32
    p = np.zeros((prm.nx, prm.ny), dtype=DTYPE)
    u = np.zeros((prm.nx + 1, prm.ny), dtype=DTYPE)
    v = np.zeros((prm.nx, prm.ny + 1), dtype=DTYPE)
    mu = DTYPE(prm.rho / prm.Re)

    # initial BCs (pre-correction style)
    apply_velocity_bcs(u, v, prm, fluid_u, fluid_v, dy, stage="pre")

    Uc = DTYPE(0.5) * (u[0 : prm.nx, :] + u[1 : prm.nx + 1, :])
    Vc = DTYPE(0.5) * (v[:, 0 : prm.ny] + v[:, 1 : prm.ny + 1])

    res_hist = {"u": [], "v": [], "p": []}
    imb_hist = []

    fig, axs, im, qv, lines_res, line_imb, ds = setup_plot(
        XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, prm
    )

    idx_u_i, idx_u_j = precompute_indices(fluid_u)
    idx_v_i, idx_v_j = precompute_indices(fluid_v)
    idx_p_i, idx_p_j = precompute_indices(fluid_P)

    # coefficient arrays (inherit dtype from like-arrays)
    AWu = np.zeros_like(u)
    AEu = np.zeros_like(u)
    ASu = np.zeros_like(u)
    ANu = np.zeros_like(u)
    APu = np.zeros_like(u)
    bu = np.zeros_like(u)
    AWv = np.zeros_like(v)
    AEv = np.zeros_like(v)
    ASv = np.zeros_like(v)
    ANv = np.zeros_like(v)
    APv = np.zeros_like(v)
    bv = np.zeros_like(v)
    AWp = np.zeros_like(p)
    AEp = np.zeros_like(p)
    ASp = np.zeros_like(p)
    ANp = np.zeros_like(p)
    APp = np.zeros_like(p)
    bp = np.zeros_like(p)
    d_e = np.zeros_like(p)
    d_w = np.zeros_like(p)
    d_n = np.zeros_like(p)
    d_s = np.zeros_like(p)

    Fe_u = np.zeros((prm.nx - 1, prm.ny), dtype=DTYPE)
    Fw_u = np.zeros((prm.nx - 1, prm.ny), dtype=DTYPE)
    Fn_u = np.zeros((prm.nx - 1, prm.ny), dtype=DTYPE)
    Fs_u = np.zeros((prm.nx - 1, prm.ny), dtype=DTYPE)

    Fe_v = np.zeros((prm.nx, prm.ny - 1), dtype=DTYPE)
    Fw_v = np.zeros((prm.nx, prm.ny - 1), dtype=DTYPE)
    Fn_v = np.zeros((prm.nx, prm.ny - 1), dtype=DTYPE)
    Fs_v = np.zeros((prm.nx, prm.ny - 1), dtype=DTYPE)

    u_star = u.copy()
    v_star = v.copy()
    pcor = np.zeros_like(p)

    init_res = None
    start = time.time()

    for it in range(1, prm.max_iters + 1):
        # --- predictor (momentum) ---
        build_momentum_u(
            u,
            v,
            p,
            mu,
            dx,
            dy,
            fluid_u,
            fluid_P,
            prm.alpha_u,
            AWu,
            AEu,
            ASu,
            ANu,
            APu,
            bu,
            Fe_u,
            Fw_u,
            Fn_u,
            Fs_u,
            idx_u_i,
            idx_u_j,
        )
        build_momentum_v(
            u,
            v,
            p,
            mu,
            dx,
            dy,
            fluid_v,
            fluid_P,
            prm.alpha_u,
            AWv,
            AEv,
            ASv,
            ANv,
            APv,
            bv,
            Fe_v,
            Fw_v,
            Fn_v,
            Fs_v,
            idx_v_i,
            idx_v_j,
        )

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

        apply_velocity_bcs(u_star, v_star, prm, fluid_u, fluid_v, dy, stage="pre")

        # --- pressure correction (with p' outlet) ---
        build_pressure_correction(
            u_star,
            v_star,
            APu,
            APv,
            fluid_P,
            dx,
            dy,
            AWp,
            AEp,
            ASp,
            ANp,
            APp,
            bp,
            d_e,
            d_w,
            d_n,
            d_s,
        )
        pcor.fill(FZERO)
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
        correct_uvp(u, v, p, pcor, fluid_P, dx, dy, d_e, d_w, d_n, d_s, prm.alpha_p)

        np.clip(u, FMINUS_FIVE, FFIVE, out=u)
        np.clip(v, FMINUS_FIVE, FFIVE, out=v)
        apply_velocity_bcs(
            u, v, prm, fluid_u, fluid_v, dy, stage="post"
        )  # don't overwrite outlet u

        # --- monitors ---
        ru = float(
            compute_residuals_u(AWu, AEu, ASu, ANu, APu, bu, u, idx_u_i, idx_u_j)
        )
        rv = float(
            compute_residuals_v(AWv, AEv, ASv, ANv, APv, bv, v, idx_v_i, idx_v_j)
        )
        div = (u[1 : prm.nx + 1, :] - u[0 : prm.nx, :]) * dy + (
            v[:, 1 : prm.ny + 1] - v[:, 0 : prm.ny]
        ) * dx
        rp = float(np.mean(np.abs(div[fluid_P])))
        res_hist["u"].append(ru)
        res_hist["v"].append(rv)
        res_hist["p"].append(rp)

        imb, inflow, outflow = global_mass_imbalance(u, v, fluid_P, dx, dy)
        imb_hist.append(float(imb))

        if init_res is None and len(res_hist["u"]) >= 2:
            init_res = (res_hist["u"][0], res_hist["v"][0], res_hist["p"][0])

        if it % 10 == 0 or it == 1:
            print(
                f"Iter {it:5d}: Ru={ru:.3e}, Rv={rv:.3e}, Rp={rp:.3e}, MassImb={float(imb)*100:.2f}%"
            )

        if (it % prm.plot_interval == 0) or (it == 1):
            Uc = DTYPE(0.5) * (u[0 : prm.nx, :] + u[1 : prm.nx + 1, :])
            Vc = DTYPE(0.5) * (v[:, 0 : prm.ny] + v[:, 1 : prm.ny + 1])
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

        done = False
        if init_res is not None:
            ruf = res_hist["u"][-1] / (init_res[0] + 1e-30)
            rvf = res_hist["v"][-1] / (init_res[1] + 1e-30)
            rpf = res_hist["p"][-1] / (init_res[2] + 1e-30)
            if (
                (ruf <= 1e-3)
                and (rvf <= 1e-3)
                and (rpf <= 1e-3)
                and (imb <= DTYPE(5e-3))
            ):
                done = True
        if done:
            print("Converged: residuals dropped >=3 orders and mass imbalance <= 0.5%.")
            break

        # ---- gentle throttle (optional) ----
        if args.throttle_ms > 0 and (it % 5 == 0):
            time.sleep(args.throttle_ms / 1000.0)

    elapsed = time.time() - start
    print(f"Finished at iter {it} in {elapsed:.1f}s.")
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
