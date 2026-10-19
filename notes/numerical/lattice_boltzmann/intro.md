# Introduction to Lattice Boltzmann Analysis

Modeling fluid flows directly from the **Navier–Stokes Equations (NSE)** can be challenging due to their inherent complexity. This difficulty has led to the exploration of alternative numerical strategies, including the **lattice Boltzmann method (LBM)**. Before diving into LBM, it is helpful to understand the traditional obstacles faced by analysts and engineers when solving fluid dynamics problems.

## Challenges of Solving NSE Analytically

The **Navier–Stokes equations** are the cornerstone of fluid mechanics at the continuum scale. They describe how velocity, pressure, and other fluid properties evolve over space and time. However, they pose several analytical challenges:

I. **Non-Linearity:**

- The NSE are **non-linear** due to the convective term $(u \cdot \nabla)u$.
- Non-linearity complicates finding closed-form solutions.

$$
\rho \left(\frac{\partial u}{\partial t} + (u \cdot \nabla)u \right) = -\nabla p + \eta
\nabla^2 u + f
$$

II. **Partial Differential Equations (PDEs):**

- NSE are **partial differential equations**, more complicated than ordinary differential equations due to multi-dimensional spatial and temporal dependencies.
- Solutions require simultaneous consideration of variations in multiple directions and over time.

III. **Boundary Conditions:**

- Correctly specifying and carrying out **boundary conditions** is vital.
- Complicated geometries, moving boundaries, and multi-phase interfaces increase difficulty.

```
ASCII Diagram: Complexity of NSE

Non-linearity + PDE nature + Complicated Boundaries
            |
            v
   Analytical Solutions Rare, Require Numerical Methods
```

# Computational Fluid Dynamics (CFD)

To tackle the complexity of NSE, researchers rely on **computational fluid dynamics (CFD)** methods. CFD converts the continuous equations into a discrete form suitable for numerical computation, enabling approximate solutions where analytical ones are difficult or impossible.

## Numerical Methods in CFD

I. **Finite Difference Method (FDM):**

- Approximates derivatives using **differences** between neighboring points.
- Conceptually simple but may require very fine meshes to achieve desired accuracy.

II. **Finite Volume Method (FVM):**

- Integrates equations over **control volumes**, making sure local conservation of mass, momentum, and energy.
- Widely used in industry for its balance between accuracy and computational cost.

III. **Spectral Methods:**

- Represent solutions using global basis functions (e.g., **Fourier series**, polynomials).
- Highly accurate for smooth problems but can be expensive and complicated for complicated geometries.

IV. **Finite Element Method (FEM):**

- Subdivides the domain into **elements**.
- Excellent for complicated geometries and boundary conditions, using variational formulations.

```
ASCII Diagram: Common CFD Methods

PDE -> Discretization:

FDM: Grid-based differences
FVM: Integrates over volumes
FEM: Subdivides domain into elements
Spectral: Expands solution in global functions
```

# Common Issues with CFD

Despite their strengths, traditional CFD methods face certain issues:

I. **Mesh Generation:**

- Creating a suitable **mesh** that represents complicated geometries faithfully is non-trivial.
- Mesh quality influences solution accuracy and stability.

II. **Boundary Conditions:**

- Correct application of **boundary conditions** is important. Errors lead to non-physical results.
- Common types: Dirichlet (specifying values), Neumann (specifying fluxes), and mixed conditions.

III. **Poisson Pressure Equation:**

- The pressure field often emerges from a **Poisson equation**:

$$
\nabla^2 p = f(u)
$$

- Making sure stable, accurate pressure solutions can be challenging, especially in complicated flows.

```
ASCII Diagram: CFD Workflow Challenges

Geometry -> Meshing -> Solve PDEs (NSE) -> Extract Pressure, Velocity
     ^                                      |
     |                                      |
  Iterations to get stable, accurate solutions
```

## Alternative Perspectives in Fluid Mechanics

### Representative Elementary Volume (REV) vs. Fluid Particle

- **REV:**
- Conceptual averaging volume, bridging microscopic details and macroscopic quantities.
- Enables a continuum description.
- **Fluid Particle:**
- Focuses on an infinitesimal element of fluid, capturing local variations.
  From microscopic scales (where molecular dynamics might apply) to macroscopic scales (NSE-based modeling), different viewpoints and averaging processes help effective modeling strategies.

```
ASCII Diagram: Scales of Analysis

Molecular Scale (nm) -> Mesoscopic (µm) -> Macroscopic (mm+)
MD/DSMC               LBM               NSE/CFD
```

## Collisions, Mean Free Path, and Time Scales

On a molecular level:

- **Thermal Motion:**\
  Molecules like argon at room temperature move at ~400 m/s.

- **Mean Free Path (MFP):**\
  The average distance a molecule travels between collisions (~70 nm for a gas at atmospheric pressure; the mean spacing between molecules is only ~3 nm).

- **Collision Times:**\
  Times between collisions (~$`10^{-10}`$ s at atmospheric pressure) far smaller than macroscopic flow timescales.

These microscopic properties underlie the **continuum assumption**, where macroscopic fields (velocity, pressure) represent averaged effects of countless molecular interactions.

## Macroscopic Fluids: Continuum Assumption

**Continuum Hypothesis:**

- Macroscopic properties vary smoothly and are well-defined at every point in the fluid domain.

- Large separation of scales between molecular mean free path and engineering scales justifies treating fluids as continuous.
  **Conservation Equations:**

- Continuity and NSE form the backbone of continuum fluid mechanics.

## Scale Comparison: Micro, Meso, Macro

|  | **Micro** (Molecular) | **Meso** (Relating to motion) | **Macro** (Continuum) |
| --- | --- | --- | --- |
| **Scale** | ~10^-9 m | 10^-9 to 10^-6 m | >10^-6 m |
| **Physics** | Molecular Interactions | Probabilistic (Boltzmann) | Continuous Fields (NSE) |
| **Equations** | Newton's Laws (MD) | Boltzmann Equation | Navier–Stokes Equations |
| **Methods** | Molecular Dynamics | Direct Simulation Monte Carlo | CFD (FDM, FVM, FEM, etc.) |

This table highlights the hierarchy of modeling approaches. The **lattice Boltzmann method (LBM)** occupies a mesoscopic niche. It models fluid at a kinetic level using distribution functions, bridging microscopic molecular interactions and macroscopic flow fields.

# Numerical Modelling Process

From reality to simulation:

```
                 +-----------+ 
   ------------> | "Reality" |  
   |             +-----------+  
   |                   |      
   |                   v 
   |             +----------------+                       
   |             | Physical model |                       
   |             +----------------+                       
   |                   |                                 
   |                   v                                  
+------------+       +--------------------+    
| validation |       | Mathematical model | <----------------
+------------+       +--------------------+                 |
   ^                   |                                |
   |                   v                                |
   |             +------------------+           +--------------+
   |             | Numerical model  |           | verification |
   |             +------------------+           +--------------+
   |                   |                                ^
   |                   v                                |
   |             +-------------+                        |
   --------------| Simulation  | ------------------------
                 +-------------+ 
```

**Explanation:**

- Move from **physical models** (conceptual) to **mathematical models** (equations).
- Convert equations into **numerical models** suitable for computation.
- **Simulation** solves these models, while **verification** makes sure numerical correctness and **validation** checks physical realism.

## Purpose in CFD

This note motivates the Lattice Boltzmann Method (LBM) by reviewing the challenges of solving the Navier–Stokes equations directly: nonlinearity, complex meshes, and the pressure Poisson equation. It introduces the hierarchy of modeling scales (microscopic → mesoscopic → macroscopic) and positions LBM as a mesoscopic alternative that bridges molecular dynamics and continuum CFD.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Physical domain, flow regime (Reynolds number), choice of modeling scale, boundary complexity assessment |
| **Outputs** | Justification for choosing LBM vs. traditional CFD, understanding of scale hierarchy (molecular → Boltzmann → Navier–Stokes) |

## Related Scripts

- [Lattice Boltzmann Cylinder Flow Simulation](../../../scripts/simulations/lattice_boltzmann_cylinder_flow/): simulates 2D flow past a circular cylinder with the lattice Boltzmann method (D2Q9 lattice, BGK collision operator) and animates the velocity magnitude and the vorticity with Matplotlib.

## Exercises

**Exercise 1.** The companion script simulates flow past a cylinder at $\mathrm{Re} = UD/\nu = 350$. For water ($\nu = 1.0 \times 10^{-6}$ m²/s) flowing at $U = 0.1$ m/s, what cylinder diameter gives this Reynolds number?

<details>
<summary>Answer</summary>

$`D = \mathrm{Re}\,\nu / U = 350 \times 10^{-6} / 0.1 = 3.5 \times 10^{-3}`$ m, i.e. 3.5 mm.

</details>

**Exercise 2.** For argon (molar mass 39.948 g/mol) at $T = 293.15$ K, compute the mean thermal speed $\bar{v} = \sqrt{8 k_B T/(\pi m)}$. Taking a hard-sphere diameter $d = 0.36$ nm and $p = 101325$ Pa, compute the mean free path $`\ell_{\text{mfp}} = k_B T/(\sqrt{2}\,\pi d^2 p)`$ and the mean collision time $\ell_{\text{mfp}}/\bar{v}$. Compare with the values quoted in the note.

<details>
<summary>Answer</summary>

The molecular mass is $m = 39.948 \times 1.6605 \times 10^{-27} \approx 6.63 \times 10^{-26}$ kg.

- $\bar{v} = \sqrt{8 \times 1.380649 \times 10^{-23} \times 293.15 / (\pi \times 6.63 \times 10^{-26})} \approx 394$ m/s, consistent with "~400 m/s".
- $\ell_{\text{mfp}} \approx 6.9 \times 10^{-8}$ m, about 69 nm.
- Collision time $\approx 6.9 \times 10^{-8} / 394 \approx 1.8 \times 10^{-10}$ s, of order $10^{-10}$ s.

Both are many orders of magnitude below engineering length and time scales, which justifies the continuum hypothesis.

</details>

**Exercise 3.** Argon at atmospheric pressure flows through a microchannel of height 50 µm. Using $\ell_{\text{mfp}}$ from Exercise 2, compute the Knudsen number $\mathrm{Kn} = \ell_{\text{mfp}}/\ell$. Which column of the scale-comparison table applies, and is the continuum hypothesis valid (a common criterion is $\mathrm{Kn} < 0.01$)?

<details>
<summary>Answer</summary>

$\mathrm{Kn} = 6.9 \times 10^{-8} / 5 \times 10^{-5} \approx 1.4 \times 10^{-3}$. This is below 0.01, so the continuum hypothesis holds and the macroscopic (NSE) description applies. A mesoscopic method such as LBM remains usable because it is built to recover the NSE in this small-Kn limit.

</details>

**Exercise 4.** Take the divergence of the incompressible NSE of Section 1 (constant $\rho$, body force $f = 0$) to derive the pressure Poisson equation $`\nabla^2 p = -\rho \, \partial_i u_j \, \partial_j u_i`$ (summation over repeated indices). Verify it for solid-body rotation $u = (-\Omega y, \Omega x)$, whose pressure field is $p = p_0 + \rho \Omega^2 (x^2 + y^2)/2$.

<details>
<summary>Answer</summary>

Because $\nabla \cdot u = 0$, the divergence of $\partial u/\partial t$ and of $\eta \nabla^2 u$ both vanish. For the convective term,

```math
\partial_i \left(u_j \partial_j u_i \right) = \partial_i u_j \, \partial_j u_i + u_j
\partial_j \left(\partial_i u_i \right) = \partial_i u_j \, \partial_j u_i
```

so $`\rho \, \partial_i u_j \, \partial_j u_i = -\nabla^2 p`$.

For solid-body rotation, $\partial_x u_x = 0$, $\partial_y u_x = -\Omega$, $\partial_x u_y = \Omega$ and $\partial_y u_y = 0$. Then $`\partial_i u_j \, \partial_j u_i = (\partial_x u_x)^2 + 2\,\partial_y u_x \, \partial_x u_y + (\partial_y u_y)^2 = -2\Omega^2`$, which gives $\nabla^2 p = 2\rho\Omega^2$. Directly, $\nabla^2 \left[\rho\Omega^2(x^2 + y^2)/2\right] = \rho\Omega^2(1 + 1) = 2\rho\Omega^2$, so the two agree. In a CFD solver this equation must be solved at every time step, which LBM avoids.

</details>

## References

- J. H. Ferziger and M. Perić, *Computational Methods for Fluid Dynamics*, 3rd ed., Springer, 2002.
- G. A. Bird, *Molecular Gas Dynamics and the Direct Simulation of Gas Flows*, Oxford University Press, 1994.
- T. Krüger, H. Kusumaatmaja, A. Kuzmin, O. Shardt, G. Silva and E. M. Viggen, *The Lattice Boltzmann Method: Principles and Practice*, Springer, 2017.
- S. Succi, *The Lattice Boltzmann Equation for Fluid Dynamics and Beyond*, Oxford University Press, 2001.
