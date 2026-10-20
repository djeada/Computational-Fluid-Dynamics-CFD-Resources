"""Show how far information travels through message passing on a CFD mesh graph.

A graded unstructured triangle mesh is built around a circular cylinder by
placing nodes on concentric rings whose spacing grows away from the wall,
filling the rest of the box with a jittered grid, and triangulating with
scipy's Delaunay routine. The mesh edges form the graph of a graph neural
network. The first figure colours the nodes by hop distance from one wake
node and shows the receptive field after 1, 2, 4 and 8 message-passing steps.
The second figure runs a linear message-passing update whose messages are
cotangent-weighted differences between neighbours. That update is the
vertex-centred finite-volume discretisation of the diffusion equation, so a
Gaussian blob spreads at the analytical rate while the integral of the field
is conserved to round-off.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import BoundaryNorm
from scipy import sparse
from scipy.spatial import Delaunay

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 3
RADIUS = 0.5  # cylinder radius [m]
BOX = (-2.5, 6.0, -2.5, 2.5)  # x_min, x_max, y_min, y_max [m]
H_WALL = 0.04  # node spacing on the cylinder wall [m]
SPACING_GROWTH = 0.15  # increase of spacing per metre of wall distance [-]
H_FAR = 0.25  # node spacing far from the cylinder [m]
JITTER = 0.25  # random shift of far-field nodes, as a fraction of H_FAR
SOURCE_POINT = (0.62, 0.0)  # node whose receptive field is shown [m]
HOP_STEPS = (1, 2, 4, 8)  # message-passing steps shown in the first figure
ZOOM = (-1.2, 2.2, -1.25, 1.25)  # view window for the receptive-field panels [m]

KAPPA = 1.0  # diffusivity [m^2/s]
BLOB_CENTRE = (1.0, 0.45)  # centre of the initial Gaussian [m]
BLOB_SIGMA = 0.1  # standard deviation of the initial Gaussian [m]
SNAPSHOT_TIMES = (0.0, 0.02, 0.1)  # times of the field panels [s]
WEIGHT_FLOOR = 1e-12  # cotangent weights below this are treated as zero [-]
DT_SAFETY = 0.9  # fraction of the positivity-preserving explicit time step


def spacing(wall_distance):
    """Target node spacing as a function of distance from the cylinder wall."""
    return np.minimum(H_WALL + SPACING_GROWTH * wall_distance, H_FAR)


def cylinder_mesh(seed=SEED):
    """Return node coordinates and triangles of a graded mesh around the cylinder."""
    rng = np.random.default_rng(seed)
    points = []
    radius, ring = RADIUS, 0
    while spacing(radius - RADIUS) < H_FAR:
        h = spacing(radius - RADIUS)
        n_theta = int(np.ceil(2.0 * np.pi * radius / h))
        theta = 2.0 * np.pi * (np.arange(n_theta) + 0.5 * (ring % 2)) / n_theta
        points.append(np.column_stack([radius * np.cos(theta), radius * np.sin(theta)]))
        radius += h
        ring += 1
    ring_edge = radius

    x_min, x_max, y_min, y_max = BOX
    xs = np.linspace(x_min, x_max, int(round((x_max - x_min) / H_FAR)) + 1)
    ys = np.linspace(y_min, y_max, int(round((y_max - y_min) / H_FAR)) + 1)
    gx, gy = np.meshgrid(xs, ys)
    grid = np.column_stack([gx.ravel(), gy.ravel()])
    on_box = (
        np.isclose(grid[:, 0], x_min)
        | np.isclose(grid[:, 0], x_max)
        | np.isclose(grid[:, 1], y_min)
        | np.isclose(grid[:, 1], y_max)
    )
    shift = JITTER * H_FAR * rng.uniform(-1.0, 1.0, size=grid.shape)
    grid = grid + np.where(on_box[:, None], 0.0, shift)
    keep = np.hypot(grid[:, 0], grid[:, 1]) > ring_edge + 0.3 * H_FAR
    points.append(grid[keep])

    points = np.vstack(points)
    triangles = Delaunay(points).simplices
    centroids = points[triangles].mean(axis=1)
    triangles = triangles[np.hypot(centroids[:, 0], centroids[:, 1]) > RADIUS]
    return points, triangles


def unique_edges(triangles):
    """Return the undirected edges of a triangulation as sorted index pairs."""
    pairs = np.vstack(
        [triangles[:, [0, 1]], triangles[:, [1, 2]], triangles[:, [2, 0]]]
    )
    return np.unique(np.sort(pairs, axis=1), axis=0)


def adjacency(n_nodes, edges):
    """Symmetric CSR adjacency matrix of an undirected edge list."""
    data = np.ones(2 * len(edges))
    rows = np.concatenate([edges[:, 0], edges[:, 1]])
    cols = np.concatenate([edges[:, 1], edges[:, 0]])
    return sparse.csr_matrix((data, (rows, cols)), shape=(n_nodes, n_nodes))


def hop_distances(n_nodes, edges, source):
    """Breadth-first search: number of edges from `source` to each node (-1 if unreachable)."""
    graph = adjacency(n_nodes, edges)
    hops = np.full(n_nodes, -1, dtype=int)
    hops[source] = 0
    frontier = np.array([source])
    level = 0
    while frontier.size:
        level += 1
        neighbours = np.unique(graph[frontier].indices)
        frontier = neighbours[hops[neighbours] < 0]
        hops[frontier] = level
    return hops


def cotangent_weights(points, triangles):
    """Edge list and cotangent weights w_uv = (cot a + cot b) / 2 of the P1 Laplacian.

    For a piecewise-linear field, w_uv * (h_u - h_v) is the diffusive flux
    from u to v through the median-dual face that crosses the edge, so the
    weights define a vertex-centred finite-volume scheme. Weights below
    WEIGHT_FLOOR (round-off around zero where four nodes are cocircular, or
    negative for obtuse boundary angles) are set to zero.
    """
    pairs, weights = [], []
    for k in range(3):
        i, j, o = triangles[:, k], triangles[:, (k + 1) % 3], triangles[:, (k + 2) % 3]
        a = points[i] - points[o]
        b = points[j] - points[o]
        cross = np.abs(a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0])
        cot = np.einsum("ij,ij->i", a, b) / cross
        pairs.append(np.sort(np.column_stack([i, j]), axis=1))
        weights.append(0.5 * cot)
    pairs = np.vstack(pairs)
    weights = np.concatenate(weights)
    edges, inverse = np.unique(pairs, axis=0, return_inverse=True)
    summed = np.bincount(inverse.ravel(), weights=weights, minlength=len(edges))
    return edges, np.where(summed > WEIGHT_FLOOR, summed, 0.0)


def lumped_areas(points, triangles):
    """Control-volume area of each node: one third of the adjacent triangle areas."""
    p0, p1, p2 = (points[triangles[:, k]] for k in range(3))
    area = 0.5 * np.abs(
        (p1[:, 0] - p0[:, 0]) * (p2[:, 1] - p0[:, 1])
        - (p1[:, 1] - p0[:, 1]) * (p2[:, 0] - p0[:, 0])
    )
    nodal = np.zeros(len(points))
    for k in range(3):
        np.add.at(nodal, triangles[:, k], area / 3.0)
    return nodal


def stable_time_step(edges, weights, areas, kappa=KAPPA):
    """Largest explicit step that keeps every update a convex combination."""
    degree = np.bincount(
        edges.ravel(), weights=np.repeat(weights, 2), minlength=len(areas)
    )
    return float(np.min(areas / (kappa * np.maximum(degree, 1e-300))))


def message_passing_step(h, edges, weights, areas, dt, kappa=KAPPA):
    """One linear message-passing update that discretises dh/dt = kappa * laplacian(h).

    Each directed edge u -> v carries the message w_uv (h_u - h_v), messages
    are summed at the receiving node, and the node update adds
    dt * kappa / A_v times the aggregate to h_v.
    """
    u, v = edges[:, 0], edges[:, 1]
    flux = weights * (h[u] - h[v])  # message from u to v; v -> u carries -flux
    aggregate = np.bincount(v, weights=flux, minlength=len(h))
    aggregate -= np.bincount(u, weights=flux, minlength=len(h))
    return h + dt * kappa * aggregate / areas


def gaussian(points, centre, sigma):
    """Normalised 2D Gaussian with standard deviation `sigma` at each point."""
    r2 = (points[:, 0] - centre[0]) ** 2 + (points[:, 1] - centre[1]) ** 2
    return np.exp(-0.5 * r2 / sigma**2) / (2.0 * np.pi * sigma**2)


def spread_variance(points, h, areas):
    """Per-direction variance of the field about its centroid, sigma^2."""
    mass = np.sum(areas * h)
    centre = (areas * h) @ points / mass
    r2 = np.sum((points - centre) ** 2, axis=1)
    return 0.5 * np.sum(areas * h * r2) / mass


def run_diffusion(points, triangles, times=SNAPSHOT_TIMES):
    """March the message-passing diffusion and record snapshots and diagnostics."""
    edges, weights = cotangent_weights(points, triangles)
    areas = lumped_areas(points, triangles)
    dt = DT_SAFETY * stable_time_step(edges, weights, areas)
    h = gaussian(points, BLOB_CENTRE, BLOB_SIGMA)
    t, snapshots = 0.0, {}
    history = {"t": [0.0], "variance": [spread_variance(points, h, areas)]}
    mass0 = np.sum(areas * h)
    for target in times:
        while t < target - 1e-12:
            step = min(dt, target - t)
            h = message_passing_step(h, edges, weights, areas, step)
            t += step
            history["t"].append(t)
            history["variance"].append(spread_variance(points, h, areas))
        snapshots[target] = h.copy()
    drift = abs(np.sum(areas * h) - mass0) / mass0
    return snapshots, history, dt, drift


def draw_edges(ax, points, edges, color="0.8", width=0.3):
    """Draw every mesh edge as a thin line."""
    ax.add_collection(LineCollection(points[edges], colors=color, linewidths=width))


def style_axes(ax, window):
    """Equal-aspect axes limited to `window` with the cylinder drawn in grey."""
    ax.add_patch(plt.Circle((0.0, 0.0), RADIUS, color="0.35", zorder=3))
    ax.set_xlim(window[0], window[1])
    ax.set_ylim(window[2], window[3])
    ax.set_aspect("equal")
    ax.set_xlabel("$x$ [m]", fontsize=10)
    ax.set_ylabel("$y$ [m]", fontsize=10)


def receptive_field_figure(points, edges, hops, source):
    """Panels of the k-hop neighbourhood, a full-domain hop map and the reach curve."""
    n_nodes = len(points)
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.6), layout="constrained")
    cmap = plt.get_cmap("viridis", max(HOP_STEPS) + 1)
    norm = BoundaryNorm(np.arange(-0.5, max(HOP_STEPS) + 1.5), cmap.N)
    for ax, k in zip(axes.flat[:4], HOP_STEPS, strict=True):
        draw_edges(ax, points, edges)
        reached = (hops >= 0) & (hops <= k)
        ax.scatter(*points[~reached].T, s=2, color="0.7", zorder=1)
        sc = ax.scatter(
            *points[reached].T, s=14, c=hops[reached], cmap=cmap, norm=norm, zorder=2
        )
        ax.scatter(*points[source], s=70, marker="*", color="tab:red", zorder=4)
        style_axes(ax, ZOOM)
        ax.set_title(
            f"after {k} step{'s' if k > 1 else ''}: {reached.sum()} of {n_nodes} "
            f"nodes ({100 * reached.mean():.1f} %)",
            fontsize=10,
        )
    fig.colorbar(
        sc,
        ax=axes[0, :],
        label="hop distance from source",
        ticks=range(max(HOP_STEPS) + 1),
        shrink=0.9,
    )

    ax = axes[1, 1]
    diameter = hops.max()
    sc = ax.tripcolor(
        points[:, 0], points[:, 1], hops, cmap="viridis", shading="gouraud"
    )
    ax.scatter(*points[source], s=70, marker="*", color="tab:red", zorder=4)
    style_axes(ax, BOX)
    ax.set_title(f"hops to every node (max {diameter})", fontsize=10)
    fig.colorbar(sc, ax=ax, label="hop distance", shrink=0.7)

    ax = axes[1, 2]
    ks = np.arange(diameter + 1)
    fraction = np.array([np.mean(hops <= k) for k in ks])
    ax.plot(ks, 100 * fraction, color="tab:blue", linewidth=2)
    for k in HOP_STEPS:
        ax.plot(k, 100 * fraction[k], "o", color="tab:orange")
    ax.set_xlabel("message-passing steps $k$", fontsize=10)
    ax.set_ylabel("nodes reached [%]", fontsize=10)
    ax.set_title("receptive field size", fontsize=10)
    ax.set_xlim(0, diameter)
    ax.set_ylim(0, 102)
    ax.grid(True, linestyle="--", linewidth=0.5)
    fig.suptitle(
        "Receptive field of one wake node on a cylinder mesh "
        f"({n_nodes} nodes, {len(edges)} edges)",
        fontsize=13,
    )
    return fig


def diffusion_figure(points, triangles, snapshots, history, dt, drift):
    """Field snapshots of the message-passing diffusion and the variance growth."""
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.8), layout="constrained")
    window = (-1.0, 2.2, -1.2, 1.7)
    for ax, t in zip(axes[:3], SNAPSHOT_TIMES, strict=True):
        h = snapshots[t]
        tpc = ax.tripcolor(
            points[:, 0],
            points[:, 1],
            triangles,
            h / h.max(),
            cmap="cividis",
            shading="gouraud",
            vmin=0.0,
            vmax=1.0,
        )
        style_axes(ax, window)
        ax.set_title(f"$t$ = {t:.2f} s, max $h$ = {h.max():.1f}", fontsize=10)
    fig.colorbar(tpc, ax=axes[2], label="$h$ / max $h$", shrink=0.85)

    ax = axes[3]
    t = np.asarray(history["t"])
    ax.plot(
        t, history["variance"], color="tab:blue", linewidth=2, label="message passing"
    )
    ax.plot(
        t,
        BLOB_SIGMA**2 + 2.0 * KAPPA * t,
        "--",
        color="tab:orange",
        label=r"free space: $\sigma_0^2 + 2\kappa t$",
    )
    ax.set_xlabel("$t$ [s]", fontsize=10)
    ax.set_ylabel(r"spread $\sigma^2$ [m$^2$]", fontsize=10)
    ax.set_title(f"{len(t) - 1} steps, relative mass drift {drift:.1e}", fontsize=10)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, linestyle="--", linewidth=0.5)
    fig.suptitle(
        "Linear message passing with cotangent-weighted messages reproduces diffusion",
        fontsize=13,
    )
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    points, triangles = cylinder_mesh()
    edges = unique_edges(triangles)
    source = int(np.argmin(np.hypot(*(points - np.array(SOURCE_POINT)).T)))
    hops = hop_distances(len(points), edges, source)
    for k in HOP_STEPS:
        print(f"k = {k}: {np.sum((hops >= 0) & (hops <= k))} nodes reached")
    print(f"nodes {len(points)}, edges {len(edges)}, max hops {hops.max()}")

    snapshots, history, dt, drift = run_diffusion(points, triangles)
    print(
        f"dt = {dt:.2e} s, steps = {len(history['t']) - 1}, "
        f"sigma^2 = {history['variance'][-1]:.4f} "
        f"(exact {BLOB_SIGMA**2 + 2 * KAPPA * SNAPSHOT_TIMES[-1]:.4f}), "
        f"mass drift = {drift:.1e}"
    )

    figures = {
        "gnn_message_passing.png": receptive_field_figure(points, edges, hops, source),
        "gnn_message_passing_diffusion.png": diffusion_figure(
            points, triangles, snapshots, history, dt, drift
        ),
    }
    finish_figures(figures, output=args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
