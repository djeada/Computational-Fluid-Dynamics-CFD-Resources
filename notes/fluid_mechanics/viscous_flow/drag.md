## Understanding Drag

Drag refers to the resistive force that slows down objects as they move through a fluid, whether that fluid is air or water. It is often thought of as a kind of aerodynamic or hydrodynamic friction that opposes motion, making it more difficult to move quickly and efficiently. People may notice drag when they extend a hand out the window of a moving car and feel the force pushing backward, or when they try to run through waist-deep water and discover that moving forward demands a lot more effort.

```
 airflow direction
 -----> -----> -----> ----->

           +---------+
           |         |
           |  Block  |
           |         |
           +---------+
            <----- <-----
              drag force
```

The diagram above shows a simple block exposed to airflow. The arrows moving left to right represent the airflow, and the arrows behind the block pointing left represent the direction of the drag force. In this simplified view, the block pushes against the air, and the air pushes back, creating resistance.

### Causes of Drag

Objects moving through fluids encounter drag for several reasons. Form drag, sometimes called pressure drag, occurs due to the shape of the object and how the fluid flows around it. A blunt shape causes air to separate and form turbulent wakes, increasing the force that pushes backward. Skin friction drag emerges from the interaction between the object’s surface and the fluid molecules. Even a smooth object has microscopic imperfections that cause friction. In winged vehicles like airplanes, induced drag comes into play when creating lift. Generating lift leads to vortices at the wingtips, which in turn increase overall resistance. Combining these factors, every shape and surface feature influences how much drag an object will feel.

### Drag Equation

The drag equation for an object moving through a fluid (e.g., air or water) is:

$$
F = \frac{1}{2} \rho \, v^{2} \, C_{d} \, A
$$

where:

- $F$ = drag force $(\mathrm{N})$
- $\rho$ = fluid density $\bigl(\mathrm{kg/m^3}\bigr)$
- $v$ = velocity of the object relative to the fluid $(\mathrm{m/s})$
- $C_{d}$ = drag coefficient (dimensionless), which depends on the shape and how streamlined it is
- $A$ = cross-sectional area of the object perpendicular to the flow $\bigl(\mathrm{m^2}\bigr)$

#### Drag on a Car

Calculate the drag force $F$.

- Air density ($\rho$) = $1.225\,\mathrm{kg/m^3}$ (sea-level standard air)
- Velocity ($v$) = $30\,\mathrm{m/s}$ (about $108\,\mathrm{km/h}$)
- Drag coefficient ($C_d$) = $0.30$ (typical for a moderately aerodynamic car)
- Cross-sectional area ($A$) = $2.2\,\mathrm{m^2}$

I. **Square the velocity**:

$$
v^2 = 30^2 = 900 \,\mathrm{(m/s)}^2
$$

II. **Multiply by the fluid density and the 0.5 factor**:

$$
\frac{1}{2} \rho = 0.5 \times 1.225 = 0.6125\,\mathrm{kg/m^3}
$$

Then:

$$
0.6125 \times 900 = 551.25 \,\mathrm{(kg/m^3) \cdot (m/s)^2}
$$

III. **Include the drag coefficient**:

$$
551.25 \times 0.30 = 165.375
$$

IV. **Include the cross-sectional area**:

$$
165.375 \times 2.2 = 363.825 \,\mathrm{N}
$$

So, the drag force is approximately **$364\,\mathrm{N}$**.

### How to Decrease Drag

Engineers work tirelessly to reduce drag because even small gains in aerodynamic efficiency can translate into big improvements in energy consumption and speed potential. A well-designed racing car is often a great example, with a sleek body and a smooth underbelly that lets air flow gently around its surfaces, minimizing wake and turbulence. Designers use wind tunnels, computational fluid dynamics, and scale models to tweak shapes and surfaces, hunting for ways to lower the drag coefficient. Similar efforts apply to airplanes, where wings and fuselages are crafted to minimize both form and induced drag, thus improving fuel efficiency and allowing for faster, more controlled flight.

- Streamlining the design lowers the *drag coefficient* ($C_d$).
- Minimizing the exposed cross-section reduces the *frontal area* ($A$).
- Operating in a less dense medium decreases the *fluid density* ($\rho$).
- Slowing down diminishes the impact of dynamic forces linked to *velocity* ($v$).

### Comparing Drag in Air vs. Water

Now let’s see how drastically drag can change in a denser fluid, using a small spherical object as an example.

#### Drag in Air

- Sphere radius $r$ = $0.05\,\mathrm{m}$
- Cross-sectional area $A$ = $\pi r^2 = \pi \times (0.05)^2 \approx 0.00785\,\mathrm{m^2}$
- Velocity ($v$) = $15\,\mathrm{m/s}$
- Fluid density ($\rho$, air) = $1.225\,\mathrm{kg/m^3}$
- Drag coefficient ($C_d$) ≈ $0.47$ (typical for a smooth sphere)

I. **Square the velocity**:

$$
v^2 = 15^2 = 225 \,\mathrm{(m/s)}^2
$$

II. **Compute the half-density term**:

$$
\frac{1}{2} \rho = 0.5 \times 1.225 = 0.6125\,\mathrm{kg/m^3}
$$

III. **Multiply by $v^2$**:

$$
0.6125 \times 225 = 137.8125
$$

IV. **Include the drag coefficient**:

$$
137.8125 \times 0.47 \approx 64.772
$$

V. **Multiply by the cross-sectional area**:

$$
64.772 \times 0.00785 \approx 0.508\,\mathrm{N}
$$

So, **in air**, the drag force on this sphere is about **$0.51\,\mathrm{N}$**.

#### Drag in Water

Let's keep everything the same except for the fluid density. Water has a density of approximately $1000\,\mathrm{kg/m^3}$ (fresh water at around room temperature).

I. **Half-density term**:

$$
\frac{1}{2} \rho_{\text{water}} = 0.5 \times 1000 = 500
$$

II. **Multiply by $v^2$** ($v=15\,\mathrm{m/s}$):

$$
500 \times 225 = 112{,}500
$$

III. **Include the drag coefficient**:

$$
112{,}500 \times 0.47 = 52{,}875
$$

IV. **Multiply by the cross-sectional area ($0.00785\,\mathrm{m^2}$)**:

$$
52{,}875 \times 0.00785 \approx 415.07\,\mathrm{N}
$$

So, **in water**, the drag force on the same sphere (moving at the same speed) is about **$415\,\mathrm{N}$**—hundreds of times greater than in air, highlighting how a more dense fluid enormously increases drag.

### Real-world Examples

Observing how drag affects common activities makes the concept clearer and easier to imagine. For instance, professional cyclists intentionally position their bodies close to the handlebars and wear *aerodynamic helmets* to reduce drag, allowing them to pedal faster with considerably less effort. In another context, a large cargo ship moving through dense ocean water must overcome *immense resistance* created by drag, which necessitates powerful engines and substantial fuel consumption to maintain speed. Even in swimming, competitors carefully *streamline their bodies* and choose smooth, form-fitting swimsuits designed specifically to minimize drag, thereby enhancing their ability to move efficiently through the water.

```
   airflow direction
   -----> -----> -----> -----> ----->

       ______________
   --->|              \
   --->|   Aerodynamic \
   --->|     Design     \________
       |                /
   --->|______________/

   Reduced wake area = Lower drag
```

In the diagram above, an aerodynamic shape helps keep the airflow smoother and more attached, which reduces the size of the wake region behind it. The smaller and gentler the wake, the lower the drag. This design principle carries across cars, trains, aircraft, bicycles, and even buildings in windy conditions.

### Related Scripts

- [Drag Coefficient Prediction](../../../scripts/plots/drag_coefficient_prediction/): compares two synthetic drag-coefficient predictors with reference values in a predicted-vs-reference plot, adding a regression line and $R^2$ for each.
- [Eulerian Cylinder Flow](../../../scripts/simulations/eulerian_cylinder_flow/): simulates 2D incompressible, inviscid flow past a circular cylinder on a fixed Eulerian grid and renders a dye tracer in real time with Pygame.
- [Flow Separation in a Boundary Layer](../../../scripts/plots/flow_separation_boundary_layer/): draws a schematic of boundary-layer separation: an attached layer that thickens downstream, a separation point, and a recirculation region under the separated shear layer.
- [Laminar vs. Turbulent Boundary Layer Profiles](../../../scripts/plots/laminar_vs_turbulent_boundary_layer/): plots normalised laminar and turbulent boundary-layer velocity profiles on the same axes to show how much fuller the turbulent profile is.
- [Ship Hull in Water](../../../scripts/plots/ship_hull_in_water/): draws a side-view sketch of a ship hull sitting in a sinusoidal free-surface wave and annotates it with the Froude number $Fr = U/\sqrt{gL}$.
- [Turbulent Boundary Layer Velocity Profile](../../../scripts/plots/boundary_layer_velocity_profile/): plots the one-seventh power-law velocity profile of a turbulent boundary layer in normalised form, $u/U_\infty$ against $y/\delta$.

### Exercises

**Exercise 1.** Using the car example ($\rho = 1.225$ kg/m³, $C_d = 0.30$, $A = 2.2$ m²), find the power needed to overcome drag at 30 m/s and at 40 m/s.

<details>
<summary>Answer</summary>

$P = Fv = \frac{1}{2}\rho C_d A v^3$:

- At 30 m/s: $F = 363.8$ N and $P = 10.9$ kW.
- At 40 m/s: $F = 646.8$ N and $P = 25.9$ kW.

A 33% increase in speed raises drag by 78% and power by 137%, since power scales with $v^3$.

</details>

**Exercise 2.** A skydiver of mass 80 kg falls belly-down with $C_d A \approx 0.7$ m² ($C_d = 1.0$, $A = 0.7$ m²) in air with $\rho = 1.225$ kg/m³. Find the terminal velocity.

<details>
<summary>Answer</summary>

At terminal velocity the weight balances the drag, $mg = \frac{1}{2}\rho v_t^2 C_d A$, so

$$
v_t = \sqrt{\frac{2mg}{\rho C_d A}} = \sqrt{\frac{2 \times 80 \times 9.81}{1.225 \times 0.7}} = 42.8 \text{ m/s}
$$

That is about 154 km/h.

</details>

**Exercise 3.** The note's sphere examples use $C_d = 0.47$ in both air and water. Check the Reynolds numbers for $D = 0.1$ m and $v = 15$ m/s, with $\nu_{air} = 1.5 \times 10^{-5}$ m²/s and $\nu_{water} = 1.0 \times 10^{-6}$ m²/s. Is a constant $C_d$ justified?

<details>
<summary>Answer</summary>

- Air: $Re = 15 \times 0.1/1.5 \times 10^{-5} = 1.0 \times 10^5$. This is in the subcritical range, where $C_d \approx 0.47$ is reasonable for a smooth sphere.
- Water: $Re = 15 \times 0.1/10^{-6} = 1.5 \times 10^6$. This is above the drag crisis (around $3 \times 10^5$ for a smooth sphere). The boundary layer turns turbulent before separating, the wake narrows, and $C_d$ typically falls to roughly 0.1–0.2.

So the 415 N water estimate is probably too high by a factor of two or more. $C_d$ always has to be taken at the right $Re$.

</details>

**Exercise 4.** At $Re \ll 1$, the drag on a sphere is given by Stokes' law, $F = 3\pi\mu D v$. (a) Show that this corresponds to $C_d = 24/Re$. (b) Find the terminal velocity of a water droplet with $D = 50$ μm ($\rho_p = 998$ kg/m³) falling in air ($\rho = 1.2$ kg/m³, $\mu = 1.81 \times 10^{-5}$ Pa s), and check that $Re < 1$.

<details>
<summary>Answer</summary>

(a)

$$
C_d = \frac{3\pi\mu D v}{\frac{1}{2}\rho v^2 \frac{\pi D^2}{4}} = \frac{24\mu}{\rho v D} = \frac{24}{Re}
$$

(b) Balance weight minus buoyancy against drag: $(\rho_p - \rho)g\frac{\pi D^3}{6} = 3\pi\mu D v_t$. This gives

$$
v_t = \frac{(\rho_p - \rho)gD^2}{18\mu} = \frac{996.8 \times 9.81 \times (5 \times 10^{-5})^2}{18 \times 1.81 \times 10^{-5}} = 0.075 \text{ m/s}
$$

Check: $Re = 1.2 \times 0.075 \times 5 \times 10^{-5}/1.81 \times 10^{-5} = 0.25 < 1$, so Stokes' law applies.

</details>

### References

- S. F. Hoerner, *Fluid-Dynamic Drag*, published by the author, 1965.
- F. M. White, *Fluid Mechanics*, 8th ed., McGraw-Hill Education, 2016.
- R. Clift, J. R. Grace, M. E. Weber, *Bubbles, Drops, and Particles*, Academic Press, 1978.
- H. Schlichting, K. Gersten, *Boundary-Layer Theory*, 9th ed., Springer, 2017.
