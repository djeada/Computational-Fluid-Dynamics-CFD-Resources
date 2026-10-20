# Reading Airfoil Polars with Airfoil Tools

Airfoil Tools (airfoiltools.com) is a free website that combines a large airfoil coordinate database with precomputed XFOIL polars, a comparison page and a few small calculators. It is a quick way to shortlist sections for a wing, a propeller, a model aircraft or a wind-turbine blade before running one's own XFOIL or CFD analyses. This note describes what the site provides, how to read the five polar plots it shows, where the numbers come from and where they stop being trustworthy. The airfoil geometry and aerodynamics behind the plots are in [Airfoil Design](airfoil_design.md).

## Problem Statement

Given the operating conditions of a lifting surface (chord $c$, speed range $V$, air properties $\rho$ and $\mu$, hence the Reynolds number $Re = \rho Vc/\mu$), a design lift coefficient or range of lift coefficients, and constraints such as minimum thickness, pitching-moment limits and stall behaviour, select a section whose two-dimensional polar gives low drag (or high $c_l/c_d$) over the operating range and acceptable $c_{l,max}$ and $c_m$.

The data used are steady, two-dimensional, incompressible ($M = 0$) section polars computed by XFOIL with free transition, at a few fixed Reynolds numbers. The result is a shortlist, to be confirmed by analyses at the actual $Re$ and $M$, by three-dimensional wing analysis and, for a new design, by wind-tunnel or flight tests.

## What the Site Provides

| Tool | What it does |
| --- | --- |
| Airfoil database search | more than a thousand sections, most taken from the UIUC Airfoil Coordinates Database, searchable by name and filterable by thickness and camber |
| Airfoil details page | coordinates (downloadable as a text file), a plot of the shape, maximum thickness and camber with their positions, and the XFOIL polars with a summary table of the maximum $c_l/c_d$ and the angle at which it occurs |
| Lift/drag polars | the polar data behind the plots, one file per Reynolds number and transition setting |
| Airfoil comparison | overlays the shapes and the polars of several sections from the database or from coordinates the user adds |
| Airfoil plotter | prints the section at a chosen chord as a full-size or paginated template, or exports it as PDF or SVG |
| NACA 4- and 5-digit generators | produce coordinates for any section of these families from its parameters |
| Reynolds number calculator | $Re$ from speed, chord and air properties |

![Airfoil Tools comparison page with NACA 0012-64 and Clark Y](https://github.com/user-attachments/assets/5d3a76f7-d64b-4ecc-a954-b6e773e7fb25)

The comparison page above overlays a NACA 0012-64 (a 12% symmetric section with maximum thickness at 40% chord) and the Clark Y (11.7% thick, 3.4% camber, almost flat lower surface). Each database entry has an identifier ending in `-il`, the suffix for sections taken from the Illinois (UIUC) collection.

## Where the Numbers Come From

XFOIL (Drela, 1989) couples a linear-vorticity panel method for the inviscid flow with an integral boundary-layer formulation, iterated until the boundary layer and the inviscid flow agree. Transition is predicted with the $e^N$ method: the boundary layer becomes turbulent where the amplification of the most unstable Tollmien–Schlichting waves reaches $e^{N_{crit}}$. The polars on the site are computed for:

- Reynolds numbers of 50 000, 100 000, 200 000, 500 000 and 1 000 000;
- $N_{crit} = 9$, the standard value for an average wind tunnel, and $N_{crit} = 5$, which models a disturbed free stream or a rougher surface and moves transition forward;
- $M = 0$ and free transition on both surfaces.

The Reynolds numbers cover model aircraft, UAVs, small wind turbines and the outboard wings of sailplanes. A light aircraft ($Re \approx 3$–$`6 \times 10^6`$) or an airliner ($Re \approx 3 \times 10^7$) is beyond the highest polar, and its section data should come from wind-tunnel collections such as Abbott and von Doenhoff or from one's own XFOIL or RANS runs ([The Reynolds Number in Flight](reynolds_number.md)).

## Reading a Polar

![XFOIL polars of two sections at two Reynolds numbers from the comparison page](https://github.com/user-attachments/assets/79160ccf-b985-4421-810d-0827287dd801)

The site shows five plots per set of polars. The image above shows them for the two sections of the comparison, each at a low and a high Reynolds number (four curves).

| Plot | What to read from it |
| --- | --- |
| $c_l$ against $c_d$ | the drag polar: the drag paid for each lift coefficient. The line from the origin tangent to the curve touches it at the maximum $c_l/c_d$. Laminar sections show a "drag bucket", a range of $c_l$ with low, nearly constant drag |
| $c_l$ against $\alpha$ | the lift curve: slope close to 0.1 per degree in attached flow, the zero-lift angle (negative for cambered sections), $c_{l,max}$ and the stall angle. Kinks and plateaus at low $Re$ are laminar separation bubbles |
| $c_l/c_d$ against $\alpha$ | section efficiency: the angle of best $c_l/c_d$ and how sharp the peak is. A broad peak keeps the efficiency over a range of flight speeds |
| $c_d$ against $\alpha$ | where the drag rises towards stall; the width of the low-drag range |
| $c_m$ against $\alpha$ | the pitching moment about the quarter chord: near zero for symmetric sections, negative and roughly constant for cambered ones in attached flow; a rapid change marks separation |

Reading the low- and high-$`Re`$ curves together shows the effects described in [Airfoil Design](airfoil_design.md#reynolds-number-effects): at the lower Reynolds number the drag is higher, $c_l/c_d$ is much lower, the lift curve has kinks from separation bubbles and stall comes earlier.

## Limits of XFOIL Data

XFOIL agrees well with wind-tunnel measurements in attached flow at moderate Reynolds numbers, which is why it is the standard tool for section design. Its polars should still be read with the following limits in mind:

1. They are two-dimensional. A wing has induced drag $C_L^2/(\pi e AR)$ in addition to the section drag, often larger than it, so a section $c_l/c_d$ of 100 does not mean an aircraft $L/D$ of 100 (Exercise 2).
2. Stall and post-stall values are unreliable. Integral boundary-layer methods handle massive separation poorly, and XFOIL usually overpredicts $c_{l,max}$; points past the stall may be missing where the iteration did not converge.
3. Transition depends on $N_{crit}$. Comparing the $N_{crit} = 9$ and $N_{crit} = 5$ polars shows how sensitive a section is to turbulence and roughness; a laminar section whose low drag disappears at $N_{crit} = 5$ will lose it on a dirty wing.
4. Below about $Re = 10^5$ the results depend strongly on the modelling of separation bubbles and should be checked against measurements such as the UIUC low-speed tests (Selig et al., 1995).
5. The data are incompressible. Above about $M = 0.3$ compressibility raises the suction peaks and, at transonic speeds, causes shocks and drag divergence that XFOIL at $M = 0$ cannot show.
6. Fixed Reynolds numbers. Real wings work at a continuum of $Re$ along the span and over the speed range, so interpolation between polars is needed, and it is least reliable at low $Re$ where the curves change quickly.

## Selecting a Section

1. Compute the Reynolds number range of the wing from its chord (root and tip) and its speed range, using the calculator or $Re = Vc/\nu$.
2. Compute the design lift coefficients: $C_L = 2W/(\rho V^2S)$ at cruise, at climb and near the minimum speed.
3. Shortlist sections in the database by thickness (structure, fuel, spar depth) and camber (design $c_l$).
4. Compare the shortlisted polars at the nearest Reynolds numbers: drag at the cruise $c_l$, width of the low-drag range, $c_{l,max}$, stall character, $c_m$ (tail trim drag) and sensitivity to $N_{crit}$.
5. Download the coordinates of the best candidates, run XFOIL or a 2D RANS analysis at the actual Reynolds and Mach numbers, and include the induced drag of the wing before judging the aircraft performance.

### Commonly Used Sections

| Section | Character | Typical use |
| --- | --- | --- |
| NACA 0012 | symmetric, 12% thick | tail surfaces, aerobatic aircraft, rotor-blade studies, CFD validation |
| NACA 2412 | 2% camber, 12% thick, gentle trailing-edge stall | general-aviation wings |
| NACA 4412 | 4% camber, 12% thick, higher $c_{l,max}$ and nose-down moment | slow aircraft, wind-tunnel and CFD test case |
| NACA 23012 | five-digit, forward camber, high $c_{l,max}$, small moment, sharper stall | light aircraft and older transports |
| Clark Y | 11.7% thick, flat lower surface | historic aircraft, models (easy to build on a flat board) |
| NACA $63_2$-415 and other six-series | shaped for extended laminar flow and a drag bucket | laminar-flow wings, wind-turbine blades |
| Eppler, Selig, Wortmann families | designed for low Reynolds numbers | sailplanes, model aircraft, UAVs |

## Related Scripts

- [NACA 4-Digit Airfoil Profile](../../../../scripts/plots/airfoil_profile/): draws an annotated NACA 4-digit airfoil profile (NACA 4412 by default) from its four-digit designation, marking the chord line, the mean camber line, the maximum camber and thickness and the leading-edge radius, and compares it with sections of different camber and thickness.
- [Thin-Airfoil Theory, Panel Method and Drag Polar](../../../../scripts/algorithms/airplane_thin_airfoil_and_polar/): computes the lift of a NACA 4-digit airfoil with thin-airfoil theory and with a Hess–Smith panel method, then turns the section result into a finite-wing lift curve, a parabolic drag polar and the power-required curve of a light aircraft.
- [Reynolds Numbers of Flyers](../../../../scripts/plots/airplane_reynolds_number_scale/): computes the chord Reynolds number $Re_c = Vc/\nu$ of fourteen flyers, from a fruit fly to an airliner at cruise, and draws them on one logarithmic axis next to the flat-plate skin-friction laws for laminar, turbulent and transitional boundary layers.

## Exercises

**Exercise 1.** Which of the site's polars should you look at for (a) a full-size glider wing with a 0.9 m chord flying at 25 m/s, and (b) a model glider with a 0.2 m chord flying at 10 m/s? Use sea-level air: $\rho = 1.225$ kg/m³, $\mu = 1.81 \times 10^{-5}$ Pa s.

<details>
<summary>Answer</summary>

(a) $Re = 1.225 \times 25 \times 0.9/1.81 \times 10^{-5} = 1.52 \times 10^6$. Use the 1 000 000 polar, remembering that drag at the real Reynolds number will be somewhat lower and $c_{l,max}$ somewhat higher.

(b) $Re = 1.225 \times 10 \times 0.2/1.81 \times 10^{-5} = 1.35 \times 10^5$. Look at both the 100 000 and 200 000 polars to bracket it. Section behaviour changes quickly with $Re$ in this range, so interpolation is less reliable.

</details>

**Exercise 2.** A section polar shows $c_l = 0.8$ with $c_d = 0.008$, i.e. $c_l/c_d = 100$. The section is used on a wing with $AR = 20$ and $e = 0.9$. Estimate the wing's lift-to-drag ratio, ignoring fuselage and tail drag.

<details>
<summary>Answer</summary>

```math
C_{D_i} = \frac{C_L^2}{\pi e AR} = \frac{0.64}{\pi \times 0.9 \times 20} = 0.0113
```

$C_D \approx 0.008 + 0.0113 = 0.0193$, so $L/D \approx 0.8/0.0193 = 41$.

The induced drag is larger than the section drag even on this slender wing. Section $c_l/c_d$ ranks airfoils but greatly overstates the lift-to-drag ratio of the aircraft.

</details>

**Exercise 3.** Decode the designations NACA 0012, 2412 and 4412. Then explain why the NACA 0012 is a poor choice for a supersonic aircraft even though it is symmetric.

<details>
<summary>Answer</summary>

- NACA 0012: no camber, 12% thick.
- NACA 2412: 2% camber at 40% chord, 12% thick.
- NACA 4412: 4% camber at 40% chord, 12% thick.

At supersonic speed the wave drag of a thin section grows with the square of the thickness ratio, and a blunt, round leading edge produces a detached bow shock. Supersonic wings therefore use much thinner sections (a few percent thick) with sharp or small-radius leading edges. A 12% section with a round nose suits low-speed aerobatic aircraft, rotors and tail surfaces.

</details>

**Exercise 4.** Comparing the 50 000 and 1 000 000 polars of almost any section shows much lower $c_l/c_d$ at the lower Reynolds number. Explain the physical reason, and name two design responses for aircraft that must fly at low Reynolds numbers.

<details>
<summary>Answer</summary>

At low Reynolds numbers the boundary layer stays laminar over much of the surface. A laminar boundary layer separates easily in the adverse pressure gradient behind the suction peak and often forms a laminar separation bubble, which thickens the wake, raises drag and makes the lift curve non-linear. Skin-friction coefficients are also higher at low $Re$ ($c_f \propto Re^{-1/2}$ for laminar flow).

Design responses:

- Use sections designed for low $Re$, thin and with carefully shaped pressure recovery (Eppler and Selig families).
- Trip the boundary layer to turbulence ahead of the laminar separation point with turbulator tape or zig-zag strips.

</details>

**Exercise 5.** A sailplane has a best glide ratio $L/D = 40$. How far can it glide in still air from 1000 m? Does a heavier sailplane with the same $L/D$ glide farther?

<details>
<summary>Answer</summary>

In a steady glide the glide ratio equals $L/D$, so the distance is $40 \times 1000$ m = 40 km.

Weight does not change the maximum $L/D$, only the speed at which it occurs (which scales with $\sqrt{W}$), so a heavier sailplane glides the same distance but faster. That is why racing sailplanes carry water ballast on strong-thermal days.

</details>

## References

- Drela, M., "XFOIL: An analysis and design system for low Reynolds number airfoils", in Mueller, T. J. (ed.), *Low Reynolds Number Aerodynamics*, Lecture Notes in Engineering, vol. 54, Springer, 1989, pp. 1–12.
- Drela, M., and Youngren, H., *XFOIL 6.9 User Primer*, MIT Department of Aeronautics and Astronautics, 2001.
- Selig, M. S., Guglielmo, J. J., Broeren, A. P., and Giguère, P., *Summary of Low-Speed Airfoil Data*, Vol. 1, SoarTech Publications, 1995.
- Abbott, I. H., and von Doenhoff, A. E., *Theory of Wing Sections: Including a Summary of Airfoil Data*, Dover, 1959.
- Anderson, J. D., Jr., *Fundamentals of Aerodynamics*, 6th ed., McGraw-Hill Education, 2017.
