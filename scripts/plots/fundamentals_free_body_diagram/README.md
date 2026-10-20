# Free-Body Diagram of a Beam

This script turns a loaded, supported beam into its free-body diagram and solves the three planar equilibrium equations for the support reactions. An 8 m beam with a pin at $A$ and a roller at $B$ carries a 20 kN load inclined at $60^\circ$ below the horizontal at 3 m and a 5 kN/m uniform load over its last 3 m.

## Overview

- Resolves each inclined point load into components and replaces each linearly varying distributed load by its resultant at the centroid.
- Solves $\sum F_x = 0$, $\sum F_y = 0$ and $\sum M_A = 0$ for $A_x$, $A_y$ and $B_y$.
- Checks the solution with an independent moment sum about $B$.
- Draws the space diagram (supports as symbols, loads as given) above the free-body diagram (supports replaced by reactions, distributed load by its dashed resultant), with the solved values on the arrows.

## Mathematical Background

A linearly varying load from $w_0$ at $x_0$ to $w_1$ at $x_1$ has the resultant and centroid

$$
R = \frac{w_0 + w_1}{2}(x_1 - x_0),
\qquad \bar{x} = x_0 + (x_1 - x_0) \frac{w_0 + 2w_1}{3(w_0 + w_1)}
$$

which reduce to $wL$ at the midpoint for a uniform load and to $\tfrac{1}{2}w_1L$ at $\tfrac{2}{3}L$ from the zero end for a triangular one. With point loads $(P_{x,k}, P_{y,k})$ at $x_k$ and distributed resultants $R_m$ (downward) at $\bar{x}_m$, the equilibrium of a pin–roller beam of length $L$ gives

$$
B_y = \frac{1}{L}\left(\sum_m R_m \bar{x}_m - \sum_k P_{y,k} x_k\right),
\qquad A_y = \sum_m R_m - \sum_k P_{y,k} - B_y,
\qquad A_x = -\sum_k P_{x,k}
$$

The moment equation is taken about $A$ so that it contains one unknown.

## Implementation

- `point_load_components(loads)` converts `(x, magnitude, angle)` to `(x, F_x, F_y)`.
- `distributed_resultant(x0, x1, w0, w1)` implements the resultant and centroid formulas.
- `beam_reactions(length, point_loads, distributed)` returns `(A_x, A_y, B_y)` in kN.
- `equilibrium_residual(reactions)` returns $\sum F_x$, $\sum F_y$ and $\sum M_B$ including the reactions, all of which should vanish.
- `make_figure` draws the two panels with `draw_beam`, `draw_supports`, `draw_loads` and `force_arrow`. Constants `LENGTH`, `POINT_LOADS`, `DISTRIBUTED_LOADS` and `ARROW_SCALE` set the problem and the drawing scale.

## Usage

```bash
python main.py                          # print the reactions and show the figure
python main.py --no-show --output .     # save fundamentals_free_body_diagram.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints $A_x = -10.000$ kN (10 kN to the left), $A_y = 13.638$ kN and $B_y = 18.683$ kN, and an equilibrium check whose three sums are zero to round-off.

![Space diagram and free-body diagram of a pin-roller beam](fundamentals_free_body_diagram.png)

The top panel is what the engineer is given. In the bottom panel the pin has become two force components and the roller one, the distributed load has become a single 15 kN force at $x = 6.5$ m, and $A_x$ points left because the horizontal component of the inclined load pushes the beam to the right.

## Related Notes

- [Free-Body Diagrams](../../../notes/applied_mechanics/fundamentals/free_body_diagrams.md)
- [Introduction to Applied Mechanics](../../../notes/applied_mechanics/fundamentals/intro.md)
