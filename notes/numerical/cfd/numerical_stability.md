# Numerical Stability

## Convergence of Iterations

- In some examples, iterations converge rapidly, with the residual falling below $10^{-9}$ in just 6 iterations.
- In more complex problems, iterations converge more slowly and may even diverge.
- Understanding the conditions for convergence a priori is crucial and determined by stability analysis.

## Stability Analysis

- A numerical method is **stable** if the iterative process converges and **unstable** if it diverges.
- Exact stability analysis for Euler or Navier-Stokes equations is not possible.
- Stability analysis of simpler model equations provides useful insight and approximate conditions for stability.

## Time-Marching to Steady State

### Approach

- Common strategy in CFD for steady problems: solve unsteady equations and march the solution in time until it converges to a steady state.
- Stability analysis is performed in the context of time-marching.

### Goal

- Accurately obtain the asymptotic behavior at large times.
- Use the largest possible time-step $\Delta t$ to reach steady state with the least number of steps.

### Maximum Allowable Time-Step

- There is usually a maximum allowable time-step $\Delta t_{max}$.
- If $\Delta t > \Delta t_{max}$, numerical errors grow exponentially, causing divergence.
- The value of $\Delta t_{max}$ depends on the numerical discretization scheme used.

## Explicit and Implicit Schemes

### Example: Wave Equation

- **Wave Equation:**

$$
\frac{\partial u}{\partial t} + c \frac{\partial u}{\partial x} = 0
$$

where $c$ is the wave speed.

- **Discretization at Grid Point $i$ and Time-Level $n$:**

$$
\frac{u_i^n - u_i^{n-1}}{\Delta t} + c
\frac{u_i^n - u_{i-1}^n}{\Delta x} = O(\Delta t, \Delta x)
$$

- **Solution for $u_i^n$:**

$$
u_i^n = \frac{u_i^{n-1} + \left(\frac{c \Delta t}{\Delta x}\right) u_{i-1}^n}{1 + \frac{c \Delta t}{\Delta x}}
$$

### Explicit Scheme

- **Definition:**
  - An explicit expression allows the value of $u_i^n$ at any grid point to be calculated directly without matrix inversion.
  - Example scheme:

$$
\frac{u_i^n - u_i^{n-1}}{\Delta t} + c
\frac{u_i^{n-1} - u_{i-1}^{n-1}}{\Delta x} = O(\Delta t, \Delta x)
$$

- Solving for $u_i^n$:

$$
u_i^n = \left[1 - \left(\frac{c \Delta t}{\Delta x}\right)\right] u_i^{n-1} +
\left(\frac{c \Delta t}{\Delta x}\right) u_{i-1}^{n-1}
$$

- **Advantages:**

  - Easy to implement on a computer.
  - Each grid point can be updated independently.

- **Stability Condition:**

  - Stable only when the Courant number $C$ satisfies:

$$
C = \frac{c \Delta t}{\Delta x} \leq 1
$$

- This condition is known as the Courant-Friedrichs-Lewy (CFL) condition.
- The CFL condition imposes a severe limitation on $\Delta t_{max}$.

### Implicit Scheme

- **Definition:**
  - Evaluates the spatial derivative term at the $n$ time-level:

$$
\frac{u_i^n - u_i^{n-1}}{\Delta t} + c
\frac{u_i^n - u_{i-1}^n}{\Delta x} = O(\Delta t, \Delta x)
$$

- **Implementation:**

  - Requires solving a system of algebraic equations to calculate values at all grid points simultaneously.

- **Advantages:**

  - Unconditionally stable for the wave equation, meaning numerical errors are damped regardless of the time-step size.

### Stability Comparison for Wave Equation

- **Explicit Scheme:**
  - Stability limited by CFL condition.
- **Implicit Scheme:**
  - Unconditionally stable, allowing larger time-steps.

## Application to Euler and Navier-Stokes Equations

- **Explicit Schemes:**
  - Same restriction as the wave equation: Courant number $\leq 1$.
- **Implicit Schemes:**
  - Not unconditionally stable due to nonlinearities in the governing equations.
  - Allow larger Courant numbers than explicit schemes.
  - The maximum allowable Courant number is problem-dependent.

## Key Points on Numerical Stability

1. **Setting the Courant Number:**

   - CFD codes allow setting the Courant number (CFL number) for time-stepping.
   - Larger time-steps lead to faster convergence to a steady state.
   - Set the Courant number as large as possible within stability limits for steady problems.

2. **Adjusting Courant Number During Simulation:**

   - Lower Courant numbers might be needed during startup due to high nonlinearity.
   - Increase the Courant number as the solution progresses towards steady state.

3. **Numerical Stability and Scheme Choice:**

   - **Explicit Schemes:**
     - Simpler to implement.
     - Strict stability constraints (CFL condition).
   - **Implicit Schemes:**
     - More complex and computationally intensive.
     - Greater stability and larger allowable time-steps.

## Purpose in CFD

Choosing a time step that is too large can cause exponential error growth and solver divergence. This note explains stability analysis for explicit and implicit time-stepping schemes using the wave equation as a model problem. It introduces the Courant–Friedrichs–Lewy (CFL) condition $C = c\Delta t / \Delta x \le 1$ for explicit schemes and discusses practical strategies for setting the Courant number during a CFD simulation.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Wave speed $c$, grid spacing $\Delta x$, time step $\Delta t$, choice of explicit or implicit scheme |
| **Outputs** | Maximum allowable time step $\Delta t_{\max}$, Courant number $C$, stable or unstable solution behavior |

## Related Scripts

- [1D Heat and Wave Equation Simulations](../../../scripts/simulations/1d_heat_and_wave_equations/): solves the 1D heat equation with the implicit Crank–Nicolson scheme and the 1D wave equation with the explicit leapfrog scheme, animating both from the same initial Gaussian pulse.
- [2D Schrödinger Equation Simulation](../../../scripts/simulations/schroedinger_equation/): solves the time-dependent Schrödinger equation for a free particle in two dimensions with the split-step Fourier method and animates the probability density of the spreading wavepacket as a 3D surface.
- [2D Wave Equation Simulation](../../../scripts/simulations/2d_wave_simulation/): solves the 2D scalar wave equation on a square domain with an explicit leapfrog finite difference scheme and animates the result as a 3D surface.
- [Kelvin-Helmholtz Instability Simulation](../../../scripts/simulations/kelvin_helmholtz_instability/): simulates the Kelvin-Helmholtz instability, the rolling-up of a shear layer between fluid streams moving in opposite directions, in a periodic 2D incompressible flow animated with Matplotlib.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Rayleigh-Bénard Convection Simulation](../../../scripts/simulations/rayleigh_benard_convection/): simulates Rayleigh-Bénard convection, the buoyancy-driven flow in a fluid layer heated from below and cooled from above, and animates the temperature field with Matplotlib.
- [Simplified Real-Time Fluid Dynamics Simulator](../../../scripts/simulations/simplified_real_time_fluid_dynamics_simulator/): is an interactive 2D smoke simulation that uses Jos Stam's Stable Fluids algorithm (1999) to approximate the incompressible Navier-Stokes equations fast enough to run in real time in a Matplotlib window.

## Exercises

**Exercise 1.** An acoustic pulse travels at $c = 340$ m/s on a grid with $\Delta x = 1$ mm. What is $\Delta t_{\max}$ for the explicit upwind scheme, and how many time steps does it take to simulate 0.01 s?

<details>
<summary>Answer</summary>

$\Delta t_{\max} = \Delta x/c = 10^{-3}/340 \approx 2.94 \times 10^{-6}$ s.

The number of steps is $0.01/2.94 \times 10^{-6} = 3400$.

</details>

**Exercise 2.** Use von Neumann analysis on the explicit scheme $u_i^n = (1 - C)u_i^{n-1} + C u_{i-1}^{n-1}$. Substitute $u_i^n = G^n e^{\mathrm{i}i\theta}$ (with $\mathrm{i}$ the imaginary unit and $\theta$ the phase angle per cell) to find the amplification factor $G$ and $|G|^2$. Evaluate $|G|$ at $\theta = \pi$ for $C = 0.5$ and $C = 1.2$, and derive the stability condition.

<details>
<summary>Answer</summary>

$G = 1 - C + C e^{-\mathrm{i}\theta}$, and

```math
|G|^2 = (1 - C + C\cos\theta)^2 + C^2\sin^2\theta = 1 - 2C(1 - C)(1 - \cos\theta)
```

At $\theta = \pi$: $G = 1 - 2C$. For $C = 0.5$, $|G| = 0$ (the shortest wave is removed in one step). For $C = 1.2$, $|G| = 1.4$, so errors grow by 40% per step.

$|G| \le 1$ for every $\theta$ requires $C(1 - C) \ge 0$, that is $0 \le C \le 1$. This is the CFL condition in the note.

</details>

**Exercise 3.** Repeat the analysis for the implicit scheme $\frac{u_i^n - u_i^{n-1}}{\Delta t} + c\frac{u_i^n - u_{i-1}^n}{\Delta x} = 0$. Show that it is unconditionally stable and evaluate $|G|$ at $C = 5$ for $\theta = \pi$ and $\theta = \pi/2$. What does this mean for accuracy?

<details>
<summary>Answer</summary>

$G(1 + C - Ce^{-\mathrm{i}\theta}) = 1$, so

```math
|G|^2 = \frac{1}{1 + 2C(1 + C)(1 - \cos\theta)} \le 1 \quad \text{for all } C \ge 0
```

and the scheme is unconditionally stable.

At $C = 5$: $|G| = 1/11 \approx 0.091$ for $\theta = \pi$ and $|G| \approx 0.128$ for $\theta = \pi/2$.

Large time steps are stable but heavily damp everything except long waves. That is fine for marching to a steady state, but it destroys time accuracy in unsteady problems.

</details>

**Exercise 4.** On a periodic grid, apply two steps of the explicit scheme with $C = 0.5$ to $u^0 = (0, 0, 1, 0, 0)$, with the flow moving towards larger $i$. Then describe what happens with $C = 1$.

<details>
<summary>Answer</summary>

$u_i^n = 0.5u_i^{n-1} + 0.5u_{i-1}^{n-1}$:

- Step 1: $(0, 0, 0.5, 0.5, 0)$
- Step 2: $(0, 0, 0.25, 0.5, 0.25)$

The pulse moves right while spreading out (numerical diffusion), and the sum stays 1.

With $C = 1$ the update is $u_i^n = u_{i-1}^{n-1}$, an exact shift by one cell per step with no diffusion. That is the special case where the upwind scheme reproduces the exact solution.

</details>

**Exercise 5.** A steady solution is reached by marching the model equation until $t = 5L/c$, with $L = 1$ m, $c = 1$ m/s and $\Delta x = 0.01$ m. Compare the number of steps for the explicit scheme at $C = 0.9$ and the implicit scheme at $C = 20$. What is the trade-off?

<details>
<summary>Answer</summary>

Explicit: $\Delta t = 0.009$ s, so $5/0.009 \approx 556$ steps.

Implicit: $\Delta t = 0.2$ s, so 25 steps.

Each implicit step needs a linear system to be solved, so it costs more than an explicit update. For steady problems, and especially for the nonlinear Euler and Navier–Stokes equations where the allowed Courant number depends on the problem, the implicit approach usually wins. This is why the note recommends using the largest stable Courant number and increasing it as the solution settles.

</details>

## References

- Courant, R., Friedrichs, K., & Lewy, H., "Über die partiellen Differenzengleichungen der mathematischen Physik", *Mathematische Annalen* 100, 1928.
- LeVeque, R. J., *Finite Difference Methods for Ordinary and Partial Differential Equations*, SIAM, 2007.
- Strikwerda, J. C., *Finite Difference Schemes and Partial Differential Equations*, 2nd ed., SIAM, 2004.
- Hirsch, C., *Numerical Computation of Internal and External Flows*, Vol. 1, 2nd ed., Butterworth-Heinemann, 2007.
- Anderson, J. D., *Computational Fluid Dynamics: The Basics with Applications*, McGraw-Hill, 1995.
