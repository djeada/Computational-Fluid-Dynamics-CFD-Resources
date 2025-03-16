## Viscosity and Viscous Flow

Viscosity measures how strongly a fluid resists flow. Think of it as an “internal friction” arising from momentum transfer between adjacent layers moving at different speeds.

- Fluids like honey or molten lava flow slowly because they have strong intermolecular interactions.
- Fluids like water or air flow easily due to weaker shear resistance.

### Molecular Perspective

At a microscopic level, molecules in a faster-moving layer collide with those in a slower-moving layer, transferring momentum and effectively “pulling” each other. This momentum exchange shows up as viscous friction.

### Visualizing Viscosity

Below is a diagram showing fluid layers with different speeds. Viscosity acts to even out these speeds, resisting relative motion between layers.

![velocity_layers_viscosity](https://github.com/user-attachments/assets/0ac9ac84-a609-41c8-ba58-311b73f7795b)

- The velocity of the bottom layer can be nearly zero if there is a solid boundary (the **no-slip condition**).
- The gradient in speed across these layers is the **velocity gradient**, and viscosity resists differences in speed.

### Newtonian Fluids

For **Newtonian fluids**, shear stress $\tau$ is proportional to shear rate $\dot{\gamma}$:

$$\tau = \mu \, \dot{\gamma},$$

where $\mu$ is the **dynamic viscosity**, assumed constant under fixed temperature and pressure. Examples include water, air, many oils, and other “simple” fluids.

Below is a rough  representation comparing a **Newtonian** fluid curve (straight line) to a **shear-thinning** fluid curve (curve flattens with increased shear) and a **shear-thickening** fluid (curve steepens).

```
          shear stress (τ)
                  ^
                  |
   Shear-         |         Shear-Thickening
   Thinning       |               /
       (curved)   |    Newtonian / 
                  |           /
                  |         /
                  |       /
                  +-----------------> shear rate (γ̇)
```

- straight line (slope = µ, constant).
- curve that starts steep and flattens out.
- curve that starts shallow and steepens.

### Non-Newtonian Fluids

For **Non-Newtonian fluids**, the effective viscosity changes depending on shear rate. Common examples:

I. **Shear-Thinning (Pseudoplastic)**:
   - Viscosity **decreases** with increasing shear rate (e.g., paint, ketchup).  
II. **Shear-Thickening (Dilatant)**:
   - Viscosity **increases** with increasing shear rate (e.g., cornstarch in water).  
III. **Bingham Plastic**:
   - Needs a **yield stress** to flow (like toothpaste).

### Temperature Effects

- As temperature **increases**, viscosity generally **decreases** (molecules slide past one another more easily).
- As temperature **increases**, viscosity generally **increases** (more frequent and energetic molecular collisions).

### Pressure Effects

- **Higher pressure** typically squeezes molecules closer, slightly increasing viscosity.  
- However, for most common fluids (under moderate pressures), temperature changes often overshadow pressure effects.

### Laminar vs. Turbulent Flow

Viscosity helps determine whether flow is **laminar** (smooth layers) or **turbulent** (chaotic, swirling eddies). The **Reynolds number** ($Re$) is a dimensionless group used to predict flow regime:

$$Re = \frac{\rho \, U \, L}{\mu},$$

- $\rho$ = fluid density  
- $U$ = characteristic velocity  
- $L$ = characteristic length scale (e.g., diameter of a pipe)  
- $\mu$ = dynamic viscosity
- laminar flow (viscous forces dominate).
- turbulent flow (inertial forces dominate).

 Diagram for Flow Regimes

```
Low Re (Laminar)          High Re (Turbulent)
-----------               -------------------
1) Smooth, layer-like     1) Chaotic, swirling
   flow.                     eddies.
   
   --> --> --> -->           ~~~>>> ~~>>> ~> ~>
   --> --> --> -->           ->> ~~~~ >> ~~~ >> 
   --> --> --> -->           
   
2) Little mixing.         2) Rapid mixing and
   Viscosity critical.        momentum exchange.
```

### Boundary Layers and Viscous Effects

When a fluid encounters a solid boundary, the **no-slip condition** dictates that fluid directly in contact with the surface is at rest relative to that surface. This forces a transition region called the **boundary layer**, where velocity increases from near-zero at the wall to the free-stream velocity in the bulk flow.

#### Boundary Layer Basics
- The distance from the wall to where the velocity is ~99% of the free-stream value.
- **High Viscosity** $\rightarrow$ thicker boundary layer (slower development of velocity profile).
- **Low Viscosity** $\rightarrow$ thinner boundary layer (velocity transitions quickly).

 Boundary Layer Diagram

```
   Free-stream velocity (U∞)
        ---> ---> ---> ---> ---> 
        _________________________
        ^ Boundary layer region 
        |
Wall ->  |--- fluid at rest (no slip)
          Solid boundary (wall)
```

I. Velocity near the wall is forced to **zero** due to the no-slip condition.

II. Over a small distance (the boundary layer thickness), velocity ramps up to **U∞**.

III. The shape/thickness of this boundary layer has a big impact on drag and heat transfer.
