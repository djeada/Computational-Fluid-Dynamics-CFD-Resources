# 2D Schrödinger Equation Simulation

This script numerically solves the time-dependent Schrödinger equation in two spatial dimensions using the split-step Fourier method and animates the probability density of the evolving wavefunction. Watch the demo: [![YouTube](https://img.youtube.com/vi/Za9TGx75ElI/maxresdefault.jpg)](https://youtu.be/Za9TGx75ElI?si=ikGQMCyG8am8Qyz-)

## Overview

- **2D time-dependent Schrödinger equation** solved on a uniform spatial grid with $\hbar = m = 1$.
- **Split-step Fourier method**: alternates kinetic evolution in Fourier space with potential evolution in real space.
- **Gaussian initial wavefunction** representing a localized free particle at $t=0$.
- **Probability density** $|\psi|^2$ animated over time to demonstrate quantum dispersion and norm conservation.

## Mathematical Background

### Schrödinger Equation

The time-dependent Schrödinger equation in two dimensions (with $\hbar = m = 1$):

$$i\hbar\frac{\partial\psi(x,y,t)}{\partial t} = \left(-\frac{\hbar^2}{2m}\nabla^2 + V(x,y)\right)\psi(x,y,t)$$

For a free particle ($V=0$) this reduces to $i\,\partial_t\psi = -\tfrac{1}{2}\nabla^2\psi$.

### Initial Wavefunction

The simulation starts with a 2D Gaussian wavepacket localized at the origin:

$$\psi_0(x,y) = e^{-(x^2+y^2)/2}$$

### Numerical Method: Split-Step Fourier Method

The evolution operator is split into kinetic (Fourier-space) and potential (real-space) half-steps.

**Kinetic half-step** in Fourier space, where $k^2 = k_x^2 + k_y^2$:

$$\tilde{\psi}(k_x,k_y,\,t+\Delta t/2) = \tilde{\psi}(k_x,k_y,t)\cdot e^{-ik^2\Delta t/4}$$

**Potential full-step** in real space:

$$\psi(x,y,\,t+\Delta t/2) = \psi(x,y,t)\cdot e^{-iV(x,y)\Delta t}$$

A second kinetic half-step completes the symmetric (Strang) splitting, giving second-order accuracy in time.

## Implementation

1. Discretize the 2D domain into a uniform grid; define wave-number arrays $k_x$, $k_y$ via `np.fft.fftfreq`.
2. Set the initial wavefunction $\psi_0$ as a 2D Gaussian; normalize so $\int|\psi_0|^2\,dA = 1$.
3. Define the potential array $V$ (zero everywhere for a free particle, or any user-specified barrier).
4. Each time step: FFT $\psi$ → apply kinetic phase factor → IFFT → apply potential phase factor → FFT → apply kinetic phase factor → IFFT.
5. Compute probability density $|\psi|^2$ and update the animated color-map plot.
6. Repeat for the desired number of time steps.

## Output

The animation displays $|\psi(x,y,t)|^2$ as a `viridis` color map evolving over time:

- The initially localized Gaussian wavepacket spreads outward, demonstrating quantum dispersion.
- Total probability $\int|\psi|^2\,dA$ is conserved to machine precision, confirming unitarity of the split-step scheme.
- The grid and time discretization can be adjusted at the top of the script to explore different dispersion rates.
