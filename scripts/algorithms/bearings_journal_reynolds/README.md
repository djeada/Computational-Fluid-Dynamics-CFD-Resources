# Journal Bearing Reynolds Equation

This script solves the Reynolds equation of a hydrodynamic journal bearing by finite differences and reproduces the classical load-capacity results: the closed-form full-Sommerfeld solution of the long bearing, the effect of film rupture under the Reynolds cavitation condition, and the Raimondi–Boyd design table for a bearing with $L/D = 1$. Cavitation is posed as a linear complementarity problem, $p \ge 0$ with the Reynolds equation holding wherever $p > 0$, and solved by a primal-dual active-set method. The figure shows pressure against angle for several eccentricity ratios, the Sommerfeld number against eccentricity ratio for each model and the 2D pressure field of the finite bearing.

## Overview

- Discretises the non-dimensional Reynolds equation with conservative central differences on a grid of 144 points around the bearing, periodic in angle; the finite bearing adds 41 points across its length with ambient pressure at both ends.
- Holds the pressure at ambient along the line $\theta = 0$ (the position of maximum film thickness), which stands for an axial supply groove.
- Solves the long bearing without cavitation and compares with the full-Sommerfeld closed form.
- Solves the long bearing and the $L/D = 1$ bearing with the Reynolds condition by the active-set method, starting from the unconstrained solution.
- Integrates the pressure for the load components, the Sommerfeld number and the attitude angle at ten eccentricity ratios from 0.1 to 0.97.
- Plots the short-bearing (Ocvirk) formula and the Raimondi–Boyd table for $L/D = 1$ alongside.

## Mathematical Background

### Reynolds Equation

For a film of thickness $h(\theta)$ between a journal of radius $R$ turning at $\omega$ and a stationary bearing, the Reynolds equation (derived in the bearings note) is

$$
\frac{1}{R^2}
\frac{\partial}{\partial\theta}\left(h^3 \frac{\partial p}{\partial\theta}\right) +
\frac{\partial}{\partial z}\left(h^3 \frac{\partial p}{\partial z}\right) = 6\mu\omega
\frac{\partial h}{\partial\theta}
$$

with $h = c(1 + \varepsilon\cos\theta)$, radial clearance $c$, eccentricity ratio $\varepsilon = e/c$ and $\theta$ measured from the point of maximum film thickness in the direction of rotation. With $H = h/c$, $\zeta = z/R$ and $P = p c^2/(\mu\omega R^2)$,

$$
\frac{\partial}{\partial\theta}\left(H^3 \frac{\partial P}{\partial\theta}\right) +
\frac{\partial}{\partial\zeta}\left(H^3 \frac{\partial P}{\partial\zeta}\right) = 6
\frac{\partial H}{\partial\theta}
$$

### Closed-Form Solutions

For the infinitely long bearing ($\partial/\partial\zeta = 0$) with periodic pressure, the full-Sommerfeld solution is

```math
P = \frac{6\varepsilon\sin\theta\,(2 + \varepsilon\cos\theta)}{(2 + \varepsilon^2)(1 + \varepsilon\cos\theta)^2}
```

It is antisymmetric, with as much suction in the diverging half of the film as pressure in the converging half, so the load acts at 90° to the line of centres and the Sommerfeld number is $S = (2 + \varepsilon^2)\sqrt{1 - \varepsilon^2}/(12\pi^2\varepsilon)$. For the short bearing (Ocvirk) the circumferential term is dropped and the negative half discarded, which gives

$$
S\left(\frac{L}{D}\right)^2 = \frac{(1 - \varepsilon^2)^2}{\pi\varepsilon\sqrt{\pi^2(1 - \varepsilon^2) + 16\varepsilon^2}}
$$

### Cavitation as a Complementarity Problem

A liquid film cannot sustain the large suction of the full-Sommerfeld solution; it ruptures near ambient pressure. The Reynolds (Swift–Stieber) condition requires $p = 0$ and $\partial p/\partial n = 0$ at the rupture boundary, whose position is unknown. With $\mathbf{A}$ the matrix of $-\nabla\cdot(H^3\nabla P)$ and $\mathbf{b}$ the discrete $`-6\,\partial H/\partial\theta`$, the discrete problem is

$$
\mathbf{P} \ge 0,
\qquad \mathbf{A}\mathbf{P} - \mathbf{b} \ge 0,
\qquad P_i\left(\mathbf{A}\mathbf{P} - \mathbf{b}\right)_i = 0
$$

The active-set method solves $\mathbf{A}\mathbf{P} = \mathbf{b}$ with $P = 0$ on a trial cavitated set, moves a point out of that set where the multiplier $\mathbf{A}\mathbf{P} - \mathbf{b}$ is negative and into it where $P$ is negative, and stops when the set no longer changes.

### Load and Sommerfeld Number

The load components along and normal to the line of centres are the integrals of $p\cos\theta$ and $p\sin\theta$ over the film. With $W$ the total load, $N = \omega/2\pi$ the speed in rev/s and $P_m = W/(LD)$ the mean pressure,

$$
S = \frac{\mu N}{P_m}\left(\frac{R}{c}\right)^2
$$

and the attitude angle $\phi$ is the angle between the load line and the line of centres. A small $S$ means a heavily loaded or slow bearing running at a large eccentricity.

## Implementation

- `assemble(eps, n_theta, n_axial, l_over_r)` builds the sparse matrix with face values of $H^3$ and the right-hand side; `fix_supply_line` sets $P = 0$ on $\theta = 0$.
- `solve_lcp(a, b)` is the active-set solver, using `scipy.sparse.linalg.spsolve` on the free points at each iteration.
- `solve_long(eps, cavitation)` and `solve_finite(eps, l_over_d)` return pressure profiles and fields.
- `sommerfeld_pressure`, `sommerfeld_number_full` and `sommerfeld_number_short` are the closed forms.
- `load_components` and `sommerfeld_and_attitude` integrate the pressure.
- `RAIMONDI_BOYD_LD1` holds the published values for $L/D = 1$ (Raimondi and Boyd 1958).

## Usage

```bash
python main.py                          # print the table and show the figure
python main.py --no-show --output .     # save bearings_journal_reynolds.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

Without cavitation the finite-difference pressure is within $1.1\times10^{-4}$ of the closed form at $\varepsilon = 0.2$ and within $1.1\times10^{-3}$ at $\varepsilon = 0.8$, relative to the peak pressure; the error falls at second order with the grid. With cavitation the $L/D = 1$ results match the Raimondi–Boyd table to three figures:

| $\varepsilon$ | $S$ computed | $S$ Raimondi–Boyd | $\phi$ computed | $\phi$ Raimondi–Boyd | $S$ short bearing |
| --- | --- | --- | --- | --- | --- |
| 0.1 | 1.331 | 1.33 | 79.4° | 79.5° | 0.990 |
| 0.2 | 0.632 | 0.631 | 73.9° | 74.0° | 0.461 |
| 0.4 | 0.261 | 0.264 | 62.6° | 63.1° | 0.171 |
| 0.6 | 0.121 | 0.121 | 50.5° | 50.6° | 0.0625 |
| 0.8 | 0.0446 | 0.0446 | 36.2° | 36.2° | 0.0139 |
| 0.9 | 0.0188 | 0.0188 | 26.5° | 26.5° | 0.0033 |
| 0.97 | 0.0048 | 0.00474 | 15.5° | 15.5° | 0.0003 |

![Journal bearing pressure and load capacity](bearings_journal_reynolds.png)

Panel (a) shows the antisymmetric full-Sommerfeld pressure, with the finite-difference points on the closed form. Panel (b) shows the pressure once negative values are excluded: the long-bearing film ruptures at $\theta = 242^\circ$ for $\varepsilon = 0.2$ and at $200^\circ$ for $\varepsilon = 0.8$, past the minimum film thickness at $180^\circ$, and the mid-plane pressure of the $L/D = 1$ bearing is well below the long-bearing value because the oil also escapes axially. Panel (c) is the design chart: for a given $S$ the finite bearing runs at a larger eccentricity than either long-bearing model predicts, and the short-bearing formula is only a rough guide at $L/D = 1$. Panel (d) shows the pressure field of the finite bearing, falling to zero at both ends and at the rupture line.

## Related Notes

- [Bearings and Lubrication](../../../notes/applied_mechanics/mechanical_systems/bearings.md)
- [Navier-Stokes Equations](../../../notes/fluid_mechanics/governing_equations/navier_stokes.md)
- [Viscosity](../../../notes/fluid_mechanics/fluid_properties/viscosity.md)
