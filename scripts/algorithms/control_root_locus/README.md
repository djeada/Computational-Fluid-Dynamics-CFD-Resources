# Root Locus and Routh–Hurwitz

This script computes the root locus of a third-order position servo by sweeping the gain, marks the asymptotes, breakaway point and damping-ratio design point, and checks that the gain where the locus crosses the imaginary axis equals the Routh–Hurwitz critical gain. The loop transfer function is $L(s) = K/[s(s + 2)(s + 5)]$: a DC motor whose angle integrates its speed, with a mechanical pole and an amplifier pole.

## Overview

- Computes the closed-loop poles, the roots of $D(s) + KN(s)$, with `numpy.roots` for 4000 gains between $10^{-3}$ and $10^3$, and orders them into continuous branches by nearest-neighbour matching.
- Computes the asymptote centroid and angles, and the breakaway point from $N D' - N' D = 0$ with $K = -D/N > 0$.
- Builds the Routh array of the characteristic polynomial, including the $\varepsilon$ substitution for a zero pivot and the auxiliary-polynomial rule for a row of zeros, and finds the critical gain by bisection on the number of first-column sign changes.
- Finds, independently, the gain at which the largest real part of the closed-loop poles crosses zero, and the frequency of the imaginary-axis crossing from the auxiliary polynomial.
- Finds the gain that places the complex pair on the line of damping ratio 0.5.

## Mathematical Background

A point $s$ lies on the root locus when $KN(s)/D(s) = -1$, which requires $\angle N(s)/D(s) = \pm 180^\circ(2q+1)$ and $K = \lvert D(s)/N(s)\rvert$. With $n$ poles and $m$ zeros, $n - m$ branches leave along asymptotes at angles $(2q + 1)180^\circ/(n - m)$ from the centroid $\sigma_a = (\sum p_i - \sum z_j)/(n - m)$, and branches leave the real axis where $dK/ds = 0$.

For $P(s) = s^3 + 7s^2 + 10s + K$ the Routh array has first column $1$, $7$, $(70 - K)/7$, $K$, so the loop is stable for $0 < K < 70$. At $K = 70$ the auxiliary polynomial $7s^2 + 70$ gives the crossing $s = \pm j\sqrt{10}$. The breakaway condition $3s^2 + 14s + 10 = 0$ gives $s = (-14 + \sqrt{76})/6 = -0.880$.

## Implementation

- `closed_loop_polynomial(k)` and `closed_loop_poles(k)` form and solve $D(s) + KN(s)$; `root_locus(gains)` returns the ordered branches.
- `asymptotes()` and `breakaway_points()` return the centroid, angles and the breakaway point with its gain.
- `routh_array(coeffs)` builds the array with both special cases; `sign_changes(column)` counts right-half-plane roots.
- `routh_critical_gain()` bisects on the Routh sign changes; `locus_crossing_gain()` bisects on the largest real part of the roots; `crossing_frequency(k)` reads the auxiliary polynomial.
- `damping_line_gain(zeta)` bisects for the gain that gives the requested damping ratio on the complex branch.
- `make_figure(gains, branches, data)` draws the two panels. `NUMERATOR` and `DENOMINATOR` define the loop.

## Usage

```bash
python main.py                          # print the results and show the figure
python main.py --no-show --output .     # save control_root_locus.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints an asymptote centroid of $-2.3333$ with angles $60^\circ$, $180^\circ$ and $300^\circ$, a breakaway point at $s = -0.8804$ with $K = 4.0607$, a Routh critical gain of $K_u = 70.000000$, the same value from the locus crossing, and a crossing frequency of 3.162278 rad/s ($\sqrt{10}$). The damping ratio 0.5 is reached at $K = 11.37$, with poles $-0.714 \pm 1.237j$ and $-5.571$.

![Root locus with asymptotes, breakaway point and imaginary-axis crossing, and largest real part of the closed-loop poles against gain](control_root_locus.png)

Panel (a) shows the three branches, the open-loop poles, the dashed asymptotes from the centroid, the breakaway point, the design point on the $\zeta = 0.5$ line and the imaginary-axis crossing labelled with the Routh result. Panel (b) shows the largest real part of the closed-loop poles against $K$: it dips to its most negative value at the breakaway gain and crosses zero at the Routh critical gain.

## Related Notes

- [Stability Analysis](../../../notes/applied_mechanics/control_systems/stability_analysis.md)
- [Feedback Control](../../../notes/applied_mechanics/control_systems/feedback_control.md)
