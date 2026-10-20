# Path, Polar and Rotating-Frame Coordinates

This script draws the acceleration of three moving particles resolved in the coordinate system that suits each of them: normal–tangential components along a projectile path, radial–transverse components for a bead on a rotating rod, and Coriolis and centrifugal terms for a puck seen from a rotating turntable. The vectors are computed from the exact motions, not sketched.

## Overview

- Resolves gravity into $a_t$ along and $a_n$ normal to the path of a drag-free projectile (30 m/s at $50^\circ$) at four points and draws the osculating circle of radius $\rho = v^2/a_n$ at the first.
- Draws the unit vectors $`\mathbf{e}_r`$, $`\mathbf{e}_\theta`$ and the acceleration of a bead on a frictionless rod rotating at 3 rad/s, $r = r_0\cosh\omega t$, whose radial acceleration is zero.
- Transforms a puck sliding at constant velocity into a frame rotating at 0.6 rad/s and draws the Coriolis and centrifugal accelerations that bend its apparent path.
- Checks numerically that the relative acceleration in the rotating frame equals $-2\boldsymbol{\Omega} \times \mathbf{v}_{\mathrm{rel}} - \boldsymbol{\Omega} \times (\boldsymbol{\Omega} \times \mathbf{r})$.

## Mathematical Background

Along a path, $`\mathbf{a} = \dot{v}\,\mathbf{e}_t + (v^2/\rho)\,\mathbf{e}_n`$. For the projectile $\mathbf{a} = -g\mathbf{j}$, so $`a_n = g\,|v_x|/v`$ and $\rho = v^3/(g|v_x|)$; at the apex $\rho = v_x^2/g$.

In polar coordinates,

```math
\mathbf{a} = (\ddot{r} - r\dot{\theta}^2)\,\mathbf{e}_r + (r\ddot{\theta} + 2\dot{r}\dot{\theta})\,\mathbf{e}_\theta
```

For the bead, $\dot{\theta} = \omega$ and $r = r_0\cosh\omega t$ give $\ddot{r} = r\omega^2$, so $a_r = 0$ and $a_\theta = 2\dot{r}\omega$: the rod pushes the bead sideways and nothing pushes it outward.

For a frame rotating at constant $\boldsymbol{\Omega}$ about a fixed origin, the absolute acceleration is $`\mathbf{a} = \mathbf{a}_{\mathrm{rel}} + 2\boldsymbol{\Omega} \times \mathbf{v}_{\mathrm{rel}} + \boldsymbol{\Omega} \times (\boldsymbol{\Omega} \times \mathbf{r})`$. The puck has $\mathbf{a} = \mathbf{0}$, so in the plane $`\mathbf{a}_{\mathrm{rel}} = -2\boldsymbol{\Omega} \times \mathbf{v}_{\mathrm{rel}} + \Omega^2\mathbf{r}`$.

## Implementation

- `projectile_state(t)` and `normal_tangential(v, a)` give the path components, unit vectors and radius of curvature.
- `bead_state(t)` and `polar_acceleration(...)` give the polar coordinates, their rates and $a_r$, $a_\theta$.
- `puck_in_rotating_frame(t)` rotates the inertial straight-line path by $-\Omega t$; `rotating_frame_accelerations(r, v)` returns the Coriolis and centrifugal terms.
- `rotating_frame_check(n)` differentiates the rotating-frame path twice with `np.gradient` and returns the largest mismatch.
- `make_figure()` draws the three panels.

## Usage

```bash
python main.py                          # print the checks and show the figure
python main.py --no-show --output .     # save dynamics_path_coordinates.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The projectile's radius of curvature is 142.7 m at launch and 37.9 m at the apex. At $t = 0.5$ s the bead is at $r = 0.235$ m with $a_r = 0$ and $a_\theta = 3.83$ m/s². The finite-difference relative acceleration of the puck matches the Coriolis and centrifugal terms to $2\times10^{-8}$ m/s².

![Normal-tangential, polar and rotating-frame accelerations](dynamics_path_coordinates.png)

Panel (a) shows $a_t$ opposing the velocity on the way up, vanishing at the apex and aiding it on the way down, while $a_n$ always points into the curve. Panel (b) shows the acceleration of the bead lying along $\mathbf{e}_\theta$ although the bead moves outward ever faster. Panel (c) shows a straight inertial path (dashed) that appears curved to the right in the counterclockwise-rotating frame, bent by the Coriolis term.

## Related Notes

- [Kinematics of Particles](../../../notes/applied_mechanics/dynamics/kinematics_particles.md)
- [Kinetics of Particles](../../../notes/applied_mechanics/dynamics/kinetics_particles.md)
- [Rigid Body Kinematics](../../../notes/applied_mechanics/dynamics/rigid_body_kinematics.md)
