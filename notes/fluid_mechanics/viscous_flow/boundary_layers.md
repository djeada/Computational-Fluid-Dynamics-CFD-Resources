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

$$
\delta^* = \int_0^\delta \left(1 - \frac{u(y)}{U_\infty}\right) \, dy
$$

III. **$\theta$ (Momentum Thickness)**

Relates to the lost momentum flux due to the boundary layer.

$$
\theta = \int_0^\delta \frac{u(y)}{U_\infty}\left(1 - \frac{u(y)}{U_\infty}\right)\, dy
$$

Velocity Profile & Thicknesses

![boundary_layer_velocity_profile](../../../scripts/plots/boundary_layer_velocity_profile/boundary_layer_velocity_profile.png)

### Laminar vs. Turbulent Boundary Layers

![laminar_vs_turbulent_boundary_layer](https://github.com/user-attachments/assets/f3c4d10c-e5c9-46c6-a51e-654283177761)

> As Reynolds number (based on distance, $Re_x = \frac{U_\infty x}{\nu}$) grows, the laminar layer can become unstable and transition to turbulence.

#### Laminar Boundary Layer

- The laminar flow exhibits a *smooth, orderly* motion near the wall.
- The velocity profile is described by solutions such as the *Blasius solution* for a flat plate or other exact solutions for simple geometries.
- Shear stresses in laminar flow are driven solely by molecular viscosity.
- The boundary layer in laminar flow is typically thinner and experiences less mixing compared to turbulent layers.
- Under adverse pressure gradients, laminar flow is more prone to *boundary-layer separation*.

#### Example: Blasius (Flat Plate) Boundary Layer Growth

$$
\delta \sim \sqrt{\frac{\nu x}{U_\infty}}
$$

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

$$
u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} = \nu
\frac{\partial^2 u}{\partial y^2}
$$

with continuity:

$$
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0
$$

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

![flow_separation_boundary_layer](../../../scripts/plots/flow_separation_boundary_layer/flow_separation_boundary_layer.png)

**Turbulent boundary layers** can better resist separation than laminar ones because turbulence brings high-momentum fluid from outer layers near the wall.

### Related Scripts

- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Flow Separation in a Boundary Layer](../../../scripts/plots/flow_separation_boundary_layer/): draws a schematic of boundary-layer separation: an attached layer that thickens downstream, a separation point, and a recirculation region under the separated shear layer.
- [Generating Synthetic Data for Boundary Layer Simulation](../../../scripts/plots/boundary_layer_problem/): generates noisy synthetic velocity samples across a boundary layer from a simple square-root profile, saves them to a CSV file and plots them against the wall-normal distance.
- [Laminar vs. Turbulent Boundary Layer Profiles](../../../scripts/plots/laminar_vs_turbulent_boundary_layer/): plots normalised laminar and turbulent boundary-layer velocity profiles on the same axes to show how much fuller the turbulent profile is.
- [Mean Pressure Coefficient Along Vehicle Centreline](../../../scripts/plots/mean_pressure_coefficient/): plots a mock validation figure of mean pressure coefficient $C_P$ against streamwise position, comparing "experimental" data with a "CFD SRS" (scale-resolving simulation) curve that under-predicts a separation plateau.
- [Steady and Unsteady Pathlines Around a Cylinder with Vortex Shedding](../../../scripts/simulations/steady_and_unsteady_pathlines_with_vortex_shedding/): compares streamlines and particle pathlines for steady potential flow past a cylinder with circulation and for an unsteady version of the same flow with a kinematic vortex-shedding model.
- [Turbulent Boundary Layer Velocity Profile](../../../scripts/plots/boundary_layer_velocity_profile/): plots the one-seventh power-law velocity profile of a turbulent boundary layer in normalised form, $u/U_\infty$ against $y/\delta$.
- [Velocity Layers and Viscosity](../../../scripts/plots/velocity_layers_viscosity/): draws a schematic of three stacked fluid layers moving at different speeds to illustrate Newton's law of viscosity, $\tau = \mu\, du/dy$.

### Exercises

**Exercise 1.** Air ($\nu = 1.5 \times 10^{-5}$ m²/s) flows at $U_\infty = 10$ m/s over a smooth flat plate. Taking transition at $Re_x \approx 5 \times 10^5$, how far from the leading edge does the boundary layer stay laminar?

<details>
<summary>Answer</summary>

$x_{tr} = Re_{x,tr}\,\nu/U_\infty = 5 \times 10^5 \times 1.5 \times 10^{-5}/10 = 0.75$ m.

</details>

**Exercise 2.** For the same flow, use the Blasius results $\delta \approx 5.0\,x/\sqrt{Re_x}$, $\delta^* = 1.721\,x/\sqrt{Re_x}$ and $\theta = 0.664\,x/\sqrt{Re_x}$ to evaluate the three thicknesses and the shape factor $H = \delta^*/\theta$ at $x = 0.5$ m.

<details>
<summary>Answer</summary>

$Re_x = 10 \times 0.5/1.5 \times 10^{-5} = 3.33 \times 10^5$, so $\sqrt{Re_x} = 577$.

- $\delta = 5.0 \times 0.5/577 = 4.33$ mm. The more precise coefficient 4.91 gives 4.25 mm.
- $\delta^* = 1.49$ mm.
- $\theta = 0.575$ mm.
- $H = 1.721/0.664 = 2.59$.

The layer is only a few millimetres thick after half a metre, which justifies the thin-layer approximations.

</details>

**Exercise 3.** Approximate the laminar profile by the parabola $u/U_\infty = 2\eta - \eta^2$, with $\eta = y/\delta$, for $0 \le \eta \le 1$. Compute $\delta^*/\delta$, $\theta/\delta$ and $H$.

<details>
<summary>Answer</summary>

$$
\frac{\delta^*}{\delta} = \int_0^1 (1 - 2\eta + \eta^2)\, d\eta = \frac{1}{3}
$$

$$
\frac{\theta}{\delta} = \int_0^1 (2\eta - \eta^2)(1 - \eta)^2\, d\eta = \int_0^1
(2\eta - 5\eta^2 + 4\eta^3 - \eta^4)\, d\eta = 1 - \frac{5}{3} + 1 -
\frac{1}{5} = \frac{2}{15}
$$

$H = (1/3)/(2/15) = 2.5$, close to the Blasius value of 2.59.

</details>

**Exercise 4.** Combine the parabolic profile of Exercise 3 with the von Kármán momentum-integral equation for zero pressure gradient, $\tau_w = \rho U_\infty^2\, d\theta/dx$, to derive $\delta(x)$ and the skin-friction coefficient $C_f = \tau_w/(\frac{1}{2}\rho U_\infty^2)$. Compare with Blasius.

<details>
<summary>Answer</summary>

The wall shear is $\tau_w = \mu\,\partial u/\partial y|_0 = 2\mu U_\infty/\delta$, and $\theta = 2\delta/15$. Substituting,

$$
\rho U_\infty^2 \frac{2}{15} \frac{d\delta}{dx} = \frac{2\mu U_\infty}{\delta} \quad
\Rightarrow \quad \delta\, d\delta = \frac{15\nu}{U_\infty}dx \quad \Rightarrow \quad
\delta^2 = \frac{30\nu x}{U_\infty}
$$

so

$$
\frac{\delta}{x} = \frac{\sqrt{30}}{\sqrt{Re_x}} = \frac{5.48}{\sqrt{Re_x}}
$$

Then $C_f = 4\nu/(U_\infty\delta) = 0.730/\sqrt{Re_x}$. Blasius gives 5.0 (or 4.91) and 0.664. A simple assumed profile therefore captures the $x^{1/2}$ growth and gets the coefficients within about 10%.

</details>

### References

- H. Schlichting, K. Gersten, *Boundary-Layer Theory*, 9th ed., Springer, 2017.
- F. M. White, *Viscous Fluid Flow*, 3rd ed., McGraw-Hill, 2006.
- H. Blasius, "Grenzschichten in Flüssigkeiten mit kleiner Reibung", *Zeitschrift für Mathematik und Physik* 56, 1–37, 1908.
