"""Stability regions, order of accuracy and stiffness of common time integrators.

Draws the absolute-stability regions of explicit Euler, RK2, RK3, RK4, AB2 and
BDF2 in the complex plane of z = lambda dt, together with the scaled
eigenvalues of the semi-discrete central-advection, upwind-advection and
diffusion operators, so the stable combinations of space and time
discretisation can be read off. It then measures the order of accuracy of each
method on y' = y cos t, integrates the stiff Prothero-Robinson problem
y' = lambda (y - cos t) - sin t with explicit and implicit methods, and plots
the damping |R(z)| of very stiff modes on the negative real axis.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

ADVECTION_COURANT = 1.0  # C = a dt / dx for the central-advection overlay
UPWIND_COURANT = 0.8  # C for the upwind-advection overlay
DIFFUSION_NUMBER = 0.5  # r = nu dt / dx^2 for the eigenvalue overlay
N_MODES = 64  # Fourier modes of the periodic semi-discrete operators
ORDER_T_END = 2.0  # final time of the order test (s)
ORDER_STEPS = (10, 20, 40, 80, 160, 320)  # steps over [0, ORDER_T_END]
STIFF_LAMBDA = -1000.0  # eigenvalue of the stiff problem (1/s)
STIFF_T_END = 2.0  # (s)
STIFF_DT = 0.05  # large step: lambda dt = -50 (s)
STIFF_DT_EXPLICIT_STABLE = (
    0.002  # RK4 step inside its stability limit, lambda dt = -2 (s)
)
STIFF_PERTURBATION = 1.0  # y(0) - cos(0): initial fast transient

RK_COEFFS = {  # Taylor coefficients of R(z) for s-stage RK of order s = 1..4
    "Explicit Euler": (1, 1),
    "RK2": (1, 1, 1 / 2),
    "RK3 (SSP)": (1, 1, 1 / 2, 1 / 6),
    "RK4": (1, 1, 1 / 2, 1 / 6, 1 / 24),
}
COLORS = {
    "Explicit Euler": "tab:red",
    "RK2": "tab:orange",
    "RK3 (SSP)": "tab:green",
    "RK4": "tab:blue",
    "AB2": "tab:purple",
    "BDF2": "tab:brown",
    "Implicit Euler": "tab:gray",
    "Crank-Nicolson": "tab:olive",
}


def rk_stability_function(name, z):
    """R(z) = sum_k z^k / k! up to the method's order (all s-stage, order-s RK)."""
    return np.polyval(RK_COEFFS[name][::-1], z)


def implicit_stability_function(name, z):
    """R(z) of implicit Euler and Crank-Nicolson."""
    if name == "Implicit Euler":
        return 1.0 / (1.0 - z)
    if name == "Crank-Nicolson":
        return (1.0 + 0.5 * z) / (1.0 - 0.5 * z)
    raise ValueError(name)


def multistep_polynomials(name):
    """(rho, sigma) coefficient arrays (highest power first) of AB2 and BDF2."""
    if name == "AB2":
        return np.array([1.0, -1.0, 0.0]), np.array([0.0, 1.5, -0.5])
    if name == "BDF2":
        return np.array([1.5, -2.0, 0.5]), np.array([1.0, 0.0, 0.0])
    raise ValueError(name)


def boundary_locus(name, n=721):
    """Boundary z(phi) = rho(e^{i phi}) / sigma(e^{i phi}) of a two-step method."""
    rho, sigma = multistep_polynomials(name)
    xi = np.exp(1j * np.linspace(0.0, 2.0 * np.pi, n))
    return np.polyval(rho, xi) / np.polyval(sigma, xi)


def multistep_growth(name, z):
    """Largest |root| of rho(xi) - z sigma(xi) = 0, the growth factor per step."""
    rho, sigma = multistep_polynomials(name)
    z = np.atleast_1d(z)
    return np.array([np.max(np.abs(np.roots(rho - zz * sigma))) for zz in z])


def rk_boundary(name, n_rays=360, r_max=6.0, tol=1e-12):
    """Points with |R(z)| = 1 found by bisection along rays from z = -1.

    z = -1 lies inside the region of every RK method here, and each ray is
    marched outwards to the first sign change of |R| - 1, then bisected.
    """
    points = []
    for phi in np.linspace(0.0, 2.0 * np.pi, n_rays, endpoint=False):
        direction = np.exp(1j * phi)
        ds = 0.01
        s = ds
        while s < r_max and abs(rk_stability_function(name, -1 + s * direction)) <= 1:
            s += ds
        lo, hi = s - ds, s
        while hi - lo > tol:
            mid = 0.5 * (lo + hi)
            if abs(rk_stability_function(name, -1 + mid * direction)) <= 1:
                lo = mid
            else:
                hi = mid
        points.append(-1 + 0.5 * (lo + hi) * direction)
    return np.array(points)


def imaginary_axis_limit(name):
    """Largest y with |R(i s)| <= 1 for 0.01 <= s <= y, or 0 if there is none.

    The scan starts at 0.01 so that the O(y^4) growth of RK2 near the origin is
    not hidden by the round-off tolerance.
    """
    y = np.linspace(0.01, 4, 399001)
    ok = np.abs(rk_stability_function(name, 1j * y)) <= 1 + 1e-12
    return 0.0 if not ok[0] else y[np.argmin(ok)] if not ok.all() else y[-1]


def real_axis_limit(name):
    """Most negative x with |R(x)| <= 1 on [x, 0]."""
    x = -np.linspace(0, 6, 600001)[1:]
    ok = np.abs(rk_stability_function(name, x)) <= 1 + 1e-12
    return x[np.argmin(ok)]


def operator_eigenvalues(
    n=N_MODES, c=ADVECTION_COURANT, c_up=UPWIND_COURANT, r=DIFFUSION_NUMBER
):
    """lambda dt of the periodic semi-discrete operators for theta = 2 pi k / n."""
    theta = 2.0 * np.pi * np.arange(n) / n
    central = -1j * c * np.sin(theta)
    upwind = -c_up * (1.0 - np.exp(-1j * theta))
    diffusion = -4.0 * r * np.sin(0.5 * theta) ** 2 + 0j
    return central, upwind, diffusion


# ---- Integrators for linear ODEs y' = a(t) y + b(t) ------------------------


def _f(a, b, t, y):
    return a(t) * y + b(t)


def integrate(method, a, b, y0, t_end, n_steps):
    """Integrate y' = a(t) y + b(t) with a named method; returns times and values.

    Implicit stages are solved exactly because the ODE is linear in y. The
    two-step methods take their first step with a one-step method: RK2 for AB2
    and implicit Euler for BDF2 (one first-order step has a local error of
    O(dt^2), so the global order stays 2, and it keeps the start L-stable).
    """
    dt = t_end / n_steps
    t = np.linspace(0.0, t_end, n_steps + 1)
    y = np.empty(n_steps + 1)
    y[0] = y0
    for n in range(n_steps):
        tn, yn = t[n], y[n]
        if method == "Explicit Euler":
            y[n + 1] = yn + dt * _f(a, b, tn, yn)
        elif method == "RK2":  # Heun's method
            k1 = _f(a, b, tn, yn)
            k2 = _f(a, b, tn + dt, yn + dt * k1)
            y[n + 1] = yn + 0.5 * dt * (k1 + k2)
        elif method == "RK3 (SSP)":  # Shu and Osher (1988)
            y1 = yn + dt * _f(a, b, tn, yn)
            y2 = 0.75 * yn + 0.25 * (y1 + dt * _f(a, b, tn + dt, y1))
            y[n + 1] = yn / 3.0 + 2.0 / 3.0 * (y2 + dt * _f(a, b, tn + 0.5 * dt, y2))
        elif method == "RK4":
            k1 = _f(a, b, tn, yn)
            k2 = _f(a, b, tn + 0.5 * dt, yn + 0.5 * dt * k1)
            k3 = _f(a, b, tn + 0.5 * dt, yn + 0.5 * dt * k2)
            k4 = _f(a, b, tn + dt, yn + dt * k3)
            y[n + 1] = yn + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        elif method == "Implicit Euler" or (method == "BDF2" and n == 0):
            y[n + 1] = (yn + dt * b(tn + dt)) / (1.0 - dt * a(tn + dt))
        elif method == "Crank-Nicolson":
            rhs = yn + 0.5 * dt * (_f(a, b, tn, yn) + b(tn + dt))
            y[n + 1] = rhs / (1.0 - 0.5 * dt * a(tn + dt))
        elif method == "BDF2":
            rhs = (4.0 * yn - y[n - 1]) / 3.0 + 2.0 / 3.0 * dt * b(tn + dt)
            y[n + 1] = rhs / (1.0 - 2.0 / 3.0 * dt * a(tn + dt))
        elif method == "AB2" and n == 0:
            k1 = _f(a, b, tn, yn)
            k2 = _f(a, b, tn + dt, yn + dt * k1)
            y[n + 1] = yn + 0.5 * dt * (k1 + k2)
        elif method == "AB2":
            y[n + 1] = yn + dt * (
                1.5 * _f(a, b, tn, yn) - 0.5 * _f(a, b, t[n - 1], y[n - 1])
            )
        else:
            raise ValueError(method)
        if not np.isfinite(y[n + 1]) or abs(y[n + 1]) > 1e30:
            y[n + 1 :] = np.nan
            break
    return t, y


def order_test_problem():
    """y' = cos(t) y, y(0) = 1, exact y = exp(sin t)."""
    return np.cos, lambda t: 0.0 * t, 1.0, lambda t: np.exp(np.sin(t))


def stiff_problem(lam=STIFF_LAMBDA, perturbation=STIFF_PERTURBATION):
    """Prothero-Robinson: y' = lam (y - cos t) - sin t, exact cos t + perturbation e^{lam t}."""

    def a(t):
        return lam + 0.0 * t

    def b(t):
        return -lam * np.cos(t) - np.sin(t)

    def exact(t):
        return np.cos(t) + perturbation * np.exp(lam * t)

    return a, b, 1.0 + perturbation, exact


ORDER_METHODS = (
    "Explicit Euler",
    "Implicit Euler",
    "RK2",
    "AB2",
    "BDF2",
    "Crank-Nicolson",
    "RK3 (SSP)",
    "RK4",
)


def order_study():
    """Final-time errors and observed orders on the smooth test problem."""
    a, b, y0, exact = order_test_problem()
    errors = {}
    for method in ORDER_METHODS:
        errors[method] = np.array(
            [
                abs(
                    integrate(method, a, b, y0, ORDER_T_END, n)[1][-1]
                    - exact(ORDER_T_END)
                )
                for n in ORDER_STEPS
            ]
        )
    return errors


def observed_order(errors, steps=ORDER_STEPS):
    """Slope of log(error) against log(dt) between the two finest runs."""
    return np.log(errors[-2] / errors[-1]) / np.log(steps[-1] / steps[-2])


def make_figure(errors):
    fig, axes = plt.subplots(2, 2, figsize=(13, 12), layout="constrained")
    fig.get_layout_engine().set(h_pad=0.15)

    ax = axes[0, 0]
    xr = np.linspace(-4.5, 4.5, 601)
    yr = np.linspace(-3.5, 3.5, 501)
    zz = xr[None, :] + 1j * yr[:, None]
    for name in RK_COEFFS:
        mag = np.abs(rk_stability_function(name, zz))
        ax.contourf(xr, yr, mag, levels=[0, 1], colors=[COLORS[name]], alpha=0.08)
        ax.contour(xr, yr, mag, levels=[1], colors=[COLORS[name]], linewidths=2)
        ax.plot([], [], color=COLORS[name], linewidth=2, label=name)
    for name, style in (("AB2", "-"), ("BDF2", "--")):
        z = boundary_locus(name)
        label = name + (" (stable outside)" if name == "BDF2" else "")
        ax.plot(z.real, z.imag, style, color=COLORS[name], linewidth=2, label=label)
    central, upwind, diffusion = operator_eigenvalues()
    ax.plot(
        central.real,
        central.imag,
        "kD",
        markersize=4,
        label=f"central advection, C = {ADVECTION_COURANT:g}",
    )
    ax.plot(
        upwind.real,
        upwind.imag,
        "ko",
        markersize=4,
        fillstyle="none",
        label=f"upwind advection, C = {UPWIND_COURANT:g}",
    )
    ax.plot(
        diffusion.real,
        diffusion.imag,
        "k^",
        markersize=4,
        label=f"central diffusion, r = {DIFFUSION_NUMBER:g}",
    )
    ax.axhline(0, color="k", linewidth=0.6)
    ax.axvline(0, color="k", linewidth=0.6)
    ax.set_aspect("equal")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xlabel(r"Re$(\lambda\Delta t)$ [-]", fontsize=11)
    ax.set_ylabel(r"Im$(\lambda\Delta t)$ [-]", fontsize=11)
    ax.set_title("(a) Stability regions and operator eigenvalues", fontsize=12)
    ax.legend(fontsize=9.5, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3)

    ax = axes[0, 1]
    dt = ORDER_T_END / np.array(ORDER_STEPS)
    for method in ORDER_METHODS:
        p = observed_order(errors[method])
        style = "--" if method in ("Implicit Euler", "AB2", "Crank-Nicolson") else "-"
        ax.loglog(
            dt,
            errors[method],
            "o" + style,
            color=COLORS[method],
            markersize=4,
            label=f"{method}: p = {p:.2f}",
        )
    ax.set_xlabel(r"Time step $\Delta t$ [s]", fontsize=11)
    ax.set_ylabel(r"Error $|y_N - y(T)|$ at $T$ = 2 s [-]", fontsize=11)
    ax.set_title(r"(b) Order of accuracy on $y' = y\cos t$", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower right", ncol=2)

    ax = axes[1, 0]
    a, b, y0, exact = stiff_problem()
    tf = np.linspace(0, STIFF_T_END, 2001)
    ax.plot(tf, exact(tf), "k-", linewidth=1.5, label="exact")
    n_big = int(round(STIFF_T_END / STIFF_DT))
    for method, marker in (
        ("Implicit Euler", "s"),
        ("BDF2", "^"),
        ("Crank-Nicolson", "o"),
    ):
        t, y = integrate(method, a, b, y0, STIFF_T_END, n_big)
        ax.plot(
            t,
            y,
            marker + "-",
            color=COLORS[method],
            markersize=4,
            linewidth=1,
            label=rf"{method}, $\Delta t$ = {STIFF_DT}",
        )
    t, y = integrate("RK4", a, b, y0, STIFF_T_END, n_big)
    finite = np.isfinite(y)
    ax.plot(
        t[finite][:4],
        y[finite][:4],
        "x-",
        color=COLORS["RK4"],
        markersize=7,
        label=rf"RK4, $\Delta t$ = {STIFF_DT} (diverges)",
    )
    n_small = int(round(STIFF_T_END / STIFF_DT_EXPLICIT_STABLE))
    t, y = integrate("RK4", a, b, y0, STIFF_T_END, n_small)
    ax.plot(
        t,
        y,
        ":",
        color=COLORS["RK4"],
        linewidth=2.5,
        label=rf"RK4, $\Delta t$ = {STIFF_DT_EXPLICIT_STABLE} ({n_small} steps)",
    )
    ax.set_ylim(-1.5, 2.5)
    ax.set_xlabel("Time $t$ [s]", fontsize=11)
    ax.set_ylabel("$y$ [-]", fontsize=11)
    ax.set_title(
        rf"(c) Stiff problem, $\lambda$ = {STIFF_LAMBDA:g} s$^{{-1}}$", fontsize=12
    )
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="upper right")

    ax = axes[1, 1]
    x = -np.logspace(-1, 3, 400)
    for name in ("Implicit Euler", "Crank-Nicolson"):
        ax.loglog(
            -x,
            np.abs(implicit_stability_function(name, x)),
            color=COLORS[name],
            linewidth=2,
            label=name,
        )
    ax.loglog(
        -x,
        multistep_growth("BDF2", x),
        color=COLORS["BDF2"],
        linewidth=2,
        label="BDF2 (largest root)",
    )
    ax.loglog(
        -x,
        np.abs(rk_stability_function("RK4", x)),
        color=COLORS["RK4"],
        linewidth=2,
        label="RK4",
    )
    ax.axhline(1.0, color="k", linewidth=0.8)
    ax.axvline(-STIFF_LAMBDA * STIFF_DT, color="0.5", linestyle=":", linewidth=1)
    ax.text(
        -STIFF_LAMBDA * STIFF_DT * 1.1,
        2e-3,
        r"$|\lambda|\Delta t$ of (c)",
        fontsize=10,
        color="0.3",
    )
    ax.set_ylim(1e-3, 1e3)
    ax.set_xlabel(r"$-\lambda\Delta t$ on the negative real axis [-]", fontsize=11)
    ax.set_ylabel(r"Growth factor per step $|R(\lambda\Delta t)|$ [-]", fontsize=11)
    ax.set_title("(d) Damping of stiff modes (L-stability)", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="upper left")

    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for name in RK_COEFFS:
        print(
            f"{name:15s} real-axis limit {real_axis_limit(name):.4f}, "
            f"imaginary-axis limit {imaginary_axis_limit(name):.4f}"
        )
    errors = order_study()
    for method in ORDER_METHODS:
        print(
            f"{method:15s} observed order {observed_order(errors[method]):.3f}, error at dt = {ORDER_T_END / ORDER_STEPS[-1]:.4g}: {errors[method][-1]:.2e}"
        )
    a, b, y0, exact = stiff_problem()
    n_big = int(round(STIFF_T_END / STIFF_DT))
    for method in ("Implicit Euler", "BDF2", "Crank-Nicolson", "RK4"):
        t, y = integrate(method, a, b, y0, STIFF_T_END, n_big)
        err = np.nanmax(np.abs(y[1:] - exact(t[1:]))) if np.isfinite(y[-1]) else np.inf
        print(f"stiff, dt = {STIFF_DT}: {method:15s} max error after t = 0: {err:.3e}")
    z = STIFF_LAMBDA * STIFF_DT
    print(
        f"z = {z:g}: |R| implicit Euler {abs(implicit_stability_function('Implicit Euler', z)):.4f}, "
        f"Crank-Nicolson {abs(implicit_stability_function('Crank-Nicolson', z)):.4f}, "
        f"BDF2 {multistep_growth('BDF2', z)[0]:.4f}, RK4 {abs(rk_stability_function('RK4', z)):.3e}"
    )

    fig = make_figure(errors)
    finish_figures(
        {"time_integrator_stability.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
