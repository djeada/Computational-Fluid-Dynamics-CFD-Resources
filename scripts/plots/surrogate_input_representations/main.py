"""Show one airfoil in the four input representations used by neural surrogates.

A NACA 2412 section (with the closed-trailing-edge thickness coefficient) is
encoded as (a) a short parameter vector of shape and operating-condition
values normalised to their design ranges, (b) a signed distance field sampled
on a coarse Cartesian grid, the input of a convolutional network, (c) an
unordered point cloud sampled uniformly by arc length on the surface, with
outward normals, the input of a PointNet-type network, and (d) a graded
triangle mesh whose nodes and edges form the graph of a graph neural network,
with nodes coloured by boundary type.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.path import Path as PolygonPath
from scipy.spatial import Delaunay, cKDTree
from skimage.measure import find_contours

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 1
NACA_CODE = "2412"  # 2 % camber at 40 % chord, 12 % thickness
N_SURFACE = 400  # chordwise stations per surface for the exact outline
ALPHA_DEG = 4.0  # angle of attack [deg]
REYNOLDS = 3.0e6  # chord Reynolds number [-]
# design ranges (low, high) used to normalise each parameter to [0, 1]
PARAMETER_RANGES = {
    "camber $m$": (0.0, 0.06),
    "camber position $p$": (0.2, 0.7),
    "thickness $t$": (0.06, 0.20),
    r"$\alpha$ [deg]": (-4.0, 12.0),
    r"$\log_{10} Re$": (6.0, 7.0),
}
GRID_SPACING = 0.025  # SDF grid spacing [chords]
GRID_BOX = (-0.3, 1.3, -0.3, 0.3)  # SDF grid extent [chords]
N_CLOUD = 80  # points in the surface point cloud
H_WALL = 0.012  # mesh spacing on the wall [chords]
SPACING_GROWTH = 0.35  # increase of mesh spacing per chord of wall distance [-]
MESH_DISTANCE = 0.3  # wall distance of the outermost mesh layer [chords]


def naca4(code=NACA_CODE, n=N_SURFACE):
    """Closed counter-clockwise outline (x, y) of a NACA 4-digit airfoil, unit chord."""
    m, p, t = int(code[0]) / 100, int(code[1]) / 10, int(code[2:]) / 100
    beta = np.linspace(0.0, np.pi, n)
    x = 0.5 * (1.0 - np.cos(beta))  # cosine spacing clusters at both edges
    yt = (t / 0.2) * (
        0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1036 * x**4
    )
    if m > 0:
        yc = np.where(
            x < p,
            m / p**2 * (2 * p * x - x**2),
            m / (1 - p) ** 2 * (1 - 2 * p + 2 * p * x - x**2),
        )
        dyc = np.where(x < p, 2 * m / p**2 * (p - x), 2 * m / (1 - p) ** 2 * (p - x))
    else:
        yc, dyc = np.zeros_like(x), np.zeros_like(x)
    theta = np.arctan(dyc)
    upper = np.column_stack([x - yt * np.sin(theta), yc + yt * np.cos(theta)])
    lower = np.column_stack([x + yt * np.sin(theta), yc - yt * np.cos(theta)])
    # trailing edge -> upper surface -> leading edge -> lower surface -> trailing edge
    return np.vstack([upper[::-1], lower[1:]])


def resample(outline, spacing):
    """Points spaced `spacing` apart in arc length along a closed polyline."""
    closed = np.vstack([outline, outline[:1]])
    s = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(closed, axis=0).T))])
    n = max(int(np.ceil(s[-1] / spacing)), 3)
    targets = np.linspace(0.0, s[-1], n, endpoint=False)
    return np.column_stack([np.interp(targets, s, closed[:, k]) for k in range(2)])


def signed_distance(points, outline):
    """Distance to the outline, negative inside the airfoil."""
    dense = resample(outline, 5e-4)
    distance, _ = cKDTree(dense).query(points)
    inside = PolygonPath(outline).contains_points(points)
    return np.where(inside, -distance, distance)


def normalised_parameters(code=NACA_CODE, alpha=ALPHA_DEG, reynolds=REYNOLDS):
    """Raw and [0, 1]-normalised values of the parameter vector."""
    raw = [
        int(code[0]) / 100,
        int(code[1]) / 10,
        int(code[2:]) / 100,
        alpha,
        np.log10(reynolds),
    ]
    ranges = np.array(list(PARAMETER_RANGES.values()))
    return np.array(raw), (np.array(raw) - ranges[:, 0]) / (ranges[:, 1] - ranges[:, 0])


def sdf_grid(outline):
    """Cell-centre coordinates and SDF values on the coarse CNN input grid."""
    x0, x1, y0, y1 = GRID_BOX
    xs = np.arange(x0 + 0.5 * GRID_SPACING, x1, GRID_SPACING)
    ys = np.arange(y0 + 0.5 * GRID_SPACING, y1, GRID_SPACING)
    gx, gy = np.meshgrid(xs, ys)
    phi = signed_distance(np.column_stack([gx.ravel(), gy.ravel()]), outline)
    return xs, ys, phi.reshape(gx.shape)


def point_cloud(outline, n=N_CLOUD, seed=SEED):
    """Random surface points (uniform in arc length) and their outward unit normals."""
    rng = np.random.default_rng(seed)
    closed = np.vstack([outline, outline[:1]])
    seg = np.diff(closed, axis=0)
    s = np.concatenate([[0.0], np.cumsum(np.hypot(*seg.T))])
    targets = rng.uniform(0.0, s[-1], n)
    pts = np.column_stack([np.interp(targets, s, closed[:, k]) for k in range(2)])
    index = np.clip(np.searchsorted(s, targets) - 1, 0, len(seg) - 1)
    tangent = seg[index] / np.hypot(*seg[index].T)[:, None]
    normal = np.column_stack([tangent[:, 1], -tangent[:, 0]])  # outward for CCW outline
    return pts, normal


def mesh_graph(outline):
    """Graded triangle mesh from SDF level sets: nodes, edges and node types.

    Node types: 0 = wall, 1 = fluid, 2 = far-field (outermost layer).
    """
    spacing = lambda d: H_WALL + SPACING_GROWTH * d  # noqa: E731
    wall = resample(outline, H_WALL)
    layers, types = [wall], [np.zeros(len(wall), dtype=int)]

    fine = 0.004
    xs = np.arange(-0.6, 1.6, fine)
    ys = np.arange(-0.6, 0.6, fine)
    gx, gy = np.meshgrid(xs, ys)
    phi = signed_distance(np.column_stack([gx.ravel(), gy.ravel()]), outline)
    phi = phi.reshape(gx.shape)

    d = spacing(0.0)
    while d < MESH_DISTANCE + 1e-9:
        contour = max(find_contours(phi, d), key=len)
        xy = np.column_stack(
            [
                np.interp(contour[:, 1], np.arange(len(xs)), xs),
                np.interp(contour[:, 0], np.arange(len(ys)), ys),
            ]
        )
        layer = resample(xy, spacing(d))
        last = d + spacing(d) > MESH_DISTANCE + 1e-9
        layers.append(layer)
        types.append(np.full(len(layer), 2 if last else 1))
        d += spacing(d)

    nodes = np.vstack(layers)
    node_type = np.concatenate(types)
    triangles = Delaunay(nodes).simplices
    centroids = nodes[triangles].mean(axis=1)
    keep = ~PolygonPath(outline).contains_points(centroids)
    # drop hull triangles that bridge concave parts of the outermost layer
    edge_len = np.max(
        [
            np.hypot(*(nodes[triangles[:, a]] - nodes[triangles[:, b]]).T)
            for a, b in ((0, 1), (1, 2), (2, 0))
        ],
        axis=0,
    )
    keep &= edge_len < 2.0 * spacing(MESH_DISTANCE)
    triangles = triangles[keep]
    pairs = np.vstack(
        [triangles[:, [0, 1]], triangles[:, [1, 2]], triangles[:, [2, 0]]]
    )
    edges = np.unique(np.sort(pairs, axis=1), axis=0)
    return nodes, edges, node_type


def make_figure(outline):
    """Draw the four representations in a 2 x 2 layout."""
    fig, axes = plt.subplots(
        2, 2, figsize=(13, 6.6), layout="constrained", width_ratios=[1, 1.3]
    )

    ax = axes[0, 0]
    raw, normed = normalised_parameters()
    labels = list(PARAMETER_RANGES)
    colors = ["tab:blue"] * 3 + ["tab:orange"] * 2
    bars = ax.barh(labels[::-1], normed[::-1], color=colors[::-1])
    for bar, value in zip(bars, raw[::-1], strict=True):
        ax.text(
            bar.get_width() + 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.3g}",
            va="center",
            fontsize=10,
        )
    ax.set_xlim(0, 1.15)
    ax.set_xlabel("value normalised to its design range [-]", fontsize=10)
    ax.set_title(
        f"(a) parameter vector: NACA {NACA_CODE} shape (blue) + operating point (orange)",
        fontsize=10,
    )
    ax.tick_params(labelsize=10)

    ax = axes[0, 1]
    xs, ys, phi = sdf_grid(outline)
    lim = np.abs(phi).max()
    extent = (
        xs[0] - GRID_SPACING / 2,
        xs[-1] + GRID_SPACING / 2,
        ys[0] - GRID_SPACING / 2,
        ys[-1] + GRID_SPACING / 2,
    )
    im = ax.imshow(
        phi,
        origin="lower",
        extent=extent,
        cmap="RdBu_r",
        vmin=-lim,
        vmax=lim,
        interpolation="nearest",
    )
    ax.contour(xs, ys, phi, levels=[0.0], colors="black", linewidths=1.2)
    ax.plot(*np.vstack([outline, outline[:1]]).T, "--", color="tab:green", linewidth=1)
    fig.colorbar(im, ax=ax, label=r"signed distance $\phi$ [chords]", shrink=0.8)
    ax.set_title(
        f"(b) signed distance field on a {phi.shape[1]} x {phi.shape[0]} grid (CNN input)",
        fontsize=10,
    )

    ax = axes[1, 0]
    pts, normal = point_cloud(outline)
    ax.plot(*np.vstack([outline, outline[:1]]).T, color="0.75", linewidth=1)
    ax.quiver(
        *pts.T,
        *normal.T,
        color="tab:gray",
        angles="xy",
        scale_units="xy",
        scale=15,
        width=0.003,
    )
    ax.scatter(*pts.T, s=16, color="tab:blue", zorder=3)
    ax.set_title(
        f"(c) unordered point cloud: {N_CLOUD} surface points with normals", fontsize=10
    )

    ax = axes[1, 1]
    nodes, edges, node_type = mesh_graph(outline)
    ax.add_collection(LineCollection(nodes[edges], colors="0.6", linewidths=0.4))
    names = ("wall", "fluid", "far field")
    for kind, (name, color) in enumerate(
        zip(names, ("tab:red", "tab:blue", "tab:orange"), strict=True)
    ):
        sel = node_type == kind
        ax.scatter(
            *nodes[sel].T, s=5, color=color, label=f"{name} ({sel.sum()})", zorder=3
        )
    ax.legend(
        fontsize=9,
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        markerscale=2.5,
        title="node type",
        title_fontsize=9,
    )
    ax.set_title(
        f"(d) mesh graph: {len(nodes)} nodes, {len(edges)} edges (GNN input)",
        fontsize=10,
    )

    for ax in (axes[0, 1], axes[1, 0], axes[1, 1]):
        ax.set_aspect("equal")
        ax.set_xlabel("$x/c$", fontsize=10)
        ax.set_ylabel("$y/c$", fontsize=10)
    axes[1, 0].set_xlim(-0.1, 1.1)
    axes[1, 0].set_ylim(-0.25, 0.25)
    axes[1, 1].set_xlim(-0.35, 1.35)
    axes[1, 1].set_ylim(-0.4, 0.4)
    fig.suptitle(
        f"One airfoil (NACA {NACA_CODE}), four surrogate input representations",
        fontsize=13,
    )
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    outline = naca4()
    fig = make_figure(outline)
    finish_figures(
        {"surrogate_input_representations.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
