"""PID tuning of a first-order-plus-dead-time process: Ziegler-Nichols against SIMC, and integrator windup.

The process is an electrically heated water stream whose outlet temperature
responds to heater power as G(s) = K exp(-theta s) / (tau s + 1). Three
controllers are tuned from the model: Ziegler-Nichols PID from the step-response
(reaction-curve) table, Ziegler-Nichols PID from the ultimate gain and period,
and the SIMC PI rule of Skogestad (2003) with tau_c = theta. Each closed loop is
simulated in discrete time for a set-point step and a load disturbance, and its
gain margin, phase margin and peak sensitivity are computed. The last two
panels repeat a set-point step with the heater power limited, with and without
back-calculation anti-windup.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

PROCESS_GAIN = 2.0  # K, outlet temperature rise per heater power (K/kW)
TIME_CONSTANT = 10.0  # tau, mixing-volume time constant (s)
DEAD_TIME = 3.0  # theta, transport delay from heater to sensor (s)
DT = 0.01  # controller sample time and simulation step (s)
T_END = 120.0  # simulated time per run (s)
T_PLOT = 80.0  # plotted time window (s)
DERIVATIVE_FILTER_N = 10.0  # N, derivative filter T_f = T_d / N
SETPOINT_STEP = 1.0  # set-point change (K)
LOAD_STEP = -0.5  # load disturbance at the process input (kW), e.g. colder inflow
U_MAX = 0.65  # heater power limit for the windup study (kW); steady state needs 0.5
U_MIN = 0.0  # heater cannot cool (kW)


def ultimate_gain_period(k=PROCESS_GAIN, tau=TIME_CONSTANT, theta=DEAD_TIME):
    """Ultimate gain and period of the FOPDT process under proportional control.

    The phase arctan(w tau) + w theta reaches 180 deg at w_u; K_u = 1/|G(j w_u)|.
    """
    w_u = brentq(lambda w: np.arctan(w * tau) + w * theta - np.pi, 1e-6, np.pi / theta)
    k_u = np.sqrt(1.0 + (w_u * tau) ** 2) / k
    return k_u, 2.0 * np.pi / w_u


def zn_step_pid(k=PROCESS_GAIN, tau=TIME_CONSTANT, theta=DEAD_TIME):
    """Ziegler-Nichols reaction-curve PID: Kc = 1.2 tau/(K theta), Ti = 2 theta, Td = theta/2."""
    return {"kc": 1.2 * tau / (k * theta), "ti": 2.0 * theta, "td": 0.5 * theta}


def zn_ultimate_pid(k=PROCESS_GAIN, tau=TIME_CONSTANT, theta=DEAD_TIME):
    """Ziegler-Nichols ultimate-gain PID: Kc = 0.6 Ku, Ti = Tu/2, Td = Tu/8."""
    k_u, t_u = ultimate_gain_period(k, tau, theta)
    return {"kc": 0.6 * k_u, "ti": t_u / 2.0, "td": t_u / 8.0}


def simc_pi(k=PROCESS_GAIN, tau=TIME_CONSTANT, theta=DEAD_TIME, tau_c=None):
    """SIMC PI (Skogestad 2003): Kc = tau/(K (tau_c + theta)), Ti = min(tau, 4 (tau_c + theta))."""
    tau_c = theta if tau_c is None else tau_c
    return {
        "kc": tau / (k * (tau_c + theta)),
        "ti": min(tau, 4.0 * (tau_c + theta)),
        "td": 0.0,
    }


def controller_response(omega, gains, n=DERIVATIVE_FILTER_N):
    """C(j omega) of the ideal-form PID with a first-order derivative filter."""
    s = 1j * np.asarray(omega, dtype=float)
    td = gains["td"]
    deriv = td * s / (1.0 + td / n * s) if td > 0 else 0.0
    return gains["kc"] * (1.0 + 1.0 / (gains["ti"] * s) + deriv)


def process_response(omega, k=PROCESS_GAIN, tau=TIME_CONSTANT, theta=DEAD_TIME):
    s = 1j * np.asarray(omega, dtype=float)
    return k * np.exp(-theta * s) / (tau * s + 1.0)


def loop_margins(gains):
    """Gain margin, phase margin (deg) and peak sensitivity M_s of C G."""
    omega = np.logspace(-3, 1.5, 200000)
    loop = controller_response(omega, gains) * process_response(omega)
    mag = np.abs(loop)
    phase = np.unwrap(np.angle(loop))
    i_gc = np.nonzero((mag[:-1] >= 1.0) & (mag[1:] < 1.0))[0][0]
    i_pc = np.nonzero((phase[:-1] > -np.pi) & (phase[1:] <= -np.pi))[0][0]
    return {
        "gm": 1.0 / mag[i_pc],
        "pm": 180.0 + np.degrees(phase[i_gc]),
        "ms": np.max(1.0 / np.abs(1.0 + loop)),
    }


def simulate(
    gains,
    setpoint=SETPOINT_STEP,
    load=0.0,
    t_load=0.0,
    u_limits=(-np.inf, np.inf),
    anti_windup=True,
    t_end=T_END,
    dt=DT,
    k=PROCESS_GAIN,
    tau=TIME_CONSTANT,
    theta=DEAD_TIME,
):
    """Discrete-time closed loop of the PID and the FOPDT process.

    The process is discretized exactly for a zero-order hold,
    y[k+1] = a y[k] + K (1 - a) v[k - d] with a = exp(-dt/tau), where v is the
    applied heater power plus the load and d = theta/dt samples. The PID acts
    on the error in P and I and on the measurement in D (no derivative kick),
    with derivative filter T_f = T_d / N. With anti_windup the integrator uses
    back-calculation with tracking time T_t = sqrt(T_i T_d) (T_t = T_i / 2
    for a PI controller).

    Returns t, y, the command u before saturation and the applied u.
    """
    n = int(round(t_end / dt))
    delay = int(round(theta / dt))
    a = np.exp(-dt / tau)
    kc, ti, td = gains["kc"], gains["ti"], gains["td"]
    tf = td / DERIVATIVE_FILTER_N
    t_track = np.sqrt(ti * td) if td > 0 else 0.5 * ti
    t = np.arange(n + 1) * dt
    y = np.zeros(n + 1)
    u_cmd = np.zeros(n + 1)
    u_app = np.zeros(n + 1)
    v_hist = np.zeros(n + 1 + delay)  # v_hist[i + delay] is the input at step i
    integral = 0.0
    deriv = 0.0
    y_prev = 0.0
    for i in range(n + 1):
        e = setpoint - y[i]
        if td > 0:
            deriv = (tf * deriv - kc * td * (y[i] - y_prev)) / (tf + dt)
        u = kc * e + integral + deriv
        u_sat = min(max(u, u_limits[0]), u_limits[1])
        integral += kc * dt / ti * e
        if anti_windup:
            integral += dt / t_track * (u_sat - u)
        u_cmd[i], u_app[i] = u, u_sat
        v_hist[i + delay] = u_sat + (load if t[i] >= t_load else 0.0)
        y_prev = y[i]
        if i < n:
            y[i + 1] = a * y[i] + k * (1.0 - a) * v_hist[i]
    return t, y, u_cmd, u_app


def step_metrics(t, y, target, band=0.02):
    """Overshoot (%) and 2 % settling time of a set-point response."""
    overshoot = 100.0 * max(0.0, (y.max() - target) / target)
    outside = np.nonzero(np.abs(y - target) > band * abs(target))[0]
    settling = (
        t[outside[-1] + 1] if outside.size and outside[-1] + 1 < t.size else np.nan
    )
    return overshoot, settling


def iae(t, y, target):
    """Integral of the absolute error."""
    return np.trapezoid(np.abs(target - y), t)


def tunings():
    return {
        "Ziegler-Nichols step PID": zn_step_pid(),
        "Ziegler-Nichols ultimate PID": zn_ultimate_pid(),
        r"SIMC PI ($\tau_c = \theta$)": simc_pi(),
    }


def make_figure(results, windup):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9.5))
    colors = ("C0", "C1", "C2")
    ax, bx = axes[0]
    for (name, res), color in zip(results.items(), colors):
        ax.plot(res["sp"][0], res["sp"][1], color=color, lw=2, label=name)
        bx.plot(res["ld"][0], res["ld"][1], color=color, lw=2, label=name)
    ax.axhline(SETPOINT_STEP, color="k", lw=0.8, ls=":")
    ax.set_title("(a) Set-point step of 1 K", fontsize=12)
    ax.set_ylabel("Outlet temperature change $y$ (K)", fontsize=11)
    bx.axhline(0.0, color="k", lw=0.8, ls=":")
    bx.set_title(f"(b) Load step of {LOAD_STEP:g} kW at the process input", fontsize=12)
    bx.set_ylabel("Temperature deviation $y$ (K)", fontsize=11)
    for axis in (ax, bx):
        axis.set_xlabel("Time $t$ (s)", fontsize=11)
        axis.set_xlim(0, T_PLOT)
        axis.grid(alpha=0.3)
        axis.legend(fontsize=10, loc="lower right")

    cx, dx = axes[1]
    for (label, (t, y, u_cmd, u_app)), color in zip(windup.items(), ("C3", "C0")):
        cx.plot(t, y, color=color, lw=2, label=label)
        dx.plot(t, u_app, color=color, lw=2, label=f"applied, {label}")
        dx.plot(t, u_cmd, color=color, lw=1.2, ls="--", label=f"PID output, {label}")
    cx.axhline(SETPOINT_STEP, color="k", lw=0.8, ls=":")
    dx.axhline(U_MAX, color="k", lw=0.8)
    dx.text(T_PLOT * 0.98, U_MAX + 0.03, f"limit {U_MAX:g} kW", ha="right", fontsize=10)
    cx.set_title("(c) Saturated heater: integrator windup (SIMC PI)", fontsize=12)
    cx.set_ylabel("Outlet temperature change $y$ (K)", fontsize=11)
    dx.set_title("(d) Heater power, commanded and applied", fontsize=12)
    dx.set_ylabel("Heater power $u$ (kW)", fontsize=11)
    dx.set_ylim(0.0, 1.2)
    for axis in (cx, dx):
        axis.set_xlabel("Time $t$ (s)", fontsize=11)
        axis.set_xlim(0, T_PLOT)
        axis.grid(alpha=0.3)
        axis.legend(fontsize=9, loc="lower right" if axis is cx else "upper right")
    fig.tight_layout()
    return fig


def analyse():
    results = {}
    for name, gains in tunings().items():
        results[name] = {
            "gains": gains,
            "margins": loop_margins(gains),
            "sp": simulate(gains),
            "ld": simulate(gains, setpoint=0.0, load=LOAD_STEP),
        }
    pi = simc_pi()
    windup = {
        "no anti-windup": simulate(pi, u_limits=(U_MIN, U_MAX), anti_windup=False),
        "back-calculation": simulate(pi, u_limits=(U_MIN, U_MAX), anti_windup=True),
    }
    return results, windup


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    k_u, t_u = ultimate_gain_period()
    print(
        f"Process K = {PROCESS_GAIN} K/kW, tau = {TIME_CONSTANT} s, theta = {DEAD_TIME} s"
    )
    print(f"Ultimate gain K_u = {k_u:.4f} kW/K, ultimate period T_u = {t_u:.4f} s")
    results, windup = analyse()
    for name, res in results.items():
        g, m = res["gains"], res["margins"]
        t, y, _, _ = res["sp"]
        os_, ts = step_metrics(t, y, SETPOINT_STEP)
        t_l, y_l, _, _ = res["ld"]
        print(
            f"{name.replace('$', '').replace(chr(92), ''):34s} Kc = {g['kc']:.3f},"
            f" Ti = {g['ti']:.2f} s, Td = {g['td']:.2f} s | GM = {m['gm']:.2f},"
            f" PM = {m['pm']:.1f} deg, Ms = {m['ms']:.2f} | overshoot {os_:.1f} %,"
            f" t_s = {ts:.1f} s, IAE sp = {iae(t, y, SETPOINT_STEP):.2f},"
            f" peak load dev = {y_l.min():.3f} K, IAE load = {iae(t_l, y_l, 0.0):.2f},"
            f" final error {SETPOINT_STEP - y[-1]:.1e}"
        )
    for label, (t, y, u_cmd, u_app) in windup.items():
        os_, ts = step_metrics(t, y, SETPOINT_STEP)
        print(
            f"Saturated SIMC PI, {label}: overshoot {os_:.1f} %, t_s = {ts:.1f} s,"
            f" max PID output {u_cmd.max():.2f} kW"
        )

    fig = make_figure(results, windup)
    finish_figures(
        {"control_pid_tuning.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
