"""Two-degree-of-freedom spring-mass chain: normal modes and a tuned mass damper.

A 1000 kg primary mass on a 2 Hz spring carries a 50 kg absorber tuned to the
same frequency (mass ratio 0.05). The generalized eigenproblem K phi = w^2 M phi
gives the two natural frequencies and mass-normalized mode shapes, which are
checked against the closed-form roots of the characteristic quadratic. The
receptance of the primary mass shows the single resonance without absorber,
the two resonances and the antiresonance at sqrt(k2/m2) of the undamped
absorber, and the flattened response of Den Hartog's optimally damped absorber.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from scipy.linalg import eigh

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

PRIMARY_MASS = 1000.0  # m1 (kg)
PRIMARY_FREQUENCY_HZ = 2.0  # sqrt(k1/m1) / (2 pi) (Hz)
PRIMARY_DAMPING_RATIO = 0.01  # zeta1 = c1 / (2 sqrt(k1 m1))
MASS_RATIO = 0.05  # mu = m2 / m1
FORCE_AMPLITUDE = 1000.0  # F0 applied to the primary mass (N)

M1 = PRIMARY_MASS
K1 = M1 * (2.0 * np.pi * PRIMARY_FREQUENCY_HZ) ** 2  # k1 (N/m)
C1 = 2.0 * PRIMARY_DAMPING_RATIO * np.sqrt(K1 * M1)  # c1 (N s/m)
M2 = MASS_RATIO * M1  # m2 (kg)


def matrices(m1, m2, k1, k2, c1=0.0, c2=0.0):
    """Mass, stiffness and damping matrices of the chain ground-k1-m1-k2-m2."""
    mass = np.diag([m1, m2])
    stiffness = np.array([[k1 + k2, -k2], [-k2, k2]])
    damping = np.array([[c1 + c2, -c2], [-c2, c2]])
    return mass, stiffness, damping


def normal_modes(mass, stiffness):
    """Natural frequencies (rad/s) and mass-normalized modes (columns)."""
    eigenvalues, modes = eigh(stiffness, mass)
    return np.sqrt(eigenvalues), modes


def closed_form_frequencies(m1, m2, k1, k2):
    """Roots of m1 m2 w^4 - (m1 k2 + m2 (k1 + k2)) w^2 + k1 k2 = 0 (rad/s)."""
    a = m1 * m2
    b = m1 * k2 + m2 * (k1 + k2)
    c = k1 * k2
    disc = np.sqrt(b**2 - 4.0 * a * c)
    return np.sqrt(np.array([(b - disc) / (2.0 * a), (b + disc) / (2.0 * a)]))


def receptance(omega, mass, stiffness, damping, force):
    """Complex steady-state amplitudes X(w) = (K - w^2 M + i w C)^-1 F."""
    out = np.empty((len(omega), len(force)), dtype=complex)
    for i, w in enumerate(omega):
        dynamic = stiffness - w**2 * mass + 1j * w * damping
        out[i] = np.linalg.solve(dynamic, force)
    return out


def den_hartog_tuning(mu):
    """Optimal frequency ratio f = w_a / w_1 and absorber damping ratio."""
    return 1.0 / (1.0 + mu), np.sqrt(3.0 * mu / (8.0 * (1.0 + mu) ** 3))


def plain(label):
    """Strip TeX markup from a legend label for console output."""
    return label.replace("$", "").replace("\\", "").replace("\n", ", ")


def absorber_cases():
    """Return (label, k2, c2) for the undamped tuned and optimally damped absorbers."""
    omega1 = np.sqrt(K1 / M1)
    k_tuned = M2 * omega1**2
    f_opt, zeta_opt = den_hartog_tuning(MASS_RATIO)
    k_opt = M2 * (f_opt * omega1) ** 2
    c_opt = 2.0 * zeta_opt * np.sqrt(k_opt * M2)
    return [
        ("tuned, undamped", k_tuned, 0.0),
        (
            rf"Den Hartog optimum"
            "\n"
            rf"$f_a/f_1$ = {f_opt:.3f}, $\zeta_a$ = {zeta_opt:.3f}",
            k_opt,
            c_opt,
        ),
    ]


def spring_xy(x_start, x_end, y, coils=6, height=0.08):
    """Zigzag polyline of a spring between two x positions at height y."""
    lead = 0.15 * (x_end - x_start)
    xs = np.linspace(x_start + lead, x_end - lead, 2 * coils + 1)
    ys = y + height * np.array(
        [0.0] + [(-1) ** i for i in range(2 * coils - 1)] + [0.0]
    )
    return np.r_[x_start, xs, x_end], np.r_[y, ys, y]


def draw_modes(ax, frequencies, modes):
    """Draw the chain at rest (dashed) and displaced in each mode (filled)."""
    colors = plt.get_cmap("tab10").colors
    sizes = (0.34, 0.24)  # drawn box sizes of m1 and m2
    x_rest = np.array([1.0, 2.0])
    for j in range(2):
        y = -1.5 * j
        x_mode = x_rest + modes[:, j] / np.max(np.abs(modes[:, j])) * 0.4
        ax.plot([0.0, 0.0], [y - 0.3, y + 0.3], color="0.2", linewidth=3)
        for xr, xm, size in zip(x_rest, x_mode, sizes):
            ax.add_patch(
                Rectangle(
                    (xr - size / 2, y - size / 2),
                    size,
                    size,
                    fill=False,
                    edgecolor="0.6",
                    linestyle="--",
                )
            )
            ax.add_patch(
                Rectangle(
                    (xm - size / 2, y - size / 2),
                    size,
                    size,
                    color=colors[j],
                    alpha=0.9,
                )
            )
            if abs(xm - xr) > 0.02:
                ax.annotate(
                    "",
                    xy=(xm, y + 0.3),
                    xytext=(xr, y + 0.3),
                    arrowprops={"arrowstyle": "->", "color": "k", "lw": 1.4},
                )
        for x_a, x_b in ((0.0, x_mode[0] - sizes[0] / 2),):
            ax.plot(*spring_xy(x_a, x_b, y), color="0.3", linewidth=1.1)
        ax.plot(
            *spring_xy(x_mode[0] + sizes[0] / 2, x_mode[1] - sizes[1] / 2, y),
            color="0.3",
            linewidth=1.1,
        )
        ratio = modes[1, j] / modes[0, j]
        ax.text(
            1.25,
            y - 0.6,
            f"mode {j + 1}: {frequencies[j] / (2 * np.pi):.3f} Hz, "
            rf"$\phi_2/\phi_1$ = {ratio:+.2f}",
            ha="center",
            fontsize=10,
        )
    for xr, name in zip(x_rest, ("$m_1$", "$m_2$")):
        ax.text(xr, 0.5, name, ha="center", fontsize=11)
    ax.set(xlim=(-0.2, 2.6), ylim=(-2.4, 0.8), aspect="equal")
    ax.set_title("(a) Mode shapes, tuned absorber")
    ax.axis("off")


def make_figure():
    """Draw mode shapes and the receptance of the primary and absorber masses."""
    k_tuned = absorber_cases()[0][1]
    mass, stiffness, _ = matrices(M1, M2, K1, k_tuned)
    frequencies, modes = normal_modes(mass, stiffness)

    fig = plt.figure(figsize=(13.0, 5.4))
    grid = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.15, 1.0])
    ax_modes = fig.add_subplot(grid[0])
    ax_frf = fig.add_subplot(grid[1])
    ax_abs = fig.add_subplot(grid[2])
    draw_modes(ax_modes, frequencies, modes)

    f_hz = np.linspace(1.0, 3.0, 2001)
    omega = 2.0 * np.pi * f_hz
    static = FORCE_AMPLITUDE / K1
    colors = plt.get_cmap("tab10").colors
    alone = FORCE_AMPLITUDE / np.abs(K1 - omega**2 * M1 + 1j * omega * C1)
    ax_frf.plot(f_hz, alone / static, color="0.4", label="no absorber")
    for i, (label, k2, c2) in enumerate(absorber_cases()):
        m, k, c = matrices(M1, M2, K1, k2, C1, c2)
        x = receptance(omega, m, k, c, np.array([FORCE_AMPLITUDE, 0.0]))
        ax_frf.plot(f_hz, np.abs(x[:, 0]) / static, color=colors[i + 2], label=label)
        ax_abs.plot(
            f_hz,
            np.abs(x[:, 1] - x[:, 0]) / static,
            color=colors[i + 2],
            label=label,
        )
    f_anti = np.sqrt(k_tuned / M2) / (2.0 * np.pi)
    for f in frequencies / (2.0 * np.pi):
        ax_frf.axvline(f, color=colors[0], linestyle=":", linewidth=1.0)
    ax_frf.annotate(
        f"antiresonance\n{f_anti:.2f} Hz",
        xy=(f_anti, 0.02),
        xytext=(1.2, 0.03),
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "k"},
    )
    ax_frf.set(
        yscale="log",
        ylim=(0.01, 3000.0),
        xlim=(f_hz[0], f_hz[-1]),
        xlabel="forcing frequency (Hz)",
        ylabel=r"$|X_1| k_1 / F_0$",
        title="(b) Primary mass response, $\\mu$ = 0.05",
    )
    ax_frf.legend(fontsize=9, loc="upper left")
    ax_abs.set(
        yscale="log",
        ylim=(0.1, 1000.0),
        xlim=(f_hz[0], f_hz[-1]),
        xlabel="forcing frequency (Hz)",
        ylabel=r"$|X_2 - X_1| k_1 / F_0$",
        title="(c) Absorber stroke relative to primary",
    )
    ax_abs.legend(fontsize=9, loc="lower right")
    for ax in (ax_frf, ax_abs):
        ax.grid(True, which="both", linewidth=0.5, alpha=0.4)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for label, k2, c2 in absorber_cases():
        mass, stiffness, _ = matrices(M1, M2, K1, k2)
        frequencies, modes = normal_modes(mass, stiffness)
        exact = closed_form_frequencies(M1, M2, K1, k2)
        print(f"{plain(label)}: k2 = {k2:.1f} N/m, c2 = {c2:.1f} N s/m")
        print(
            f"  eigh: f = {frequencies / (2 * np.pi)} Hz, "
            f"closed form: {exact / (2 * np.pi)} Hz"
        )
        print(f"  mode ratios phi2/phi1 = {modes[1] / modes[0]}")
    f_hz = np.linspace(1.0, 3.0, 2001)
    omega = 2.0 * np.pi * f_hz
    for label, k2, c2 in absorber_cases():
        m, k, c = matrices(M1, M2, K1, k2, C1, c2)
        x = receptance(omega, m, k, c, np.array([FORCE_AMPLITUDE, 0.0]))
        peak = np.max(np.abs(x[:, 0])) * K1 / FORCE_AMPLITUDE
        print(f"  peak |X1| k1/F0 = {peak:.2f} ({plain(label)})")
    print(f"primary alone peak = {1.0 / (2.0 * PRIMARY_DAMPING_RATIO):.1f}")

    finish_figures(
        {"dynamics_two_dof_modes.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
