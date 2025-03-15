## Boundary Layers

A **boundary layer** is a thin region adjacent to a solid surface where viscous effects are significant. Outside this layer, the flow is often approximated as inviscid (or nearly so), but near the boundary, the fluid velocity transitions from zero at the wall (the **no-slip condition**) to the free-stream velocity away from the wall.

> Ludwig Prandtl introduced the concept of boundary layers in 1904, revolutionizing fluid mechanics by explaining how viscosity, though small, remains critical in a thin layer near surfaces.

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

Commonly the distance from the wall to where the local velocity is about $0.99U_\infty$.  

II. **$\delta^*$ (Displacement Thickness)**  

A measure of how much the external inviscid flow is “displaced” by the presence of the boundary layer.  

$$\delta^* = \int_0^\delta \left(1 - \frac{u(y)}{U_\infty}\right) \, dy.$$

III. **$\theta$ (Momentum Thickness)**  

Relates to the lost momentum flux due to the boundary layer.  

$$\theta = \int_0^\delta \frac{u(y)}{U_\infty}\left(1 - \frac{u(y)}{U_\infty}\right)\, dy.$$

Velocity Profile & Thicknesses

![boundary_layer_velocity_profile](https://github.com/user-attachments/assets/0b3f51b4-7771-4d87-b59a-0bde6705b383)

### Laminar vs. Turbulent Boundary Layers

![laminar_vs_turbulent_boundary_layer](https://github.com/user-attachments/assets/f3c4d10c-e5c9-46c6-a51e-654283177761)

> As Reynolds number (based on distance, $\Re_x = \frac{U_\infty x}{\nu}$) grows, the laminar layer can become unstable and transition to turbulence.

#### Laminar Boundary Layer

- The laminar flow exhibits a *smooth, orderly* motion near the wall.
- The velocity profile is described by solutions such as the *Blasius solution* for a flat plate or other exact solutions for simple geometries.
- Shear stresses in laminar flow are driven solely by molecular viscosity.
- The boundary layer in laminar flow is typically thinner and experiences less mixing compared to turbulent layers.
- Under adverse pressure gradients, laminar flow is more prone to *boundary-layer separation*.

#### Example: Blasius (Flat Plate) Boundary Layer Growth

$$\delta \sim \sqrt{\frac{\nu x}{U_\infty}}$$

- $\nu$ = kinematic viscosity,  
- $x$ = distance along the plate from the leading edge.

#### Turbulent Boundary Layer

- The turbulent flow near the wall is characterized by *chaotic, swirling* movement that defines its overall behavior.
- High mixing in turbulent conditions produces a *fuller velocity profile* with higher velocities near the wall compared to laminar flow.
- Intense momentum transfer by turbulent eddies results in increased *friction drag* on the surface.
- The effective turbulent mixing supplies momentum from the outer flow to near-wall regions, offering improved *resistance to separation*.

### Boundary-Layer Equations

Prandtl devised simplified **boundary-layer equations** under assumptions of:

- The boundary layer exhibits a *small boundary-layer thickness* $\delta$ when compared to the overall length scale $L$.
- Within the layer, the flow is predominantly in one direction, indicating a strong *streamwise* component.
- The pressure remains nearly constant across the thin boundary layer, reflecting a *negligible pressure variation* that is taken from the outer inviscid flow.

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

- Near the wall, the fluid lacks sufficient kinetic energy to overcome the increasing pressure, which leads to the *boundary layer* separating from the surface.
- The local flow may reverse its direction, forming a *separation bubble* that defines the beginning of a separated region.
- The separated flow contributes to an increase in pressure drag, resulting in a higher *pressure drag* on the surface.
- Airfoils experience a reduction in lift as the disrupted flow alters the pressure distribution and diminishes the overall *lift*.
- Unsteady flow behavior can occur, where the separated region develops a pattern of *vortex shedding* that produces flow oscillations.

Flow Separation

![flow_separation_boundary_layer](https://github.com/user-attachments/assets/aac53dde-9acf-4f5f-857d-00ef54ecbf6b)

**Turbulent boundary layers** can better resist separation than laminar ones because turbulence brings high-momentum fluid from outer layers near the wall.

