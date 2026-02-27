# Lattice Boltzmann Cylinder Flow Simulation

This script simulates 2D incompressible flow around a cylinder using the Lattice Boltzmann Method (LBM) with the D2Q9 velocity set and BGK collision operator. LBM operates at the mesoscopic level, evolving probability distribution functions rather than macroscopic variables directly, and recovers the Navier-Stokes equations in the low-Mach-number limit. A short demonstration is available on YouTube: [![Watch on YouTube](https://i9.ytimg.com/vi/Jzsxy2BsQRM/mqdefault.jpg?sqp=CMSXlrQG-oaymwEoCMACELQB8quKqQMcGADwAQH4AbYIgAL6DYoCDAgAEAEYYCATKH8wDw==&rs=AOn4CLDbqZndaVyMLoKIe0VMTCGB6TlvrQ)](https://youtube.com/shorts/mOMWcGnXtFQ)

## Overview

- D2Q9 lattice with 9 discrete velocity directions per grid node
- BGK (single-relaxation-time) collision operator for computational simplicity
- Bounce-back boundary condition on cylinder surface to enforce no-slip
- Macroscopic density and velocity recovered from distribution function moments
- Colour-mapped visualisation of velocity magnitude or vorticity

## Mathematical Background

### Boltzmann Equation

LBM is a discretisation of the Boltzmann equation describing the evolution of the particle distribution function $f(\mathbf{x}, \mathbf{v}, t)$:

$$\frac{\partial f}{\partial t} + \mathbf{v} \cdot \nabla f = \Omega(f)$$

### BGK Collision and Streaming

With the BGK approximation, the combined collision-and-streaming step becomes:

$$f_i(\mathbf{x} + \mathbf{c}_i \Delta t,\; t + \Delta t) = f_i(\mathbf{x}, t) - \frac{1}{\tau}\!\left(f_i(\mathbf{x}, t) - f_i^{eq}(\mathbf{x}, t)\right)$$

where $\tau$ is the relaxation time (related to kinematic viscosity by $\nu = c_s^2(\tau - \tfrac{1}{2})\Delta t$).

### D2Q9 Equilibrium Distribution

$$f_i^{eq} = w_i \rho \left(1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2c_s^4} - \frac{u^2}{2c_s^2}\right)$$

where $w_i$ are the D2Q9 lattice weights and $c_s = 1/\sqrt{3}$ is the lattice speed of sound.

### Macroscopic Quantities

Density and velocity are recovered as zeroth and first moments of $f_i$:

$$\rho = \sum_i f_i, \qquad \mathbf{u} = \frac{1}{\rho}\sum_i f_i \mathbf{c}_i$$

## Implementation

1. Initialise D2Q9 lattice weights $w_i$, velocity vectors $\mathbf{c}_i$, and domain arrays
2. Set inflow conditions and mark cylinder nodes for bounce-back
3. Compute equilibrium distributions $f_i^{eq}$ from $\rho$ and $\mathbf{u}$
4. Apply BGK collision: $f_i \leftarrow f_i - (f_i - f_i^{eq})/\tau$
5. Stream: shift each $f_i$ along its lattice direction $\mathbf{c}_i$
6. Apply bounce-back on cylinder surface; compute macroscopic fields and render

## Output

- **Real-time visualisation**: colour-mapped velocity magnitude or vorticity field showing vortex shedding behind the cylinder as the simulation evolves
