"""Static and dynamic stability: potential wells and the five free responses.

The first figure shows the static picture: a ball in a bowl, on a hill and on
a flat surface, with the potential energy V(x), the restoring force -dV/dx and
the sign of the stiffness d2V/dx2. The second figure integrates
x'' + c x' + k x = 0 from x(0) = 1, x'(0) = 0 for five (c, k) pairs that give
a non-oscillatory convergence, a damped oscillation, a neutral oscillation, a
divergent oscillation and a monotonic divergence, and places the eigenvalues
of all five in the complex plane.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch
from scipy.linalg import expm

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Unit-mass oscillators x'' + c x' + k x = 0: (title, c in 1/s, k in 1/s^2).
CASES = (
    ("Non-oscillatory convergence", 3.0, 2.0),
    ("Damped oscillation", 0.5, 4.0),
    ("Neutral oscillation", 0.0, 4.0),
    ("Divergent oscillation", -0.3, 4.0),
    ("Monotonic divergence", 0.5, -1.0),
)
COLOURS = ("tab:blue", "tab:green", "tab:gray", "tab:orange", "tab:red")
DURATION = 12.0  # s
N_TIMES = 1201
STATIC_STIFFNESS = (1.0, -1.0, 0.0)  # bowl, hill, flat (curvature of V)
BALL_RADIUS = 0.12
DISPLACEMENT = 0.45  # displaced position of the ghost ball


def eigenvalues(c, k):
    """Roots of lambda^2 + c lambda + k = 0."""
    return np.roots([1.0, c, k])


def free_response(c, k, t, x0=1.0, v0=0.0):
    """x(t) of x'' + c x' + k x = 0 by the matrix exponential."""
    a = np.array([[0.0, 1.0], [-k, -c]])
    return np.array([(expm(a * ti) @ [x0, v0])[0] for ti in t])


def classify(c, k):
    """Static and dynamic classification of x'' + c x' + k x = 0."""
    static = "stable" if k > 0 else ("neutral" if k == 0 else "unstable")
    lam = eigenvalues(c, k)
    max_real = lam.real.max()
    if max_real < -1e-12:
        dynamic = "stable"
    elif max_real > 1e-12:
        dynamic = "unstable"
    else:
        dynamic = "neutral"
    oscillatory = bool(np.any(np.abs(lam.imag) > 1e-12))
    return static, dynamic, oscillatory


def plot_static():
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.0))
    x = np.linspace(-1.0, 1.0, 200)
    titles = ("Statically stable: bowl", "Statically unstable: hill", "Neutral: flat")
    for ax, k, title in zip(axes, STATIC_STIFFNESS, titles, strict=True):
        v = 0.5 * k * x**2
        ax.fill_between(x, -0.65, v, color="0.85")
        ax.plot(x, v, color="0.2", lw=2)

        def surface_point(xp, k=k):
            # Centre of a ball resting on the curve, offset along its normal.
            slope = k * xp
            n = np.array([-slope, 1.0]) / np.hypot(slope, 1.0)
            return np.array([xp, 0.5 * k * xp**2]) + BALL_RADIUS * n

        ax.add_patch(Circle(surface_point(0.0), BALL_RADIUS, color="tab:blue"))
        ghost = surface_point(DISPLACEMENT)
        ax.add_patch(Circle(ghost, BALL_RADIUS, fc="none", ec="tab:blue", ls="--"))
        force = -k * DISPLACEMENT
        if force != 0:
            ax.add_patch(
                FancyArrowPatch(
                    ghost + [0, 0.22],
                    ghost + [0.5 * force, 0.22],
                    arrowstyle="-|>",
                    mutation_scale=15,
                    color="tab:red",
                )
            )
            ax.text(ghost[0], ghost[1] + 0.3, r"$-dV/dx$", color="tab:red", ha="center")
        else:
            ax.text(ghost[0], ghost[1] + 0.25, "no force", color="tab:red", ha="center")
        sign = ">" if k > 0 else ("<" if k < 0 else "=")
        ax.text(0, -0.5, rf"$d^2V/dx^2 {sign} 0$", ha="center", fontsize=11)
        ax.set_xlim(-1.0, 1.0)
        ax.set_ylim(-0.65, 0.75)
        ax.set_aspect("equal")
        ax.set_xlabel("Displacement $x$")
        ax.set_ylabel("Potential energy $V$")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)
    fig.tight_layout()
    return fig


def plot_dynamic():
    t = np.linspace(0, DURATION, N_TIMES)
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.2))
    flat = axes.ravel()
    for i, ((title, c, k), colour) in enumerate(zip(CASES, COLOURS, strict=True)):
        ax = flat[i]
        x = free_response(c, k, t)
        ax.plot(t, x, color=colour, lw=2)
        lam = eigenvalues(c, k)
        if np.any(np.abs(lam.imag) > 1e-12):
            envelope = np.exp(lam.real.max() * t)
            ax.plot(t, envelope, ":", color="0.4", lw=1)
            ax.plot(t, -envelope, ":", color="0.4", lw=1)
        static, dynamic, _ = classify(c, k)
        ax.axhline(0, color="0.6", lw=0.8)
        ax.set_ylim(-3, 3)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("$x(t)$")
        ax.set_title(
            f"{title}\nc = {c:g}, k = {k:g}: static {static}, dynamic {dynamic}",
            fontsize=10,
        )
        ax.grid(alpha=0.3)

    ax = flat[5]
    for (title, c, k), colour in zip(CASES, COLOURS, strict=True):
        lam = eigenvalues(c, k)
        ax.plot(lam.real, lam.imag, "x", color=colour, ms=10, mew=2.5, label=title)
    ax.axvspan(-3, 0, color="tab:green", alpha=0.07)
    ax.axhline(0, color="0.6", lw=0.8)
    ax.axvline(0, color="0.3", lw=1)
    ax.text(-2.9, 2.55, "stable half-plane", fontsize=9, color="tab:green")
    ax.set_xlim(-3, 1.5)
    ax.set_ylim(-3, 3)
    ax.set_xlabel(r"Re $\lambda$ (1/s)")
    ax.set_ylabel(r"Im $\lambda$ (rad/s)")
    ax.set_title("Eigenvalues of the five systems", fontsize=10)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def main(argv=None):
    args = create_parser(__doc__).parse_args(argv)
    for title, c, k in CASES:
        lam = eigenvalues(c, k)
        roots = ", ".join(f"{z.real:+.3f}{z.imag:+.3f}j" for z in lam)
        print(f"{title:28s} c = {c:+.1f}, k = {k:+.1f}: lambda = {roots}")
    finish_figures(
        {
            "airplane_static_stability.png": plot_static(),
            "airplane_dynamic_stability.png": plot_dynamic(),
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
