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

- Attractive forces between **like** molecules (fluid-fluid).
- Attractive forces between **unlike** molecules (fluid-solid).

Whether a liquid spreads or beads up on a surface depends on the balance between adhesion to the surface and the liquid’s own cohesive forces.

- Fluid “wets” the surface (spreads out).
- Fluid remains in a beaded shape, minimizing contact area.

### Capillarity and Meniscus Formation

When a **narrow tube** (capillary) is inserted into a liquid, the combination of **surface tension**, **cohesion**, and **adhesion** can cause fluid to **rise** or **fall** in the tube. This phenomenon is called **capillarity**.

#### Meniscus Shapes

![meniscus_behavior](https://github.com/user-attachments/assets/9d3eee1d-b9f8-4ed2-b7cb-e95a23bec953)

- In (a), water wets glass strongly -> meniscus curves upward.
- In (b), mercury does not wet glass well -> meniscus curves downward.

#### Capillary Rise Equation

For a liquid that wets the tube (like water in glass), the **capillary rise** $h$ can be approximated by:

$$h = \frac{2 \cdot \sigma \cdot \cos \theta}{\rho \cdot g \cdot r},$$

- surface tension
- contact angle (liquid-solid interface)
- liquid density
- gravitational acceleration
- capillary radius

- If $\theta < 90^\circ$, fluid rises (concave meniscus).  
- If $\theta > 90^\circ$, fluid is depressed (convex meniscus).

### Young-Laplace Equation

The **Young-Laplace equation** relates the pressure difference $\Delta p$ across a curved interface to its curvatures and surface tension:

$$\Delta p = \sigma \left( \frac{1}{R_1} + \frac{1}{R_2} \right).$$

- principal radii of curvature of the interface.

$$\Delta p = \frac{2 \, \sigma}{R}.$$

A smaller droplet (smaller $R$) has a **larger** internal pressure difference, which explains why tiny bubbles/droplets are more unstable and why they tend to coalesce into larger ones to reduce overall surface energy.

![pressure_difference_across_spherical_droplet](https://github.com/user-attachments/assets/706c8d64-e5c4-4108-8803-4e6bbbc63d4a)

Pressure inside the droplet is $p_{in} = p_{out} + \frac{2 \, \sigma}{R}$.

### Dimensionless Groups: Bond Number, Weber Number

While the **Reynolds number** is often used for inertial vs. viscous forces, **surface tension** phenomena have other dimensionless groups:

I. **Bond Number** $Bo$:

$$Bo = \frac{\rho \cdot g \cdot L^2}{\sigma}$$

- Compares gravitational forces to surface tension.  
- surface tension dominates (tiny droplets, strong curvature).
- gravity dominates (large droplets, flattened shapes).

II. **Weber Number** $We$:

$$We = \frac{\rho \cdot U^2 \cdot L}{\sigma}$$

Compares inertial forces to surface tension (important in droplet breakup or sprays).

### Practical Relevance

- Lung alveoli depend on surfactants to reduce surface tension and prevent collapse, as explained in *Biology*.
- Droplet formation in inkjet printing relies on a balance between inertial and surface tension forces, a process outlined in *Inkjet Printing*.
- Cleaning efficiency is improved when surface tension is lowered by agents discussed in *Detergents/Surfactants*.
- The manipulation of tiny droplets in lab-on-a-chip devices is achieved through precise control of surface tension, a method described in *Microfluidics*.
