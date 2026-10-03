# Wall Shear in Pipe Cross-Section

This script sketches fully developed laminar (Hagen-Poiseuille) flow in a circular pipe, with velocity arrows whose lengths follow the parabolic profile $u(r) = u_{max}(1 - (r/R)^2)$. Labels mark the no-slip condition at the wall, the high-shear region at the wall, the velocity gradient and the maximum velocity on the centreline.

## Overview

- Draws the pipe as a grey circle of radius $R = 1$.
- Draws velocity arrows at 5 evenly spaced radii $r = 0, R/4, R/2, 3R/4, R$, on both sides of the centreline, with length proportional to $u(r)$ ($u_{max} = 2$). At the wall, where $u = 0$, a dot replaces the arrow.
- Draws the parabola through the arrow tips as a dashed line.
- Labels the maximum velocity at $r = 0$, the velocity gradient $du/dr$, the no-slip condition ($u = 0$) at the wall, and the high-shear region at the wall.
- The velocity is along the pipe axis, perpendicular to the cross-section; the arrows are drawn in the plane of the figure for illustration.

## Mathematical Background

### Hagen-Poiseuille Velocity Profile

For fully developed, incompressible laminar flow driven by a pressure drop $\Delta p$ over a length $L$, the axial velocity at radius $r$ is

$$
u(r) = \frac{\Delta p}{4\mu L}(R^2 - r^2)
$$

where $\mu$ is the dynamic viscosity and $R$ the pipe radius.

### Maximum Velocity

The velocity is largest on the centreline ($r = 0$):

$$
u_{max} = \frac{\Delta p\, R^2}{4\mu L}
$$

so the profile can be written as $u(r) = u_{max}\left(1 - (r/R)^2\right)$, which is the form the script uses.

### Wall Shear Stress

The velocity gradient $du/dr = -2u_{max}r/R^2$ is zero on the centreline and steepest at the wall, so the shear stress is largest there:

$$
\tau_w = -\mu
\frac{du}{dr}\bigg|_{r=R} = \frac{2\mu u_{max}}{R} = \frac{\Delta p\, R}{2L}
$$

### No-Slip Condition

$$
u(R) = 0
$$

## Implementation

- `ARROW_SCALE`: plot length per unit velocity.
- `poiseuille_velocity(r, pipe_radius, max_velocity)` returns $u(r)$.
- `plot_wall_shear(pipe_radius=1, max_velocity=2, n_radii=5)` draws the circle, the arrows (`ax.arrow` with `length_includes_head=True`, so arrow length is proportional to $u$), the dashed profile, and the text annotations, with the axes hidden. Returns the figure.
- `main(argv=None)` parses the flags, saves the figure if requested, and shows it.

## Usage

```bash
python main.py                      # open the figure in a window
python main.py --no-show --output . # save wall_shear_pipe_cross_section.png without opening a window
```

| Flag | Description |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure there as a PNG |

## Output

The pipe section with parabolic velocity arrows, longest on the centreline and shrinking to zero at the wall, the dashed profile through their tips, and labels for the no-slip wall, the high-shear wall region and the centreline maximum.

![Wall shear in pipe cross-section](wall_shear_pipe_cross_section.png)

## Related Notes

- [Pipe Flow](../../../notes/fluid_mechanics/internal_flow/pipes.md)
- [Viscosity](../../../notes/fluid_mechanics/fluid_properties/viscosity.md)
- [Navier-Stokes Equations](../../../notes/fluid_mechanics/governing_equations/navier_stokes.md)
