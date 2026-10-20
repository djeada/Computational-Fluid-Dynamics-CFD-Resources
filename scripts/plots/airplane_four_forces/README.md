# Forces on an Aircraft in a Steady Climb

This script draws the free-body diagram of a 1100 kg light aircraft in a steady climb, with lift, drag, weight and thrust computed from the equilibrium conditions and drawn to scale, and checks that the four forces close into a polygon. It makes visible two facts that are easy to get wrong: in a climb the lift is slightly less than the weight, and thrust and drag are an order of magnitude smaller than lift and weight.

## Overview

- Takes the aircraft of the other airplane scripts ($m = 1100$ kg, $S = 16.2$ m², $b = 11.0$ m, $e = 0.80$, $C_{D0} = 0.027$) at $V = 40$ m/s on a flight path inclined at $\gamma = 6^\circ$, at sea level.
- Computes $L = W\cos\gamma$, $C_L$, $C_D$ from the parabolic polar, $D$ and $T = D + W\sin\gamma$, with thrust along the flight path.
- Draws the four forces on a side view of the aircraft with one length scale for all of them.
- Adds the vectors head to tail in a second panel and reports the closure error of the polygon.

## Mathematical Background

For steady, unaccelerated flight on a straight path inclined at $\gamma$, with thrust along the path, the force balances along and normal to the path are

$$
T - D - W\sin\gamma = 0,
\qquad L - W\cos\gamma = 0
$$

and the aerodynamic forces follow from

```math
C_L = \frac{W\cos\gamma}{\tfrac{1}{2}\rho V^2 S},
\qquad
C_D = C_{D0} + \frac{C_L^2}{\pi e AR},
\qquad
D = \tfrac{1}{2}\rho V^2 S C_D
```

Multiplying the first balance by $V$ gives the rate of climb $V\sin\gamma = (T - D)V/W$, the excess power divided by the weight.

## Implementation

- `climb_forces(speed, gamma_deg)` returns $L$, $D$, $W$, $T$, $C_L$, $C_D$, the rate of climb and the excess power.
- `draw_aircraft(ax, pitch)` draws a fuselage, wing and tail with matplotlib patches, rotated to the flight-path angle.
- `plot_forces(f)` draws the free-body diagram and the force polygon; `_arrow` draws one labelled force.
- Constants `RHO`, `G`, `MASS`, `WING_AREA`, `SPAN`, `OSWALD`, `CD0`, `SPEED` and `CLIMB_ANGLE` hold the inputs.

## Usage

```bash
python main.py                          # print the forces and show the figure
python main.py --no-show --output .     # save the PNG in the current directory
```

## Output

The script prints $C_L = 0.676$, $C_D = 0.0513$, $L/D = 13.2$, $`W = 10\,791`$ N, $`L = 10\,732`$ N, $D = 815$ N and $T = 1943$ N, a rate of climb of 4.18 m/s and an excess power of 45.1 kW. The polygon closes to $10^{-12}$ N.

![Free-body diagram of a climbing aircraft and its force polygon](airplane_four_forces.png)

In panel (a) the lift is tilted back from the vertical by $\gamma$ and is 59 N smaller than the weight; the climb comes from the thrust exceeding the drag by $W\sin\gamma = 1128$ N. Panel (b) shows the same four vectors added head to tail, returning to the starting point.

## Related Notes

- [How Airplanes Fly](../../../notes/applied_mechanics/transportation/airplanes/how_airplanes_work.md)
