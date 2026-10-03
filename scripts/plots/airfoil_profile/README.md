# NACA 4-Digit Airfoil Profile

This script draws an annotated NACA 4-digit airfoil profile (NACA 4412 by default) from its four-digit designation, labelling the leading edge, trailing edge, chord line and mean camber line. It computes the piecewise parabolic camber line and the standard NACA thickness distribution, and offsets the surfaces perpendicular to the camber line.

## Overview

- Parses a four-digit code (`--naca`, default `4412`) into maximum camber $m$, camber position $p$ and thickness ratio $t$.
- Evaluates the camber line $y_c(x)$ and its slope at 500 chordwise stations on a unit chord.
- Applies the NACA thickness distribution and offsets the surfaces perpendicular to the camber line.
- Draws the upper and lower surfaces, the chord line and the dashed mean camber line.
- Adds text labels for the leading edge, trailing edge, chord line, mean camber line and both surfaces.
- Uses equal axis scaling with the axes hidden.
- Handles symmetric sections such as `0012` (zero camber).

## Mathematical Background

For code `MPXX`: $m = M/100$, $p = P/10$ and $t = XX/100$.

### Camber Line

$$
y_c = \begin{cases} \dfrac{m c}{p^2}\left(2p\dfrac{x}{c} - \left(\dfrac{x}{c}\right)^2\right), & x < pc, \\ \dfrac{m c}{(1-p)^2}\left((1-2p) + 2p\dfrac{x}{c} - \left(\dfrac{x}{c}\right)^2\right), & x \geq pc, \end{cases}
$$

with slope

$$
\frac{dy_c}{dx} = \begin{cases} \dfrac{2m}{p^2}\left(p - \dfrac{x}{c}\right), & x < pc, \\ \dfrac{2m}{(1-p)^2}\left(p - \dfrac{x}{c}\right), & x \geq pc. \end{cases}
$$

### Thickness Distribution

$$
y_t = \frac{t}{0.2}\,
c\left(0.2969 \sqrt{\frac{x}{c}} - 0.1260 \frac{x}{c} -
0.3516\left(\frac{x}{c}\right)^2 + 0.2843\left(\frac{x}{c}\right)^3 -
0.1015\left(\frac{x}{c}\right)^4\right)
$$

With these coefficients the trailing edge has a small finite thickness.

### Upper and Lower Surfaces

With $\theta = \arctan(dy_c/dx)$:

$$
x_u = x - y_t\sin\theta,
\qquad y_u = y_c + y_t\cos\theta
$$

$$
x_l = x + y_t\sin\theta,
\qquad y_l = y_c - y_t\cos\theta
$$

## Implementation

- `parse_naca4(code)` returns `(m, p, t)`.
- `camber_line(x, m, p, c)` returns $y_c$ and $dy_c/dx$, both zero for symmetric sections.
- `thickness_distribution(x, t, c)` returns $y_t$.
- `naca4_geometry(code, c, n)` combines these into the camber line and the surface coordinates.
- `plot_airfoil(code, c, n)` draws and labels the profile.
- `DEFAULT_CODE`, `CHORD` and `N_POINTS` set the defaults.

## Usage

```bash
python main.py                          # NACA 4412
python main.py --naca 0012              # any 4-digit code
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Annotated NACA 4412 airfoil profile](airfoil_profile.png)

The figure shows the 12 %-thick NACA 4412 section. The surfaces are gray, the chord line is yellow and the mean camber line is dashed red, reaching its maximum of 4 % of the chord at 40 % chord. Text boxes label the leading and trailing edges, the chord line and the camber line.

## Related Notes

- [Airfoil Design](../../../notes/applied_mechanics/transportation/airplanes/airfoil_design.md)
- [Airfoil Tools Walkthrough](../../../notes/applied_mechanics/transportation/airplanes/airfoil_tools_walkthrough.md)
