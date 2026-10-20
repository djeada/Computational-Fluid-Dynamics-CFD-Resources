"""Validate a D2Q9 BGK lattice Boltzmann solver on body-force-driven Poiseuille flow.

A channel of width H (lattice units) is periodic in x and closed by half-way
bounce-back walls at y = 0 and y = H, which lie halfway between the wall-adjacent
fluid node and the (virtual) solid node. A uniform body force with Guo et al.
(2002) forcing drives the flow, and the steady velocity profile is compared with
the exact parabola for several relaxation times tau. The figure shows the
profiles, the second-order decrease of the L2 error with resolution, and the
tau-dependent wall slip of BGK bounce-back, which vanishes at
tau = 1/2 + sqrt(3/16).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numba import njit

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# D2Q9 lattice in lattice units (dx = dt = 1), counter-clockwise ordering:
# 0 rest, 1-4 axis directions (E, N, W, S), 5-8 diagonals (NE, NW, SW, SE).
VELOCITIES = np.array(
    [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
)
WEIGHTS = np.array([4 / 9] + [1 / 9] * 4 + [1 / 36] * 4)
OPPOSITE = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6])
CS2 = 1.0 / 3.0  # squared lattice speed of sound c_s^2 [-]

# Flow set-up (lattice units)
U_MAX = 0.05  # centreline velocity of the exact profile; Ma = U_MAX / c_s = 0.087
NX = 1  # nodes along the periodic x direction (the flow is invariant in x)
DECAY_TIMES = 20.0  # run length in units of the slowest viscous time H^2 / (pi^2 nu)

# Studies shown in the figure
PROFILE_WIDTH = 8  # channel width H [nodes] of the profile panel
PROFILE_TAUS = (0.6, 1.0, 2.0)
RESOLUTIONS = (8, 16, 32, 64, 128)  # channel widths H of the convergence study
CONVERGENCE_TAUS = (0.8, 1.0, 1.5)
SCAN_WIDTH = 16  # channel width of the slip-versus-tau scan
SCAN_TAUS = (0.51, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0)
MAGIC_TAU = 0.5 + np.sqrt(3.0 / 16.0)  # (tau - 1/2)^2 = 3/16: exact wall location


def viscosity(tau):
    """Lattice kinematic viscosity nu = c_s^2 (tau - 1/2) of the BGK scheme."""
    return CS2 * (tau - 0.5)


def equilibrium(rho, ux, uy):
    """Second-order D2Q9 equilibrium f_i^eq for arrays rho, ux, uy; shape (9, ...)."""
    cu = VELOCITIES[:, 0, None, None] * ux + VELOCITIES[:, 1, None, None] * uy
    usq = ux**2 + uy**2
    return (
        WEIGHTS[:, None, None]
        * rho
        * (1.0 + cu / CS2 + cu**2 / (2 * CS2**2) - usq / (2 * CS2))
    )


@njit(cache=False)
def advance(f, tau, force, n_steps, cx, cy, w, opposite):
    """Advance populations f (9, nx, ny) by n_steps collide-and-stream updates.

    BGK collision with the Guo forcing term for a body force density (force, 0),
    push streaming that is periodic in x, and half-way bounce-back at the walls
    below y = 0 and above y = ny - 1: a population that would leave the fluid
    returns to the node it left, in the opposite direction, one step later.
    """
    q, nx, ny = f.shape
    f_new = np.empty_like(f)
    for _ in range(n_steps):
        for x in range(nx):
            for y in range(ny):
                rho = 0.0
                mx = 0.0
                my = 0.0
                for i in range(q):
                    rho += f[i, x, y]
                    mx += f[i, x, y] * cx[i]
                    my += f[i, x, y] * cy[i]
                ux = (mx + 0.5 * force) / rho  # Guo: half the force enters u
                uy = my / rho
                usq = ux * ux + uy * uy
                for i in range(q):
                    cu = cx[i] * ux + cy[i] * uy
                    feq = w[i] * rho * (1.0 + 3.0 * cu + 4.5 * cu * cu - 1.5 * usq)
                    source = (
                        (1.0 - 0.5 / tau)
                        * w[i]
                        * (3.0 * (cx[i] - ux) + 9.0 * cu * cx[i])
                        * force
                    )
                    post = f[i, x, y] - (f[i, x, y] - feq) / tau + source
                    y_target = y + cy[i]
                    if y_target < 0 or y_target >= ny:
                        f_new[opposite[i], x, y] = post  # half-way bounce-back
                    else:
                        f_new[i, (x + cx[i]) % nx, y_target] = post
        f, f_new = f_new, f
    return f


def node_positions(width):
    """Distance of the fluid nodes from the lower wall, y_j = j + 1/2."""
    return np.arange(width) + 0.5


def driving_force(width, tau, u_max=U_MAX):
    """Body force density g that gives centreline velocity u_max: g = 8 nu u_max / H^2."""
    return 8.0 * viscosity(tau) * u_max / width**2


def exact_profile(y, width, tau, force):
    """Plane Poiseuille profile u(y) = g y (H - y) / (2 nu) with walls at 0 and H."""
    return force * y * (width - y) / (2.0 * viscosity(tau))


def predicted_slip(tau, force):
    """BGK bounce-back slip velocity u_s = g (16 Lambda - 3) / (24 nu), Lambda = (tau - 1/2)^2."""
    return force * (16.0 * (tau - 0.5) ** 2 - 3.0) / (24.0 * viscosity(tau))


def macroscopic(f, force):
    """Density and x velocity (force-corrected) of populations f (9, nx, ny)."""
    rho = f.sum(axis=0)
    ux = (np.tensordot(VELOCITIES[:, 0], f, axes=1) + 0.5 * force) / rho
    return rho, ux


def simulate_channel(width, tau, u_max=U_MAX, nx=NX, decay_times=DECAY_TIMES):
    """Run the channel to steady state; return y, LBM profile, exact profile, steps.

    The populations start at equilibrium with the exact profile, and the run
    lasts decay_times slowest viscous time scales H^2 / (pi^2 nu), so that the
    start-up transient has decayed by a factor exp(-decay_times).
    """
    force = driving_force(width, tau, u_max)
    y = node_positions(width)
    u_exact = exact_profile(y, width, tau, force)
    ux = np.broadcast_to(u_exact, (nx, width))
    f = equilibrium(np.ones((nx, width)), ux, np.zeros((nx, width)))
    n_steps = int(np.ceil(decay_times * width**2 / (np.pi**2 * viscosity(tau))))
    f = advance(
        f,
        tau,
        force,
        n_steps,
        VELOCITIES[:, 0].copy(),
        VELOCITIES[:, 1].copy(),
        WEIGHTS,
        OPPOSITE,
    )
    _, u = macroscopic(f, force)
    return y, u.mean(axis=0), u_exact, n_steps


def relative_l2_error(u, u_exact):
    """||u - u_exact||_2 / ||u_exact||_2 over the fluid nodes."""
    return np.linalg.norm(u - u_exact) / np.linalg.norm(u_exact)


def convergence_study(taus=CONVERGENCE_TAUS, widths=RESOLUTIONS):
    """Relative L2 error for every (tau, H); returns an array (len(taus), len(widths))."""
    errors = np.empty((len(taus), len(widths)))
    for a, tau in enumerate(taus):
        for b, width in enumerate(widths):
            _, u, u_exact, _ = simulate_channel(width, tau)
            errors[a, b] = relative_l2_error(u, u_exact)
    return errors


def slip_scan(taus=SCAN_TAUS, width=SCAN_WIDTH):
    """Measured mean slip u - u_exact in units of g / nu for each tau."""
    slips = []
    for tau in taus:
        _, u, u_exact, _ = simulate_channel(width, tau)
        force = driving_force(width, tau)
        slips.append(np.mean(u - u_exact) * viscosity(tau) / force)
    return np.array(slips)


def observed_orders(errors, widths=RESOLUTIONS):
    """Observed order log(e_k / e_k+1) / log(H_k+1 / H_k) between successive widths."""
    widths = np.asarray(widths, dtype=float)
    return np.log(errors[..., :-1] / errors[..., 1:]) / np.log(widths[1:] / widths[:-1])


def make_figure(profiles, errors, slips):
    """Three panels: profiles, error versus resolution, slip versus tau."""
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))
    colors = plt.cm.tab10.colors

    ax = axes[0]
    y_fine = np.linspace(0.0, PROFILE_WIDTH, 200)
    ax.plot(
        y_fine / PROFILE_WIDTH,
        4 * y_fine * (PROFILE_WIDTH - y_fine) / PROFILE_WIDTH**2,
        "k-",
        linewidth=1.5,
        label="exact",
    )
    for color, (tau, (y, u, _)) in zip(colors, profiles.items()):
        ax.plot(
            y / PROFILE_WIDTH,
            u / U_MAX,
            "o",
            color=color,
            markersize=7,
            label=rf"LBM, $\tau = {tau:g}$",
        )
    ax.set_xlabel(r"Wall-normal position $y / H$ [-]", fontsize=11)
    ax.set_ylabel(r"Velocity $u / u_{\max}$ [-]", fontsize=11)
    ax.set_title(f"(a) Steady profiles, H = {PROFILE_WIDTH} nodes", fontsize=12)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.25)
    ax.legend(fontsize=10, loc="lower center")
    ax.grid(alpha=0.3)

    ax = axes[1]
    widths = np.array(RESOLUTIONS, dtype=float)
    for color, tau, err in zip(colors, CONVERGENCE_TAUS, errors):
        ax.loglog(widths, err, "o-", color=color, label=rf"$\tau = {tau:g}$")
    reference = 0.4 * errors[1, 0] * (widths / widths[0]) ** -2
    ax.loglog(widths, reference, "k--", linewidth=1, label="slope $-2$")
    ax.set_xlabel("Channel width H [nodes]", fontsize=11)
    ax.set_ylabel(r"Relative $L_2$ error [-]", fontsize=11)
    ax.set_title("(b) Convergence with resolution", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, which="both")

    ax = axes[2]
    tau_fine = np.linspace(0.505, 2.0, 300)
    ax.plot(
        tau_fine,
        predicted_slip(tau_fine, 1.0) * viscosity(tau_fine),
        "k-",
        linewidth=1.5,
        label=r"$(16\Lambda - 3)/24$",
    )
    ax.plot(SCAN_TAUS, slips, "o", color=colors[0], markersize=7, label="LBM, H = 16")
    ax.axhline(0.0, color="0.5", linewidth=0.8)
    ax.axvline(MAGIC_TAU, color=colors[3], linestyle=":", linewidth=1.5)
    ax.annotate(
        rf"$\tau = 1/2 + \sqrt{{3/16}} \approx {MAGIC_TAU:.3f}$",
        xy=(MAGIC_TAU, 0.0),
        xytext=(0.52, 0.55),
        fontsize=10,
        color=colors[3],
        arrowprops={"arrowstyle": "->", "color": colors[3]},
    )
    ax.set_xlabel(r"Relaxation time $\tau$ [-]", fontsize=11)
    ax.set_ylabel(r"Wall slip $u_s\,\nu / g$ [-]", fontsize=11)
    ax.set_title(r"(c) Bounce-back slip, $\Lambda = (\tau - 1/2)^2$", fontsize=12)
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    profiles = {}
    for tau in PROFILE_TAUS:
        y, u, u_exact, n_steps = simulate_channel(PROFILE_WIDTH, tau)
        profiles[tau] = (y, u, u_exact)
        print(
            f"H = {PROFILE_WIDTH}, tau = {tau:g}: {n_steps} steps, relative L2 error "
            f"{relative_l2_error(u, u_exact):.3e}"
        )

    errors = convergence_study()
    orders = observed_orders(errors)
    for tau, err, order in zip(CONVERGENCE_TAUS, errors, orders):
        print(
            f"tau = {tau:g}: errors "
            + ", ".join(f"{e:.2e}" for e in err)
            + "; observed orders "
            + ", ".join(f"{p:.3f}" for p in order)
        )

    slips = slip_scan()
    predicted = predicted_slip(np.array(SCAN_TAUS), 1.0) * viscosity(
        np.array(SCAN_TAUS)
    )
    print(
        "max |measured - predicted| slip (units of g/nu): "
        f"{np.max(np.abs(slips - predicted)):.2e}"
    )
    _, u, u_exact, _ = simulate_channel(SCAN_WIDTH, MAGIC_TAU)
    print(
        f"tau = {MAGIC_TAU:.4f} (exact wall location), H = {SCAN_WIDTH}: "
        f"relative L2 error {relative_l2_error(u, u_exact):.2e}"
    )

    finish_figures(
        {"lbm_poiseuille_validation.png": make_figure(profiles, errors, slips)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
