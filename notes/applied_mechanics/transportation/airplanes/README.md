# Airplanes

These notes treat the airplane as an applied-mechanics problem: a rigid body held in equilibrium by aerodynamic forces that depend on the shape of its wings, on the Reynolds number and on its attitude. They start from the four forces and the origin of lift, move to airfoil geometry and the polars used to choose a section, explain the role of the Reynolds number, and end with static and dynamic stability, including the longitudinal and lateral modes and pilot-induced oscillations. Inertial navigation and the manufacturing and design process are covered in two further notes. Several notes are illustrated by scripts that compute the results they discuss: a panel method and thin-airfoil theory for NACA sections, the drag polar and power curve of a light aircraft, and the eigenvalues of its longitudinal modes.

## Table of Contents

### 1. [How Airplanes Fly](./how_airplanes_work.md)

The four forces, lift from the pressure distribution and from circulation (Kutta–Joukowski and the Kutta condition), why the equal-transit-time explanation is wrong, lift and drag coefficients, finite wings and induced drag, the drag polar, level-flight power, climb and glide, and control surfaces.

### 2. [Airfoil Design](./airfoil_design.md)

Airfoil geometry, the NACA four-digit equations, thin-airfoil zero-lift angle and moment, pressure distributions, centre of pressure and aerodynamic centre, types of stall, design trade-offs, Reynolds-number effects and high-lift devices.

### 3. [Reading Airfoil Polars with Airfoil Tools](./airfoil_tools_walkthrough.md)

What the Airfoil Tools website provides, how its XFOIL polars are computed, how to read the five polar plots, the limits of XFOIL data and a procedure for selecting a section.

### 4. [The Reynolds Number in Flight](./reynolds_number.md)

Definition and meaning, air properties with altitude, Reynolds numbers of flyers from insects to airliners, transition regimes, effects on skin friction and maximum lift, and Reynolds- and Mach-number matching in wind tunnels.

### 5. [Airplane Stability and Control](./airplane_stability.md)

Static longitudinal stability, neutral point and static margin, trim and elevator gradients, short-period and phugoid modes with Lanchester's approximation, flying-qualities requirements, and the lateral–directional modes and dihedral effect.

### 6. [Static and Dynamic Stability of Oscillating Systems](./pecking.md)

Static versus dynamic stability, the five free responses of a damped oscillator and their eigenvalues, the classification applied to aircraft pitch, and pilot-induced oscillations from a delayed pilot in the loop.

### 7. [Inertial Navigation Systems](./inertial_navigation_systems.md)

Accelerometers and gyroscopes and their error models, strapdown and gimballed mechanizations, attitude representations, the navigation equations, error growth and the Schuler oscillation, and INS/GNSS fusion with a Kalman filter.

### 8. [Aircraft Design and Manufacturing](./manufacturing_and_design_process.md)

Requirements and conceptual, preliminary and detailed design, weight-fraction sizing, the Breguet range equation and the constraint diagram, the role of CFD and wind-tunnel tests, certification, and airframe materials and manufacturing.
