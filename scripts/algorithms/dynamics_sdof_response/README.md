# SDOF Vibration Response

This script computes the free and forced response of a single-degree-of-freedom mass–spring–damper and checks the Newmark-β integrator against the closed-form free response. A 1 kg mass on a 1 Hz spring is released from 10 mm for damping ratios 0, 0.1, 1 and 2, and the magnification factor, phase lag and transmissibility of harmonic excitation are drawn for six damping ratios.

## Overview

- Evaluates the exact free response of $m\ddot{x} + c\dot{x} + kx = 0$ in the underdamped, critically damped and overdamped regimes from $x_0 = 10$ mm, $\dot{x}_0 = 0$.
- Integrates the same equation with the Newmark-β average-acceleration method ($\beta = 1/4$, $\gamma = 1/2$) at $\Delta t = T_n/50$ and reports the largest error relative to $x_0$.
- Plots the magnification factor $Xk/F_0$ and the phase lag of harmonic forcing for $\zeta = 0.05, 0.1, 0.2, 0.5, 0.707, 1$ and marks each resonance peak at $r = \sqrt{1 - 2\zeta^2}$.
- Plots the transmissibility of base excitation, which equals the force transmissibility of a machine on a mount, for the same damping ratios.

## Mathematical Background

With $\omega_n = \sqrt{k/m}$ and $\zeta = c/(2\sqrt{km})$, the free response for $\zeta < 1$ is

```math
x(t) = e^{-\zeta\omega_n t}\left[x_0\cos\omega_d t + \frac{\dot{x}_0 + \zeta\omega_n x_0}{\omega_d}\sin\omega_d t\right],
\qquad \omega_d = \omega_n\sqrt{1 - \zeta^2}
```

For $\zeta = 1$ it is $`x = e^{-\omega_n t}\left[x_0 + (\dot{x}_0 + \omega_n x_0)t\right]`$, and for $`\zeta > 1`$ it is $`x = C_1e^{s_1t} + C_2e^{s_2t}`$ with $`s_{1,2} = (-\zeta \pm \sqrt{\zeta^2 - 1})\omega_n`$.

For a force $F_0\sin\omega t$ and frequency ratio $r = \omega/\omega_n$, the steady-state amplitude, phase lag and transmissibility are

```math
\frac{Xk}{F_0} = \frac{1}{\sqrt{(1 - r^2)^2 + (2\zeta r)^2}},
\qquad
\tan\phi = \frac{2\zeta r}{1 - r^2},
\qquad
T = \sqrt{1 + (2\zeta r)^2}\,\frac{Xk}{F_0}
```

The Newmark method advances $x$ and $\dot{x}$ with

```math
x_{n+1} = x_n + \Delta t\,\dot{x}_n + \Delta t^2\left[\left(\tfrac{1}{2} - \beta\right)\ddot{x}_n + \beta\,\ddot{x}_{n+1}\right],
\qquad
\dot{x}_{n+1} = \dot{x}_n + \Delta t\left[(1 - \gamma)\ddot{x}_n + \gamma\,\ddot{x}_{n+1}\right]
```

and enforces the equation of motion at $t_{n+1}$. With $\beta = 1/4$, $\gamma = 1/2$ it is second-order accurate, unconditionally stable and adds no numerical damping; its only error on a linear oscillator is a period elongation of about $(\omega_n\Delta t)^2/12$.

## Implementation

- `free_response(t, zeta, omega_n, x0, v0)` returns the closed-form free response for any $\zeta \ge 0$.
- `newmark(m, c, k, force, dt, x0, v0, beta, gamma)` implements the incremental form of the Newmark method with the effective stiffness $\hat{k} = k + \gamma c/(\beta\Delta t) + m/(\beta\Delta t^2)$; `force` holds $f$ at every time level.
- `magnification(r, zeta)`, `phase_lag(r, zeta)`, `transmissibility(r, zeta)` and `peak_frequency_ratio(zeta)` evaluate the frequency-response formulas.
- `free_decay_study()` runs both solutions for `FREE_ZETAS`; `make_figure` draws the four panels.
- Constants `MASS`, `NATURAL_FREQUENCY_HZ`, `X0`, `STEPS_PER_PERIOD`, `FREE_ZETAS` and `FRF_ZETAS` set the case.

## Usage

```bash
python main.py                          # print the comparison and show the figure
python main.py --no-show --output .     # save dynamics_sdof_response.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The largest Newmark error relative to $x_0$ over 3 s is $2.3\times10^{-2}$ for $\zeta = 0$, $4.8\times10^{-3}$ for $\zeta = 0.1$ and below $10^{-3}$ for $\zeta = 1$ and 2; in the undamped case the error is the accumulated phase lag of the period elongation, 0.13% per cycle at 50 steps per period. The magnification peaks are at $r = 0.9975, 0.9899, 0.9592, 0.7071$ with heights 10.01, 5.03, 2.55 and 1.155 for $\zeta = 0.05, 0.1, 0.2, 0.5$; $1/(2\zeta)$ is the value at $r = 1$, slightly below the peak.

![SDOF free response, magnification, phase and transmissibility](dynamics_sdof_response.png)

Panel (a) shows the four damping regimes, with the critically damped curve returning to zero fastest without overshoot. Panel (b) shows the resonance peak shrinking and moving to lower $r$ as damping rises, and disappearing for $\zeta \ge 1/\sqrt{2}$. Panel (c) shows that every curve passes through $90^\circ$ at $r = 1$. Panel (d) shows that all transmissibility curves cross 1 at $r = \sqrt{2}$, and that above it more damping means less isolation.

## Related Notes

- [Mechanical Vibrations](../../../notes/applied_mechanics/dynamics/vibrations.md)
- [Lagrangian Mechanics](../../../notes/applied_mechanics/dynamics/lagrangian_mechanics.md)
