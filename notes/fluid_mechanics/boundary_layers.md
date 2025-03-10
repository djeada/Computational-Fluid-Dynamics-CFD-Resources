## Boundary Layers

A **boundary layer** is a thin region adjacent to a solid surface where viscous effects are significant. Outside this layer, the flow is often approximated as inviscid (or nearly so), but near the boundary, the fluid velocity transitions from zero at the wall (the **no-slip condition**) to the free-stream velocity away from the wall.

* Ludwig Prandtl introduced the concept of boundary layers in 1904, revolutionizing fluid mechanics by explaining how viscosity, though small, remains critical in a thin layer near surfaces.

```
      Free Stream Velocity, U∞
            ---> ---> ---> ---> ---> 
       (Outer Flow Region: U ≈ U∞)

-------------------------------------------------
|                                               |
|             Boundary-Layer Region             |
|  (Velocity transitions from 0 at wall to U∞)  |
|                                               |
-------------------------------------------------
                 ↑
           Wall (Solid Surface)
      No-slip condition: v = 0 at the wall
```

### Formation and Features

I. **No-Slip Condition**  
   - At a solid boundary, the fluid velocity exactly matches the wall velocity (zero if the wall is stationary).  
   - This demands a large velocity gradient near the wall if free-stream velocity $U_\infty$ is significant.
II. **Thin Region**  
   - Because viscosity is typically small, the layer where viscous stresses matter is thin compared to the overall flow domain (e.g., a small fraction of an aircraft wing chord).
III. **Transition from Wall to Free Stream**  
   - Within the boundary layer, the velocity gradually increases from $0$ at the wall to $U_\infty$ in the outer region.  
   - This gradient sets up shear stresses that dominate flow friction (skin friction drag).

### Boundary-Layer Thickness Definitions

Because velocity changes continuously, there is no single abrupt boundary. Engineers define various **thicknesses** to quantify the boundary layer:

I. **$\delta$ (Boundary-Layer Thickness)**  
   - Commonly the distance from the wall to where the local velocity is about $0.99U_\infty$.  
II. **$\delta^*$ (Displacement Thickness)**  
   - A measure of how much the external inviscid flow is “displaced” by the presence of the boundary layer.  

   $$\delta^* = \int_0^\delta \left(1 - \frac{u(y)}{U_\infty}\right) \, dy.$$
III. **$\theta$ (Momentum Thickness)**  
   - Relates to the lost momentum flux due to the boundary layer.  

   $$\theta = \int_0^\delta \frac{u(y)}{U_\infty}\left(1 - \frac{u(y)}{U_\infty}\right)\, dy.$$

Velocity Profile & Thicknesses

![boundary_layer_velocity_profile](https://github.com/user-attachments/assets/0b3f51b4-7771-4d87-b59a-0bde6705b383)

### Laminar vs. Turbulent Boundary Layers

![laminar_vs_turbulent_boundary_layer](https://github.com/user-attachments/assets/f3c4d10c-e5c9-46c6-a51e-654283177761)


* As Reynolds number (based on distance, $\Re_x = \frac{U_\infty x}{\nu}$) grows, the laminar layer can become unstable and transition to turbulence.

#### Laminar Boundary Layer

- **Smooth, orderly** flow near the wall.  
- Velocity profile is described by solutions like the **Blasius solution** (flat plate) or other exact solutions for simple geometries.  
- Shear stresses are driven by molecular viscosity alone.  
- Typically thinner, with less mixing than turbulent layers.  
- More prone to **boundary-layer separation** under adverse pressure gradients.

#### Example: Blasius (Flat Plate) Boundary Layer Growth

$$\delta \sim \sqrt{\frac{\nu x}{U_\infty}}$$

- $\nu$ = kinematic viscosity,  
- $x$ = distance along the plate from the leading edge.

#### Turbulent Boundary Layer

- **Chaotic, swirling** flow near the wall.  
- High mixing leads to a **fuller velocity profile** (larger velocity near the wall vs. laminar).  
- Higher friction drag due to intense momentum transfer by turbulent eddies.  
- More resistant to separation because turbulent mixing can supply momentum from outer flow to near-wall regions.

### Boundary-Layer Equations

Prandtl devised simplified **boundary-layer equations** under assumptions of:

I. Small boundary-layer thickness $\delta$ compared to length scale $L$.

II. Predominantly one-directional flow (streamwise) within the layer.

III. Negligible pressure variation across the thin boundary layer (pressure taken from outer inviscid flow).

#### Form of the 2D Boundary-Layer Equations

For steady, incompressible flow over a flat plate (in x-direction), the boundary-layer momentum equation is often written as:

$$u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y}

= \nu \frac{\partial^2 u}{\partial y^2},$$
with continuity:

$$\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0.$$

- $u$ = streamwise velocity (dominant),  
- $v$ = normal velocity (much smaller),  
- $\nu$ = kinematic viscosity,  
- $y$ = normal distance from wall.

**Pressure gradient** $\frac{\partial p}{\partial x}$ is often specified by the external (inviscid) flow solution.

### Boundary-Layer Separation

When the pressure gradient becomes **adverse** (increasing pressure in the flow direction), the boundary layer can **separate** from the surface:

- Near the wall, fluid lacks enough kinetic energy to overcome the rising pressure.
- Flow **reverses** locally, forming a **separation bubble** or large separated region.
* 
- Dramatic increase in drag (pressure drag).  
- Loss of lift on airfoils.  
- Possible flow oscillations or unsteady vortex shedding.

Flow Separation

![flow_separation_boundary_layer](https://github.com/user-attachments/assets/aac53dde-9acf-4f5f-857d-00ef54ecbf6b)

**Turbulent boundary layers** can better resist separation than laminar ones because turbulence brings high-momentum fluid from outer layers near the wall.

