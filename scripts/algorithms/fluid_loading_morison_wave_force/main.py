"""Morison wave force on a vertical pile in a linear (Airy) wave.

Solves the dispersion relation omega^2 = g k tanh(k h) by Newton iteration,
evaluates the Airy particle velocity and acceleration over the depth of a
vertical pile, and integrates the drag and inertia terms of the Morison
equation from the seabed to the still-water level. The figure shows the
force amplitudes per unit length against depth, the time series of the drag,
inertia and total base shear over one wave period with the maximum marked,
and how the share of drag and inertia in the peak force depends on the
Keulegan-Carpenter number.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

G = 9.81  # gravitational acceleration (m/s^2)
RHO_SEA = 1025.0  # seawater density (kg/m^3)

# Example: monopile in intermediate water depth.
PILE_DIAMETER = 2.0  # D (m)
WATER_DEPTH = 20.0  # h (m)
WAVE_HEIGHT = 6.0  # H, crest to trough (m)
WAVE_PERIOD = 10.0  # T (s)
DRAG_COEFF = 1.0  # C_d (-)
INERTIA_COEFF = 2.0  # C_m = 1 + C_a (-)

N_DEPTH = 64  # Gauss-Legendre points over the depth
N_TIME = 721  # samples over one wave period


def wave_number(omega, depth, g=G, tol=1e-12, max_iter=50):
    """Solve omega^2 = g k tanh(k h) for k (rad/m) by Newton iteration.

    The starting value omega^2 / (g sqrt(tanh(omega^2 h / g))) is within a
    few per cent of the root at every depth, so a handful of steps suffices.
    """
    k0 = omega**2 / g
    k = k0 / np.sqrt(np.tanh(k0 * depth))
    for _ in range(max_iter):
        th = np.tanh(k * depth)
        f = g * k * th - omega**2
        df = g * th + g * k * depth * (1.0 - th**2)
        step = f / df
        k = k - step
        if np.all(np.abs(step) < tol * k):
            return k
    raise RuntimeError("dispersion relation did not converge")


def airy_kinematics(z, phase, height, period, depth, g=G):
    """Horizontal velocity and acceleration at x = 0 under an Airy wave.

    z is measured upward from the still-water level (-h <= z <= 0) and
    phase = omega t. The surface elevation is eta = (H/2) cos(phase), so the
    crest passes at phase 0 and the fluid acceleration peaks a quarter period
    earlier, at phase -pi/2. Returns (u, du/dt) broadcast over z and phase.
    """
    omega = 2.0 * np.pi / period
    k = wave_number(omega, depth, g)
    a = 0.5 * height
    shape = np.cosh(k * (z + depth)) / np.sinh(k * depth)
    u = a * omega * shape * np.cos(phase)
    dudt = -a * omega**2 * shape * np.sin(phase)
    return u, dudt


def morison_per_length(u, dudt, diameter, cd, cm, rho=RHO_SEA):
    """Drag and inertia force per unit length (N/m) of the Morison equation."""
    drag = 0.5 * rho * diameter * cd * np.abs(u) * u
    inertia = rho * cm * np.pi * diameter**2 / 4.0 * dudt
    return drag, inertia


def pile_force(
    phase,
    diameter=PILE_DIAMETER,
    depth=WATER_DEPTH,
    height=WAVE_HEIGHT,
    period=WAVE_PERIOD,
    cd=DRAG_COEFF,
    cm=INERTIA_COEFF,
    rho=RHO_SEA,
    n_depth=N_DEPTH,
):
    """Drag, inertia and total base shear (N) and overturning moment (N m).

    Integrates the Morison force per unit length from z = -h to z = 0 (linear
    theory, no stretching above the still-water level) with Gauss-Legendre
    quadrature. The moment is taken about the seabed.
    """
    xg, wg = np.polynomial.legendre.leggauss(n_depth)
    z = -depth * 0.5 * (1.0 - xg)  # map [-1, 1] to [-h, 0]
    w = 0.5 * depth * wg
    u, dudt = airy_kinematics(
        z[:, None], np.atleast_1d(phase)[None, :], height, period, depth
    )
    fd, fi = morison_per_length(u, dudt, diameter, cd, cm, rho)
    drag = w @ fd
    inertia = w @ fi
    moment = (w * (z + depth)) @ (fd + fi)
    return drag, inertia, drag + inertia, moment


def force_amplitudes(
    diameter=PILE_DIAMETER,
    depth=WATER_DEPTH,
    height=WAVE_HEIGHT,
    period=WAVE_PERIOD,
    cd=DRAG_COEFF,
    cm=INERTIA_COEFF,
    rho=RHO_SEA,
):
    """Closed-form amplitudes (F_D, F_I) of the depth-integrated force (N).

    With a = H/2 and kh from the dispersion relation,
    F_I = rho C_m (pi D^2 / 4) a omega^2 / k and
    F_D = (1/2) rho D C_d (a omega)^2 [sinh(2kh)/(4k) + h/2] / sinh^2(kh).
    """
    omega = 2.0 * np.pi / period
    k = wave_number(omega, depth)
    a = 0.5 * height
    f_i = rho * cm * np.pi * diameter**2 / 4.0 * a * omega**2 / k
    profile = (np.sinh(2 * k * depth) / (4 * k) + depth / 2) / np.sinh(k * depth) ** 2
    f_d = 0.5 * rho * diameter * cd * (a * omega) ** 2 * profile
    return f_d, f_i


def peak_force(f_d, f_i):
    """Maximum over phase of F_D |cos(phi)| cos(phi) - F_I sin(phi).

    The peak is F_I when F_D <= F_I / 2, and F_D + F_I^2 / (4 F_D) otherwise.
    """
    f_d = np.asarray(f_d, dtype=float)
    f_i = np.asarray(f_i, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        mixed = f_d + f_i**2 / (4.0 * f_d)
    return np.where(f_d <= f_i / 2.0, f_i, mixed)


def drag_to_inertia_ratio(kc, cd=DRAG_COEFF, cm=INERTIA_COEFF):
    """Ratio of drag to inertia amplitude per unit length, C_d KC / (pi^2 C_m)."""
    return cd * np.asarray(kc) / (np.pi**2 * cm)


def make_figure(depth_case, time_case, kc_case):
    z, fd_amp, fi_amp = depth_case
    phase, drag, inertia, total, i_max = time_case
    kc, kc_example = kc_case
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))

    ax = axes[0]
    ax.plot(fi_amp / 1e3, z, color="tab:blue", lw=2, label="inertia amplitude")
    ax.plot(fd_amp / 1e3, z, color="tab:orange", lw=2, label="drag amplitude")
    ax.axhline(0.0, color="0.4", lw=1, ls="--")
    ax.set_xlim(left=0.0)
    ax.set_xlabel("Force per unit length (kN/m)", fontsize=11)
    ax.set_ylabel("Elevation above still-water level $z$ (m)", fontsize=11)
    ax.set_title("(a) Morison force amplitudes over the depth", fontsize=12)
    ax.legend(fontsize=10, loc="center left")
    ax.grid(True, ls="--", lw=0.5, alpha=0.6)

    ax = axes[1]
    deg = np.degrees(phase)
    ax.plot(deg, inertia / 1e3, color="tab:blue", lw=1.5, label="inertia")
    ax.plot(deg, drag / 1e3, color="tab:orange", lw=1.5, label="drag")
    ax.plot(deg, total / 1e3, color="k", lw=2.2, label="total")
    ax.plot(
        deg[i_max],
        total[i_max] / 1e3,
        "o",
        color="tab:red",
        ms=9,
        label=f"max {total[i_max] / 1e3:.0f} kN at {deg[i_max]:.0f}$^\\circ$",
    )
    ax.axhline(0.0, color="0.4", lw=1)
    ax.set_xlim(-180, 180)
    ax.set_xticks(np.arange(-180, 181, 90))
    ax.set_xlabel("Wave phase $\\omega t$ (degrees, crest at 0)", fontsize=11)
    ax.set_ylabel("Base shear on the pile (kN)", fontsize=11)
    ax.set_title("(b) Depth-integrated force over one period", fontsize=12)
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(True, ls="--", lw=0.5, alpha=0.6)

    ax = axes[2]
    ratio = drag_to_inertia_ratio(kc)
    fmax = peak_force(ratio, 1.0)
    ax.semilogx(kc, 1.0 / fmax, color="tab:blue", lw=2, label="$F_I / F_{max}$")
    ax.semilogx(kc, ratio / fmax, color="tab:orange", lw=2, label="$F_D / F_{max}$")
    kc_first = np.pi**2 * INERTIA_COEFF / (2 * DRAG_COEFF)
    kc_equal = np.pi**2 * INERTIA_COEFF / DRAG_COEFF
    ax.axvline(kc_first, color="0.3", ls="--", lw=1)
    ax.axvline(kc_equal, color="0.3", ls=":", lw=1)
    ax.text(kc_first * 0.93, 1.6, "$F_D = F_I/2$", ha="right", fontsize=10)
    ax.text(kc_equal * 1.07, 1.6, "$F_D = F_I$", ha="left", fontsize=10)
    ax.axvline(kc_example, color="tab:red", lw=1.5)
    ax.text(
        kc_example * 1.06,
        0.12,
        f"example,\nsurface\nKC = {kc_example:.1f}",
        color="tab:red",
        fontsize=10,
    )
    ax.set_ylim(0, 1.8)
    ax.set_xlim(kc[0], kc[-1])
    ax.set_xlabel("Keulegan-Carpenter number KC", fontsize=11)
    ax.set_ylabel("Amplitude / peak total force", fontsize=11)
    ax.set_title(
        f"(c) Regimes per unit length, $C_d$ = {DRAG_COEFF:g}, $C_m$ = {INERTIA_COEFF:g}",
        fontsize=12,
    )
    ax.legend(fontsize=10, loc="center left")
    ax.grid(True, which="both", ls="--", lw=0.5, alpha=0.6)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    omega = 2.0 * np.pi / WAVE_PERIOD
    k = wave_number(omega, WATER_DEPTH)
    wavelength = 2.0 * np.pi / k
    u_max, _ = airy_kinematics(0.0, 0.0, WAVE_HEIGHT, WAVE_PERIOD, WATER_DEPTH)
    _, a_max = airy_kinematics(0.0, -np.pi / 2, WAVE_HEIGHT, WAVE_PERIOD, WATER_DEPTH)
    kc_example = u_max * WAVE_PERIOD / PILE_DIAMETER
    print(
        f"k = {k:.5f} rad/m, wavelength = {wavelength:.1f} m, kh = {k * WATER_DEPTH:.3f}, "
        f"D/L = {PILE_DIAMETER / wavelength:.4f}"
    )
    print(
        f"surface u_max = {u_max:.3f} m/s, du/dt max = {a_max:.3f} m/s^2, "
        f"KC = {kc_example:.2f}"
    )

    z = np.linspace(-WATER_DEPTH, 0.0, 200)
    u_amp, _ = airy_kinematics(z, 0.0, WAVE_HEIGHT, WAVE_PERIOD, WATER_DEPTH)
    _, a_amp = airy_kinematics(z, -np.pi / 2, WAVE_HEIGHT, WAVE_PERIOD, WATER_DEPTH)
    fd_amp, fi_amp = morison_per_length(
        u_amp, a_amp, PILE_DIAMETER, DRAG_COEFF, INERTIA_COEFF
    )

    phase = np.linspace(-np.pi, np.pi, N_TIME)
    drag, inertia, total, moment = pile_force(phase)
    i_max = int(np.argmax(total))
    f_d, f_i = force_amplitudes()
    print(f"closed form: F_D = {f_d / 1e3:.1f} kN, F_I = {f_i / 1e3:.1f} kN")
    print(
        f"quadrature:  F_D = {drag.max() / 1e3:.1f} kN, F_I = {inertia.max() / 1e3:.1f} kN"
    )
    print(
        f"peak base shear = {total[i_max] / 1e3:.1f} kN at omega t = "
        f"{np.degrees(phase[i_max]):.1f} deg (closed form {peak_force(f_d, f_i) / 1e3:.1f} kN)"
    )
    print(f"peak overturning moment about seabed = {moment.max() / 1e6:.2f} MN m")

    kc = np.logspace(0, 2.3, 400)
    fig = make_figure(
        (z, fd_amp, fi_amp),
        (phase, drag, inertia, total, i_max),
        (kc, kc_example),
    )
    finish_figures(
        {"fluid_loading_morison_wave_force.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
