# Laminar vs Turbulent Pipe Flow

This script plots laminar and turbulent radial velocity profiles of pipe flow in side-by-side panels to show how much flatter the turbulent profile is. The laminar profile is the Hagen–Poiseuille parabola and the turbulent profile is the empirical 1/7 power law, with the same centreline velocity. Radius is on the vertical axis, running from the centreline at the top to the wall at the bottom, and velocity is on the horizontal axis.

## Overview

- Evaluates both profiles at 200 radii from the centreline ($r = 0$) to the wall ($r = R = 1$) with $u_{\max} = 2$
- Plots the laminar profile (blue) and turbulent profile (red) in separate panels with shared, inverted radius axes
- Laminar annotations mark the centreline maximum and the no-slip condition at the wall
- Turbulent annotations mark the flat core produced by turbulent mixing and the steep drop to zero at the wall

## Mathematical Background

### Laminar Profile (Hagen–Poiseuille)

For $Re \lesssim 2300$ the fully developed axial velocity is

$$
u(r) = u_{\max}\left[1 - \left(\frac{r}{R}\right)^2\right]
$$

and the mean velocity is half the centreline value, $\bar{u} = u_{\max}/2$.

### Turbulent Profile (1/7 Power Law)

For turbulent flow ($Re \gtrsim 4000$) the time-averaged profile is approximated by

$$
u(r) = u_{\max}\left(1 - \frac{r}{R}\right)^{1/7}
$$

Averaging over the cross-section gives

$$
\frac{\bar{u}}{u_{\max}} = \frac{2}{u_{\max} R^2}\int_0^R u(r)\, r\,
dr = \frac{2n^2}{(n+1)(2n+1)} = \frac{49}{60} \approx 0.817 \quad (n = 7)
$$

so the turbulent profile is much fuller than the parabola. The power law has an infinite slope at the wall, so it does not describe the viscous sublayer.

### Reynolds Number

$$
Re = \frac{\rho\, \bar{u}\, D}{\mu},
\qquad D = 2R
$$

Transition from laminar to turbulent pipe flow typically occurs in the range $2300 < Re < 4000$. The script does not compute $Re$; it just draws one profile of each type.

## Implementation

- `laminar_profile(r, pipe_radius, max_velocity)` and `turbulent_profile(r, pipe_radius, max_velocity)` evaluate the two formulas.
- `plot_laminar_vs_turbulent(pipe_radius, max_velocity)` builds a 1 × 2 figure with `sharex=True, sharey=True`, inverts the shared radius axis, and places the annotations on the curves. It returns the figure.
- Constants: `PIPE_RADIUS = 1`, `MAX_VELOCITY = 2`.
- `main(argv=None)` handles the flags.

## Usage

```bash
python main.py                          # open the figure window
python main.py --no-show --output out   # save laminar_vs_turbulent_pipe.png into out/
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The left panel shows the parabola, falling steadily from $u_{\max}$ on the centreline to zero at the wall. The right panel shows the turbulent profile: still above 90% of $u_{\max}$ halfway to the wall, then dropping sharply to zero in a thin region next to it.

![Laminar vs. turbulent pipe flow profiles](laminar_vs_turbulent_pipe.png)

## Related Notes

- [Pipe Flow](../../../notes/fluid_mechanics/internal_flow/pipes.md)
- [Turbulence Modeling](../../../notes/numerical/cfd/turbulence_modeling.md)
- [Reynolds Number](../../../notes/applied_mechanics/transportation/airplanes/reynolds_number.md)
