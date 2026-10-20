# Second-Order Step Response

This script simulates the step response of the standard second-order system for six damping ratios, measures rise time, peak time, overshoot and settling time, and compares them with the closed-form formulas and the pole locations. It shows on one figure how the damping ratio and natural frequency of a pole pair translate into the time-domain specifications used to design control loops.

## Overview

- Simulates $G(s) = \omega_n^2/(s^2 + 2\zeta\omega_n s + \omega_n^2)$ with $\omega_n = 2$ rad/s and $\zeta = 0.1, 0.3, 0.5, 0.7, 1.0, 2.0$ using `scipy.signal.step` on a 1 ms grid over 20 s.
- Measures from each response the 10–90% rise time, the peak time, the percentage overshoot and the 2% settling time, using linear interpolation for the 10% and 90% crossings.
- Compares the measured overshoot and peak time with $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ and $t_p = \pi/\omega_d$, and the settling time with $`4/\lvert\mathrm{Re}\,p\rvert`$ of the slowest pole.
- Draws the poles in the $s$-plane with rays of constant damping ratio and arcs of constant natural frequency.

## Mathematical Background

For $0 < \zeta < 1$ the poles are $s = -\zeta\omega_n \pm j\omega_d$ with $\omega_d = \omega_n\sqrt{1 - \zeta^2}$, and the unit step response is

```math
y(t) = 1 - \frac{e^{-\zeta\omega_n t}}{\sqrt{1-\zeta^2}}\sin\left(\omega_d t + \arccos\zeta\right)
```

Its first maximum is at $t_p = \pi/\omega_d$, where $y = 1 + M_p$ with $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$. The envelope reaches 2% after about $4/(\zeta\omega_n)$. For $\zeta > 1$ the poles are real, $-\omega_n(\zeta \pm \sqrt{\zeta^2 - 1})$, and the slower one sets the settling time $4/[\omega_n(\zeta - \sqrt{\zeta^2 - 1})]$. The damping ratio of a pole $p$ is $`-\mathrm{Re}\,p/\lvert p\rvert`$, constant along a ray from the origin, and $\omega_n = \lvert p\rvert$, constant on a circle.

## Implementation

- `second_order_system(zeta, omega_n)` builds the `scipy.signal.lti` object and `step_response(zeta)` simulates it on `N_TIME` points up to `T_END`.
- `step_metrics(t, y)` returns the rise time, peak time, overshoot fraction and settling time (band `SETTLING_BAND`); `_crossing_time` interpolates the 10% and 90% crossings.
- `overshoot_formula`, `peak_time_formula`, `settling_time_estimate` and `poles` give the analytic values; `zeta_from_overshoot(mp)` inverts the overshoot formula.
- `make_figure(results)` draws the four panels. Constants `OMEGA_N`, `ZETAS` and `ANNOTATED_ZETA` set the cases.

## Usage

```bash
python main.py                          # print the table and show the figure
python main.py --no-show --output .     # save control_second_order_response.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints, for $\omega_n = 2$ rad/s:

| $\zeta$ | $t_r$ (s) | $t_p$ (s) | $M_p$ (%) | $M_p$ formula (%) | $t_s$ (s) | $`4/\lvert\mathrm{Re}\,p\rvert`$ (s) |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.552 | 1.579 | 72.92 | 72.92 | 19.19 | 20.00 |
| 0.3 | 0.661 | 1.647 | 37.23 | 37.23 | 5.62 | 6.67 |
| 0.5 | 0.819 | 1.814 | 16.30 | 16.30 | 4.04 | 4.00 |
| 0.7 | 1.063 | 2.200 | 4.60 | 4.60 | 2.99 | 2.86 |
| 1.0 | 1.679 |  | 0 | 0 | 2.92 | 2.00 |
| 2.0 | 4.115 |  | 0 | 0 | 7.44 | 7.46 |

![Second-order step responses, specifications and pole locations](control_second_order_response.png)

Panel (a) shows the six responses with the rise time, overshoot and settling time of the $\zeta = 0.3$ curve marked and the 2% band shaded. Panel (b) compares the measured overshoot with the formula, and panel (c) the measured settling, peak and rise times with the estimates; the settling time is a staircase function of $\zeta$, so $4/(\zeta\omega_n)$ is only approximate. Panel (d) places the poles on the grid of constant-$`\zeta`$ rays and constant-$`\omega_n`$ arcs.

## Related Notes

- [Introduction to Control Systems](../../../notes/applied_mechanics/control_systems/intro.md)
- [System Modeling](../../../notes/applied_mechanics/control_systems/system_modeling.md)
- [Stability Analysis](../../../notes/applied_mechanics/control_systems/stability_analysis.md)
- [Frequency Response](../../../notes/applied_mechanics/control_systems/frequency_response.md)
