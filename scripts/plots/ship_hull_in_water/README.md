# Ship Hull in Water

This script draws a side-view sketch of a ship hull sitting in a sinusoidal free-surface wave and annotates it with the Froude number $Fr = U/\sqrt{gL}$. The wavelength of the drawn wave is linked to the ship speed through the deep-water dispersion relation, so the figure also reports the speed and Froude number that the sketch corresponds to.

## Overview

- Draws a stylised hull profile (side view, bow at $x = 0$, stern at $x = L = 10$ m, draught 0.7 m) as a filled polygon.
- Draws a free-surface wave $\eta(x) = A \sin(2\pi x/\lambda)$ with $A = 0.1$ m and $\lambda = 4$ m, extended 2 m beyond each end of the hull, and a dashed still-water line.
- Draws an arrow labelled "Velocity U" for the oncoming flow in the ship's frame of reference.
- Writes the Froude number formula above the hull.
- Computes the ship speed whose transverse waves have wavelength $\lambda$, and the resulting Froude number, and writes them below the hull ($U \approx 2.50$ m/s, $Fr \approx 0.25$).

## Mathematical Background

### Free-Surface Wave Profile

$$
\eta(x) = A\sin\left(\frac{2\pi x}{\lambda}\right)
$$

### Froude Number

$$
Fr = \frac{U}{\sqrt{gL}}
$$

where $U$ is the ship speed, $g$ the gravitational acceleration and $L$ the waterline length. $Fr$ compares inertia with gravity and governs the wave pattern and wave-making resistance of a hull; model tests of ships are run at the same Froude number as the full-scale vessel.

### Wavelength of Ship Waves

A deep-water gravity wave of wavelength $\lambda$ travels at phase speed $c = \sqrt{g\lambda/2\pi}$. The transverse waves of a ship are steady relative to the hull, so they travel at the ship speed, $c = U$. Therefore

```math
U = \sqrt{\frac{g\lambda}{2\pi}},
\qquad \frac{\lambda}{L} = 2\pi\, Fr^2
```

With $\lambda = 4$ m and $L = 10$ m this gives $U = 2.50$ m/s and $Fr = 0.25$. When $\lambda = L$ ($Fr = 1/\sqrt{2\pi} \approx 0.40$, the classical "hull speed") the bow and stern waves reinforce each other and wave-making resistance rises steeply.

## Implementation

- Constants: `G` (m/s$`^2`$), `HULL_LENGTH` (m), `WAVE_LENGTH` (m) and `WAVE_AMPLITUDE` (m).
- `ship_speed_from_wavelength(wavelength, g)` returns $\sqrt{g\lambda/2\pi}$.
- `froude_number(speed, length, g)` returns $U/\sqrt{gL}$.
- `draw_ship_hull_and_waves(hull_length, wavelength, amplitude)` plots the wave, fills the hull polygon (scaled to `hull_length`), draws the velocity arrow, still-water line and annotations, and returns the figure. The axes use equal scaling.
- `main(argv=None)` parses the flags, saves the figure if requested, and shows it.

## Usage

```bash
python main.py                      # open the figure in a window
python main.py --no-show --output . # save ship_hull_in_water.png without opening a window
```

| Flag | Description |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure there as a PNG |

## Output

A side view of the hull below the still-water line, the sinusoidal free surface, the flow arrow, the Froude number formula, and the computed speed and Froude number for the drawn wavelength. The sketch is qualitative: the wave is drawn everywhere, including ahead of the bow, whereas a real ship's waves trail behind it.

![Ship hull in water](ship_hull_in_water.png)

## Related Notes

- [Dimensionless Numbers](../../../notes/fluid_mechanics/dimensions.md)
- [Fluid Loading](../../../notes/applied_mechanics/fluid_loading/intro.md)
- [Wave Loading](../../../notes/applied_mechanics/fluid_loading/wave_loading.md)
- [Drag](../../../notes/fluid_mechanics/viscous_flow/drag.md)
