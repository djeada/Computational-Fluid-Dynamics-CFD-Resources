"""Road-load power and energy of a passenger car, and quarter-car ride response.

The road-load equation F = m g C_rr + rho C_d A U^2 / 2 + m g sin(theta) + m a
is split into its rolling and aerodynamic parts to find the speed at which
they are equal, the power needed at constant speed, and the energy per 100 km
at constant speed and over a synthetic stop-and-go and highway cycle, with
and without recovery of braking energy. A two-degree-of-freedom quarter-car
model (sprung body, unsprung wheel, suspension spring and damper, tyre
spring) gives the frequency response of body acceleration and tyre
deflection to road displacement for two damping ratios.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GRAVITY = 9.81  # (m/s^2)
RHO_AIR = 1.225  # (kg/m^3)
KWH = 3.6e6  # (J)

# Mid-size car.
MASS = 1500.0  # test mass (kg)
C_RR = 0.010  # rolling-resistance coefficient
C_D = 0.30  # drag coefficient
FRONTAL_AREA = 2.2  # A (m^2)
REGEN_FRACTION = 0.6  # share of braking energy at the wheels that is recovered

# Synthetic drive cycle: (cruise speed km/h, cruise time s, stop time s).
CYCLE_SEGMENTS = (
    (30.0, 20.0, 15.0),
    (50.0, 40.0, 15.0),
    (30.0, 30.0, 10.0),
    (50.0, 60.0, 20.0),
    (80.0, 120.0, 10.0),
    (60.0, 60.0, 10.0),
    (120.0, 300.0, 10.0),
    (100.0, 120.0, 20.0),
)
ACCELERATION = 1.0  # cycle acceleration (m/s^2)
DECELERATION = 0.8  # cycle braking deceleration (m/s^2)
CYCLE_DT = 0.5  # cycle time step (s)

# Quarter car.
SPRUNG_MASS = 400.0  # m_s, a quarter of the body (kg)
UNSPRUNG_MASS = 40.0  # m_u, wheel, hub, brake (kg)
SPRING_RATE = 22.0e3  # k_s, suspension spring (N/m)
TYRE_RATE = 200.0e3  # k_t, tyre vertical stiffness (N/m)
DAMPING_RATIOS = (0.2, 0.5)  # zeta = c_s / (2 sqrt(k_s m_s))


def rolling_force(mass=MASS, crr=C_RR):
    return mass * GRAVITY * crr


def aero_force(speed, cd=C_D, area=FRONTAL_AREA, rho=RHO_AIR):
    return 0.5 * rho * cd * area * speed**2


def road_load(speed, accel=0.0, grade=0.0, mass=MASS):
    """Tractive force F = m g C_rr + rho C_d A U^2/2 + m g sin(theta) + m a (N)."""
    return (
        rolling_force(mass)
        + aero_force(speed)
        + mass * GRAVITY * np.sin(grade)
        + mass * accel
    )


def crossover_speed(mass=MASS, crr=C_RR, cd=C_D, area=FRONTAL_AREA, rho=RHO_AIR):
    """Speed at which aerodynamic drag equals rolling resistance (m/s)."""
    return np.sqrt(2.0 * mass * GRAVITY * crr / (rho * cd * area))


def constant_speed_energy(speed):
    """Wheel energy per 100 km at constant speed on a level road (kWh)."""
    return road_load(speed) * 1.0e5 / KWH


def drive_cycle(segments=CYCLE_SEGMENTS, dt=CYCLE_DT):
    """Speed trace (m/s) of trapezoidal segments that each start and end at rest."""
    speeds = [0.0]
    for v_kmh, cruise, stop in segments:
        v = v_kmh / 3.6
        speeds += list(
            np.arange(1, int(v / (ACCELERATION * dt)) + 1) * ACCELERATION * dt
        )
        speeds += [v] * int(cruise / dt)
        speeds += list(
            v - np.arange(1, int(v / (DECELERATION * dt)) + 1) * DECELERATION * dt
        )
        speeds += [0.0] * int(stop / dt)
    u = np.clip(np.array(speeds), 0.0, None)
    return np.arange(len(u)) * dt, u


def cycle_energy(t, u):
    """Distance (m), traction and braking energy at the wheels (J) of a speed trace."""
    dt = t[1] - t[0]
    u_mid = 0.5 * (u[1:] + u[:-1])
    accel = np.diff(u) / dt
    power = road_load(u_mid, accel) * u_mid
    power = np.where(u_mid > 0.0, power, 0.0)  # no rolling load when stationary
    distance = np.sum(u_mid) * dt
    traction = np.sum(np.clip(power, 0.0, None)) * dt
    braking = -np.sum(np.clip(power, None, 0.0)) * dt
    return distance, traction, braking, power


def quarter_car_matrices(
    zeta, ms=SPRUNG_MASS, mu=UNSPRUNG_MASS, ks=SPRING_RATE, kt=TYRE_RATE
):
    """Mass, damping and stiffness matrices for the coordinates (z_s, z_u)."""
    cs = 2.0 * zeta * np.sqrt(ks * ms)
    m = np.diag([ms, mu])
    c = np.array([[cs, -cs], [-cs, cs]])
    k = np.array([[ks, -ks], [-ks, ks + kt]])
    return m, c, k


def natural_frequencies(ms=SPRUNG_MASS, mu=UNSPRUNG_MASS, ks=SPRING_RATE, kt=TYRE_RATE):
    """Undamped body and wheel-hop frequencies (Hz) from the eigenvalue problem."""
    m, _, k = quarter_car_matrices(0.0, ms, mu, ks, kt)
    omega2 = np.sort(np.linalg.eigvals(np.linalg.solve(m, k)).real)
    return np.sqrt(omega2) / (2.0 * np.pi)


def quarter_car_response(freq, zeta):
    """Body acceleration and tyre deflection per unit road displacement.

    The road enters through the tyre spring as a force k_t z_r on the wheel.
    Returns |a_s / z_r| in (m/s^2)/m and |(z_u - z_r) / z_r|.
    """
    m, c, k = quarter_car_matrices(zeta)
    force = np.array([0.0, TYRE_RATE])
    accel = np.empty(len(freq))
    tyre = np.empty(len(freq))
    for i, f in enumerate(freq):
        w = 2.0 * np.pi * f
        z = np.linalg.solve(k - w**2 * m + 1j * w * c, force)
        accel[i] = abs(-(w**2) * z[0])
        tyre[i] = abs(z[1] - 1.0)
    return accel, tyre


def make_road_load_figure():
    colors = plt.get_cmap("tab10").colors
    u = np.linspace(0.0, 45.0, 300)
    u_c = crossover_speed()
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))

    ax = axes[0]
    p_roll = rolling_force() * u / 1e3
    p_aero = aero_force(u) * u / 1e3
    ax.stackplot(
        u * 3.6,
        p_roll,
        p_aero,
        colors=[colors[0], colors[1]],
        alpha=0.6,
        labels=["rolling resistance", "aerodynamic drag"],
    )
    ax.plot(u * 3.6, p_roll + p_aero, "k", lw=1.5, label="total")
    ax.axvline(u_c * 3.6, color="k", ls="--", lw=1)
    ax.text(u_c * 3.6 + 2, 30, f"$U_c$ = {u_c * 3.6:.0f} km/h", fontsize=10)
    ax.set_xlabel("speed (km/h)")
    ax.set_ylabel("power at the wheels (kW)")
    ax.set_title("(a) Level-road power at constant speed")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3)

    t, speed = drive_cycle()
    distance, traction, braking, power = cycle_energy(t, speed)
    ax = axes[1]
    ax.plot(t, speed * 3.6, color="k", lw=1.5)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("speed (km/h)", color="k")
    ax.set_title("(b) Synthetic drive cycle and wheel power")
    ax.grid(True, alpha=0.3)
    ax2 = ax.twinx()
    t_mid = 0.5 * (t[1:] + t[:-1])
    ax2.fill_between(
        t_mid,
        power / 1e3,
        0.0,
        where=power > 0,
        color=colors[3],
        alpha=0.4,
        label="traction",
    )
    ax2.fill_between(
        t_mid,
        power / 1e3,
        0.0,
        where=power < 0,
        color=colors[2],
        alpha=0.5,
        label="braking",
    )
    ax2.set_ylabel("wheel power (kW)")
    ax2.legend(fontsize=9, loc="upper left")

    ax = axes[2]
    u_e = np.linspace(20.0, 150.0, 200) / 3.6
    ax.plot(
        u_e * 3.6,
        constant_speed_energy(u_e),
        color=colors[0],
        lw=2,
        label="constant speed",
    )
    per_100 = 1.0e5 / distance / KWH
    ax.axhline(
        traction * per_100, color=colors[3], ls="--", lw=1.5, label="cycle, no recovery"
    )
    ax.axhline(
        (traction - REGEN_FRACTION * braking) * per_100,
        color=colors[2],
        ls="--",
        lw=1.5,
        label=f"cycle, {REGEN_FRACTION:.0%} of braking recovered",
    )
    ax.set_xlabel("speed (km/h)")
    ax.set_ylabel("wheel energy (kWh per 100 km)")
    ax.set_title("(c) Energy demand at the wheels")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def make_quarter_car_figure():
    colors = plt.get_cmap("tab10").colors
    freq = np.logspace(-1, np.log10(30.0), 600)
    f_body, f_wheel = natural_frequencies()
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for zeta, color in zip(DAMPING_RATIOS, colors):
        accel, tyre = quarter_car_response(freq, zeta)
        axes[0].loglog(freq, accel, color=color, lw=2, label=rf"$\zeta$ = {zeta}")
        axes[1].loglog(freq, tyre, color=color, lw=2, label=rf"$\zeta$ = {zeta}")
    titles = (
        "(a) Body acceleration per unit road displacement",
        "(b) Tyre deflection per unit road displacement",
    )
    ylabels = (r"$|\ddot z_s / z_r|$ ((m/s$^2$)/m)", r"$|(z_u - z_r) / z_r|$")
    for ax, title, ylabel in zip(axes, titles, ylabels):
        for f0, name in ((f_body, "body"), (f_wheel, "wheel hop")):
            ax.axvline(f0, color="0.5", ls=":", lw=1)
            ax.text(
                f0 * 1.05, ax.get_ylim()[0] * 1.5, f"{name}\n{f0:.2f} Hz", fontsize=9
            )
        ax.set_xlabel("frequency (Hz)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(fontsize=10, loc="upper left")
        ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    u_c = crossover_speed()
    print(
        f"Rolling resistance {rolling_force():.0f} N, crossover speed {u_c:.1f} m/s "
        f"= {u_c * 3.6:.0f} km/h"
    )
    for v_kmh in (50, 90, 120):
        v = v_kmh / 3.6
        print(
            f"  {v_kmh:3d} km/h: force {road_load(v):.0f} N, power {road_load(v) * v / 1e3:.1f} kW, "
            f"{constant_speed_energy(v):.1f} kWh/100 km"
        )
    t, speed = drive_cycle()
    distance, traction, braking, _ = cycle_energy(t, speed)
    per_100 = 1.0e5 / distance / KWH
    print(
        f"Cycle: {t[-1]:.0f} s, {distance / 1e3:.2f} km, mean speed {distance / t[-1] * 3.6:.0f} km/h"
    )
    print(
        f"  traction {traction * per_100:.1f} kWh/100 km, braking {braking * per_100:.1f} kWh/100 km, "
        f"net with {REGEN_FRACTION:.0%} recovery "
        f"{(traction - REGEN_FRACTION * braking) * per_100:.1f} kWh/100 km"
    )
    f_body, f_wheel = natural_frequencies()
    print(f"Quarter car: body {f_body:.2f} Hz, wheel hop {f_wheel:.2f} Hz")

    finish_figures(
        {
            "car_road_load.png": make_road_load_figure(),
            "car_quarter_car.png": make_quarter_car_figure(),
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
