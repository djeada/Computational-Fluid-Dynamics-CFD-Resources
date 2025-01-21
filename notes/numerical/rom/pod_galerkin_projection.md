## POD-Galerkin Projection with Finite Volume

Reduced-order modeling (ROM) has become a important tool in computational fluid dynamics (CFD) to accelerate simulations while retaining acceptable accuracy. Among ROM techniques, the **Proper Orthogonal Decomposition (POD)** combined with **Galerkin projection** is well-set up. In classical treatments, these methods often assume a finite element (FE) formulation because the weak variational form and associated inner products naturally emerge from FE theory.

However, many industrial and academic CFD solvers (e.g., OpenFOAM) use **finite volume discretizations (FVD)**. FVD enforces integral conservation laws on discrete control volumes, directly handling fluxes at cell interfaces. This integral viewpoint does not directly produce a “weak form” amenable to standard POD-Galerkin derivations. Consequently, extending the **POD-Galerkin** framework to a finite volume context requires additional care—particularly in how fluxes, pressure fields, boundary conditions, and nonlinear terms are projected onto the reduced basis. Below, we outline the necessary steps for constructing a POD-Galerkin ROM from a finite volume solver, focusing on both **laminar** and **turbulent (RANS)** Navier–Stokes equations.

## Equations and Problem Setting

### Governing Equations

We consider the **incompressible** Navier–Stokes equations, which, in their important form, read:

I. **Laminar (Viscous Incompressible)**

$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} 
= -\,\nabla p + \nu \,\Delta \mathbf{u}$$
$$\nabla \cdot \mathbf{u} = 0$$
where $\mathbf{u}(x,t)$ is the velocity field, $p(x,t)$ is the (kinematic) pressure (often normalized by density), and $\nu$ is the kinematic viscosity.

II. **RANS Equations (Turbulent Flow)**

For turbulent, time-averaged flows, the Reynolds-Averaged Navier–Stokes (RANS) equations introduce a **turbulent viscosity** $\nu_{t}$ to model the Reynolds stresses:

$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} 
= -\,\nabla p + \nabla \cdot \Bigl[\bigl(\nu + \nu_t\bigr)\,\nabla \mathbf{u}\Bigr]$$
$$\nabla \cdot \mathbf{u} = 0$$
where $\nu_t = \nu_t(x,t)$ is determined by a turbulence model (e.g., $k\text{-}\epsilon$, $k\text{-}\omega$), adding spatially and temporally varying eddy viscosity to the laminar component $\nu$.

**Remark**: Although we present the equations in continuous form, **finite volume** implementations discretize these equations by integrating over control volumes and approximating fluxes at cell faces.

## Reduced-Order Modeling via POD

The **Proper Orthogonal Decomposition (POD)** is a data-driven strategy to identify the most energetic “modes” (or spatial patterns) in a set of high-fidelity solutions. It proceeds as follows:

I. **Finite Volume Discretization**  

   - Suppose the domain $\Omega$ is partitioned into $n$ cells $\{V_1, V_2, \ldots, V_n\}$.  
   - The **finite volume solver** (e.g., OpenFOAM) outputs velocity fields (and possibly pressure fields or other quantities) at cell centers or nodes for discrete times $t_1, t_2, \ldots, t_{N_s}$.

II. **Snapshot Collection**  

   - Let $\mathbf{u}(x,t_k)$ for $k=1, \ldots, N_s$ be the **snapshots** of the velocity solution, typically stored in a vector form $\mathbf{u}_k \in \mathbb{R}^n$.  
   - Collect these snapshots into a matrix $\mathbf{U} \in \mathbb{R}^{n \times N_s}$, where each column corresponds to a snapshot.

III. **Correlation Matrix and Eigenvalue Problem**  

   - Define the correlation matrix 
     $$C_{ij} = \frac{1}{N_s}\,(\mathbf{u}_i,\,\mathbf{u}_j)_{L^2}, 
       \quad i,j = 1,\ldots,N_s$$

   - The inner product $(\cdot,\cdot)_{L^2}$ is approximated in the **finite volume** sense:
     $$(\mathbf{u},\,\mathbf{v})_{L^2}
       \approx 
       \sum_{\ell=1}^{n} \mathbf{u}_{\ell}\,\mathbf{v}_{\ell}\,\Delta V_{\ell}$$
     where $\Delta V_{\ell}$ is the volume of cell $\ell$, and $\mathbf{u}_\ell \cdot \mathbf{v}_\ell$ is the dot product of velocity components.  

   - Solve the eigenvalue problem $C\,g_i = \lambda_i \,g_i$. The eigenvalues $\lambda_i$ measure the “energy” captured by the corresponding eigenvectors $g_i$.

IV. **POD Modes**  

   - For each eigenvector $g_i$, the **POD mode** $\phi_i \in \mathbb{R}^n$ (in discrete form) is typically obtained by:
     $$\phi_i 
       = 
       \frac{1}{\sqrt{\lambda_i}}
       \sum_{k=1}^{N_s} g_{ik}\,\mathbf{u}_k$$

   - Choose the first $N$ modes $\{\phi_1, \ldots, \phi_N\}$ with the largest eigenvalues, ensuring $\sum_{i=1}^{N}\lambda_i$ retains a high percentage (e.g., 90-99%) of the total energy $\sum_{i=1}^{N_s}\lambda_i$.  
   - The velocity field is then approximated by
     $$\mathbf{u}(x,t) 
       \approx 
       \sum_{i=1}^{N} a_i(t)\,\phi_i(x)$$
     where $\phi_i(x)$ is the continuous counterpart of the discrete mode $\phi_i$, and $a_i(t)$ are **time-dependent** modal coefficients.

## Galerkin Projection in a Finite Volume Context

In a classical **finite element** framework, one would take the weak form of the Navier–Stokes equations and directly project it onto POD modes. **Finite volume**, however, operates on the **integral form** of the PDEs and computes fluxes across cell faces. Extending the Galerkin projection idea to FVM involves the following steps:

### I. Integral (Cell-Based) Formulation

For a single cell $V_p$ with boundary $\partial V_p$, the integral form of the laminar Navier–Stokes equations reads:

$$\int_{V_p} \frac{\partial \mathbf{u}}{\partial t}\, dV
+
\int_{\partial V_p} (\mathbf{u}\cdot \mathbf{n})\,\mathbf{u}\, dS
=
-\,\int_{V_p} \nabla p\, dV
+
\nu \int_{\partial V_p} \nabla \mathbf{u}\cdot \mathbf{n}\, dS$$
where $\mathbf{n}$ is the outward unit normal on $\partial V_p$. For a RANS model, the term $\nu$ becomes $\nu + \nu_t$, and there may be additional modeled stress terms.

### II. POD Expansions for All Fields

To apply POD-Galerkin, we typically expand not only $\mathbf{u}$ but also any additional fields that appear in the equations:

- **Velocity**:
  $$\mathbf{u}(x,t) 
    \approx 
    \sum_{i=1}^N a_i(t)\,\phi_i(x)$$

- **Pressure** (if needed for strong coupling):
  $$p(x,t) 
    \approx 
    \sum_{i=1}^N a_i(t)\,\chi_i(x)$$

- **Turbulent viscosity** $\nu_t$ (RANS case):
  $$\nu_t(x,t) 
    \approx 
    \sum_{i=1}^N a_i(t)\,\xi_i(x)$$

Here, $\phi_i(x)$, $\chi_i(x)$, and $\xi_i(x)$ are the POD modes for velocity, pressure, and turbulent viscosity, respectively. Each additional field may require a separate snapshot set and POD procedure if it must be dynamically approximated.

### III. Inserting the Reduced Expansions

Substitute the expansions into the finite volume integral equations. Each term—convective flux, diffusive flux, and pressure gradient—becomes a function of $\{a_i(t)\}$. For instance, the **nonlinear convection** term in cell $V_p$ can be written as:

$$\int_{\partial V_p} (\mathbf{u}\cdot \mathbf{n})\,\mathbf{u}\, dS
\approx
\int_{\partial V_p} 
\Bigl(\sum_{i=1}^N a_i(t)\,\phi_i\Bigr)\,\cdot \mathbf{n}
\Bigl(\sum_{j=1}^N a_j(t)\,\phi_j\Bigr)\, dS$$

Such products yield **bilinear** or higher-order combinations in the coefficients $a_i(t)$. In practice, one often assembles these flux integrals offline using the known POD modes to create “projection” tensors or matrices.

### IV. Projection onto the POD Modes

To derive the final **reduced** system of ODEs in time, we perform an additional projection (or inner product) with each POD mode, typically the same discrete $L^2$-type product used in the POD generation. Formally, for each mode $\phi_m$,

$$\int_{V_p} 
\phi_m^\top \,\frac{\partial \mathbf{u}}{\partial t}\, dV
+
\int_{V_p} 
\phi_m^\top \,\nabla \cdot (\mathbf{u}\otimes \mathbf{u})\, dV
=
-\,
\int_{V_p} 
\phi_m^\top \,\nabla p\, dV
+
\nu
\int_{V_p} 
\phi_m^\top \,\nabla \cdot (\nabla \mathbf{u})\, dV$$
summing over all cells in practice. Numerically, we replace volume integrals by discrete cell-based sums and face-based flux computations:

$$\sum_{p=1}^{n} 
\phi_m^\top(p)\,\Delta V_p \,\frac{\partial \mathbf{u}(p,t)}{\partial t}
+
\sum_{faces} \cdots
=
\ldots$$

After collecting terms in $\{a_i(t)\}$, we obtain a **nonlinear ODE system** for the time evolution of the modal coefficients $a_i(t)$:

$$\frac{d a_j(t)}{dt}
=
F_j\bigl(\{a_i(t)\}\bigr),
\quad
j = 1,\ldots,N$$
where $F_j(\cdot)$ represents the combination of **convective**, **diffusive**, and **pressure** effects (and turbulence if RANS). The result is a system of dimension $N \ll n$, allowing faster simulations once it has been assembled.

## Handling Pressure and Boundary Conditions

### Pressure Treatment

- **Divergence-Free Modes**: In some FE-based POD-Galerkin approaches, the velocity modes are chosen to be **divergence-free**, which can simplify the pressure term. However, in an FVM approach, velocity fields often only satisfy $\nabla \cdot \mathbf{u} = 0$ in an integral sense across faces.  
- **Pressure Modes**: One approach is to include **pressure** in the reduced basis. Then we expand $p$ in its own set of POD modes $\{\chi_i\}$. This can be important for open domains or strongly varying pressure fields.  
- **Pressure Correction Step**: Some implementations adopt a fractional-step or pressure-correction scheme in the high-fidelity code. Adapting these steps in the reduced model can be tricky but sometimes necessary for stability and consistency.

### Boundary Conditions

- **Physical Boundaries**: In FVM, boundary conditions are enforced through face-based flux definitions. The POD modes themselves might not strictly enforce boundary conditions if the snapshots did not revolve around the same BC setting.  
- **Data-Consistent Snapshots**: A practical strategy is to make sure all high-fidelity snapshots **respect** the intended boundary conditions so that the resulting POD modes naturally reflect them.  
- **Penalization or Correction**: If boundary conditions vary or are only partially enforced by the modes, a separate **penalty term** or correction approach in the reduced system might be required.

## Discretization of Nonlinear Terms

In an FVM code, the nonlinear convection term is typically computed as a flux:

$$\int_{V_p} (\mathbf{u} \cdot \nabla)\mathbf{u} \, dV
=
\sum_{faces \in \partial V_p} \mathbf{F}_{face}$$
where $\mathbf{F}_{face}$ is evaluated using an **upwind**, **central differencing**, or another flux-limiting scheme. For the reduced model:

I. **Flux Approximation**: Each $\mathbf{F}_{face}$ must be approximated in terms of the POD coefficients $\{a_i\}$.  

II. **Quadratic Terms**: Because $\mathbf{F}_{face}$ depends on $\mathbf{u}^2$ (schematically) through $(\mathbf{u}\cdot \mathbf{n})\mathbf{u}$, the resulting expression will have **quadratic** dependence on $\{a_i\}$.  

III. **Pre-Computed Operators**: Often, one pre-computes certain integrals or flux evaluations offline using the known POD modes, then assembles them into a smaller operator or tensor to expedite the online solution phase.

## Turbulence Modeling for RANS

In the **RANS** context, a major complication is the additional **turbulent viscosity** $\nu_t$:

$$\nabla \cdot [(\nu + \nu_t) \nabla \mathbf{u}]$$
One may generate snapshots of $\nu_t(x,t)$ from the high-fidelity simulations (e.g., from a $k\text{-}\epsilon$ solver) and then compute POD modes for $\nu_t$ similarly. The final reduced model might look like:

$$\frac{d a_j(t)}{dt}
=
-\,(\text{nonlinear convection in } \{a_i\})
+
(\text{diffusion with } \nu + \nu_t(\{a_i\}))
+
\ldots$$

Because $\nu_t$ depends on the same or an additional set of modes, the resulting system may exhibit **higher-order nonlinearities**, requiring careful treatment (e.g., **empirical interpolation** or other hyper-reduction strategies) for computational efficiency.

## Final Reduced System

After including all relevant terms—convective, diffusive, pressure, turbulence, boundary corrections—the reduced system emerges as:

$$\dot{a}(t)
=
\mathbf{F}\bigl(a(t)\bigr)$$

where $a(t) = (a_1(t),\ldots,a_N(t))^\top$, and $\mathbf{F}$ encodes the integrals and fluxes in the reduced basis. This system can be:

- **Nonlinear ODE** of dimension $N$.  
- **Stiff** if the original CFD problem is stiff, often tackled with appropriate time-stepping or implicit methods.  
- **Significantly cheaper** than the full FVM model (dimension $n$), provided $N \ll n$.

### Computational Considerations

- **Mode Computation**:
The POD modes $\phi_i(x)$ are computed once, offline, using snapshots from a high-fidelity simulation.
- **Assembly of ROM Operators**:
Integrals needed for $B, C, A$ (and turbulence matrices) can be computed via numerical quadrature at cell centers/faces, reusing the FVM geometry data.
- **Efficiency Gains**:

By reducing from a large-scale CFD problem (millions of cells) to a handful of ODEs in terms of $a_i(t)$, significant computational speedups are possible during repeated simulations, sensitivity analyses, or real-time control.

### Challenges and Ongoing Research

I. **Ensuring Divergence-Free Modes**:

In FE-based POD, it's common to ensure each mode is approximately divergence-free. In FVM, achieving divergence-free modes may require a special POD procedure or additional constraints.

II. **Pressure Treatment**:

Without explicitly projecting the pressure field, some approximation or correction might be needed. Alternatively, one can include pressure modes or rely on a pressure Poisson equation at the reduced level.

III. **Turbulence Modeling**:

For RANS, incorporating turbulence closure terms at the reduced level is non-trivial. One must snapshot also the turbulent viscosity (or turbulent kinetic energy and dissipation fields), form POD modes for these fields, and incorporate them into the reduced system.

IV. **Non-Orthogonality of Grids and Flux Formulations**:

FVM often deals with complex, non-orthogonal grids. Incorporating geometric complexities into POD-Galerkin integrals is more complicated than in structured FE meshes. Care is needed in computing scalar products and flux projections.

