# Torque-Free Rigid Body Rotation

This script integrates Euler's equations for a rigid box spinning with no applied moment and shows that rotation about the axis of intermediate moment of inertia is unstable. A 0.5 kg box of 200 × 100 × 30 mm is spun at 10 rad/s about each principal axis with a 1% disturbance, and its kinetic energy and angular momentum magnitude are tracked as checks on the integration.

## Overview

- Computes the principal moments of inertia of a uniform rectangular box, $I_1 < I_2 < I_3$.
- Integrates the torque-free Euler equations in body axes with `solve_ivp(method="DOP853")` at `rtol = 1e-11`.
- Starts each run with $\omega = \Omega$ about one axis and $0.01\Omega$ about the other two.
- Compares the motion with the linearized wobble frequencies about axes 1 and 3 and the growth rate about axis 2.
- Reports the relative change of $T$ and $|\mathbf{H}_G|$, both exact invariants.

## Mathematical Background

In principal body axes with no applied moment, $\sum\mathbf{M}_G = \dot{\mathbf{H}}_G = \mathbf{0}$ becomes

```math
I_1\dot{\omega}_1 = (I_2 - I_3)\,\omega_2\omega_3,
\qquad
I_2\dot{\omega}_2 = (I_3 - I_1)\,\omega_3\omega_1,
\qquad
I_3\dot{\omega}_3 = (I_1 - I_2)\,\omega_1\omega_2
```

For a spin $\Omega$ about axis 1 with small $\omega_2$, $\omega_3$, eliminating one component gives $`\ddot{\omega}_2 = \Omega^2(I_3 - I_1)(I_1 - I_2)/(I_2I_3)\,\omega_2`$. The coefficient is negative when $I_1$ is the smallest or the largest moment, so the disturbance oscillates, and positive when it is the intermediate one, so the disturbance grows. For spin about axis 2 the growth rate is

```math
\lambda = \Omega\sqrt{\frac{(I_2 - I_1)(I_3 - I_2)}{I_1I_3}}
```

and the wobble frequencies about axes 1 and 3 are $\Omega\sqrt{(I_2 - I_1)(I_3 - I_1)/(I_2I_3)}$ and $\Omega\sqrt{(I_3 - I_1)(I_3 - I_2)/(I_1I_2)}$. The exact solution conserves $T = \tfrac{1}{2}\sum I_i\omega_i^2$ and $|\mathbf{H}_G|^2 = \sum I_i^2\omega_i^2$.

## Implementation

- `principal_inertia()` returns $m(b^2 + c^2)/12$, $m(a^2 + c^2)/12$ and $m(a^2 + b^2)/12$ for the edges `LENGTH`, `WIDTH` and `THICKNESS`.
- `euler_rhs(t, omega, inertia)` evaluates the three equations; `spin(axis, ...)` integrates one case.
- `invariants(omega, inertia)` returns $T$ and $|\mathbf{H}_G|$ along a solution.
- `linear_rates(inertia)` returns the two wobble frequencies and the growth rate.
- `make_figure()` draws the three runs side by side.

## Usage

```bash
python main.py                          # print the rates and invariants, show the figure
python main.py --no-show --output .     # save dynamics_torque_free_rigid_body.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The principal moments are $4.54\times10^{-4}$, $1.70\times10^{-3}$ and $2.08\times10^{-3}$ kg m². The linearized wobble frequencies about axes 1 and 3 are 7.57 and 8.93 rad/s and the growth rate about axis 2 is 7.08 s⁻¹. In the axis-2 run $\omega_2$ reverses completely, reaching $-\Omega$; in the other two runs the spin component stays at $\Omega$. The relative changes of $T$ and $|\mathbf{H}_G|$ are below $4\times10^{-11}$ in all three runs.

![Torque-free rotation about the three principal axes](dynamics_torque_free_rigid_body.png)

Panels (a) and (c) show small bounded wobbles about the axes of smallest and largest inertia. Panel (b) shows the intermediate-axis spin flipping sign about every 1.8 s, with $\omega_1$ and $\omega_3$ pulsing during each flip, while the invariants printed in the panel stay constant.

## Related Notes

- [Rigid Body Kinetics](../../../notes/applied_mechanics/dynamics/rigid_body_kinetics.md)
- [Impulse and Momentum](../../../notes/applied_mechanics/dynamics/impulse_momentum.md)
