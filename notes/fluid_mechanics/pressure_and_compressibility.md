## Pressure and Compressibility

### Governing Equations
* The system is defined by the governing equations, the equation of state, constitutive relations, and boundary conditions.
* These equations describe compressible flow.
* Pressure waves are part of the solution and travel at the speed of sound (approximately 347 m/s at 1 atm and 300 K).

### Compressible vs. Incompressible Flow
* At low speeds relative to the speed of sound (low Mach numbers), the flow is largely unaffected by these waves and is termed incompressible.
* From Bernoulli's equation (ignoring gravity), we have:

$$
\Delta P = \frac{\rho \Delta v^2}{2}.
$$

* Taking pressures relative to stagnation and using $\Delta v = v$, we get:

$$
\frac{\Delta P}{P} = \frac{\gamma}{2} \text{Ma}^2,
$$

where $\gamma = c_p/c_v$ and Ma is the Mach number ($v/c$).

### Examples
* For $v = 100$ m/s, $\Delta P/P_{\text{atm}}$ is 6% (Ma = 0.288 at 1 atm).
* For $v = 347$ m/s, $\Delta P/P_{\text{atm}}$ is 70% (Ma = 1 at 1 atm).
* Flows are considered incompressible for $\text{Ma} < 0.3$.

### Low-Mach Flows
* At low speeds, acoustic waves do not significantly alter the thermodynamic state or velocity fields.
* However, unsteady, explicit flow solvers must take timesteps based on the smallest timescales, corresponding to acoustic waves ( $v + c$).
* This creates a numerically *stiff* problem, requiring many small timesteps for stability.
* The ratio of timesteps needed for stability to those needed for accuracy is $(v + c) / v = 1 + 1/\text{Ma}$.

### Example of Stiffness
* At Ma = 0.1 (34.7 m/s in air at 1 atm), 11 times more steps are needed for stability than for accuracy.

## Incompressible Flow

### Numerical Stiffness Removal
* Numerical stiffness can be removed by assuming the flow is incompressible and using a pressure projection method.
* Density is assumed constant, and the energy equation is not required.
* The resulting equations, ignoring gravity and using $\hat{\tau} = \tau/\rho$ and $\hat{P} = P/\rho$, are:

#### Mass Conservation

$$
\int_A \vec{v} \cdot \vec{n} \, dA = 0
$$

#### Momentum Conservation

$$
\frac{d}{dt} \int_V \vec{v} \, dV + \int_A \vec{v} \vec{v} \cdot \vec{n} \, dA = -\int_A \hat{\boldsymbol{\tau}} \cdot \vec{n} \, dA - \int_A \hat{P} \boldsymbol{\delta} \cdot \vec{n} \, dA
$$

### Pressure and Velocity
* These are two equations in $\vec{v}$ and $P$.
* The momentum equation provides $\vec{v}$, but there is no explicit pressure equation.
* The mass equation (continuity) constrains the velocities.
* Pressure acts as a scalar field that adjusts velocity components to satisfy continuity.
* A pressure equation is derived by taking the divergence of the momentum equation.

### Pressure Equation
* Consider the differential form of the mass and momentum equations (dropping vector arrows for simplicity):

\begin{align}
\text{mass:} & \quad 
abla \cdot v = 0 \\
\text{momentum:} & \quad \frac{dv}{dt} = -
abla \cdot vv - 
abla \cdot \hat{\boldsymbol{\tau}} - 
abla \hat{P}
\end{align}

* Apply a simple Explicit Euler integration over one timestep $h = \Delta t$:

$$
v^{n+1} = \underbrace{v^n + h\left(-
abla \cdot vv - 
abla \cdot \hat{\boldsymbol{\tau}}\right)^n}_{H^n} - h 
abla \hat{P}^{n+1}.
$$

* Here, $\hat{P}$ is taken at step $n+1$.

* Using $
abla \cdot v = 0$ applied to this $v^{n+1}$ equation, we get an equation for $\hat{P}^{n+1}$:

$$

abla^2 \hat{P}^{n+1} = \frac{1}{h} 
abla \cdot H^n.
$$

* **To advance a step, solve this equation for $\hat{P}$, then use it in the momentum advancement equation for $v^{n+1}$:

$$
v^{n+1} = H^n - h 
abla \hat{P}^{n+1}.
$$

* This velocity satisfies continuity by construction.

### Boundary Conditions
* The pressure equation requires boundary conditions, which are best determined from the momentum equations evaluated on the boundary.
* Pressure boundary conditions are inherently built-in by the insertion of velocities into the continuity equation, considering boundary velocities.
