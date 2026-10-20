"""TVD flux limiters on periodic 1D linear advection of a Gaussian, square wave and triangle.

Advects a profile made of a smooth Gaussian, a square wave and a triangle
once around a periodic domain with the explicit flux-limited scheme of Sweby
(1984). The limiter psi(r) selects the method: psi = 0 is first-order upwind,
psi = 1 is Lax-Wendroff, and the minmod, van Leer, superbee, MC and van Albada
limiters give second-order TVD schemes (for linear advection this is the same
update as MUSCL-Hancock with the corresponding slope limiter). The script
checks that the total variation never grows for the TVD schemes, that the
integral of phi is conserved to round-off, and measures the order of accuracy
on a smooth sine wave. It draws the transported profiles, the total variation
history, the Sweby diagram with the TVD region shaded and the error against
the number of cells.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

VELOCITY = 1.0  # advection speed u (m/s)
LENGTH = 1.0  # periodic domain length (m)
N_CELLS = 200  # cells for the profile test
COURANT = 0.5  # C = u dt / dx [-]
PERIODS = 1  # number of times the profile crosses the domain
N_CONVERGENCE = (25, 50, 100, 200, 400, 800)  # cells for the sine-wave study
SUBSAMPLES = 32  # quadrature points per cell for the initial cell averages


def psi_upwind(r):
    return np.zeros_like(r)


def psi_lax_wendroff(r):
    return np.ones_like(r)


def psi_minmod(r):
    return np.maximum(0.0, np.minimum(1.0, r))


def psi_van_leer(r):
    return (r + np.abs(r)) / (1.0 + np.abs(r))


def psi_superbee(r):
    return np.maximum.reduce(
        [np.zeros_like(r), np.minimum(2.0 * r, 1.0), np.minimum(r, 2.0)]
    )


def psi_mc(r):
    return np.maximum(0.0, np.minimum.reduce([2.0 * r, 0.5 * (1.0 + r), 2.0 + 0 * r]))


def psi_van_albada(r):
    return np.where(r > 0.0, (r * r + r) / (r * r + 1.0), 0.0)


LIMITERS = {
    "upwind": psi_upwind,
    "Lax-Wendroff": psi_lax_wendroff,
    "minmod": psi_minmod,
    "van Leer": psi_van_leer,
    "superbee": psi_superbee,
    "MC": psi_mc,
    "van Albada": psi_van_albada,
}
TVD_LIMITERS = ("minmod", "van Leer", "superbee", "MC", "van Albada")
PLOTTED = ("upwind", "Lax-Wendroff", "minmod", "van Leer", "superbee")
COLORS = {
    "upwind": "tab:blue",
    "Lax-Wendroff": "tab:red",
    "minmod": "tab:green",
    "van Leer": "tab:purple",
    "superbee": "tab:orange",
    "MC": "tab:brown",
    "van Albada": "tab:cyan",
}


def profile(x):
    """Gaussian at x = 0.15, square wave on [0.35, 0.55], triangle on [0.7, 0.9]."""
    gauss = np.exp(-(((x - 0.15) / 0.05) ** 2))
    square = ((x >= 0.35) & (x <= 0.55)).astype(float)
    triangle = np.maximum(0.0, 1.0 - np.abs(x - 0.8) / 0.1)
    return gauss + square + triangle


def smooth_profile(x):
    return np.sin(2.0 * np.pi * x / LENGTH)


def cell_averages(func, n):
    """Cell averages of func on n uniform cells by midpoint sub-sampling."""
    dx = LENGTH / n
    offsets = (np.arange(SUBSAMPLES) + 0.5) / SUBSAMPLES * dx
    x_left = np.arange(n) * dx
    return func(x_left[:, None] + offsets[None, :]).mean(axis=1)


def smoothness_ratio(phi):
    """r_i = (phi_i - phi_(i-1)) / (phi_(i+1) - phi_i) on a periodic grid.

    Where the denominator vanishes r is set to 0. The limited correction is
    psi(r) times that denominator, so the choice does not matter.
    """
    num = phi - np.roll(phi, 1)
    den = np.roll(phi, -1) - phi
    safe = np.abs(den) > 1e-300
    return np.where(safe, num / np.where(safe, den, 1.0), 0.0), den


def step(phi, psi, courant, velocity=VELOCITY):
    """One step of the flux-limited scheme for u > 0, in conservative form.

    F_(i+1/2) = u phi_i + u (1 - C)/2 psi(r_i)(phi_(i+1) - phi_i), and
    phi_i^(n+1) = phi_i - (C / u)(F_(i+1/2) - F_(i-1/2)).
    """
    r, den = smoothness_ratio(phi)
    flux = velocity * (phi + 0.5 * (1.0 - courant) * psi(r) * den)
    return phi - (courant / velocity) * (flux - np.roll(flux, 1))


def total_variation(phi):
    return np.sum(np.abs(np.roll(phi, -1) - phi))


def advect(phi0, psi, n_steps, courant=COURANT):
    """Advance n_steps; return the final field and TV and integral histories."""
    phi = phi0.copy()
    tv = np.empty(n_steps + 1)
    mass = np.empty(n_steps + 1)
    tv[0], mass[0] = total_variation(phi), phi.sum()
    for k in range(1, n_steps + 1):
        phi = step(phi, psi, courant)
        tv[k], mass[k] = total_variation(phi), phi.sum()
    return phi, tv, mass


def steps_per_period(n, courant=COURANT):
    steps = round(n / courant)
    if not np.isclose(steps * courant, n):
        raise ValueError("choose C so that one period is a whole number of steps")
    return steps


def profile_test(n=N_CELLS, periods=PERIODS, courant=COURANT):
    """Transport the composite profile with every limiter."""
    phi0 = cell_averages(profile, n)
    n_steps = periods * steps_per_period(n, courant)
    results = {}
    for name, psi in LIMITERS.items():
        phi, tv, mass = advect(phi0, psi, n_steps, courant)
        results[name] = {
            "phi": phi,
            "tv": tv,
            "l1": np.mean(np.abs(phi - phi0)),
            "max": phi.max(),
            "min": phi.min(),
            "max_tv_increase": np.max(np.diff(tv)),
            "mass_drift": np.max(np.abs(mass - mass[0])) / n,
        }
    return phi0, n_steps, results


def convergence_test(n_values=N_CONVERGENCE, courant=COURANT):
    """L1 error after one period of a sine wave for every limiter."""
    n_values = np.array(n_values)
    errors = {name: [] for name in LIMITERS}
    for n in n_values:
        phi0 = cell_averages(smooth_profile, n)
        n_steps = steps_per_period(n, courant)
        for name, psi in LIMITERS.items():
            phi, _, _ = advect(phi0, psi, n_steps, courant)
            errors[name].append(np.mean(np.abs(phi - phi0)))
    return n_values, {k: np.array(v) for k, v in errors.items()}


def observed_order(n_values, errors):
    return np.log(errors[-2] / errors[-1]) / np.log(n_values[-1] / n_values[-2])


def make_profile_figure(phi0, n_steps, results, n=N_CELLS):
    x = (np.arange(n) + 0.5) * LENGTH / n
    fig, axes = plt.subplots(2, 3, figsize=(13, 8), sharex=False)
    letters = "abcde"
    for ax, name, letter in zip(axes.flat, PLOTTED, letters):
        ax.plot(x, phi0, "k-", linewidth=1.5, label="exact")
        ax.plot(
            x,
            results[name]["phi"],
            "o",
            color=COLORS[name],
            markersize=3,
            label=name,
        )
        ax.set_title(
            f"({letter}) {name}, L1 error {results[name]['l1']:.4f}", fontsize=12
        )
        ax.set_xlabel("x [m]", fontsize=11)
        ax.set_ylabel(r"$\phi$ [-]", fontsize=11)
        ax.set_ylim(-0.3, 1.6)
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
        ax.legend(fontsize=9, loc="upper center", ncol=2, framealpha=0.9)

    ax = axes[1, 2]
    t = np.arange(n_steps + 1) * COURANT * (LENGTH / n) / VELOCITY
    for name in PLOTTED:
        tv = results[name]["tv"]
        ax.plot(t, tv / tv[0], color=COLORS[name], linewidth=1.8, label=name)
    ax.axhline(1.0, color="k", linestyle=":", linewidth=1)
    ax.set_xlabel("t [s] (one period = 1 s)", fontsize=11)
    ax.set_ylabel(r"$TV(\phi^n) / TV(\phi^0)$ [-]", fontsize=11)
    ax.set_title("(f) Total variation history", fontsize=12)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower left")
    fig.suptitle(
        f"Linear advection after {PERIODS} period, N = {n}, C = {COURANT}",
        fontsize=13,
    )
    fig.tight_layout()
    return fig


def make_sweby_figure(conv):
    n_values, errors = conv
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    ax = axes[0]
    r = np.linspace(0.0, 3.0, 601)
    ax.fill_between(r, 0.0, np.minimum(2 * r, 2.0), color="0.85", label="TVD region")
    lower = np.minimum(r, 1.0)
    upper = np.maximum(np.minimum(2 * r, 1.0), np.minimum(r, 2.0))
    ax.fill_between(r, lower, upper, color="0.65", label="second-order TVD region")
    for name in TVD_LIMITERS:
        width = 4.0 if name == "minmod" else 2.0  # minmod lies on psi = r, psi = 1
        ax.plot(r, LIMITERS[name](r), color=COLORS[name], linewidth=width, label=name)
    ax.plot(
        r,
        np.ones_like(r),
        "--",
        color=COLORS["Lax-Wendroff"],
        linewidth=1.2,
        label=r"Lax-Wendroff ($\psi = 1$)",
    )
    ax.plot(r, r, ":", color="k", linewidth=1.2, label=r"Beam-Warming ($\psi = r$)")
    ax.plot([1.0], [1.0], "ko", markersize=6)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 2.6)
    ax.set_xlabel(r"Smoothness ratio $r$ [-]", fontsize=11)
    ax.set_ylabel(r"Limiter $\psi(r)$ [-]", fontsize=11)
    ax.set_title("(a) Sweby diagram", fontsize=12)
    ax.legend(fontsize=9, loc="lower right", framealpha=0.95)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)

    ax = axes[1]
    for name in LIMITERS:
        p = observed_order(n_values, errors[name])
        ax.loglog(
            n_values,
            errors[name],
            "o-",
            color=COLORS[name],
            markersize=5,
            label=f"{name} (p = {p:.2f})",
        )
    e_ref = errors["Lax-Wendroff"][-1]
    ax.loglog(
        n_values,
        e_ref * (n_values[-1] / n_values) ** 2,
        "k--",
        linewidth=1,
        label="slope 2",
    )
    e_ref = errors["upwind"][-1]
    ax.loglog(
        n_values, e_ref * (n_values[-1] / n_values), "k:", linewidth=1, label="slope 1"
    )
    ax.set_xticks(n_values, [str(n) for n in n_values])
    ax.minorticks_off()
    ax.set_xlabel("Number of cells N [-]", fontsize=11)
    ax.set_ylabel("L1 error after one period [-]", fontsize=11)
    ax.set_title(f"(b) Smooth sine wave, C = {COURANT}", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower left", ncol=2)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    phi0, n_steps, results = profile_test()
    print(
        f"Composite profile, N = {N_CELLS}, C = {COURANT}, {n_steps} steps "
        f"({PERIODS} period), TV(phi0) = {total_variation(phi0):.4f}"
    )
    print(
        "  scheme         L1 error   max phi   min phi   TV end/TV0  max dTV/step  mass drift"
    )
    for name, res in results.items():
        print(
            f"  {name:13s} {res['l1']:9.5f} {res['max']:9.4f} {res['min']:9.4f}"
            f" {res['tv'][-1] / res['tv'][0]:10.4f} {res['max_tv_increase']:12.2e}"
            f" {res['mass_drift']:11.1e}"
        )
    conv = convergence_test()
    print("Sine wave, L1 error after one period")
    n_values, errors = conv
    print("  N            " + " ".join(f"{n:9d}" for n in n_values))
    for name, err in errors.items():
        print(
            f"  {name:13s}"
            + " ".join(f"{e:9.2e}" for e in err)
            + f"   p = {observed_order(n_values, err):.2f}"
        )

    finish_figures(
        {
            "tvd_advection_profiles.png": make_profile_figure(phi0, n_steps, results),
            "sweby_diagram.png": make_sweby_figure(conv),
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
