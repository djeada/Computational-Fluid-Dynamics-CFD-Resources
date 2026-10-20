# Double Pendulum from Lagrange's Equations

This script integrates the Lagrange equations of a planar double pendulum and compares its small-amplitude motion with the normal modes of the linearized equations. Two 1 kg point masses on massless 1 m rods are released in each linear mode shape, from a mixed small-amplitude state and from a large-amplitude state that produces chaotic motion, and the drift of the total energy is used to check the integration.

## Overview

- Solves the two coupled Lagrange equations for $\ddot{\theta}_1$ and $\ddot{\theta}_2$ at every evaluation and integrates the first-order system with `solve_ivp(method="RK45")` at `rtol = 1e-10`.
- Linearizes about the hanging equilibrium to obtain $\mathbf{M}\ddot{\mathbf{q}} + \mathbf{K}\mathbf{q} = \mathbf{0}$ and solves $\mathbf{K}\boldsymbol{\phi} = \omega^2\mathbf{M}\boldsymbol{\phi}$.
- Releases the nonlinear system from rest in each mode shape with a largest angle of 0.02 rad and measures its frequency from the zero crossings of $\theta_1$ over 40 s.
- Computes the spectrum of a release from $\theta_1 = 0.02$ rad, $\theta_2 = 0$, which excites both modes.
- Releases the system from $\theta_1 = 120^\circ$, $\theta_2 = -10^\circ$, draws the path of the lower bob and tracks $E = T + V$.

## Mathematical Background

With generalized coordinates $\theta_1$, $\theta_2$ measured from the downward vertical and $\delta = \theta_1 - \theta_2$,

```math
T = \tfrac{1}{2}(m_1 + m_2)l_1^2\dot{\theta}_1^2 + \tfrac{1}{2}m_2l_2^2\dot{\theta}_2^2 + m_2l_1l_2\dot{\theta}_1\dot{\theta}_2\cos\delta,
\qquad
V = -(m_1 + m_2)gl_1\cos\theta_1 - m_2gl_2\cos\theta_2
```

and $\frac{d}{dt}(\partial L/\partial\dot{\theta}_i) - \partial L/\partial\theta_i = 0$ with $L = T - V$ gives

```math
\begin{aligned}
(m_1 + m_2)l_1\ddot{\theta}_1 + m_2l_2\cos\delta\,\ddot{\theta}_2 &= -m_2l_2\sin\delta\,\dot{\theta}_2^2 - (m_1 + m_2)g\sin\theta_1 \\
l_1\cos\delta\,\ddot{\theta}_1 + l_2\ddot{\theta}_2 &= l_1\sin\delta\,\dot{\theta}_1^2 - g\sin\theta_2
\end{aligned}
```

Keeping second-order terms of $T$ and $V$ about $\theta_1 = \theta_2 = 0$ gives

```math
\mathbf{M} = \begin{bmatrix} (m_1 + m_2)l_1^2 & m_2l_1l_2 \\ m_2l_1l_2 & m_2l_2^2 \end{bmatrix},
\qquad
\mathbf{K} = \begin{bmatrix} (m_1 + m_2)gl_1 & 0 \\ 0 & m_2gl_2 \end{bmatrix}
```

For equal masses and lengths $\omega^2 = (g/l)(2 \mp \sqrt{2})$ with mode shapes $\theta_2/\theta_1 = \pm\sqrt{2}$. The exact system conserves $E$, so $E(t) - E(0)$ measures the integration error.

## Implementation

- `accelerations(theta1, theta2, omega1, omega2)` solves the 2 × 2 system above by Cramer's rule; `rhs` wraps it for `solve_ivp`.
- `energy(state)` and `energy_drift(states)` give $E$ and the drift relative to the energy above the rest state, $E_0 - E_{\mathrm{rest}}$.
- `linearized_matrices()` and `linear_modes()` return $\mathbf{M}$, $\mathbf{K}$ and the eigenpairs from `scipy.linalg.eigh`.
- `integrate(state0, duration)` runs RK45 with output every 5 ms; `measured_frequency(t, signal)` interpolates the upward zero crossings.
- `small_amplitude_study()` runs one release per mode; `make_figure` draws the four panels.

## Usage

```bash
python main.py                          # print the frequency comparison and show the figure
python main.py --no-show --output .     # save dynamics_double_pendulum_lagrange.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The linearized frequencies are 2.39720 and 5.78735 rad/s (0.382 and 0.921 Hz), equal to the closed form. The nonlinear releases at 0.02 rad oscillate at 2.39716 and 5.78521 rad/s, within 0.04% of the linear values; the small shift is the amplitude dependence of a pendulum's frequency. The large-amplitude run keeps $`|E - E_0|/(E_0 - E_{\mathrm{rest}})`$ below $1.4\times10^{-9}$ over 20 s.

![Double pendulum modes, spectrum, chaotic path and energy drift](dynamics_double_pendulum_lagrange.png)

Panel (a) shows the in-phase lower mode and the out-of-phase upper mode, each a single harmonic in both angles. Panel (b) shows the two spectral lines of the mixed release sitting on the linearized frequencies. Panel (c) shows the irregular path of the lower bob after a large release. Panel (d) shows that RK45, which is not symplectic, lets the energy of the regular runs drift slowly and steadily, about $10^{-8}$ in 40 s, while the error in the chaotic run stays bounded but noisy.

## Related Notes

- [Lagrangian Mechanics](../../../notes/applied_mechanics/dynamics/lagrangian_mechanics.md)
- [Mechanical Vibrations](../../../notes/applied_mechanics/dynamics/vibrations.md)
- [Work and Energy Methods](../../../notes/applied_mechanics/dynamics/work_energy.md)
