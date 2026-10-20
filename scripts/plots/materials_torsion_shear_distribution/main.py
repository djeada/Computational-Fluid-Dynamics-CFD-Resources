"""Plot torsional shear stress in solid, hollow, rectangular and thin-walled sections.

A solid 60 mm shaft and a hollow 70/50 mm shaft carry the same torque; the
shear stress grows linearly with radius, tau = T rho / J, and the hollow
shaft uses less material at a lower peak stress. The coefficients alpha and
beta of a solid rectangle (tau_max = T/(alpha a b^2), J_t = beta a b^3) are
computed from Saint-Venant's series solution. A thin-walled rectangular tube
with walls of different thickness carries a constant shear flow
q = T/(2 A_m), so by the Bredt-Batho formula the thinnest wall has the
highest stress.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

TORQUE_SHAFT = 3.0e3  # torque on both circular shafts (N m)
D_SOLID = 0.060  # solid shaft diameter (m)
D_OUTER, D_INNER = 0.070, 0.050  # hollow shaft diameters (m)

TORQUE_TUBE = 1.0e3  # torque on the thin-walled tube (N m)
TUBE_WIDTH, TUBE_HEIGHT = 0.100, 0.050  # median-line dimensions of the tube (m)
TUBE_WALLS = {"top": 3e-3, "bottom": 3e-3, "left": 5e-3, "right": 2e-3}  # (m)
SHEAR_MODULUS = 80e9  # steel (Pa)
WALL_DRAW_SCALE = 2.0  # walls are drawn this many times thicker for visibility

SERIES_TERMS = 60  # odd terms in the rectangle series


def polar_moment(d_outer, d_inner=0.0):
    """Return the polar second moment of area J of a (hollow) circle (m^4)."""
    return np.pi * (d_outer**4 - d_inner**4) / 32.0


def shaft_shear(torque, rho, d_outer, d_inner=0.0):
    """Return tau = T rho / J (Pa) at radius rho inside the material."""
    return torque * np.asarray(rho) / polar_moment(d_outer, d_inner)


def rectangle_coefficients(aspect, terms=SERIES_TERMS):
    """Return (alpha, beta) for a solid a x b rectangle with aspect = a/b >= 1.

    tau_max = T / (alpha a b^2) at the middle of the long side and the
    torsion constant is J_t = beta a b^3, so the twist rate is T/(G J_t).
    From the series solution of Saint-Venant (Timoshenko and Goodier).
    """
    aspect = np.atleast_1d(np.asarray(aspect, dtype=float))[:, None]
    n = np.arange(1, 2 * terms, 2, dtype=float)[None, :]
    x = n * np.pi * aspect / 2.0
    beta = (
        1.0 - 192.0 / (np.pi**5 * aspect[:, 0]) * np.sum(np.tanh(x) / n**5, axis=1)
    ) / 3.0
    sech = 2.0 * np.exp(-x) / (1.0 + np.exp(-2.0 * x))
    k = 1.0 - 8.0 / np.pi**2 * np.sum(sech / n**2, axis=1)
    alpha = beta / k
    return alpha.squeeze(), beta.squeeze()


def tube_properties(
    torque=TORQUE_TUBE,
    width=TUBE_WIDTH,
    height=TUBE_HEIGHT,
    walls=TUBE_WALLS,
    shear_modulus=SHEAR_MODULUS,
):
    """Return shear flow q (N/m), wall stresses (Pa) and twist rate (rad/m)."""
    area = width * height
    q = torque / (2.0 * area)
    stresses = {name: q / t for name, t in walls.items()}
    lengths = {"top": width, "bottom": width, "left": height, "right": height}
    contour = sum(lengths[name] / t for name, t in walls.items())
    twist_rate = torque * contour / (4.0 * area**2 * shear_modulus)
    return q, stresses, twist_rate


def draw_sections(ax):
    """Colour the solid and hollow cross-sections by |tau|."""
    vmax = shaft_shear(TORQUE_SHAFT, D_SOLID / 2, D_SOLID) / 1e6
    images = []
    for centre, d_o, d_i, name in (
        (-0.045, D_SOLID, 0.0, "solid 60 mm"),
        (0.045, D_OUTER, D_INNER, "hollow 70/50 mm"),
    ):
        x = np.linspace(-d_o / 2, d_o / 2, 301)
        xx, yy = np.meshgrid(x, x)
        rho = np.hypot(xx, yy)
        tau = shaft_shear(TORQUE_SHAFT, rho, d_o, d_i) / 1e6
        tau = np.where((rho <= d_o / 2) & (rho >= d_i / 2), tau, np.nan)
        images.append(
            ax.pcolormesh(
                (xx + centre) * 1e3,
                yy * 1e3,
                tau,
                cmap="viridis",
                vmin=0,
                vmax=vmax,
                shading="auto",
            )
        )
        for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            for rho_a in (0.6 * d_o / 2, 0.92 * d_o / 2):
                if rho_a < d_i / 2:
                    continue
                px, py = rho_a * np.cos(angle), rho_a * np.sin(angle)
                length = rho_a / (d_o / 2) * 7e-3
                ax.annotate(
                    "",
                    xy=(
                        (centre + px - length * np.sin(angle)) * 1e3,
                        (py + length * np.cos(angle)) * 1e3,
                    ),
                    xytext=((centre + px) * 1e3, py * 1e3),
                    arrowprops={
                        "arrowstyle": "-|>",
                        "color": "white",
                        "lw": 0.9,
                        "mutation_scale": 10,
                    },
                )
        ax.text(
            centre * 1e3, -d_o / 2 * 1e3 - 6, name, ha="center", va="top", fontsize=10
        )
    plt.colorbar(images[0], ax=ax, label=r"$\tau$ (MPa)", shrink=0.8)
    ax.set(
        aspect="equal",
        xlim=(-85, 85),
        ylim=(-50, 40),
        xlabel="$y$ (mm)",
        ylabel="$z$ (mm)",
        title=rf"Same torque $T$ = {TORQUE_SHAFT / 1e3:.0f} kN m, arrows show $\tau$",
    )


def make_figure():
    """Draw the four panels."""
    fig = plt.figure(figsize=(13, 9.5))
    grid = fig.add_gridspec(2, 5)
    sections = fig.add_subplot(grid[0, :3])
    profile = fig.add_subplot(grid[0, 3:])
    rect = fig.add_subplot(grid[1, :2])
    tube = fig.add_subplot(grid[1, 2:])

    draw_sections(sections)

    for d_o, d_i, color, name in (
        (D_SOLID, 0.0, "tab:blue", "solid 60 mm"),
        (D_OUTER, D_INNER, "tab:orange", "hollow 70/50 mm"),
    ):
        rho = np.linspace(d_i / 2, d_o / 2, 50)
        tau = shaft_shear(TORQUE_SHAFT, rho, d_o, d_i) / 1e6
        area = np.pi * (d_o**2 - d_i**2) / 4 * 1e6
        profile.plot(
            rho * 1e3,
            tau,
            color=color,
            lw=2,
            label=rf"{name}: $\tau_{{max}}$ = {tau[-1]:.1f} MPa, A = {area:.0f} mm$^2$",
        )
        profile.plot(rho[-1] * 1e3, tau[-1], "o", color=color)
    profile.plot(
        [0, D_OUTER / 2 * 1e3],
        [0, shaft_shear(TORQUE_SHAFT, D_OUTER / 2, D_OUTER, D_INNER) / 1e6],
        color="tab:orange",
        lw=0.8,
        ls=":",
    )
    profile.set(
        xlim=(0, 37),
        ylim=(0, 100),
        xlabel=r"radius $\rho$ (mm)",
        ylabel=r"shear stress $\tau$ (MPa)",
        title=r"Linear profile $\tau = T\rho/J$",
    )
    profile.legend(fontsize=10, loc="upper left")

    ratio = np.linspace(1.0, 10.0, 200)
    alpha, beta = rectangle_coefficients(ratio)
    rect.plot(
        ratio,
        alpha,
        color="tab:blue",
        lw=2,
        label=r"$\alpha$: $\tau_{max} = T/(\alpha a b^2)$",
    )
    rect.plot(
        ratio, beta, color="tab:orange", lw=2, label=r"$\beta$: $J_t = \beta a b^3$"
    )
    rect.axhline(1 / 3, color="0.4", ls="--", lw=1, label=r"thin strip limit $1/3$")
    marks = np.array([1.0, 2.0, 4.0, 10.0])
    a_m, b_m = rectangle_coefficients(marks)
    for r, a, b in zip(marks, a_m, b_m):
        rect.plot([r, r], [a, b], "o", color="0.2", ms=4)
        rect.annotate(
            f"{a:.3f}",
            (r, a),
            xytext=(4, 6),
            textcoords="offset points",
            fontsize=10,
            color="tab:blue",
        )
        rect.annotate(
            f"{b:.3f}",
            (r, b),
            xytext=(4, -14),
            textcoords="offset points",
            fontsize=10,
            color="tab:orange",
        )
    rect.set(
        xlim=(1, 10),
        ylim=(0.1, 0.36),
        xlabel="aspect ratio $a/b$ (long/short side)",
        ylabel="coefficient (-)",
        title="Solid rectangle, Saint-Venant series",
    )
    rect.legend(fontsize=10, loc="center right")

    q, stresses, twist = tube_properties()
    vmin, vmax = 0.0, max(stresses.values()) / 1e6
    cmap = plt.get_cmap("viridis")
    w, h = TUBE_WIDTH * 1e3, TUBE_HEIGHT * 1e3
    walls = TUBE_WALLS
    t = {name: WALL_DRAW_SCALE * value * 1e3 for name, value in walls.items()}
    geometry = {
        "top": (-w / 2, h / 2 - t["top"] / 2, w, t["top"]),
        "bottom": (-w / 2, -h / 2 - t["bottom"] / 2, w, t["bottom"]),
        "left": (-w / 2 - t["left"] / 2, -h / 2, t["left"], h),
        "right": (w / 2 - t["right"] / 2, -h / 2, t["right"], h),
    }
    for name, (x0, y0, dx, dy) in geometry.items():
        tau = stresses[name] / 1e6
        tube.add_patch(Rectangle((x0, y0), dx, dy, color=cmap(tau / vmax)))
    labels = {
        "top": (0, h / 2 + 5, "center", "bottom"),
        "bottom": (0, -h / 2 - 5, "center", "top"),
        "left": (-w / 2 - 10, 0, "right", "center"),
        "right": (w / 2 + 6, 0, "left", "center"),
    }
    for name, (x, y, ha, va) in labels.items():
        tube.text(
            x,
            y,
            f"t = {walls[name] * 1e3:.0f} mm\n"
            + rf"$\tau$ = {stresses[name] / 1e6:.1f} MPa",
            ha=ha,
            va=va,
            fontsize=10,
        )
    tube.plot(
        [-w / 2, w / 2, w / 2, -w / 2, -w / 2],
        [h / 2, h / 2, -h / 2, -h / 2, h / 2],
        color="0.5",
        lw=0.6,
        ls="--",
    )
    tube.text(
        0,
        0,
        f"median line {w:.0f} x {h:.0f} mm\n$A_m$ = {w * h:.0f} mm$^2$\n"
        f"q = T/(2$A_m$) = {q / 1e3:.0f} N/mm",
        ha="center",
        va="center",
        fontsize=10,
    )
    tube.text(
        0,
        -54,
        rf"twist rate {np.degrees(twist):.3f}$^\circ$/m for G = 80 GPa;"
        f" walls drawn {WALL_DRAW_SCALE:.0f}x thicker",
        ha="center",
        va="top",
        fontsize=10,
        color="0.3",
    )
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin, vmax))
    plt.colorbar(sm, ax=tube, label=r"$\tau = q/t$ (MPa)", shrink=0.8)
    tube.set(
        aspect="equal",
        xlim=(-112, 112),
        ylim=(-62, 50),
        xlabel="$y$ (mm)",
        ylabel="$z$ (mm)",
        title=rf"Thin-walled tube, $T$ = {TORQUE_TUBE / 1e3:.0f} kN m (Bredt-Batho)",
    )

    for ax in (profile, rect):
        ax.grid(True, lw=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for d_o, d_i, name in (
        (D_SOLID, 0.0, "solid 60 mm"),
        (D_OUTER, D_INNER, "hollow 70/50"),
    ):
        j = polar_moment(d_o, d_i)
        tau = shaft_shear(TORQUE_SHAFT, d_o / 2, d_o, d_i)
        print(
            f"{name}: J = {j * 1e12:.4g} mm^4, tau_max = {tau / 1e6:.2f} MPa, "
            f"area = {np.pi * (d_o**2 - d_i**2) / 4 * 1e6:.0f} mm^2"
        )
    for ratio in (1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0):
        alpha, beta = rectangle_coefficients(ratio)
        print(
            f"a/b = {ratio:4.1f}: alpha = {float(alpha):.4f}, beta = {float(beta):.4f}"
        )
    q, stresses, twist = tube_properties()
    text = ", ".join(f"{k} {v / 1e6:.1f}" for k, v in stresses.items())
    print(f"tube: q = {q:.0f} N/m, tau (MPa): {text}, twist rate = {twist:.3e} rad/m")

    finish_figures(
        {"materials_torsion_shear_distribution.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
