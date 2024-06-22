# Navier-Stokes Equations (NSE)

## Challenges of Solving NSE Analytically

1. **Non-Linearity:**
   - The Navier-Stokes equations are non-linear in the velocity field $u$.
   - Mathematical representation:
     
$$
     \rho \left( \frac{\partial u}{\partial t} + (u \cdot 
abla)u \right) = -
abla p + \eta 
abla^2 u + f
     $$

   - Non-linearity arises from the convective term $(u \cdot 
abla)u$.

2. **Partial Differential Equations (PDEs):**
   - NSE are PDEs, which are inherently more complex to solve than ordinary differential equations (ODEs).
   - Solutions require consideration of spatial and temporal variations.

3. **Boundary Conditions:**
   - Accurate solutions necessitate proper application of boundary conditions, which can be complex and varied depending on the problem domain.

# Computational Fluid Dynamics (CFD)

## Numerical Methods in CFD

1. **Finite Difference Method:**
   - Approximates derivatives using difference equations.
   - Simple implementation but may require fine meshing for accuracy.

2. **Finite Volume Method:**
   - Conserves quantities like mass, momentum, and energy by integrating over control volumes.
   - Widely used in industry due to its balance of accuracy and computational efficiency.

3. **Spectral Methods:**
   - Use global functions (e.g., Fourier series) to approximate solutions.
   - Highly accurate for problems with smooth solutions but can be computationally intensive.

4. **Finite Element Method (FEM):**
   - Divides the domain into smaller sub-domains (elements) and uses variational methods to solve.
   - Particularly useful for complex geometries and boundary conditions.

# Common Issues with CFD

1. **Mesh Generation:**
   - Creating a computational grid (mesh) that accurately represents the geometry of the problem domain.
   - Quality of mesh significantly affects solution accuracy and convergence.

2. **Boundary Conditions:**
   - Properly defining and implementing boundary conditions is critical for accurate simulations.
   - Common types include Dirichlet, Neumann, and mixed boundary conditions.

3. **Poisson Pressure Equation:**
   - The pressure field is obtained by solving the Poisson equation:
     
$$
     
abla^2 p = f(u)
     $$

   - Ensuring numerical stability and accuracy in solving this equation is a common challenge.


## Alternative Perspectives in Fluid Mechanics

### Representative Elementary Volume (REV) vs. Fluid Particle
- **REV:**
  - Conceptual volume over which fluid properties are averaged.
  - Facilitates macroscopic analysis of fluid behavior.
- **Fluid Particle:**
  - Infinitesimal volume element used to study flow properties at specific points.
  - Represents microscopic analysis in fluid mechanics.

### Transition from Microscopic to Macroscopic Analysis
- REV helps in transitioning from detailed molecular-level analysis to a broader, averaged-out perspective suitable for practical engineering problems.

## Collisions and Mean Free Path

### Thermal Motion of Molecules
- **Example: Argon at Room Temperature**
  - Thermal velocity ($v_{\text{th}}$): Approximately 400 m/s.
  - Thermal velocity squared ($\left\langle v_{\text{th}}^2 \right\rangle$): Given by $\frac{3kT}{m}$.

### Number Density
- Number of molecules per unit volume:
  - $n/V = \frac{p}{RT} \approx 40 \, \text{mol/m}^3$.
- **Atomic Radius:** $\ell_a \approx 0.1 \, \text{nm}$.
- **Mean Free Path:** Average distance between molecular collisions, $\ell_{\text{mfp}} \approx 3 \, \text{nm}$.

### Time Scales
- **Collision Time ($t_c$)**: 
  - Time between molecular collisions.
  - $t_c = \ell_a / v_{\text{th}} \approx 0.3 \, \text{ps}$.
- **Mean Free Path Time ($t_{\text{mfp}}$)**:
  - Time to travel the mean free path distance.
  - $t_{\text{mfp}} = \ell_{\text{mfp}} / v_{\text{th}} \approx 10 \, \text{ps}$.

## Macroscopic Fluids: Continuum Assumption

### Key Points
- **Scale Separation**: 
  - Macroscopic scales ($\ell$) are much larger than mean free path ($\ell_{\text{mfp}}$).
- **Continuum Hypothesis**: 
  - Fluids are treated as continuous fields with properties such as velocity ($u$), pressure ($p$), and density ($\rho$).
- **Coarse-Graining**:
  - Averaging microscopic properties to obtain macroscopic fields.
- **Conservation Equations**:
  - Govern fluid behavior at macroscopic scale.
  - Include continuity equation and Navier-Stokes equations (NSE).

## Scale Comparison: Micro, Meso, Macro

|          | **Micro**                    | **Meso**                         | **Macro**         |
|----------|------------------------------|----------------------------------|-------------------|
| **Scale**| $10^{-9} \, \text{m}$      | $10^{-9} - 10^{-6} \, \text{m}$| $> 10^{-6} \, \text{m}$ |
| **Physics** | Molecular                 | Probabilistic                    | Continuous        |
| **Governing Equations** | Newton's Laws  | Boltzmann Equation               | Navier-Stokes Equations (NSE) |
| **Numerical Methods** | Molecular Dynamics (MD) | Direct Simulation Monte Carlo (DSMC) | Computational Fluid Dynamics (CFD) |


# Numerical Modelling

## Process Flow:

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

### Explanation:

1. **Reality**:
   - The starting point, representing the actual physical system or phenomenon being studied.

2. **Physical Model**:
   - Conceptualization of reality into a simplified version, capturing essential physical aspects.

3. **Mathematical Model**:
   - Formalization of the physical model into mathematical equations and expressions.

4. **Numerical Model**:
   - Discretization of the mathematical model to make it suitable for numerical computation.

5. **Simulation**:
   - Implementation and programming of the numerical model to perform simulations.

6. **Verification**:
   - Ensuring the numerical model accurately solves the mathematical model.

7. **Validation**:
   - Ensuring the mathematical model accurately represents reality.

