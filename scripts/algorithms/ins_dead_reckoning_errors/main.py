"""Strapdown INS error growth in a vertical plane and INS/GNSS Kalman fusion.

A two-dimensional strapdown mechanization (along-track x, altitude z, pitch
angle theta) integrates a pitch-rate gyro and two body-axis accelerometers.
The script checks the classical error-growth laws on a stationary vehicle:
an accelerometer bias b gives a position error b t^2 / 2, a gyro bias eps
tilts the computed frame and leaks gravity into the horizontal channel,
giving g eps t^3 / 6, and white accelerometer noise gives a random-walk
error with standard deviation N sqrt(t^3 / 3). With Schuler feedback the
bias errors become an 84.4-minute oscillation. A flight profile flown with a
MEMS-grade IMU then shows unaided drift against an error-state Kalman filter
that fuses 1 Hz GNSS position fixes, including a GNSS outage.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GRAVITY = 9.81  # g (m/s^2), flat-Earth constant gravity
EARTH_RADIUS = 6.371e6  # R (m), used only for the Schuler loop
DEG_PER_HOUR = np.pi / 180.0 / 3600.0  # (rad/s) per (deg/h)
SCHULER_PERIOD = 2.0 * np.pi * np.sqrt(EARTH_RADIUS / GRAVITY)  # (s)

# Stationary error-growth study: a navigation-grade IMU.
NAV_ACCEL_BIAS = 5.0e-4  # b (m/s^2), about 50 micro-g
NAV_GYRO_BIAS = 0.01 * DEG_PER_HOUR  # eps (rad/s), 0.01 deg/h
STATIONARY_DT = 1.0  # time step of the stationary runs (s)
STATIONARY_DURATION = 7200.0  # length of the stationary runs (s)
VRW = 0.05 / 60.0  # velocity random walk N (m/s per sqrt(s)), 0.05 m/s/sqrt(h)
NOISE_RUNS = 400  # Monte Carlo runs for the random-walk check
NOISE_DT = 0.1  # time step of the random-walk runs (s)
NOISE_DURATION = 600.0  # length of the random-walk runs (s)

# Flight with a MEMS-grade IMU and GNSS aiding.
IMU_DT = 0.1  # IMU sample interval (s), 10 Hz
FLIGHT_DURATION = 600.0  # (s)
MEMS_ACCEL_BIAS = np.array([0.02, -0.015])  # body-axis accelerometer biases (m/s^2)
MEMS_GYRO_BIAS = 10.0 * DEG_PER_HOUR  # pitch-gyro bias (rad/s), 10 deg/h
MEMS_VRW = 0.1 / 60.0  # accelerometer white noise (m/s per sqrt(s))
MEMS_ARW = 0.3 * np.pi / 180.0 / 60.0  # angle random walk (rad per sqrt(s))
ACCEL_BIAS_RW = 1.0e-4  # accelerometer bias random walk in the filter (m/s^2/sqrt(s))
GYRO_BIAS_RW = 1.0e-6  # gyro bias random walk in the filter (rad/s/sqrt(s))
INITIAL_PITCH_ERROR = 0.5e-3  # initial attitude error of the INS (rad)
GNSS_INTERVAL = 1.0  # time between GNSS fixes (s)
GNSS_SIGMA = np.array([3.0, 5.0])  # GNSS position noise, along-track and vertical (m)
GNSS_OUTAGE = (360.0, 420.0)  # interval without GNSS fixes (s)
SEED = 3


def rotation(theta):
    """Body-to-navigation rotation matrices C_b^n for an array of pitch angles."""
    c, s = np.cos(theta), np.sin(theta)
    return np.stack([np.stack([c, -s], -1), np.stack([s, c], -1)], -2)


GRAVITY_N = np.array([0.0, -GRAVITY])  # gravity in the navigation frame (z up)
J = np.array([[0.0, -1.0], [1.0, 0.0]])  # d C_b^n / d theta = J C_b^n


def smoothstep(t, t0, t1):
    """C1 ramp from 0 at t0 to 1 at t1."""
    s = np.clip((t - t0) / (t1 - t0), 0.0, 1.0)
    return s * s * (3.0 - 2.0 * s)


def flight_profile(t):
    """Speed (m/s) and pitch (rad) of a climb, cruise and descent profile."""
    speed = 70.0 + 50.0 * smoothstep(t, 0.0, 120.0)
    pitch = np.radians(6.0) * (smoothstep(t, 10.0, 40.0) - smoothstep(t, 200.0, 230.0))
    pitch -= np.radians(4.0) * (
        smoothstep(t, 430.0, 460.0) - smoothstep(t, 540.0, 570.0)
    )
    return speed, pitch


def truth_and_imu(t, speed, pitch, start=(0.0, 0.0)):
    """Truth states and the error-free IMU outputs consistent with `mechanize`.

    The IMU samples are obtained by inverting the discrete mechanization, so
    perfect sensors reproduce the truth to round-off.
    """
    dt = t[1] - t[0]
    vel = speed[:, None] * np.stack([np.cos(pitch), np.sin(pitch)], -1)
    gyro = np.diff(pitch) / dt
    accel_n = np.diff(vel, axis=0) / dt
    mid_pitch = pitch[:-1] + 0.5 * gyro * dt
    force_n = accel_n - GRAVITY_N
    force_b = np.einsum("kji,kj->ki", rotation(mid_pitch), force_n)
    pos = np.zeros_like(vel)
    pos[0] = start
    pos[1:] = pos[0] + np.cumsum(0.5 * (vel[:-1] + vel[1:]) * dt, axis=0)
    return {"pos": pos, "vel": vel, "pitch": pitch}, gyro, force_b


def mechanize(dt, gyro, force_b, pos0, vel0, pitch0, schuler=False):
    """Strapdown mechanization in the local-level frame (vectorized unless Schuler).

    theta_{k+1} = theta_k + omega_k dt, f^n = C_b^n(theta_mid) f^b,
    v_{k+1} = v_k + (f^n + g^n) dt, p_{k+1} = p_k + (v_k + v_{k+1}) dt / 2.
    With `schuler=True` the frame is also rotated at the transport rate
    v_x / R, which closes the Schuler loop.
    """
    n = len(gyro)
    if not schuler:
        pitch = pitch0 + np.concatenate(([0.0], np.cumsum(gyro * dt)))
        mid = pitch[:-1] + 0.5 * gyro * dt
        accel = np.einsum("kij,kj->ki", rotation(mid), force_b) + GRAVITY_N
        vel = vel0 + np.concatenate(([[0.0, 0.0]], np.cumsum(accel * dt, axis=0)))
        pos = pos0 + np.concatenate(
            ([[0.0, 0.0]], np.cumsum(0.5 * (vel[:-1] + vel[1:]) * dt, axis=0))
        )
        return pos, vel, pitch
    pos = np.zeros((n + 1, 2))
    vel = np.zeros((n + 1, 2))
    pitch = np.zeros(n + 1)
    pos[0], vel[0], pitch[0] = pos0, vel0, pitch0
    for k in range(n):
        rate = gyro[k] + vel[k, 0] / EARTH_RADIUS  # gyro plus transport rate
        mid = pitch[k] + 0.5 * rate * dt
        accel = rotation(mid) @ force_b[k] + GRAVITY_N
        pitch[k + 1] = pitch[k] + rate * dt
        vel[k + 1] = vel[k] + accel * dt
        pos[k + 1] = pos[k] + 0.5 * (vel[k] + vel[k + 1]) * dt
    return pos, vel, pitch


def stationary_error(
    accel_bias=0.0,
    gyro_bias=0.0,
    schuler=False,
    dt=STATIONARY_DT,
    duration=STATIONARY_DURATION,
):
    """Along-track position error of a level, stationary INS with constant biases."""
    n = int(round(duration / dt))
    t = np.arange(n + 1) * dt
    force_b = np.tile([accel_bias, GRAVITY], (n, 1))  # true f^b = (0, g) plus bias
    gyro = np.full(n, gyro_bias)
    pos, _, _ = mechanize(dt, gyro, force_b, (0.0, 0.0), (0.0, 0.0), 0.0, schuler)
    return t, pos[:, 0]


def schuler_error(t, accel_bias=0.0, gyro_bias=0.0):
    """Linearized Schuler-loop position errors for constant biases (magnitudes)."""
    w = np.sqrt(GRAVITY / EARTH_RADIUS)
    from_accel = accel_bias / w**2 * (1.0 - np.cos(w * t))
    from_gyro = EARTH_RADIUS * gyro_bias * (t - np.sin(w * t) / w)
    return from_accel, from_gyro


def random_walk_study(
    runs=NOISE_RUNS, dt=NOISE_DT, duration=NOISE_DURATION, vrw=VRW, seed=SEED
):
    """RMS along-track error of a stationary INS with white accelerometer noise."""
    rng = np.random.default_rng(seed)
    n = int(round(duration / dt))
    t = np.arange(n + 1) * dt
    noise = rng.normal(0.0, vrw / np.sqrt(dt), size=(runs, n))
    vel = np.concatenate((np.zeros((runs, 1)), np.cumsum(noise * dt, axis=1)), axis=1)
    pos = np.concatenate(
        (np.zeros((runs, 1)), np.cumsum(0.5 * (vel[:, :-1] + vel[:, 1:]) * dt, axis=1)),
        axis=1,
    )
    return t, np.sqrt(np.mean(pos**2, axis=0)), vrw * np.sqrt(t**3 / 3.0)


def error_state_model(force_n, pitch):
    """Continuous-time error-state matrix F for [dp(2), dv(2), dtheta, ba(2), bg]."""
    f = np.zeros((8, 8))
    f[0:2, 2:4] = np.eye(2)
    f[2:4, 4] = J @ force_n
    f[2:4, 5:7] = rotation(pitch)
    f[4, 7] = 1.0
    return f


def run_flight(seed=SEED, aided=True, outage=GNSS_OUTAGE):
    """Fly the profile with a noisy MEMS IMU; optionally fuse GNSS with a Kalman filter.

    Returns a dictionary with time, truth, INS estimate, GNSS fixes and, when
    aided, the position standard deviations, bias estimates and the minimum
    covariance eigenvalue seen during the run.
    """
    rng = np.random.default_rng(seed)
    dt = IMU_DT
    n = int(round(FLIGHT_DURATION / dt))
    t = np.arange(n + 1) * dt
    speed, pitch = flight_profile(t)
    truth, gyro, force_b = truth_and_imu(t, speed, pitch)
    gyro_m = gyro + MEMS_GYRO_BIAS + rng.normal(0.0, MEMS_ARW / np.sqrt(dt), n)
    force_m = (
        force_b + MEMS_ACCEL_BIAS + rng.normal(0.0, MEMS_VRW / np.sqrt(dt), (n, 2))
    )
    gnss_every = int(round(GNSS_INTERVAL / dt))
    gnss = truth["pos"] + rng.normal(0.0, 1.0, (n + 1, 2)) * GNSS_SIGMA

    pos = np.zeros((n + 1, 2))
    vel = np.zeros((n + 1, 2))
    att = np.zeros(n + 1)
    pos[0], vel[0] = truth["pos"][0], truth["vel"][0]
    att[0] = truth["pitch"][0] + INITIAL_PITCH_ERROR
    accel_bias = np.zeros(2)
    gyro_bias = 0.0

    p = np.diag(
        [
            3.0**2,
            5.0**2,
            0.1**2,
            0.1**2,
            (1e-3) ** 2,
            0.03**2,
            0.03**2,
            (20.0 * DEG_PER_HOUR) ** 2,
        ]
    )
    q = (
        np.diag(
            [
                0.0,
                0.0,
                MEMS_VRW**2,
                MEMS_VRW**2,
                MEMS_ARW**2,
                ACCEL_BIAS_RW**2,
                ACCEL_BIAS_RW**2,
                GYRO_BIAS_RW**2,
            ]
        )
        * dt
    )
    h = np.zeros((2, 8))
    h[:, 0:2] = np.eye(2)
    r = np.diag(GNSS_SIGMA**2)
    sigma = np.zeros((n + 1, 2))
    sigma[0] = np.sqrt(np.diag(p)[:2])
    bias_hist = np.zeros((n + 1, 3))
    min_eig = np.inf

    for k in range(n):
        w = gyro_m[k] - gyro_bias
        f_b = force_m[k] - accel_bias
        mid = att[k] + 0.5 * w * dt
        f_n = rotation(mid) @ f_b
        att[k + 1] = att[k] + w * dt
        vel[k + 1] = vel[k] + (f_n + GRAVITY_N) * dt
        pos[k + 1] = pos[k] + 0.5 * (vel[k] + vel[k + 1]) * dt
        if aided:
            phi = np.eye(8) + error_state_model(f_n, mid) * dt
            p = phi @ p @ phi.T + q
            fix = (k + 1) % gnss_every == 0
            in_outage = outage is not None and outage[0] <= t[k + 1] < outage[1]
            if fix and not in_outage:
                z = pos[k + 1] - gnss[k + 1]  # INS minus GNSS = dp + noise
                s = h @ p @ h.T + r
                gain = p @ h.T @ np.linalg.inv(s)
                dx = gain @ z
                ikh = np.eye(8) - gain @ h
                p = ikh @ p @ ikh.T + gain @ r @ gain.T  # Joseph form
                pos[k + 1] -= dx[0:2]  # closed-loop correction, then reset
                vel[k + 1] -= dx[2:4]
                att[k + 1] -= dx[4]
                accel_bias += dx[5:7]
                gyro_bias += dx[7]
                min_eig = min(min_eig, np.linalg.eigvalsh(0.5 * (p + p.T)).min())
            sigma[k + 1] = np.sqrt(np.diag(p)[:2])
        bias_hist[k + 1] = (*accel_bias, gyro_bias)

    result = {
        "t": t,
        "truth": truth,
        "pos": pos,
        "vel": vel,
        "pitch": att,
        "gnss": gnss[::gnss_every],
        "t_gnss": t[::gnss_every],
    }
    if aided:
        result.update(sigma=sigma, bias=bias_hist, min_eig=min_eig)
    return result


def make_error_growth_figure():
    t, err_accel = stationary_error(accel_bias=NAV_ACCEL_BIAS)
    _, err_gyro = stationary_error(gyro_bias=NAV_GYRO_BIAS)
    _, sch_accel = stationary_error(accel_bias=NAV_ACCEL_BIAS, schuler=True)
    _, sch_gyro = stationary_error(gyro_bias=NAV_GYRO_BIAS, schuler=True)
    lin_accel, lin_gyro = schuler_error(t, NAV_ACCEL_BIAS, NAV_GYRO_BIAS)
    t_rw, rms, rw_theory = random_walk_study()

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    colors = plt.get_cmap("tab10").colors
    ax = axes[0]
    ax.loglog(
        t[1:],
        np.abs(err_accel[1:]),
        color=colors[0],
        lw=2.5,
        label=r"accelerometer bias, simulated",
    )
    ax.loglog(
        t[1:],
        0.5 * NAV_ACCEL_BIAS * t[1:] ** 2,
        "k--",
        lw=1,
        label=r"$\frac{1}{2} b t^2$",
    )
    ax.loglog(
        t[1:],
        np.abs(err_gyro[1:]),
        color=colors[1],
        lw=2.5,
        label="gyro bias, simulated",
    )
    ax.loglog(
        t[1:],
        GRAVITY * NAV_GYRO_BIAS * t[1:] ** 3 / 6.0,
        "k:",
        lw=1.2,
        label=r"$\frac{1}{6} g \varepsilon t^3$",
    )
    ax.set_xlabel("time (s)")
    ax.set_ylabel("along-track position error (m)")
    ax.set_title("(a) Flat-Earth error growth, stationary")
    ax.set_ylim(1e-4, 1e5)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, which="both", alpha=0.3)

    ax = axes[1]
    minutes = t / 60.0
    ax.plot(
        minutes,
        np.abs(err_accel) / 1e3,
        color=colors[0],
        lw=1.2,
        ls="--",
        label="accel. bias, flat Earth",
    )
    ax.plot(
        minutes,
        np.abs(sch_accel) / 1e3,
        color=colors[0],
        lw=2.5,
        label="accel. bias, Schuler loop",
    )
    ax.plot(
        minutes,
        np.abs(err_gyro) / 1e3,
        color=colors[1],
        lw=1.2,
        ls="--",
        label="gyro bias, flat Earth",
    )
    ax.plot(
        minutes,
        np.abs(sch_gyro) / 1e3,
        color=colors[1],
        lw=2.5,
        label="gyro bias, Schuler loop",
    )
    ax.plot(minutes, lin_accel / 1e3, "k:", lw=1)
    ax.plot(minutes, lin_gyro / 1e3, "k:", lw=1, label="linearized Schuler solution")
    ax.axvline(SCHULER_PERIOD / 60.0, color="0.5", lw=1)
    ax.text(SCHULER_PERIOD / 60.0 + 1, 4.4, r"$T_s = 84.4$ min", fontsize=10)
    ax.set_ylim(0, 5)
    ax.set_xlim(0, minutes[-1])
    ax.set_xlabel("time (min)")
    ax.set_ylabel("along-track position error (km)")
    ax.set_title("(b) Schuler loop bounds the bias errors")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3)

    ax = axes[2]
    ax.loglog(
        t_rw[1:], rms[1:], color=colors[2], lw=2.5, label=f"RMS of {NOISE_RUNS} runs"
    )
    ax.loglog(t_rw[1:], rw_theory[1:], "k--", lw=1, label=r"$N\sqrt{t^3/3}$")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("RMS position error (m)")
    ax.set_title("(c) Velocity random walk, N = 0.05 m/s/$\\sqrt{h}$")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    return fig


def make_fusion_figure(free, aided):
    colors = plt.get_cmap("tab10").colors
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    t = aided["t"]
    ax = axes[0]
    truth = aided["truth"]["pos"] / 1e3
    ax.plot(truth[:, 0], truth[:, 1], color="k", lw=2.5, label="truth")
    ax.plot(
        free["pos"][:, 0] / 1e3,
        free["pos"][:, 1] / 1e3,
        color=colors[3],
        lw=1.5,
        label="INS only",
    )
    ax.plot(
        aided["pos"][:, 0] / 1e3,
        aided["pos"][:, 1] / 1e3,
        color=colors[0],
        lw=1.5,
        ls="--",
        label="INS/GNSS",
    )
    ax.set_xlabel("along-track distance x (km)")
    ax.set_ylabel("altitude z (km)")
    ax.set_title("(a) Trajectories, MEMS IMU")
    ax.legend(fontsize=9, loc="lower left")
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    err_free = np.linalg.norm(free["pos"] - free["truth"]["pos"], axis=1)
    err_aided = np.linalg.norm(aided["pos"] - truth * 1e3, axis=1)
    sigma3 = 3.0 * np.linalg.norm(aided["sigma"], axis=1)
    ax.semilogy(t, err_free, color=colors[3], lw=2, label="INS only")
    ax.semilogy(t, err_aided, color=colors[0], lw=1.2, label="INS/GNSS")
    ax.semilogy(t, sigma3, color="k", lw=1, ls="--", label=r"filter $3\sigma$")
    ax.axvspan(*GNSS_OUTAGE, color="0.85", label="GNSS outage")
    ax.set_ylim(0.1, 1e5)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("position error (m)")
    ax.set_title("(b) Position error")
    ax.legend(fontsize=9, loc="upper left", ncol=2)
    ax.grid(True, which="both", alpha=0.3)

    ax = axes[2]
    ax.plot(
        t,
        aided["bias"][:, 2] / DEG_PER_HOUR,
        color=colors[1],
        lw=2,
        label="estimated gyro bias",
    )
    ax.axhline(
        MEMS_GYRO_BIAS / DEG_PER_HOUR, color="k", ls="--", lw=1, label="true gyro bias"
    )
    ax.set_xlabel("time (s)")
    ax.set_ylabel("gyro bias (deg/h)")
    ax.set_title("(c) Gyro bias estimate")
    ax.axvspan(*GNSS_OUTAGE, color="0.85")
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    t, err_accel = stationary_error(accel_bias=NAV_ACCEL_BIAS)
    _, err_gyro = stationary_error(gyro_bias=NAV_GYRO_BIAS)
    _, sch_accel = stationary_error(accel_bias=NAV_ACCEL_BIAS, schuler=True)
    print(f"Schuler period: {SCHULER_PERIOD:.0f} s = {SCHULER_PERIOD / 60:.1f} min")
    for minutes in (1, 10, 60, 120):
        k = int(minutes * 60 / STATIONARY_DT)
        print(
            f"  t = {minutes:3d} min: accel-bias error {abs(err_accel[k]):9.1f} m "
            f"(b t^2/2 = {0.5 * NAV_ACCEL_BIAS * t[k] ** 2:9.1f} m), "
            f"gyro-bias error {abs(err_gyro[k]):9.1f} m "
            f"(g eps t^3/6 = {GRAVITY * NAV_GYRO_BIAS * t[k] ** 3 / 6:9.1f} m)"
        )
    print(
        f"  max accel-bias error with Schuler loop: {np.abs(sch_accel).max():.0f} m "
        f"(2 b R / g = {2 * NAV_ACCEL_BIAS * EARTH_RADIUS / GRAVITY:.0f} m)"
    )

    free = run_flight(aided=False)
    aided = run_flight(aided=True)
    err_free = np.linalg.norm(free["pos"] - free["truth"]["pos"], axis=1)
    err_aided = np.linalg.norm(aided["pos"] - aided["truth"]["pos"], axis=1)
    out = (aided["t"] >= GNSS_OUTAGE[0]) & (aided["t"] <= GNSS_OUTAGE[1])
    with_fix = (aided["t"] > 30.0) & ~out
    print("Flight with MEMS IMU:")
    print(
        f"  INS only: error after 60 s {err_free[600]:.0f} m, "
        f"after {FLIGHT_DURATION:.0f} s {err_free[-1]:.0f} m"
    )
    print(
        f"  INS/GNSS: RMS error with fixes {np.sqrt(np.mean(err_aided[with_fix] ** 2)):.2f} m, "
        f"max during {GNSS_OUTAGE[1] - GNSS_OUTAGE[0]:.0f} s outage {err_aided[out].max():.1f} m"
    )
    print(
        f"  final gyro bias estimate {aided['bias'][-1, 2] / DEG_PER_HOUR:.2f} deg/h "
        f"(true {MEMS_GYRO_BIAS / DEG_PER_HOUR:.1f} deg/h)"
    )
    print(f"  smallest covariance eigenvalue after an update: {aided['min_eig']:.2e}")

    finish_figures(
        {
            "ins_error_growth.png": make_error_growth_figure(),
            "ins_gnss_fusion.png": make_fusion_figure(free, aided),
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
