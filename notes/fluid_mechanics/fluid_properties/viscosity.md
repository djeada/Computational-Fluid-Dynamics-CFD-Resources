## Viscosity and Viscous Flow

Viscosity measures how strongly a fluid resists flow. Think of it as an “internal friction” arising from momentum transfer between adjacent layers moving at different speeds.

- Fluids like honey or molten lava flow slowly because they have strong intermolecular interactions.
- Fluids like water or air flow easily due to weaker shear resistance.

### Molecular Perspective

At a microscopic level, molecules in a faster-moving layer collide with those in a slower-moving layer, transferring momentum and effectively “pulling” each other. This momentum exchange shows up as viscous friction.

### Visualizing Viscosity

Below is a diagram showing fluid layers with different speeds. Viscosity acts to even out these speeds, resisting relative motion between layers.

![velocity_layers_viscosity](../../../scripts/plots/velocity_layers_viscosity/velocity_layers_viscosity.png)

- The velocity of the bottom layer can be nearly zero if there is a solid boundary (the **no-slip condition**).
- The gradient in speed across these layers is the **velocity gradient**, and viscosity resists differences in speed.

### Newtonian Fluids

For **Newtonian fluids**, shear stress $\tau$ is proportional to shear rate $\dot{\gamma}$:

```math
\tau = \mu \, \dot{\gamma}
```

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

- Newtonian: straight line (slope = $\mu$, constant).
- Shear-thinning: curve that starts steep and flattens out.
- Shear-thickening: curve that starts shallow and steepens.

### Non-Newtonian Fluids

For **Non-Newtonian fluids**, the effective viscosity changes depending on shear rate. Common examples:

I. **Shear-Thinning (Pseudoplastic)**:

- Viscosity **decreases** with increasing shear rate (e.g., paint, ketchup).\
  II. **Shear-Thickening (Dilatant)**:
- Viscosity **increases** with increasing shear rate (e.g., cornstarch in water).\
  III. **Bingham Plastic**:
- Needs a **yield stress** to flow (like toothpaste).

### Temperature Effects

- **Liquids**: as temperature **increases**, viscosity generally **decreases** (molecules slide past one another more easily).
- **Gases**: as temperature **increases**, viscosity generally **increases** (more frequent and energetic molecular collisions).

### Pressure Effects

- **Higher pressure** typically squeezes molecules closer, slightly increasing viscosity.
- However, for most common fluids (under moderate pressures), temperature changes often overshadow pressure effects.

### Laminar vs. Turbulent Flow

Viscosity helps determine whether flow is **laminar** (smooth layers) or **turbulent** (chaotic, swirling eddies). The **Reynolds number** ($Re$) is a dimensionless group used to predict flow regime:

```math
Re = \frac{\rho \, U \, L}{\mu}
```

- $\rho$ = fluid density
- $U$ = characteristic velocity
- $L$ = characteristic length scale (e.g., diameter of a pipe)
- $\mu$ = dynamic viscosity
- Low $Re$: laminar flow (viscous forces dominate).
- High $Re$: turbulent flow (inertial forces dominate).

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

- Boundary-layer thickness $\delta$: the distance from the wall to where the velocity is ~99% of the free-stream value.
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

II. Over a small distance (the boundary layer thickness), velocity ramps up to **$U_\infty$**.

III. The shape/thickness of this boundary layer has a big impact on drag and heat transfer.

### Related Scripts

- [Velocity Layers and Viscosity](../../../scripts/plots/velocity_layers_viscosity/): draws a schematic of three stacked fluid layers moving at different speeds to illustrate Newton's law of viscosity, $`\tau = \mu\, du/dy`$.
- [Wall Shear in Pipe Cross-Section](../../../scripts/plots/wall_shear_pipe_cross_section/): sketches fully developed laminar (Hagen-Poiseuille) flow in a circular pipe, with velocity arrows whose lengths follow the parabolic profile $u(r) = u_{max}(1 - (r/R)^2)$.

### Exercises

**Exercise 1.** Air at 20 °C has $\mu = 1.81 \times 10^{-5}$ Pa s and $\rho = 1.204$ kg/m³. Water has $\mu = 1.0 \times 10^{-3}$ Pa s and $\rho = 998$ kg/m³. Compute the kinematic viscosity $\nu = \mu/\rho$ of each. Which fluid is "more viscous" in each sense?

<details>
<summary>Answer</summary>

- Water: $\nu = 1.0 \times 10^{-3}/998 = 1.00 \times 10^{-6}$ m²/s.
- Air: $\nu = 1.81 \times 10^{-5}/1.204 = 1.50 \times 10^{-5}$ m²/s.

Water has the dynamic viscosity about 55 times larger. Air has the kinematic viscosity (momentum diffusivity) about 15 times larger, because its density is so low. At the same speed and size, air flow therefore has a smaller Reynolds number than water flow.

</details>

**Exercise 2.** A flat plate of area 0.1 m² slides at $U = 2$ m/s over a film of SAE 30 oil ($\mu \approx 0.29$ Pa s) that is $h = 0.5$ mm thick. Assuming a linear velocity profile, find the shear rate, the shear stress, and the force needed to move the plate.

<details>
<summary>Answer</summary>

- Shear rate: $\dot{\gamma} = U/h = 2/0.0005 = 4000$ s⁻¹.
- Shear stress: $\tau = \mu\dot{\gamma} = 0.29 \times 4000 = 1160$ Pa.
- Force: $F = \tau A = 1160 \times 0.1 = 116$ N.

</details>

**Exercise 3.** Fluid flows at $U = 0.08$ m/s through a pipe of diameter $L = 25$ mm. Compute $Re$ for (a) water ($\rho = 998$ kg/m³, $\mu = 1.0 \times 10^{-3}$ Pa s) and (b) glycerin ($\rho = 1260$ kg/m³, $\mu = 1.49$ Pa s), and classify each.

<details>
<summary>Answer</summary>

(a) $Re = 998 \times 0.08 \times 0.025/10^{-3} = 1996$. This is laminar, but close to the pipe transition range (about 2300).

(b) $Re = 1260 \times 0.08 \times 0.025/1.49 = 1.7$. This is deeply laminar and dominated by viscous forces.

</details>

**Exercise 4.** A shear-thinning paint follows the power law $\tau = K\dot{\gamma}^n$ with $K = 10$ Pa sⁿ and $n = 0.5$. Derive the apparent viscosity $\mu_{app} = \tau/\dot{\gamma}$ and evaluate it at $\dot{\gamma} = 1$ s⁻¹ (paint resting on a wall) and $\dot{\gamma} = 100$ s⁻¹ (paint under a brush).

<details>
<summary>Answer</summary>

$`\mu_{app} = K\dot{\gamma}^{n-1} = 10\,\dot{\gamma}^{-0.5}`$.

- At $\dot{\gamma} = 1$ s⁻¹: $\mu_{app} = 10$ Pa s.
- At $\dot{\gamma} = 100$ s⁻¹: $\mu_{app} = 1$ Pa s.

The paint is ten times thinner while being brushed, so it spreads easily, and thick at rest, so it does not run. That is exactly the behaviour wanted from a shear-thinning fluid.

</details>

**Exercise 5.** The viscosity of a gas rises with temperature. Sutherland's law, $\mu = \mu_0 (T/T_0)^{3/2}(T_0 + S)/(T + S)$, with $\mu_0 = 1.716 \times 10^{-5}$ Pa s, $T_0 = 273$ K and $S = 111$ K for air, captures this. Find $\mu$ at 373 K and the ratio $\mu(373)/\mu(273)$.

<details>
<summary>Answer</summary>

```math
\mu = 1.716 \times 10^{-5}\left(\frac{373}{273}\right)^{3/2}
\frac{273 + 111}{373 + 111} = 2.17 \times 10^{-5} \text{ Pa s}
```

The ratio is about 1.27, so heating air by 100 K raises its viscosity by roughly 27%. Liquids behave the opposite way: the viscosity of water falls by about a factor of 3.5 between 0 °C and 100 °C.

</details>

### References

- F. M. White, *Viscous Fluid Flow*, 3rd ed., McGraw-Hill, 2006.
- R. B. Bird, W. E. Stewart, E. N. Lightfoot, *Transport Phenomena*, 2nd ed., Wiley, 2002.
- R. P. Chhabra, J. F. Richardson, *Non-Newtonian Flow and Applied Rheology*, 2nd ed., Butterworth-Heinemann, 2008.
