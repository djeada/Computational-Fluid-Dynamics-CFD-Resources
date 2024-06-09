# Weak Formulation of PDEs

The finite element method (FEM) is a powerful tool for numerically solving partial differential equations (PDEs). A crucial step in employing FEM is deriving the weak formulation of the PDE. Here we will explain the process using a reaction-diffusion PDE as an example.

## The Strong Form of the PDE

Consider the reaction-diffusion equation:

$$
\frac{\partial u}{\partial t} = 
abla \cdot (D 
abla u) - s u
$$

where:
- $u = u(\mathbf{x}, t)$ is the state variable
- $D$ is the diffusion coefficient
- $s$ is the reaction term

## Test and Trial Function Spaces

### Test Function Space

Define a space of test functions:

$$
\mathcal{V} = \{ v(\mathbf{x}) \mid \mathbf{x} \in \Omega, v(\mathbf{x}) \in \mathcal{H}^{1}(\Omega), v(\mathbf{x}) = 0 \text{ on } \Gamma \}
$$

where:
- $\Omega$ is the domain of interest
- $\Gamma$ is the boundary of $\Omega$
- $\mathcal{H}^{1}(\Omega)$ is the Sobolev space of functions with square-integrable derivatives in $\Omega$

### Trial Function Space

The solution $u$ belongs to a trial function space:

$$
\mathcal{S}_{t} = \{ u(\mathbf{x}, t) \mid \mathbf{x} \in \Omega, t > 0, u(\mathbf{x}, t) \in \mathcal{H}^{1}(\Omega), \frac{\partial u}{\partial n} = 0 \text{ on } \Gamma \}
$$

## Deriving the Weak Form

1. **Multiply the PDE by an arbitrary test function $v \in \mathcal{V}$:**

$$
\frac{\partial u}{\partial t} v = 
abla \cdot (D 
abla u) v - s u v
$$

2. **Integrate over the domain $\Omega$:**

$$
\int_{\Omega} \frac{\partial u}{\partial t} v \, d\omega = \int_{\Omega} 
abla \cdot (D 
abla u) v \, d\omega - \int_{\Omega} s u v \, d\omega
$$

3. **Apply integration by parts to the diffusion term:**

$$
\int_{\Omega} 
abla \cdot (D 
abla u) v \, d\omega = \int_{\Omega} 
abla \cdot [v (D 
abla u)] \, d\omega - \int_{\Omega} (
abla v) \cdot (D 
abla u) \, d\omega
$$

4. **Convert the surface integral using Green’s theorem:**

$$
\int_{\Omega} 
abla \cdot [v (D 
abla u)] \, d\omega = \int_{\Gamma} D v \frac{\partial u}{\partial n} \, d\gamma
$$

Since there is a no-flux boundary condition ($\frac{\partial u}{\partial n} = 0$ on $\Gamma$), this term is zero.

5. **Discretize the temporal term using the backward Euler scheme:**

$$
\frac{\partial u}{\partial t} \approx \frac{u - u^{n}}{\Delta t}
$$

6. **Combine all terms into the integral form:**

$$
\int_{\Omega} \frac{u - u^{n}}{\Delta t} v \, d\omega = - \int_{\Omega} D 
abla u \cdot 
abla v \, d\omega - \int_{\Omega} s u v \, d\omega
$$

7. **Rearrange to obtain the weak form:**

$$
\int_{\Omega} \frac{u}{\Delta t} v \, d\omega + \int_{\Omega} D 
abla u \cdot 
abla v \, d\omega + \int_{\Omega} s u v \, d\omega = \int_{\Omega} \frac{u^{n}}{\Delta t} v \, d\omega
$$

8. **Multiply by $\Delta t$ for the final weak form:**

$$
\int_{\Omega} u v \, d\omega + \int_{\Omega} \Delta t D 
abla u \cdot 
abla v \, d\omega + \int_{\Omega} \Delta t s u v \, d\omega = \int_{\Omega} u^{n} v \, d\omega
$$

This final equation is the weak formulation of the reaction-diffusion PDE, ready for numerical methods such as FEM.
