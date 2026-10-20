# Slider-Crank Kinematics

This script solves the velocity and acceleration of a slider-crank mechanism with the rigid-body relative-motion equations and checks the results against finite differences of the exact slider position. A 0.1 m crank turning at 10 rad/s drives a 0.3 m connecting rod, and the instantaneous centre of the rod is located at a crank angle of $60^\circ$.

## Overview

- Places the crank pin $A$ at $r(\cos\theta, \sin\theta)$ and the slider $B$ on the $x$ axis at $x_B = r\cos\theta + \sqrt{l^2 - r^2\sin^2\theta}$.
- Solves $`\mathbf{v}_B = \mathbf{v}_A + \omega_{AB}\mathbf{k} \times \mathbf{r}_{B/A}`$ for $\omega_{AB}$ and $v_B$, and $`\mathbf{a}_B = \mathbf{a}_A + \alpha_{AB}\mathbf{k} \times \mathbf{r}_{B/A} - \omega_{AB}^2\mathbf{r}_{B/A}`$ for $`\alpha_{AB}`$ and $a_B$, at every crank angle.
- Compares $v_B$ and $a_B$ with central differences of $x_B(\theta(t))$.
- Locates the instantaneous centre (IC) of the rod and draws the mechanism with $\mathbf{v}_A$ and $\mathbf{v}_B$.
- Overlays the two-term approximation of the piston acceleration used in engine balancing.

## Mathematical Background

With constant crank speed $\omega$ (counterclockwise), $\mathbf{v}_A = \omega\mathbf{k} \times \mathbf{r}_A$ and $`\mathbf{a}_A = -\omega^2\mathbf{r}_A`$. Writing $`\mathbf{r}_{B/A} = (b_x, b_y)`$, the $\mathbf{j}$ components of the relative-motion equations must vanish because $B$ moves along $x$:

```math
\omega_{AB} = -\frac{v_{A,y}}{b_x},
\quad
v_B = v_{A,x} - \omega_{AB}b_y,
\quad
\alpha_{AB} = \frac{\omega_{AB}^2 b_y - a_{A,y}}{b_x},
\quad
a_B = a_{A,x} - \alpha_{AB}b_y - \omega_{AB}^2 b_x
```

The IC of the rod lies on the line $OA$ extended (perpendicular to $\mathbf{v}_A$) and on the vertical through $B$ (perpendicular to $\mathbf{v}_B$), at $(x_B, x_B\tan\theta)$. Expanding $x_B$ in powers of $r/l$ gives the two-term piston acceleration

```math
a_B \approx -r\omega^2\left(\cos\theta + \frac{r}{l}\cos 2\theta\right)
```

## Implementation

- `slider_position(theta)` returns the exact $x_B$.
- `kinematics(theta)` returns a dictionary with the positions of $A$ and $B$, $`\mathbf{r}_{B/A}`$, $`\mathbf{v}_A`$, $`\omega_{AB}`$, $`\alpha_{AB}`$, $v_B$ and $a_B$.
- `instantaneous_centre(theta)` returns the IC of the rod; `approximate_piston_acceleration(theta)` the two-term series.
- `finite_difference_check(n)` differentiates $x_B$ on a periodic grid of $n$ crank angles.
- `draw_mechanism(ax, theta)` and `make_figure()` draw the figure; `CRANK`, `ROD`, `CRANK_RATE` and `DRAW_ANGLE_DEG` set the case.

## Usage

```bash
python main.py                          # print values at four crank angles and show the figure
python main.py --no-show --output .     # save dynamics_slider_crank_kinematics.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

At $\theta = 60^\circ$ the script prints $v_B = -1.017$ m/s, $a_B = -3.34$ m/s², $\omega_{AB} = -1.741$ rad/s (clockwise) and $\alpha_{AB} = 29.2$ rad/s². At $\theta = 90^\circ$, $v_B = -r\omega = -1$ m/s and $\omega_{AB} = 0$: the rod translates instantaneously. At the dead centres $v_B = 0$, and $a_B = -13.33$ m/s² at $\theta = 0$ and $+6.67$ m/s² at $180^\circ$, the values $\mp r\omega^2(1 \pm r/l)$. The largest differences from the finite differences on 720 angles are $1.9\times10^{-5}$ m/s and $1.4\times10^{-4}$ m/s².

![Slider-crank mechanism with IC, slider and rod kinematics](dynamics_slider_crank_kinematics.png)

Panel (a) shows the mechanism at $60^\circ$ with the IC of the rod where the line $OA$ extended meets the vertical through $B$. Panel (b) shows that the slider acceleration at $\theta = 0$ is twice that at $180^\circ$ for $r/l = 1/3$, which the two-term series reproduces closely. Panel (c) shows $\omega_{AB}$ and $\alpha_{AB}$ over one revolution.

## Related Notes

- [Rigid Body Kinematics](../../../notes/applied_mechanics/dynamics/rigid_body_kinematics.md)
- [Rigid Body Kinetics](../../../notes/applied_mechanics/dynamics/rigid_body_kinetics.md)
