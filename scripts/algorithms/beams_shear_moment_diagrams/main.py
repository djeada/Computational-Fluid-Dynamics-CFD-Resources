"""Load, shear, moment and deflection diagrams of beams from a finite-element solver.

The beam is discretised with two-node Euler-Bernoulli (Hermite cubic) elements,
which handle statically determinate and indeterminate supports alike. The
support reactions come from the solved system; the shear force and bending
moment are then evaluated exactly from the applied loads and the reactions
with singularity functions (Macaulay brackets). Two cases are drawn: an
overhanging beam with a partial uniform load, a couple and an end load, and a
propped cantilever under a uniform load (one redundant reaction).

Sign convention: loads positive downward, applied couples positive clockwise,
deflection v positive upward, V(x) = sum of upward forces left of the section,
M(x) positive when sagging, so that dV/dx = -w, dM/dx = V and EI v'' = M.
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

KN = 1.0e3  # N per kN
E_STEEL = 200.0e9  # Young's modulus (Pa)
I_SECTION = 8.0e-5  # second moment of area (m^4), 8.0e7 mm^4
EI_DEFAULT = E_STEEL * I_SECTION  # flexural rigidity (N m^2)
N_ELEMENTS = 240  # elements of the base mesh (key points are added to it)


@dataclass
class Beam:
    """A straight beam on 0 <= x <= length.

    supports: list of (x, kind) with kind "pin", "roller" or "fixed".
    point_loads: list of (x, P), P in N, positive downward.
    couples: list of (x, C), C in N m, positive clockwise.
    distributed: list of (x1, x2, w1, w2), linearly varying load in N/m,
    positive downward, from w1 at x1 to w2 at x2.
    """

    length: float  # m
    ei: float = EI_DEFAULT  # N m^2
    supports: list = field(default_factory=list)
    point_loads: list = field(default_factory=list)
    couples: list = field(default_factory=list)
    distributed: list = field(default_factory=list)

    def key_points(self):
        """Positions where a support or a load starts, ends or acts."""
        points = {0.0, self.length}
        points.update(x for x, _ in self.supports)
        points.update(x for x, _ in self.point_loads)
        points.update(x for x, _ in self.couples)
        for x1, x2, _, _ in self.distributed:
            points.update((x1, x2))
        return np.array(sorted(points))


@dataclass
class Reaction:
    """Support reaction: force in N (positive up), couple in N m (positive clockwise)."""

    x: float
    force: float
    couple: float = 0.0


def element_stiffness(ei, h):
    """Stiffness matrix of a Hermite beam element, DOFs (v1, theta1, v2, theta2)."""
    return (ei / h**3) * np.array(
        [
            [12.0, 6 * h, -12.0, 6 * h],
            [6 * h, 4 * h**2, -6 * h, 2 * h**2],
            [-12.0, -6 * h, 12.0, -6 * h],
            [6 * h, 2 * h**2, -6 * h, 4 * h**2],
        ]
    )


def hermite_shapes(xi, h):
    """Hermite cubic shape functions on an element of length h, xi in [0, 1]."""
    return np.array(
        [
            1 - 3 * xi**2 + 2 * xi**3,
            h * (xi - 2 * xi**2 + xi**3),
            3 * xi**2 - 2 * xi**3,
            h * (-(xi**2) + xi**3),
        ]
    )


def load_intensity(beam, x):
    """Distributed load w(x) in N/m (positive downward); right-continuous at ends."""
    x = np.asarray(x, dtype=float)
    w = np.zeros_like(x)
    for x1, x2, w1, w2 in beam.distributed:
        inside = (x >= x1) & (x < x2)
        w[inside] += w1 + (w2 - w1) * (x[inside] - x1) / (x2 - x1)
    return w


def build_mesh(beam, n_elements=N_ELEMENTS):
    """Uniform nodes plus every key point, so loads and supports sit on nodes."""
    nodes = np.union1d(np.linspace(0.0, beam.length, n_elements + 1), beam.key_points())
    keep = np.concatenate(([True], np.diff(nodes) > 1e-9 * beam.length))
    return nodes[keep]


def node_index(nodes, x):
    """Index of the node at position x."""
    i = int(np.argmin(np.abs(nodes - x)))
    if abs(nodes[i] - x) > 1e-9 * max(1.0, nodes[-1]):
        raise ValueError(f"no node at x = {x}")
    return i


def assemble(beam, nodes):
    """Global stiffness matrix and consistent load vector (upward force, ccw moment)."""
    n_dof = 2 * len(nodes)
    k = np.zeros((n_dof, n_dof))
    f = np.zeros(n_dof)
    gauss_xi = 0.5 * (1 + np.array([-np.sqrt(3 / 5), 0.0, np.sqrt(3 / 5)]))
    gauss_wt = 0.5 * np.array([5 / 9, 8 / 9, 5 / 9])
    for e in range(len(nodes) - 1):
        h = nodes[e + 1] - nodes[e]
        dofs = slice(2 * e, 2 * e + 4)
        k[dofs, dofs] += element_stiffness(beam.ei, h)
        # Three-point Gauss is exact for a cubic shape function times a linear load.
        w = load_intensity(beam, nodes[e] + gauss_xi * h)
        f[dofs] -= h * hermite_shapes(gauss_xi, h) @ (gauss_wt * w)
    for x, p in beam.point_loads:
        f[2 * node_index(nodes, x)] -= p
    for x, c in beam.couples:
        f[2 * node_index(nodes, x) + 1] -= c  # clockwise couple = negative ccw moment
    return k, f


def constrained_dofs(beam, nodes):
    """Degrees of freedom fixed to zero by the supports."""
    fixed = []
    for x, kind in beam.supports:
        i = node_index(nodes, x)
        if kind in ("pin", "roller"):
            fixed.append(2 * i)
        elif kind == "fixed":
            fixed.extend((2 * i, 2 * i + 1))
        else:
            raise ValueError(f"unknown support kind {kind!r}")
    return np.array(fixed, dtype=int)


def solve_beam(beam, n_elements=N_ELEMENTS):
    """Solve K u = f with the support constraints.

    Returns (nodes, deflection v in m, rotation theta in rad, reactions).
    """
    nodes = build_mesh(beam, n_elements)
    k, f = assemble(beam, nodes)
    fixed = constrained_dofs(beam, nodes)
    free = np.setdiff1d(np.arange(len(f)), fixed)
    u = np.zeros_like(f)
    u[free] = np.linalg.solve(k[np.ix_(free, free)], f[free])
    residual = k @ u - f  # reaction forces (up) and ccw reaction moments
    reactions = []
    for x, kind in beam.supports:
        i = node_index(nodes, x)
        couple = -residual[2 * i + 1] if kind == "fixed" else 0.0
        reactions.append(Reaction(x, residual[2 * i], couple))
    return nodes, u[0::2], u[1::2], reactions


def macaulay(x, a, n):
    """Singularity function <x - a>^n, equal to 1 for x >= a when n = 0."""
    s = np.asarray(x, dtype=float) - a
    if n == 0:
        return (s >= 0).astype(float)
    return np.where(s > 0, s, 0.0) ** n


def internal_forces(beam, reactions, x):
    """Shear V(x) in N and moment M(x) in N m from singularity functions."""
    v = np.zeros_like(np.asarray(x, dtype=float))
    m = np.zeros_like(v)
    forces = [(r.x, r.force) for r in reactions] + [
        (a, -p) for a, p in beam.point_loads
    ]
    for a, force in forces:
        v += force * macaulay(x, a, 0)
        m += force * macaulay(x, a, 1)
    couples = [(r.x, r.couple) for r in reactions] + list(beam.couples)
    for a, c in couples:
        m += c * macaulay(x, a, 0)
    for x1, x2, w1, w2 in beam.distributed:
        s = (w2 - w1) / (x2 - x1)  # load slope (N/m^2)
        v -= w1 * macaulay(x, x1, 1) + s / 2 * macaulay(x, x1, 2)
        v += w2 * macaulay(x, x2, 1) + s / 2 * macaulay(x, x2, 2)
        m -= w1 / 2 * macaulay(x, x1, 2) + s / 6 * macaulay(x, x1, 3)
        m += w2 / 2 * macaulay(x, x2, 2) + s / 6 * macaulay(x, x2, 3)
    return v, m


def evaluation_points(beam, n=1200):
    """Fine grid with a point just left of every key point, to draw the jumps."""
    keys = beam.key_points()
    left = np.nextafter(keys[1:], -np.inf)
    return np.union1d(np.linspace(0.0, beam.length, n), np.concatenate((keys, left)))


def equilibrium_residual(beam, reactions):
    """Net upward force (N) and net ccw moment about x = 0 (N m); both should vanish."""
    force = sum(r.force for r in reactions) - sum(p for _, p in beam.point_loads)
    moment = sum(r.force * r.x - r.couple for r in reactions)
    moment -= sum(p * a for a, p in beam.point_loads) + sum(c for _, c in beam.couples)
    for x1, x2, w1, w2 in beam.distributed:
        total = 0.5 * (w1 + w2) * (x2 - x1)
        centroid = x1 + (x2 - x1) * (w1 + 2 * w2) / (3 * (w1 + w2))
        force -= total
        moment -= total * centroid
    return force, moment


def overhanging_beam():
    """Pin at A (0), roller at B (6 m), overhang to C (8 m); determinate."""
    return Beam(
        length=8.0,
        supports=[(0.0, "pin"), (6.0, "roller")],
        distributed=[(0.0, 3.0, 10 * KN, 10 * KN)],
        couples=[(4.5, 9 * KN)],
        point_loads=[(8.0, 15 * KN)],
    )


def propped_cantilever():
    """Fixed at A (0), roller at B (6 m), uniform 10 kN/m; one redundant."""
    return Beam(
        length=6.0,
        supports=[(0.0, "fixed"), (6.0, "roller")],
        distributed=[(0.0, 6.0, 10 * KN, 10 * KN)],
    )


def draw_support(ax, x, kind, size):
    """Draw a pin (triangle), roller (triangle on a line) or fixed wall."""
    if kind == "fixed":
        side = -1 if x == 0 else 1
        ax.plot([x, x], [-1.6 * size, 1.6 * size], color="k", linewidth=2.5)
        for y in np.linspace(-1.5 * size, 1.5 * size, 7):
            ax.plot([x, x + side * 0.5 * size], [y, y - 0.5 * size], color="k", lw=1)
        return
    tri = Polygon(
        [[x, 0], [x - 0.6 * size, -1.1 * size], [x + 0.6 * size, -1.1 * size]],
        closed=True,
        facecolor="0.8",
        edgecolor="k",
    )
    ax.add_patch(tri)
    if kind == "roller":
        ax.plot([x - 0.8 * size] * 2, [0, 0], color="k")
        ax.plot([x - 0.8 * size, x + 0.8 * size], [-1.45 * size] * 2, color="k")
        for dx in (-0.3, 0.3):
            ax.add_patch(
                plt.Circle((x + dx * size, -1.27 * size), 0.17 * size, fc="w", ec="k")
            )


def draw_loads(ax, beam, reactions):
    """Schematic of the beam, supports, loads and computed reactions."""
    size = 0.06 * beam.length
    ax.plot([0, beam.length], [0, 0], color="k", linewidth=4, solid_capstyle="butt")
    for x, kind in beam.supports:
        draw_support(ax, x, kind, size)
    for x1, x2, w1, w2 in beam.distributed:
        xs = np.linspace(x1, x2, max(4, int(12 * (x2 - x1) / beam.length) + 2))
        top = 0.6 * size + 1.6 * size * (w1 + (w2 - w1) * (xs - x1) / (x2 - x1)) / max(
            w1, w2
        )
        ax.fill_between(xs, 0.15 * size, top, color="tab:blue", alpha=0.15)
        for xi, ti in zip(xs, top, strict=True):
            ax.annotate(
                "",
                (xi, 0.15 * size),
                (xi, ti),
                arrowprops={"arrowstyle": "->", "color": "tab:blue"},
            )
        ax.text(
            0.5 * (x1 + x2),
            top.max() + 0.25 * size,
            f"w = {w1 / KN:g} kN/m",
            ha="center",
            va="bottom",
            color="tab:blue",
            fontsize=10,
        )
    for x, p in beam.point_loads:
        ax.annotate(
            "",
            (x, 0.15 * size),
            (x, 3.0 * size),
            arrowprops={"arrowstyle": "-|>", "color": "tab:red", "lw": 2},
        )
        ax.text(
            x,
            3.15 * size,
            f"P = {p / KN:g} kN",
            ha="center",
            va="bottom",
            color="tab:red",
            fontsize=10,
        )
    for x, c in beam.couples:
        arc = FancyArrowPatch(
            (x - 0.7 * size, 0.3 * size),
            (x + 0.7 * size, 0.3 * size),
            connectionstyle="arc3,rad=-0.9",
            arrowstyle="-|>",
            mutation_scale=14,
            color="tab:purple",
            lw=1.8,
        )
        ax.add_patch(arc)
        ax.text(
            x,
            1.6 * size,
            f"C = {c / KN:g} kN m",
            ha="center",
            va="bottom",
            color="tab:purple",
            fontsize=10,
        )
    for r in reactions:
        ax.annotate(
            "",
            (r.x, -1.7 * size),
            (r.x, -4.0 * size),
            arrowprops={"arrowstyle": "-|>", "color": "tab:green", "lw": 2},
        )
        label = f"{r.force / KN:.2f} kN"
        if r.couple:
            sense = "cw" if r.couple > 0 else "ccw"
            label += f"\n{abs(r.couple) / KN:.2f} kN m ({sense})"
        dx = 0.02 * beam.length if r.x < beam.length else -0.02 * beam.length
        ax.text(
            r.x + dx,
            -3.6 * size,
            label,
            ha="left" if dx > 0 else "right",
            va="center",
            color="tab:green",
            fontsize=10,
        )
    ax.set(
        xlim=(-0.05 * beam.length, 1.05 * beam.length), ylim=(-4.4 * size, 5.0 * size)
    )
    ax.set_yticks([])
    for spine in ("left", "right", "top"):
        ax.spines[spine].set_visible(False)


def annotate_extreme(ax, x, y, fmt, which="max"):
    """Mark the maximum or minimum of y on ax."""
    rounded = np.round(y, 6)  # so the first point of a flat extreme is chosen
    i = int(np.argmax(rounded) if which == "max" else np.argmin(rounded))
    ax.plot(x[i], y[i], "o", color="k", markersize=5)
    offset = 12 if which == "max" else -16
    right_end = x[i] > x[0] + 0.7 * (x[-1] - x[0])
    ax.annotate(
        fmt.format(y[i], x[i]),
        (x[i], y[i]),
        textcoords="offset points",
        xytext=(-6 if right_end else 6, offset),
        ha="right" if right_end else "left",
        fontsize=10,
        va="center",
    )


def draw_case(axes, beam, title):
    """Fill one column of panels (load, V, M, v) for a beam and return the results."""
    nodes, v_def, _, reactions = solve_beam(beam)
    x = evaluation_points(beam)
    shear, moment = internal_forces(beam, reactions, x)
    draw_loads(axes[0], beam, reactions)
    axes[0].set_title(title)

    axes[1].fill_between(x, shear / KN, color="tab:blue", alpha=0.25, lw=0)
    axes[1].plot(x, shear / KN, color="tab:blue")
    axes[1].set(ylabel="V (kN)", title="Shear force")
    annotate_extreme(axes[1], x, shear / KN, "{:.2f} kN", "max")
    annotate_extreme(axes[1], x, shear / KN, "{:.2f} kN", "min")

    axes[2].fill_between(x, moment / KN, color="tab:orange", alpha=0.25, lw=0)
    axes[2].plot(x, moment / KN, color="tab:orange")
    axes[2].set(ylabel="M (kN m)", title="Bending moment (sagging positive)")
    annotate_extreme(axes[2], x, moment / KN, "{:.2f} kN m at x = {:.2f} m", "max")
    annotate_extreme(axes[2], x, moment / KN, "{:.2f} kN m at x = {:.2f} m", "min")

    axes[3].plot(nodes, v_def * 1e3, color="tab:green")
    axes[3].set(
        ylabel="v (mm)",
        xlabel="x (m)",
        title=f"Deflection, EI = {beam.ei / 1e6:.0f} MN m$^2$",
    )
    annotate_extreme(axes[3], nodes, v_def * 1e3, "{:.2f} mm at x = {:.2f} m", "min")
    if v_def.max() > 1e-6:
        annotate_extreme(
            axes[3], nodes, v_def * 1e3, "{:.2f} mm at x = {:.2f} m", "max"
        )
    for ax in axes[1:]:
        ax.axhline(0, color="0.3", lw=0.8)
        ax.grid(True, lw=0.5, alpha=0.5)
        ax.margins(y=0.3)
    return nodes, v_def, reactions, x, shear, moment


def report(name, beam, nodes, v_def, reactions, x, shear, moment):
    """Print reactions, extreme values and the equilibrium check."""
    print(name)
    for r in reactions:
        extra = f", couple {r.couple / KN:+.3f} kN m (+ = cw)" if r.couple else ""
        print(f"  reaction at x = {r.x:.2f} m: {r.force / KN:+.3f} kN{extra}")
    i_max, i_min = np.argmax(moment), np.argmin(moment)
    print(f"  M_max = {moment[i_max] / KN:+.3f} kN m at x = {x[i_max]:.3f} m")
    print(f"  M_min = {moment[i_min] / KN:+.3f} kN m at x = {x[i_min]:.3f} m")
    print(f"  |V|_max = {np.abs(shear).max() / KN:.3f} kN")
    j = np.argmax(np.abs(v_def))
    print(f"  extreme deflection {v_def[j] * 1e3:+.3f} mm at x = {nodes[j]:.3f} m")
    force, mom = equilibrium_residual(beam, reactions)
    print(f"  equilibrium residuals: {force:.2e} N, {mom:.2e} N m")


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    cases = [
        ("Overhanging beam (statically determinate)", overhanging_beam()),
        ("Propped cantilever (one redundant)", propped_cantilever()),
    ]
    fig, axes = plt.subplots(
        4, 2, figsize=(13, 12), gridspec_kw={"height_ratios": [1.15, 1, 1, 1]}
    )
    for col, (title, beam) in enumerate(cases):
        results = draw_case(axes[:, col], beam, title)
        report(title, beam, *results)
        for ax in axes[1:, col]:
            ax.sharex(axes[0, col])
    fig.tight_layout()

    finish_figures(
        {"beams_shear_moment_diagrams.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
