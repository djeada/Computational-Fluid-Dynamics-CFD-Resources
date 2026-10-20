# Coplanar Force Resultant

This script reduces a coplanar system of forces and a couple acting on a plate to an equivalent force–couple system at a point and then to a single resultant force on its line of action. Three forces of 400 N, 300 N and 250 N and a 400 N·m couple act on a 4 m × 2 m plate; the script computes the resultant force, its moment about the corner $O$, the perpendicular distance from $O$ to the line of action, and where that line crosses the plate.

## Overview

- Builds the force vectors from magnitudes and directions in `FORCES` and sums them into the resultant $\mathbf{R}$.
- Sums the moments of the forces about $O$ with $M_O = xF_y - yF_x$ and adds the applied couple `COUPLE`.
- Finds the line of action of the single resultant, the foot of the perpendicular from $O$ and the moment arm $d = |M_O|/|\mathbf{R}|$.
- Draws three panels: the applied loads, the force–couple system at $O$, and the single resultant on its line of action.
- Prints the resultant, its direction, $M_O$, $d$ and the two points where the line of action crosses the top and bottom edges of the plate.

## Mathematical Background

Two force systems are equivalent for a rigid body when they have the same resultant force and the same resultant moment about one (and therefore every) point. For coplanar forces $\mathbf{F}_i$ applied at $(x_i, y_i)$ and couples $C_j$ (counterclockwise positive),

$$
\mathbf{R} = \sum_i \mathbf{F}_i,
\qquad M_O = \sum_i \left(x_i F_{iy} - y_i F_{ix}\right) + \sum_j C_j
$$

If $\mathbf{R} \neq \mathbf{0}$, a single force $\mathbf{R}$ placed at a point $(x, y)$ is equivalent to the system when its moment about $O$ equals $M_O$:

$$
x R_y - y R_x = M_O
$$

This is the equation of the line of action. Its distance from $O$ is $d = |M_O|/|\mathbf{R}|$. If $\mathbf{R} = \mathbf{0}$ the system reduces to a pure couple and has no line of action.

## Implementation

- `force_vectors(forces)` converts `(magnitude, angle, point)` triples into arrays of vectors and points.
- `moment_2d(point, force, about)` returns $x F_y - y F_x$ relative to `about`.
- `resultant(vectors, points, couple, about)` returns $\mathbf{R}$ and $M$ about `about`.
- `line_of_action(total, moment, about)` returns the foot of the perpendicular from `about` and the unit direction of $\mathbf{R}$; it raises `ValueError` for a zero resultant.
- `axis_intercept(total, moment, y)` returns the $x$ where the line of action crosses height $y$.
- `make_figure` draws the plate with `draw_plate`, forces with `draw_force` and couples with `draw_couple`. `ARROW_SCALE` sets the drawn length per newton.

## Usage

```bash
python main.py                          # print the results and show the figure
python main.py --no-show --output .     # save fundamentals_force_resultant.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints $\mathbf{R} = (-100.0, -659.8)$ N, $|\mathbf{R}| = 667.3$ N directed $-98.6^\circ$ from $+x$, $M_O = -624.5$ N·m (624.5 N·m clockwise) and $d = 0.936$ m. The line of action crosses $y = 0$ at $x = 0.947$ m and $y = 2$ m at $x = 1.250$ m.

![Coplanar force system, force-couple system at O and single resultant](fundamentals_force_resultant.png)

Panel (a) shows the applied loads, panel (b) the same system replaced by $\mathbf{R}$ acting at $O$ together with the couple $M_O$, and panel (c) the single force $\mathbf{R}$ moved sideways until its own moment about $O$ equals $M_O$. All three are equivalent for the equilibrium of the plate; they differ in the internal forces they cause.

## Related Notes

- [Force Systems and Resultants](../../../notes/applied_mechanics/fundamentals/force_systems.md)
- [Moments and Couples](../../../notes/applied_mechanics/fundamentals/moments_couples.md)
