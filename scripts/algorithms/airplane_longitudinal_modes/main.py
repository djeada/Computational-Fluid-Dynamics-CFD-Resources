"""Longitudinal modes of a light aircraft and a pilot-in-the-loop oscillation.

Builds the linearized longitudinal equations of a representative 1100 kg
light aircraft in level flight at 55 m/s from stated non-dimensional
stability derivatives, finds the short-period and phugoid eigenvalues and
compares them with the classical two-state approximations (the phugoid with
Lanchester's omega = sqrt(2) g / U), and integrates the response to a
one-degree elevator step. A second figure closes a pitch-attitude loop with
a pure-gain pilot and a 0.3 s reaction delay: below the critical gain the
loop is stable, above it the pilot drives a growing pilot-induced oscillation.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

G = 9.81  # m/s^2

# Representative four-seat light aircraft, sea level, level flight.
AIRCRAFT = dict(
    mass=1100.0,  # kg
    inertia_y=1825.0,  # kg m^2, pitch moment of inertia
    wing_area=16.2,  # m^2
    chord=1.49,  # m, mean aerodynamic chord
    span=11.0,  # m
    rho=1.225,  # kg/m^3
    speed=55.0,  # m/s, trim airspeed
    cd0=0.027,  # zero-lift drag coefficient
    oswald=0.80,  # span efficiency
    cl_alpha=4.6,  # 1/rad, aircraft lift-curve slope
    cm_alpha=-0.89,  # 1/rad, static stability (static margin 0.19)
    cm_q=-12.4,  # pitch damping per unit q c / (2U)
    cm_alpha_dot=-5.2,  # per unit alpha_dot c / (2U)
    cl_delta_e=0.43,  # 1/rad, elevator lift effectiveness
    cm_delta_e=-1.28,  # 1/rad, elevator control power
)

ELEVATOR_STEP = np.radians(-1.0)  # rad, trailing edge up (nose-up command)
PILOT_DELAY = 0.3  # s, pilot reaction time
PILOT_GAINS = (0.5, 1.0)  # fractions of the critical gain, plus PIO_FACTOR
PIO_FACTOR = 1.1  # gain above critical used to show the divergent PIO
PITCH_COMMAND = np.radians(2.0)  # rad, step in commanded pitch attitude


def trim_and_derivatives(ac=AIRCRAFT):
    """Return trim quantities and the dimensional stability derivatives.

    Body (stability) axes, x forward along the trim velocity, z down,
    nose-up pitch positive. Thrust effects and Z_q, Z_wdot are neglected.
    """
    u0 = ac["speed"]
    q_dyn = 0.5 * ac["rho"] * u0**2
    s, c, m, iy = ac["wing_area"], ac["chord"], ac["mass"], ac["inertia_y"]
    ar = ac["span"] ** 2 / s
    k = 1 / (np.pi * ac["oswald"] * ar)
    cl = m * G / (q_dyn * s)
    cd = ac["cd0"] + k * cl**2
    cd_alpha = 2 * k * cl * ac["cl_alpha"]
    d = dict(u0=u0, cl=cl, cd=cd, q_dyn=q_dyn, aspect_ratio=ar)
    d["Xu"] = -2 * cd * q_dyn * s / (m * u0)
    d["Xw"] = -(cd_alpha - cl) * q_dyn * s / (m * u0)
    d["Zu"] = -2 * cl * q_dyn * s / (m * u0)
    d["Zw"] = -(ac["cl_alpha"] + cd) * q_dyn * s / (m * u0)
    d["Mu"] = 0.0
    d["Mw"] = ac["cm_alpha"] * q_dyn * s * c / (iy * u0)
    d["Mwdot"] = ac["cm_alpha_dot"] * c / (2 * u0) * q_dyn * s * c / (iy * u0)
    d["Mq"] = ac["cm_q"] * c / (2 * u0) * q_dyn * s * c / iy
    d["Zde"] = -ac["cl_delta_e"] * q_dyn * s / m
    d["Mde"] = ac["cm_delta_e"] * q_dyn * s * c / iy
    return d


def state_space(d):
    """A and B of x = [u, w, q, theta], input elevator deflection (rad)."""
    u0 = d["u0"]
    a = np.array(
        [
            [d["Xu"], d["Xw"], 0.0, -G],
            [d["Zu"], d["Zw"], u0, 0.0],
            [
                d["Mu"] + d["Mwdot"] * d["Zu"],
                d["Mw"] + d["Mwdot"] * d["Zw"],
                d["Mq"] + d["Mwdot"] * u0,
                0.0,
            ],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )
    b = np.array([0.0, d["Zde"], d["Mde"] + d["Mwdot"] * d["Zde"], 0.0])
    return a, b


def mode_properties(eigenvalue):
    """Natural frequency (rad/s), damping ratio and period (s) of a complex pole."""
    wn = abs(eigenvalue)
    zeta = -eigenvalue.real / wn
    period = 2 * np.pi / abs(eigenvalue.imag)
    return wn, zeta, period


def split_modes(eigenvalues):
    """Return (short-period, phugoid) poles with positive imaginary part."""
    upper = sorted((e for e in eigenvalues if e.imag > 0), key=abs)
    if len(upper) != 2:
        raise ValueError("expected two oscillatory longitudinal modes")
    return upper[1], upper[0]


def short_period_approximation(d):
    """omega_sp and zeta_sp from the constant-speed two-state model."""
    u0 = d["u0"]
    z_alpha, m_alpha = u0 * d["Zw"], u0 * d["Mw"]
    m_alpha_dot = u0 * d["Mwdot"]
    wn = np.sqrt(z_alpha * d["Mq"] / u0 - m_alpha)
    zeta = -(d["Mq"] + m_alpha_dot + z_alpha / u0) / (2 * wn)
    return wn, zeta


def phugoid_approximation(d):
    """Lanchester frequency sqrt(2) g/U and the damping of the 2-state model."""
    wn = np.sqrt(-d["Zu"] * G / d["u0"])
    zeta = -d["Xu"] / (2 * wn)
    return wn, zeta, np.sqrt(2) * G / d["u0"]


def step_response(a, b, amplitude, t):
    """Exact zero-order-hold response of x' = A x + B u to a step in u."""
    dt = t[1] - t[0]
    n = len(b)
    aug = np.zeros((n + 1, n + 1))
    aug[:n, :n], aug[:n, n] = a * dt, b * dt
    phi = expm(aug)
    ad, bd = phi[:n, :n], phi[:n, n]
    x = np.zeros((len(t), n))
    for i in range(1, len(t)):
        x[i] = ad @ x[i - 1] + bd * amplitude
    return x


def altitude(x, t, u0):
    """Height change from h' = U (theta - alpha), alpha = w / U."""
    hdot = u0 * x[:, 3] - x[:, 1]
    return np.concatenate([[0.0], np.cumsum(0.5 * (hdot[1:] + hdot[:-1]) * np.diff(t))])


# --------------------------------------------------------------------------
# Pilot in the loop
# --------------------------------------------------------------------------
def pitch_frequency_response(a, b, omega):
    """theta / delta_e at s = j omega."""
    out = []
    for w in np.atleast_1d(omega):
        x = np.linalg.solve(1j * w * np.eye(4) - a, b)
        out.append(x[3])
    return np.array(out)


def critical_pilot_gain(a, b, delay=PILOT_DELAY):
    """Gain K of delta_e = K (theta - theta_c) at which the loop is neutral.

    The open loop is L(j w) = -K G(j w) exp(-j w tau); the loop is neutral
    where its phase is -180 degrees and |L| = 1.
    """

    def phase(w):
        val = -pitch_frequency_response(a, b, w)[0] * np.exp(-1j * w * delay)
        return np.angle(val)

    # Scan for the first -180 degree crossing above the phugoid.
    grid = np.linspace(0.8, 20, 4000)
    phases = np.unwrap([phase(w) for w in grid])
    idx = np.where(np.diff(np.sign(phases + np.pi)) != 0)[0][0]
    w180 = brentq(
        lambda w: np.interp(w, grid, phases) + np.pi, grid[idx], grid[idx + 1]
    )
    mag = abs(pitch_frequency_response(a, b, w180)[0])
    return 1 / mag, w180


def simulate_pilot_loop(a, b, gain, t, delay=PILOT_DELAY, command=PITCH_COMMAND):
    """Integrate the aircraft with a delayed pure-gain pitch-attitude pilot.

    delta_e(t) = gain (theta(t - tau) - theta_c); the delay is applied with a
    history buffer on a fixed step, and each step is propagated exactly with
    the zero-order-hold discretization.
    """
    dt = t[1] - t[0]
    n = len(b)
    aug = np.zeros((n + 1, n + 1))
    aug[:n, :n], aug[:n, n] = a * dt, b * dt
    phi = expm(aug)
    ad, bd = phi[:n, :n], phi[:n, n]
    lag = int(round(delay / dt))
    x = np.zeros((len(t), n))
    de = np.zeros(len(t))
    for i in range(1, len(t)):
        theta_seen = x[i - 1 - lag, 3] if i - 1 - lag >= 0 else 0.0
        de[i - 1] = np.clip(gain * (theta_seen - command), -0.5, 0.5)
        x[i] = ad @ x[i - 1] + bd * de[i - 1]
    de[-1] = de[-2]
    return x, de


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def plot_modes(d, a, b, eig):
    sp, ph = split_modes(eig)
    sp_wn, sp_z = short_period_approximation(d)
    ph_wn, ph_z, lanchester = phugoid_approximation(d)
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))

    ax = axes[0]
    for e, label, colour in (
        (sp, "Short period", "tab:blue"),
        (ph, "Phugoid", "tab:orange"),
    ):
        ax.plot(
            [e.real, e.real],
            [e.imag, -e.imag],
            "x",
            color=colour,
            ms=10,
            mew=2,
            label=label,
        )
    sp_approx = -sp_z * sp_wn + 1j * sp_wn * np.sqrt(1 - sp_z**2)
    ax.plot(
        [sp_approx.real] * 2,
        [sp_approx.imag, -sp_approx.imag],
        "o",
        mfc="none",
        color="tab:blue",
        ms=10,
        label="Short-period approximation",
    )
    ax.plot(
        [0, 0],
        [lanchester, -lanchester],
        "s",
        mfc="none",
        color="tab:orange",
        ms=9,
        label=r"Lanchester $\pm j\sqrt{2}g/U$",
    )
    ax.axhline(0, color="0.6", lw=0.8)
    ax.axvline(0, color="0.6", lw=0.8)
    ax.set_xlabel("Real part (1/s)")
    ax.set_ylabel("Imaginary part (rad/s)")
    ax.set_title("(a) Longitudinal eigenvalues")
    ax.legend(fontsize=9, loc="center left")
    ax.grid(alpha=0.3)
    zoom = ax.inset_axes([0.62, 0.58, 0.34, 0.36])
    zoom.plot(
        [ph.real, ph.real], [ph.imag, -ph.imag], "x", color="tab:orange", ms=9, mew=2
    )
    zoom.plot(
        [0, 0], [lanchester, -lanchester], "s", mfc="none", color="tab:orange", ms=8
    )
    zoom.axhline(0, color="0.6", lw=0.8)
    zoom.axvline(0, color="0.6", lw=0.8)
    zoom.set_xlim(-0.06, 0.02)
    zoom.set_ylim(-0.32, 0.32)
    zoom.set_title("Phugoid (zoom)", fontsize=9)
    zoom.tick_params(labelsize=8)

    t_short = np.linspace(0, 6, 601)
    x_short = step_response(a, b, ELEVATOR_STEP, t_short)
    ax = axes[1]
    ax.plot(
        t_short,
        np.degrees(x_short[:, 1] / d["u0"]),
        color="tab:blue",
        label=r"$\Delta\alpha$ (deg)",
    )
    ax.plot(t_short, np.degrees(x_short[:, 2]), color="tab:red", label=r"$q$ (deg/s)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Response")
    ax.set_title(r"(b) First seconds after $\delta_e = -1^\circ$ step")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    t_long = np.linspace(0, 150, 3001)
    x_long = step_response(a, b, ELEVATOR_STEP, t_long)
    h = altitude(x_long, t_long, d["u0"])
    ax = axes[2]
    ax.plot(t_long, x_long[:, 0], color="tab:green", label=r"$\Delta u$ (m/s)")
    ax.plot(
        t_long,
        np.degrees(x_long[:, 3]),
        color="tab:purple",
        label=r"$\Delta\theta$ (deg)",
    )
    ax.plot(t_long, h / 10, color="0.4", ls="--", label=r"$\Delta h$ / 10 (m)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Response")
    ax.set_title("(c) Phugoid after the same step")
    ax.legend(fontsize=10, loc="lower right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def plot_pilot_loop(a, b):
    k_crit, w180 = critical_pilot_gain(a, b)
    t = np.linspace(0, 10, 2001)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6))
    colours = ("tab:blue", "tab:green", "tab:red")
    for factor, colour in zip((*PILOT_GAINS, PIO_FACTOR), colours, strict=True):
        x, de = simulate_pilot_loop(a, b, factor * k_crit, t)
        label = f"K = {factor:g} K$_{{crit}}$"
        axes[0].plot(t, np.degrees(x[:, 3]), color=colour, label=label)
        axes[1].plot(t, np.degrees(de), color=colour, label=label)
    axes[0].axhline(np.degrees(PITCH_COMMAND), color="0.4", ls=":", label="Command")
    axes[0].set_ylim(-6, 10)
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel(r"Pitch attitude $\Delta\theta$ (deg)")
    axes[0].set_title(f"(a) Pilot tracking a 2 deg pitch step, delay {PILOT_DELAY} s")
    axes[0].legend(fontsize=10, loc="upper left")
    axes[0].grid(alpha=0.3)
    axes[1].set_ylim(-15, 15)
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel(r"Elevator $\delta_e$ (deg)")
    axes[1].set_title(
        f"(b) Elevator; K$_{{crit}}$ = {k_crit:.2f}, oscillation at {w180:.2f} rad/s"
    )
    axes[1].legend(fontsize=10, loc="upper left")
    axes[1].grid(alpha=0.3)
    fig.tight_layout()
    return fig, k_crit, w180


def main(argv=None):
    args = create_parser(__doc__).parse_args(argv)
    d = trim_and_derivatives()
    a, b = state_space(d)
    eig = np.linalg.eigvals(a)
    sp, ph = split_modes(eig)
    print(f"Trim: U = {d['u0']:.1f} m/s, C_L = {d['cl']:.3f}, C_D = {d['cd']:.4f}")
    print(
        "Derivatives: "
        + ", ".join(
            f"{k} = {d[k]:.4g}"
            for k in ("Xu", "Xw", "Zu", "Zw", "Mw", "Mwdot", "Mq", "Zde", "Mde")
        )
    )
    for name, e in (("short period", sp), ("phugoid", ph)):
        wn, zeta, period = mode_properties(e)
        print(
            f"  {name}: lambda = {e.real:.4f} +/- {e.imag:.4f}j, "
            f"omega_n = {wn:.3f} rad/s, zeta = {zeta:.3f}, period = {period:.2f} s"
        )
    sp_wn, sp_z = short_period_approximation(d)
    ph_wn, ph_z, lanchester = phugoid_approximation(d)
    print(
        f"  short-period approximation: omega_n = {sp_wn:.3f} rad/s, zeta = {sp_z:.3f}"
    )
    print(
        f"  phugoid approximation: omega_n = {ph_wn:.4f} rad/s (Lanchester {lanchester:.4f}), "
        f"zeta = {ph_z:.4f}, period = {2 * np.pi / lanchester:.1f} s"
    )

    fig_modes = plot_modes(d, a, b, eig)
    fig_pio, k_crit, w180 = plot_pilot_loop(a, b)
    print(
        f"Pilot loop: critical gain {k_crit:.3f} rad/rad at {w180:.3f} rad/s "
        f"(period {2 * np.pi / w180:.2f} s) with a {PILOT_DELAY} s delay"
    )

    finish_figures(
        {
            "airplane_longitudinal_modes.png": fig_modes,
            "airplane_pilot_induced_oscillation.png": fig_pio,
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
