## Pressure and Compressibility

Accurately describing how **pressure** behaves in compressible fluids is important for predicting flows where **density** changes and **pressure waves** are significant. When fluid speeds approach or exceed the speed of sound, such density variations strongly affect the flow field, characterizing the regime as **compressible flow**. At lower speeds, density changes are often insignificant, allowing an **incompressible flow** approximation.

This distinction is important in many applications:

- **Aeronautics:** Aircraft speeds relative to the speed of sound (Mach number) dictate whether compressibility effects (like shocks) must be accounted for.  
- **Industrial flows and pipelines:** Gases moving at high speed can generate shock waves, influencing safety and efficiency.  
- **Acoustics and noise control:** The propagation of pressure waves in gases depends on the speed of sound and compressibility.

### Visualizing Compressible Flow

Imagine air moving through a nozzle:

![nozzle_flow](https://github.com/user-attachments/assets/59f30e4b-664a-4e9b-a438-a305eac2f131)

As the air accelerates to speeds closer to the speed of sound, density changes and pressure waves must be considered.

At **low Mach numbers**, acoustic waves have minimal influence on bulk flow properties, so density can be approximated as constant. At **high Mach numbers**, these pressure waves (traveling at or near the local speed of sound) strongly impact the flow, making compressibility effects unavoidable.

### Governing Equations

When modeling a **compressible** fluid (such as air at higher speeds), **density** $\rho$, **pressure** $p$, and **temperature** $T$ can all vary. The primary equations include:

I. **Continuity (Mass Conservation)**  

$$\frac{\partial \rho}{\partial t} + \nabla \cdot \bigl(\rho,\mathbf{u}\bigr) = 0$$  

where $\mathbf{u} = (u, v, w)$ is the velocity vector. This equation enforces overall mass conservation.

II. **Momentum (Navier–Stokes)**  

$$\frac{\partial (\rho,\mathbf{u})}{\partial t} + \nabla \cdot \bigl(\rho,\mathbf{u},\mathbf{u} + p,\mathbf{I} - \boldsymbol{\tau}\bigr) = \rho,\mathbf{f}$$  

- $\mathbf{u}\mathbf{u}$ is the outer product of the velocity vector with itself.  
- $p,\mathbf{I}$ is the isotropic pressure term ($\mathbf{I}$ = identity tensor).  
- $\boldsymbol{\tau}$ is the viscous stress tensor.  
- $\mathbf{f}$ is a body force per unit volume, such as $\rho,\mathbf{g}$ for gravity.

III. **Energy Equation**  

A common form for the total energy $E$ (internal + relating to motion) is:

$$\frac{\partial (\rho,E)}{\partial t} + \nabla \cdot \Bigl[\mathbf{u},(\rho,E + p) - \mathbf{q}\Bigr] = \rho,\mathbf{f},\cdot,\mathbf{u}$$  

- $E = e + \tfrac{1}{2}|\mathbf{u}|^2$, with $e$ the internal energy per unit mass.  
- $\mathbf{q}$ is the heat flux (e.g., $\mathbf{q} = -k,\nabla T$).  
- The right-hand side represents function done by body forces.

IV. **Equation of State**  

For an ideal gas,

$$p = \rho,R,T$$

linking pressure, density, and temperature. The gas constant $R$ is specific to the fluid in question (e.g., for air, $R \approx 287,\text{J/(kg·K)}$).

### Speed of Sound and Pressure Waves

A key hallmark of **compressible** flow is the presence of **acoustic waves**, traveling at the local speed of sound $a$. For an ideal gas:

$$a = \sqrt{\gamma,\frac{p}{\rho}} = \sqrt{\gamma,R,T}$$

where $\gamma = \tfrac{C_p}{C_v}$ is the ratio of specific heats. At standard atmospheric conditions ($1\text{ atm}$ and $300\text{ K}$), the speed of sound in air is about **347 m/s**.

- In **compressible** flow, these pressure waves strongly influence how the fluid responds to changes.  
- In **incompressible** flow, we effectively set $a \to \infty$, ignoring acoustic wave propagation since density is (nearly) constant.

### Compressible vs. Incompressible Flow

Whether a flow is treated as compressible or incompressible often depends on the **Mach number**:

$$\mathrm{Ma} = \frac{\|\mathbf{u}\|}{a}$$

where $\|\mathbf{u}\|$ is the flow velocity magnitude and $a$ is the local speed of sound.

- **Incompressible Flow ($\mathrm{Ma} \ll 1$)**  
  - Density $\rho$ is nearly constant.  
  - Simplifies to $\nabla \cdot \mathbf{u} = 0$.  
  - Pressure adjusts to enforce mass conservation rather than carrying significant compressibility effects.
- **Compressible Flow ($\mathrm{Ma} \approx 1$ or higher)**  
  - Density varies with changes in pressure and temperature.  
  - Must account for shocks, expansion waves, and other high-speed phenomena.  
  - Requires specialized numerical schemes (finite-volume, Riemann solvers, etc.).
A practical **rule of thumb** in engineering is that if $\mathrm{Ma} < 0.3$, compressibility effects are insignificant, and an incompressible approximation is usually valid.

#### Quantifying Pressure Changes with Mach Number

A simplified Bernoulli-like relation suggests:

$$\frac{\Delta P}{P} \approx \frac{\gamma}{2},\mathrm{Ma}^2$$

- At $\mathrm{Ma} = 0.1$: $\Delta P / P$ is around 0.5%, often considered insignificant.  
- At $\mathrm{Ma} = 0.3$: $\Delta P / P$ grows to a few percent—still small but not always trivial.  
- Approaching $\mathrm{Ma} = 1$: $\Delta P$ becomes a significant fraction of $P$.
When speeds reach a substantial fraction of the speed of sound, treating the flow as incompressible can yield large errors; **density changes matter** and must be included.

#### Example: Air Moving Through a Pipe

Below is a schematic illustrating how **incompressible** vs. **compressible** flow assumptions matter. At lower speeds, density remains nearly constant; at higher speeds, density variations and pressure waves dominate.

![compressible_vs_incompressible](https://github.com/user-attachments/assets/73f166dd-d6da-45aa-91b2-16f0cdd52d8e)

**Incompressible Flow (Low Speed):**  

- Pressure primarily adapts to satisfy $\nabla \cdot \mathbf{u} = 0$.  
- No need to model fast acoustic waves; density changes are ignored.

**Compressible Flow (High Speed):**  

- Density and pressure are closely coupled.  
- Speed of sound governs the propagation of waves and shocks.  
- Numerical modeling grows more complicated, requiring explicit treatment of compressibility.

### Low-Mach Flows and Numerical Stiffness

When $\mathrm{Ma}$ is small, a **fully compressible** solver must still resolve **acoustic waves**, which travel at speed $a \gg \|\mathbf{u}\|$. For explicit time-integration methods, the **timestep** $\Delta t$ is limited by the highest wave speed present (the **Courant–Friedrichs–Lewy (CFL)** condition). Consequently:

- **Stability Constraint:** $\Delta t$ must be small enough to capture acoustic waves.  
- **Accuracy Constraint:** $\Delta t$ also must resolve the slower convective flow speed $\|\mathbf{u}\|$.  


Because $\|\mathbf{u}\| / a = \mathrm{Ma} \ll 1$, **acoustic waves** can force **very small** $\Delta t$. This introduces **numerical stiffness**, drastically increasing computational cost.

#### Removing Stiffness via Incompressible Approximation

To avoid solving for extremely fast acoustic waves at small Mach numbers, many simulations use an **incompressible** flow model:

I. **Assume $\rho \approx \text{constant}$** throughout the domain.  

II. **Drop the equation of state** for $\rho$.  

III. **Continuity equation** becomes $\nabla \cdot \mathbf{u} = 0$.  

IV. **Pressure** enforces $\nabla \cdot \mathbf{u} = 0$, rather than evolving from acoustic considerations.

This removes the large disparity in wave speeds and allows larger timesteps, **greatly reducing** the computational burden for $\mathrm{Ma} \ll 1$ flows.

### Deriving the Pressure Equation (Incompressible Flow)

In an **incompressible** flow solver, one typically uses a **pressure projection** or **pressure correction** approach:

I. **Predictor Step (Momentum Update):**  

$$\mathbf{u}^* = \mathbf{u}^n
+ \Delta t \Bigl[-\nabla \cdot (\mathbf{u}\mathbf{u}) - \nabla \cdot \hat{\boldsymbol{\tau}}\Bigr]^n$$

ignoring the new-time pressure term (or using an old-time guess).

II. **Enforce Continuity:**  

$\nabla \cdot \mathbf{u}^{n+1} = 0$  

Since $\mathbf{u}^{n+1} = \mathbf{u}^* - \Delta t ,\nabla \hat{P}^{,n+1}$,

applying $\nabla \cdot$ to both sides yields:

$$\nabla^2 \hat{P}^{,n+1}
= \frac{1}{\Delta t},\nabla \cdot \mathbf{u}^*$$

III. **Corrector Step (Pressure Update):**  

Solve this **Poisson equation** for $\hat{P}^{,n+1} = P^{n+1}/\rho$. Then update  

$$\mathbf{u}^{n+1} = \mathbf{u}^* - \Delta t,\nabla \hat{P}^{,n+1}$$

The result is a divergence-free velocity field.

#### Boundary Conditions and Pressure Fields

For **incompressible** flow, the pressure boundary conditions arise from the momentum equation plus the requirement of zero normal velocity flux at solid walls (or specified inflow/outflow conditions). The resulting Poisson equation for pressure makes sure mass conservation ($\nabla \cdot \mathbf{u}^{n+1} = 0$). Thus, **pressure** acts as a **Lagrange multiplier**, enforcing incompressibility by adjusting velocities so that fluid neither compresses nor dilates within the domain.
