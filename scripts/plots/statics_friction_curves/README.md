# Friction Curves

This script plots the friction force on a block as the push grows through impending motion to sliding, the capstan ratio $e^{\mu\beta}$ against wrap angle, and the efficiency of a square-threaded screw against lead angle with its self-locking range. The three panels cover the Coulomb friction law, belt friction and thread friction, the three uses of dry friction in statics.

## Overview

- Panel (a): a block with normal force 100 N, $\mu_s = 0.5$ and $\mu_k = 0.4$ is pushed horizontally with $0 \leq P \leq 80$ N; friction equals the push up to 50 N and is 40 N once the block slides.
- Panel (b): $T_2/T_1 = e^{\mu\beta}$ for $\mu = 0.1, 0.2, 0.3, 0.5$ over up to three turns of wrap, on a logarithmic axis, with the 2.5-turn, $\mu = 0.3$ example marked.
- Panel (c): screw efficiency $\eta = \tan\lambda/\tan(\lambda + \phi)$ for $\mu = 0.05, 0.1, 0.15, 0.25$, with the self-locking range $\lambda \leq \phi$ shaded and the maximum at $\lambda = 45^\circ - \phi/2$ marked.
- Prints the slip and sliding forces, the capstan ratio per turn and, for each screw coefficient, $\phi$, the efficiency at the self-locking limit and the maximum efficiency.

## Mathematical Background

Coulomb's law states $|F| \leq \mu_s N$ at rest and $|F| = \mu_k N$ when sliding. For a belt on a drum, an element $d\theta$ is pressed with $`dN = T\,d\theta`$ and friction supports $`dT = \mu\,dN`$, so

```math
\frac{dT}{T} = \mu\,d\theta \implies \frac{T_2}{T_1} = e^{\mu\beta}
```

A square thread of lead angle $\lambda$ is an incline. Raising a load $W$ at mean radius $r$ needs the moment $M = Wr\tan(\lambda + \phi)$, with $\phi = \tan^{-1}\mu$, and the efficiency is the ideal moment $Wr\tan\lambda$ divided by $M$:

```math
\eta = \frac{\tan\lambda}{\tan(\lambda + \phi)}, \qquad
\eta_{\max} \text{ at } \lambda = 45^\circ - \frac{\phi}{2}, \qquad
\eta(\lambda = \phi) = \frac{1 - \mu^2}{2}
```

The screw is self-locking for $\lambda \leq \phi$, where the efficiency is below one half.

## Implementation

- `friction_force(push, weight, mu_s, mu_k)` returns the friction force for an array of pushes.
- `capstan_ratio(mu, wrap)` returns $e^{\mu\beta}$ with the wrap angle in radians.
- `screw_efficiency(lead_angle, mu)` returns the raising efficiency with the lead angle in radians.
- `make_figure()` draws the three panels; constants `BLOCK_WEIGHT`, `MU_STATIC`, `MU_KINETIC`, `CAPSTAN_MU`, `MAX_TURNS` and `SCREW_MU` set the cases.

## Usage

```bash
python main.py                          # print the values and show the figure
python main.py --no-show --output .     # save statics_friction_curves.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The block slips at $P = 50$ N, after which friction is 40 N. One turn of wrap multiplies the tension by 1.87, 3.51, 6.59 and 23.1 for $\mu = 0.1, 0.2, 0.3, 0.5$, and 2.5 turns at $\mu = 0.3$ give a ratio of 111. For the screw with $\mu = 0.15$, $\phi = 8.53^\circ$, the efficiency is 0.489 at the self-locking limit and reaches its maximum of 0.742 at $\lambda = 40.7^\circ$; with $\mu = 0.05$ the maximum is 0.905.

![Friction regimes, capstan curves and screw efficiency](statics_friction_curves.png)

## Related Notes

- [Friction](../../../notes/applied_mechanics/statics/friction.md)
- [Particle Equilibrium](../../../notes/applied_mechanics/statics/particle_equilibrium.md)
