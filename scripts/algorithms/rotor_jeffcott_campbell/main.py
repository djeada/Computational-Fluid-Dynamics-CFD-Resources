"""Jeffcott rotor unbalance response and the Campbell diagram of an overhung rotor.

The Jeffcott rotor is a point disk of mass m on a massless shaft of lateral
stiffness k with viscous damping c and mass eccentricity e. In the complex
whirl coordinate z = x + i y its equation of motion is
m z'' + c z' + k z = m e Omega^2 exp(i Omega t). The script plots the
steady-state whirl amplitude |z|/e and the phase lag between the heavy spot and
the displacement against Omega/omega_n for several damping ratios, and checks
the formula at a set of speeds by integrating the equation of motion in time
until the transient has decayed.

The second part is a rigid disk at the free end of a cantilever shaft, with
translation and tilt coupled through the shaft flexibility and the gyroscopic
moment I_p Omega acting on the tilt. The forward and backward whirl frequencies
are the real roots of a quartic at each speed; plotted against speed they form
the Campbell diagram, and its intersections with the synchronous (1X) line are
the critical speeds, which the script also finds in closed form.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Jeffcott rotor (non-dimensional: omega_n = 1, e = 1).
DAMPING_RATIOS = (0.05, 0.1, 0.2, 0.5)  # zeta = c / (2 sqrt(k m))
CHECK_ZETA = 0.1  # damping ratio of the time-integration check
CHECK_SPEEDS = (0.3, 0.6, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.3, 1.6, 2.0, 2.6)

# Overhung rotor: steel disk at the free end of a steel cantilever shaft.
YOUNGS_MODULUS = 200e9  # E (Pa)
DENSITY = 7850.0  # rho (kg/m^3)
SHAFT_DIAMETER = 0.020  # (m)
SHAFT_LENGTH = 0.10  # bearing to disk (m)
DISK_RADIUS = 0.15  # (m)
DISK_THICKNESS = 0.030  # (m)
MAX_RPM = 15000.0  # speed range of the Campbell diagram (rev/min)


def unbalance_response(speed_ratio, zeta):
    """Steady whirl amplitude |z|/e and phase lag (rad) of the Jeffcott rotor.

    |z|/e = s^2 / sqrt((1 - s^2)^2 + (2 zeta s)^2), phase = atan2(2 zeta s, 1 - s^2),
    with s = Omega / omega_n.
    """
    s = np.asarray(speed_ratio, dtype=float)
    amplitude = s**2 / np.sqrt((1 - s**2) ** 2 + (2 * zeta * s) ** 2)
    phase = np.arctan2(2 * zeta * s, 1 - s**2)
    return amplitude, phase


def peak_response(zeta):
    """Speed ratio and amplitude of the unbalance-response peak (zeta < 1/sqrt 2)."""
    s_peak = 1.0 / np.sqrt(1 - 2 * zeta**2)
    return s_peak, 1.0 / (2 * zeta * np.sqrt(1 - zeta**2))


def integrate_response(speed_ratio, zeta, periods_settle=None):
    """Integrate z'' + 2 zeta z' + z = s^2 exp(i s t) from rest (omega_n = 1, e = 1).

    Returns the amplitude and phase lag of the last few whirl periods, after
    the free vibration has decayed below 1e-6 of its initial size.
    """
    s = speed_ratio
    t_settle = 14.0 / zeta  # exp(-zeta t) < 1e-6
    period = 2 * np.pi / s
    t_end = t_settle + 3 * period

    def rhs(t, y):
        x, vx, yy, vy = y
        fx, fy = s**2 * np.cos(s * t), s**2 * np.sin(s * t)
        return [vx, fx - 2 * zeta * vx - x, vy, fy - 2 * zeta * vy - yy]

    t_eval = np.linspace(t_end - 2 * period, t_end, 400)
    sol = solve_ivp(rhs, (0.0, t_end), [0.0] * 4, t_eval=t_eval, rtol=1e-9, atol=1e-11)
    z = sol.y[0] + 1j * sol.y[2]
    amplitude = np.abs(z).mean()
    # Phase lag of z behind the heavy spot exp(i s t).
    lag = np.angle(np.exp(1j * s * sol.t) / z).mean()
    return amplitude, lag


def overhung_rotor():
    """Mass, inertias and the 2 x 2 stiffness matrix of the overhung disk.

    Coordinates: disk translation and tilt. The flexibility matrix of a
    cantilever loaded at its tip is [[L^3/3, L^2/2], [L^2/2, L]] / (E I).
    """
    second_moment = np.pi * SHAFT_DIAMETER**4 / 64
    ei = YOUNGS_MODULUS * second_moment
    length = SHAFT_LENGTH
    flex = np.array([[length**3 / 3, length**2 / 2], [length**2 / 2, length]]) / ei
    stiffness = np.linalg.inv(flex)
    mass = DENSITY * np.pi * DISK_RADIUS**2 * DISK_THICKNESS
    i_polar = 0.5 * mass * DISK_RADIUS**2
    i_diam = mass * (3 * DISK_RADIUS**2 + DISK_THICKNESS**2) / 12
    return mass, i_polar, i_diam, stiffness


def whirl_frequencies(spin, mass, i_polar, i_diam, stiffness):
    """Whirl frequencies (rad/s) at spin speed Omega (rad/s).

    With z = A exp(i lambda t) the characteristic equation is
    (k11 - m lambda^2)(k22 - I_d lambda^2 + I_p Omega lambda) - k12^2 = 0.
    Returns the four real roots sorted ascending: two backward (negative)
    and two forward (positive).
    """
    k11, k12, k22 = stiffness[0, 0], stiffness[0, 1], stiffness[1, 1]
    coeffs = [
        mass * i_diam,
        -mass * i_polar * spin,
        -(mass * k22 + i_diam * k11),
        k11 * i_polar * spin,
        k11 * k22 - k12**2,
    ]
    roots = np.roots(coeffs)
    return np.sort(roots.real)


def critical_speeds(mass, i_polar, i_diam, stiffness, direction=+1):
    """Spin speeds (rad/s) where a whirl frequency equals direction * Omega.

    Setting lambda = +Omega (forward) or -Omega (backward) in the characteristic
    equation gives m (I_d - d I_p) W^2 - (m k22 + (I_d - d I_p) k11) W + det K = 0
    with W = Omega^2 and d = direction. Only positive W are returned.
    """
    k11, k22 = stiffness[0, 0], stiffness[1, 1]
    i_eff = i_diam - direction * i_polar
    roots = np.roots(
        [mass * i_eff, -(mass * k22 + i_eff * k11), np.linalg.det(stiffness)]
    )
    roots = roots.real[(np.abs(roots.imag) < 1e-9) & (roots.real > 0)]
    return np.sort(np.sqrt(roots))


def campbell_data(n=300):
    mass, i_polar, i_diam, stiffness = overhung_rotor()
    spins = np.linspace(0.0, MAX_RPM * 2 * np.pi / 60, n)
    freqs = np.array(
        [whirl_frequencies(w, mass, i_polar, i_diam, stiffness) for w in spins]
    )
    forward = critical_speeds(mass, i_polar, i_diam, stiffness, +1)
    backward = critical_speeds(mass, i_polar, i_diam, stiffness, -1)
    return spins, freqs, forward, backward


def make_figure(checks, campbell):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4), constrained_layout=True)
    s = np.linspace(0.0, 3.0, 1201)
    colors = ("tab:blue", "tab:orange", "tab:green", "tab:red")
    for zeta, col in zip(DAMPING_RATIOS, colors, strict=True):
        amp, phase = unbalance_response(s, zeta)
        axes[0].plot(s, amp, color=col, label=rf"$\zeta$ = {zeta:g}")
        axes[1].plot(s, np.degrees(phase), color=col, label=rf"$\zeta$ = {zeta:g}")
    s_chk, amp_chk, lag_chk = checks
    axes[0].plot(s_chk, amp_chk, "ko", ms=5, mfc="none", label="time integration")
    axes[1].plot(
        s_chk, np.degrees(lag_chk), "ko", ms=5, mfc="none", label="time integration"
    )
    axes[0].set_ylim(0, 6)
    axes[0].set_ylabel(r"whirl amplitude $|z|/e$")
    axes[0].set_title("(a) Unbalance response amplitude")
    axes[1].set_ylabel("phase lag of displacement behind heavy spot (deg)")
    axes[1].set_yticks(range(0, 181, 30))
    axes[1].axhline(90, color="0.5", lw=0.8)
    axes[1].set_title("(b) Phase")
    for ax in axes[:2]:
        ax.axvline(1.0, color="0.5", lw=0.8, ls="--")
        ax.set_xlabel(r"speed ratio $\Omega/\omega_n$")
        ax.set_xlim(0, 3)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=9)

    ax = axes[2]
    spins, freqs, forward, backward = campbell
    rpm = spins * 60 / (2 * np.pi)
    ax.plot(rpm, freqs[:, 2] / (2 * np.pi), color="tab:blue", label="forward, mode 1")
    ax.plot(rpm, freqs[:, 3] / (2 * np.pi), color="tab:green", label="forward, mode 2")
    ax.plot(
        rpm,
        -freqs[:, 1] / (2 * np.pi),
        color="tab:orange",
        ls="--",
        label="backward, mode 1",
    )
    ax.plot(
        rpm,
        -freqs[:, 0] / (2 * np.pi),
        color="tab:red",
        ls="--",
        label="backward, mode 2",
    )
    ax.plot(rpm, rpm / 60, color="black", lw=1, label="1X (synchronous)")
    for k, w in enumerate(forward):
        label = "forward critical speed" if k == 0 else None
        ax.plot(w * 60 / (2 * np.pi), w / (2 * np.pi), "ks", ms=7, label=label)
        ax.annotate(
            f"{w * 60 / (2 * np.pi):.0f} rpm", (w * 60 / (2 * np.pi), w / (2 * np.pi)),
            textcoords="offset points", xytext=(8, -12), fontsize=9,
        )  # fmt: skip
    for k, w in enumerate(backward):
        label = "backward crossing" if k == 0 else None
        ax.plot(
            w * 60 / (2 * np.pi), w / (2 * np.pi), "ko", ms=6, mfc="none", label=label
        )
    ax.set_xlim(0, MAX_RPM)
    ax.set_ylim(0, 450)
    ax.set_xlabel("rotor speed (rpm)")
    ax.set_ylabel("whirl frequency (Hz)")
    ax.set_title("(c) Campbell diagram, overhung disk")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for zeta in DAMPING_RATIOS:
        s_peak, a_peak = peak_response(zeta)
        print(
            f"zeta = {zeta:4.2f}: peak |z|/e = {a_peak:6.3f} at s = {s_peak:.4f}; "
            f"|z|/e at s = 1: {1 / (2 * zeta):.3f}"
        )
    s_chk = np.array(CHECK_SPEEDS)
    results = [integrate_response(s, CHECK_ZETA) for s in s_chk]
    amp_chk = np.array([r[0] for r in results])
    lag_chk = np.array([r[1] for r in results])
    amp_ref, lag_ref = unbalance_response(s_chk, CHECK_ZETA)
    print(
        f"time integration (zeta = {CHECK_ZETA}): max amplitude error "
        f"{np.abs(amp_chk - amp_ref).max():.1e}, max phase error "
        f"{np.degrees(np.abs(lag_chk - lag_ref)).max():.1e} deg"
    )

    mass, i_polar, i_diam, stiffness = overhung_rotor()
    w0 = whirl_frequencies(0.0, mass, i_polar, i_diam, stiffness)
    print(
        f"overhung disk: m = {mass:.3f} kg, Ip = {i_polar:.5f}, Id = {i_diam:.5f} kg m^2; "
        f"non-rotating frequencies {w0[2] / (2 * np.pi):.1f} and {w0[3] / (2 * np.pi):.1f} Hz"
    )
    campbell = campbell_data()
    for label, direction in (("forward", +1), ("backward", -1)):
        speeds = critical_speeds(mass, i_polar, i_diam, stiffness, direction)
        print(
            f"{label} critical speeds: "
            + ", ".join(f"{w * 30 / np.pi:.0f} rpm" for w in speeds)
        )

    finish_figures(
        {
            "rotor_jeffcott_campbell.png": make_figure(
                (s_chk, amp_chk, lag_chk), campbell
            )
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
