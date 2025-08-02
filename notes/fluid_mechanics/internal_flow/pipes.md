## Pipe Flow

Pipes are ubiquitous in industrial and municipal infrastructure, serving to **transport fluids** (liquids or gases) efficiently. Whether delivering drinking water to homes, carrying chemical reagents in manufacturing plants, or pumping oil across continents, the physics of **flow in pipes** underpins cost-effectiveness, safety, and reliability.

- The flow regime is determined by calculating the Reynolds number, which indicates if the flow is **laminar** or exhibits turbulent behavior.
- Pressure losses are computed using formulas like the Darcy-Weisbach equation, where energy loss is mainly attributed to **friction**.
- Wall shear stress is estimated by measuring the force per unit area on the pipe wall, with the effects of **shear** forces informing material choices.
- System requirements are defined by evaluating the desired flow rate, available pressure, and pumping energy, while the **flow** rate is used to size the system components.

### Flow Rate and Velocity Profile

#### Flow Rate $(Q)$

The volumetric flow rate $Q$ is given by:

$$Q = A \, V_{\text{avg}},$$

where:

- $A$ = cross-sectional area of the pipe ($\pi D^2/4$ for a circular pipe of diameter $D$).  
- $V_{\text{avg}}$ = average fluid velocity through the cross section.

![flow_rate](https://github.com/user-attachments/assets/9c141451-1a94-4067-9a25-5f7cb0486c61)

In **practical design**, engineers pick a pipe diameter and desired flow velocity range to meet a target flow rate $Q$. For example, a chemical plant might specify $Q$ precisely to ensure reactants arrive at the correct ratio.

#### Velocity Profile

Because of **viscous effects** and the **no-slip condition** at the pipe wall, fluid velocity is **zero at the wall** and **maximum at the center**. This distribution depends heavily on the flow regime:

Smooth, orderly layers. Velocity profile is **parabolic**:

$$v(r) = v_{\text{max}} \left(1 - \left(\frac{r}{R}\right)^2\right),$$

where $r$ is the radial distance from the center and $R$ is the pipe radius.  

Chaotic eddies and mixing. The velocity profile is **flatter** in the core, with steep gradients near the wall.

Here is the plot comparing Laminar vs. Turbulent Flow Velocity Profiles:

![laminar_vs_turbulent_flow](https://github.com/user-attachments/assets/1af25fd7-75f3-4687-8ecb-2d24e05a7793)

- The velocity profile in laminar flow is parabolic, with maximum speed at the center and zero speed at the pipe wall due to the no-slip condition, resulting in a **parabolic** distribution.
- The velocity profile in turbulent flow is flatter, showing a more uniform core with sharp drops near the walls because of mixing effects, leading to a **flatter** profile.

### Flow Regimes and Reynolds Number

The **Reynolds number** $(Re)$ helps classify flow as laminar or turbulent:

$$Re = \frac{\rho \, V_{\text{avg}} \, D}{\mu},$$

- fluid density
- average velocity
- pipe diameter
- dynamic viscosity
- $Re < \approx 2{,}300$. Flow is smooth and orderly.
- $2{,}300 \lesssim Re \lesssim 4{,}000$.
- $Re > \approx 4{,}000$. Flow is chaotic with eddies.

**Turbulent flow** is common in large pipes or high-velocity scenarios, while **laminar flow** is typical in microfluidics or very viscous fluids moving slowly.

### Wall Shear Stress ($\tau_w$)

$$\tau_w = \mu \left.\frac{dv}{dr}\right|_{r=R} \quad (\text{laminar}),$$

but is more often related to the **pressure drop** via engineering correlations.

- Frictional losses increase when wall shear stress is high, resulting in a greater pressure drop that is notable in fluid systems.
- Material wear accelerates on surfaces experiencing high shear, particularly with abrasive or corrosive fluids, and the degradation is measurable over time.
- The boundary-layer thickness is affected by wall shear stress, which in turn influences convective heat transfer rates in thermal management, and this relationship is evident.

Here is the plot illustrating Wall Shear in Pipe Cross-Section:

![wall_shear_pipe_cross_section](https://github.com/user-attachments/assets/47c89e71-e6ab-4530-b00b-9b0db72fca68)

- The velocity vectors illustrate a parabolic velocity profile with maximum speed at the center ($r=0$) and a gradual decrease toward the pipe walls, resulting in a parabolic flow structure.  
- The no-slip condition is observed at the pipe wall where the fluid velocity drops to zero.  
- The high shear region is located near the wall where the velocity gradient is steep and the shear stress reaches its peak.  
- The wall shear is defined as the frictional force exerted by the fluid on the pipe walls, and it is measured to assess material wear and energy losses.

#### Pressure Drop and Energy Considerations

As fluid moves through the pipe, friction converts mechanical energy into heat, causing a **pressure drop** $\Delta P$. Engineers often use the **Darcy-Weisbach equation**:

$$\Delta P = f \frac{L}{D} \, \frac{\rho \, V_{\text{avg}}^2}{2},$$

where:

- pipe length
- pipe diameter
- fluid density
- average velocity
- friction factor (dimensionless), determined by flow regime and pipe roughness.

#### Friction Factor ($f$)

- $f = \frac{64}{Re}$.
- Empirical or semi-empirical correlations (e.g., Colebrook equation, Moody chart) account for **pipe roughness** ($\epsilon$).

Pipe Flow Schematic with Pressure Drop

```
  Inlet (higher pressure p_in)
    --->     ________
    ---> --->|        |
    --->     |  Flow  | --->   Outlet (lower pressure p_out)
    --->     |        |
             ‾‾‾‾‾‾‾‾
 
 Pressure drop Δp = p_in - p_out
 Over length L of pipe.
```

Minimizing $\Delta P$ reduces **pumping power** and operational costs. Strategies include selecting **larger diameters** (lower velocity, lower friction) or **smoother pipe materials**.

### Industrial Pipe Systems and Applications

I. **Oil & Gas Transmission** 

- **High pressures**, long distances.  
- Must control frictional losses, ensure pipeline integrity, handle multiphase flows, or high-temperature conditions.

II. **Municipal Water Supply**  

- Delivering water at acceptable pressure to residences.  
- Low friction losses for energy efficiency.  
- Typically handle moderate pressures, large diameters.

III. **Chemical & Process Industries**  

- Often require precise flow control to maintain reaction stoichiometry.  
- Material compatibility with corrosive or reactive fluids (e.g., stainless steel, lined pipes).  
- CIP (clean-in-place) for sanitary conditions in food/pharma.

IV. **Cooling Water Systems in Power Plants**  

- Large-diameter pipes for **massive** flow rates.  
- Minimal head loss is critical to avoid excessive pumping energy.  
- Sometimes use open channels vs. closed piping.

V. **Sanitary Piping (Food/Pharmaceutical)**  

- Smooth surfaces to prevent bacterial growth.  
- Must withstand cleaning/sterilization protocols without corroding or contaminating products.

### Pipe Material and Roughness

- Some pipe materials are strong and widely used, though they are prone to corrosion if not properly coated, which is expected in many installations.
- Materials that are corrosion-resistant are common in food and pharmaceutical systems despite their higher cost, and they are selected for their hygienic properties.
- Lightweight materials offer low cost and are effective under moderate pressure conditions, making them practical for certain applications.
- Pipes used in domestic plumbing are easy to form and offer some resistance to corrosion, which is beneficial for residential use.
- Roughness ($\epsilon$), indicated by epsilon, plays an important role in turbulent flow because it affects the friction factor, which is quantifiable in engineering analyses.
- Smooth pipes made of materials like plastic or polished metal reduce friction in turbulent flow, and they are considered efficient.
- Rough surfaces such as those found in cast iron pipes increase turbulence near the wall and raise friction levels, which is observable in flow measurements.

