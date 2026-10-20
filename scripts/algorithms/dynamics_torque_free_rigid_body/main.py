"""Torque-free rotation of a rigid box from Euler's equations: stable and unstable axes.

A 0.5 kg box of 200 x 100 x 30 mm is spun at 10 rad/s about each of its three
principal axes with a 1 % disturbance on the other two components. Euler's
equations I1 w1' = (I2 - I3) w2 w3 (and cyclic) are integrated with scipy's
DOP853. Spin about the axes of largest and smallest moment of inertia stays
close to the initial axis, while spin about the intermediate axis grows at the
linearized rate and flips periodically (the tennis-racket or Dzhanibekov
effect). Kinetic energy and the magnitude of the angular momentum, both exact
invariants, are monitored as a check on the integration.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

MASS = 0.5  # m (kg)
LENGTH, WIDTH, THICKNESS = 0.20, 0.10, 0.03  # box edges a, b, c (m)
SPIN_RATE = 10.0  # Omega, initial spin about the chosen axis (rad/s)
DISTURBANCE = 0.01  # other two components as a fraction of Omega
DURATION = 8.0  # (s)
RTOL, ATOL = 1e-11, 1e-12  # DOP853 tolerances


def principal_inertia(m=MASS, a=LENGTH, b=WIDTH, c=THICKNESS):
    """Principal moments (kg m^2) about the axes along a, b and c, ascending."""
    return np.array(
        [m * (b**2 + c**2) / 12.0, m * (a**2 + c**2) / 12.0, m * (a**2 + b**2) / 12.0]
    )


def euler_rhs(_t, omega, inertia):
    """Euler's equations with zero applied moment, body-frame components."""
    i1, i2, i3 = inertia
    w1, w2, w3 = omega
    return [
        (i2 - i3) * w2 * w3 / i1,
        (i3 - i1) * w3 * w1 / i2,
        (i1 - i2) * w1 * w2 / i3,
    ]


def spin(axis, inertia=None, rate=SPIN_RATE, eps=DISTURBANCE, duration=DURATION):
    """Integrate a spin about principal axis `axis` (0, 1, 2) with a small disturbance."""
    inertia = principal_inertia() if inertia is None else inertia
    omega0 = np.full(3, eps * rate)
    omega0[axis] = rate
    t = np.linspace(0.0, duration, 2001)
    sol = solve_ivp(
        euler_rhs,
        (0.0, duration),
        omega0,
        args=(inertia,),
        method="DOP853",
        t_eval=t,
        rtol=RTOL,
        atol=ATOL,
    )
    return sol.t, sol.y


def invariants(omega, inertia):
    """Rotational kinetic energy (J) and |H_G| (kg m^2/s) along a solution."""
    h = inertia[:, None] * omega
    return 0.5 * np.sum(inertia[:, None] * omega**2, axis=0), np.linalg.norm(h, axis=0)


def linear_rates(inertia, rate=SPIN_RATE):
    """Small-disturbance rate about each axis: real growth rate for the intermediate
    axis, wobble frequency (rad/s) for the other two."""
    i1, i2, i3 = inertia
    wobble_1 = rate * np.sqrt((i2 - i1) * (i3 - i1) / (i2 * i3))
    growth_2 = rate * np.sqrt((i2 - i1) * (i3 - i2) / (i1 * i3))
    wobble_3 = rate * np.sqrt((i3 - i1) * (i3 - i2) / (i1 * i2))
    return wobble_1, growth_2, wobble_3


def make_figure():
    """Draw the body-frame angular velocity for spin about each principal axis."""
    inertia = principal_inertia()
    rates = linear_rates(inertia)
    colors = plt.get_cmap("tab10").colors
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), sharey=True)
    titles = (
        rf"(a) Spin about axis 1 ($I_{{min}}$), wobble {rates[0]:.2f} rad/s",
        rf"(b) Axis 2 ($I_{{mid}}$), growth rate {rates[1]:.2f} 1/s",
        rf"(c) Axis 3 ($I_{{max}}$), wobble {rates[2]:.2f} rad/s",
    )
    for axis, ax in enumerate(axes):
        t, omega = spin(axis)
        for j in range(3):
            ax.plot(
                t,
                omega[j] / SPIN_RATE,
                color=colors[j],
                label=rf"$\omega_{j + 1}/\Omega$",
            )
        energy, h = invariants(omega, inertia)
        drift = max(np.ptp(energy) / energy[0], np.ptp(h) / h[0])
        ax.text(
            0.03,
            0.04,
            f"relative change of $T$, $|H_G|$: {drift:.1e}",
            transform=ax.transAxes,
            fontsize=9,
        )
        ax.set(
            xlabel="time $t$ (s)",
            title=titles[axis],
            xlim=(0.0, DURATION),
            ylim=(-1.35, 1.35),
        )
        ax.grid(True, linewidth=0.5, alpha=0.5)
    axes[0].set_ylabel(r"body angular velocity $\omega_i / \Omega$")
    axes[0].legend(fontsize=9, loc="upper right", ncol=3)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    inertia = principal_inertia()
    print(f"I1, I2, I3 = {inertia} kg m^2")
    w1, lam, w3 = linear_rates(inertia)
    print(
        f"linearized: wobble about axis 1 = {w1:.3f} rad/s, growth about axis 2 = {lam:.3f} 1/s, "
        f"wobble about axis 3 = {w3:.3f} rad/s"
    )
    for axis in range(3):
        t, omega = spin(axis)
        energy, h = invariants(omega, inertia)
        print(
            f"spin about axis {axis + 1}: min omega_{axis + 1}/Omega = "
            f"{omega[axis].min() / SPIN_RATE:+.3f}, "
            f"rel. change T = {np.ptp(energy) / energy[0]:.1e}, |H| = {np.ptp(h) / h[0]:.1e}"
        )
    finish_figures(
        {"dynamics_torque_free_rigid_body.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
