# Surrogate Input Representations

This script draws one NACA 2412 airfoil in the four forms a neural-network surrogate can take as input: a parameter vector, a signed distance field on a Cartesian grid, a surface point cloud, and a mesh graph. Each form fixes which network family can be used (multilayer perceptron, convolutional network, PointNet-type network, graph neural network) and how much geometric detail survives the encoding. The figure puts them side by side so the trade-offs can be seen on the same shape.

## Overview

- Builds the NACA 2412 outline from the 4-digit thickness and camber formulas with cosine spacing and the closed-trailing-edge coefficient $-0.1036$.
- Panel (a) shows the parameter vector $(m, p, t, \alpha, \log_{10} Re) = (0.02, 0.4, 0.12, 4^\circ, 6.48)$ as bars normalised to assumed design ranges, with shape parameters and operating conditions in different colours.
- Panel (b) samples the signed distance $\phi$ (negative inside) at the 64 x 24 cell centres of a grid with spacing $0.025c$ on $[-0.3, 1.3]c \times [-0.3, 0.3]c$, and overlays the zero contour of the sampled field (black) on the exact outline (green dashed).
- Panel (c) draws 80 surface points sampled uniformly in arc length from a seeded generator, with their outward unit normals.
- Panel (d) builds a graded triangle mesh with 681 nodes and 1835 edges from level sets of $\phi$ and colours the nodes by type: 171 wall, 473 fluid and 37 far-field nodes.

## Mathematical Background

### NACA 4-Digit Airfoil

For maximum camber $m$, camber position $p$ and thickness $t$ (fractions of the chord $c = 1$), the half-thickness is

```math
y_t = \frac{t}{0.2}\left(0.2969\sqrt{x} - 0.1260\,x - 0.3516\,x^2 + 0.2843\,x^3 - 0.1036\,x^4\right)
```

and the surfaces are offset by $\pm y_t$ normal to the piecewise-parabolic camber line $y_c(x)$. The coefficient $-0.1036$ (instead of $-0.1015$) closes the trailing edge.

### Normalised Parameters

Each parameter $p_i$ is scaled to its design range $[p_i^{\min}, p_i^{\max}]$:

$$
\tilde{p}_i = \frac{p_i - p_i^{\min}}{p_i^{\max} - p_i^{\min}}
$$

The ranges in `PARAMETER_RANGES` are illustrative: $m \in [0, 0.06]$, $p \in [0.2, 0.7]$, $t \in [0.06, 0.20]$, $\alpha \in [-4^\circ, 12^\circ]$, $\log_{10} Re \in [6, 7]$.

### Signed Distance Field

```math
\phi(\mathbf{x}) = \pm \min_{\mathbf{y} \in \partial\Omega} \|\mathbf{x} - \mathbf{y}\|
```

with the minus sign inside the body $\Omega$. The script approximates the minimum with a k-d tree over the outline resampled every $5 \times 10^{-4} c$, and takes the sign from a point-in-polygon test. The field is continuous across the wall and $|\nabla\phi| = 1$ almost everywhere, which makes it a smoother network input than a binary occupancy mask.

### Graded Mesh from Level Sets

Mesh layers are placed on the contours $\phi = d_j$ with $d_{j+1} = d_j + h(d_j)$ and spacing $`h(d) = 0.012c + 0.35\, d`$, up to $d = 0.3c$. Each contour is resampled at spacing $h(d_j)$, the nodes are triangulated with `scipy.spatial.Delaunay`, and triangles inside the airfoil or with an edge longer than $2h(0.3c)$ are removed.

## Implementation

- `naca4(code, n)` returns the closed counter-clockwise outline; `resample(outline, spacing)` places points evenly in arc length.
- `signed_distance(points, outline)` evaluates $\phi$; `sdf_grid(outline)` evaluates it on the CNN grid defined by `GRID_SPACING` and `GRID_BOX`.
- `normalised_parameters(code, alpha, reynolds)` returns raw and normalised parameters.
- `point_cloud(outline, n, seed)` samples surface points and outward normals.
- `mesh_graph(outline)` extracts level sets of a fine $\phi$ grid with `skimage.measure.find_contours` and returns nodes, edges and node types (0 wall, 1 fluid, 2 far field).
- `make_figure(outline)` draws the four panels; `main(argv=None)` parses the flags and saves or shows the figure.
- [`tests/test_gnn_ml.py`](../../../tests/test_gnn_ml.py) checks the sign and magnitude of $\phi$ for NACA 0012 and that the point cloud lies on the surface with unit outward normals.

## Usage

```bash
python main.py                          # open the figure window
python main.py --no-show --output out   # save surrogate_input_representations.png into out/
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

Panel (a) holds five numbers, the most compact input, but it can only describe shapes inside the NACA family. In panel (b), 133 of the 1536 grid cells lie inside the airfoil, and the last cell centre inside the section is at $x = 0.94c$. The airfoil is thinner than one cell ($0.025c$) over the last 9 % of the chord, so the zero contour of the sampled field stops short of the trailing edge. This is the resolution loss of grid-based inputs. Panel (c) keeps the exact surface but no connectivity and no point order. Panel (d) keeps the wall exactly and concentrates nodes near it, which is what a CFD mesh does and what a graph network consumes.

![Four input representations of a NACA 2412 airfoil](surrogate_input_representations.png)

## Related Notes

- [Neural-Network Surrogates for Aerodynamics](../../../notes/machine_learning/neural_networks/intro.md)
- [Graph Neural Networks for CFD](../../../notes/machine_learning/neural_networks/graph_neural_networks.md)
- [Machine Learning on CAD](../../../notes/machine_learning/geometry/ml_on_cad.md)
