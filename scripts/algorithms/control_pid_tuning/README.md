# PID Tuning and Windup

This script tunes a PID controller for a first-order-plus-dead-time process with the Ziegler–Nichols and SIMC rules, compares the set-point and load responses and the stability margins, and shows integrator windup under actuator saturation with and without back-calculation. The process is an electrically heated water stream whose outlet temperature responds to heater power with gain 2 K/kW, time constant 10 s and a 3 s transport delay to the sensor.

## Overview

- Computes the ultimate gain and period of the process from the phase condition $\arctan(\omega\tau) + \omega\theta = \pi$.
- Tunes three controllers: Ziegler–Nichols step-response PID, Ziegler–Nichols ultimate-gain PID and SIMC PI with $\tau_c = \theta$.
- Computes the gain margin, phase margin and peak sensitivity of each loop from $C(j\omega)G(j\omega)$ on a dense frequency grid.
- Simulates each closed loop in discrete time ($T_s = 0.01$ s) for a 1 K set-point step and for a $-0.5$ kW load step at the process input, and reports overshoot, settling time, integrated absolute error and the final error.
- Repeats the set-point step for the SIMC PI controller with the heater limited to 0–0.65 kW, without anti-windup and with back-calculation.

## Mathematical Background

The process is $G(s) = Ke^{-\theta s}/(\tau s + 1)$ with $K = 2$ K/kW, $\tau = 10$ s and $\theta = 3$ s. The tuning rules are

```math
\text{ZN step: } K_c = \frac{1.2\tau}{K\theta},\ T_i = 2\theta,\ T_d = \frac{\theta}{2}; \qquad \text{ZN ultimate: } K_c = 0.6K_u,\ T_i = \frac{T_u}{2},\ T_d = \frac{T_u}{8}; \qquad \text{SIMC: } K_c = \frac{\tau}{K(\tau_c + \theta)},\ T_i = \min(\tau, 4(\tau_c + \theta))
```

The process is discretized exactly for a zero-order hold, $`y[k+1] = a\,y[k] + K(1 - a)\,v[k - d]`$ with $a = e^{-T_s/\tau}$ and $d = \theta/T_s$, where $v$ is the applied heater power plus the load. The controller is the ideal-form PID with proportional and integral action on the error and a filtered derivative ($T_f = T_d/N$, $N = 10$) on the measurement. Back-calculation adds $(T_s/T_t)(u_{\mathrm{sat}} - u)$ to the integral each step, with $T_t = \sqrt{T_iT_d}$ for a PID and $T_i/2$ for a PI controller. For a PI loop with zero final error, the integrated error after a load step $d$ is $\lvert d\rvert T_i/K_c$.

## Implementation

- `ultimate_gain_period()`, `zn_step_pid()`, `zn_ultimate_pid()` and `simc_pi(tau_c)` return the tunings as dictionaries of `kc`, `ti` and `td`.
- `controller_response(omega, gains)` and `process_response(omega)` give the frequency responses; `loop_margins(gains)` returns GM, PM and $M_s$.
- `simulate(gains, setpoint, load, u_limits, anti_windup)` runs the discrete closed loop and returns time, output, the PID output before saturation and the applied input.
- `step_metrics(t, y, target)` and `iae(t, y, target)` evaluate the responses; `analyse()` runs all cases and `make_figure(results, windup)` draws the four panels.
- Constants `PROCESS_GAIN`, `TIME_CONSTANT`, `DEAD_TIME`, `DT`, `DERIVATIVE_FILTER_N`, `SETPOINT_STEP`, `LOAD_STEP`, `U_MIN` and `U_MAX` set the case.

## Usage

```bash
python main.py                          # print the comparison and show the figure
python main.py --no-show --output .     # save control_pid_tuning.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The ultimate gain is $K_u = 2.945$ kW/K with $T_u = 10.82$ s. The script prints:

| Tuning | $K_c$ | $T_i$ (s) | $T_d$ (s) | GM | PM | $M_s$ | Overshoot | $t_s$ (s) | Set-point IAE | Peak load deviation (K) | Load IAE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ziegler–Nichols step PID | 2.000 | 6.00 | 1.50 | 1.34 | $44.3^\circ$ | 3.94 | 52.9% | 28.7 | 7.37 | $-0.271$ | 1.71 |
| Ziegler–Nichols ultimate PID | 1.767 | 5.41 | 1.35 | 1.62 | $42.8^\circ$ | 2.65 | 50.3% | 22.6 | 7.49 | $-0.276$ | 1.77 |
| SIMC PI ($\tau_c = \theta$) | 0.833 | 10.00 | 0 | 3.14 | $61.4^\circ$ | 1.59 | 4.1% | 18.2 | 6.51 | $-0.388$ | 6.00 |

All final set-point errors are below $10^{-6}$ K. With the heater limited to 0.65 kW, the SIMC PI loop overshoots by 15.4% and settles in 47.7 s without anti-windup (the PID output reaches 1.08 kW), and does not overshoot and settles in 30.9 s with back-calculation.

![PID tuning comparison and integrator windup](control_pid_tuning.png)

Panels (a) and (b) show the set-point and load responses of the three tunings. Panel (c) shows the saturated set-point response with and without anti-windup, and panel (d) the heater power applied (solid) and the PID output before saturation (dashed), with the limit drawn as a horizontal line.

## Related Notes

- [PID Controllers](../../../notes/applied_mechanics/control_systems/pid_controllers.md)
- [Feedback Control](../../../notes/applied_mechanics/control_systems/feedback_control.md)
