#!/usr/bin/env python3
"""
2D Backward-Facing Step (BFS) — Steady, incompressible, laminar flow (Re=200)
Solved using SIMPLE on a uniform staggered finite-volume grid with NumPy only.
Matplotlib used for live visualization of velocity magnitude and residuals.

Domain (non-dimensional):
- Upstream channel height H = 1
- Step height h = 0.5 H
- Upstream length 4H, downstream length 20H, total Lx = 24H
- Downstream full height = H + h = 1.5H
- Coordinates: x in [0, 24], y in [0, 1.5]
  Upstream (x < 4): fluid occupies y in [0.5, 1.5] (bottom region [0,0.5) is solid)
  Downstream (x >= 4): fluid occupies y in [0.0, 1.5]

Boundary conditions:
- Inlet x=0: u(y) = 6 Uavg (y/H)(1 - y/H) applied only over open channel [0.5, 1.5]; v=0
- Outlet x=24: zero-gradient for u, v; pressure reference: p' = 0 on the last pressure column (i = nx-1)
- Walls (top, bottom, and step faces): no-slip (u=v=0)

Numerics:
- SIMPLE: momentum -> p' -> correct u,v,p (under-relax)
- Convection: first-order upwind; Diffusion: central difference
- Linear solves: Gauss–Seidel SOR (fixed sweeps per outer iteration)

Visualization:
- Live updates every plot_interval iterations
- Top: velocity magnitude with quiver (downsampled)
- Bottom-left: residual history (semilogy)
- Bottom-right: global mass imbalance history

Notes:
- Default grid nx=240, ny=80; pass --demo for a faster small run.
- This is a compact educational implementation; not optimized for speed.
"""

import argparse
import time
from dataclasses import dataclass

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt


@dataclass
class Params:
    nx: int = 240
    ny: int = 80
    Re: float = 200.0
    H: float = 1.0
    h: float = 0.5  # 0.5*H
    Lx: float = 24.0
    Ly: float = 1.5  # H + h
    rho: float = 1.0
    alpha_u: float = 0.3
    alpha_p: float = 0.3
    omega_mom: float = 1.0  # SOR factor for momentum (GS SOR ~1.0 .. 1.7); keep modest
    omega_p: float = 1.5    # SOR factor for pressure correction
    mom_sweeps: int = 1     # GS sweeps per SIMPLE iter for u and v
    pcor_sweeps: int = 150  # GS SOR sweeps per SIMPLE iter for p'
    max_iters: int = 3000
    plot_interval: int = 20
    quiver_ds: int = 3      # downsample for quiver plotting (cell-center vectors)
    seed: int = 0


def build_geometry_masks(nx, ny, Lx, Ly, H, h):
    """Return boolean masks for fluid cells at P, and derived masks for u and v locations.

    Staggering:
    - Pressure (P) at cell centers: shape (nx, ny)
    - u at vertical faces: shape (nx+1, ny) located between P[i-1,j] and P[i,j]
    - v at horizontal faces: shape (nx, ny+1) located between P[i,j-1] and P[i,j]
    """
    dx = Lx / nx
    dy = Ly / ny

    xP = (np.arange(nx) + 0.5) * dx
    yP = (np.arange(ny) + 0.5) * dy
    XP, YP = np.meshgrid(xP, yP, indexing="ij")

    # Fluid region definition for P-cells
    fluid_P = np.ones((nx, ny), dtype=bool)
    # Upstream region (x < 4H): bottom y < h is solid
    fluid_P[(XP < 4.0) & (YP < h)] = False
    # Elsewhere (downstream x >= 4), full height is fluid

    # u-face mask: face between P[i-1,j] and P[i,j] is fluid if both neighbors are fluid
    fluid_u = np.zeros((nx + 1, ny), dtype=bool)
    fluid_u[1:nx, :] = fluid_P[:-1, :] & fluid_P[1:, :]
    # Leftmost and rightmost boundary u-faces: we'll set BCs explicitly where adjacent cell is fluid
    fluid_u[0, :] = fluid_P[0, :]
    fluid_u[nx, :] = fluid_P[nx - 1, :]

    # v-face mask: face between P[i,j-1] and P[i,j]
    fluid_v = np.zeros((nx, ny + 1), dtype=bool)
    fluid_v[:, 1:ny] = fluid_P[:, :-1] & fluid_P[:, 1:]
    # Bottom and top boundary v-faces
    fluid_v[:, 0] = fluid_P[:, 0]
    fluid_v[:, ny] = fluid_P[:, ny - 1]

    return fluid_P, fluid_u, fluid_v, dx, dy, XP, YP


def inlet_parabolic_profile(y, H, Uavg=1.0):
    # Only valid for y in [0.5H, 1.5H] when using downstream coordinates with bottom at 0
    # Map y' = y - 0.5H to [0, H]
    y_prime = y - 0.5 * H
    return 6.0 * Uavg * (y_prime / H) * (1.0 - y_prime / H)


def gs_sor_scalar(AW, AE, AS, AN, AP, b, phi, mask, omega, sweeps):
    """Gauss–Seidel SOR for a 5-point stencil system on a structured grid.
    Arrays are (nx, ny). mask marks active cells to iterate.
    A coefficients and b should already include under-relaxation and boundary contributions.
    """
    nx, ny = phi.shape
    for _ in range(sweeps):
        # Red-black or lexicographic; here simple lexicographic GS with SOR
        for i in range(nx):
            for j in range(ny):
                if not mask[i, j]:
                    continue
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
                phi_new = (b[i, j] + nb) / ap
                phi[i, j] = phi[i, j] + omega * (phi_new - phi[i, j])
    return phi


def compute_face_fluxes_u(u, v, dx, dy):
    """Compute mass fluxes at faces for u-control-volumes.
    Returns Fe, Fw, Fn, Fs arrays with shapes matching u-internal cells (nx+1, ny) used via indices.
    For simplicity we compute fluxes on the same grid and will index appropriately when building coeffs.
    """
    rho = 1.0
    # Mass fluxes across faces of u CV located at (i,j) for u[1..nx-1, 0..ny-1]
    # East/West faces use neighboring u values; North/South need v at staggered positions.
    # We'll build arrays Fe,Fw,Fn,Fs of shape like u.
    nxp1, ny = u.shape
    nx = nxp1 - 1

    # East/West mass fluxes at u-faces: Fe at between u[i] and u[i+1]
    # For convection coeffs at u[i,j], Fe = rho * u[i+1,j] * dy, Fw = rho * u[i-1,j] * dy
    Fe = rho * u[2:nx + 1, :] * dy  # shape (nx-1, ny) aligned to u[1..nx-1]
    Fw = rho * u[0:nx - 1, :] * dy

    # North/South: need v at y-faces around the u-CV. Approximate by averaging nearest v faces.
    # v has shape (nx, ny+1), we need v at positions aligned with u[i,j]. We'll average v at i-1 and i indices.
    # For u[i,j], the north face is at j+1/2; use v_avg_n = 0.5*(v[i-1,j+1] + v[i,j+1])
    # Similarly south face at j-1/2: 0.5*(v[i-1,j] + v[i,j])
    # Build north/south fluxes aligned to u indices i=1..nx-1, j=0..ny-1
    # v_n(i,j) = 0.5*(v[i-1,j+1] + v[i,j+1]) for i=1..nx-1, j=0..ny-1
    v_n = 0.5 * (v[0:nx - 1, 1:ny + 1] + v[1:nx, 1:ny + 1])  # (nx-1, ny)
    # v_s(i,j) = 0.5*(v[i-1,j] + v[i,j]) for i=1..nx-1
    v_s = 0.5 * (v[0:nx - 1, 0:ny] + v[1:nx, 0:ny])          # (nx-1, ny)
    Fn = rho * v_n * dx
    Fs = rho * v_s * dx

    return Fe, Fw, Fn, Fs


def compute_face_fluxes_v(u, v, dx, dy):
    """Compute mass fluxes at faces for v-control-volumes.
    Returns Fe, Fw, Fn, Fs aligned to v[0..nx-1, 1..ny-1] internal cells.
    """
    rho = 1.0
    nx, nyp1 = v.shape
    ny = nyp1 - 1

    # East/West faces: average u at j-1 and j to align with v at j (1..ny-1)
    # u_e(i,j) = 0.5*(u[i+1,j] + u[i+1,j-1]); u_w(i,j) = 0.5*(u[i,j] + u[i,j-1])
    u_e = 0.5 * (u[1:nx + 1, 1:ny] + u[1:nx + 1, 0:ny - 1])  # (nx, ny-1)
    u_w = 0.5 * (u[0:nx, 1:ny] + u[0:nx, 0:ny - 1])          # (nx, ny-1)
    Fe = rho * u_e * dy
    Fw = rho * u_w * dy

    # North/South faces: use v above/below at j+1 and j-1
    Fn = rho * v[:, 2:ny + 1] * dx   # (nx, ny-1)
    Fs = rho * v[:, 0:ny - 1] * dx   # (nx, ny-1)

    return Fe, Fw, Fn, Fs


def build_momentum_u(u, v, p, mu, dx, dy, fluid_u, fluid_P, alpha_u):
    """Build coefficients for u-momentum equation at interior u cells (1..nx-1, 0..ny-1).
    Returns AW, AE, AS, AN, AP, b (all (nx+1, ny) with nonzero only where fluid_u True).
    """
    nxp1, ny = u.shape
    nx = nxp1 - 1

    De = mu * dy / dx
    Dw = mu * dy / dx
    Dn = mu * dx / dy
    Ds = mu * dx / dy

    AW = np.zeros_like(u)
    AE = np.zeros_like(u)
    AS = np.zeros_like(u)
    AN = np.zeros_like(u)
    AP = np.zeros_like(u)
    b = np.zeros_like(u)

    # Compute mass fluxes for convection (aligned to u[1..nx-1])
    Fe, Fw, Fn, Fs = compute_face_fluxes_u(u, v, dx, dy)

    for i in range(1, nx):
        for j in range(ny):
            if not fluid_u[i, j]:
                continue
            # Skip solid-neighbored faces (if either adjacent P cell is solid, treat as boundary with Dirichlet)
            if (not fluid_P[i - 1, j]) or (not fluid_P[i, j]):
                # Wall or outside — enforce u=0 here via AP=1, b=0 (unless inlet/outlet handled elsewhere)
                AP[i, j] = 1.0
                b[i, j] = 0.0
                continue

            aE = De + max(-Fe[i - 1, j], 0.0)
            aW = Dw + max(Fw[i - 1, j], 0.0)
            aN = Dn + max(-Fn[i - 1, j], 0.0)
            aS = Ds + max(Fs[i - 1, j], 0.0)

            aP = aE + aW + aN + aS + (Fe[i - 1, j] - Fw[i - 1, j] + Fn[i - 1, j] - Fs[i - 1, j])

            # Pressure gradient source across the u-CV (between P[i-1,j] and P[i,j])
            # b includes + (p_W - p_E) * dy
            bsrc = (p[i - 1, j] - p[i, j]) * dy

            # Under-relaxation by aP /= alpha_u, add source from old value
            AP[i, j] = aP / alpha_u
            AW[i, j] = aW
            AE[i, j] = aE
            AS[i, j] = aS
            AN[i, j] = aN
            b[i, j] = bsrc + (1.0 - alpha_u) / alpha_u * aP * u[i, j]

    # Boundary faces: enforce BCs
    # Inlet u at i=0 is Dirichlet at open channel; outlet i=nx zero-gradient (handled later)
    return AW, AE, AS, AN, AP, b


def build_momentum_v(u, v, p, mu, dx, dy, fluid_v, fluid_P, alpha_u):
    nx, nyp1 = v.shape
    ny = nyp1 - 1

    De = mu * dy / dx
    Dw = mu * dy / dx
    Dn = mu * dx / dy
    Ds = mu * dx / dy

    AW = np.zeros_like(v)
    AE = np.zeros_like(v)
    AS = np.zeros_like(v)
    AN = np.zeros_like(v)
    AP = np.zeros_like(v)
    b = np.zeros_like(v)

    Fe, Fw, Fn, Fs = compute_face_fluxes_v(u, v, dx, dy)

    for i in range(nx):
        for j in range(1, ny):
            if not fluid_v[i, j]:
                continue
            if (not fluid_P[i, j - 1]) or (not fluid_P[i, j]):
                AP[i, j] = 1.0
                b[i, j] = 0.0
                continue

            aE = De + max(-Fe[i, j - 1], 0.0)
            aW = Dw + max(Fw[i, j - 1], 0.0)
            aN = Dn + max(-Fn[i, j - 1], 0.0)
            aS = Ds + max(Fs[i, j - 1], 0.0)

            aP = aE + aW + aN + aS + (Fe[i, j - 1] - Fw[i, j - 1] + Fn[i, j - 1] - Fs[i, j - 1])

            # Pressure gradient across v-CV: (p_S - p_N) * dx
            bsrc = (p[i, j - 1] - p[i, j]) * dx

            AP[i, j] = aP / alpha_u
            AW[i, j] = aW
            AE[i, j] = aE
            AS[i, j] = aS
            AN[i, j] = aN
            b[i, j] = bsrc + (1.0 - alpha_u) / alpha_u * aP * v[i, j]

    return AW, AE, AS, AN, AP, b


def apply_velocity_bcs(u, v, params, fluid_u, fluid_v, dy):
    """Set inlet, outlet, and wall BCs for u and v in-place."""
    H = params.H
    Lx = params.Lx
    Ly = params.Ly

    nxp1, ny = u.shape
    nx = nxp1 - 1
    nyp1 = v.shape[1]
    ny_v = nyp1 - 1

    # Inlet at x=0: u[0, j] = parabolic over y in [0.5H, 1.5H], zero elsewhere
    y_vc = (np.arange(ny) + 0.5) * (Ly / ny)  # cell-center y for u faces
    u_in = np.zeros(ny)
    mask_open = y_vc >= 0.5 * H
    u_in[mask_open] = inlet_parabolic_profile(y_vc[mask_open], H, Uavg=1.0)
    # Apply only where the adjacent P cell is fluid (left column)
    u[0, :] = 0.0
    for j in range(ny):
        if fluid_u[0, j]:
            u[0, j] = u_in[j]

    # v at inlet is zero
    v[0, :] = 0.0

    # Outlet x=L: zero-gradient u and v (copy from interior)
    u[nx, :] = u[nx - 1, :]
    v[nx - 1, :] = v[nx - 2, :]

    # Top wall y=Ly: v at top boundary faces zero; u at top boundary faces zero
    v[:, ny_v] = 0.0
    u[:, ny - 1] = 0.0  # top u face adjacent to top wall (no-slip)

    # Bottom wall: upstream wall at y=h for x<4H; downstream wall at y=0
    # Enforce no-slip: v at bottom boundary faces zero; u at bottom face zero
    v[:, 0] = 0.0
    u[:, 0] = 0.0

    # Additionally, zero velocities adjacent to solid step surfaces
    # We'll simply zero any u/v faces marked non-fluid
    u[~fluid_u] = 0.0
    v[~fluid_v] = 0.0

    # Clip to avoid runaway due to initial transients
    np.clip(u, -5.0, 5.0, out=u)
    np.clip(v, -5.0, 5.0, out=v)


def build_pressure_correction(u_star, v_star, APu, APv, fluid_P, dx, dy):
    """Build coefficients for pressure correction p'.
    aE = rho * dy * d_e, etc., with d_e = 1/aP_u at the corresponding face (here dy/aP_u since A=dy, rho=1).
    RHS is the mass imbalance from u*, v*.
    Returns AW, AE, AS, AN, AP, b for p' on P cells.
    """
    nx, ny = fluid_P.shape

    # Face areas
    Ae = dy
    Aw = dy
    An = dx
    As = dx

    # d at faces from momentum aP (Rhie–Chow-like stabilization omitted, simple d = A/aP)
    # u faces exist at i=1..nx-1; map to P faces east/west
    d_e = np.zeros((nx, ny))
    d_w = np.zeros((nx, ny))
    d_n = np.zeros((nx, ny))
    d_s = np.zeros((nx, ny))

    # Avoid division by zero
    APu_safe = APu.copy(); APu_safe[APu_safe == 0] = 1e30
    APv_safe = APv.copy(); APv_safe[APv_safe == 0] = 1e30

    # East face between P[i,j] and P[i+1,j] corresponds to u at i+1
    d_e[0:nx - 1, :] = Ae / APu_safe[1:nx, :]
    # West face corresponds to u at i
    d_w[1:nx, :] = Aw / APu_safe[1:nx, :]

    # North face corresponds to v at j+1
    d_n[:, 0:ny - 1] = An / APv_safe[:, 1:ny]
    # South face corresponds to v at j
    d_s[:, 1:ny] = As / APv_safe[:, 0:ny - 1]

    # RHS from tentative velocities (negative divergence)
    b = (-(u_star[1:nx + 1, :] - u_star[0:nx, :]) * dy - (v_star[:, 1:ny + 1] - v_star[:, 0:ny]) * dx)

    AE = d_e.copy(); AW = d_w.copy(); AN = d_n.copy(); AS = d_s.copy()
    AP = AE + AW + AN + AS

    # Apply solid mask
    mask = fluid_P.copy()
    AW[~mask] = 0.0; AE[~mask] = 0.0; AS[~mask] = 0.0; AN[~mask] = 0.0; AP[~mask] = 0.0; b[~mask] = 0.0

    # Reference pressure correction at outlet line i = nx-1
    iref = nx - 1
    AW[iref, :] = 0.0; AE[iref, :] = 0.0; AS[iref, :] = 0.0; AN[iref, :] = 0.0; AP[iref, :] = 1.0; b[iref, :] = 0.0

    return AW, AE, AS, AN, AP, b, d_e, d_w, d_n, d_s


def correct_uvp(u, v, p, pcor, fluid_P, dx, dy, d_e, d_w, d_n, d_s, alpha_p):
    nx, ny = fluid_P.shape

    # Correct u on faces between P[i-1] and P[i]
    for i in range(1, nx):
        for j in range(ny):
            dp = pcor[i - 1, j] - pcor[i, j]
            # Use d at corresponding east/west faces; approximate with average of d_e at west cell and d_w at east cell
            d_face = 0.5 * (d_e[i - 1, j] + d_w[i, j])
            u[i, j] = u[i, j] + d_face * dp

    # Correct v on faces between P[i,j-1] and P[i,j]
    for i in range(nx):
        for j in range(1, ny):
            dp = pcor[i, j - 1] - pcor[i, j]
            d_face = 0.5 * (d_n[i, j - 1] + d_s[i, j])
            v[i, j] = v[i, j] + d_face * dp

    # Pressure correction
    p[:, :] = p[:, :] + alpha_p * pcor


def compute_residuals_u(AW, AE, AS, AN, AP, b, u, mask):
    nxp1, ny = u.shape
    res = 0.0
    count = 0
    for i in range(1, nxp1 - 1):
        for j in range(ny):
            if not mask[i, j]:
                continue
            r = b[i, j] + AW[i, j] * u[i - 1, j] + AE[i, j] * u[i + 1, j] + AS[i, j] * u[i, j - 1 if j > 0 else j] + AN[i, j] * u[i, j + 1 if j < ny - 1 else j] - AP[i, j] * u[i, j]
            res += abs(r)
            count += 1
    return res / max(count, 1)


def compute_residuals_v(AW, AE, AS, AN, AP, b, v, mask):
    nx, nyp1 = v.shape
    res = 0.0
    count = 0
    for i in range(0, nx):
        for j in range(1, nyp1 - 1):
            if not mask[i, j]:
                continue
            r = b[i, j] + AW[i, j] * v[i - 1 if i > 0 else i, j] + AE[i, j] * v[i + 1 if i < nx - 1 else i, j] + AS[i, j] * v[i, j - 1] + AN[i, j] * v[i, j + 1] - AP[i, j] * v[i, j]
            res += abs(r)
            count += 1
    return res / max(count, 1)


def global_mass_imbalance(u, v, fluid_P, dx, dy):
    nx, ny = fluid_P.shape
    # Net flux through domain boundaries
    # Inlet (x=0): integrate u[0,j]*dy over open faces that are adjacent to fluid cells
    inlet_flux = 0.0
    for j in range(ny):
        if fluid_P[0, j]:
            inlet_flux += u[0, j] * dy
    # Outlet (x=L): u[nx,j]
    outlet_flux = 0.0
    for j in range(ny):
        if fluid_P[nx - 1, j]:
            outlet_flux += u[nx, j] * dy
    # Walls: v at bottom/top boundaries ideally zero; compute side imbalance as difference
    net = inlet_flux - outlet_flux  # positive if accumulation
    denom = abs(inlet_flux) if abs(inlet_flux) > 1e-12 else 1.0
    return abs(net) / denom, inlet_flux, outlet_flux


def setup_plot(XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, params):
    plt.ion()
    fig = plt.figure(figsize=(11, 8))
    gs = fig.add_gridspec(2, 2, height_ratios=[2.0, 1.0])
    ax0 = fig.add_subplot(gs[0, :])
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])

    speed = np.sqrt(Uc ** 2 + Vc ** 2)
    speed_masked = ma.array(speed.T, mask=~fluid_P.T)
    im = ax0.imshow(speed_masked, origin="lower", extent=[XP.min(), XP.max(), YP.min(), YP.max()], aspect="auto", cmap="viridis")
    cbar = fig.colorbar(im, ax=ax0, fraction=0.046, pad=0.04)
    cbar.set_label("|U|")

    # Quiver on cell centers (downsample)
    ds = params.quiver_ds
    Xc = XP[::ds, ::ds]
    Yc = YP[::ds, ::ds]
    Uc_ds = Uc[::ds, ::ds]
    Vc_ds = Vc[::ds, ::ds]
    qv = ax0.quiver(Xc, Yc, Uc_ds.T, Vc_ds.T, color="white", scale=30)

    ax0.set_title("Velocity magnitude with quiver (Backward-Facing Step)")
    ax0.set_xlim([XP.min(), XP.max()])
    ax0.set_ylim([YP.min(), YP.max()])

    # Residual plot
    ax1.set_title("Residuals")
    ax1.set_yscale("log")
    (line_ru,) = ax1.plot(res_hist["u"], label="u")
    (line_rv,) = ax1.plot(res_hist["v"], label="v")
    (line_rp,) = ax1.plot(res_hist["p"], label="p")
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Residual")
    ax1.legend(loc="best")

    # Mass imbalance plot
    ax2.set_title("Global mass imbalance")
    (line_imb,) = ax2.plot(imb_hist, color="tab:red")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("|Net flux| / Inlet flux")
    ax2.set_ylim([1e-4, 1])
    ax2.set_yscale("log")

    fig.tight_layout()
    plt.pause(0.001)

    # Fix color limits after first draw
    im.set_clim(vmin=0.0, vmax=max(1.0, speed_masked.max()))

    return fig, (ax0, ax1, ax2), im, qv, (line_ru, line_rv, line_rp), line_imb, ds


def update_plot(axs, im, qv, lines_res, line_imb, XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, ds):
    # Update scalar field
    speed = np.sqrt(Uc ** 2 + Vc ** 2)
    speed_masked = ma.array(speed.T, mask=~fluid_P.T)
    im.set_data(speed_masked)

    # Update quiver (downsampled)
    Xc = XP[::ds, ::ds]
    Yc = YP[::ds, ::ds]
    Uc_ds = Uc[::ds, ::ds]
    Vc_ds = Vc[::ds, ::ds]
    qv.set_UVC(Uc_ds.T, Vc_ds.T)

    # Residuals
    lines_res[0].set_data(np.arange(len(res_hist["u"])), res_hist["u"])
    lines_res[1].set_data(np.arange(len(res_hist["v"])), res_hist["v"])
    lines_res[2].set_data(np.arange(len(res_hist["p"])), res_hist["p"])
    axs[1].relim(); axs[1].autoscale_view()

    # Imbalance
    line_imb.set_data(np.arange(len(imb_hist)), imb_hist)
    axs[2].relim(); axs[2].autoscale_view()

    plt.draw(); plt.pause(0.001)


def main():
    parser = argparse.ArgumentParser(description="2D BFS SIMPLE (NumPy) with live visualization")
    parser.add_argument("--nx", type=int, default=240)
    parser.add_argument("--ny", type=int, default=80)
    parser.add_argument("--max-iters", type=int, default=3000)
    parser.add_argument("--plot-interval", type=int, default=20)
    parser.add_argument("--demo", action="store_true", help="Run a quick demo (smaller grid, fewer iterations)")
    args = parser.parse_args()

    if args.demo:
        nx, ny = 96, 32
        max_iters = 400
        plot_interval = 10
    else:
        nx, ny = args.nx, args.ny
        max_iters = args.max_iters
        plot_interval = args.plot_interval

    prm = Params(nx=nx, ny=ny, max_iters=max_iters, plot_interval=plot_interval)

    np.random.seed(prm.seed)

    # Grid and geometry
    fluid_P, fluid_u, fluid_v, dx, dy, XP, YP = build_geometry_masks(prm.nx, prm.ny, prm.Lx, prm.Ly, prm.H, prm.h)

    # Fields
    p = np.zeros((prm.nx, prm.ny))
    u = np.zeros((prm.nx + 1, prm.ny))
    v = np.zeros((prm.nx, prm.ny + 1))

    mu = prm.rho / prm.Re

    # Initial BCs
    apply_velocity_bcs(u, v, prm, fluid_u, fluid_v, dy)

    # Visualization setup (initial field at P centers)
    Uc = 0.5 * (u[0:prm.nx, :] + u[1:prm.nx + 1, :])
    Vc = 0.5 * (v[:, 0:prm.ny] + v[:, 1:prm.ny + 1])

    res_hist = {"u": [], "v": [], "p": []}
    imb_hist = []

    fig, axs, im, qv, lines_res, line_imb, ds = setup_plot(XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, prm)

    # Convergence tracking
    init_res = None

    start = time.time()
    for it in range(1, prm.max_iters + 1):
        # 1) Build momentum equations
        AWu, AEu, ASu, ANu, APu, bu = build_momentum_u(u, v, p, mu, dx, dy, fluid_u, fluid_P, prm.alpha_u)
        AWv, AEv, ASv, ANv, APv, bv = build_momentum_v(u, v, p, mu, dx, dy, fluid_v, fluid_P, prm.alpha_u)

        # 2) Solve momentum for u*, v* (Gauss–Seidel SOR)
        u_star = u.copy()
        v_star = v.copy()
        u_star = gs_sor_scalar(AWu, AEu, ASu, ANu, APu, bu, u_star, fluid_u, prm.omega_mom, prm.mom_sweeps)
        v_star = gs_sor_scalar(AWv, AEv, ASv, ANv, APv, bv, v_star, fluid_v, prm.omega_mom, prm.mom_sweeps)

        # Re-apply BCs to u*, v*
        apply_velocity_bcs(u_star, v_star, prm, fluid_u, fluid_v, dy)

        # 3) Build and solve pressure correction
        AWp, AEp, ASp, ANp, APp, bp, d_e, d_w, d_n, d_s = build_pressure_correction(u_star, v_star, APu, APv, fluid_P, dx, dy)
        pcor = np.zeros_like(p)
        pcor = gs_sor_scalar(AWp, AEp, ASp, ANp, APp, bp, pcor, fluid_P, prm.omega_p, prm.pcor_sweeps)

        # 4) Correct velocities and pressure
        u = u_star.copy(); v = v_star.copy()
        correct_uvp(u, v, p, pcor, fluid_P, dx, dy, d_e, d_w, d_n, d_s, prm.alpha_p)
        # Clip velocities to maintain stability in the educational solver
        np.clip(u, -5.0, 5.0, out=u)
        np.clip(v, -5.0, 5.0, out=v)

        # Apply BCs again
        apply_velocity_bcs(u, v, prm, fluid_u, fluid_v, dy)

        # Residuals
        ru = compute_residuals_u(AWu, AEu, ASu, ANu, APu, bu, u, fluid_u)
        rv = compute_residuals_v(AWv, AEv, ASv, ANv, APv, bv, v, fluid_v)
        # Pressure residual: L1 norm of divergence
        div = (u[1:prm.nx + 1, :] - u[0:prm.nx, :]) * dy + (v[:, 1:prm.ny + 1] - v[:, 0:prm.ny]) * dx
        rp = np.mean(np.abs(div[fluid_P]))

        res_hist["u"].append(ru)
        res_hist["v"].append(rv)
        res_hist["p"].append(rp)

        imb, inflow, outflow = global_mass_imbalance(u, v, fluid_P, dx, dy)
        imb_hist.append(imb)

        if init_res is None and len(res_hist["u"]) >= 2:
            init_res = (res_hist["u"][0], res_hist["v"][0], res_hist["p"][0])

        # Logging
        if it % 10 == 0 or it == 1:
            print(f"Iter {it:5d}: Ru={ru:.3e}, Rv={rv:.3e}, Rp={rp:.3e}, MassImb={imb*100:.2f}%")

        # 5) Visualization update
        if (it % prm.plot_interval == 0) or (it == 1):
            Uc = 0.5 * (u[0:prm.nx, :] + u[1:prm.nx + 1, :])
            Vc = 0.5 * (v[:, 0:prm.ny] + v[:, 1:prm.ny + 1])
            update_plot(axs, im, qv, lines_res, line_imb, XP, YP, fluid_P, Uc, Vc, res_hist, imb_hist, ds)

        # 6) Convergence check
        done = False
        if init_res is not None:
            ruf = res_hist["u"][-1] / (init_res[0] + 1e-30)
            rvf = res_hist["v"][-1] / (init_res[1] + 1e-30)
            rpf = res_hist["p"][-1] / (init_res[2] + 1e-30)
            if (ruf <= 1e-3) and (rvf <= 1e-3) and (rpf <= 1e-3) and (imb <= 5e-3):
                done = True
        if done:
            print("Converged: residuals dropped >=3 orders and mass imbalance <= 0.5%.")
            break

    elapsed = time.time() - start
    print(f"Finished at iter {it} in {elapsed:.1f}s.")

    # Final draw to keep the window responsive
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
