# Cable Force Polygon

This script solves the tensions of a mass held by two cables, draws its free-body diagram and closed force polygon to scale, and plots how the tension of a sagging cable grows as the sag angle shrinks. A 100 kg mass hangs from cables at $30^\circ$ and $45^\circ$ above the horizontal; the same linear solver also handles the three-cable system of the particle-equilibrium note.

## Overview

- Solves $\sum_i T_i\mathbf{u}_i + \mathbf{F} = \mathbf{0}$ for the cable tensions as a linear system, in 2D and 3D, and compares the 2D result with the closed form.
- Panel (a): free-body diagram of the mass with both tensions and the weight drawn to the same scale.
- Panel (b): the weight and the two tensions placed head to tail; the printed closure error is the magnitude of their sum.
- Panel (c): $T/W = 1/(2\sin\theta)$ for a symmetric cable carrying a load at its midpoint, with the 20 kg traffic light at $15^\circ$ marked.

## Mathematical Background

With unit vectors $\mathbf{u}_i$ from the particle towards each anchor, equilibrium is the square linear system

```math
\begin{bmatrix} \mathbf{u}_1 & \cdots & \mathbf{u}_n \end{bmatrix}\mathbf{T} = -\mathbf{F}_{\mathrm{app}}
```

For two cables at $\theta_1$ and $\theta_2$ above the horizontal on opposite sides,

```math
T_1 = \frac{W\cos\theta_2}{\sin(\theta_1 + \theta_2)}, \qquad T_2 = \frac{W\cos\theta_1}{\sin(\theta_1 + \theta_2)}
```

and for a symmetric cable with both halves at the sag angle $\theta$, $T = W/(2\sin\theta)$.

## Implementation

- `concurrent_tensions(directions, load)` normalises the direction vectors and solves the system with `numpy.linalg.solve`.
- `two_cable_closed_form(weight, theta1, theta2)` evaluates the closed form.
- `arrow(ax, start, vector, color, ...)` draws a force arrow; `make_figure(weight, t1, t2)` draws the three panels.
- Constants `MASS`, `GRAVITY`, `ANGLE_RIGHT`, `ANGLE_LEFT`, `TRAFFIC_LIGHT_MASS` and `TRAFFIC_LIGHT_ANGLE` set the cases.

## Usage

```bash
python main.py                          # print the tensions and show the figure
python main.py --no-show --output .     # save statics_cable_force_polygon.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints $T_1 = 718.1$ N and $T_2 = 879.5$ N for the two-cable case, equal to the closed form, and $T_A = 103.1$ N, $T_B = 266.5$ N, $T_C = 209.8$ N for the three cables anchored at $(3, 0, 4)$, $(-2, 2, 5)$ and $(1, -3, 6)$ m holding 500 N.

![Free-body diagram, force polygon and cable tension against sag angle](statics_cable_force_polygon.png)

The force polygon closes to round-off ($2 \times 10^{-13}$ N). The traffic light at $15^\circ$ sag puts 379 N, 1.93 times its weight, into each half of the cable.

## Related Notes

- [Particle Equilibrium](../../../notes/applied_mechanics/statics/particle_equilibrium.md)
