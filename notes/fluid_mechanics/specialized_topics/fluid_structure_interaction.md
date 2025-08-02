# Fluid-Structure Interaction Theory

Fluid-Structure Interaction (FSI) represents one of the most challenging problems in fluid mechanics, involving the theoretical coupling between fluid flow equations and structural dynamics. This section covers the fundamental theoretical framework underlying FSI phenomena.

## Mathematical Formulation

### Governing Equations

#### Fluid Domain (Ωf)
The fluid motion is governed by the Navier-Stokes equations:

**Conservation of mass (continuity)**:
$$\frac{\partial \rho_f}{\partial t} + \nabla \cdot (\rho_f \mathbf{v}) = 0$$

**Conservation of momentum**:
$$\rho_f \frac{D\mathbf{v}}{Dt} = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho_f \mathbf{f}$$

where:
- $\rho_f$ = fluid density
- $\mathbf{v}$ = fluid velocity vector  
- $p$ = pressure
- $\boldsymbol{\tau}$ = viscous stress tensor
- $\mathbf{f}$ = body forces per unit mass

**Stress tensor** for Newtonian fluids:
$$\boldsymbol{\tau} = \mu \left[\nabla \mathbf{v} + (\nabla \mathbf{v})^T\right] - \frac{2}{3}\mu(\nabla \cdot \mathbf{v})\mathbf{I}$$

#### Structural Domain (Ωs)  
The structural motion follows elastodynamics:

**Conservation of momentum**:
$$\rho_s \frac{\partial^2 \mathbf{u}}{\partial t^2} = \nabla \cdot \boldsymbol{\sigma} + \rho_s \mathbf{b}$$

**Constitutive relation** (linear elasticity):
$$\boldsymbol{\sigma} = \mathbf{C} : \boldsymbol{\varepsilon}$$

**Strain-displacement relation**:
$$\boldsymbol{\varepsilon} = \frac{1}{2}\left[\nabla \mathbf{u} + (\nabla \mathbf{u})^T\right]$$

where:
- $\mathbf{u}$ = displacement vector
- $\rho_s$ = structural density
- $\boldsymbol{\sigma}$ = stress tensor
- $\mathbf{C}$ = elasticity tensor
- $\mathbf{b}$ = body forces per unit mass

### Interface Conditions

At the fluid-structure interface (Γ), two conditions must be satisfied:

#### 1. Kinematic Compatibility
The fluid and structure velocities must match at the interface:
$$\mathbf{v}_f = \frac{\partial \mathbf{u}_s}{\partial t} \quad \text{on } \Γ$$

#### 2. Dynamic Equilibrium  
The traction forces must be in equilibrium:
$$\boldsymbol{\sigma}_f \cdot \mathbf{n} = \boldsymbol{\sigma}_s \cdot \mathbf{n} \quad \text{on } \Γ$$

where $\mathbf{n}$ is the unit normal vector pointing from fluid to structure.

## Theoretical Classification

### By Coupling Mechanism

#### Added Mass Effect
The fluid adds apparent mass to the structure:
$$M_{total} = M_s + M_{added}$$

**Theoretical basis**: Potential flow theory around accelerating bodies
$$M_{added} = \rho_f \int_{\Omega_f} \phi \frac{\partial \phi}{\partial n} d\Omega$$

#### Fluid Damping  
Viscous effects provide damping to structural motion:
$$C_{total} = C_s + C_{fluid}$$

#### Fluid Stiffness
Flow-dependent restoring forces:
$$K_{total} = K_s + K_{fluid}$$

### By Flow Regime

#### Potential Flow FSI
For inviscid, irrotational flow:
$$\nabla^2 \phi = 0$$
$$\mathbf{v} = \nabla \phi$$

**Advantages**: Linear theory, analytical solutions possible
**Limitations**: No viscous effects, no flow separation

#### Viscous Flow FSI  
Full Navier-Stokes equations required:
- Boundary layer effects
- Flow separation and reattachment
- Vortex shedding phenomena

#### Turbulent Flow FSI
Additional complexity from turbulence:
- Reynolds-averaged equations
- Turbulence-structure interaction
- Broadband forcing spectra

## Stability Analysis

### Linear Stability Theory

For small perturbations about equilibrium:
$$\mathbf{u} = \mathbf{u}_0 + \delta\mathbf{u}e^{st}$$
$$\mathbf{v} = \mathbf{v}_0 + \delta\mathbf{v}e^{st}$$

**Characteristic equation**: $\det(\mathbf{A} - s\mathbf{I}) = 0$

**Stability criteria**:
- $\Re(s) < 0$: Stable (damped)
- $\Re(s) = 0$: Neutral stability  
- $\Re(s) > 0$: Unstable (growing)

### Flutter Analysis

**Critical flutter speed** determined by:
$$\det\left[K + iV C_A + V^2 M_A - \omega^2(M + M_A)\right] = 0$$

where:
- $M_A$ = aerodynamic mass matrix
- $C_A$ = aerodynamic damping matrix  
- $K$ = structural stiffness matrix

### Lock-in Phenomenon

**Strouhal frequency**: $f_{St} = \frac{St \cdot U}{D}$

**Lock-in condition**: $f_{St} \approx f_n$ (structural natural frequency)

**Theoretical prediction**: Van der Pol oscillator model
$$\ddot{y} + 2\zeta\omega_n\dot{y} + \omega_n^2 y = F_{fluid}(\dot{y}, y, t)$$

## Dimensional Analysis

### Key Dimensionless Parameters

#### Reynolds Number
$$Re = \frac{\rho U L}{\mu}$$
Controls the ratio of inertial to viscous forces.

#### Reduced Velocity  
$$U_r = \frac{U}{f_n D}$$
Determines the likelihood of resonance phenomena.

#### Mass Ratio
$$m^* = \frac{m_s}{\rho_f \pi D^2 L/4}$$
Ratio of structural to fluid mass.

#### Damping Parameter
$$\zeta = \frac{c}{2\sqrt{km}}$$
Structural damping ratio.

#### Froude Number (for free surface flows)
$$Fr = \frac{U}{\sqrt{gL}}$$

### Similarity Laws

For model testing, maintain similarity:
$$Re_{model} = Re_{prototype}$$
$$U_r^{model} = U_r^{prototype}$$
$$m^{*model} = m^{*prototype}$$

## Theoretical Solution Methods

### Analytical Methods

#### Perturbation Theory
For weakly coupled problems:
$$\mathbf{u} = \mathbf{u}^{(0)} + \epsilon\mathbf{u}^{(1)} + \epsilon^2\mathbf{u}^{(2)} + ...$$

#### Method of Multiple Scales
For problems with disparate time scales:
$$\mathbf{u}(t) = \mathbf{u}(T_0, T_1, T_2, ...)$$
where $T_n = \epsilon^n t$

#### Matched Asymptotic Expansions
For boundary layer problems in FSI.

### Theoretical Models

#### Quasi-Steady Theory
Assumes instantaneous flow adjustment:
$$F(t) = F_{static}[U(t), \alpha(t)]$$

**Limitations**: Invalid for rapid structural motion

#### Unsteady Aerodynamic Theory
Accounts for flow memory effects:
$$F(t) = \int_{-\infty}^t G(t-\tau)\frac{d\alpha(\tau)}{d\tau}d\tau$$

#### Theodorsen Theory
For oscillating airfoils:
$$F = \pi\rho b^2\ddot{h} + \pi\rho b^2 c\ddot{\alpha} + 2\pi\rho Ub C(k)[\dot{h} + Ub\dot{\alpha}]$$

where $C(k)$ is Theodorsen's function.

## Advanced Theoretical Topics

### Nonlinear FSI Theory

#### Geometric Nonlinearity
Large deformations require updated geometry:
$$\boldsymbol{\varepsilon} = \frac{1}{2}\left[\nabla \mathbf{u} + (\nabla \mathbf{u})^T + (\nabla \mathbf{u})^T \nabla \mathbf{u}\right]$$

#### Material Nonlinearity  
Non-Hookean constitutive relations:
$$\boldsymbol{\sigma} = \mathbf{C}(\boldsymbol{\varepsilon}) : \boldsymbol{\varepsilon}$$

#### Flow Nonlinearity
Flow separation and vortex dynamics require nonlinear analysis.

### Stochastic FSI

For random excitation (turbulence, waves):
$$\mathbb{E}[\mathbf{u}(t)] = \int_{-\infty}^{\infty} \mathbf{h}(\tau)\mathbb{E}[\mathbf{F}(t-\tau)]d\tau$$

**Power spectral density approach**:
$$S_{uu}(\omega) = |\mathbf{H}(\omega)|^2 S_{FF}(\omega)$$

### Computational Theory

#### Arbitrary Lagrangian-Eulerian (ALE)
Mesh motion to track interface:
$$\frac{\partial \mathbf{v}}{\partial t}\bigg|_{\chi} + (\mathbf{v} - \mathbf{w}) \cdot \nabla \mathbf{v} = \mathbf{f}$$

where $\mathbf{w}$ is mesh velocity.

#### Interface Tracking Methods
- Level set method
- Volume of fluid (VOF)  
- Immersed boundary method

#### Partitioned vs. Monolithic Coupling
**Partitioned**: Separate fluid and structural solvers
**Monolithic**: Unified system solution

## Theoretical Applications

### Aeroelasticity Theory
- Wing flutter prediction
- Gust response analysis
- Control surface effectiveness

### Hydroelasticity Theory  
- Ship hull vibrations
- Sloshing dynamics
- Wave-structure interaction

### Bio-FSI Theory
- Blood flow in arteries
- Heart valve dynamics
- Swimming and flying locomotion

### Industrial FSI Theory
- Heat exchanger tube vibrations
- Turbine blade dynamics  
- Pipeline flow-induced vibrations

## Open Theoretical Questions

### Turbulence-Structure Interaction
- Coherent structure effects
- Energy transfer mechanisms
- Modelling challenges

### Multi-scale Problems
- Bridging molecular and continuum scales
- Homogenization techniques
- Scale separation issues

### Extreme Events
- Rogue wave impacts
- Blast loading theory
- Cavitation-structure interaction

This theoretical framework provides the foundation for understanding FSI phenomena, enabling the development of predictive models and solution methods for complex multiphysics problems.
