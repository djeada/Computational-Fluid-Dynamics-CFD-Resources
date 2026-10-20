# Thin-Airfoil Theory, Panel Method and Drag Polar

This script computes the lift of a NACA 4-digit airfoil with thin-airfoil theory and with a Hess–Smith panel method, then turns the section result into a finite-wing lift curve, a parabolic drag polar and the power-required curve of a light aircraft. Thin-airfoil theory gives the zero-lift angle, the lift slope $2\pi$ and the quarter-chord moment from integrals of the camber-line slope; the panel method solves the inviscid flow around the real, thick section and gives its surface pressure distribution, so the two can be compared directly.

## Overview

- Integrates the NACA 2412 camber-line slope (or any `--naca` code) to obtain $\alpha_{L0}$, the Fourier coefficients $A_0, A_1, \dots$, $c_l$, $c_{m,c/4}$ and the chordwise load $\Delta C_p(x)$.
- Discretizes the closed-trailing-edge section into 160 cosine-spaced panels and solves for constant source strengths on each panel plus one uniform vortex strength, with the Kutta condition at the trailing edge.
- Computes $C_p$ on both surfaces at $\alpha = 4^\circ$, $c_l$ by pressure integration and by Kutta–Joukowski, and $c_{m,c/4}$.
- Sweeps $\alpha$ from $-6^\circ$ to $12^\circ$ with the panel method and compares the lift curve with $2\pi(\alpha - \alpha_{L0})$ and with the finite-wing slope $a/(1 + a/(\pi e AR))$.
- Builds the drag polar $C_D = C_{D0} + kC_L^2$ of a 1100 kg aircraft with $S = 16.2$ m², $b = 11.0$ m, $e = 0.80$, $C_{D0} = 0.027$, marks $(L/D)_{max}$, and plots the power $DV$ required for level flight at sea level.

## Mathematical Background

### Thin-Airfoil Theory

With $x = \tfrac{c}{2}(1 - \cos\theta)$ and camber line $z(x)$, the vortex sheet that makes the camber line a streamline gives

```math
\alpha_{L0} = -\frac{1}{\pi}\int_0^\pi \frac{dz}{dx}(\cos\theta - 1)\,d\theta,
\qquad
A_0 = \alpha - \frac{1}{\pi}\int_0^\pi \frac{dz}{dx}\,d\theta,
\qquad
A_n = \frac{2}{\pi}\int_0^\pi \frac{dz}{dx}\cos n\theta\,d\theta
```

and

```math
c_l = \pi(2A_0 + A_1) = 2\pi(\alpha - \alpha_{L0}),
\qquad
c_{m,c/4} = \frac{\pi}{4}(A_2 - A_1),
\qquad
\Delta C_p = 4\left[A_0\frac{1 + \cos\theta}{\sin\theta} + \sum_{n \ge 1} A_n\sin n\theta\right]
```

The NACA 4-digit camber line has $dz/dx = \tfrac{2m}{p^2}(p - x/c)$ ahead of the maximum-camber station $x = pc$ and $\tfrac{2m}{(1-p)^2}(p - x/c)$ behind it. The slope has a kink at $\theta_p = \arccos(1 - 2p)$, which is passed to `scipy.integrate.quad` as a breakpoint.

### Hess–Smith Panel Method

Each of the $N$ straight panels carries a constant source density $q_j$, and all carry the same vortex density $\gamma$. In the local frame of panel $j$ (length $l_j$), a point at $(x', y')$ at distances $r_1$, $r_2$ from the panel ends, which subtends the angle $\beta$, receives

```math
u'_s = \frac{q}{2\pi}\ln\frac{r_1}{r_2}, \quad v'_s = \frac{q}{2\pi}\beta,
\qquad
u'_v = -\frac{\gamma}{2\pi}\beta, \quad v'_v = \frac{\gamma}{2\pi}\ln\frac{r_1}{r_2}
```

with $\beta = \pi$ at a panel's own midpoint. Zero normal velocity at the $N$ midpoints and equal tangential speeds on the two trailing-edge panels (the Kutta condition) give $N + 1$ linear equations. The surface pressure is $C_p = 1 - (V_t/V_\infty)^2$, and the clockwise circulation $\Gamma = -\gamma\sum_j l_j$ gives $c_l = 2\Gamma/(V_\infty c)$ by Kutta–Joukowski.

### Finite Wing, Polar and Power

```math
a_{3D} = \frac{a}{1 + a/(\pi e AR)},
\qquad
C_D = C_{D0} + kC_L^2, \quad k = \frac{1}{\pi e AR},
\qquad
\left(\frac{L}{D}\right)_{max} = \frac{1}{2\sqrt{C_{D0}k}} \text{ at } C_L^* = \sqrt{C_{D0}/k}
```

In level flight $C_L = 2W/(\rho V^2 S)$ and the power required is $P = DV$. It is smallest at $C_L = \sqrt{3C_{D0}/k}$, at a speed $3^{-1/4} = 0.760$ times the minimum-drag speed.

## Implementation

- `parse_naca4`, `camber_line` and `camber_slope` define the section; `naca4_panels(code, n_panels)` returns the panel end points clockwise from the lower trailing edge, with the closed-trailing-edge coefficient $-0.1036$.
- `zero_lift_angle`, `fourier_coefficients`, `thin_airfoil_coefficients` and `thin_airfoil_loading` implement thin-airfoil theory.
- `panel_influence(xs, ys)` builds the source and vortex influence coefficients; `solve_panels(xs, ys, alpha)` solves the system and returns $C_p$, $c_l$ (pressure and Kutta–Joukowski), $c_{m,c/4}$, the circulation and the net source strength, which is zero for a closed body.
- `finite_wing_slope`, `induced_drag_factor`, `drag_polar`, `max_lift_to_drag`, `level_flight_speed` and `power_required` give the wing and aircraft results.
- `plot_pressure` and `plot_lift_and_polar` draw the two figures. Constants `N_PANELS`, `ALPHA_CP`, `ALPHA_RANGE`, `MASS`, `WING_AREA`, `SPAN`, `OSWALD`, `CD0` and `CL_MAX` hold the inputs.

## Usage

```bash
python main.py                          # NACA 2412, print the results and show both figures
python main.py --naca 4412              # any 4-digit section
python main.py --no-show --output .     # save the PNGs in the current directory
```

## Output

For NACA 2412 the script prints:

| Quantity | Thin-airfoil theory | Panel method |
| --- | --- | --- |
| $\alpha_{L0}$ | $-2.077^\circ$ | $-2.121^\circ$ |
| $dc_l/d\alpha$ | $2\pi = 6.283$ per rad | 6.872 per rad |
| $c_l$ at $4^\circ$ | 0.666 | 0.737 (Kutta–Joukowski 0.743) |
| $c_{m,c/4}$ | $-0.0531$ | $-0.0598$ |

The 12% thickness raises the inviscid lift slope by 9.4%, close to the empirical $`1 + 0.77\,t/c`$; the boundary layer in a real flow lowers it again, and measured slopes of 12% sections are close to 0.1 per degree (about 6 per radian). For the aircraft, $AR = 7.47$ gives $a_{3D} = 4.71$ per rad, $k = 0.0533$, $`(L/D)_{max} = 13.2`$ at $`C_L^* = 0.71`$, a minimum drag of 818 N at 39.1 m/s, a minimum power of 28.1 kW at 29.7 m/s and a stall speed of 26.1 m/s with $`C_{L,max} = 1.6`$.

![Panel-method pressure distribution on NACA 2412](airplane_airfoil_pressure.png)

Panel (a) shows the suction peak just behind the leading edge on the upper surface and the nearly uniform small positive pressure on the lower surface. Panel (b) compares the load $\Delta C_p$ with thin-airfoil theory: theory has an integrable $1/\sqrt{x}$ singularity at the nose, which the round leading edge of the real section removes, and the thick section carries a slightly larger load everywhere.

![Lift curves, drag polar and power required](airplane_lift_curve_and_polar.png)

Panel (a) shows that both section models cross zero lift near $-2.1^\circ$ while the finite wing has a much lower slope. In panel (b) the tangent from the origin touches the polar at $(L/D)_{max}$, where induced drag equals the zero-lift drag. Panel (c) shows the power-required minimum between the stall speed and the minimum-drag speed.

## Related Notes

- [How Airplanes Work](../../../notes/applied_mechanics/transportation/airplanes/how_airplanes_work.md)
- [Airfoil Design](../../../notes/applied_mechanics/transportation/airplanes/airfoil_design.md)
- [Reading Airfoil Polars with Airfoil Tools](../../../notes/applied_mechanics/transportation/airplanes/airfoil_tools_walkthrough.md)
- [Potential Flow](../../../notes/fluid_mechanics/inviscid_flow/potential_flow.md)
