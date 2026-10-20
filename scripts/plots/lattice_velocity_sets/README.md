# Lattice Velocity Sets

This script draws the D2Q9 and D3Q19 velocity sets with their indices and weights, the streaming step on a small lattice, and half-way bounce-back at a wall. The top row shows the discrete velocities of the two most common lattice Boltzmann lattices, and the bottom row shows what one time step does to the populations of a single D2Q9 node.

## Overview

- Panel (a) shows the nine D2Q9 velocities in the counter-clockwise ordering $i = 0$ (rest), 1 to 4 (east, north, west, south) and 5 to 8 (north-east, north-west, south-west, south-east), each labelled with its index and weight 4/9, 1/9 or 1/36 and coloured by speed.
- Panel (b) is a 3D quiver of the D3Q19 velocities, the 6 face neighbours (weight 1/18) and 12 edge neighbours (weight 1/36) of a cube, with the rest velocity (weight 1/3) at the centre.
- Panel (c) draws the eight moving post-collision populations of the centre node of a $3 \times 3$ patch, drawn as short arrows in their directions.
- Panel (d) draws the same populations after streaming, each now attached to the neighbour $\mathbf{x} + \mathbf{c}_i$, with a dotted line showing the link it travelled.
- Panel (e) shows a fluid node next to a wall at mid-link, with the south and south-east populations leaving towards the wall and returning as the north and north-west populations one step later.
- Prints the zeroth, first and second moments of both weight sets as a check.

## Mathematical Background

### Velocity Sets and Weights

The D2Q9 velocities are $(0,0)$, $(\pm 1, 0)$, $(0, \pm 1)$ and $(\pm 1, \pm 1)$ in units of $\Delta x/\Delta t$. D3Q19 consists of the rest velocity, the six face neighbours $(\pm 1, 0, 0), (0, \pm 1, 0), (0, 0, \pm 1)$ and the twelve edge neighbours with two nonzero components. The weights satisfy

```math
\sum_i w_i = 1, \qquad \sum_i w_i \mathbf{c}_i = \mathbf{0}, \qquad \sum_i w_i \mathbf{c}_i \mathbf{c}_i = c_s^2 \mathbf{I}, \qquad c_s^2 = \frac{1}{3}
```

and the fourth-order isotropy condition $\sum_i w_i c_{i\alpha}c_{i\beta}c_{i\gamma}c_{i\delta} = c_s^4(\delta_{\alpha\beta}\delta_{\gamma\delta} + \delta_{\alpha\gamma}\delta_{\beta\delta} + \delta_{\alpha\delta}\delta_{\beta\gamma})$, which makes the lattice viscosity isotropic.

### Streaming and Bounce-Back

Streaming moves each post-collision population one link along its velocity, $f_i(\mathbf{x} + \mathbf{c}_i\Delta t, t + \Delta t) = f_i^\star(\mathbf{x}, t)$. At a fluid node $`\mathbf{x}_b`$ next to a wall located halfway along the link, half-way bounce-back returns the population to its own node in the opposite direction $`\bar\imath`$, $`\mathbf{c}_{\bar\imath} = -\mathbf{c}_i`$:

```math
f_{\bar\imath}(\mathbf{x}_b, t + \Delta t) = f_i^\star(\mathbf{x}_b, t)
```

## Implementation

- `D2Q9_VELOCITIES`, `D2Q9_WEIGHTS` and `D2Q9_OPPOSITE` hold the 2D lattice; `d3q19_velocities()` builds the 19 velocities by shell and `d3q19_weights()` assigns the weights by squared speed.
- `draw_d2q9`, `draw_d3q19`, `draw_streaming(ax, after)` and `draw_bounce_back` each draw one panel with Matplotlib patches and a 3D quiver; `arrow` wraps `FancyArrowPatch`.
- `make_figure` arranges the five panels on a 2 × 6 grid, and `main` prints the moment checks before saving or showing the figure.

## Usage

```bash
python main.py                          # print the moment checks and show the figure
python main.py --no-show --output .     # save lattice_velocity_sets.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints

```text
D2Q9: sum w = 1.000000, sum w c = 0.0e+00, sum w c c = 0.333333 I (off-diagonal 0.0e+00)
D3Q19: sum w = 1.000000, sum w c = 0.0e+00, sum w c c = 0.333333 I (off-diagonal 0.0e+00)
```

![D2Q9 and D3Q19 velocity sets, streaming and half-way bounce-back](lattice_velocity_sets.png)

The axis velocities of D2Q9 carry four times the weight of the diagonals, and D3Q19 has no corner velocities. In panels (c) and (d) each colour is one population index, so the arrow of colour $i$ moves from the centre to the neighbour in direction $i$. In panel (e) the solid arrows are populations leaving $\mathbf{x}_b$ at time $t$ and the dashed arrows are the reversed populations that arrive back at $\mathbf{x}_b$ at $t + \Delta t$; the reflection happens at the wall line, halfway between the fluid node and the solid nodes below it.

## Related Notes

- [From Boltzmann to Lattice Boltzmann](../../../notes/numerical/lattice_boltzmann/from_boltzmann_to_lattice_boltzmann.md)
- [The Lattice Boltzmann Algorithm](../../../notes/numerical/lattice_boltzmann/lattice_boltzmann_algorithm.md)
- [Introduction to the Lattice Boltzmann Method](../../../notes/numerical/lattice_boltzmann/intro.md)
