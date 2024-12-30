# 1. Introduction to Boundary Layers

A **boundary layer** is a thin region adjacent to a solid surface where viscous effects are significant. Outside this layer, the flow is often approximated as inviscid (or nearly so), but near the boundary, the fluid velocity transitions from zero at the wall (the **no-slip condition**) to the free-stream velocity away from the wall.

* Ludwig Prandtl introduced the concept of boundary layers in 1904, revolutionizing fluid mechanics by explaining how viscosity, though small, remains critical in a thin layer near surfaces.

## 2. Formation and Features

I. **No-Slip Condition**  
   - At a solid boundary, the fluid velocity exactly matches the wall velocity (zero if the wall is stationary).  
   - This demands a large velocity gradient near the wall if free-stream velocity $U_\infty$ is significant.
II. **Thin Region**  
   - Because viscosity is typically small, the layer where viscous stresses matter is thin compared to the overall flow domain (e.g., a small fraction of an aircraft wing chord).
III. **Transition from Wall to Free Stream**  
   - Within the boundary layer, the velocity gradually increases from $0$ at the wall to $U_\infty$ in the outer region.  
   - This gradient sets up shear stresses that dominate flow friction (skin friction drag).

### ASCII Diagram: Boundary Layer Concept

```
        Free stream velocity U∞
         ---> ---> ---> ---> --->  (outer flow region)
            ______________________
            ^ boundary-layer region
            | velocity transitions
Wall (solid) | from 0 to U∞
     no-slip: v=0 at wall
```

## 3. Boundary-Layer Thickness Definitions

Because velocity changes continuously, there is no single abrupt boundary. Engineers define various **thicknesses** to quantify the boundary layer:

I. **$\delta$ (Boundary-Layer Thickness)**  
   - Commonly the distance from the wall to where the local velocity is about $0.99U_\infty$.  
II. **$\delta^*$ (Displacement Thickness)**  
   - A measure of how much the external inviscid flow is “displaced” by the presence of the boundary layer.  

   $$\delta^* = \int_0^\delta \left(1 - \frac{u(y)}{U_\infty}\right) \, dy.$$
III. **$\theta$ (Momentum Thickness)**  
   - Relates to the lost momentum flux due to the boundary layer.  

   $$\theta = \int_0^\delta \frac{u(y)}{U_\infty}\left(1 - \frac{u(y)}{U_\infty}\right)\, dy.$$

### ASCII Diagram: Velocity Profile & Thicknesses

```
   Velocity profile u(y)
     ^
     |  u = U∞  (outer region)
     |    \  
     |     \  boundary layer
     |      \
     |       \
     |--------+----> y = δ (approx. where u ~ 0.99 U∞)
     |
     +---------------------> wall (y=0, u=0)
```

## 4. Laminar vs. Turbulent Boundary Layers

### 4.1 Laminar Boundary Layer

- **Smooth, orderly** flow near the wall.  
- Velocity profile is described by solutions like the **Blasius solution** (flat plate) or other exact solutions for simple geometries.  
- Shear stresses are driven by molecular viscosity alone.  
- Typically thinner, with less mixing than turbulent layers.  
- More prone to **boundary-layer separation** under adverse pressure gradients.

#### Example: Blasius (Flat Plate) Boundary Layer Growth

$$\delta \sim \sqrt{\frac{\nu x}{U_\infty}},$$
- $\nu$ = kinematic viscosity,  
- $x$ = distance along the plate from the leading edge.

### 4.2 Turbulent Boundary Layer

- **Chaotic, swirling** flow near the wall.  
- High mixing leads to a **fuller velocity profile** (larger velocity near the wall vs. laminar).  
- Higher friction drag due to intense momentum transfer by turbulent eddies.  
- More resistant to separation because turbulent mixing can supply momentum from outer flow to near-wall regions.

#### ASCII Diagram: Laminar vs. Turbulent Profiles

```
 Laminar BL:           Turbulent BL:
   u/U∞                u/U∞
     ^                   ^
 1.0 |                   |1.0
     |        laminar    |    turbulent
     |         profile   |      profile (fuller)
     |            \      |       __
     |             \     |      /  \
     |              \    |____ /    \
     +-------------------> y   +------------------->
      (thin) BL                (thicker but more mixing)
```

* As Reynolds number (based on distance, $\Re_x = \frac{U_\infty x}{\nu}$) grows, the laminar layer can become unstable and transition to turbulence.

## 5. Boundary-Layer Equations

Prandtl devised simplified **boundary-layer equations** under assumptions of:

I. Small boundary-layer thickness $\delta$ compared to length scale $L$.

II. Predominantly one-directional flow (streamwise) within the layer.

III. Negligible pressure variation across the thin boundary layer (pressure taken from outer inviscid flow).

### 5.1 Form of the 2D Boundary-Layer Equations

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

## 6. Boundary-Layer Separation

When the pressure gradient becomes **adverse** (increasing pressure in the flow direction), the boundary layer can **separate** from the surface:

- Near the wall, fluid lacks enough kinetic energy to overcome the rising pressure.
- Flow **reverses** locally, forming a **separation bubble** or large separated region.
* 
- Dramatic increase in drag (pressure drag).  
- Loss of lift on airfoils.  
- Possible flow oscillations or unsteady vortex shedding.

### ASCII Diagram: Flow Separation

```
 Free stream
   ---> --->  (adverse pressure gradient)
         ~~~~~
        /    (attached BL)
  Wall  / 
  -----/--------------->   Boundary layer
       \               \
        \   separated   \  Flow recirculation
         \---- region----\
```

**Turbulent boundary layers** can better resist separation than laminar ones because turbulence brings high-momentum fluid from outer layers near the wall.

