## Pressure and Compressibility

Understanding how pressure behaves in fluids that can be compressed is important for accurately describing and predicting the flow of gases at different speeds and conditions. When fluid velocities approach the speed of sound, changes in density and pressure waves become significant, leading to what is known as compressible flow. At lower speeds, where these pressure waves have little effect, the flow can be approximated as incompressible. This distinction matters greatly in fields like aeronautics, where an aircraft’s Mach number (its speed relative to the speed of sound) determines whether compressibility needs to be accounted for.

  
```
 Visualizing Compressible Flow:
 
 Imagine air moving through a nozzle:
 
    Narrowing nozzle (increasing speed)
    ----------------->   --->   -> 
   (Low Ma)                     (Higher Ma)
        |                        |
        v                        v
     incompressible         compressible
         flow                 flow region

 As the air accelerates to speeds closer 
 to the speed of sound, density changes and 
 pressure waves must be considered.
```

  
The governing equations for compressible flow include the continuity equation, momentum equations (Navier-Stokes), the equation of state, and any relevant boundary conditions. Pressure waves traveling at the local speed of sound influence how the fluid responds to changes. At speeds much lower than the speed of sound, these waves do not strongly affect the flow, allowing one to treat density as nearly constant and ignore compressibility effects.

  
### Governing Equations

These equations define the system and characterize compressible behavior:

• The equations of motion and state describe how pressure, density, and velocity interact in compressible conditions.  
• Pressure waves travel at the speed of sound, about **347 m/s at 1 atm and 300 K**, carrying information about changes in the flow.  
• Compressible flow models must handle these traveling waves, whereas incompressible flow approximations can ignore them.

  
### Compressible vs. Incompressible Flow

Considering how close the flow speed is to the speed of sound helps determine whether compressibility matters. At low Mach numbers, defined as **Ma = v/c** where **v** is the flow velocity and **c** is the speed of sound, density changes are small enough to be neglected. Bernoulli’s equation for incompressible flow states:

\[
\Delta P = \frac{\rho \Delta v^2}{2}.
\]

Taking pressures relative to stagnation and substituting \(\Delta v = v\):

\[
\frac{\Delta P}{P} = \frac{\gamma}{2} \text{Ma}^2,
\]

where **\(\gamma = c_p/c_v\)** is the ratio of specific heats. As speed increases, the Mach number grows, and so does the relative change in pressure. For example:

• At **v = 100 m/s**, Ma ≈ 0.288 at 1 atm, giving \(\Delta P/P_{\text{atm}}\) ≈ 6%. This small percentage shows that density changes remain modest.  
• At **v = 347 m/s**, Ma = 1 at 1 atm, giving \(\Delta P/P_{\text{atm}}\) ≈ 70%, indicating substantial compressibility effects.

When **Ma < 0.3**, compressibility effects are usually negligible, allowing the flow to be considered incompressible. This threshold is widely used as a practical guideline in engineering calculations.

  
### Low-Mach Flows and Numerical Stiffness

Even at low Mach numbers, if the flow is considered compressible in a numerical simulation, one must account for the presence of acoustic waves (sound waves), which are very fast compared to the flow velocity. Unsteady flow solvers must take very small timesteps to resolve these fast-moving waves. The required ratio of timesteps increases as Mach number decreases, because the speed of sound dominates the timescale:

• The ratio of stability-driven timesteps to accuracy-driven timesteps is \(1 + 1/\text{Ma}\).  
• At **Ma = 0.1**, this ratio is 11, meaning 11 times more steps are needed for stability than would be required for accuracy alone. This situation makes the problem numerically **stiff**, prompting methods to reduce this computational burden.

  
## Incompressible Flow

In cases where the Mach number is low and compressibility is negligible, assuming **incompressible flow** simplifies the equations dramatically. Density is taken as constant, and the energy equation can often be ignored. Removing density changes also removes the need to handle acoustic waves, eliminating the numerical stiffness associated with them. With incompressibility, the pressure field adapts itself to satisfy mass conservation constraints, effectively decoupling pressure from density changes.

  
```
 Incompressible Flow Visualization:
 
 Consider a pipe with water:
 
     --> --> -->  (constant density)
 
  Pressure adjusts to ensure 
  mass conservation. Density 
  remains constant, removing 
  the compressibility complexity.
```

  
### Numerical Stiffness Removal

Assuming incompressibility allows using methods like the pressure projection technique:

• Density stays constant, \(\rho = \text{const}\).  
• The energy equation can be ignored, simplifying the math.  
• Equations reduce to mass conservation and momentum conservation.

The nondimensionalized forms of the mass and momentum equations, ignoring gravity, are:

Mass Conservation:

\[
\int_A \vec{v} \cdot \vec{n} \, dA = 0,
\]

ensuring that there is no net flux of fluid out of any closed surface.

Momentum Conservation:

\[
\frac{d}{dt} \int_V \vec{v} \, dV + \int_A \vec{v}(\vec{v}\cdot\vec{n}) \, dA = -\int_A \hat{\boldsymbol{\tau}}\cdot\vec{n} \, dA - \int_A \hat{P}\boldsymbol{\delta}\cdot\vec{n} \, dA,
\]

where \(\hat{\tau} = \tau/\rho\) and \(\hat{P} = P/\rho\). The momentum equation determines velocity given a pressure field, but there is no standalone pressure equation. Instead, pressure must be found by ensuring that the velocity field remains divergence-free.

  
### Deriving the Pressure Equation

Combining the mass and momentum equations leads to a scalar pressure Poisson equation. Starting from the momentum update:

\[
v^{n+1} = v^n + h(-\nabla \cdot vv - \nabla \cdot \hat{\boldsymbol{\tau}})^n - h\nabla \hat{P}^{n+1},
\]

where \(h = \Delta t\). Applying \(\nabla \cdot\) and using \(\nabla \cdot v=0\):

\[
\nabla^2 \hat{P}^{n+1} = \frac{1}{h}\nabla \cdot (v^n + h(-\nabla \cdot vv - \nabla \cdot \hat{\boldsymbol{\tau}})^n).
\]

Once \(\hat{P}^{n+1}\) is found, the corrected velocity satisfies continuity:

\[
v^{n+1} = H^n - h\nabla \hat{P}^{n+1},
\]

with \(H^n = v^n + h(-\nabla \cdot vv - \nabla \cdot \hat{\boldsymbol{\tau}})^n\).

  
### Boundary Conditions and Pressure Fields

Pressure boundary conditions emerge naturally from applying the momentum equation at boundaries. The result is a velocity field that inherently satisfies incompressibility. Pressure acts as the force that adjusts velocities so that no net fluid accumulates or disappears, effectively enforcing the mass conservation constraint.
