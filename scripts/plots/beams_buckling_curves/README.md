# Column Buckling Curves

This script plots the Euler, Johnson, AISC and secant-formula column curves for a structural steel, computes the buckled modes and effective-length factors of four end conditions with a finite-element eigenvalue analysis, and fits a Southwell plot to synthetic test readings. The column curves show where elastic buckling, inelastic buckling and yielding govern, and how much an eccentric load lowers the capacity. The finite-element analysis uses Hermite beam elements with the consistent geometric stiffness matrix and recovers the theoretical factors $K = 1, 2, 0.699$ and $0.5$. The Southwell plot shows how the critical load of an imperfect column is estimated from deflections measured well below it.

## Overview

- Plots, for $E = 200$ GPa and $\sigma_Y = 250$ MPa, the Euler hyperbola, the Johnson parabola up to the transition slenderness and Euler beyond it, the yield cut-off, the AISC 360 nominal stress $F_{cr}$, and the secant-formula stress at first yield for $ec/r^2 = 0.1$ and 0.3, against $KL/r$ from 1 to 250.
- Marks the transition slenderness $\lambda_t = \sqrt{2\pi^2E/\sigma_Y} = 125.7$ and the slenderness 88.9 at which the Euler stress equals yield.
- Solves the generalized eigenvalue problem $`\mathbf{K}\boldsymbol{\phi} = P\,\mathbf{K}_G\boldsymbol{\phi}`$ on 40 elements for pinned–pinned, fixed–free, fixed–pinned and fixed–fixed columns, draws the first mode of each, and prints $`K = \pi/\sqrt{P_{cr}L^2/EI}`$.
- Generates twelve seeded readings of the extra mid-height deflection of a pin-ended steel strut (2 m long, 30 mm diameter, initial bow 2 mm) between 15% and 85% of the critical load with 0.02 mm reading noise, and fits the Southwell line.

## Mathematical Background

### Column Curves

The Euler and Johnson stresses are

```math
\sigma_E = \frac{\pi^2E}{\lambda^2}, \qquad
\sigma_J = \sigma_Y - \frac{1}{E}\left(\frac{\sigma_Y\lambda}{2\pi}\right)^2, \qquad \lambda = \frac{KL}{r}
```

and they touch, with equal slope, at $\lambda_t = \sqrt{2\pi^2E/\sigma_Y}$, where both equal $\sigma_Y/2$. The AISC 360 nominal stress, with $F_e = \sigma_E$ and $F_y = \sigma_Y$, is $0.658^{F_y/F_e}F_y$ for $F_y/F_e \le 2.25$ and $0.877F_e$ otherwise. The secant formula for a pin-ended column with eccentricity $e$, extreme-fibre distance $c$ and radius of gyration $r$,

```math
\sigma_{\max} = \frac{P}{A}\left[1 + \frac{ec}{r^2}\sec\left(\frac{\lambda}{2}\sqrt{\frac{P}{AE}}\right)\right] = \sigma_Y
```

is solved for $P/A$ at each slenderness with `scipy.optimize.brentq`.

### Buckling Eigenproblem

With Hermite cubic elements of length $h$, the geometric stiffness matrix that represents the work of the axial load $P$ through the slopes is

```math
\mathbf{k}_G = \frac{1}{30h}
\begin{bmatrix}
36 & 3h & -36 & 3h \\
3h & 4h^2 & -3h & -h^2 \\
-36 & -3h & 36 & -3h \\
3h & -h^2 & -3h & 4h^2
\end{bmatrix}
```

and the critical loads are the eigenvalues of $`\mathbf{K}\boldsymbol{\phi} = P\,\mathbf{K}_G\boldsymbol{\phi}`$ after the support constraints are applied. The lowest eigenvalue converges from above to the exact value as the mesh is refined.

### Southwell Plot

For an initial bow $\delta_0\sin(\pi x/L)$, the additional mid-height deflection under load $P$ is $\delta = \delta_0 (P/P_{cr})/(1 - P/P_{cr})$, which rearranges to

```math
\frac{\delta}{P} = \frac{\delta}{P_{cr}} + \frac{\delta_0}{P_{cr}}
```

a straight line in $(\delta, \delta/P)$ with slope $1/P_{cr}$ and intercept $\delta_0/P_{cr}$.

## Implementation

- `euler_stress`, `transition_slenderness`, `johnson_stress`, `aisc_stress` and `secant_stress(slenderness, ecc_ratio)` evaluate the column curves.
- `beam_matrices(length, n_elements, ei)` assembles $\mathbf{K}$ and $`\mathbf{K}_G`$; `buckling_mode(condition, length, ei, n_elements)` applies the end conditions of `END_CONDITIONS` and solves the eigenproblem with `scipy.linalg.eigh`, returning $P_{cr}$ and the normalized mode; `effective_length_factor(condition)` converts $`P_{cr}`$ to $K$.
- `southwell_readings(seed)` generates the synthetic test data and `southwell_fit(loads, delta)` fits the line with `numpy.polyfit`.
- `plot_column_curves`, `plot_southwell`, `draw_end` and `plot_mode` draw the panels.
- Constants: `E_STEEL`, `SIGMA_Y`, `ECCENTRICITY_RATIOS`, `N_ELEMENTS` = 40, and `STRUT_LENGTH`, `STRUT_DIAMETER`, `STRUT_CROOKEDNESS`, `READING_NOISE`, `SEED` for the Southwell test.

## Usage

```bash
python main.py                          # print the results and show the figure
python main.py --no-show --output .     # save beams_buckling_curves.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints the transition slenderness 125.66, the slenderness 88.86 at which the Euler stress reaches yield, effective-length factors from the finite-element analysis of 1.0000, 2.0000, 0.6992 and 0.5000, and a Southwell estimate of $P_{cr} = 19.627$ kN against the exact 19.621 kN, with $\delta_0 = 2.002$ mm against the true 2.000 mm.

![Column curves for a structural steel, a Southwell plot, and the first buckled modes for four end conditions](beams_buckling_curves.png)

In panel (a), the Johnson parabola meets the Euler hyperbola tangentially at half the yield stress; the AISC curve lies below it everywhere, and the secant curves start below yield at zero slenderness, at $\sigma_Y/(1 + ec/r^2)$, and approach the Euler curve for slender columns. Panel (b) shows the readings on a straight line, as the Southwell relation predicts. Panel (c) shows that each mode is a piece of a sine wave whose half-wavelength between inflection points is the effective length $KL$.

## Related Notes

- [Buckling of Columns](../../../notes/applied_mechanics/strength_materials/buckling.md)
- [Bending of Beams](../../../notes/applied_mechanics/strength_materials/beam_bending.md)
