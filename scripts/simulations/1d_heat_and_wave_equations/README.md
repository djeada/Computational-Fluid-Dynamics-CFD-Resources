## The Heat Equation

The **heat equation** is a fundamental partial differential equation (PDE) that models the distribution of heat (or temperature variations) in a given region over time. It is widely used in physics, engineering, and other scientific disciplines to describe how heat diffuses through materials. Mathematically, in one spatial dimension, the heat equation is expressed as:

$$\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$$

Here, $u(x, t)$ represents the temperature at position $x$ and time $t$, while $\alpha$ is the thermal diffusivity constant, a material-specific parameter that quantifies the rate at which heat spreads. The equation signifies that the rate of change of temperature at any point is proportional to the curvature of the temperature profile at that point, encapsulating the essence of heat diffusion.

### Numerical Solutions for the Heat Equation

Solving the heat equation analytically is feasible for simple geometries and boundary conditions, but most practical problems require numerical approaches. **Finite difference methods** are commonly employed, where the continuous spatial and temporal domains are discretized into a grid. For instance, using an explicit finite difference scheme, the spatial second derivative is approximated by:

$$\frac{\partial^2 u}{\partial x^2} \approx \frac{u_{i+1}^n - 2u_i^n + u_{i-1}^n}{\Delta x^2}$$

and the time derivative by:

$$\frac{\partial u}{\partial t} \approx \frac{u_i^{n+1} - u_i^n}{\Delta t}$$

Substituting these into the heat equation yields an update rule for the temperature at each grid point. However, explicit schemes must adhere to stability conditions, such as the **Courant–Friedrichs–Lewy (CFL) condition**, which constrains the time step $\Delta t$ relative to the spatial step $\Delta x$ to ensure numerical stability:

$$\Delta t \leq \frac{\Delta x^2}{2\alpha}$$

Violating this condition can lead to numerical instabilities, causing the solution to diverge or exhibit non-physical oscillations.

## The Wave Equation

The **wave equation** is another pivotal PDE that describes the propagation of waves, such as sound waves, light waves, or water waves, through a medium. Unlike the heat equation, which models diffusive processes, the wave equation captures oscillatory and propagative phenomena. In one spatial dimension, the wave equation is formulated as:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}$$

In this equation, $u(x, t)$ denotes the wave displacement at position $x$ and time $t$, and $c$ represents the wave speed in the medium. The equation indicates that the acceleration of the wave displacement is proportional to the spatial curvature of the wave profile, facilitating the understanding of how waves maintain their shape while traveling through space.

### Numerical Approaches for the Wave Equation

Numerically solving the wave equation also typically involves finite difference methods, but the discretization differs due to the second-order time derivative. A common explicit scheme approximates the second time derivative as:

$$\frac{\partial^2 u}{\partial t^2} \approx \frac{u_i^{n+1} - 2u_i^n + u_i^{n-1}}{\Delta t^2}$$

and the spatial second derivative similarly to the heat equation. Substituting these into the wave equation provides an update rule that calculates the wave displacement at the next time step based on current and previous states. Stability for the wave equation is governed by the CFL condition tailored for hyperbolic equations:

$$\frac{c \Delta t}{\Delta x} \leq 1$$

Adhering to this condition is crucial to prevent numerical instabilities, such as artificial reflections or exponential growth of wave amplitudes, ensuring accurate and stable wave propagation in the simulation.
