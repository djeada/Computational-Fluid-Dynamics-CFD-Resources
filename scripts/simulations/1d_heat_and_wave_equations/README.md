## The Heat Equation

The heat equation describes how temperature changes over time in a material. In one dimension, it is:

$$\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$$

Here, $u(x, t)$ is the temperature at position $x$ and time $t$, and $\alpha$ is the thermal diffusivity, which controls how fast heat spreads. The equation shows that the temperature change rate depends on the curvature of the temperature profile.

### Numerical Solutions for the Heat Equation

Analytical solutions exist for simple cases, but most real problems use numerical methods. A common approach is the explicit finite difference method. The second spatial derivative is approximated by:

$$\frac{\partial^2 u}{\partial x^2} \approx \frac{u_{i+1}^n - 2u_i^n + u_{i-1}^n}{\Delta x^2}$$

and the time derivative by:

$$\frac{\partial u}{\partial t} \approx \frac{u_i^{n+1} - u_i^n}{\Delta t}$$

Putting these into the heat equation gives an update formula for each grid point. To keep the solution stable, the time step must satisfy:

$$\Delta t \leq \frac{\Delta x^2}{2\alpha}$$

If $\Delta t$ is too large, the solution can become unstable or oscillate.

## The Wave Equation

The wave equation models how waves move through a medium. In one dimension:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}$$

Here, $u(x, t)$ is the displacement at position $x$ and time $t$, and $c$ is the wave speed. The equation means the acceleration of the wave is linked to its spatial curvature.

### Numerical Approaches for the Wave Equation

Finite difference methods work here too, but account for the second-order time derivative. One explicit scheme uses:

$$\frac{\partial^2 u}{\partial t^2} \approx \frac{u_i^{n+1} - 2u_i^n + u_i^{n-1}}{\Delta t^2}$$

with the same spatial derivative as before. This yields an update rule using current and past values. Stability requires:

$$\frac{c \Delta t}{\Delta x} \leq 1$$

If this condition isn’t met, the simulation can show artificial reflections or growing amplitudes.
