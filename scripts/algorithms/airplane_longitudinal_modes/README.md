# Longitudinal Modes of a Light Aircraft

This script finds the short-period and phugoid modes of a representative 1100 kg light aircraft from its linearized longitudinal equations, compares them with the classical two-mode approximations, and shows how a pilot with a reaction delay can turn the well-damped short period into a pilot-induced oscillation. The stability derivatives are built from stated non-dimensional coefficients of a four-seat single-engine aircraft in level flight at 55 m/s at sea level, so every number can be traced back to an input.

## Overview

- Computes the trim lift coefficient, the drag coefficient from a parabolic polar and the dimensional derivatives $X_u, X_w, Z_u, Z_w, M_w, M_{\dot w}, M_q, Z_{\delta_e}, M_{\delta_e}$.
- Assembles the four-state model $\mathbf{x} = [\Delta u, \Delta w, q, \Delta\theta]^T$ and its eigenvalues.
- Compares the short period with the constant-speed approximation and the phugoid with Lanchester's $`\omega_{ph} = \sqrt{2}\,g/U`$.
- Integrates the exact zero-order-hold response to a $-1^\circ$ (trailing-edge-up) elevator step over 6 s and 150 s, including the height change.
- Closes a pitch-attitude loop with a pure-gain pilot, $\delta_e = K(\theta(t - \tau) - \theta_c)$ with $\tau = 0.3$ s, finds the critical gain from the frequency response and simulates $K = 0.5$, 1 and 1.1 times the critical value.

## Mathematical Background

### Equations of Motion

In stability axes with thrust effects, $Z_q$ and $Z_{\dot w}$ neglected and level trim ($\theta_0 = 0$):

```math
\begin{aligned}
\Delta\dot u &= X_u\Delta u + X_w\Delta w - g\,\Delta\theta \\
\Delta\dot w &= Z_u\Delta u + Z_w\Delta w + U q + Z_{\delta_e}\delta_e \\
\dot q &= M_u\Delta u + M_w\Delta w + M_{\dot w}\Delta\dot w + M_q q + M_{\delta_e}\delta_e \\
\Delta\dot\theta &= q
\end{aligned}
```

with $\Delta\dot w$ substituted into the pitch equation. With $Q = \tfrac{1}{2}\rho U^2$, mass $m$ and pitch inertia $I_y$ the derivatives are

```math
X_u = -\frac{2C_D QS}{mU}, \quad X_w = -\frac{(C_{D_\alpha} - C_L)QS}{mU}, \quad Z_u = -\frac{2C_L QS}{mU} = -\frac{2g}{U}, \quad Z_w = -\frac{(C_{L_\alpha} + C_D)QS}{mU}
```

```math
M_w = \frac{C_{m_\alpha}QS\bar c}{I_y U}, \quad M_{\dot w} = \frac{C_{m_{\dot\alpha}}\bar c}{2U}\frac{QS\bar c}{I_y U}, \quad M_q = \frac{C_{m_q}\bar c}{2U}\frac{QS\bar c}{I_y}, \quad Z_{\delta_e} = -\frac{C_{L_{\delta_e}}QS}{m}, \quad M_{\delta_e} = \frac{C_{m_{\delta_e}}QS\bar c}{I_y}
```

with $C_{D_\alpha} = 2kC_LC_{L_\alpha}$ from the polar $C_D = C_{D0} + kC_L^2$, and $M_u = 0$ (no compressibility or thrust effects).

### Mode Approximations

```math
\omega_{sp} = \sqrt{\frac{Z_\alpha M_q}{U} - M_\alpha},
\qquad
\zeta_{sp} = -\frac{M_q + M_{\dot\alpha} + Z_\alpha/U}{2\omega_{sp}},
\qquad
Z_\alpha = UZ_w,\ M_\alpha = UM_w,\ M_{\dot\alpha} = UM_{\dot w}
```

```math
\omega_{ph} = \sqrt{-\frac{gZ_u}{U}} = \frac{\sqrt{2}\,g}{U},
\qquad
\zeta_{ph} = -\frac{X_u}{2\omega_{ph}}
```

The phugoid approximation assumes constant angle of attack and no pitch dynamics.

### Pilot Loop

With $G(s) = \Delta\theta/\delta_e$ and the pilot $\delta_e = K(\theta(t - \tau) - \theta_c)$, the open loop is $L(j\omega) = -KG(j\omega)e^{-j\omega\tau}$. The loop is neutrally stable at the gain $K_{crit} = 1/|G(j\omega_{180})|$, where $\omega_{180}$ is the frequency at which the phase of $-G(j\omega)e^{-j\omega\tau}$ is $-180^\circ$. A larger gain gives a growing oscillation at about $\omega_{180}$.

## Implementation

- `AIRCRAFT` holds the inputs: $m = 1100$ kg, $I_y = 1825$ kg m², $S = 16.2$ m², $\bar c = 1.49$ m, $b = 11.0$ m, $U = 55$ m/s, $C_{D0} = 0.027$, $e = 0.80$, $C_{L_\alpha} = 4.6$, $C_{m_\alpha} = -0.89$ (static margin 0.19), $C_{m_q} = -12.4$, $C_{m_{\dot\alpha}} = -5.2$, $C_{L_{\delta_e}} = 0.43$, $C_{m_{\delta_e}} = -1.28$ (all per radian).
- `trim_and_derivatives(ac)` and `state_space(d)` build the model; `split_modes` and `mode_properties` extract $\omega_n$, $\zeta$ and the period.
- `short_period_approximation(d)` and `phugoid_approximation(d)` implement the formulas above.
- `step_response(a, b, amplitude, t)` uses the matrix exponential of the augmented system, so each step is exact for a piecewise-constant input; `altitude` integrates $\dot h = U\Delta\theta - \Delta w$.
- `pitch_frequency_response`, `critical_pilot_gain` (phase scan plus `scipy.optimize.brentq`) and `simulate_pilot_loop` (history buffer for the delay, elevator limited to $\pm 0.5$ rad) implement the pilot loop.

## Usage

```bash
python main.py                          # print the modes and show both figures
python main.py --no-show --output .     # save the PNGs in the current directory
```

## Output

The trim lift coefficient is 0.360. The script prints:

| Mode | Eigenvalue (1/s) | $\omega_n$ (rad/s) | $\zeta$ | Period (s) | Approximation |
| --- | --- | --- | --- | --- | --- |
| Short period | $-4.07 \pm 3.83j$ | 5.59 | 0.728 | 1.64 | $\omega_n = 5.59$, $\zeta = 0.728$ |
| Phugoid | $-0.0149 \pm 0.210j$ | 0.211 | 0.071 | 29.9 | Lanchester $\omega = 0.252$, period 24.9 s, $\zeta = 0.067$ |

The short-period approximation is accurate to three figures. Lanchester's estimate is 20% high for this aircraft; setting $M_q = M_{\dot w} = 0$ in the full model brings the phugoid frequency to within 0.1% of $`\sqrt{2}\,g/U`$, so the difference comes from pitch damping coupling the two modes. The pilot loop has $K_{crit} = 1.14$ rad of elevator per rad of pitch error, and the oscillation at the critical gain has a frequency of 4.62 rad/s (period 1.36 s).

![Longitudinal eigenvalues and responses to an elevator step](airplane_longitudinal_modes.png)

Panel (a) shows the well-separated poles, with the phugoid enlarged in the inset next to Lanchester's purely imaginary estimate. Panel (b) shows the short period settling within about one second into a new angle of attack and a slowly varying pitch rate. Panel (c) shows the lightly damped phugoid exchanging speed and pitch attitude; the response tends to a new trim 8.3 m/s slower with $\Delta\alpha = 1.44^\circ$ and a steady climb of 0.89 m/s, because at fixed thrust a lower speed (still above the minimum-drag speed) needs less power.

![Pilot-induced oscillation with a delayed pure-gain pilot](airplane_pilot_induced_oscillation.png)

At half the critical gain the pitch attitude reaches the command in under a second and then sags slowly below it, because a proportional pilot leaves a steady error and the phugoid is still active. At the critical gain the oscillation neither grows nor decays, and 10% above it the pilot's own corrections drive a divergent oscillation at about 4.6 rad/s.

## Related Notes

- [Airplane Stability](../../../notes/applied_mechanics/transportation/airplanes/airplane_stability.md)
- [Static and Dynamic Stability of Oscillating Systems](../../../notes/applied_mechanics/transportation/airplanes/pecking.md)
