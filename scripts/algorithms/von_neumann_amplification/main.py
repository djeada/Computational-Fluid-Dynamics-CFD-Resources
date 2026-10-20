"""Von Neumann amplification factors of classic advection and diffusion schemes.

Evaluates the amplification factor G(theta) of FTCS, first-order upwind,
Lax-Friedrichs and Lax-Wendroff for u_t + a u_x = 0 and of FTCS, BTCS and
Crank-Nicolson for u_t = nu u_xx, where theta = k dx is the phase angle of a
Fourier mode per cell. It then marches a square wave on a periodic grid with
each scheme, so the damping, dispersion and growth that |G| and arg(G) predict
can be seen in the solution.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

COURANT = 0.8  # C = a dt / dx for the advection panels
UNSTABLE_COURANT = 1.1  # upwind above the CFL limit
N_CELLS = 100  # periodic grid on [0, 1)
PULSE = (0.2, 0.4)  # square wave u = 1 on this interval, 0 elsewhere
GROWTH_STEPS = 60  # steps in the growth panel
DIFFUSION_NUMBERS = (0.25, 0.5, 0.6)  # r = nu dt / dx^2 for FTCS in the G panel
IMPLICIT_R = 5.0  # r for BTCS and Crank-Nicolson
DIFFUSION_TIME = 1.0e-3  # nu t for the diffusion march (m^2 with nu in m^2/s, t in s)
DIFFUSION_MARCH = (
    ("FTCS", 0.55),
    ("FTCS", 0.45),
    ("BTCS", IMPLICIT_R),
    ("Crank-Nicolson", IMPLICIT_R),
)

ADVECTION_SCHEMES = ("FTCS", "Upwind", "Lax-Friedrichs", "Lax-Wendroff")
COLORS = dict(
    zip(ADVECTION_SCHEMES, ("tab:red", "tab:blue", "tab:green", "tab:purple"))
)


def advection_amplification(scheme, theta, c):
    """G(theta) of a two-level scheme for u_t + a u_x = 0 with a > 0 and Courant number c."""
    if scheme == "FTCS":
        return 1.0 - 1j * c * np.sin(theta)
    if scheme == "Upwind":
        return 1.0 - c * (1.0 - np.exp(-1j * theta))
    if scheme == "Lax-Friedrichs":
        return np.cos(theta) - 1j * c * np.sin(theta)
    if scheme == "Lax-Wendroff":
        return 1.0 - 1j * c * np.sin(theta) - c**2 * (1.0 - np.cos(theta))
    raise ValueError(scheme)


def diffusion_amplification(scheme, theta, r):
    """G(theta) for u_t = nu u_xx with r = nu dt / dx^2 (real for all three schemes)."""
    s = np.sin(0.5 * theta) ** 2
    if scheme == "FTCS":
        return 1.0 - 4.0 * r * s
    if scheme == "BTCS":
        return 1.0 / (1.0 + 4.0 * r * s)
    if scheme == "Crank-Nicolson":
        return (1.0 - 2.0 * r * s) / (1.0 + 2.0 * r * s)
    raise ValueError(scheme)


def relative_phase_speed(scheme, theta, c):
    """Numerical over exact phase change per step, -arg(G) / (c theta); 1 is exact."""
    return -np.angle(advection_amplification(scheme, theta, c)) / (c * theta)


def advection_step(u, scheme, c):
    """One step of the named scheme on a periodic grid (a > 0)."""
    up, um = np.roll(u, -1), np.roll(u, 1)  # u_{i+1}, u_{i-1}
    if scheme == "FTCS":
        return u - 0.5 * c * (up - um)
    if scheme == "Upwind":
        return u - c * (u - um)
    if scheme == "Lax-Friedrichs":
        return 0.5 * (up + um) - 0.5 * c * (up - um)
    if scheme == "Lax-Wendroff":
        return u - 0.5 * c * (up - um) + 0.5 * c**2 * (up - 2.0 * u + um)
    raise ValueError(scheme)


def periodic_second_difference(n):
    """Dense periodic matrix of u_{i+1} - 2 u_i + u_{i-1}."""
    d = -2.0 * np.eye(n) + np.eye(n, k=1) + np.eye(n, k=-1)
    d[0, -1] = d[-1, 0] = 1.0
    return d


def diffusion_march(u0, scheme, r, steps):
    """March u_t = nu u_xx on a periodic grid with FTCS, BTCS or Crank-Nicolson."""
    n = len(u0)
    d2 = periodic_second_difference(n)
    eye = np.eye(n)
    if scheme == "FTCS":
        step = eye + r * d2
    elif scheme == "BTCS":
        step = np.linalg.inv(eye - r * d2)
    elif scheme == "Crank-Nicolson":
        step = np.linalg.solve(eye - 0.5 * r * d2, eye + 0.5 * r * d2)
    else:
        raise ValueError(scheme)
    u = u0.copy()
    for _ in range(steps):
        u = step @ u
    return u


def square_wave(x, pulse=PULSE):
    """1 inside the pulse interval, 0 outside."""
    return ((x >= pulse[0]) & (x < pulse[1])).astype(float)


def exact_diffusion(u0, nu_t):
    """Exact periodic heat-equation solution of the trigonometric interpolant of u0."""
    n = len(u0)
    k = 2.0 * np.pi * np.fft.fftfreq(n, d=1.0 / n)  # wavenumbers on [0, 1)
    return np.real(np.fft.ifft(np.fft.fft(u0) * np.exp(-(k**2) * nu_t)))


def numerical_viscosity_upwind(a, dx, c):
    """Leading-order artificial viscosity of first-order upwind: a dx (1 - c) / 2."""
    return 0.5 * a * dx * (1.0 - c)


def make_figure():
    theta = np.linspace(1e-3, np.pi, 400)
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    ax = axes[0, 0]
    for scheme in ADVECTION_SCHEMES:
        g = np.abs(advection_amplification(scheme, theta, COURANT))
        ax.plot(theta, g, color=COLORS[scheme], linewidth=2, label=scheme)
    g_unstable = np.abs(advection_amplification("Upwind", theta, UNSTABLE_COURANT))
    ax.plot(
        theta,
        g_unstable,
        "--",
        color=COLORS["Upwind"],
        label=f"Upwind, C = {UNSTABLE_COURANT}",
    )
    ax.axhline(1.0, color="k", linewidth=0.8)
    ax.set_xlabel(r"Phase angle $\theta = k\Delta x$ [rad]", fontsize=11)
    ax.set_ylabel(r"$|G(\theta)|$ [-]", fontsize=11)
    ax.set_title(f"(a) Advection: amplitude per step, C = {COURANT}", fontsize=12)
    ax.set_xlim(0, np.pi)
    ax.set_ylim(0, 1.6)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="upper left")

    ax = axes[0, 1]
    for scheme in ADVECTION_SCHEMES:
        ax.plot(
            theta,
            relative_phase_speed(scheme, theta, COURANT),
            color=COLORS[scheme],
            linewidth=2,
            label=scheme,
        )
    ax.axhline(1.0, color="k", linewidth=0.8)
    ax.set_xlabel(r"Phase angle $\theta = k\Delta x$ [rad]", fontsize=11)
    ax.set_ylabel(r"Numerical / exact phase speed [-]", fontsize=11)
    ax.set_title(f"(b) Advection: phase error, C = {COURANT}", fontsize=12)
    ax.set_xlim(0, np.pi)
    ax.set_ylim(0, 1.5)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="lower left")

    ax = axes[0, 2]
    cmap = plt.get_cmap("Reds")
    for r, shade in zip(DIFFUSION_NUMBERS, (0.45, 0.7, 0.95)):
        ax.plot(
            theta,
            diffusion_amplification("FTCS", theta, r),
            color=cmap(shade),
            linewidth=2,
            label=f"FTCS, r = {r}",
        )
    ax.plot(
        theta,
        diffusion_amplification("BTCS", theta, IMPLICIT_R),
        color="tab:blue",
        linewidth=2,
        label=f"BTCS, r = {IMPLICIT_R:g}",
    )
    ax.plot(
        theta,
        diffusion_amplification("Crank-Nicolson", theta, IMPLICIT_R),
        color="tab:green",
        linewidth=2,
        label=f"Crank-Nicolson, r = {IMPLICIT_R:g}",
    )
    ax.plot(
        theta,
        np.exp(-IMPLICIT_R * theta**2),
        "k:",
        linewidth=1.5,
        label=rf"exact $e^{{-r\theta^2}}$, r = {IMPLICIT_R:g}",
    )
    ax.axhline(-1.0, color="k", linewidth=0.8)
    ax.axhline(1.0, color="k", linewidth=0.8)
    ax.set_xlabel(r"Phase angle $\theta = k\Delta x$ [rad]", fontsize=11)
    ax.set_ylabel(r"$G(\theta)$ (real) [-]", fontsize=11)
    ax.set_title("(c) Diffusion: amplification factor", fontsize=12)
    ax.set_xlim(0, np.pi)
    ax.set_ylim(-1.5, 1.1)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower left")

    dx = 1.0 / N_CELLS
    x = (np.arange(N_CELLS) + 0.5) * dx
    u0 = square_wave(x)
    steps_period = int(round(1.0 / (COURANT * dx)))
    ax = axes[1, 0]
    ax.plot(
        x, u0, "k-", linewidth=1.5, drawstyle="steps-mid", label="exact (one period)"
    )
    for scheme in ADVECTION_SCHEMES[1:]:
        u = u0.copy()
        for _ in range(steps_period):
            u = advection_step(u, scheme, COURANT)
        ax.plot(x, u, color=COLORS[scheme], linewidth=2, label=scheme)
    ax.set_xlabel("$x$ [m]", fontsize=11)
    ax.set_ylabel("$u$ [-]", fontsize=11)
    ax.set_title(f"(d) Square wave after one period, {steps_period} steps", fontsize=12)
    ax.set_ylim(-0.35, 1.45)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="upper right")

    ax = axes[1, 1]
    runs = (
        ("FTCS", COURANT, "-"),
        ("Upwind", UNSTABLE_COURANT, "--"),
        ("Upwind", COURANT, "-"),
        ("Lax-Wendroff", COURANT, "-"),
    )
    for scheme, c, style in runs:
        u = u0.copy()
        amplitude = [np.max(np.abs(u))]
        for _ in range(GROWTH_STEPS):
            u = advection_step(u, scheme, c)
            amplitude.append(np.max(np.abs(u)))
        ax.semilogy(
            amplitude,
            style,
            color=COLORS[scheme],
            linewidth=2,
            label=f"{scheme}, C = {c}",
        )
    ax.set_xlabel("Time step $n$ [-]", fontsize=11)
    ax.set_ylabel(r"$\max_i |u_i^n|$ [-]", fontsize=11)
    ax.set_title("(e) Growth of the square wave's maximum", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="upper left")

    ax = axes[1, 2]
    march_colors = ("0.6", "tab:orange", "tab:blue", "tab:green")
    for (scheme, r), color in zip(DIFFUSION_MARCH, march_colors):
        steps = int(round(DIFFUSION_TIME / (r * dx**2)))
        u = diffusion_march(u0, scheme, r, steps)
        label = f"{scheme}, r = {r:g} ({steps} steps)"
        unstable = scheme == "FTCS" and r > 0.5
        if unstable:
            label += f", max |u| = {np.max(np.abs(u)):.2g}"
        ax.plot(x, u, color=color, linewidth=0.8 if unstable else 2, label=label)
    ax.plot(x, exact_diffusion(u0, DIFFUSION_TIME), "k--", linewidth=1.5, label="exact")
    ax.set_xlabel("$x$ [m]", fontsize=11)
    ax.set_ylabel("$u$ [-]", fontsize=11)
    ax.set_title(
        rf"(f) Diffusion of the square wave, $\nu t$ = {DIFFUSION_TIME:g} m$^2$",
        fontsize=12,
    )
    ax.set_ylim(-0.6, 1.6)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower right")

    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    theta = np.linspace(1e-6, np.pi, 2001)
    for scheme in ADVECTION_SCHEMES:
        g = np.abs(advection_amplification(scheme, theta, COURANT))
        print(
            f"{scheme:15s} C = {COURANT}: max |G| = {g.max():.4f}, |G(pi/2)| = "
            f"{abs(advection_amplification(scheme, np.pi / 2, COURANT)):.4f}, "
            f"phase speed ratio at theta = pi/4: {relative_phase_speed(scheme, np.pi / 4, COURANT):.4f}"
        )
    g = np.abs(advection_amplification("Upwind", theta, UNSTABLE_COURANT))
    print(f"Upwind          C = {UNSTABLE_COURANT}: max |G| = {g.max():.4f}")
    for r in DIFFUSION_NUMBERS:
        print(
            f"FTCS diffusion  r = {r}: G(pi) = {diffusion_amplification('FTCS', np.pi, r):.3f}"
        )
    for scheme in ("BTCS", "Crank-Nicolson"):
        print(
            f"{scheme:15s} r = {IMPLICIT_R:g}: G(pi) = {diffusion_amplification(scheme, np.pi, IMPLICIT_R):.3f}"
        )
    dx = 1.0 / N_CELLS
    print(
        f"Upwind numerical viscosity at C = {COURANT}, a = 1, dx = {dx}: {numerical_viscosity_upwind(1.0, dx, COURANT):.2e} m^2/s"
    )

    fig = make_figure()
    finish_figures(
        {"von_neumann_amplification.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
