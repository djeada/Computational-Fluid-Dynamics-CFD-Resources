# Moment of a Force About a Point and an Axis

This script computes the moment of a 3D force about a point as a cross product and about an axis as a scalar triple product, and shows numerically which of the two depends on the choice of reference point. The force $\mathbf{F} = (100, -200, 50)$ N acts at $P(0.3, 0.4, 0.2)$ m, and the axis passes through the origin with direction $(2, 1, 2)$.

## Overview

- Computes $\mathbf{M}_O = \mathbf{r} \times \mathbf{F}$ and the axis moment $M_a = \hat{\mathbf{u}} \cdot (\mathbf{r} \times \mathbf{F})$ as a 3 × 3 determinant.
- Splits $\mathbf{M}_O$ into the component along the axis and the component perpendicular to it.
- Moves the reference point $Q$ along the axis and the point of application along the line of action of $\mathbf{F}$, recording $|\mathbf{M}_Q|$ and $M_a$ for each shift.
- Draws $\mathbf{r}$, $\mathbf{F}$, $\mathbf{M}_O$ and its projection in 3D, and the invariance study as curves against the shift.

## Mathematical Background

The moment of $\mathbf{F}$ about a point $Q$ is $`\mathbf{M}_Q = \mathbf{r}_{QP} \times \mathbf{F}`$, with $\mathbf{r}_{QP}$ from $Q$ to any point $P$ on the line of action. The moment about an axis through $A$ with unit vector $\hat{\mathbf{u}}$ is the component of $\mathbf{M}_A$ along the axis:

```math
M_a = \hat{\mathbf{u}} \cdot (\mathbf{r}_{AP} \times \mathbf{F}) =
\begin{vmatrix} u_x & u_y & u_z \\ r_x & r_y & r_z \\ F_x & F_y & F_z \end{vmatrix}
```

Moving $Q$ along the axis to $Q' = Q + s\hat{\mathbf{u}}$ changes the point moment by $`-s\,\hat{\mathbf{u}} \times \mathbf{F}`$, a vector perpendicular to $\hat{\mathbf{u}}$, so $M_a$ is unchanged while $|\mathbf{M}_Q|$ varies. Sliding $P$ along $\mathbf{F}$ adds $`t\,\hat{\mathbf{F}} \times \mathbf{F} = \mathbf{0}`$, so neither moment changes. Since $`|\mathbf{M}_Q|^2 = M_a^2 + |\mathbf{M}_{Q,\perp}|^2`$, the point moment is never smaller than $|M_a|$, and $`|\mathbf{M}_Q| = |\mathbf{F}|\,d_Q`$ with $d_Q$ the distance from $Q$ to the line of action.

## Implementation

- `unit(vector)` normalizes a vector and rejects the zero vector.
- `moment_about_point(about, point, force)` returns $\mathbf{r} \times \mathbf{F}$.
- `moment_about_axis(axis_point, axis_direction, point, force)` evaluates the determinant with `numpy.linalg.det`.
- `split_moment(moment, axis_direction)` returns the parallel and perpendicular parts.
- `invariance_study(shifts)` returns $|\mathbf{M}_Q|$ and $M_a$ over the shifts in `SHIFTS` (from $-1$ to $1$ m).
- `make_figure` draws the 3D panel with `draw_vector` (forces scaled by `FORCE_SCALE`, moments by `MOMENT_SCALE`) and the invariance curves.

## Usage

```bash
python main.py                          # print the moments and show the figure
python main.py --no-show --output .     # save fundamentals_moment_about_axis.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints $\mathbf{M}_O = (60, 5, -100)$ N·m with $|\mathbf{M}_O| = 116.7$ N·m, $\hat{\mathbf{u}} = (0.6667, 0.3333, 0.6667)$ and $M_a = -25.00$ N·m. The parallel part of $\mathbf{M}_O$ is 25.00 N·m and the perpendicular part 114.02 N·m. Over the shifts, $|\mathbf{M}_Q|$ ranges from 25.3 to 341.6 N·m while $M_a$ varies by less than $10^{-13}$ N·m.

![Moment about a point and about an axis](fundamentals_moment_about_axis.png)

In panel (a) the purple arrow on the dashed axis is the projection of $\mathbf{M}_O$; the negative sign of $M_a$ means it points opposite to $\hat{\mathbf{u}}$, so the force tends to turn a body clockwise about the axis when viewed from the tip of $\hat{\mathbf{u}}$. In panel (b) the point moment is $|\mathbf{F}|$ times the distance from $Q$ to the line of action, so its minimum, 25.27 N·m, occurs at $s = 0.503$ m, the point of the axis closest to the line of action; it stays above $|M_a| = 25$ N·m because $\mathbf{F}$ has a 33.3 N component along the axis, which adds to the point moment a part perpendicular to the axis but nothing to $M_a$.

## Related Notes

- [Moments and Couples](../../../notes/applied_mechanics/fundamentals/moments_couples.md)
- [Vector Analysis in Mechanics](../../../notes/applied_mechanics/fundamentals/vector_analysis.md)
