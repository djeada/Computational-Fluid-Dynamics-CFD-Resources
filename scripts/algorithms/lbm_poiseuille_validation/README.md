# LBM Poiseuille Validation

This script validates a D2Q9 BGK lattice Boltzmann solver against the exact solution for body-force-driven channel flow with half-way bounce-back walls. The channel is periodic in the flow direction, a uniform body force with the Guo forcing scheme drives it, and the steady velocity profile is compared with the exact parabola for several relaxation times $\tau$ and channel widths $H$. The figure shows the second-order convergence of the error and the $\tau$-dependent wall slip of BGK bounce-back, which vanishes at $\tau = 1/2 + \sqrt{3/16}$.

## Overview

- Solves plane Poiseuille flow on a lattice of $1 \times H$ nodes (lattice units, $\Delta x = \Delta t = 1$). The flow is invariant in $x$, so one periodic column is enough; the kernel works for any number of columns.
- Places the walls halfway between the outermost fluid nodes and the virtual solid nodes, at $y = 0$ and $y = H$, so the fluid nodes sit at $y_j = j + 1/2$.
- Chooses the body force for each $(H, \tau)$ so that the exact centreline velocity is $u_{\max} = 0.05$ (Mach number 0.087).
- Starts from equilibrium populations with the exact profile and runs for 20 slowest viscous time scales $H^2/(\pi^2\nu)$, so the start-up transient has decayed by $e^{-20}$.
- Draws the profiles for $\tau = 0.6, 1, 2$ on a channel 8 nodes wide.
- Measures the relative $L_2$ error for $H = 8, 16, 32, 64, 128$ at $\tau = 0.8, 1, 1.5$ and prints the observed orders.
- Scans the wall slip over $0.51 \le \tau \le 2$ at $H = 16$, compares it with the analytical prediction, and prints the error at the exact-wall value of $\tau$.
- The inner loop is compiled with Numba; the whole script runs in about 5 s.

## Mathematical Background

### Lattice Boltzmann Equation with Guo Forcing

With D2Q9 velocities $\mathbf{c}_i$ (counter-clockwise ordering, opposite directions $\bar\imath$), weights $w_i = 4/9, 1/9, 1/36$ and $c_s^2 = 1/3$, each step performs

```math
f_i^\star = f_i - \frac{1}{\tau}\left(f_i - f_i^{\mathrm{eq}}\right) + \left(1 - \frac{1}{2\tau}\right) w_i \left[\frac{\mathbf{c}_i - \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})\,\mathbf{c}_i}{c_s^4}\right] \cdot \mathbf{F}
```

with the second-order equilibrium $`f_i^{\mathrm{eq}} = w_i\rho[1 + 3\,\mathbf{c}_i\cdot\mathbf{u} + \frac{9}{2}(\mathbf{c}_i\cdot\mathbf{u})^2 - \frac{3}{2}|\mathbf{u}|^2]`$, the moments $\rho = \sum_i f_i$ and $\rho\mathbf{u} = \sum_i \mathbf{c}_i f_i + \mathbf{F}/2$, and the force density $\mathbf{F} = (g, 0)$. Streaming moves $f_i^\star$ to $\mathbf{x} + \mathbf{c}_i$. A population that would cross a wall is reflected back to the node it left (half-way bounce-back):

```math
f_{\bar\imath}(\mathbf{x}_b, t + 1) = f_i^\star(\mathbf{x}_b, t)
```

### Exact Solution and Wall Slip

The steady solution of $`\nu\,u'' = -g`$ with $u(0) = u(H) = 0$ is

```math
u(y) = \frac{g}{2\nu}\,y\,(H - y), \qquad \nu = c_s^2\left(\tau - \frac{1}{2}\right), \qquad g = \frac{8\nu u_{\max}}{H^2}
```

With BGK collisions the computed profile is exactly this parabola plus a uniform slip velocity,

```math
u_s = \frac{g}{\nu}\,\frac{16\Lambda - 3}{24}, \qquad \Lambda = \left(\tau - \frac{1}{2}\right)^2
```

which is zero at $\tau = 1/2 + \sqrt{3/16} \approx 0.933$. Relative to the centreline velocity, $u_s/u_{\max} = (16\Lambda - 3)/(3H^2)$, so the error decreases as $1/H^2$ at every fixed $\tau$: half-way bounce-back is second order, with a $\tau$-dependent error constant.

## Implementation

- `advance(f, tau, force, n_steps, cx, cy, w, opposite)` is the Numba kernel: per node it computes the moments, the equilibrium and the Guo source, collides, and pushes the result to the neighbours, writing bounced-back populations into the opposite direction of the same node at the walls.
- `simulate_channel(width, tau)` sets the force with `driving_force`, initialises the populations with `equilibrium`, chooses the run length from `DECAY_TIMES`, and returns the node positions, the computed and the exact profile (`exact_profile`) and the number of steps.
- `predicted_slip(tau, force)` evaluates the slip formula; `relative_l2_error`, `convergence_study`, `slip_scan` and `observed_orders` produce the numbers in the figure.
- `make_figure` draws the three panels. The studies are set by `PROFILE_TAUS`, `RESOLUTIONS`, `CONVERGENCE_TAUS`, `SCAN_TAUS`, `SCAN_WIDTH` and `U_MAX`.

## Usage

```bash
python main.py                          # print the results and show the figure
python main.py --no-show --output .     # save lbm_poiseuille_validation.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints:

```text
H = 8, tau = 0.6: 3891 steps, relative L2 error 2.025e-02
H = 8, tau = 1: 779 steps, relative L2 error 7.131e-03
H = 8, tau = 2: 260 steps, relative L2 error 2.353e-01
tau = 0.8: errors 1.11e-02, 2.78e-03, 6.95e-04, 1.74e-04, 4.35e-05; observed orders 2.000, 2.000, 2.000, 2.000
tau = 1: errors 7.13e-03, 1.78e-03, 4.46e-04, 1.11e-04, 2.79e-05; observed orders 2.000, 2.000, 2.000, 2.000
tau = 1.5: errors 9.27e-02, 2.32e-02, 5.79e-03, 1.45e-03, 3.62e-04; observed orders 2.000, 2.000, 2.000, 2.000
max |measured - predicted| slip (units of g/nu): 1.51e-09
tau = 0.9330 (exact wall location), H = 16: relative L2 error 4.20e-12
```

![Poiseuille flow validation of the D2Q9 BGK lattice Boltzmann method](lbm_poiseuille_validation.png)

Panel (a) shows the steady profiles on a channel only 8 nodes wide: at $\tau = 0.6$ and $\tau = 1$ the nodes lie close to the parabola, while at $\tau = 2$ the whole profile is lifted by the wall slip, a 24% error. Panel (b) shows the relative $L_2$ error decreasing with slope $-2$ for every $\tau$; the observed orders are 2.000 to four digits because the error is a pure slip, whose size relative to $u_{\max}$ scales exactly as $H^{-2}$. Panel (c) shows that the measured slip, in units of $g/\nu$, lies on the curve $(16\Lambda - 3)/24$ to within $2 \times 10^{-9}$: it is negative for small $\tau$, zero at $\tau \approx 0.933$, where the profile error drops to $4 \times 10^{-12}$, and grows quadratically beyond.

## Related Notes

- [The Lattice Boltzmann Algorithm](../../../notes/numerical/lattice_boltzmann/lattice_boltzmann_algorithm.md)
- [The Lattice Boltzmann Method in Practice](../../../notes/numerical/lattice_boltzmann/practical_lbm.md)
- [From Boltzmann to Lattice Boltzmann](../../../notes/numerical/lattice_boltzmann/from_boltzmann_to_lattice_boltzmann.md)
- [Introduction to the Lattice Boltzmann Method](../../../notes/numerical/lattice_boltzmann/intro.md)
