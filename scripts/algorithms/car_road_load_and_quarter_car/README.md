# Car Road Load and Quarter-Car Ride

This script computes the road-load power and energy demand of a mid-size car and the ride response of a quarter-car suspension model. The road-load part splits the tractive force into rolling resistance and aerodynamic drag, finds the speed at which the two are equal, and integrates the wheel energy over a synthetic urban and highway cycle with and without braking-energy recovery. The ride part solves the two-degree-of-freedom quarter-car model in the frequency domain and plots body acceleration and tyre deflection against frequency for two damping ratios.

## Overview

- Uses a 1500 kg car with $C_{rr} = 0.010$, $C_d = 0.30$ and $A = 2.2$ m² in air of density 1.225 kg/m³.
- Computes level-road force, power and wheel energy per 100 km at constant speed, and the crossover speed $U_c$ where rolling and aerodynamic forces are equal.
- Builds a synthetic drive cycle of eight trapezoidal segments (accelerate at 1.0 m/s², cruise at 30 to 120 km/h, brake at 0.8 m/s², stop); it is a generic stop-and-go and highway trace, not a regulatory cycle.
- Integrates positive (traction) and negative (braking) wheel power over the cycle and reports the energy per 100 km without recovery and with 60% of the braking energy recovered.
- Builds the quarter-car mass, damping and stiffness matrices ($m_s = 400$ kg, $m_u = 40$ kg, $k_s = 22$ kN/m, $k_t = 200$ kN/m), computes the undamped natural frequencies, and evaluates the frequency response for damping ratios 0.2 and 0.5.

## Mathematical Background

### Road Load

The tractive force at the wheels is

$$
F = m g C_{rr} + \tfrac{1}{2}\rho C_d A U^2 + m g\sin\theta + m a
$$

with mass $m$, rolling-resistance coefficient $C_{rr}$, drag area $C_dA$, speed $U$, road grade $\theta$ and acceleration $a$ (rotating inertia is not included). The rolling and aerodynamic terms are equal at

$$
U_c = \sqrt{\frac{2 m g C_{rr}}{\rho C_d A}}
$$

The power is $P = FU$ and the wheel energy per unit distance at constant speed is simply $F$, so 1 N corresponds to $10^5$ J = 0.0278 kWh per 100 km. Over a cycle that starts and ends at rest, traction energy minus braking energy equals the work done against rolling resistance and drag.

### Quarter-Car Model

With body displacement $z_s$, wheel displacement $z_u$ and road profile $z_r$,

```math
m_s\ddot z_s + c_s(\dot z_s - \dot z_u) + k_s(z_s - z_u) = 0
```

```math
m_u\ddot z_u - c_s(\dot z_s - \dot z_u) - k_s(z_s - z_u) + k_t(z_u - z_r) = 0
```

The damper is $c_s = 2\zeta\sqrt{k_s m_s}$. For harmonic road input $z_r e^{i\omega t}$ the complex amplitudes solve $(\mathbf{K} - \omega^2\mathbf{M} + i\omega\mathbf{C})\mathbf{z} = (0, k_t)^T z_r$. The undamped frequencies are the roots of

$$
m_s m_u\omega^4 - \left[m_s(k_s + k_t) + m_u k_s\right]\omega^2 + k_s k_t = 0
$$

which for $m_u \ll m_s$ and $k_s \ll k_t$ are close to $\omega_{body} \approx \sqrt{k_s k_t/((k_s + k_t)m_s)}$ and $\omega_{wheel} \approx \sqrt{(k_s + k_t)/m_u}$.

## Implementation

- `road_load(speed, accel, grade)`, `rolling_force()`, `aero_force(speed)` and `crossover_speed()` implement the road-load relations; `constant_speed_energy(speed)` returns kWh per 100 km.
- `drive_cycle()` builds the speed trace from `CYCLE_SEGMENTS`, and `cycle_energy(t, u)` returns distance, traction and braking energy and the wheel power.
- `quarter_car_matrices(zeta)` returns $\mathbf{M}$, $\mathbf{C}$, $\mathbf{K}$; `natural_frequencies()` solves the undamped eigenvalue problem; `quarter_car_response(freq, zeta)` solves the complex system at each frequency.
- `make_road_load_figure()` and `make_quarter_car_figure()` draw the two figures.

## Usage

```bash
python main.py                          # print the results and show both figures
python main.py --no-show --output .     # save car_road_load.png and car_quarter_car.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figures as PNG |

## Output

Rolling resistance is 147 N and the crossover speed is 19.1 m/s (69 km/h). At 50, 90 and 120 km/h the level-road force is 225, 400 and 596 N, the power 3.1, 10.0 and 19.9 kW, and the wheel energy 6.3, 11.1 and 16.6 kWh per 100 km. The synthetic cycle covers 22.3 km in 1180 s (mean 68 km/h) and needs 14.8 kWh per 100 km of traction energy; 2.3 kWh per 100 km is dissipated in braking, and recovering 60% of it lowers the net demand to 13.4 kWh per 100 km.

![Road-load power, drive cycle and energy demand](car_road_load.png)

Panel (a) shows the aerodynamic share of the power growing with $U^3$ and overtaking rolling resistance at $U_c$. Panel (b) shows the cycle and the wheel power, with braking power in green. Panel (c) compares constant-speed energy with the cycle values.

The quarter car has its body mode at 1.12 Hz and its wheel-hop mode at 11.86 Hz.

![Quarter-car frequency response](car_quarter_car.png)

With $\zeta = 0.2$ the body resonance is sharp and the body is well isolated between the two modes; with $\zeta = 0.5$ the body peak is suppressed but more wheel motion is transmitted between and above the modes. Panel (b) shows the matching trade-off for tyre deflection: low damping lets the tyre load vary strongly near wheel hop, which costs grip.

## Related Notes

- [How Cars Work](../../../notes/applied_mechanics/transportation/cars/how_cars_work.md)
- [Car Design and Manufacturing](../../../notes/applied_mechanics/transportation/cars/manufacturing_and_design_process.md)
