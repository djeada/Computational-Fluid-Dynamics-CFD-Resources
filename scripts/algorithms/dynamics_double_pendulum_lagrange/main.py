"""Double pendulum from Lagrange's equations: energy check, normal modes and chaos.

The two Lagrange equations of a planar double pendulum (point masses on
massless rods) are solved for the angular accelerations and integrated with the
adaptive Runge-Kutta 4(5) method of scipy. Linearizing about the hanging
equilibrium gives M q'' + K q = 0; the eigenfrequencies of K phi = w^2 M phi
are compared with the frequencies of the nonlinear motion started at small
amplitude in each mode shape. A large-amplitude release shows chaotic motion
and the relative drift of the total energy T + V, which measures the
integration error because the exact system conserves it.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigh

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GRAVITY = 9.81  # g (m/s^2)
M1, M2 = 1.0, 1.0  # bob masses (kg)
L1, L2 = 1.0, 1.0  # rod lengths (m)
SMALL_AMPLITUDE = 0.02  # largest angle of the small-amplitude runs (rad)
SMALL_DURATION = 40.0  # duration of the small-amplitude runs (s)
LARGE_START = (np.radians(120.0), np.radians(-10.0), 0.0, 0.0)  # th1, th2, w1, w2
LARGE_DURATION = 20.0  # duration of the chaotic run (s)
RTOL, ATOL = 1e-10, 1e-12  # RK45 tolerances
SAMPLES_PER_SECOND = 200  # output sampling of the integrated trajectories


def accelerations(theta1, theta2, omega1, omega2, m1=M1, m2=M2, l1=L1, l2=L2):
    """Solve the two Lagrange equations for the angular accelerations.

    (m1 + m2) l1 th1'' + m2 l2 cos(d) th2'' = -m2 l2 sin(d) w2^2 - (m1 + m2) g sin th1
    l1 cos(d) th1'' + l2 th2'' = l1 sin(d) w1^2 - g sin th2,  with d = th1 - th2
    """
    d = theta1 - theta2
    a11 = (m1 + m2) * l1
    a12 = m2 * l2 * np.cos(d)
    a21 = l1 * np.cos(d)
    a22 = l2
    b1 = -m2 * l2 * np.sin(d) * omega2**2 - (m1 + m2) * GRAVITY * np.sin(theta1)
    b2 = l1 * np.sin(d) * omega1**2 - GRAVITY * np.sin(theta2)
    det = a11 * a22 - a12 * a21
    return (b1 * a22 - a12 * b2) / det, (a11 * b2 - a21 * b1) / det


def rhs(_t, state):
    """First-order system for the state (th1, th2, w1, w2)."""
    theta1, theta2, omega1, omega2 = state
    alpha1, alpha2 = accelerations(theta1, theta2, omega1, omega2)
    return [omega1, omega2, alpha1, alpha2]


def energy(state, m1=M1, m2=M2, l1=L1, l2=L2):
    """Total energy T + V (J) with V = 0 at the pivot height."""
    theta1, theta2, omega1, omega2 = state
    kinetic = 0.5 * (m1 + m2) * l1**2 * omega1**2 + 0.5 * m2 * l2**2 * omega2**2
    kinetic += m2 * l1 * l2 * omega1 * omega2 * np.cos(theta1 - theta2)
    potential = -(m1 + m2) * GRAVITY * l1 * np.cos(theta1)
    potential -= m2 * GRAVITY * l2 * np.cos(theta2)
    return kinetic + potential


def energy_drift(states):
    """Energy error relative to the energy above the hanging rest state."""
    e = energy(states)
    return (e - e[0]) / (e[0] - energy([0.0, 0.0, 0.0, 0.0]))


def linearized_matrices(m1=M1, m2=M2, l1=L1, l2=L2):
    """Mass and stiffness matrices of the motion about theta1 = theta2 = 0."""
    mass = np.array([[(m1 + m2) * l1**2, m2 * l1 * l2], [m2 * l1 * l2, m2 * l2**2]])
    stiffness = np.diag([(m1 + m2) * GRAVITY * l1, m2 * GRAVITY * l2])
    return mass, stiffness


def linear_modes():
    """Eigenfrequencies (rad/s) and mode shapes (columns, largest entry 1)."""
    mass, stiffness = linearized_matrices()
    omega_sq, modes = eigh(stiffness, mass)
    modes = modes / modes[np.argmax(np.abs(modes), axis=0), [0, 1]]
    return np.sqrt(omega_sq), modes


def integrate(state0, duration):
    """Integrate with RK45; return sample times and states (4, n)."""
    t_eval = np.linspace(0.0, duration, int(duration * SAMPLES_PER_SECOND) + 1)
    sol = solve_ivp(
        rhs, (0.0, duration), state0, method="RK45", t_eval=t_eval, rtol=RTOL, atol=ATOL
    )
    return sol.t, sol.y


def measured_frequency(t, signal):
    """Angular frequency from the mean spacing of upward zero crossings."""
    s0, s1 = signal[:-1], signal[1:]
    idx = np.nonzero((s0 < 0.0) & (s1 >= 0.0))[0]
    crossings = t[idx] - s0[idx] * (t[idx + 1] - t[idx]) / (s1[idx] - s0[idx])
    return 2.0 * np.pi / np.mean(np.diff(crossings))


def small_amplitude_study():
    """Start in each linear mode shape and measure the nonlinear frequency."""
    omegas, modes = linear_modes()
    measured = []
    runs = []
    for j in range(2):
        q0 = SMALL_AMPLITUDE * modes[:, j]
        t, y = integrate([q0[0], q0[1], 0.0, 0.0], SMALL_DURATION)
        measured.append(measured_frequency(t, y[0]))
        runs.append((t, y))
    return omegas, modes, np.array(measured), runs


def make_figure(omegas, modes, measured, runs, t_large, y_large):
    """Draw modal responses, the chaotic bob path and the energy drift."""
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.0))
    (ax_mode, ax_spec), (ax_path, ax_energy) = axes
    colors = plt.get_cmap("tab10").colors

    t, y = runs[0]
    window = t <= 8.0
    for j, (t, y) in enumerate(runs):
        ax_mode.plot(
            t[window],
            np.degrees(y[0][window]),
            color=colors[j],
            label=rf"mode {j + 1}: $\theta_1$",
        )
        ax_mode.plot(
            t[window],
            np.degrees(y[1][window]),
            color=colors[j],
            linestyle="--",
            label=rf"mode {j + 1}: $\theta_2$",
        )
    ax_mode.set(
        xlabel="time $t$ (s)",
        ylabel="angle (deg)",
        title=f"(a) Release in each linear mode shape, amplitude {SMALL_AMPLITUDE} rad",
        xlim=(0.0, 8.0),
        ylim=(-1.9, 1.3),
    )
    ax_mode.legend(fontsize=9, ncol=4, loc="lower center")

    # Mixed small-amplitude start excites both modes; its spectrum has two lines.
    t_mix, y_mix = integrate([SMALL_AMPLITUDE, 0.0, 0.0, 0.0], SMALL_DURATION)
    dt = t_mix[1] - t_mix[0]
    window_fn = np.hanning(len(t_mix))
    freq = np.fft.rfftfreq(len(t_mix), dt)
    spectra = [np.abs(np.fft.rfft(y_mix[k] * window_fn)) for k in range(2)]
    peak = max(sp.max() for sp in spectra)
    for k, name in enumerate((r"$\theta_1$", r"$\theta_2$")):
        ax_spec.plot(freq, spectra[k] / peak, color=colors[k + 2], label=name)
    for j, w in enumerate(omegas):
        ax_spec.axvline(
            w / (2 * np.pi),
            color="k",
            linestyle=":",
            label="linearized $f_1$, $f_2$" if j == 0 else None,
        )
    ax_spec.set(
        xlim=(0.0, 1.5),
        ylim=(1e-4, 2.0),
        yscale="log",
        xlabel="frequency (Hz)",
        ylabel="amplitude spectrum (normalized)",
        title=r"(b) Spectrum after release from $\theta_1$ = 0.02 rad, $\theta_2$ = 0",
    )
    ax_spec.legend(fontsize=9, loc="upper right")

    th1, th2 = y_large[0], y_large[1]
    x1, z1 = L1 * np.sin(th1), -L1 * np.cos(th1)
    x2, z2 = x1 + L2 * np.sin(th2), z1 - L2 * np.cos(th2)
    points = ax_path.scatter(x2, z2, c=t_large, s=1.5, cmap="viridis")
    fig.colorbar(points, ax=ax_path, label="time (s)")
    ax_path.plot([0, x1[0], x2[0]], [0, z1[0], z2[0]], "k-o", ms=5, lw=1.5)
    ax_path.set(
        xlim=(-2.1, 2.1),
        ylim=(-2.1, 2.1),
        aspect="equal",
        xlabel="$x$ (m)",
        ylabel="$z$ (m)",
        title=r"(c) Path of bob 2, release from $\theta_1$ = 120°, $\theta_2$ = -10°",
    )

    ax_energy.plot(
        t_large, energy_drift(y_large), color=colors[3], label="large-amplitude run"
    )
    for j, (t, y) in enumerate(runs):
        ax_energy.plot(t, energy_drift(y), color=colors[j], label=f"mode {j + 1} run")
    ax_energy.set(
        xlabel="time $t$ (s)",
        ylabel=r"$(E - E_0)/(E_0 - E_{\mathrm{rest}})$",
        title=f"(d) Energy drift of RK45, rtol = {RTOL:g}",
    )
    ax_energy.legend(fontsize=9, loc="lower left")
    for ax in (ax_mode, ax_spec, ax_path, ax_energy):
        ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    omegas, modes, measured, runs = small_amplitude_study()
    for j in range(2):
        print(
            f"mode {j + 1}: linearized omega = {omegas[j]:.5f} rad/s, "
            f"nonlinear at {SMALL_AMPLITUDE} rad = {measured[j]:.5f} rad/s, "
            f"shape theta2/theta1 = {modes[1, j] / modes[0, j]:+.4f}"
        )
    exact = (
        np.sqrt(GRAVITY / L1 * (2.0 - np.sqrt(2.0))),
        np.sqrt(GRAVITY / L1 * (2.0 + np.sqrt(2.0))),
    )
    print(f"closed form (equal m, l): {exact[0]:.5f}, {exact[1]:.5f} rad/s")
    t_large, y_large = integrate(LARGE_START, LARGE_DURATION)
    drift = np.max(np.abs(energy_drift(y_large)))
    print(f"large run: max |E - E0| / (E0 - E_rest) = {drift:.2e}")

    finish_figures(
        {
            "dynamics_double_pendulum_lagrange.png": make_figure(
                omegas, modes, measured, runs, t_large, y_large
            )
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
