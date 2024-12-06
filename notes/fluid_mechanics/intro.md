## Introduction to Fluids

Fluids are substances that continuously deform under an applied shear stress, no matter how small that stress might be. They include liquids, gases, and plasmas. Unlike solids, which can resist a shear force and maintain a shape, fluids flow and take the shape of their containers. Although fluids are made up of countless molecules that move and interact, fluid mechanics often focuses on macroscopic behavior. This shift in perspective makes it possible to use continuum models rather than tracking individual molecules. By treating fluids as continuous media, engineers and scientists can describe pressure, velocity, and other properties at every point in space without worrying directly about the molecular details.

  
```
 Microscopic vs Macroscopic Perspective:
 
 Imagine a box of gas molecules:
 
  Microscopic view:
   ●  ●   ●   ●
    ●    ●  ●
     ●  ●    ● ●
   Molecules moving randomly.
 
  Macroscopic (continuum) view:
   A fluid "blob" with properties 
   defined everywhere (density, pressure).
 
 Under the continuum hypothesis, we 
 assume we can assign properties like 
 density and pressure at every point,
 as if the fluid were smooth and uniform.
```

### From Molecules to Macroscopic Fluids

It helps to start at the microscopic scale, where a fluid consists of a huge number of molecules bouncing around in random motions and interacting through collisions and intermolecular forces. Trying to follow each individual molecule is not only extremely complicated, it is also unnecessary for most practical applications. Instead, we can zoom out and treat the fluid as a continuum. This means ignoring the fine-scale molecular details and describing the fluid in terms of average properties like **density**, **temperature**, and **pressure** defined at every point in space.

By embracing the continuum hypothesis, one imagines taking a very small volume of fluid that still contains enough molecules to represent the average behavior. As this volume shrinks, it must remain large compared to molecular scales so that properties like density do not fluctuate wildly. If this condition is met, the fluid can be treated as a continuous substance with smoothly varying fields of velocity, pressure, and other properties.
  
### The Continuum Hypothesis

The continuum hypothesis is the cornerstone of classical fluid mechanics. It states that fluids can be regarded as continuous media, where properties vary smoothly and are well-defined at infinitely many points. No matter how closely one zooms in, as long as it is not reduced to molecular scales, one always finds a “continuous” fluid. Practically, this means using field variables, often written as functions of space and time, such as:

• Velocity field \(\vec{v}(x,y,z,t)\)  
• Pressure field \(p(x,y,z,t)\)  
• Density field \(\rho(x,y,z,t)\)

This approach greatly simplifies the math and physics, making it possible to write down equations like the Navier-Stokes equations that govern fluid flow. As long as the smallest length scale of interest is much larger than the molecular mean free path, the continuum assumption holds well.

  
### Pressure in Fluids

Pressure is one of the most fundamental properties used to describe fluids at the macroscopic scale. Physically, pressure can be thought of as the average force per unit area that the fluid’s molecules exert on a surface. In a gas, molecules are constantly hitting the walls of a container, and the collective effect of these collisions results in a measurable pressure. In a liquid, molecules are closer together, and the pressure reflects the short-range intermolecular forces.

At the continuum level, pressure is treated as a smoothly varying scalar field defined at every point in the fluid. It influences how fluids move and respond to forces. For example, pressure differences drive fluid flows. If one region of a fluid has higher pressure than another, the fluid moves from high-pressure zones to low-pressure zones. In equilibrium, pressure often varies with depth or height due to gravity, leading to familiar situations like higher pressure at the bottom of a swimming pool than at its surface.

  
```
 Pressure Variation Example:
 
 Imagine a container of water:
 
   Surface (low pressure)
    ~~~~~~~~~~~  p = p0
     |
     |  Increasing depth
     |  -> Increasing pressure
     V
    [ H2O H2O H2O H2O ]
    [ molecules closer ]
 
 The deeper you go, the more 
 fluid weight above you, and 
 thus higher pressure.
```

  
In a static fluid, the pressure variation with depth \(z\) (taking the vertical axis positive upward) can be described by the hydrostatic equation:

\[
\frac{dp}{dz} = -\rho g,
\]

where \(\rho\) is the fluid density and \(g\) is gravitational acceleration. This relationship shows that pressure increases as you move downward in a fluid under gravity.
