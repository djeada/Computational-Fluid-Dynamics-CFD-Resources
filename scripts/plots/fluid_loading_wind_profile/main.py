"""Log-law and power-law wind profiles and velocity pressure over four terrains.

Mean wind speed in the neutral atmospheric surface layer follows the log law
U(z) = (u_* / kappa) ln(z / z_0). The script fixes U = 25 m/s at 10 m over
open country and, as a simple stand-in for a common wind above the surface
layer, gives every terrain the same mean speed at 300 m. It fits a power-law
exponent to each log profile between 10 and 200 m, and evaluates the mean
velocity pressure q = rho U^2 / 2 and a peak velocity pressure using the
turbulence intensity I_u = 1 / ln(z / z_0) and a peak factor of 3.5. It
prints the friction velocities, exponents and the base shear of a 100 m tall
building in each terrain.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

KAPPA = 0.41  # von Karman constant (-)
RHO_AIR = 1.225  # air density (kg/m^3)
TERRAINS = {  # name: aerodynamic roughness length z_0 (m)
    "open sea": 0.0002,
    "open country": 0.03,
    "suburbs": 0.3,
    "city centre": 1.0,
}
U10_OPEN = 25.0  # mean speed at 10 m over open country (m/s)
Z_COMMON = 300.0  # height at which all terrains share the same mean speed (m)
PEAK_FACTOR = 3.5  # g_p in q_peak = q (1 + 2 g_p I_u)
FIT_RANGE = (10.0, 200.0)  # heights used to fit the power-law exponent (m)
Z_MIN, Z_MAX = 5.0, 300.0  # plotted heights (m)

# Building used for the base-shear comparison.
BUILDING_HEIGHT = 100.0  # H (m)
BUILDING_WIDTH = 30.0  # B (m)
BUILDING_CD = 1.3  # overall drag coefficient (-)


def log_law(z, u_star, z0, kappa=KAPPA):
    """Mean wind speed U(z) = (u_* / kappa) ln(z / z_0) in m/s."""
    return u_star / kappa * np.log(np.asarray(z, dtype=float) / z0)


def friction_velocity(u_ref, z_ref, z0, kappa=KAPPA):
    """u_* such that the log law gives u_ref at height z_ref."""
    return kappa * u_ref / np.log(z_ref / z0)


def power_law(z, u_ref, z_ref, alpha):
    """Power-law profile U(z) = U_ref (z / z_ref)^alpha."""
    return u_ref * (np.asarray(z, dtype=float) / z_ref) ** alpha


def fit_power_law(u_star, z0, z_range=FIT_RANGE, n=200):
    """Least-squares fit of ln U = ln U_10 + alpha ln(z / 10) to the log law.

    Uses n heights spaced geometrically over z_range; returns (alpha, U_10).
    """
    z = np.geomspace(*z_range, n)
    u = log_law(z, u_star, z0)
    alpha, intercept = np.polyfit(np.log(z / 10.0), np.log(u), 1)
    return alpha, np.exp(intercept)


def turbulence_intensity(z, z0):
    """Longitudinal turbulence intensity I_u = 1 / ln(z / z_0) (sigma_u ~ 2.5 u_*)."""
    return 1.0 / np.log(np.asarray(z, dtype=float) / z0)


def velocity_pressure(u, rho=RHO_AIR):
    """Mean velocity pressure q = rho U^2 / 2 in Pa."""
    return 0.5 * rho * np.asarray(u) ** 2


def peak_velocity_pressure(z, u, z0, g_p=PEAK_FACTOR, rho=RHO_AIR):
    """Peak velocity pressure q (1 + 2 g_p I_u), the linearised gust form."""
    return velocity_pressure(u, rho) * (1.0 + 2.0 * g_p * turbulence_intensity(z, z0))


def terrain_profiles(z):
    """Speed, mean and peak velocity pressure, u_* and alpha for each terrain."""
    u_star_open = friction_velocity(U10_OPEN, 10.0, TERRAINS["open country"])
    u_common = log_law(Z_COMMON, u_star_open, TERRAINS["open country"])
    out = {}
    for name, z0 in TERRAINS.items():
        u_star = friction_velocity(u_common, Z_COMMON, z0)
        u = log_law(z, u_star, z0)
        out[name] = {
            "z0": z0,
            "u_star": u_star,
            "u": u,
            "q": velocity_pressure(u),
            "q_peak": peak_velocity_pressure(z, u, z0),
            "power_fit": fit_power_law(u_star, z0),
            "u10": float(log_law(10.0, u_star, z0)),
        }
    return out


def base_shear(z0, u_star, height=BUILDING_HEIGHT, peak=False, n=400):
    """Integral of q C_D B over the height (N).

    The log law is used from z = max(1 m, 2 z_0) upward; the strip below that
    height, where the law does not apply, is taken as unloaded.
    """
    z = np.linspace(max(1.0, 2.0 * z0), height, n)
    u = log_law(z, u_star, z0)
    q = peak_velocity_pressure(z, u, z0) if peak else velocity_pressure(u)
    return np.trapezoid(q * BUILDING_CD * BUILDING_WIDTH, z)


def make_figure(z, profiles):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6), sharey=True)
    colors = ("tab:blue", "tab:green", "tab:orange", "tab:red")
    for (name, p), color in zip(profiles.items(), colors):
        alpha, u10_fit = p["power_fit"]
        label = f"{name}, $z_0$ = {p['z0']:g} m, $\\alpha$ = {alpha:.3f}"
        axes[0].plot(p["u"], z, color=color, lw=2, label=label)
        u_pow = power_law(z, u10_fit, 10.0, alpha)
        axes[0].plot(u_pow, z, color=color, lw=1.2, ls="--")
        axes[1].plot(p["q"] / 1e3, z, color=color, lw=2, label=name)
        axes[2].plot(p["q_peak"] / 1e3, z, color=color, lw=2, label=name)
    axes[0].set_xlabel("Mean wind speed $U$ (m/s)", fontsize=11)
    axes[0].set_ylabel("Height above ground $z$ (m)", fontsize=11)
    axes[0].set_title("(a) Log law (solid), fitted power law (dashed)", fontsize=12)
    axes[0].legend(fontsize=9, loc="upper left")
    axes[0].set_xlim(0, 55)
    axes[1].set_xlabel("Mean velocity pressure $\\rho U^2/2$ (kPa)", fontsize=11)
    axes[1].set_title("(b) Mean velocity pressure", fontsize=12)
    axes[1].legend(fontsize=10, loc="upper left")
    axes[2].set_xlabel("Peak velocity pressure $q(1 + 7 I_u)$ (kPa)", fontsize=11)
    axes[2].set_title("(c) Peak velocity pressure, $I_u = 1/\\ln(z/z_0)$", fontsize=12)
    axes[2].legend(fontsize=10, loc="upper left")
    for ax in axes:
        ax.set_ylim(0, Z_MAX)
        ax.grid(True, ls="--", lw=0.5, alpha=0.6)
    axes[1].set_xlim(left=0)
    axes[2].set_xlim(left=0)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    z = np.linspace(Z_MIN, Z_MAX, 300)
    profiles = terrain_profiles(z)
    for name, p in profiles.items():
        f_mean = base_shear(p["z0"], p["u_star"])
        f_peak = base_shear(p["z0"], p["u_star"], peak=True)
        print(
            f"{name:13s} z0 = {p['z0']:<7g} u* = {p['u_star']:.2f} m/s, "
            f"U(10) = {p['u10']:.1f} m/s, U(100) = "
            f"{float(log_law(100.0, p['u_star'], p['z0'])):.1f} m/s, alpha = {p['power_fit'][0]:.3f}, "
            f"I_u(10) = {turbulence_intensity(10.0, p['z0']):.3f}, "
            f"base shear mean = {f_mean / 1e6:.2f} MN, peak-pressure envelope = "
            f"{f_peak / 1e6:.2f} MN"
        )

    fig = make_figure(z, profiles)
    finish_figures(
        {"fluid_loading_wind_profile.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
