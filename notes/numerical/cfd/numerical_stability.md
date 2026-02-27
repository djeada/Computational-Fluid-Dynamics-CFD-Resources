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
\frac{u_i^n - u_i^{n-1}}{\Delta t} + c \frac{u_i^n - u_{i-1}^n}{\Delta x} = O(\Delta t, \Delta x)
$$

- **Solution for $u_i^n$:**

$$
u_i^n = \left[1 - \left(\frac{c \Delta t}{\Delta x}\right)\right] u_i^{n-1} + \left(\frac{c \Delta t}{\Delta x}\right) u_{i-1}^n
$$

### Explicit Scheme
- **Definition:**
  - An explicit expression allows the value of $u_i^n$ at any grid point to be calculated directly without matrix inversion.
  - Example scheme: 

$$
\frac{u_i^n - u_i^{n-1}}{\Delta t} + c \frac{u_i^{n-1} - u_{i-1}^{n-1}}{\Delta x} = O(\Delta t, \Delta x)
$$

  - Solving for $u_i^n$:

$$
u_i^n = \left[1 - \left(\frac{c \Delta t}{\Delta x}\right)\right] u_i^{n-1} + \left(\frac{c \Delta t}{\Delta x}\right) u_{i-1}^{n-1}
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
\frac{u_i^n - u_i^{n-1}}{\Delta t} + c \frac{u_i^n - u_{i-1}^n}{\Delta x} = O(\Delta t, \Delta x)
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
|---|---|
| **Inputs** | Wave speed $c$, grid spacing $\Delta x$, time step $\Delta t$, choice of explicit or implicit scheme |
| **Outputs** | Maximum allowable time step $\Delta t_{\max}$, Courant number $C$, stable or unstable solution behavior |

## Related Python Scripts

| Script | Description |
|---|---|
| `scripts/simulations/1d_heat_and_wave_equations/main.py` | Solves the 1-D heat and wave equations with explicit time-stepping, demonstrating CFL stability constraints in practice. |
| `scripts/simulations/2d_wave_simulation/main.py` | 2-D wave equation solver whose time step must respect the CFL condition to remain stable. |
