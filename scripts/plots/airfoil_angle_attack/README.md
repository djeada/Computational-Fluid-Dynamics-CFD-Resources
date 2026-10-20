# Airfoil Angle of Attack

This script draws a NACA 2412 airfoil pitched nose-up about its leading edge to several angles of attack, $0^\circ$, $8^\circ$ and $16^\circ$ by default, relative to a free stream flowing left to right. Each angle gets its own panel with the extended chord line, the angle-of-attack arc and the thin-airfoil lift coefficient $c_l = 2\pi(\alpha - \alpha_{L0})$.

## Overview

- Builds the NACA 4-digit geometry with $m = 0.02$, $p = 0.4$ and $t = 0.12$ (NACA 2412) on a unit chord with 200 stations per surface.
- Offsets the upper and lower surfaces perpendicular to the camber line.
- Rotates the airfoil clockwise about the leading edge by each angle of attack, so the trailing edge drops below the leading edge.
- Draws the free-stream direction, the chord line extended ahead of the nose and an arc between the two marking $\alpha$.
- Prints the thin-airfoil lift coefficient in each panel title, with $\alpha_{L0} = -2.08^\circ$ for NACA 2412.
- Accepts other angles with `--angles`.

## Mathematical Background

### Camber Line

```math
y_c = \begin{cases} \dfrac{m c}{p^2}\left(2p\dfrac{x}{c} - \left(\dfrac{x}{c}\right)^2\right), & x < pc, \\ \dfrac{m c}{(1-p)^2}\left((1-2p) + 2p\dfrac{x}{c} - \left(\dfrac{x}{c}\right)^2\right), & x \geq pc. \end{cases}
```

### Thickness Distribution

```math
y_t = \frac{t}{0.2}\,
c\left(0.2969 \sqrt{\frac{x}{c}} - 0.1260 \frac{x}{c} -
0.3516\left(\frac{x}{c}\right)^{2} + 0.2843\left(\frac{x}{c}\right)^{3} -
0.1015\left(\frac{x}{c}\right)^{4}\right)
```

### Surfaces

With $\theta = \arctan(dy_c/dx)$:

$$
x_u = x - y_t\sin\theta, \quad y_u = y_c + y_t\cos\theta,
\qquad x_l = x + y_t\sin\theta, \quad y_l = y_c - y_t\cos\theta
$$

### Pitching by the Angle of Attack

The free stream flows in the $+x$ direction. A positive angle of attack $\alpha$ is therefore a clockwise rotation about the leading edge at the origin:

```math
\begin{pmatrix}x'\\ y'\end{pmatrix} = \begin{pmatrix}\cos\alpha & \sin\alpha\\ -\sin\alpha & \cos\alpha\end{pmatrix}\begin{pmatrix}x\\ y\end{pmatrix}
```

This moves the trailing edge to $`(c\cos\alpha,\, -c\sin\alpha)`$.

### Lift Estimate

Thin-airfoil theory gives $c_l = 2\pi(\alpha - \alpha_{L0})$ with $\alpha$ in radians; the zero-lift angle of NACA 2412 is $-2.08^\circ$ (computed in [Thin-Airfoil Theory, Panel Method and Drag Polar](../../algorithms/airplane_thin_airfoil_and_polar/)). The theory has no viscosity and does not predict stall: a real NACA 2412 at Reynolds numbers of a few million stalls at about $16^\circ$ with $c_{l,max}$ near 1.6–1.7, so the value printed at $16^\circ$ is an upper bound.

## Implementation

- `naca4_airfoil(m, p, t, c, n)` returns the upper and lower surface coordinates.
- `pitch_airfoil(x, y, angle_of_attack)` applies the clockwise rotation above.
- `plot_multiple_airfoils(angles_of_attack)` draws one panel per angle with the airfoil, free-stream arrows, extended chord line, angle arc and lift estimate.
- `MAX_CAMBER`, `CAMBER_POSITION`, `THICKNESS`, `CHORD`, `N_POINTS`, `DEFAULT_ANGLES` and `ALPHA_ZERO_LIFT` hold the parameters.

## Usage

```bash
python main.py                            # 0, 8 and 16 degrees
python main.py --angles 2 5 10 15         # any list of angles in degrees
python main.py --no-show --output .       # save the figure as a PNG in the current directory
```

## Output

![NACA 2412 at 0, 8 and 16 degrees angle of attack](airfoil_angle_attack.png)

The angle of attack is measured between the free stream and the chord line, not the camber line, which is why the cambered section already has $c_l = 0.23$ at $\alpha = 0^\circ$. The thin-airfoil values rise to 1.11 at $8^\circ$ and 1.98 at $16^\circ$.

## Related Notes

- [Airfoil Design](../../../notes/applied_mechanics/transportation/airplanes/airfoil_design.md)
- [How Airplanes Work](../../../notes/applied_mechanics/transportation/airplanes/how_airplanes_work.md)
