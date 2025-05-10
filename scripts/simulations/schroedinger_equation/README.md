## Schrödinger Equation Simulation

[![Watch the Demo on YouTube](https://img.youtube.com/vi/Za9TGx75ElI/maxresdefault.jpg)](https://youtu.be/Za9TGx75ElI?si=ikGQMCyG8am8Qyz-)

### Schrödinger Equation

The Schrödinger equation is a fundamental equation in quantum mechanics that describes how the quantum state of a physical system changes over time. In this example, we're dealing with the time-dependent Schrödinger equation in two dimensions for a free particle (i.e., no potential).

The time-dependent Schrödinger equation in two dimensions is given by:

$$i\hbar \frac{\partial \psi(x, y, t)}{\partial t} = \left( -\frac{\hbar^2}{2m} \nabla^2 + V(x, y) \right) \psi(x, y, t)$$

where:

- $\psi(x, y, t)$ is the wave function.
- $\hbar$ is the reduced Planck's constant.
- $m$ is the mass of the particle.
- $\nabla^2$ is the Laplacian operator.
- $V(x, y)$ is the potential energy, which is zero in the free particle case.

For simplicity, we set $\hbar = 1$ and $m = 1$, reducing the equation to:

$$
i \frac{\partial \psi(x, y, t)}{\partial t} = -\frac{1}{2} \nabla^2 \psi(x, y, t)
$$

### Initial Wavefunction

The initial wavefunction is a 2D Gaussian function:

$$
\psi_0(x, y) = e^{-\frac{x^2 + y^2}{2}}
$$

This represents a localized particle in space at $t = 0$.

### Numerical Method: Split-Step Fourier Method

The split-step Fourier method is used to numerically solve the time-dependent Schrödinger equation. This method is particularly effective for problems involving linear and nonlinear dispersive waves. It splits the evolution into two parts:
1. **Linear part**: Handles the kinetic energy term in Fourier space.
2. **Nonlinear part**: Handles the potential energy term in real space.

##### Step-by-Step Process

1. **Fourier Transform**: The wavefunction $\psi$ is transformed into Fourier space using the Fast Fourier Transform (FFT). In Fourier space, spatial derivatives become multiplications, which simplifies the kinetic term.

2. **Evolution in Fourier Space**: Apply the kinetic energy operator in Fourier space. For the kinetic part, the evolution is given by:

$$
\tilde{\psi}(k_x, k_y, t + \Delta t/2) = \tilde{\psi}(k_x, k_y, t) \cdot e^{-i \frac{k^2}{2} \Delta t/2}
$$

where $k_x$ and $k_y$ are the wave numbers, and $k^2 = k_x^2 + k_y^2$.

3. **Inverse Fourier Transform**: Transform back to real space using the Inverse FFT (IFFT).

4. **Evolution in Real Space**: Apply the potential energy operator in real space. For the potential part, the evolution is given by:

$$
\psi(x, y, t + \Delta t) = \psi(x, y, t + \Delta t/2) \cdot e^{-i V(x, y) \Delta t}
$$

5. **Repeat**: These steps are repeated for each time step to evolve the wavefunction over time.

### Implementation Details

- **Grid and Time Steps**: The spatial domain is discretized into a grid, and time is discretized into small steps.
- **Initial Condition**: The initial wavefunction is set as a 2D Gaussian.
- **Potential**: For a free particle, the potential $V$ is zero everywhere.
- **FFT and IFFT**: The numpy library functions `np.fft.fft2` and `np.fft.ifft2` are used for transforming to and from Fourier space.

### Visualization

The wavefunction's magnitude squared $|\psi|^2$, which represents the probability density, is plotted over time to show the dynamic evolution of the quantum system. 
