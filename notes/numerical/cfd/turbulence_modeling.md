# Turbulence Modeling

## Flow States: Laminar vs. Turbulent

### Laminar Flow
- **Characteristics:**
  - Smoothly varying velocity fields in space and time.
  - Individual "laminae" (sheets) move past each other without generating cross currents.
- **Conditions:**
  - Occurs when fluid viscosity is large enough to damp out any perturbations.
  - Typically observed at low-to-moderate Reynolds numbers.

### Turbulent Flow
- **Characteristics:**
  - Large, nearly random fluctuations in velocity and pressure in both space and time.
  - Fluctuations arise from instabilities growing until nonlinear interactions break them into finer whirls.
  - Whirls are eventually dissipated into heat by viscosity.
- **Conditions:**
  - Occurs at high Reynolds numbers.

## Flow Variable History
- **Typical Time History of Flow Variable $ u $ at a Fixed Point:**
  - Shows the variation of a component of velocity over time.
  - Dashed line indicates the "average" velocity.

## Types of Averages
1. **Time Average**
2. **Volume Average**
3. **Ensemble Average**

### Ensemble Average
- **Definition:**
  - Repeating an experiment multiple times and averaging the quantity (e.g., velocity) at the same position and time in each experiment.
- **Practicality:**
  - Rarely done due to practicality; time or volume averages are used assuming equivalence to the ensemble average.

### Time Average (Stationary Flow)
- **Definition:**
  $$ \overline{u}(y) \equiv \lim_{\tau \to \infty} \frac{1}{2 \tau} \int_{-\tau}^{\tau} u(y, t) dt $$
  - This is the mean value of the flow variable over a long period.

### Velocity Fluctuation
- **Definition:**
  $$ u' \equiv u - \overline{u} $$
  - Deviation of the velocity from its mean value.
- **Properties:**
  - The average of the fluctuation, $ \overline{u'} $, is zero by definition.

### Measuring Fluctuation Strength
- **Average of the Square of the Fluctuating Quantity:**
  - Provides a better measure of fluctuation strength.
  - Always greater than zero.
  
### Example Illustrations
1. **Time History of Velocity:**
   - Shows the time history of a component of a fluctuating velocity at a point in a turbulent flow.
   - Dashed line indicates the average velocity.
   ![Time History of Velocity](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/84461e4c-8c1a-44c3-a8f6-af1ed51fd49e)
2. **Fluctuating Component of Velocity:**
   - Illustrates the fluctuating component of velocity, $ u' $.
3. **Square of the Fluctuating Velocity:**
   - Displays the square of the fluctuating velocity, $ u'^2 $.
   - Dashed line indicates the time average of the square of the fluctuation.

## Governing Equations for Turbulent Flow

### Similarity to Laminar Flow
- The equations governing turbulent flow are the same as those for laminar flow.
- However, solving these equations in the turbulent regime is significantly more complex.

### Solution Approaches
1. **Direct Numerical Simulations (DNS)**
   - Utilizes the computational power of modern computers to integrate the Navier-Stokes equations.
   - Resolves all spatial and temporal fluctuations without modeling.
   - Similar to laminar flow solution procedures but must handle all fluctuations in velocity and pressure.
   - Limited to simple geometries (e.g., channel flows, jets, and boundary layers) due to high computational cost.

2. **Reynolds Averaged Navier-Stokes (RANS) Equations**
   - Found in most CFD packages (e.g., FLUENT).
   - Governs mean velocity and pressure, which vary smoothly and are easier to solve.
   - Requires modeling to "close" the equations, which introduces significant error.

## The Closure Problem in RANS

### Example: Fully Developed Turbulent Flow in a Channel
- **Geometry:**
  - Channel height: $2H$
- **Objective:**
  - Solve for the mean velocity $\overline{u}(y)$.

### Averaged Navier-Stokes Equation
- **Equation:**
  $$ \frac{d}{dy} \overline{u'v'} + \frac{1}{\rho} \frac{dp}{dx} = 
u \frac{d^2 \overline{u}(y)}{dy^2} $$
  - Subject to boundary conditions:
    $$ 
    y = 0 \quad \frac{d \overline{u}}{dy} = 0, \\
    y = H \quad \overline{u} = 0.
    $$
  - Kinematic viscosity $
u = \mu / \rho$.
  - $\overline{u'v'}$ is the Reynolds stress, a higher-order moment needing modeling in terms of $\overline{u}(y)$ and its derivatives.

### Reynolds Stress Modeling (Closure Approximation)
- **Importance:**
  - The quality of the modeling of Reynolds stress determines the reliability of computations.

### Turbulence Parameters
1. **Turbulent Kinetic Energy (k)**
   - Defined as:
     $$ k = \frac{1}{2} (\overline{u'^2} + \overline{v'^2} + \overline{w'^2}) $$
   - Zero for laminar flow.
   - Can be up to 5% of the kinetic energy of the mean flow in highly turbulent cases.

2. **Turbulent Energy Dissipation Rate (ε)**
   - Defined as:
     $$ \epsilon = 
u \left[ \left( \frac{\partial \overline{u'}}{\partial x} \right)^2 + \left( \frac{\partial \overline{v'}}{\partial y} \right)^2 + \left( \frac{\partial \overline{w'}}{\partial z} \right)^2 \right] + \left( \frac{\partial v'}{\partial x} \right)^2 + \left( \frac{\partial w'}{\partial y} \right)^2 + \left( \frac{\partial u'}{\partial z} \right)^2 \right] $$
   - Where $(u', v', w')$ is the fluctuating velocity vector.

### Turbulence Modeling in CFD
- **k-ε Models:**
  - Form the basis of most CFD packages, including FLUENT.
  - Used to model Reynolds stress in terms of $k$ and $\epsilon$.
