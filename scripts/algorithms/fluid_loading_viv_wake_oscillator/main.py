"""Vortex-induced vibration of a cylinder with a van der Pol wake oscillator.

Integrates the coupled structure and wake oscillators of Facchinetti, de
Langre and Biolley (2004) for an elastically mounted rigid cylinder free to
move across the flow. The wake variable q stands for the fluctuating lift
coefficient and obeys a van der Pol equation forced by the cylinder
acceleration; the cylinder is a damped oscillator forced by the lift. A sweep
over the reduced velocity U_r = U / (f_n D) gives the steady amplitude
response and the response frequency, which locks onto the natural frequency
over a band of U_r instead of following the Strouhal law. A second sweep over
structural damping gives the peak amplitude against mass-damping.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Wake-oscillator constants of Facchinetti et al. (2004).
STROUHAL = 0.2  # St, shedding frequency f_s = St U / D
LIFT_AMPLITUDE = 0.3  # C_L0, lift coefficient of the fixed cylinder
DRAG_COEFF = 2.0  # C_D in the stall parameter gamma = C_D / (4 pi St)
VDP_EPS = 0.3  # van der Pol parameter epsilon
COUPLING_A = 12.0  # acceleration coupling coefficient A
ADDED_MASS_COEFF = 1.0  # C_a of the potential-flow added mass

# Cases.
MASS_RATIOS = (2.0, 20.0)  # m* = m / (rho pi D^2 / 4): water-like and heavier
DAMPING = 0.002  # structural damping ratio zeta of the U_r sweep
UR_SWEEP = np.linspace(2.0, 14.0, 61)  # reduced velocities U / (f_n D)
UR_PEAK = np.linspace(3.5, 9.0, 23)  # band searched for the peak amplitude
DAMPING_SWEEP = np.logspace(-3.5, -0.5, 13)  # zeta values of the mass-damping sweep

DURATION = 800.0  # dimensionless time (units of 1 / Omega_f)
DT = 0.08  # RK4 time step (dimensionless)
KEEP = 0.4  # fraction of the record (at the end) used for statistics


def model_coefficients(ur, mass_ratio, damping):
    """Dimensionless coefficients of the coupled oscillators.

    Time is scaled with the Strouhal angular frequency Omega_f = 2 pi St U / D
    and displacement with D. Returns (delta, c, forcing) for
        y'' + c y' + delta^2 y = forcing q,
    with delta = 1 / (St U_r), c = 2 zeta delta + gamma / mu and
    forcing = C_L0 / (16 pi^2 St^2 mu), where mu = (m* + C_a) pi / 4.
    """
    ur = np.asarray(ur, dtype=float)
    mu = (np.asarray(mass_ratio, dtype=float) + ADDED_MASS_COEFF) * np.pi / 4.0
    delta = 1.0 / (STROUHAL * ur)
    gamma = DRAG_COEFF / (4.0 * np.pi * STROUHAL)
    c = 2.0 * np.asarray(damping, dtype=float) * delta + gamma / mu
    forcing = LIFT_AMPLITUDE / (16.0 * np.pi**2 * STROUHAL**2 * mu)
    return delta, c, forcing


def simulate(
    ur,
    mass_ratio,
    damping,
    duration=DURATION,
    dt=DT,
    coupling=COUPLING_A,
    q0=0.1,
):
    """Integrate all cases at once with RK4; returns (t, y, q) of the kept tail.

    ``ur``, ``mass_ratio`` and ``damping`` broadcast to one array of cases.
    The wake equation q'' + eps (q^2 - 1) q' + q = A y'' uses the structural
    acceleration from the structure equation, so the system is explicit.
    """
    ur, mass_ratio, damping = np.broadcast_arrays(
        np.asarray(ur, float), np.asarray(mass_ratio, float), np.asarray(damping, float)
    )
    delta, c, forcing = model_coefficients(ur, mass_ratio, damping)

    def rhs(state):
        y, v, q, w = state
        acc = forcing * q - c * v - delta**2 * y
        wake = -VDP_EPS * (q * q - 1.0) * w - q + coupling * acc
        return np.stack((v, acc, w, wake))

    state = np.stack(
        (np.zeros_like(ur), np.zeros_like(ur), np.full_like(ur, q0), np.zeros_like(ur))
    )
    n_steps = int(round(duration / dt))
    n_keep = int(KEEP * n_steps)
    y_tail = np.empty((n_keep,) + ur.shape)
    q_tail = np.empty_like(y_tail)
    for i in range(n_steps):
        k1 = rhs(state)
        k2 = rhs(state + 0.5 * dt * k1)
        k3 = rhs(state + 0.5 * dt * k2)
        k4 = rhs(state + dt * k3)
        state = state + dt / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        j = i - (n_steps - n_keep)
        if j >= 0:
            y_tail[j] = state[0]
            q_tail[j] = state[2]
    t = dt * np.arange(n_steps - n_keep + 1, n_steps + 1)
    return t, y_tail, q_tail


def dominant_frequency(signal, dt=DT):
    """Angular frequency of the largest peak of a Hann-windowed, padded FFT."""
    x = signal - signal.mean(axis=0)
    window = np.hanning(len(x)).reshape((-1,) + (1,) * (x.ndim - 1))
    n_fft = 8 * len(x)
    spectrum = np.abs(np.fft.rfft(x * window, n=n_fft, axis=0))
    freqs = 2.0 * np.pi * np.fft.rfftfreq(n_fft, dt)
    return freqs[spectrum.argmax(axis=0)]


def response(ur, mass_ratio, damping, **kwargs):
    """Amplitude A/D and response frequency ratio f / f_n for each case."""
    ur, mass_ratio, damping = np.broadcast_arrays(
        np.asarray(ur, float), np.asarray(mass_ratio, float), np.asarray(damping, float)
    )
    _, y, q = simulate(ur, mass_ratio, damping, **kwargs)
    delta, _, _ = model_coefficients(ur, mass_ratio, damping)
    amplitude = np.abs(y).max(axis=0)
    f_ratio = dominant_frequency(y) / delta
    wake_ratio = dominant_frequency(q) / delta
    return amplitude, f_ratio, wake_ratio


def lock_in_band(ur, f_ratio, tol=0.05):
    """First and last U_r at which |f / f_n - 1| < tol (None if never)."""
    locked = np.abs(f_ratio - 1.0) < tol
    if not locked.any():
        return None
    return ur[locked].min(), ur[locked].max()


def make_figure(sweep, peak):
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.0))
    colors = ("tab:blue", "tab:orange")
    for m_star, color in zip(MASS_RATIOS, colors):
        amp, f_ratio = sweep[m_star]
        label = f"$m^*$ = {m_star:g}"
        axes[0].plot(UR_SWEEP, amp, "o-", ms=4, color=color, label=label)
        axes[1].plot(UR_SWEEP, f_ratio, "o-", ms=4, color=color, label=label)
    axes[0].set_xlabel("Reduced velocity $U_r = U/(f_n D)$", fontsize=11)
    axes[0].set_ylabel("Cross-flow amplitude $A/D$", fontsize=11)
    axes[0].set_title(f"(a) Amplitude response, $\\zeta$ = {DAMPING:g}", fontsize=12)
    axes[0].legend(fontsize=10)

    ax = axes[1]
    ax.plot(
        UR_SWEEP,
        STROUHAL * UR_SWEEP,
        "k--",
        lw=1,
        label="Strouhal law $f_s/f_n = St\\,U_r$",
    )
    ax.axhline(1.0, color="0.4", ls=":", lw=1.2, label="$f = f_n$")
    ax.set_xlabel("Reduced velocity $U_r = U/(f_n D)$", fontsize=11)
    ax.set_ylabel("Response frequency $f/f_n$", fontsize=11)
    ax.set_title("(b) Frequency lock-in", fontsize=12)
    ax.legend(fontsize=10, loc="upper left")

    ax = axes[2]
    for m_star, color in zip(MASS_RATIOS, colors):
        mass_damping = (m_star + ADDED_MASS_COEFF) * DAMPING_SWEEP
        ax.loglog(
            mass_damping,
            peak[m_star],
            "o-",
            ms=5,
            color=color,
            label=f"$m^*$ = {m_star:g}",
        )
    ax.set_xlabel("Mass-damping $(m^* + C_a)\\,\\zeta$", fontsize=11)
    ax.set_ylabel("Peak amplitude $A_{max}/D$", fontsize=11)
    ax.set_title("(c) Peak amplitude against mass-damping", fontsize=12)
    ax.legend(fontsize=10, loc="lower left")
    for ax in axes:
        ax.grid(True, which="both", ls="--", lw=0.5, alpha=0.6)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    # One batched integration: U_r sweep for each mass ratio, then the
    # (zeta, U_r) grid for each mass ratio.
    n_ur, n_pk, n_z = len(UR_SWEEP), len(UR_PEAK), len(DAMPING_SWEEP)
    ur_all, m_all, z_all = [], [], []
    for m_star in MASS_RATIOS:
        ur_all.append(UR_SWEEP)
        m_all.append(np.full(n_ur, m_star))
        z_all.append(np.full(n_ur, DAMPING))
    for m_star in MASS_RATIOS:
        zz, uu = np.meshgrid(DAMPING_SWEEP, UR_PEAK, indexing="ij")
        ur_all.append(uu.ravel())
        m_all.append(np.full(uu.size, m_star))
        z_all.append(zz.ravel())
    amp, f_ratio, _ = response(
        np.concatenate(ur_all), np.concatenate(m_all), np.concatenate(z_all)
    )

    sweep, peak = {}, {}
    start = 0
    for m_star in MASS_RATIOS:
        sweep[m_star] = (amp[start : start + n_ur], f_ratio[start : start + n_ur])
        start += n_ur
    for m_star in MASS_RATIOS:
        block = amp[start : start + n_z * n_pk].reshape(n_z, n_pk)
        peak[m_star] = block.max(axis=1)
        start += n_z * n_pk

    for m_star in MASS_RATIOS:
        a, f = sweep[m_star]
        i = int(np.argmax(a))
        band = lock_in_band(UR_SWEEP, f)
        band_text = "none" if band is None else f"{band[0]:.1f} to {band[1]:.1f}"
        print(
            f"m* = {m_star:g}, zeta = {DAMPING:g}: peak A/D = {a[i]:.3f} at U_r = "
            f"{UR_SWEEP[i]:.1f} (f/f_n = {f[i]:.3f}); |f/f_n - 1| < 5% for U_r {band_text}"
        )
        print(
            "  peak A/D over zeta = "
            + ", ".join(
                f"{z:.4f}: {p:.3f}" for z, p in zip(DAMPING_SWEEP, peak[m_star])
            )
        )

    fig = make_figure(sweep, peak)
    finish_figures(
        {"fluid_loading_viv_wake_oscillator.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
