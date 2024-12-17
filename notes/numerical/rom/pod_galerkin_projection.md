## POD-Galerkin Projection with Finite Volume

Reduced-order modeling (ROM) has become an invaluable technique for accelerating computational fluid dynamics (CFD) simulations without sacrificing too much accuracy. Among ROM techniques, the Proper Orthogonal Decomposition (POD) coupled with a Galerkin projection approach is well-established. However, most classical POD-Galerkin frameworks assume finite element (FE) formulations because the weak variational form and associated inner products emerge naturally from FE theory.

In contrast, finite volume discretizations (FVD) form the backbone of many industry and academic CFD solvers, such as OpenFOAM. FVD directly enforce integral conservation laws over discrete volumes (cells), making the derivation of a consistent POD-Galerkin-ROM less straightforward. The aim here is to extend the POD-Galerkin approach to an FVD framework, enabling us to construct reduced-order models for both laminar and turbulent (RANS) Navier-Stokes equations using data from a finite volume solver.

### Equations and Problem Setting

#### Governing Equations

For simplicity, consider the incompressible Navier-Stokes equations:

I. **Incompressible Navier-Stokes (Laminar):**

$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot 
abla)\mathbf{u} = - 
abla p + 
u \Delta \mathbf{u},$$

$$abla \cdot \mathbf{u} = 0,$$
where $\mathbf{u}(x,t)$ is the velocity field, $p(x,t)$ is the normalized pressure, and $
u$ is the kinematic viscosity.

II. **RANS Equations (Turbulent):**

For turbulent flows, the Reynolds-Averaged Navier-Stokes (RANS) equations introduce a turbulent viscosity $
u_t$ that augments the laminar viscosity:

$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot 
abla)\mathbf{u} = - 
abla p + 
abla \cdot (( 
u + 
u_t)
abla \mathbf{u}),$$
along with appropriate turbulence modeling (e.g., $k-\epsilon$ or $k-\omega$) to determine $
u_t(x,t)$.

### Reduced-Order Modeling via POD

**Proper Orthogonal Decomposition (POD)** extracts a low-dimensional subspace capturing the dominant flow dynamics. Suppose we have:

- A computational domain $\Omega$ discretized into $n$ cells (control volumes) by the finite volume method.
- A set of $N_s$ snapshots of the velocity field $\mathbf{u}(x,t_n)$ obtained from a high-fidelity solver like OpenFOAM. Each snapshot is a vector in $\mathbb{R}^n$ representing the velocity (or velocity components) at each cell center or node.

We want to represent the flow field in a reduced form:

$$\mathbf{u}(x,t) \approx u_{N}(x,t) = \sum_{i=1}^N a_i(t)\phi_i(x),$$
where $\{\phi_i(x)\}_{i=1}^N$ are the POD modes obtained from the snapshot data, and $a_i(t)$ are time-dependent coefficients.

#### POD Space Construction

I. **Snapshots:**

Collect velocity snapshots $\mathbf{u}(x,t_n)$, $n=1,\ldots,N_s$. Each snapshot is a high-fidelity solution from OpenFOAM or a similar solver. These snapshots form a snapshot matrix $\mathbf{U}$ of size $n \times N_s$.

II. **Correlation Matrix and Eigenvalue Problem:**

Construct the correlation matrix:

$$C_{ij} = \frac{1}{N_s} (\mathbf{u}(x,t_i), \mathbf{u}(x,t_j))_{L^2}, \quad i,j = 1,\ldots,N_s,$$
where the inner product can be approximated by a discrete $L^2$-inner product over the domain:

$$(\mathbf{u}, \mathbf{v})_{L^2} \approx \sum_{cell} \mathbf{u}_{cell} \cdot \mathbf{v}_{cell} \Delta V_{cell}.$$

Solve the eigenvalue problem:

$$C g_i = \lambda_i g_i,$$
yielding eigenvalues $\lambda_i$ and eigenvectors $g_i$. The eigenvalues reflect the energy content of each mode. Sorting them in descending order ensures that the first few modes capture most of the flow's kinetic energy.

III. **POD Modes:**

The POD modes are given by:

$$\phi_i(x) = \frac{1}{\sqrt{\lambda_i}}\sum_{n=1}^{N_s} g_{in}\mathbf{u}(x,t_n).$$

The dimension $N < N_s$ is chosen to retain only the most energetic modes, greatly reducing the state dimension.

### Galerkin Projection in a Finite Volume Context

Classical POD-Galerkin methods are often introduced in a finite element setting, where the weak form of Navier-Stokes equations naturally emerges, and projecting onto POD modes is straightforward. However, finite volume methods (FVM) differ: the equations are integrated over control volumes, and fluxes are computed at cell faces. This direct flux-based approach does not immediately yield a weak form suitable for standard POD-Galerkin.

To perform a Galerkin projection in FVD:

I. Start from the integral form of the Navier-Stokes equations on each cell $V_p$:

$$\int_{V_p}\frac{\partial \mathbf{u}}{\partial t} dV + \int_{\partial V_p} (\mathbf{u} \cdot 
abla)\mathbf{u} dS = -\int_{V_p} 
abla p dV + 
u \int_{\partial V_p} 
abla \mathbf{u} dS.$$

II. Use the POD expansion $\mathbf{u}(x,t) \approx \sum_{i=1}^N a_i(t)\phi_i(x)$. You must represent not only $\mathbf{u}$ but also other needed fields (e.g., fluxes, turbulence quantities, and pressure) with similar expansions:

$$F(x,t) \approx \sum_{i=1}^N a_i(t)\psi_i(x), \quad p(x,t) \approx \sum_{i=1}^N a_i(t)\chi_i(x).$$

III. Insert these expansions into the FVD integral form. Each integral, originally computed numerically by summing contributions from cell faces, must now be projected onto the POD basis. This is where complexity arises:
- The convective and diffusive flux terms must be expressed in terms of the modal expansions.
- The pressure gradient term and other non-linear terms must also be approximated in the reduced space.
- The divergence-free condition $
abla \cdot \mathbf{u}=0$ in a discrete sense requires careful handling since FVM ensures divergence-freeness via flux consistency at cell faces, not pointwise.

IV. After substitution, integrate against each POD mode $\phi_j$ using the $L^2$-inner product. This yields a system of ODEs in the coefficients $a_i(t)$:

$$\frac{da_j(t)}{dt} = 
u \sum_{i=1}^N B_{ji} a_i(t) - \sum_{k,l} C_{jkl} a_k(t) a_l(t) + \sum_{i=1}^N A_{ji} a_i(t) + \cdots$$

The matrices $B, C, A$ represent the projections of diffusive, convective, and pressure terms, respectively. Additional terms may appear for RANS turbulence modeling and pressure corrections.

### Handling Pressure and Boundary Conditions

**Pressure Term:**

A key assumption often used in FE-based POD-Galerkin is that POD modes are divergence-free. If strictly divergence-free modes are chosen, the pressure term may vanish upon projection. However, in FVM-based solutions, the velocity field may not be globally divergence-free at each cell center—divergence-free conditions are enforced in an integral sense on cell faces.

To handle pressure:
- Compute pressure modes as well, or incorporate a pressure correction step.
- If the domain is enclosed and the modes are nearly divergence-free, the pressure term may become negligible under certain conditions, but this must be checked case by case.
**Boundary Conditions:**
In FVM, boundary conditions significantly affect flux computations. POD modes might not inherently satisfy boundary conditions. To address this:
- Use a penalty method: Add terms in the Galerkin projection that enforce boundary conditions weakly.
- Ensure that at the POD stage, the chosen snapshots come from solutions that satisfy the physical BCs, improving the chance that truncated modes still respect boundaries.

### Discretization of Nonlinear Terms

In FVM, the nonlinear convection term is computed using fluxes at cell faces:

$$\int_{V_p} (\mathbf{u} \cdot 
abla)\mathbf{u} dV = \sum_{faces} \mathbf{F}_{face}(\mathbf{u}),$$
where $\mathbf{F}_{face}$ is evaluated using, e.g., an upwind or central differencing scheme.

For POD-Galerkin:
- The flux $\mathbf{F}(x,t)$ itself must be projected onto the POD modes or approximated using expansions of $\mathbf{u}$.
- A careful approximation is needed: If $\mathbf{u}$ is expanded in modes, the flux, a nonlinear function of $\mathbf{u}$, requires mixing terms (e.g., a quadratic form in coefficients $a_i(t)$).

### Turbulence Modeling for RANS

For RANS, an additional complexity is the turbulent viscosity field $
u_t(x,t)$:

$$u_t(x,t) \approx \sum_{i=1}^N a_i(t) \xi_i(x),$$
where $\xi_i(x)$ are the turbulent viscosity modes computed from turbulent viscosity snapshots. Insert this into the RANS equations to handle the extra terms involving $( 
u + 
u_t)
abla \mathbf{u}$.

This yields extra coupling terms in the reduced ODE system, typically introducing a polynomial nonlinearity in the coefficients $a_i(t)$.

### Final Reduced System

After handling all terms (convective, diffusive, pressure, turbulence, BCs), one arrives at an autonomous or semi-autonomous nonlinear ODE system:

$$\dot{a}(t) = 
u B a(t) - a(t)^T C a(t) - A a(t) + (\text{turbulence terms}) + (\text{boundary terms}),$$
defining a low-dimensional dynamical system for the coefficients $a(t)$.

### Computational Considerations

- **Mode Computation**:
The POD modes $\phi_i(x)$ are computed once, offline, using snapshots from a high-fidelity simulation.
- **Assembly of ROM Operators**:
Integrals needed for $B, C, A$ (and turbulence matrices) can be computed via numerical quadrature at cell centers/faces, reusing the FVM geometry data.
- **Efficiency Gains**:

By reducing from a large-scale CFD problem (millions of cells) to a handful of ODEs in terms of $a_i(t)$, significant computational speedups are possible during repeated simulations, sensitivity analyses, or real-time control.

### Key Challenges and Ongoing Research

I. **Ensuring Divergence-Free Modes**:

In FE-based POD, it's common to ensure each mode is approximately divergence-free. In FVM, achieving divergence-free modes may require a special POD procedure or additional constraints.

II. **Pressure Treatment**:

Without explicitly projecting the pressure field, some approximation or correction might be needed. Alternatively, one can include pressure modes or rely on a pressure Poisson equation at the reduced level.

III. **Turbulence Modeling**:

For RANS, incorporating turbulence closure terms at the reduced level is non-trivial. One must snapshot also the turbulent viscosity (or turbulent kinetic energy and dissipation fields), form POD modes for these fields, and incorporate them into the reduced system.

IV. **Non-Orthogonality of Grids and Flux Formulations**:

FVM often deals with complex, non-orthogonal grids. Incorporating geometric complexities into POD-Galerkin integrals is more complicated than in structured FE meshes. Care is needed in computing scalar products and flux projections.

