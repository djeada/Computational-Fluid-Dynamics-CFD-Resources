## Hydrostatics

Hydrostatics deals with fluids at rest and helps explain how pressure and force distribute in still fluids. When there is no flow, no shear, and no net movement, the fluid settles into a configuration where the pressure at each point supports the weight of the fluid above it. This aspect of fluid mechanics is vital for understanding everyday phenomena, like why pressure increases with depth in a swimming pool or how atmospheric pressure changes with altitude. It also lays the groundwork for designing structures such as dams, submarines, and hydraulic systems, where resisting fluid forces is essential for safety and performance.
  
In a static fluid, there are no velocity fields to track and no acceleration of fluid parcels. Instead, the fluid is at equilibrium. This simplification means that the dominant force balance in hydrostatics often involves gravity acting downward and pressure gradients acting to resist that weight. The result is that pressure typically increases with depth. By understanding this pressure-depth relationship, one can predict buoyant forces, determine forces on submerged surfaces, and analyze how containers or tanks behave under static fluid loads.

  
```
 Visualizing Pressure in a Static Fluid:
 ---------------------------------------
 
   Free surface (e.g., water surface in a tank)
    ~~~~~~~~~~~~~ p = p_0 (atmospheric pressure)
     |
     | Increasing depth (z decreasing)
     V
    At depth h:
    p = p_0 + ρ g h
    
 The pressure at depth h is higher 
 than at the surface by an amount ρ g h.
```

  
## Pressure Variation with Depth

Hydrostatics simplifies to understanding how pressure changes with depth. Consider a fluid at rest under the influence of gravity, taking the vertical coordinate \(z\) positive upward. If the fluid is incompressible and has constant density \(\rho\), the pressure distribution can be derived from equilibrium conditions. At any point within the fluid:

\[
\frac{dp}{dz} = -\rho g,
\]

where \(g\) is the acceleration due to gravity. Integrating this equation from the free surface (where pressure is often known, such as atmospheric pressure \(p_0\)) down to a depth \(h\):

\[
p = p_0 + \rho g h.
\]

This result indicates that the pressure at depth \(h\) below the free surface is greater than surface pressure by the amount \(\rho g h\). For water at standard conditions, pressure increases roughly by one atmosphere for every 10 meters of depth. This relationship explains why divers feel greater pressure on their bodies as they go deeper and why submarine hulls must withstand large compressive forces.

  
## Forces on Submerged Surfaces

The pressure distribution in a static fluid also helps determine the force exerted on submerged surfaces. Because pressure acts perpendicular to any surface, the force on a flat plate submerged at some angle can be computed by integrating the pressure over the area. If the plate is horizontal and located at a certain depth, the pressure is uniform across it, making the force calculation straightforward. For vertical or inclined surfaces, pressure varies with depth, and the average pressure must be found to determine the resultant force.

  
```
 Force on a Submerged Surface:
 -----------------------------
 
 Consider a vertical plate submerged 
 in water. Pressure at top is p_top,
 pressure at bottom is p_bottom:
 
 p_top = p_0 + ρ g h_top
 p_bottom = p_0 + ρ g h_bottom
 
 Pressure increases linearly with depth:
 
     Higher depth (h_bottom)
     |        +---------+
     |        |         |
     |        |  Plate  |
     |        |         |
     |        +---------+
     | Lower depth (h_top)
 
 The resultant force acts at the center 
 of pressure, which is deeper than the 
 centroid because pressure grows with depth.
```

  
To find the force on a vertical submerged surface of uniform width \(b\) and extending from \(z = z_1\) to \(z = z_2\), one might integrate:

\[
F = \int_{A} p \, dA.
\]

If the surface is rectangular and vertical, and the fluid density and gravity are constant, the pressure distribution is linear in depth. For a plate starting at depth \(h_1\) and ending at depth \(h_2\), the force becomes:

\[
F = \rho g b \int_{h_1}^{h_2} h \, dh = \rho g b \frac{h_2^2 - h_1^2}{2}.
\]

The line of action of this resultant force, known as the center of pressure, is located below the centroid of the area because pressure increases with depth.

  
## Buoyancy and Archimedes’ Principle

Hydrostatics also introduces buoyancy, the net upward force experienced by an object submerged in a fluid. Archimedes’ principle states that the buoyant force on an object is equal to the weight of the fluid it displaces. If an object is submerged in a fluid, the pressure on its bottom is slightly higher than the pressure on its top, producing a net upward force. This explains why objects float or sink depending on whether their density is less than or greater than that of the fluid.

For a fully submerged object of volume \(V\):

\[
F_b = \rho_{\text{fluid}} g V.
\]

If the object’s weight is \(W = \rho_{\text{object}} g V\), and if \(\rho_{\text{object}} < \rho_{\text{fluid}}\), the buoyant force exceeds the object’s weight, causing it to rise or float. Conversely, if \(\rho_{\text{object}} > \rho_{\text{fluid}}\), the object sinks. For objects that exactly match the fluid’s density, they remain neutrally buoyant, neither rising nor sinking.

  
```
 Buoyancy:
 ---------
 
 Consider a cube submerged in water:
 The pressure underneath is slightly higher 
 than the pressure on top:
 
  Top surface at depth h:
    p_top = p_0 + ρ g h
  Bottom surface at depth h + Δh:
    p_bottom = p_0 + ρ g (h+Δh)
 
 Net upward force (buoyancy) = difference 
 in pressure * area = ρ g (Δh) A.
 If this equals the cube’s weight, it floats.
```

## Stability of Submerged and Floating Bodies

Hydrostatics is not only about calculating forces but also about assessing stability. When a body floats, its stability depends on how the buoyant force aligns with its center of gravity. If a small tilt causes the buoyant force to realign in a way that returns the body to its original position, the floating body is stable. If not, it might capsize. Designing stable ships, submarines, and other floating structures involves ensuring that their centers of buoyancy and gravity are properly arranged.

In many cases, stability can be analyzed by comparing the location of the center of gravity (G) and the center of buoyancy (B). For a floating object, the center of buoyancy moves as it tilts, and if this movement leads to a restoring moment, the craft remains stable. Otherwise, additional modifications to shape, ballast, or distributed mass might be necessary.
