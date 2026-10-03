## Surface Tension

Surface tension arises because molecules at a fluid interface experience an **imbalance** of forces. In the **bulk** of the fluid, each molecule is pulled equally in all directions by neighbors. At the **surface**, however, the molecule has fewer neighbors above (if we consider a liquid-air interface) and feels a net pull **inward**.

![surface_tension_at_molecular_level](https://github.com/user-attachments/assets/82ab4a99-e370-439d-8475-555fb6f50cd7)

- Molecules in bulk -> balanced forces (all directions).
- Molecules at surface -> net inward pull (fewer neighbors on top).
- Result -> Tendency to minimize surface area.

This **inward attraction** makes the surface behave like a stretched elastic membrane, seeking configurations of **minimum surface area** (e.g., a sphere for a free droplet).

### Defining Surface Tension

Surface tension $\sigma$ (or $\gamma$) has units of **force per unit length** (N/m) or equivalently **energy per unit area** (J/m$^2$). It can be interpreted in two equivalent ways:

I. **Force-based View**: The force required to create or stretch a line of unit length at the interface.

II. **Energy-based View**: The energy cost to increase the fluid’s surface area by one square meter.

#### Common Measurement Methods

- A wire frame with a movable strip is dipped in a liquid film. The force needed to pull the strip and enlarge the film area is measured, giving the surface tension.
- Observing the shape of a droplet suspended from a needle under gravity. Fitting the droplet profile to known theoretical curves yields $\sigma$.

### Everyday Phenomena

Surface tension explains why **raindrops** form nearly spherical shapes, why certain **insects** can walk on water without sinking, and why **bubbles** remain intact.

When external forces like gravity are small (e.g., very small droplets or microgravity conditions), the droplet becomes **almost perfectly spherical** due to surface tension.

### Interplay of Cohesion and Adhesion

- **Cohesion**: attractive forces between **like** molecules (fluid-fluid).
- **Adhesion**: attractive forces between **unlike** molecules (fluid-solid).

Whether a liquid spreads or beads up on a surface depends on the balance between adhesion to the surface and the liquid’s own cohesive forces.

- Adhesion dominates: the fluid “wets” the surface (spreads out).
- Cohesion dominates: the fluid remains in a beaded shape, minimizing contact area.

### Capillarity and Meniscus Formation

When a **narrow tube** (capillary) is inserted into a liquid, the combination of **surface tension**, **cohesion**, and **adhesion** can cause fluid to **rise** or **fall** in the tube. This phenomenon is called **capillarity**.

#### Meniscus Shapes

![meniscus_behavior](../../../scripts/plots/meniscus_behavior/meniscus_behavior.png)

- In (a), water wets glass strongly -> meniscus curves upward.
- In (b), mercury does not wet glass well -> meniscus curves downward.

#### Capillary Rise Equation

For a liquid that wets the tube (like water in glass), the **capillary rise** $h$ can be approximated by:

$$
h = \frac{2 \cdot \sigma \cdot \cos \theta}{\rho \cdot g \cdot r}
$$

- $\sigma$: surface tension

- $\theta$: contact angle (liquid-solid interface)

- $\rho$: liquid density

- $g$: gravitational acceleration

- $r$: capillary radius

- If $\theta < 90^\circ$, fluid rises (concave meniscus).

- If $\theta > 90^\circ$, fluid is depressed (convex meniscus).

### Young-Laplace Equation

The **Young-Laplace equation** relates the pressure difference $\Delta p$ across a curved interface to its curvatures and surface tension:

$$
\Delta p = \sigma \left(\frac{1}{R_1} + \frac{1}{R_2} \right)
$$

- $R_1$, $R_2$: principal radii of curvature of the interface.

For a spherical droplet of radius $R$ ($R_1 = R_2 = R$):

$$
\Delta p = \frac{2 \, \sigma}{R}
$$

A smaller droplet (smaller $R$) has a **larger** internal pressure difference, which explains why tiny bubbles/droplets are more unstable and why they tend to coalesce into larger ones to reduce overall surface energy.

![pressure_difference_across_spherical_droplet](https://github.com/user-attachments/assets/706c8d64-e5c4-4108-8803-4e6bbbc63d4a)

Pressure inside the droplet is $p_{in} = p_{out} + \frac{2 \, \sigma}{R}$.

### Dimensionless Groups: Bond Number, Weber Number

While the **Reynolds number** is often used for inertial vs. viscous forces, **surface tension** phenomena have other dimensionless groups:

I. **Bond Number** $Bo$:

$$
Bo = \frac{\rho \cdot g \cdot L^2}{\sigma}
$$

- Compares gravitational forces to surface tension.
- $Bo \ll 1$: surface tension dominates (tiny droplets, strong curvature).
- $Bo \gg 1$: gravity dominates (large droplets, flattened shapes).

II. **Weber Number** $We$:

$$
We = \frac{\rho \cdot U^2 \cdot L}{\sigma}
$$

Compares inertial forces to surface tension (important in droplet breakup or sprays).

### Practical Relevance

- Lung alveoli depend on surfactants to reduce surface tension and prevent collapse, as explained in *Biology*.
- Droplet formation in inkjet printing relies on a balance between inertial and surface tension forces, a process outlined in *Inkjet Printing*.
- Cleaning efficiency is improved when surface tension is lowered by agents discussed in *Detergents/Surfactants*.
- The manipulation of tiny droplets in lab-on-a-chip devices is achieved through precise control of surface tension, a method described in *Microfluidics*.

### Related Scripts

- [Meniscus Behavior](../../../scripts/plots/meniscus_behavior/): sketches the meniscus of water and of mercury in a glass tube, showing how wetting determines whether the free surface curves up or down at the wall.
- [Pressure Difference Across a Spherical Droplet](../../../scripts/plots/pressure_difference_across_spherical_droplet/): draws an annotated schematic of the Young-Laplace pressure jump across the surface of a spherical droplet.

### Exercises

**Exercise 1.** A clean glass capillary of radius $r = 0.5$ mm is dipped in water at 20 °C ($\sigma = 0.0728$ N/m, $\rho = 998$ kg/m³, contact angle $\theta \approx 0^\circ$). How high does the water rise?

<details>
<summary>Answer</summary>

```math
h = \frac{2\sigma\cos\theta}{\rho g r} = \frac{2 \times 0.0728 \times 1}{998 \times 9.81 \times 0.0005} = 0.0297 \text{ m}
```

The water rises about 29.7 mm. Halving the radius would double the rise.

</details>

**Exercise 2.** Derive $\Delta p = 2\sigma/R$ for a spherical droplet from an energy balance: the work done by the pressure difference in a small expansion $dR$ equals the increase in surface energy. Then evaluate $\Delta p$ for (a) a water droplet with $R = 1$ μm ($\sigma = 0.0728$ N/m) and (b) a soap bubble with $R = 2$ cm and $\sigma = 0.025$ N/m, remembering that a bubble film has two surfaces.

<details>
<summary>Answer</summary>

Pressure work is $\Delta p\, dV = \Delta p\, 4\pi R^2 dR$. The surface energy increase is $\sigma\, dA = \sigma\, 8\pi R\, dR$. Equating them gives $\Delta p = 2\sigma/R$.

(a) $\Delta p = 2(0.0728)/10^{-6} = 1.456 \times 10^5$ Pa, about 1.44 atm.

(b) Two surfaces double the surface energy, so $\Delta p = 4\sigma/R = 4(0.025)/0.02 = 5$ Pa.

The tiny droplet carries a pressure excess large enough to matter in cavitation and nucleation. The large bubble's excess is negligible.

</details>

**Exercise 3.** Mercury ($\sigma = 0.485$ N/m, $\rho = 13534$ kg/m³) meets glass at a contact angle of about $140^\circ$. Find the capillary change in level in a tube of radius $r = 1$ mm, and say whether the level rises or falls.

<details>
<summary>Answer</summary>

```math
h = \frac{2 \times 0.485 \times \cos 140^\circ}{13534 \times 9.81 \times 0.001} = -0.0056 \text{ m}
```

The negative sign means the level is depressed by about 5.6 mm, with a convex meniscus, as expected for $\theta > 90^\circ$.

</details>

**Exercise 4.** For water ($\sigma = 0.0728$ N/m, $\rho = 998$ kg/m³), compute the Bond number for drops of size $L = 1$ mm and $L = 1$ cm. Then find the capillary length $\ell_c = \sqrt{\sigma/(\rho g)}$, the size at which $Bo = 1$, and explain what it means for drop shape.

<details>
<summary>Answer</summary>

$Bo = \rho g L^2/\sigma$:

- $L = 1$ mm: $Bo = 998 \times 9.81 \times 10^{-6}/0.0728 = 0.134$. Surface tension dominates and the drop is nearly spherical.
- $L = 1$ cm: $Bo = 13.4$. Gravity dominates and a drop on a surface flattens into a puddle.

$\ell_c = \sqrt{0.0728/(998 \times 9.81)} = 2.73$ mm. Drops much smaller than about 2.7 mm are shaped by surface tension, and much larger ones by gravity. The capillary rise in Exercise 1 can also be written $h = 2\ell_c^2 \cos\theta / r$.

</details>

### References

- P.-G. de Gennes, F. Brochard-Wyart, D. Quéré, *Capillarity and Wetting Phenomena: Drops, Bubbles, Pearls, Waves*, Springer, 2004.
- A. W. Adamson, A. P. Gast, *Physical Chemistry of Surfaces*, 6th ed., Wiley, 1997.
- G. K. Batchelor, *An Introduction to Fluid Dynamics*, Cambridge University Press, 1967.
