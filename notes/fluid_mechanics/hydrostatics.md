## Hydrostatics

**Hydrostatics** concerns itself with fluids at rest, focusing on how **pressure** and **forces** distribute in a fluid that is stationary (no flow, no shear). This foundational part of fluid mechanics explains everyday observations—like the fact that **pressure increases with depth** in a pool—and underpins the design of dams, submarines, and hydraulic systems.

### Equilibrium in a Static Fluid

When a fluid is at rest:

- There is **no velocity** field to track.
- All fluid parcels experience **no net acceleration**.  
- Gravitational forces are balanced by **pressure gradients** (and possibly other body forces, if present).

### Variation with Depth

Consider a fluid of **constant density** $\rho$ at rest under gravity $g$. Let $z$ be the vertical coordinate (positive upward). The fluid is taken to have a **free surface** at $z = 0$ with pressure $p_0$ (often atmospheric).

#### Governing Equation

From static equilibrium, the **hydrostatic equation** arises:

$$\frac{dp}{dz} = -\rho g.$$

Integrating from $z=0$ (where $p = p_0$) down to depth $z = -h$, we get:

$$p = p_0 + \rho g h.$$

Thus, at depth $h$ below the free surface, the pressure exceeds the surface pressure by $\rho g h$.

ASCII Diagram: Pressure in a Tank

```
Free surface (z=0)
  ~~~~~~~~~~~~~ p = p_0
       |
       |  (increasing depth -> h)
       V
  p = p_0 + ρ g h
```

- As depth **increases**, pressure **increases** linearly.
* Each **10 m** depth of water adds roughly **1 atmosphere** of pressure ($\approx 101,325 \text{ Pa}$).

### Forces on Submerged Surfaces

When a surface (like a dam wall or plate) is submerged, the fluid pressure **pushes** on it. Because **pressure acts normal** to surfaces in static fluids, we sum or integrate this pressure over the entire area to find the total force.

#### Vertical or Horizontal Plates


The pressure is the **same** across it (assuming negligible fluid density changes), simplifying force calculations to $F = p \times A$.


Pressure **varies with depth**, so the force must be found via integration:

$$F = \int_{A} p \, dA.$$

#### Example: Vertical Rectangular Plate

```
Water
~~~~~~ free surface
 | 
 | depth h1
 | ------ top of plate
 | |    |
 | |    |
 | ------ bottom of plate
 | depth h2
 V
```

- Width of plate = $b$ (into the page).  
- Extends from depth $h_1$ to $h_2$.  
- Pressure at any depth $h$ = $p(h) = p_0 + \rho g h$ 

$$dF = (p_0 + \rho g h) \cdot b dh$$

$$F = \int_{h_1}^{h_2} \rho g h \cdot b  dh$$

$$F = \rho g b \left[\frac{h^2}{2}\right]_{h_1}^{h_2}$$

$$F = \rho g b \frac{(h_2^2 - h_1^2)}{2}$$

#### Center of Pressure

Since the fluid pressure **increases with depth**, the resultant force is not at the geometric center of the plate, but at a point **deeper**, known as the **center of pressure**. Locating this point requires moment balance about a reference axis.

### Buoyancy and Archimedes’ Principle

**Buoyancy** is the net **upward** force a fluid exerts on a submerged (or partially submerged) object, arising because **pressure at the bottom** of the object is higher than **pressure at the top**.

#### Archimedes’ Principle

> *The buoyant force on a body is equal to the weight of the fluid it displaces.*

$$F_b = \rho_{\text{fluid}} g V$$

- Compare with the object’s weight $W = \rho_{\text{object}} \, g \, V$.  
- If $\rho_{\text{object}} < \rho_{\text{fluid}}$, it **floats**.  
- If $\rho_{\text{object}} > \rho_{\text{fluid}}$, it **sinks**.  
- If densities match, it is **neutrally buoyant**.

ASCII Diagram: Buoyancy

```
Object submerged
  +---------+
  |         |
 p_top    p_bottom
  |         |
h_top     h_bottom

Net upward force = (p_bottom - p_top)*Area
              = ρ_fluid * g * V
```

### Stability of Floating Bodies

Beyond buoyancy, **stability** addresses whether a floating body will **return** to equilibrium when tilted or disturbed.

- Where an object’s mass is concentrated.
- The centroid of the displaced fluid volume.

When the body tilts, **B** may shift. If **B** moves in such a way that a **restoring moment** forms (i.e., tries to push the body upright), the body is stable.

##### Metacentric Height

For many ship-like objects, we analyze stability via the **metacentric height (GM)**:

- A large positive $GM$ implies strong stability.  
- A small or negative $GM$ means the object can easily tip or capsize.

### Hydrostatics Applications

I. **Dams & Retaining Walls**  

- Must handle large lateral forces from water.  
- Structural design relies on the integrated force distribution and center of pressure.

II. **Submarines & ROVs**  

- Operate by adjusting **buoyancy** to dive or surface.  
- Hulls must withstand high external pressures at depth.

III. **Ships & Floating Vessels**  

- Must maintain suitable **stability** and **draft**.  
- Designers ensure that under loading conditions, the vessel floats safely without capsizing.

IV. **Hydraulic Systems**  

- Static fluid columns transmit force (e.g., car brakes, lifts).  
- Pressure differences $\Delta p = \rho g \Delta h$ are used to create mechanical advantages.
  
