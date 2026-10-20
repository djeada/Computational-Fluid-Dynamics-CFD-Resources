# Control-Volume Stencil

This script draws the notation of the finite volume method: a 1D cell-centred grid with nodes W, P, E and faces w, e, and two unstructured 2D cells with the face area vector, the vector between the cell centroids and the split of the face area vector used to correct the diffusion flux on non-orthogonal meshes. The geometry of the 2D panel is computed from the polygon vertices, so the centroids, the angle between $\mathbf{d}$ and $\mathbf{S}_f$, the vectors $\boldsymbol{\Delta}$ and $\mathbf{k}$ and the skewness vector $\mathbf{m}$ in the drawing are exact for the cells shown.

## Overview

- Draws five 1D cells WW, W, P, E, EE with the faces w and e of cell P, the face fluxes $J_w$ and $J_e$, the cell width $\Delta x = \delta x_{we}$, the node distances $\delta x_{WP}$, $\delta x_{PE}$ and the node-to-face distances $\delta x_{wP}$, $\delta x_{Pe}$.
- Draws an owner cell P (pentagon) and a neighbour cell N (pentagon) that share one face, with the polygon centroids $\mathbf{x}_P$, $\mathbf{x}_N$ and the face centre $\mathbf{x}_f$.
- Computes the face area vector $\mathbf{S}_f$ (pointing from P to N), $\mathbf{d} = \mathbf{x}_N - \mathbf{x}_P$, the over-relaxed split $`\mathbf{S}_f = \boldsymbol{\Delta} + \mathbf{k}`$, and the point $`\mathbf{x}_{f'}`$ where the line from P to N crosses the face, and prints them.

## Mathematical Background

For a polygon with vertices $(x_j, y_j)$ the area and centroid follow from the shoelace formula,

```math
A = \frac{1}{2}\sum_j (x_j y_{j+1} - x_{j+1} y_j),
\qquad
\mathbf{x}_c = \frac{1}{6A}\sum_j (\mathbf{x}_j + \mathbf{x}_{j+1})(x_j y_{j+1} - x_{j+1} y_j)
```

In 2D with unit depth the face area vector of a face from $\mathbf{a}$ to $\mathbf{b}$ is the face normal scaled by the face length, $\mathbf{S}_f = (b_y - a_y,\ -(b_x - a_x))$, with the sign chosen so that $\mathbf{S}_f\cdot\mathbf{d} > 0$. The over-relaxed decomposition of Jasak (1996) is

```math
\boldsymbol{\Delta} = \frac{\mathbf{S}_f\cdot\mathbf{S}_f}{\mathbf{d}\cdot\mathbf{S}_f}\,\mathbf{d},
\qquad
\mathbf{k} = \mathbf{S}_f - \boldsymbol{\Delta}
```

so $\boldsymbol{\Delta}$ is parallel to $\mathbf{d}$ and $\mathbf{k}\cdot\mathbf{S}_f = 0$. The line $\mathbf{x}_P + \lambda\mathbf{d}$ meets the face plane at $`\lambda = (\mathbf{x}_f - \mathbf{x}_P)\cdot\mathbf{S}_f/(\mathbf{d}\cdot\mathbf{S}_f)`$, which gives $`\mathbf{x}_{f'}`$ and the skewness vector $`\mathbf{m} = \mathbf{x}_f - \mathbf{x}_{f'}`$.

## Implementation

- `polygon_centroid(vertices)` returns the centroid and area of a polygon.
- `face_geometry()` returns a dictionary with $\mathbf{x}_P$, $\mathbf{x}_N$, $\mathbf{x}_f$, $\mathbf{S}_f$, $`\mathbf{d}`$, $`\boldsymbol{\Delta}`$, $`\mathbf{k}`$, $`\mathbf{x}_{f'}`$, the interpolation parameter $`\lambda`$ and the angle between $`\mathbf{d}`$ and $`\mathbf{S}_f`$.
- `draw_1d(ax)` and `draw_2d(ax, g)` draw the two panels with Matplotlib patches; `make_figure(g)` stacks them.
- Constants `DX`, `CELL_LABELS`, `FACE_A`, `FACE_B`, `OWNER` and `NEIGHBOUR` define the drawing.

## Usage

```bash
python main.py                          # print the geometry and show the figure
python main.py --no-show --output .     # save control_volume_stencil.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints the geometry of panel (b):

```text
x_P = [-0.859 -0.553], x_N = [ 1.393 -0.119], x_f = [ 0.25 -0.6 ]
S_f = [ 3.2 -0.7], |S_f| = 3.276
d = [2.252 0.435], angle(d, S_f) = 23.3 deg
Delta = [3.501 0.676], k = [-0.301 -1.376], k . S_f = -8.88e-16
f' = [ 0.31  -0.328], |m| = |f - f'| = 0.279
```

The non-orthogonality angle is 23°, so $|\boldsymbol{\Delta}| = |\mathbf{S}_f|/\cos 23.3^\circ$ is 9% larger than $|\mathbf{S}_f|$.

![Control-volume notation in 1D and on unstructured cells](control_volume_stencil.png)

In panel (a) the shaded cell is the control volume of node P; the total flux $`J = \rho u\phi - \Gamma\,d\phi/dx`$ is evaluated on the red faces. In panel (b) the dashed vector $\mathbf{d}$ crosses the shared face at $\mathbf{x}_{f'}$, not at the face centre $\mathbf{x}_f$, and the green $\boldsymbol{\Delta}$ along $\mathbf{d}$ plus the orange $\mathbf{k}$ add up to the blue face area vector $\mathbf{S}_f$.

## Related Notes

- [The Finite Volume Method](../../../notes/numerical/fvm/intro.md)
- [Finite Volume Discretization on General Meshes](../../../notes/numerical/fvm/discretization.md)
