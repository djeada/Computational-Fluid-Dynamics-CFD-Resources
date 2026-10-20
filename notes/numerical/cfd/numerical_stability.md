# Numerical Stability

A discretization can be consistent with the governing equations and still produce numbers that grow without bound. Stability analysis predicts, before a run, which combinations of scheme, time step and grid spacing keep errors bounded. This note covers the theory that links consistency, stability and convergence, von Neumann analysis of the classic advection and diffusion schemes, the CFL condition, implicit schemes, the modified equation that explains numerical diffusion, and the practical time-step limits of Euler and Navier–Stokes solvers, including local time stepping for steady problems.

The choice of time integrator for the semi-discrete equations, with stability regions in the complex plane, is treated in [Time Integration](time_integration.md). Convergence of the iterations inside a time step or a steady solve is a different question, covered in [Iterative Convergence](iterative_convergence.md).

## Problem Statement

Consider a linear partial differential equation with an initial condition, for example linear advection or diffusion of a scalar $\phi(x, t)$,

$$
\frac{\partial \phi}{\partial t} + u \frac{\partial \phi}{\partial x} = 0
\qquad \text{or}
\qquad \frac{\partial \phi}{\partial t} = \nu \frac{\partial^2 \phi}{\partial x^2}
$$

with constant velocity $u$ or diffusivity $\nu$, discretized on a grid $x_i = i\Delta x$, $t^n = n\Delta t$. A two-level scheme advances the grid values $\boldsymbol{\phi}^n = (\phi_i^n)$ by a linear operator, $\boldsymbol{\phi}^{n+1} = L_h\boldsymbol{\phi}^n$. The questions are:

1. Does the numerical solution stay bounded as $n \to \infty$ at fixed $\Delta t$ and $\Delta x$, and as the grid is refined at a fixed ratio such as the Courant number $C = u\Delta t/\Delta x$ or the diffusion number $r = \nu\Delta t/\Delta x^2$?
2. What is the largest stable time step $\Delta t_{\max}$?
3. How are the amplitude and the phase of each Fourier component of the solution changed by the scheme?

A scheme is acceptable when it is stable for the time step used and its damping and phase errors are small for the wavelengths that matter. The difficulty is that the Euler and Navier–Stokes equations are nonlinear, have variable coefficients and boundaries, so exact stability analysis is not possible. Analysis of linear model equations with frozen coefficients gives conditions that are necessary and, in practice, close to the real limits.

## Consistency, Stability and Convergence

Let $\phi(x_i, t^n)$ be the exact solution sampled on the grid. The local truncation error $\tau_i^n$ is the residual left when the exact solution is substituted into the scheme, divided by $\Delta t$:

$$
\tau_i^n = \frac{\phi(x_i, t^{n+1}) - \left(L_h \boldsymbol{\phi}(t^n)\right)_i}{\Delta t}
$$

| Property | Definition |
| --- | --- |
| Consistency | $\tau \to 0$ as $\Delta t, \Delta x \to 0$; the scheme has order $(p, q)$ if $\tau = O(\Delta t^p + \Delta x^q)$ |
| Stability | $`\lVert L_h^n\rVert \le K`$ for all $n\Delta t \le T$, with $K$ independent of $\Delta t$ and $\Delta x$ |
| Convergence | $`\max_i \lvert\phi_i^n - \phi(x_i, t^n)\rvert \to 0`$ as the grid is refined, for $n\Delta t \le T$ |

The **Lax equivalence theorem** (Lax and Richtmyer, 1956) states that for a consistent finite-difference approximation of a well-posed linear initial-value problem, stability is necessary and sufficient for convergence. The proof also gives the error bound

```math
\|\mathbf{e}^n\| \le K\, T\,\max_{m < n}\|\boldsymbol{\tau}^m\|
```

so a stable scheme converges with the order of its truncation error. Consistency is usually checked by Taylor expansion; stability is the property that needs analysis.

## Von Neumann Analysis

On a periodic grid any error can be written as a sum of Fourier modes. A linear scheme with constant coefficients maps each mode onto itself, multiplied by an **amplification factor** $G(\theta)$:

```math
\phi_i^n = G^n e^{\mathrm{i}\,i\theta},
\qquad \theta = k\Delta x \in [0, \pi]
```

where $\mathrm{i}$ is the imaginary unit and $\theta$ the phase angle per cell ($\theta = \pi$ is the shortest wave the grid can carry, two cells long). The procedure is:

1. Substitute $`\phi_i^n = G^n e^{\mathrm{i}\,i\theta}`$ into the scheme and divide by $`G^n e^{\mathrm{i}\,i\theta}`$; neighbours become $e^{\pm\mathrm{i}\theta}$.
2. Solve for $G(\theta)$, which depends on $C$ or $r$.
3. Require $|G(\theta)| \le 1$ for all $\theta$ (for problems whose exact solution grows, $|G| \le 1 + O(\Delta t)$ suffices).

### FTCS for Diffusion

Forward in time and central in space,

$$
\phi_i^{n+1} = \phi_i^n + r\left(\phi_{i+1}^n - 2\phi_i^n + \phi_{i-1}^n\right)
$$

gives $G = 1 + r(e^{\mathrm{i}\theta} - 2 + e^{-\mathrm{i}\theta}) = 1 - 2r(1 - \cos\theta)$, that is

$$
G(\theta) = 1 - 4r\sin^2 \frac{\theta}{2}
$$

$G$ is real and at most 1. The condition $G \ge -1$ is most restrictive at $\theta = \pi$, where $G = 1 - 4r$, so the scheme is stable if and only if

```math
r = \frac{\nu\,\Delta t}{\Delta x^2} \le \frac{1}{2}
```

At $r = 1/2$ the two-cell wave flips sign every step without decaying; above it, that wave grows. The time step must shrink with the square of the grid spacing, which makes explicit diffusion expensive on fine grids.

### FTCS for Advection

The same idea for advection, $\phi_i^{n+1} = \phi_i^n - \frac{C}{2}(\phi_{i+1}^n - \phi_{i-1}^n)$, gives

```math
G = 1 - \mathrm{i}\, C\sin\theta,
\qquad |G|^2 = 1 + C^2\sin^2\theta
```

which exceeds 1 for every $C > 0$ and every $\theta$ except $0$ and $\pi$. Forward Euler with central differencing of a first derivative is unconditionally unstable, however small the time step.

### First-Order Upwind

For $u > 0$ the upwind scheme takes the spatial difference from the side the information comes from:

$$
\phi_i^{n+1} = \phi_i^n - C\left(\phi_i^n - \phi_{i-1}^n\right)
$$

so $G = 1 - C + Ce^{-\mathrm{i}\theta}$ and

$$
|G|^2 = (1 - C + C\cos\theta)^2 + C^2\sin^2\theta = 1 - 2C(1 - C)(1 - \cos\theta)
$$

$|G| \le 1$ for all $\theta$ if and only if $C(1 - C) \ge 0$, that is $0 \le C \le 1$. At $C = 1$ the update is $\phi_i^{n+1} = \phi_{i-1}^n$, an exact shift by one cell.

### Lax–Friedrichs and Lax–Wendroff

Lax–Friedrichs replaces $\phi_i^n$ in FTCS by the average of its neighbours, and Lax–Wendroff adds the second-order term that a Taylor expansion in time requires ($\phi_{tt} = u^2\phi_{xx}$):

```math
\text{LF:}\ \ \phi_i^{n+1} = \tfrac{1}{2}\left(\phi_{i+1}^n + \phi_{i-1}^n\right) - \tfrac{C}{2}\left(\phi_{i+1}^n - \phi_{i-1}^n\right),
\qquad
\text{LW:}\ \ \phi_i^{n+1} = \phi_i^n - \tfrac{C}{2}\left(\phi_{i+1}^n - \phi_{i-1}^n\right) + \tfrac{C^2}{2}\left(\phi_{i+1}^n - 2\phi_i^n + \phi_{i-1}^n\right)
```

Their amplification factors are

```math
|G_{\mathrm{LF}}|^2 = 1 - (1 - C^2)\sin^2\theta,
\qquad
|G_{\mathrm{LW}}|^2 = 1 - 4C^2(1 - C^2)\sin^4\frac{\theta}{2}
```

and both are stable for $|C| \le 1$. Lax–Wendroff is second-order accurate; its damping starts at $\sin^4(\theta/2)$, so long waves are hardly damped at all.

### Summary and Figure

| Scheme | Equation | $G(\theta)$ | Stable for | Order |
| --- | --- | --- | --- | --- |
| FTCS | advection | $1 - \mathrm{i}C\sin\theta$ | never | 1 in time, 2 in space |
| Upwind | advection | $1 - C(1 - e^{-\mathrm{i}\theta})$ | $0 \le C \le 1$ | 1 |
| Lax–Friedrichs | advection | $\cos\theta - \mathrm{i}C\sin\theta$ | $\lvert C\rvert \le 1$ | 1 |
| Lax–Wendroff | advection | $1 - \mathrm{i}C\sin\theta - C^2(1 - \cos\theta)$ | $\lvert C\rvert \le 1$ | 2 |
| FTCS | diffusion | $1 - 4r\sin^2(\theta/2)$ | $r \le 1/2$ | 1 in time, 2 in space |
| BTCS | diffusion | $1/(1 + 4r\sin^2(\theta/2))$ | all $r$ | 1 in time, 2 in space |
| Crank–Nicolson | diffusion | $`\dfrac{1 - 2r\sin^2(\theta/2)}{1 + 2r\sin^2(\theta/2)}`$ | all $r$ | 2 |

![Amplification factors, phase errors and square-wave tests of the classic schemes](../../../scripts/algorithms/von_neumann_amplification/von_neumann_amplification.png)

The exact solution of the advection equation multiplies each mode by $e^{-\mathrm{i}C\theta}$ per step, so $|G| < 1$ is numerical damping and a ratio $-\arg G/(C\theta) \ne 1$ is a wrong wave speed. In panel (d), after one period on 100 cells at $C = 0.8$, upwind has smeared the square wave, Lax–Friedrichs has smeared it more and left a staircase ($|G(\pi)| = 1$, so odd and even cells decouple), and Lax–Wendroff keeps the edges sharper but leaves oscillations behind them, because its short waves travel too slowly (phase-speed ratio 0.97 at $\theta = \pi/4$). Panels (e) and (f) show the predicted blow-ups: FTCS advection grows by a factor $|G(\pi/2)| = 1.28$ per step and FTCS diffusion at $r = 0.55$ explodes through the $\theta = \pi$ mode.

### Limits of the Analysis

Von Neumann analysis assumes a periodic domain and constant coefficients. Boundary conditions can destabilize a scheme that passes the test; the normal-mode theory of Gustafsson, Kreiss and Sundström handles that case. For nonlinear equations the coefficients are frozen at local values ($u$ becomes the local velocity, or $|u| + c$ for the Euler equations), which gives a local condition that must hold everywhere. For systems of equations, $G$ becomes an amplification matrix and its eigenvalues must satisfy the condition.

## The CFL Condition

The exact solution of the advection equation at $(x_i, t^{n+1})$ depends only on the initial value at the foot of the characteristic, $x_i - u\Delta t$. An explicit three-point scheme can only use $x_{i-1}$, $x_i$ and $x_{i+1}$ at time $t^n$, so its numerical domain of dependence is $[x_{i-1}, x_{i+1}]$. If the characteristic leaves that interval the scheme cannot converge, whatever the coefficients, because the data that determine the exact solution never enter the computation. This argument of Courant, Friedrichs and Lewy (1928) gives the necessary condition

```math
C = \frac{|u|\,\Delta t}{\Delta x} \le 1
```

for three-point explicit schemes, and in general that the numerical domain of dependence must contain the physical one. It is necessary but not sufficient: FTCS satisfies it for $C \le 1$ and is still unstable. On multidimensional grids the unsplit first-order upwind scheme needs $C_x + C_y + C_z \le 1$ with $C_x = |u|\Delta t/\Delta x$ and so on, and FTCS diffusion needs $r_x + r_y + r_z \le 1/2$.

## Implicit Schemes

Evaluating the spatial terms at the new time level gives schemes that need a linear system to be solved every step but are stable for much larger time steps. Backward Euler with upwind differencing (BTCS upwind),

```math
\frac{\phi_i^{n+1} - \phi_i^n}{\Delta t} + u\,
\frac{\phi_i^{n+1} - \phi_{i-1}^{n+1}}{\Delta x} = 0
```

gives $G\left(1 + C - Ce^{-\mathrm{i}\theta}\right) = 1$, so

$$
|G|^2 = \frac{1}{1 + 2C(1 + C)(1 - \cos\theta)} \le 1 \quad \text{for all } C \ge 0
$$

and the scheme is unconditionally stable. BTCS and Crank–Nicolson are unconditionally stable for diffusion (table above).

Unconditional stability does not mean accuracy. At $C = 5$ the implicit upwind scheme multiplies the $\theta = \pi/2$ mode by 0.128 per step, so a wave that should travel unchanged disappears in a few steps. For marching to a steady state that damping is harmless, and even useful; for unsteady flows the time step must still be chosen for accuracy. Crank–Nicolson has $G(\pi) \to -1$ as $r \to \infty$: short waves are not damped but flip sign every step, which produces oscillations near steep gradients (panel (f) of the figure, and the discussion of L-stability in [Time Integration](time_integration.md)).

## Modified Equation and Numerical Diffusion

Expanding every term of a scheme in Taylor series about $(x_i, t^n)$ and using the scheme itself to replace time derivatives by space derivatives gives the **modified equation**, the PDE that the scheme actually solves to higher order (Warming and Hyett, 1974). For first-order upwind,

```math
\frac{\partial \phi}{\partial t} + u
\frac{\partial \phi}{\partial x} = \nu_{\mathrm{num}}
\frac{\partial^2 \phi}{\partial x^2} + O(\Delta x^2),
\qquad \nu_{\mathrm{num}} = \frac{u\,\Delta x}{2}(1 - C)
```

The scheme behaves like the advection–diffusion equation with an artificial viscosity proportional to $\Delta x$. This is why it smears fronts, why its stability requires $\nu_{\mathrm{num}} \ge 0$ (that is $C \le 1$), and why a first-order upwind solution of a convection-dominated flow can look plausible but correspond to a much lower Reynolds number. For $u = 1$ m/s, $\Delta x = 0.01$ m and $C = 0.8$, $\nu_{\mathrm{num}} = 10^{-3}$ m²/s, which is 67 times the kinematic viscosity of air.

For Lax–Wendroff the leading error is dispersive:

```math
\frac{\partial \phi}{\partial t} + u
\frac{\partial \phi}{\partial x} = -\frac{u\,\Delta x^2}{6}\left(1 - C^2\right)
\frac{\partial^3 \phi}{\partial x^3} + \dots
```

A third-derivative term changes the speed of each wave by an amount that depends on its wavelength, which is where the oscillations behind the square wave come from. Even-derivative error terms damp, odd-derivative terms disperse. Godunov's theorem states that no linear scheme of second order or higher can avoid such oscillations; the nonlinear limited schemes that get around it are the subject of [Convection Schemes](../fvm/convection_schemes.md).

## Stability of Euler and Navier–Stokes Solvers

### Convective and Acoustic Limit

The 1D Euler equations have the characteristic speeds $u - c$, $u$ and $u + c$, with $c$ the speed of sound. Freezing the coefficients and applying the CFL argument to the fastest wave gives, for an explicit scheme,

```math
\Delta t \le C_{\max}\, \frac{\Delta x}{|u| + c}
```

and in several dimensions a common estimate for cell $i$ is

$$
\Delta
t_i = \frac{C_{\max}}{\dfrac{|u| + c}{\Delta x} + \dfrac{|v| + c}{\Delta y} + \dfrac{|w| + c}{\Delta z}}
$$

$C_{\max}$ depends on the spatial scheme and the time integrator: about 1 for first-order upwind with forward Euler, and other values for Runge–Kutta methods, which follow from their stability regions ([Time Integration](time_integration.md)). In incompressible solvers the acoustic speed is absent and the convective limit uses $|u|$ alone. At low Mach number, $c \gg |u|$ makes a compressible explicit solver take time steps set by sound waves that carry no interest, which is the reason for low-Mach preconditioning or for pressure-based solvers.

### Viscous Limit

Explicit treatment of the viscous terms adds the diffusion limit

```math
\Delta t \le r_{\max}\, \frac{\Delta x^2}{\nu}
```

with $r_{\max} = 1/2$ in 1D for forward Euler, $1/4$ on a uniform 2D grid. Near walls, where the cells are thin in the wall-normal direction, this limit is usually far stricter than the convective one, and the viscous terms are treated implicitly. The two limits are combined in practice, for example as $`1/\Delta t = 1/\Delta t_{\mathrm{conv}} + 1/\Delta t_{\mathrm{visc}}`$.

### Implicit Solvers

For the nonlinear Euler and Navier–Stokes equations implicit schemes are not unconditionally stable in practice: the linearization is approximate, the Jacobian may be a lower-order approximation of the true one, and nonlinear effects such as moving shocks or separation can destabilize large steps. They do allow Courant numbers of tens to thousands, problem-dependent. CFD codes therefore let the user set the CFL number and often ramp it: a low value while strong transients and nonlinearity dominate the start-up, increased as the residuals fall.

## Local Time Stepping for Steady Problems

When only the steady state is wanted, the time derivative is a device for driving the residual to zero, and time accuracy is irrelevant. The semi-discrete system $d\boldsymbol{\phi}/dt = -\mathbf{R}(\boldsymbol{\phi})$ can then be marched with a different time step in every cell, each at the local stability limit:

```math
\frac{\Delta \boldsymbol{\phi}_i}{\Delta t_i} = -\mathbf{R}_i(\boldsymbol{\phi}),
\qquad \Delta t_i = C_{\max}\, \frac{\Delta x_i}{|u_i| + c_i}
```

Small cells near walls no longer limit the progress of large cells in the far field, which can save orders of magnitude in iterations on stretched grids. The converged solution satisfies $\mathbf{R}(\boldsymbol{\phi}) = \mathbf{0}$ and does not depend on the time steps, because they multiply the residual only. The intermediate states have no physical meaning, and the method must not be used for unsteady flows (dual time stepping in [Time Integration](time_integration.md) combines it with a time-accurate outer scheme). Implicit local time stepping with a CFL number that grows as the residual falls is the pseudo-transient continuation of [Dealing with Nonlinearity](dealing_with_nonlinearity.md).

## Key Takeaways

- For a consistent linear scheme, stability is equivalent to convergence (Lax equivalence theorem), so stability analysis is the main check on a new scheme.
- Von Neumann analysis gives $G(\theta)$ for each Fourier mode: $|G|$ measures damping, $\arg G$ measures phase error, and $|G| \le 1$ for all $\theta$ is the stability condition.
- Explicit diffusion needs $r = \nu\Delta t/\Delta x^2 \le 1/2$; explicit upwind advection needs $C \le 1$; FTCS advection is never stable.
- The CFL condition is necessary for every explicit scheme but not sufficient.
- First-order upwind adds the numerical viscosity $u\Delta x(1 - C)/2$; second-order linear schemes such as Lax–Wendroff produce dispersive oscillations instead.
- For the Euler equations the limit uses $|u| + c$, and viscous terms add a limit proportional to $\Delta x^2/\nu$.
- For steady problems, local time stepping at the largest stable CFL number, ramped up during the run, reaches the steady state fastest.

## Related Scripts

- [Von Neumann Amplification Factors](../../../scripts/algorithms/von_neumann_amplification/): computes the von Neumann amplification factor $G(\theta)$ of the classic finite-difference schemes for linear advection and diffusion and checks the predictions by marching a square wave with each scheme.
- [Stability Regions of Time Integrators](../../../scripts/algorithms/time_integrator_stability/): draws the absolute-stability regions of explicit Euler, RK2, RK3, RK4, AB2 and BDF2 and overlays the eigenvalues of semi-discrete advection and diffusion operators, so the stable pairings of a spatial scheme and a time integrator can be read off directly.
- [1D Heat and Wave Equation Simulations](../../../scripts/simulations/1d_heat_and_wave_equations/): solves the 1D heat equation with the implicit Crank–Nicolson scheme and the 1D wave equation with the explicit leapfrog scheme, animating both from the same initial Gaussian pulse.
- [Supersonic Forward-Facing Step](../../../scripts/simulations/supersonic_forward_facing_step/): solves the 2D compressible Euler equations for a Mach 3 stream that meets a forward-facing step in a wind tunnel, the benchmark of Woodward and Colella (1984), and animates the shock pattern that forms.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [2D Schrödinger Equation Simulation](../../../scripts/simulations/schroedinger_equation/): solves the time-dependent Schrödinger equation for a free particle in two dimensions with the split-step Fourier method and animates the probability density of the spreading wavepacket as a 3D surface.
- [2D Wave Equation Simulation](../../../scripts/simulations/2d_wave_simulation/): solves the 2D scalar wave equation on a square domain with an explicit leapfrog finite difference scheme and animates the result as a 3D surface.
- [Decaying 2D Turbulence](../../../scripts/simulations/decaying_2d_turbulence/): simulates freely decaying two-dimensional turbulence in a doubly periodic box and animates how a random vorticity field organises itself into coherent vortices that merge into ever larger ones.
- [Gray-Scott Reaction-Diffusion Simulation](../../../scripts/simulations/gray_scott_reaction_diffusion/): simulates the Gray-Scott reaction-diffusion system, in which two chemicals that react and diffuse on a periodic square turn a small seeded square into self-replicating spots or branching coral, and animates the concentration of one of them with Matplotlib.
- [Kelvin-Helmholtz Instability Simulation](../../../scripts/simulations/kelvin_helmholtz_instability/): simulates the Kelvin-Helmholtz instability, the rolling-up of a shear layer between fluid streams moving in opposite directions, in a periodic 2D incompressible flow animated with Matplotlib.
- [Mach Cone of a Moving Sound Source](../../../scripts/simulations/mach_cone_moving_source/): simulates the sound of a small source that accelerates from rest to twice the speed of sound and animates its pressure field, from the Doppler-compressed wavefronts of a subsonic source through the pile-up at Mach 1 to the Mach cone of a supersonic one.
- [Picard Iteration and Newton's Method for Steady Burgers](../../../scripts/algorithms/picard_vs_newton/): solves the discretized steady viscous Burgers equation, a 1D model of the convective nonlinearity in the Navier–Stokes equations, with Picard iteration and Newton's method and compares their convergence.
- [Raindrops on a Pond: Shallow-Water Ripples](../../../scripts/simulations/shallow_water_ripples/): simulates raindrops falling on a square basin of still water by solving the 2D shallow-water equations with a conservative finite-volume scheme, and animates the free surface as shaded relief.
- [Rayleigh-Bénard Convection Simulation](../../../scripts/simulations/rayleigh_benard_convection/): simulates Rayleigh-Bénard convection, the buoyancy-driven flow in a fluid layer heated from below and cooled from above, and animates the temperature field with Matplotlib.
- [Rayleigh-Taylor Instability](../../../scripts/simulations/rayleigh_taylor_instability/): simulates the Rayleigh-Taylor instability of heavy fluid resting on light fluid in a tall 2D box and animates how a rippled interface grows into rising bubbles and falling mushroom-shaped spikes.
- [Simplified Real-Time Fluid Dynamics Simulator](../../../scripts/simulations/simplified_real_time_fluid_dynamics_simulator/): is an interactive 2D smoke simulation that uses Jos Stam's Stable Fluids algorithm (1999) to approximate the incompressible Navier-Stokes equations fast enough to run in real time in a Matplotlib window.
- [TVD Limiters for Linear Advection](../../../scripts/algorithms/tvd_limiters_advection/): advects a Gaussian, a square wave and a triangle once around a periodic domain with first-order upwind, Lax–Wendroff and flux-limited TVD schemes, and shows the trade-off that Godunov's theorem forces on linear schemes.

## Exercises

**Exercise 1.** An acoustic pulse travels at $c = 340$ m/s through still air on a grid with $\Delta x = 1$ mm. What is $\Delta t_{\max}$ for the explicit upwind scheme, and how many time steps does it take to simulate 0.01 s? If the viscous terms ($\nu = 1.5 \times 10^{-5}$ m²/s) are also treated explicitly with forward Euler in 1D, which limit is binding?

<details>
<summary>Answer</summary>

$\Delta t_{\max} = \Delta x/c = 10^{-3}/340 \approx 2.94 \times 10^{-6}$ s, so $0.01/2.94 \times 10^{-6} = 3400$ steps.

The viscous limit is $\Delta t \le \Delta x^2/(2\nu) = 10^{-6}/(3 \times 10^{-5}) \approx 0.033$ s, more than $10^4$ times larger. The acoustic limit is binding. On a wall-normal spacing of 1 µm the viscous limit would drop to $3.3 \times 10^{-8}$ s and dominate.

</details>

**Exercise 2.** Show that FTCS for diffusion is stable if and only if $r \le 1/2$, then evaluate $G(\pi)$ for $r = 0.25$, $0.5$ and $0.6$. How many steps does it take for an error of $10^{-12}$ in the $\theta = \pi$ mode to reach order one at $r = 0.6$?

<details>
<summary>Answer</summary>

From the derivation in the note, $G = 1 - 4r\sin^2(\theta/2) \in [1 - 4r, 1]$, and $G \ge -1$ for all $\theta$ requires $1 - 4r \ge -1$, that is $r \le 1/2$.

$G(\pi) = 1 - 4r$: $0$ for $r = 0.25$ (the shortest wave is removed in one step), $-1$ for $r = 0.5$ (it flips sign without decaying), $-1.4$ for $r = 0.6$.

At $r = 0.6$ the mode grows by 1.4 per step, so $n = \ln(10^{12})/\ln 1.4 \approx 82$ steps. Round-off error is enough to trigger the instability.

</details>

**Exercise 3.** Use von Neumann analysis on the explicit upwind scheme $\phi_i^{n+1} = (1 - C)\phi_i^n + C\phi_{i-1}^n$ to find $|G|^2$. Evaluate $|G|$ at $\theta = \pi$ for $C = 0.5$ and $C = 1.2$. Then do the same for the implicit upwind scheme at $C = 5$, for $\theta = \pi$ and $\theta = \pi/2$. What do the implicit numbers mean for accuracy?

<details>
<summary>Answer</summary>

Explicit: $G = 1 - C + Ce^{-\mathrm{i}\theta}$ and

```math
|G|^2 = 1 - 2C(1 - C)(1 - \cos\theta)
```

At $\theta = \pi$, $G = 1 - 2C$: $|G| = 0$ for $C = 0.5$ and $|G| = 1.4$ for $C = 1.2$, where errors grow by 40% per step. Stability for all $\theta$ requires $0 \le C \le 1$.

Implicit: $|G|^2 = 1/\left(1 + 2C(1 + C)(1 - \cos\theta)\right)$. At $C = 5$: $|G| = 1/\sqrt{121} = 1/11 \approx 0.091$ for $\theta = \pi$, and $|G| = 1/\sqrt{61} \approx 0.128$ for $\theta = \pi/2$.

Large time steps are stable but damp everything except long waves within a few steps. That is fine for marching to a steady state but destroys time accuracy in unsteady problems.

</details>

**Exercise 4.** On a periodic grid, apply two steps of the explicit upwind scheme with $C = 0.5$ to $\boldsymbol{\phi}^0 = (0, 0, 1, 0, 0)$, with the flow moving towards larger $i$. Relate the spreading to the modified equation, and describe what happens with $C = 1$.

<details>
<summary>Answer</summary>

$\phi_i^{n+1} = 0.5\phi_i^n + 0.5\phi_{i-1}^n$:

- Step 1: $(0, 0, 0.5, 0.5, 0)$
- Step 2: $(0, 0, 0.25, 0.5, 0.25)$

The pulse moves right while spreading, and the sum stays 1. The modified equation predicts diffusion with $\nu_{\mathrm{num}} = u\Delta x(1 - C)/2$, which in grid units is $\nu_{\mathrm{num}}\Delta t/\Delta x^2 = C(1 - C)/2 = 0.125$ per step. The variance of the pulse after two steps is $0.5$ cells², and $2\nu_{\mathrm{num}}t$ gives $2 \times 0.125 \times 2 = 0.5$ cells², as predicted.

With $C = 1$ the update is $\phi_i^{n+1} = \phi_{i-1}^n$, an exact shift with $\nu_{\mathrm{num}} = 0$.

</details>

**Exercise 5.** A steady solution is reached by marching the model advection equation until $t = 5L/u$, with $L = 1$ m, $u = 1$ m/s and $\Delta x = 0.01$ m. Compare the number of steps for the explicit scheme at $C = 0.9$ and the implicit scheme at $C = 20$. What is the trade-off, and how does local time stepping change the picture on a stretched grid?

<details>
<summary>Answer</summary>

Explicit: $\Delta t = 0.009$ s, so $5/0.009 \approx 556$ steps. Implicit: $\Delta t = 0.2$ s, so 25 steps.

Each implicit step needs a linear system to be solved, so it costs more than an explicit update, but for steady problems, and especially for the nonlinear Euler and Navier–Stokes equations, the implicit approach usually wins. On a stretched grid a global time step is set by the smallest cell; local time stepping lets each cell use its own $\Delta t_i = C\Delta x_i/|u|$, so the number of steps is governed by the typical cell size rather than the smallest one.

</details>

## References

- Courant, R., Friedrichs, K., and Lewy, H., "Über die partiellen Differenzengleichungen der mathematischen Physik", *Mathematische Annalen* 100, 32–74, 1928.
- Lax, P. D., and Richtmyer, R. D., "Survey of the stability of linear finite difference equations", *Communications on Pure and Applied Mathematics* 9(2), 267–293, 1956.
- Charney, J. G., Fjørtoft, R., and von Neumann, J., "Numerical integration of the barotropic vorticity equation", *Tellus* 2(4), 237–254, 1950.
- Warming, R. F., and Hyett, B. J., "The modified equation approach to the stability and accuracy analysis of finite-difference methods", *Journal of Computational Physics* 14(2), 159–179, 1974.
- Strikwerda, J. C., *Finite Difference Schemes and Partial Differential Equations*, 2nd ed., SIAM, 2004.
- LeVeque, R. J., *Finite Difference Methods for Ordinary and Partial Differential Equations*, SIAM, 2007.
- LeVeque, R. J., *Finite Volume Methods for Hyperbolic Problems*, Cambridge University Press, 2002.
- Hirsch, C., *Numerical Computation of Internal and External Flows*, Vol. 1, 2nd ed., Butterworth-Heinemann, 2007.
- Ferziger, J. H., Perić, M., and Street, R. L., *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
