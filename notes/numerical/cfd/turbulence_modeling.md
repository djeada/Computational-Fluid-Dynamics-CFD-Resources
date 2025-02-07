# Turbulence Modeling

Turbulence modeling is one of the most challenging aspects of Computational Fluid Dynamics (CFD) due to the complicated, chaotic, and multiscale nature of turbulent flows. In turbulent flows, a wide range of interacting eddies and fluctuating structures exists, and resolving all of these scales directly (as in Direct Numerical Simulation) is often computationally unfeasible for most engineering applications. Instead, engineers rely on turbulence models to approximate the effects of these fluctuations on the mean flow.

## Flow States: Laminar vs. Turbulent

Understanding the differences between laminar and turbulent flow is important to turbulence modeling.

### Laminar Flow

- Characteristics:
- The velocity field is smooth and orderly in both space and time.
- Fluid particles move along well-defined streamlines or "laminae" that slide past one another.
- There is little to no mixing perpendicular to the flow direction.
- Conditions:
- Typically observed at low-to-moderate Reynolds numbers, where viscous forces dominate and damp out disturbances.
- The flow remains stable, and any perturbations are quickly dissipated by the fluid’s viscosity.

### Turbulent Flow

- Characteristics:
- The flow exhibits large, seemingly random fluctuations in velocity and pressure.
- Turbulent flow is characterized by chaotic eddies and vortices of varying scales.
- Energy is cascaded from larger eddies to smaller ones, finally dissipating as heat due to viscosity.
- Conditions:
- Occurs at high Reynolds numbers, where inertial forces overcome viscous damping, leading to instability and chaotic motion.
- The mixing in turbulent flows enhances momentum, heat, and mass transfer.

## Flow Variable History

One common way to analyze turbulent flows is to study the time history of flow variables, such as velocity, at a fixed point in space.

- Typical Time History of a Flow Variable $u$:
- Shows the instantaneous values of a velocity component over time.
- A dashed line or other visual indicator is often used to represent the long-term average (mean) value of the variable.
This approach helps to distinguish between the underlying mean flow and the superimposed turbulent fluctuations.

## Types of Averages

Averaging is a key concept in turbulence modeling because the instantaneous flow field is highly irregular. By applying various averaging techniques, we obtain a smoother, more tractable field that still captures the necessary physics.

I. Time Average

II. Volume Average

III. Ensemble Average

### Ensemble Average

- Definition:
- The ensemble average is calculated by repeating an experiment or simulation multiple times and averaging the quantity (e.g., velocity) at the same spatial location and time.
- Practicality:
- Although conceptually rigorous, ensemble averaging is rarely feasible in practice due to the need for multiple independent realizations. Instead, time or volume averages are often used under the assumption that they are statistically equivalent to the ensemble average (this is the ergodic hypothesis).

### Time Average (Stationary Flow)

- Definition:
$$\overline{u}(y) \equiv \lim_{\tau \to \infty} \frac{1}{2\tau} \int_{-\tau}^{\tau} u(y,t) , dt$$

- This formula represents the mean value of a flow variable over a long period and is particularly applicable to statistically stationary flows where the statistics do not change with time.

### Velocity Fluctuation

- Definition:
$$u' \equiv u - \overline{u}$$

- Here, $u'$ represents the deviation of the instantaneous velocity from its mean value. By definition, the time average of the fluctuations is zero: $\overline{u'} = 0$.

### Measuring Fluctuation Strength

- Square of the Fluctuating Quantity:
- The mean of the square of the fluctuations, $\overline{u'^2}$, provides a measure of the turbulence intensity and is always a positive value.
- This measure is often used to quantify the energy contained in the turbulent fluctuations.

## Example Illustrations

I. Time History of Velocity:

- A plot showing the instantaneous velocity at a point over time with a dashed line indicating the mean velocity. This visualization helps separate the turbulent fluctuations from the underlying mean flow.
- Dashed line indicates the average velocity.

![Time History of Velocity](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/84461e4c-8c1a-44c3-a8f6-af1ed51fd49e)
   
II. Fluctuating Component of Velocity:

- A graph illustrating $u'$, the deviation of the instantaneous velocity from the mean, highlighting the random nature of turbulence.

III. Square of the Fluctuating Velocity:

- A plot displaying $u'^2$ over time, with the dashed line representing its time average. This is a direct measure of the turbulent relating to motion energy associated with the fluctuations.

## Governing Equations for Turbulent Flow

### Similarity to Laminar Flow

- The important equations governing fluid flow—the Navier–Stokes equations—remain the same for both laminar and turbulent flows.
- However, in turbulent flow, the presence of rapid fluctuations necessitates additional techniques, such as averaging and modeling, to capture the effects of turbulence.

### Solution Approaches

I. Direct Numerical Simulations (DNS)

- Description:  
 DNS involves solving the full, unaveraged Navier–Stokes equations without any turbulence models, resolving all scales of motion.

- Advantages:  
 Provides the most detailed and accurate representation of turbulence.

- Limitations:  
 Extremely computationally expensive and typically limited to simple geometries and low Reynolds numbers.

II. Reynolds-Averaged Navier-Stokes (RANS) Equations

- Description:  
 RANS equations result from applying an averaging process (typically time averaging) to the Navier–Stokes equations, resulting in equations for the mean flow quantities.

- Advantages:  
 Computationally efficient and widely used in industrial applications.

- Limitations:  
 Require turbulence models (closure approximations) to represent the effects of the turbulent fluctuations (e.g., Reynolds stresses), which can introduce significant uncertainties.

## The Closure Problem in RANS

When the Navier–Stokes equations are averaged, additional terms known as Reynolds stresses appear. These stresses represent the momentum transfer due to turbulent fluctuations and are not directly determined by the mean flow equations. This introduces the closure problem, which requires additional modeling to relate the Reynolds stresses to the mean flow variables.

### Example: Fully Developed Turbulent Flow in a Channel

- Geometry:
- Consider a channel of height $2H$.
- Objective:
- Solve for the mean velocity profile $\overline{u}(y)$ across the channel.

### Averaged Navier-Stokes Equation

A simplified form of the averaged momentum equation in the wall-normal direction may be written as:

$$\frac{d}{dy} \overline{u'v'} + \frac{1}{\rho} \frac{dp}{dx} = \nu \frac{d^2 \overline{u}(y)}{dy^2}$$

with boundary conditions such as:

$$\begin{aligned}
& y = 0: \quad \frac{d\overline{u}}{dy} = 0, \\
& y = H: \quad \overline{u} = 0,
\end{aligned}$$

where:

- $\nu = \mu/\rho$ is the kinematic viscosity.
- $\overline{u'v'}$ is the Reynolds shear stress, a term that requires modeling in terms of $\overline{u}(y)$ and its derivatives.

### Reynolds Stress Modeling (Closure Approximation)

- Importance:  
The accuracy of RANS-based predictions depends critically on how well the Reynolds stresses are modeled. Common approaches include eddy-viscosity models, which relate the Reynolds stresses to the mean velocity gradients using a turbulent viscosity concept.

## Turbulence Parameters

Turbulence models often involve additional transport equations for turbulence quantities, which provide insight into the state of the turbulent flow and help close the RANS equations.

I. Turbulent Relating to motion Energy (k)

- Definition:
 $$k = \frac{1}{2} \left( \overline{u'^2} + \overline{v'^2} + \overline{w'^2} \right)$$

- Role:  
 Represents the energy contained in the turbulent fluctuations.

- Typical Magnitudes:  
 In highly turbulent flows, $k$ may account for a few percent (often up to 5%) of the relating to motion energy of the mean flow.

II. Turbulent Energy Dissipation Rate (ε)

- Definition:
 $$\epsilon = \nu \left[ \left( \frac{\partial \overline{u'}}{\partial x} \right)^2 + \left( \frac{\partial \overline{v'}}{\partial y} \right)^2 + \left( \frac{\partial \overline{w'}}{\partial z} \right)^2 + \left( \frac{\partial v'}{\partial x} \right)^2 + \left( \frac{\partial w'}{\partial y} \right)^2 + \left( \frac{\partial u'}{\partial z} \right)^2 \right]$$

- Role:  
 Measures the rate at which turbulent relating to motion energy is dissipated into heat due to viscosity.

- Significance:  
 Accurate modeling of $\epsilon$ is necessary for predicting the decay and spatial distribution of turbulence.

## Turbulence Modeling in CFD

- k-ε Models:
- These models are among the most widely used in industrial CFD simulations.
- They involve solving two additional transport equations—one for the turbulent relating to motion energy $k$ and one for the dissipation rate $\epsilon$—to close the RANS equations.
- Advantages:  
Simplicity and robustness in many engineering applications.

- Limitations:  
May struggle to accurately capture complicated flows with strong anisotropy or near-wall phenomena without further modifications or additional models.

- Other Models:
- k-ω Models:  
Often provide improved performance in the near-wall region.

- Reynolds Stress Models (RSM):  
Offer a more detailed representation by directly modeling the transport equations for the Reynolds stresses, at the expense of higher computational cost.

- Large Eddy Simulation (LES):  
Resolves the larger turbulent scales while modeling only the smallest scales, providing a compromise between DNS and RANS in terms of computational cost and fidelity.

Turbulence modeling remains an active area of research, with ongoing efforts to improve the accuracy of models and reduce the reliance on empirical closure approximations. The integration of data-driven approaches and advanced computational methods continues to push the boundaries of what is achievable in turbulent flow simulations.

