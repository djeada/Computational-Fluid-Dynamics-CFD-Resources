"""Solve a plane pin-jointed truss by the method of joints and by direct stiffness.

The method of joints is written for the whole truss at once: two equilibrium
equations per joint form a square linear system in the member forces and the
support reactions when the truss is statically determinate. The direct
stiffness method assembles the element stiffness matrices of axial bars,
solves for the joint displacements and recovers the member forces from them;
it also handles indeterminate trusses. The script analyses a six-panel Pratt
truss under five bottom-chord loads with both methods, checks the midspan
deflection with the unit-load method, and solves a cross-braced version that
is six times indeterminate.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_PANELS = 6  # number of panels of the Pratt truss
PANEL_WIDTH = 3.0  # m
TRUSS_HEIGHT = 3.0  # m
JOINT_LOAD = 20.0e3  # N, downward at every interior bottom-chord joint
YOUNG_MODULUS = 200.0e9  # Pa, structural steel
MEMBER_AREA = 2.0e-3  # m^2, the same for every member
ZERO_TOL = 1e-6  # N, member forces below this are reported as zero


def pratt_truss(
    n_panels=N_PANELS,
    panel=PANEL_WIDTH,
    height=TRUSS_HEIGHT,
    load=JOINT_LOAD,
    cross_braced=False,
):
    """Return nodes, members, supports and loads of a rectangular Pratt truss.

    Bottom joints are numbered 0..n and top joints n+1..2n+1. The diagonals
    slope down towards midspan, so they are in tension under gravity loads.
    With ``cross_braced=True`` every panel gets the second diagonal as well.
    ``supports`` maps a joint to its restrained directions (x, y): a pin at
    the left end and a roller at the right end.
    """
    n = n_panels
    x = np.arange(n + 1) * panel
    nodes = np.vstack(
        [
            np.column_stack([x, np.zeros(n + 1)]),
            np.column_stack([x, np.full(n + 1, height)]),
        ]
    )

    def top(i):
        return n + 1 + i

    members = []
    members += [(i, i + 1) for i in range(n)]  # bottom chord
    members += [(top(i), top(i + 1)) for i in range(n)]  # top chord
    members += [(i, top(i)) for i in range(n + 1)]  # verticals
    for i in range(n):
        tension_diagonal = (top(i), i + 1) if i < n / 2 else (i, top(i + 1))
        members.append(tension_diagonal)
        if cross_braced:
            other = (i, top(i + 1)) if i < n / 2 else (top(i), i + 1)
            members.append(other)
    members = np.array(members)

    supports = {0: (True, True), n: (False, True)}
    loads = np.zeros_like(nodes)
    loads[1:n, 1] = -load
    return nodes, members, supports, loads


def member_geometry(nodes, members):
    """Return the length and the unit vector (from first to second joint) of each member."""
    delta = nodes[members[:, 1]] - nodes[members[:, 0]]
    length = np.linalg.norm(delta, axis=1)
    return length, delta / length[:, None]


def restrained_dofs(supports):
    """Return the global degree-of-freedom indices (2 * joint + direction) held by supports."""
    dofs = []
    for joint, fixed in sorted(supports.items()):
        dofs += [2 * joint + d for d in range(2) if fixed[d]]
    return np.array(dofs, dtype=int)


def equilibrium_matrix(nodes, members, supports):
    """Assemble the 2j x (m + r) matrix of the joint equilibrium equations.

    Column e holds the unit vectors along member e pointing away from each of
    its joints, so a positive member force is tension. The last r columns put a
    unit reaction on each restrained degree of freedom. The equations read
    ``A @ [N, R] = -P``.
    """
    _, unit = member_geometry(nodes, members)
    dofs = restrained_dofs(supports)
    m, r = len(members), len(dofs)
    matrix = np.zeros((2 * len(nodes), m + r))
    for e, (i, j) in enumerate(members):
        matrix[2 * i : 2 * i + 2, e] = unit[e]
        matrix[2 * j : 2 * j + 2, e] = -unit[e]
    matrix[dofs, m + np.arange(r)] = 1.0
    return matrix


def classify_truss(nodes, members, supports):
    """Return (m + r - 2j, rank deficiency) and a word: determinate, indeterminate or unstable.

    The count m + r - 2j is the degree of indeterminacy when the truss is
    stable. The rank of the equilibrium matrix decides stability: a rank below
    2j means some load cannot be carried (a mechanism or improper supports).
    """
    matrix = equilibrium_matrix(nodes, members, supports)
    rows, cols = matrix.shape
    degree = cols - rows
    deficiency = rows - np.linalg.matrix_rank(matrix)
    if deficiency > 0:
        word = "unstable"
    elif degree == 0:
        word = "determinate"
    else:
        word = "indeterminate"
    return degree, deficiency, word


def method_of_joints(nodes, members, supports, loads):
    """Solve all joint equilibrium equations at once for a determinate truss.

    Returns member forces (N, tension positive) and the reactions on the
    restrained degrees of freedom in the order of ``restrained_dofs``.
    """
    degree, deficiency, word = classify_truss(nodes, members, supports)
    if word != "determinate":
        raise ValueError(
            f"method of joints needs a determinate truss; this one is {word} "
            f"(m + r - 2j = {degree}, rank deficiency {deficiency})"
        )
    matrix = equilibrium_matrix(nodes, members, supports)
    solution = np.linalg.solve(matrix, -loads.ravel())
    m = len(members)
    return solution[:m], solution[m:]


def element_stiffness(unit, length, ea):
    """Return the 4 x 4 global stiffness matrix of an axial bar."""
    cc = np.outer(unit, unit)
    return ea / length * np.block([[cc, -cc], [-cc, cc]])


def direct_stiffness(nodes, members, supports, loads, ea=YOUNG_MODULUS * MEMBER_AREA):
    """Solve K u = P with the support displacements set to zero.

    ``ea`` is the axial rigidity E A in N, a scalar or one value per member.
    Returns joint displacements (j x 2, m), member forces (N, tension
    positive) and reactions in the order of ``restrained_dofs``.
    """
    length, unit = member_geometry(nodes, members)
    ea = np.broadcast_to(np.asarray(ea, dtype=float), (len(members),))
    ndof = 2 * len(nodes)
    stiffness = np.zeros((ndof, ndof))
    for e, (i, j) in enumerate(members):
        dofs = [2 * i, 2 * i + 1, 2 * j, 2 * j + 1]
        stiffness[np.ix_(dofs, dofs)] += element_stiffness(unit[e], length[e], ea[e])

    fixed = restrained_dofs(supports)
    free = np.setdiff1d(np.arange(ndof), fixed)
    load_vector = loads.ravel()
    u = np.zeros(ndof)
    u[free] = np.linalg.solve(stiffness[np.ix_(free, free)], load_vector[free])

    displacement = u.reshape(-1, 2)
    elongation = np.einsum(
        "ek,ek->e", unit, displacement[members[:, 1]] - displacement[members[:, 0]]
    )
    forces = ea / length * elongation
    reactions = (stiffness @ u - load_vector)[fixed]
    return displacement, forces, reactions


def unit_load_deflection(nodes, members, supports, loads, joint, direction, ea):
    """Displacement of one joint by virtual work: delta = sum N n L / (E A).

    N are the member forces under the real loads and n those under a unit
    load at ``joint`` in ``direction`` (0 = x, 1 = y), both from the method of
    joints. Valid for determinate trusses.
    """
    length, _ = member_geometry(nodes, members)
    real, _ = method_of_joints(nodes, members, supports, loads)
    unit_loads = np.zeros_like(loads)
    unit_loads[joint, direction] = 1.0
    virtual, _ = method_of_joints(nodes, members, supports, unit_loads)
    return np.sum(real * virtual * length / ea)


def draw_supports(ax, nodes, supports, size):
    """Draw a triangle for a pin and a triangle on a circle for a roller."""
    for joint, fixed in supports.items():
        x, y = nodes[joint]
        tri = np.array([[x, y], [x - size, y - 1.6 * size], [x + size, y - 1.6 * size]])
        ax.fill(tri[:, 0], tri[:, 1], color="0.55", zorder=1)
        if not fixed[0]:
            ax.add_patch(
                plt.Circle((x, y - 1.6 * size - 0.25 * size), 0.25 * size, color="0.55")
            )


def draw_forces(ax, nodes, members, forces, norm, cmap, label_values=True):
    """Draw members coloured and width-scaled by axial force; zero-force members dashed."""
    peak = np.max(np.abs(forces))
    for e, (i, j) in enumerate(members):
        xy = nodes[[i, j]]
        if abs(forces[e]) < ZERO_TOL * peak + ZERO_TOL:
            ax.plot(xy[:, 0], xy[:, 1], color="0.5", linestyle="--", linewidth=1.2)
            value = "0"
        else:
            ax.plot(
                xy[:, 0],
                xy[:, 1],
                color=cmap(norm(forces[e] / 1e3)),
                linewidth=1.5 + 6.0 * abs(forces[e]) / peak,
                solid_capstyle="round",
            )
            value = f"{forces[e] / 1e3:+.0f}"
        if label_values:
            mid = xy.mean(axis=0)
            ax.text(
                *mid,
                value,
                fontsize=9,
                ha="center",
                va="center",
                bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none"},
                zorder=4,
            )
    ax.plot(nodes[:, 0], nodes[:, 1], "o", color="black", markersize=4, zorder=5)


def make_figure(nodes, members, supports, loads, forces, reactions, disp, braced):
    """Three panels: member forces, deflected shape, indeterminate cross-braced truss."""
    cmap = plt.get_cmap("RdBu_r")
    vmax = max(np.max(np.abs(forces)), np.max(np.abs(braced[2]))) / 1e3
    norm = Normalize(-vmax, vmax)
    span = nodes[:, 0].max()
    height = nodes[:, 1].max()
    size = 0.25

    fig = plt.figure(figsize=(12, 11.5))
    grid = fig.add_gridspec(4, 1, height_ratios=[1, 1, 1, 0.06], hspace=0.45)
    axes = [fig.add_subplot(grid[k]) for k in range(3)]
    ax = axes[0]
    draw_forces(ax, nodes, members, forces, norm, cmap)
    draw_supports(ax, nodes, supports, size)
    for joint in np.flatnonzero(loads[:, 1]):
        x, y = nodes[joint]
        ax.annotate(
            "",
            xy=(x, y - 0.1),
            xytext=(x, y - 1.2),
            arrowprops={"arrowstyle": "<|-", "color": "black", "lw": 1.5},
        )
        ax.text(x, y - 1.35, f"{-loads[joint, 1] / 1e3:.0f} kN", ha="center", va="top")
    for (joint, d), value in zip(
        [(dof // 2, dof % 2) for dof in restrained_dofs(supports)],
        reactions,
        strict=True,
    ):
        if d == 1:
            x, y = nodes[joint]
            ax.annotate(
                "",
                xy=(x - 0.9 if joint == 0 else x + 0.9, y - 0.05),
                xytext=(x - 0.9 if joint == 0 else x + 0.9, y - 1.3),
                arrowprops={"arrowstyle": "-|>", "color": "tab:green", "lw": 2},
            )
            ax.text(
                x - 0.9 if joint == 0 else x + 0.9,
                y - 1.45,
                f"{value / 1e3:.0f} kN",
                ha="center",
                va="top",
                color="tab:green",
            )
    ax.set_title(
        "(a) Member forces (kN) by the method of joints; dashed members carry zero"
    )

    ax = axes[1]
    scale = 0.12 * height / np.max(np.abs(disp))
    for i, j in members:
        ax.plot(*nodes[[i, j]].T, color="0.7", linewidth=1, linestyle="--")
    deformed = nodes + scale * disp
    for e, (i, j) in enumerate(members):
        ax.plot(*deformed[[i, j]].T, color=cmap(norm(forces[e] / 1e3)), linewidth=2)
    vertical = disp[:, 1] * 1e3
    ax.plot(deformed[:, 0], deformed[:, 1], "o", color="black", markersize=4, zorder=5)
    draw_supports(ax, nodes, supports, size)
    mid = np.argmin(np.abs(nodes[: len(nodes) // 2, 0] - span / 2))
    ax.annotate(
        f"midspan {vertical[mid]:.1f} mm",
        xy=deformed[mid],
        xytext=(deformed[mid, 0] + 2.0, deformed[mid, 1] - 1.0),
        arrowprops={"arrowstyle": "->"},
    )
    ax.set_title(
        f"(b) Deflected shape by direct stiffness (grey: undeformed), "
        f"displacements magnified {scale:.0f} times"
    )

    ax = axes[2]
    b_nodes, b_members, b_supports, _ = braced[0]
    draw_forces(ax, b_nodes, b_members, braced[2], norm, cmap, label_values=False)
    draw_supports(ax, b_nodes, b_supports, size)
    ax.set_title("(c) Cross-braced truss, 6 times indeterminate, by direct stiffness")

    for ax in axes:
        ax.set_aspect("equal")
        ax.set_xlim(-1.5, span + 1.5)
        ax.set_ylim(-2.3, height + 0.6)
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(
        sm,
        cax=fig.add_subplot(grid[3]),
        orientation="horizontal",
        label="member force (kN): red tension, blue compression",
    )
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    truss = pratt_truss()
    nodes, members, supports, loads = truss
    ea = YOUNG_MODULUS * MEMBER_AREA
    degree, _, word = classify_truss(*truss[:3])
    print(f"Pratt truss: j = {len(nodes)}, m = {len(members)}, r = 3, {word}")

    forces, reactions = method_of_joints(*truss)
    disp, forces_k, reactions_k = direct_stiffness(*truss, ea=ea)
    print(
        f"reactions (kN): A_x = {reactions[0] / 1e3:.1f}, A_y = {reactions[1] / 1e3:.1f}, "
        f"B_y = {reactions[2] / 1e3:.1f}"
    )
    print(
        f"largest tension {forces.max() / 1e3:.1f} kN, largest compression "
        f"{forces.min() / 1e3:.1f} kN, zero-force members "
        f"{int(np.sum(np.abs(forces) < ZERO_TOL))}"
    )
    print(f"max |N_joints - N_stiffness| = {np.max(np.abs(forces - forces_k)):.2e} N")

    mid = N_PANELS // 2
    delta = unit_load_deflection(*truss, joint=mid, direction=1, ea=ea)
    print(
        f"midspan deflection: stiffness {disp[mid, 1] * 1e3:.3f} mm, "
        f"unit load {delta * 1e3:.3f} mm"
    )

    braced_truss = pratt_truss(cross_braced=True)
    degree_b, _, word_b = classify_truss(*braced_truss[:3])
    disp_b, forces_b, _ = direct_stiffness(*braced_truss, ea=ea)
    print(
        f"cross-braced: m = {len(braced_truss[1])}, {word_b} (degree {degree_b}), "
        f"midspan deflection {disp_b[mid, 1] * 1e3:.3f} mm, "
        f"largest diagonal {np.abs(forces_b[3 * N_PANELS + 1 :]).max() / 1e3:.1f} kN"
    )

    fig = make_figure(
        nodes,
        members,
        supports,
        loads,
        forces,
        reactions,
        disp,
        (braced_truss, disp_b, forces_b),
    )
    finish_figures(
        {"statics_truss_solver.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
