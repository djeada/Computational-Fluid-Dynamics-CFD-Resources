## POD-Galerkin Projection with Finite Volume

- **Objective:**
  - Address POD-Galerkin projection for FVD.
  - Use OpenFOAM, an open-source FVD solver.
  - Apply POD in the FVD framework.
  - Introduce POD-ROM method in FVD for:
    - Navier-Stokes equations (laminar flow)
    - Reynolds averaged Navier-Stokes equations (turbulent flow)

- **Navier-Stokes Equations (No Turbulence):**
  - **Equations:**
    - $\frac{\partial u}{\partial t} + (u \cdot 
abla)u - 
u \Delta u = -
abla p$
    - $
abla \cdot u = 0$
    - Variables:
      - $u$: field velocity
      - $p$: normalized pressure
      - $
u$: kinematic viscosity
  - **Domain:**
    - Domain $\Omega$ with boundary and initial conditions.

- **Time Evolution:**
  - Assume reduced order solution for velocity:
    - $u(x,t) \approx u_N(x,t) = \sum_{i=1}^N a_i(t)\phi_i(x)$

- **POD Modes:**
  - Chosen for high energy content.
  - POD space:
    - $V_{POD} = \text{span}\{\phi_i\}, \quad i = 1, ..., N$

- **Snapshots:**
  - Velocities sampled at different times:
    - $u(x,t_n) = u_{N_s}(x,t_n), \quad n = 1, ..., N_s$
  - $N_s$: number of snapshots (high fidelity solutions from OpenFOAM).

- **POD Space Minimization:**
  - Minimize difference between snapshots and projection on spatial modes in $L^2$-norm:
    - $V_{POD} = \arg \min \frac{1}{N_s} \sum_{n=1}^{N_s} ||u(x,t_n) - \sum_{i=1}^{N} (u(x), \Phi_i(x))_{L^2} \Phi_i(x)||_{L^2}^2$
    - With:
      - $(\Phi_i, \Phi_j)_{L^2} = \delta_{ij}$
      - $\delta_{ij}$: Kronecker delta function.

- **Correlation Matrix and Eigenvalue Problem:**
  - Build correlation matrix of velocity snapshots.
  - Solve eigenvalue problem:
    - $C \Phi_i = \lambda_i \Phi_i, \quad 1 \leq i \leq N_s$
    - $C$: correlation matrix, $\mathbb{R}^{N_s \times N_s}$
  - Components:
    - $C_{ij} = \frac{1}{N_s} (u(x,t_i), u(x,t_j))_{L^2}, \quad \text{for } i, j = 1, ..., N_s$

- **Basis Functions:**
  - Basis functions:
    - $\Phi_i(x) = \frac{1}{\sqrt{\lambda_i}} \sum_{n=1}^{N_s} g_{in}u_n(x), \quad i = 1, ..., N_s$
  - First modes retain most energy from original solutions.

- **Insertion and Galerkin Method:**
  - Insert the reduced order solution into the Navier-Stokes equations and apply the Galerkin method:
    
$$
    \frac{da_j(t)}{dt} = 
u \sum_{i=1}^N B_{ji}a_i(t) - \sum_{i=1}^N \sum_{k=1}^N \sum_{l=1}^{N_s} C_{jkl}a_k(t)a_l(t), \quad j = 1, ..., N
    $$


- **Definitions:**
  - $B_{ji} = (
abla \Phi_j, 
abla \Phi_i)_{L^2}$
  - $C_{jkl} = (\Phi_j, (\Phi_k \cdot 
abla) \Phi_l)_{L^2}$
  - $a_j(0) = (u_0, \Phi_j)_{L^2}$

- **Autonomous Dynamical System:**
  - The equation can be written as:
    
$$
    \dot{a} = 
u Ba - a^T Ca
    $$


- **Assumptions:**
  - (i) Pressure term is omitted because POD modes are divergence-free fields satisfying the continuity equation. 
    - Galerkin projection of the pressure term:
      
$$
      (\Phi_i, 
abla p)_{L^2} = \int_\Omega \Phi_i \cdot 
abla p = - \int_\Omega p 
abla \cdot \Phi_i dx + \int_{\partial \Omega} p (\Phi_i \cdot n) ds = 0
      $$

      - First term: zero due to the continuity equation.
      - Second term: zero for enclosed flows.
  - (ii) Term $B_{ji}$ (diffusive term) derived using Green's formula in the finite element weak formulation.

- **Considerations for FVD:**
  - Important considerations for the final model for POD-G-ROM for FVD:
    - Consider momentum balance for Navier-Stokes equations.
    - Integral form on a generic control volume $V_P$:
      
$$
      \int_{t}^{t+\Delta t} \frac{\partial}{\partial t} \int_{V_p} ucdV + \int_{t}^{t+\Delta t} \int_{\partial V_p} (u \cdot 
abla)u \cdot 
u dV = \int_{t}^{t+\Delta t} \int_{\partial V_p} \Delta u \cdot 
u - \int_{t}^{t+\Delta t} \int_{V_p} 
abla p dt = 0
      $$


- **Discretization of N-S Equations:**
  - Issues to address for proper POD-FV-ROM:
    - (i) Discretize the convective non-linear term using upwind factors and Gauss theorem:
      
$$
      \int_{V_p} (u \cdot 
abla)u dV = \int_{\partial V_p} (uu \cdot 
u) \approx \sum_{S_f} S_f \cdot uu_f = \sum_{S_f} F \cdot uu_f
      $$

      - $S_f$: face area vector.
      - $F$: face flux.
      - Consider flux field for consistency with the high order model.
    - (ii) Discretize the continuity equation:
      
$$
      \int_{V_p} 
abla \cdot udV = \sum_{S_f} S_f \cdot u_f = 0
      $$

      - Divergence-free constraint applied to the face flux, not the cell center value.
      - Cannot neglect the pressure term as snapshots at the cell center are not divergence-free.
    - (iii) Discretize the diffusive term:
      
$$
      \int_{V_p} \Delta u dV = \sum_{S_f} S_f 
abla u = 
u \sum_{j} \frac{A}{d} (u_f - u_{|d|}) + k \cdot (
abla u)
      $$

      - First term: orthogonal part.
      - Second term: non-orthogonal part.
      - Another discretization method using Green's formula:
        
$$
        
u \int_{V_p} 
abla \cdot 
abla u dV = \sum_{S_f} S_f \cdot 
abla u = \sum_{S_f} \left[ f_x \left( \frac{S_f}{V_p} \cdot S_f u_f \right) + (1 - f_x) \left( \frac{S_f}{V_p} \cdot S_f u \right) \right]
        $$

      - Green's formula may lead to different discretizations; typically, the first method is preferred for its accuracy and computational efficiency.

- **POD-FV-ROM Procedure:**
  - Account for issues (i-iii) and modify the POD-G-ROM form.
  - Calculate face flux and include pressure terms.
  - Include boundary conditions in the formulations.
  - Construct face flux and pressure using the same coefficients as for velocity:
    
$$
    F(x,t) \approx F_{N_s}(x,t) = \sum_{i=1}^{N_s} a_i(t)\psi_i(x)
    $$

    
$$
    p(x,t) \approx p_{N_s}(x,t) = \sum_{i=1}^{N_s} a_i(t)\chi_i(x)
    $$

    - $\psi_i(x)$ and $\chi_i(x)$: spatial modes for flux and pressure, respectively.
    - Modes calculated using the correlation matrix of velocity.
    - Snapshots for flux and pressure:
      
$$
      \psi_i(x) = \frac{1}{\sqrt{\lambda_i}} \sum_{n=1}^{N_s} g_{in} F_n(x), \quad i = 1, ..., N_s
      $$

      
$$
      F_n(x) = F(x,t_n), \quad n = 1, ..., N_s
      $$

      
$$
      \chi_i(x) = \frac{1}{\sqrt{\lambda_i}} \sum_{n=1}^{N_s} g_{in} p_n(x), \quad i = 1, ..., N_s
      $$

      
$$
      p_n(x) = p(x,t_n), \quad n = 1, ..., N_s
      $$


- **State Vector Expansion:**
  - Expand variables of interest as linear combinations of state vector spatial modes:
    
$$
    \begin{align*}
    u(x,t) &\approx u_{N_s}(x,t) = \sum_{i=1}^{N_s} a_i(t) \phi_i(x) \\
    F(x,t) &\approx F_{N_s}(x,t) = \sum_{i=1}^{N_s} a_i(t) \psi_i(x) \\
    p(x,t) &\approx p_{N_s}(x,t) = \sum_{i=1}^{N_s} a_i(t) \chi_i(x)
    \end{align*}
    $$


- **POD-FV-ROM Equations:**
  - Insert the expansions into the Navier-Stokes equations to get:
    
$$
    \frac{da_j(t)}{dt} = 
u \sum_{i=1}^{N} B_{ji} a_i(t) - \sum_{k=1}^{N} \sum_{l=1}^{N_s} C_{jkl} a_k(t) a_l(t) + \sum_{i=1}^{N} A_{ji} a_i(t), \quad j = 1, ..., N
    $$


- **Definitions:**
  - $B_{ji} = (\phi_j, \Delta \phi_i)_{L^2}$
  - $C_{jkl} = (\phi_j, (\psi_k \cdot 
abla) \phi_l)_{L^2}$
  - $A_{ji} = (\phi_j, 
abla \chi_i)_{L^2}$

- **Dynamical System:**
  - Final system:
    
$$
    \dot{a} = 
u Ba - a^T Ca - Aa
    $$


- **Boundary Conditions:**
  - Use POD penalty method to enforce boundary conditions:
    
$$
    (\Phi_i, u + (u \cdot 
abla)u - 
u \Delta u + 
abla p + r(\tau - u_{BC}))_{L^2} = 0
    $$

  - $u_{BC}$: Dirichlet boundary condition
  - $\tau$: penalty factor
  - $r$: null function except on the boundary

- **Advantages:**
  - Ensures approximated velocity respects boundary conditions.
  - Avoids issues with long-time integration behavior.

- **Final POD-FV-ROM System:**
  - Modified system:
    
$$
    \frac{da_j(t)}{dt} = 
u \sum_{i=1}^{N} B_{ji}a_i(t) - \sum_{k=1}^{N} \sum_{l=1}^{N_s} C_{jkl}a_k(t)a_l(t) + \sum_{i=1}^{N} A_{ji}a_i(t) + \tau (u_{BC}, E_j)_{L^2}a_i(t), \quad j = 1, ..., N
    $$

  - Additional terms:
    
$$
    D_j = (\Phi_j, \Phi_j)_{L^2}
    $$

    
$$
    E_j = (\Phi_j, \Phi_j)_{L^2}a_n
    $$

  - Final dynamical system for incompressible laminar N-S equations:
    
$$
    \dot{a} = 
u Ba - a^T Ca - Aa + \tau (u_{BC} D - Ea)
    $$


- **State Vector Expansion for Turbulent Flows:**
  - Expand variables of interest as linear combinations of state vector spatial modes:
    
$$
    \begin{align*}
    u(x,t) &\approx u_{N_s}(x,t) = \sum_{i=1}^{N_s} a_i(t) \phi_i(x) \\
    F(x,t) &\approx F_{N_s}(x,t) = \sum_{i=1}^{N_s} a_i(t) \psi_i(x) \\
    p(x,t) &\approx p_{N_s}(x,t) = \sum_{i=1}^{N_s} a_i(t) \chi_i(x) \\
    
u_t(x, t) &\approx 
u_{t_N}(x, t) = \sum_{i=1}^{N_s} a_i(t) \phi_i(x)
    \end{align*}
    $$


- **POD-FV-ROM for Turbulent Flows:**
  - Insert the expansions into the RANS equations to get:
    
$$
    \frac{da_j(t)}{dt} = 
u \sum_{i=1}^{N} B_{ji}a_i(t) - \sum_{k=1}^{N} \sum_{l=1}^{N_s} C_{jkl}a_k(t)a_l(t) + \sum_{i=1}^{N} A_{ji}a_i(t) + \sum_{i=1}^{N} H_{ji}a_i(t), \quad j = 1, ..., N
    $$


- **Definitions:**
  - $H_{ji} = (
abla \Phi_j, 
u_{t} 
abla \Phi_i)_{L^2}$
  - $
u_{t}$: eddy viscosity

- **RANS Equations:**
  - RANS equations with turbulence modeling:
    
$$
    \frac{\partial u}{\partial t} + (u \cdot 
abla)u = -
abla p + (
u + 
u_{t}) \Delta u + 
abla \tau - \frac{2}{3}k I
    $$

  - Expand turbulent viscosity:
    
$$
    
u_{t}(x, t) \approx 
u_{t_N}(x, t) = \sum_{i=1}^{N} a_i(t) \phi_i(x)
    $$

  - Build snapshots for eddy viscosity:
    
$$
    \phi_i(x) = \frac{1}{\sqrt{\lambda_i}} \sum_{n=1}^{N_s} g_{in} 
u_{t_n}(x), \quad i = 1, ..., N_s
    $$

    
$$
    
u_{t_n}(x) = 
u_t(x, t_n), \quad n = 1, ..., N_s
    $$


- **POD-FV-ROM for RANS Eddy Viscosity Model:**
  - Modified system:
    
$$
    \frac{da_j(t)}{dt} = 
u \sum_{i=1}^{N} B_{ji} a_i(t) + 
u \sum_{i=1}^{N} BT_{ji} a_i(t) - \sum_{k=1}^{N} \sum_{l=1}^{N_s} CT_{jkl} a_k(t) a_l(t) + \sum_{i=1}^{N} CT2_{ji} a_i(t) a_l(t) + \sum_{i=1}^{N} A_{ji} a_i(t) - \sum_{i=1}^{N} \sum_{l=1}^{N_s} E_{jkl} a_i(t) a_l(t) + \tau (u_{BC} D - \sum_{i=1}^{N} E_j a_i(t))
    $$


- **Additional Terms:**
  - $BT_{ji} = (\Phi_j, 
abla \cdot (
u 
abla \Phi_i))_{L^2}$
  - $CT_{jkl} = (\Phi_j, \phi_k \cdot 
abla \Phi_l)_{L^2}$
  - $CT2_{ji} = (\Phi_j, 
u_t 
abla \Phi_i)_{L^2}$

- **Final Dynamical System:**
  - Combined system:
    
$$
    \dot{a} = 
u [B + BT] a - a^T (C - CT1 - CT2)a - Aa + \tau (u_{BC} D - Ea)
    $$




