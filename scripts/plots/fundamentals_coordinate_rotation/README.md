# Coordinate Rotation of a Force Vector

This script transforms the components of a force from one Cartesian frame to a rotated one with a rotation matrix and shows that the components depend on the frame while the vector does not. A 500 N force with components $(300, 400)$ N is expressed in a frame rotated counterclockwise by $30^\circ$, and the rotation angle is then swept through a full turn.

## Overview

- Builds the 2D transformation matrix $Q(\theta)$ whose rows are the new unit vectors written in the old frame, and its 3D counterpart for a rotation about $z$.
- Computes the components $\mathbf{F}' = Q\mathbf{F}$ in the rotated frame and recovers $\mathbf{F} = Q^{\mathsf{T}}\mathbf{F}'$.
- Draws the vector with both frames and its perpendicular projections onto each set of axes.
- Plots $F_{x'}$, $F_{y'}$ and $|\mathbf{F}|$ against the rotation angle from $0$ to $360^\circ$.

## Mathematical Background

If the axes $x'y'$ are the axes $xy$ rotated counterclockwise by $\theta$, the new unit vectors are $`\hat{\mathbf{e}}_{x'} = (\cos\theta, \sin\theta)`$ and $`\hat{\mathbf{e}}_{y'} = (-\sin\theta, \cos\theta)`$. A component in the new frame is the projection of the vector on a new unit vector, $F_{x'} = \mathbf{F}\cdot\hat{\mathbf{e}}_{x'}$, so

```math
\begin{bmatrix} F_{x'} \\ F_{y'} \end{bmatrix} =
\begin{bmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{bmatrix}
\begin{bmatrix} F_x \\ F_y \end{bmatrix}
```

The matrix is orthogonal ($QQ^{\mathsf{T}} = I$, $\det Q = 1$), so lengths and dot products are the same in both frames, the inverse transformation is $Q^{\mathsf{T}}$, and two successive rotations by $\alpha$ and $\beta$ equal one rotation by $\alpha + \beta$. In 3D the entries of $Q$ are the direction cosines of the new axes in the old frame.

## Implementation

- `rotation_matrix(theta_deg)` returns the 2 × 2 matrix $Q$; `rotation_matrix_z(theta_deg)` embeds it in a 3 × 3 matrix for a rotation about $z$.
- `transform(vector, theta_deg)` returns $Q\mathbf{F}$.
- `make_figure` draws the frames and projections with `draw_arrow`, and the sweep over `SWEEP` (0 to 360 degrees in 1 degree steps).
- Constants `FORCE` and `ANGLE` set the vector and the rotation of the frame in panel (a).

## Usage

```bash
python main.py                          # print the transformation and show the figure
python main.py --no-show --output .     # save fundamentals_coordinate_rotation.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints $Q(30^\circ) = [[0.8660, 0.5000], [-0.5000, 0.8660]]$, the rotated components $\mathbf{F}' = (459.81, 196.41)$ N with $|\mathbf{F}'| = 500.00$ N, and $Q^{\mathsf{T}}\mathbf{F}' = (300, 400)$ N.

![Force components in two rotated frames](fundamentals_coordinate_rotation.png)

In panel (a) the dotted lines are the projections onto $x$ and $y$ and the dashed orange lines the projections onto $x'$ and $y'$. In panel (b) $F_{x'}$ reaches the full 500 N at $\theta = 53.1^\circ$, where $x'$ is aligned with the force, and $F_{y'}$ is zero there; the dashed magnitude line stays flat.

## Related Notes

- [Vector Analysis in Mechanics](../../../notes/applied_mechanics/fundamentals/vector_analysis.md)
