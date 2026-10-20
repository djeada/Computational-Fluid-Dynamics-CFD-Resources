"""Solve statically indeterminate axial bars with two-node finite elements.

A steel-aluminium bar is fixed between two rigid walls, loaded by a point
force at the joint and heated uniformly. The finite element solution is
compared with the hand solution from equilibrium plus compatibility, for the
force alone, the temperature change alone and both together (superposition).
A tapered bar under an end load checks the deformation integral
delta = int N/(E A) dx: with constant-area elements the tip displacement
converges to the closed form at second order.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Two-material bar between rigid walls: (length m, area m^2, E Pa, alpha 1/K)
STEEL = (0.40, 600e-6, 200e9, 12e-6)
ALUMINIUM = (0.30, 900e-6, 70e9, 23e-6)
LOAD_B = 60e3  # force at the joint B, positive towards C (N)
DELTA_T = 30.0  # uniform temperature rise (K)
ELEMENTS_PER_SEGMENT = 8

# Tapered steel bar, fixed at x = 0, end load at x = L
TAPER_LENGTH = 1.0  # (m)
TAPER_W0, TAPER_W1 = 0.060, 0.020  # width at the root and at the tip (m)
TAPER_T = 0.010  # thickness (m)
TAPER_E = 200e9  # (Pa)
TAPER_LOAD = 20e3  # (N)


def build_mesh(segments, per_segment=ELEMENTS_PER_SEGMENT):
    """Return node positions and per-element (EA, alpha) for prismatic segments."""
    x = [0.0]
    ea, alpha = [], []
    for length, area, modulus, expansion in segments:
        start = x[-1]
        x.extend(start + length * np.arange(1, per_segment + 1) / per_segment)
        ea.extend([modulus * area] * per_segment)
        alpha.extend([expansion] * per_segment)
    return np.array(x), np.array(ea), np.array(alpha)


def solve_bar(x, ea, alpha=None, delta_t=0.0, nodal_loads=None, fixed=(0, -1)):
    """Solve K u = f for a bar of two-node elements.

    x are node positions (m), ea the element axial stiffness E A (N), alpha the
    element expansion coefficients (1/K), delta_t a uniform temperature change
    (K), nodal_loads a dict {node index: force (N)} and fixed the indices of
    nodes with u = 0. Returns nodal displacements u (m), element axial forces
    N (N, tension positive) and the reactions at the fixed nodes (N).
    """
    n = len(x)
    length = np.diff(x)
    alpha = np.zeros_like(ea) if alpha is None else alpha
    k = np.zeros((n, n))
    f = np.zeros(n)
    for e, (le, eae, ae) in enumerate(zip(length, ea, alpha)):
        k[e : e + 2, e : e + 2] += eae / le * np.array([[1.0, -1.0], [-1.0, 1.0]])
        f[e : e + 2] += eae * ae * delta_t * np.array([-1.0, 1.0])
    for node, force in (nodal_loads or {}).items():
        f[node] += force
    fixed = sorted({i % n for i in fixed})
    free = [i for i in range(n) if i not in fixed]
    u = np.zeros(n)
    u[free] = np.linalg.solve(k[np.ix_(free, free)], f[free])
    axial = ea * (np.diff(u) / length - alpha * delta_t)
    reactions = k[fixed] @ u - f[fixed]
    return u, axial, reactions


def hand_solution(load=LOAD_B, delta_t=DELTA_T, seg1=STEEL, seg2=ALUMINIUM):
    """Return (N_AB, N_BC, u_B) from equilibrium and compatibility.

    Equilibrium at B gives N_BC = N_AB - P; compatibility requires the total
    elongation sum(N_i L_i/(E_i A_i) + alpha_i dT L_i) to vanish.
    """
    f1 = seg1[0] / (seg1[2] * seg1[1])
    f2 = seg2[0] / (seg2[2] * seg2[1])
    thermal = delta_t * (seg1[3] * seg1[0] + seg2[3] * seg2[0])
    n_ab = (load * f2 - thermal) / (f1 + f2)
    n_bc = n_ab - load
    u_b = n_ab * f1 + seg1[3] * delta_t * seg1[0]
    return n_ab, n_bc, u_b


def taper_exact(
    length=TAPER_LENGTH,
    w0=TAPER_W0,
    w1=TAPER_W1,
    t=TAPER_T,
    modulus=TAPER_E,
    load=TAPER_LOAD,
):
    """Return the exact tip displacement P/E int_0^L dx/A(x) of the tapered bar (m)."""
    return load * length / (modulus * t * (w0 - w1)) * np.log(w0 / w1)


def taper_fem(
    elements,
    length=TAPER_LENGTH,
    w0=TAPER_W0,
    w1=TAPER_W1,
    t=TAPER_T,
    modulus=TAPER_E,
    load=TAPER_LOAD,
):
    """Return the FE tip displacement with the area of each element at its midpoint."""
    x = np.linspace(0.0, length, elements + 1)
    mid = 0.5 * (x[:-1] + x[1:])
    ea = modulus * t * (w0 + (w1 - w0) * mid / length)
    u, _, _ = solve_bar(x, ea, nodal_loads={elements: load}, fixed=(0,))
    return u[-1]


def strain_energy(x, ea, u):
    """Return U = 1/2 u^T K u = sum N^2 L / (2 E A) for a purely mechanical load (J)."""
    length = np.diff(x)
    axial = ea * np.diff(u) / length
    return float(np.sum(axial**2 * length / (2.0 * ea)))


def draw_bar(ax):
    """Sketch the two-material bar between walls."""
    l1, l2 = STEEL[0], ALUMINIUM[0]
    h1, h2 = 0.06, 0.075
    ax.add_patch(Rectangle((0, -h1 / 2), l1, h1, facecolor="0.7", edgecolor="k"))
    ax.add_patch(Rectangle((l1, -h2 / 2), l2, h2, facecolor="#cfe0f0", edgecolor="k"))
    for xw in (0.0, l1 + l2):
        ax.add_patch(
            Rectangle(
                (xw - 0.02 if xw == 0 else xw, -0.07),
                0.02,
                0.14,
                facecolor="none",
                edgecolor="k",
                hatch="////",
            )
        )
    ax.annotate(
        "",
        xy=(l1 + 0.12, 0.055),
        xytext=(l1, 0.055),
        arrowprops={"arrowstyle": "-|>", "color": "tab:red", "lw": 2},
    )
    ax.text(
        l1 + 0.06,
        0.062,
        f"P = {LOAD_B / 1e3:.0f} kN",
        color="tab:red",
        ha="center",
        va="bottom",
        fontsize=10,
    )
    ax.text(
        l1 / 2,
        0,
        f"steel\nA = {STEEL[1] * 1e6:.0f} mm$^2$",
        ha="center",
        va="center",
        fontsize=10,
    )
    ax.text(
        l1 + l2 / 2,
        0,
        f"aluminium\nA = {ALUMINIUM[1] * 1e6:.0f} mm$^2$",
        ha="center",
        va="center",
        fontsize=10,
    )
    for xp, name in ((0, "A"), (l1, "B"), (l1 + l2, "C")):
        ax.text(xp, -0.08, name, ha="center", va="top", fontsize=11)
    ax.text(
        0.35,
        -0.115,
        rf"whole bar heated by $\Delta T$ = {DELTA_T:.0f} K",
        ha="center",
        fontsize=10,
    )
    ax.set(
        xlim=(-0.05, 0.75),
        ylim=(-0.135, 0.095),
        aspect="equal",
        title="Bar fixed between rigid walls",
    )
    ax.set_axis_off()


def make_figure():
    """Draw the bar, its displacement and stress for three load cases, and the taper study."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    sketch, disp, stress, conv = axes.ravel()
    draw_bar(sketch)

    x, ea, alpha = build_mesh([STEEL, ALUMINIUM])
    joint = ELEMENTS_PER_SEGMENT
    area = np.repeat([STEEL[1], ALUMINIUM[1]], ELEMENTS_PER_SEGMENT)
    cases = [
        ("force only", LOAD_B, 0.0, "tab:blue", "--", 3.0),
        ("temperature only", 0.0, DELTA_T, "tab:orange", "-", 1.5),
        ("both", LOAD_B, DELTA_T, "tab:green", "-", 1.5),
    ]
    for name, load, dt, color, style, width in cases:
        u, axial, _ = solve_bar(x, ea, alpha, dt, {joint: load})
        n_ab, n_bc, u_b = hand_solution(load, dt)
        disp.plot(
            x,
            u * 1e3,
            marker="o",
            ms=3,
            ls=style,
            lw=width,
            color=color,
            label=f"{name}, FE",
        )
        disp.plot(STEEL[0], u_b * 1e3, "s", mfc="none", mec="k", ms=9)
        sig = axial / area / 1e6
        stress.step(
            x,
            np.append(sig, sig[-1]),
            where="post",
            color=color,
            lw=2,
            label=f"{name}: {n_ab / STEEL[1] / 1e6:.1f} / {n_bc / ALUMINIUM[1] / 1e6:.1f}"
            " MPa",
        )
    disp.plot([], [], "s", mfc="none", mec="k", label="hand solution $u_B$")
    disp.set(
        xlabel="$x$ (m)",
        ylabel="displacement $u$ (mm)",
        title="Axial displacement (FE nodes and hand solution)",
    )
    disp.legend(fontsize=10)
    stress.axhline(0.0, color="0.4", lw=0.8)
    stress.axvline(STEEL[0], color="0.6", lw=0.8, ls=":")
    stress.set(
        ylim=(-90, 100),
        xlabel="$x$ (m)",
        ylabel=r"axial stress $\sigma = N/A$ (MPa)",
        title="Stress in AB / BC (tension positive)",
    )
    stress.legend(fontsize=10, loc="upper right")

    exact = taper_exact()
    counts = np.array([1, 2, 4, 8, 16, 32, 64])
    errors = np.array([abs(taper_fem(m) - exact) / exact for m in counts])
    conv.loglog(
        counts, errors, "o-", color="tab:purple", lw=2, label="FE, midpoint area"
    )
    conv.loglog(
        counts,
        errors[0] * (counts / counts[0]) ** -2.0,
        "--",
        color="0.4",
        label="slope $-2$",
    )
    conv.set(
        xlabel="number of elements",
        ylabel=r"relative error in tip displacement",
        title=rf"Tapered bar: exact $\delta$ = {exact * 1e3:.4f} mm",
    )
    conv.legend(fontsize=10)
    for ax in (disp, stress, conv):
        ax.grid(True, which="both", lw=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    x, ea, alpha = build_mesh([STEEL, ALUMINIUM])
    for name, load, dt in (
        ("force only", LOAD_B, 0.0),
        ("temperature only", 0.0, DELTA_T),
        ("both", LOAD_B, DELTA_T),
    ):
        u, axial, reactions = solve_bar(x, ea, alpha, dt, {ELEMENTS_PER_SEGMENT: load})
        n_ab, n_bc, u_b = hand_solution(load, dt)
        print(
            f"{name}: N_AB = {axial[0] / 1e3:.3f} kN (hand {n_ab / 1e3:.3f}), "
            f"N_BC = {axial[-1] / 1e3:.3f} kN (hand {n_bc / 1e3:.3f}), "
            f"u_B = {u[ELEMENTS_PER_SEGMENT] * 1e3:.4f} mm (hand {u_b * 1e3:.4f}), "
            f"reactions {reactions[0] / 1e3:.3f}, {reactions[1] / 1e3:.3f} kN"
        )
    u, _, _ = solve_bar(x, ea, alpha, 0.0, {ELEMENTS_PER_SEGMENT: LOAD_B})
    print(
        f"strain energy (force only) = {strain_energy(x, ea, u):.3f} J, "
        f"P u_B / 2 = {0.5 * LOAD_B * u[ELEMENTS_PER_SEGMENT]:.3f} J"
    )
    exact = taper_exact()
    for m in (1, 4, 16, 64):
        print(
            f"tapered bar, {m:2d} elements: tip = {taper_fem(m) * 1e3:.5f} mm "
            f"(exact {exact * 1e3:.5f} mm)"
        )

    finish_figures(
        {"materials_axial_bar_fem.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
