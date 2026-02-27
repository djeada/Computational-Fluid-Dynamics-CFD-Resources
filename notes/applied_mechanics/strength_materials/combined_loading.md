# Combined Loading

In real engineering structures, members are rarely subjected to a single type of loading. Combined loading occurs when axial forces, shear forces, bending moments, and torsional moments act simultaneously on a structural member. Analyzing combined loading requires superposition of individual stress components and evaluation of the resulting stress state.

## Superposition of Stresses

### Principle

When a member is subjected to multiple loads, the resulting stress at any point is obtained by algebraically adding the stresses from each load acting independently, provided:

1. The material behaves linearly elastically
2. Deformations are small
3. Each load acts independently

### Normal Stress Components

At a given point, normal stresses from different sources are added directly:

$$\sigma_{total} = \sigma_{axial} + \sigma_{bending}$$

$$\sigma_{total} = \frac{P}{A} \pm \frac{My}{I}$$

The sign depends on whether the axial and bending stresses are tensile or compressive at the point of interest.

## Combined Axial and Bending

### Eccentric Axial Loading

When an axial load is applied with an eccentricity $e$ from the centroid, it produces both axial stress and bending stress:

$$\sigma = \frac{P}{A} + \frac{Pey}{I}$$

$$\sigma = \frac{P}{A}\left(1 + \frac{ecy}{I/A}\right) = \frac{P}{A}\left(1 + \frac{ey}{r^2}\right)$$

where $r = \sqrt{I/A}$ is the radius of gyration.

### Kern of a Section

The **kern** (or core) is the region within the cross-section where a compressive load can be applied without producing any tensile stress. For a rectangular section ($b \times h$):

$$e_y \leq \frac{h}{6}, \quad e_x \leq \frac{b}{6}$$

This defines the **middle-third rule** for rectangular sections — the load must fall within the middle third to avoid tension.

### Biaxial Bending

When bending occurs about both principal axes:

$$\sigma = \frac{P}{A} + \frac{M_y z}{I_y} + \frac{M_z y}{I_z}$$

where $M_y$ and $M_z$ are moments about the $y$- and $z$-axes respectively.

## Combined Bending and Torsion

### Stress State on a Shaft Element

A shaft subjected to simultaneous bending and torsion has both normal and shear stresses at the critical point (outer surface):

**Bending stress:**
$$\sigma_x = \frac{Mc}{I} = \frac{32M}{\pi d^3}$$

**Torsional shear stress:**
$$\tau_{xy} = \frac{Tc}{J} = \frac{16T}{\pi d^3}$$

### Principal Stresses

Using the stress transformation equations:

$$\sigma_{1,2} = \frac{\sigma_x}{2} \pm \sqrt{\left(\frac{\sigma_x}{2}\right)^2 + \tau_{xy}^2}$$

### Equivalent Stresses for Shaft Design

**Maximum shear stress theory (Tresca):**
$$\tau_{max} = \sqrt{\left(\frac{\sigma_x}{2}\right)^2 + \tau_{xy}^2} = \frac{16}{\pi d^3}\sqrt{M^2 + T^2}$$

**Distortion energy theory (von Mises):**
$$\sigma_{eq} = \sqrt{\sigma_x^2 + 3\tau_{xy}^2} = \frac{16}{\pi d^3}\sqrt{4M^2 + 3T^2}$$

These are used to determine the required shaft diameter for a given allowable stress.

## Pressure Vessels (Thin-Walled)

### Cylindrical Pressure Vessels

A thin-walled cylindrical pressure vessel (wall thickness $t \ll r$, typically $r/t > 10$) under internal pressure $p$ develops two principal stresses:

**Hoop (circumferential) stress:**
$$\sigma_1 = \frac{pr}{t}$$

**Longitudinal (axial) stress:**
$$\sigma_2 = \frac{pr}{2t}$$

The hoop stress is twice the longitudinal stress, which is why cylindrical pressure vessels tend to fail along a longitudinal seam.

### Spherical Pressure Vessels

For a thin-walled sphere under internal pressure:

$$\sigma_1 = \sigma_2 = \frac{pr}{2t}$$

The stress is uniform in all directions — spherical vessels are more efficient than cylindrical ones for a given volume.

### Maximum Shear Stress in a Cylindrical Vessel

**In-plane maximum shear stress:**
$$\tau_{max,in} = \frac{\sigma_1 - \sigma_2}{2} = \frac{pr}{4t}$$

**Absolute maximum shear stress** (considering the zero stress on the inner/outer surface):
$$\tau_{max,abs} = \frac{\sigma_1}{2} = \frac{pr}{2t}$$

## Mohr's Circle for Combined Stress

### Construction

Mohr's circle is a graphical method for stress transformation that provides principal stresses, maximum shear stress, and stresses on any inclined plane.

**Given:** $\sigma_x$, $\sigma_y$, and $\tau_{xy}$

**Center of the circle:**
$$C = \frac{\sigma_x + \sigma_y}{2}$$

**Radius of the circle:**
$$R = \sqrt{\left(\frac{\sigma_x - \sigma_y}{2}\right)^2 + \tau_{xy}^2}$$

**Principal stresses:**
$$\sigma_1 = C + R, \quad \sigma_2 = C - R$$

**Maximum in-plane shear stress:**
$$\tau_{max} = R$$

**Principal angle:**
$$\tan(2\theta_p) = \frac{2\tau_{xy}}{\sigma_x - \sigma_y}$$

### Interpretation

- Points on the circle represent stress states on different planes through the same point
- The top and bottom of the circle correspond to maximum shear stress planes
- The leftmost and rightmost points are the principal stress planes (where shear is zero)

## Example Problems

### Example 1: Eccentric Column Loading

A short concrete column ($300 \times 300$ mm) carries a compressive load of 500 kN applied with an eccentricity of 40 mm along one axis.

**Given:**
- $b = h = 300$ mm, $P = 500$ kN, $e = 40$ mm

**Find:** Maximum and minimum normal stress.

**Solution:**

$$A = 300 \times 300 = 90\,000 \text{ mm}^2$$

$$I = \frac{300 \times 300^3}{12} = 6.75 \times 10^8 \text{ mm}^4$$

$$\sigma = -\frac{P}{A} \pm \frac{Pec}{I}$$

$$\sigma = -\frac{500\,000}{90\,000} \pm \frac{500\,000 \times 40 \times 150}{6.75 \times 10^8}$$

$$\sigma = -5.56 \pm 4.44 \text{ MPa}$$

$$\sigma_{max} = -1.12 \text{ MPa (compression)}, \quad \sigma_{min} = -10.0 \text{ MPa (compression)}$$

Since both stresses are compressive, the load falls within the kern. Check: $e = 40$ mm $< h/6 = 50$ mm ✓

### Example 2: Shaft Under Combined Bending and Torsion

A solid steel shaft ($d = 50$ mm) is subjected to a bending moment $M = 1.2$ kN·m and a torque $T = 0.8$ kN·m.

**Given:**
- $d = 50$ mm, $M = 1.2$ kN·m, $T = 0.8$ kN·m

**Find:** Maximum shear stress and von Mises equivalent stress.

**Solution:**

**Bending stress:**
$$\sigma_x = \frac{32M}{\pi d^3} = \frac{32 \times 1200 \times 10^3}{\pi \times 50^3} = 97.8 \text{ MPa}$$

**Torsional shear stress:**
$$\tau_{xy} = \frac{16T}{\pi d^3} = \frac{16 \times 800 \times 10^3}{\pi \times 50^3} = 32.6 \text{ MPa}$$

**Maximum shear stress:**
$$\tau_{max} = \sqrt{\left(\frac{97.8}{2}\right)^2 + 32.6^2} = \sqrt{2392 + 1063} = 58.8 \text{ MPa}$$

**Von Mises equivalent stress:**
$$\sigma_{eq} = \sqrt{97.8^2 + 3 \times 32.6^2} = \sqrt{9565 + 3189} = 113.0 \text{ MPa}$$

### Example 3: Cylindrical Pressure Vessel with Axial Load

A thin-walled cylindrical tank ($r = 400$ mm, $t = 8$ mm) is under internal pressure $p = 2$ MPa and an external axial tensile force $F = 300$ kN.

**Given:**
- $r = 400$ mm, $t = 8$ mm, $p = 2$ MPa, $F = 300$ kN

**Find:** Principal stresses at the outer surface.

**Solution:**

**Hoop stress (from pressure only):**
$$\sigma_1 = \frac{pr}{t} = \frac{2 \times 400}{8} = 100 \text{ MPa}$$

**Longitudinal stress (pressure + axial force):**
$$\sigma_2 = \frac{pr}{2t} + \frac{F}{2\pi r t} = \frac{2 \times 400}{2 \times 8} + \frac{300\,000}{2\pi \times 400 \times 8}$$

$$\sigma_2 = 50 + 14.9 = 64.9 \text{ MPa}$$

The principal stresses are $\sigma_1 = 100$ MPa (hoop) and $\sigma_2 = 64.9$ MPa (longitudinal), with no shear on the principal planes.

## Failure Criteria Under Combined Loading

### Maximum Shear Stress Theory (Tresca)

$$\tau_{max} = \frac{\sigma_1 - \sigma_2}{2} \leq \frac{\sigma_y}{2}$$

Conservative for ductile materials; easy to apply.

### Distortion Energy Theory (von Mises)

$$\sigma_{eq} = \sqrt{\sigma_1^2 - \sigma_1\sigma_2 + \sigma_2^2} \leq \sigma_y$$

More accurate for ductile materials; widely used in practice and FEA.

## Applications

### Structural Engineering
- **Beam-columns**: members under simultaneous axial load and bending
- **Retaining walls**: bending from earth pressure plus axial weight
- **Eccentric connections**: combined loading at bolted and welded joints

### Mechanical Engineering
- **Rotating shafts**: bending from gear/pulley forces combined with transmitted torque
- **Pressure piping**: internal pressure combined with thermal and weight stresses
- **Crank mechanisms**: complex combined loading on connecting rods

### Aerospace Engineering
- **Fuselage panels**: pressurization (hoop and longitudinal stress) combined with flight loads
- **Landing gear struts**: combined axial, bending, and torsional loads during touchdown

## Practical Tips

- Identify the critical point on the cross-section where combined stresses are maximum
- For shafts, the critical point is typically the outer fiber on the tension side of bending
- Use Mohr's circle to visualize the stress state and find principal stresses quickly
- Always apply an appropriate failure criterion — von Mises for ductile materials, maximum normal stress for brittle
- In pressure vessels, the hoop stress governs — design the wall thickness based on $\sigma_1 = pr/t$

Combined loading analysis is essential for safe design of real-world structures where multiple load types act simultaneously.
