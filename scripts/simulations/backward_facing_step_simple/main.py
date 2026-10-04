#!/usr/bin/env python3
"""Steady 2D laminar flow over a backward-facing step, solved with SIMPLE.

The incompressible Navier-Stokes equations are discretised with the finite
volume method on a staggered (MAC) grid using first-order upwind convection
and central diffusion. Pressure and velocity are coupled with Patankar's SIMPLE
algorithm; every linear system is relaxed with Gauss-Seidel/SOR sweeps
compiled with Numba. The animation follows the outer iterations: the velocity
magnitude with arrows and the reattachment point behind the step, the residual
history and the global mass imbalance. The final iteration count and
reattachment length are printed at the end.
"""

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from matplotlib.patches import Rectangle
from numba import njit

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402
from _common import positive_int  # noqa: E402

DTYPE = np.float32

# Animation: one frame is STEPS_PER_FRAME SIMPLE (outer) iterations.
STEPS_PER_FRAME = 20  # SIMPLE iterations per animation frame
N_FRAMES = 150  # default frames: at most 3000 iterations

# Convergence test, checked after every iteration
REFERENCE_ITERATIONS = 10  # residuals are scaled by their maximum over these
RESIDUAL_DROP = 1e-3  # every residual below this fraction of its reference
MAX_IMBALANCE = 5e-3  # and |inflow - outflow| / inflow at most 0.5 %

# View
REEL_X_RANGE = (2.0, 12.0)  # part of the channel shown in a reel (x in units of H)
ARROW_ROWS = 16  # arrows across the channel height (fewer if ny is smaller)


@dataclass
class Params:
    """Geometry, flow and solver settings; lengths in units of the inlet height."""

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


@njit(cache=False)
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


@njit(cache=False)
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


@njit(cache=False)
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


@njit(cache=False)
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


class BackwardStepSimulation(Simulation):
    """SIMPLE state on the staggered grid; one step is one outer iteration.

    ``residuals`` (u-momentum, v-momentum, continuity) and ``imbalance`` hold
    one entry per iteration. ``time`` is the iteration count, and the solver
    is ``done`` once the convergence test passes.
    """

    def __init__(self, params=None):
        super().__init__()
        prm = Params() if params is None else params
        if prm.nx < 1 or prm.ny < 1:
            raise ValueError("nx and ny must be positive")
        self.prm = prm
        geometry = build_geometry_masks(prm)
        self.fluid_P, self.fluid_u, self.fluid_v = geometry[:3]  # fluid masks
        self.dx, self.dy, self.XP, self.YP = geometry[3:]  # spacing, cell centres
        self.mu = prm.rho * prm.U_avg * prm.H / prm.Re
        self.p = np.zeros((prm.nx, prm.ny), dtype=DTYPE)
        self.u = np.zeros((prm.nx + 1, prm.ny), dtype=DTYPE)
        self.v = np.zeros((prm.nx, prm.ny + 1), dtype=DTYPE)
        apply_velocity_bcs(self.u, self.v, prm, self.fluid_u, self.fluid_v, self.dy)

        self.idx_u = precompute_indices(self.fluid_u)
        self.idx_v = precompute_indices(self.fluid_v)
        self.idx_p = precompute_indices(self.fluid_P)
        # AW, AE, AS, AN, AP, b of the momentum equations, reassembled every step
        self.coeff_u = tuple(np.zeros_like(self.u) for _ in range(6))
        self.coeff_v = tuple(np.zeros_like(self.v) for _ in range(6))
        self.u_star = self.u.copy()
        self.v_star = self.v.copy()
        self.pcor = np.zeros_like(self.p)

        self.residuals = {"u": [], "v": [], "p": []}
        self.imbalance = []  # |inflow - outflow| / inflow after each iteration
        self.reference = None  # residual maxima over the first iterations
        self.converged = False

    @property
    def time(self):
        return self.steps

    @property
    def done(self):
        return self.converged

    def step(self):
        prm = self.prm
        u, v, p = self.u, self.v, self.p
        u_star, v_star, pcor = self.u_star, self.v_star, self.pcor
        momentum = (prm.rho, self.dx, self.dy, self.fluid_P, prm.alpha_u)

        # --- predictor: momentum equations with the current pressure ---
        build_momentum_u(u, v, p, self.mu, *momentum, *self.coeff_u, *self.idx_u)
        build_momentum_v(u, v, p, self.mu, *momentum, *self.coeff_v, *self.idx_v)
        ru = momentum_residual(*self.coeff_u, u, *self.idx_u)
        rv = momentum_residual(*self.coeff_v, v, *self.idx_v)
        np.copyto(u_star, u)
        np.copyto(v_star, v)
        sweeps = (prm.omega_mom, prm.mom_sweeps)
        gs_sor_scalar(*self.coeff_u, u_star, *self.idx_u, *sweeps)
        gs_sor_scalar(*self.coeff_v, v_star, *self.idx_v, *sweeps)
        apply_velocity_bcs(u_star, v_star, prm, self.fluid_u, self.fluid_v, self.dy)

        # --- pressure correction (p' = 0 at the outlet) ---
        APu, APv = self.coeff_u[4], self.coeff_v[4]
        AWp, AEp, ASp, ANp, APp, bp, du, dv = build_pressure_correction(
            u_star, v_star, APu, APv, prm,
            self.fluid_P, self.fluid_u, self.fluid_v, self.dx, self.dy,
        )  # fmt: skip
        rp = float(np.mean(np.abs(bp[self.fluid_P])))  # continuity residual of u*
        pcor.fill(0.0)
        gs_sor_scalar(
            AWp, AEp, ASp, ANp, APp, bp, pcor, *self.idx_p,
            prm.omega_p, prm.pcor_sweeps,
        )  # fmt: skip

        # --- corrector ---
        np.copyto(u, u_star)
        np.copyto(v, v_star)
        correct_uvp(u, v, p, pcor, du, dv, prm.alpha_p)
        apply_velocity_bcs(u, v, prm, self.fluid_u, self.fluid_v, self.dy)

        # --- monitors and convergence test ---
        for key, value in zip("uvp", (ru, rv, rp)):
            self.residuals[key].append(value)
        imbalance = global_mass_imbalance(u, self.fluid_P, self.dy)[0]
        self.imbalance.append(imbalance)
        if len(self.imbalance) == REFERENCE_ITERATIONS:
            self.reference = [max(self.residuals[key]) for key in "uvp"]
        if self.reference is not None:
            drops = [
                self.residuals[key][-1] / (r + 1e-30)
                for key, r in zip("uvp", self.reference)
            ]
            self.converged = max(drops) <= RESIDUAL_DROP and imbalance <= MAX_IMBALANCE

    def mass_imbalance(self):
        """|inflow - outflow| / inflow of the current velocity field."""
        return global_mass_imbalance(self.u, self.fluid_P, self.dy)[0]

    def reattachment(self):
        """Bottom-wall reattachment length x_r / h, or None without recirculation."""
        return reattachment_length(self.u, self.prm, self.dx)


def log_limits(values, floor, ceiling):
    """Log-axis limits around the positive values, at least [floor, ceiling]."""
    values = values[np.isfinite(values) & (values > 0)]
    if values.size == 0:
        return floor, ceiling
    return min(floor, 0.5 * values.min()), max(ceiling, 2.0 * values.max())


class BackwardStepView(View):
    """Velocity magnitude with arrows above the residual and imbalance histories.

    The window shows the whole channel, with the vertical scale exaggerated,
    above the two histories side by side. A reel crops the field to the step
    and the recirculation zone and stacks it above the two histories, which
    share the iteration axis. Colours and arrow lengths are fixed by the inlet
    peak speed, so every frame uses the same scale.
    """

    figsize = (11.0, 8.0)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        sim, prm = simulation, simulation.prm
        if portrait:
            mosaic, heights = [["field"], ["residual"], ["imbalance"]], [1.5, 1, 1]
        else:
            mosaic, heights = [["field", "field"], ["residual", "imbalance"]], [2, 1]
        axes = figure.subplot_mosaic(mosaic, height_ratios=heights)
        self.axes = axes

        # velocity magnitude, arrows and reattachment point
        ax = axes["field"]
        peak = 1.5 * prm.U_avg  # centreline speed of the parabolic inlet profile
        self.image = ax.imshow(
            self.speed(), extent=(0.0, prm.Lx, 0.0, prm.Ly), aspect="auto",
            cmap="viridis", vmin=0.0, vmax=peak, interpolation="bilinear",
        )  # fmt: skip
        figure.colorbar(self.image, ax=ax, label="|U|")
        solid = ~sim.fluid_P  # the step as resolved by the grid, drawn in grey
        step_size = (solid.any(axis=1).sum() * sim.dx, solid.any(axis=0).sum() * sim.dy)
        ax.add_patch(Rectangle((0.0, 0.0), *step_size, color="0.45", zorder=2))
        self.ds = max(1, round(prm.ny / ARROW_ROWS))
        # the inlet peak speed draws an arrow 0.9 arrow spacings long
        self.fac = 0.9 * self.ds * float(sim.dx) / peak
        uc, vc = cell_centre_velocity(sim.u, sim.v)
        self.quiver = ax.quiver(
            sim.XP[:: self.ds, :: self.ds], sim.YP[:: self.ds, :: self.ds],
            quiver_component(uc, self.fac, sim.fluid_P, self.ds),
            quiver_component(vc, self.fac, sim.fluid_P, self.ds),
            color="white", scale=1.0, scale_units="xy", angles="xy", pivot="mid",
            width=0.0025 if portrait else 0.0018, zorder=3,
        )  # fmt: skip
        (self.marker,) = ax.plot(
            [], [], "v", color="#ff6b6b", markersize=14, clip_on=False, zorder=4
        )
        self.marker.set_in_layout(False)  # an empty unclipped line sits at (0, 0)
        ax.set(xlim=REEL_X_RANGE if portrait else (0.0, prm.Lx), ylim=(0.0, prm.Ly))
        ax.set(xlabel="x", ylabel="y")
        self.field_title = ax.set_title(" ")

        # residual and mass-imbalance histories against the iteration count
        ax = axes["residual"]
        self.residual_lines = {
            key: ax.plot([], [], label=label)[0]
            for key, label in zip("uvp", ("u-momentum", "v-momentum", "continuity"))
        }
        ax.set(yscale="log", ylabel="mean |residual|")
        if portrait:  # a one-row legend above the panel doubles as its title
            ax.legend(
                loc="lower center", bbox_to_anchor=(0.5, 1.0), ncols=3,
                frameon=False, borderaxespad=0.1, handlelength=1.2,
            )  # fmt: skip
        else:
            ax.legend(loc="lower left")
            ax.set_title("Residuals")
        self.converged_label = ax.text(
            0.98, 0.95, "", transform=ax.transAxes, ha="right", va="top",
            color="#90be6d", fontweight="bold",
        )  # fmt: skip

        ax = axes["imbalance"]
        ax.axhline(100 * MAX_IMBALANCE, color="0.6", linestyle="--", linewidth=1)
        (self.imbalance_line,) = ax.plot([], [], color="#f4a261")
        ax.set(yscale="log", xlabel="iteration", ylabel="imbalance [%]")
        ax.set_title("Mass imbalance (dashed: 0.5 % target)")
        if portrait:
            ax.sharex(axes["residual"])
            axes["residual"].tick_params(labelbottom=False)
        else:
            axes["residual"].set_xlabel("iteration")

    def speed(self):
        """Velocity magnitude at the cell centres (zero in the step), rows along y."""
        uc, vc = cell_centre_velocity(self.simulation.u, self.simulation.v)
        return np.sqrt(uc**2 + vc**2, dtype=DTYPE).T

    def draw(self):
        sim, prm = self.simulation, self.simulation.prm
        self.image.set_data(self.speed())
        uc, vc = cell_centre_velocity(sim.u, sim.v)
        self.quiver.set_UVC(
            quiver_component(uc, self.fac, sim.fluid_P, self.ds),
            quiver_component(vc, self.fac, sim.fluid_P, self.ds),
        )
        x_r = sim.reattachment()
        if x_r is None:
            self.marker.set_data([], [])
            self.field_title.set_text("Velocity magnitude, no recirculation")
        else:
            self.marker.set_data([prm.step_length + x_r * prm.h], [0.0])
            self.field_title.set_text(
                f"Velocity magnitude, reattachment (▼) at $x_r/h$ = {x_r:.2f}"
            )

        n = len(sim.imbalance)
        iterations = np.arange(1, n + 1)
        residuals = np.array([sim.residuals[key] for key in "uvp"], dtype=float)
        for key, values in zip("uvp", residuals.reshape(3, n)):
            self.residual_lines[key].set_data(iterations, values)
        imbalance = 100 * np.asarray(sim.imbalance, dtype=float)
        self.imbalance_line.set_data(iterations, imbalance)
        for name in ("residual", "imbalance"):
            self.axes[name].set_xlim(0, max(n, 10))
        self.axes["residual"].set_ylim(*log_limits(residuals.ravel(), 1e-6, 1e-4))
        self.axes["imbalance"].set_ylim(*log_limits(imbalance, 0.1, 100.0))
        self.converged_label.set_text("converged" if sim.converged else "")

    def status(self):
        imbalance = 100 * self.simulation.mass_imbalance()
        return f"iteration {self.simulation.time}, mass imbalance {imbalance:.2f} %"


ANIMATION = Animation(
    title="Backward-Facing Step",
    subtitle=f"SIMPLE iterations to steady flow at Re = {Params.Re:g}",
    filename="backward_facing_step.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label="SIMPLE iterations",
)


def main(argv=None):
    parser = ANIMATION.parser(__doc__)
    parser.add_argument(
        "--nx",
        type=positive_int,
        default=Params.nx,
        help="pressure cells along the channel (default: %(default)s)",
    )
    parser.add_argument(
        "--ny",
        type=positive_int,
        default=Params.ny,
        help="pressure cells across the channel (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    simulation = BackwardStepSimulation(Params(nx=args.nx, ny=args.ny))
    ANIMATION.run(args, simulation, BackwardStepView)
    outcome = "Converged after" if simulation.converged else "Not converged after"
    x_r = simulation.reattachment()
    reattachment = (
        "no recirculation on the bottom wall"
        if x_r is None
        else f"reattachment length x_r/h = {x_r:.2f}"
    )
    print(
        f"{outcome} {simulation.steps} SIMPLE iterations "
        f"(mass imbalance {100 * simulation.mass_imbalance():.2f} %); {reattachment}"
    )


if __name__ == "__main__":
    main()
