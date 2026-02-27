# Torsion

Torsion refers to the twisting of a structural member when subjected to a torque (moment about the longitudinal axis). It is one of the fundamental loading modes in strength of materials, critical for the design of shafts, axles, and other rotating machinery components.

## Torsion of Circular Shafts

### Assumptions

The torsion formula for circular shafts is derived under the following assumptions:

1. The shaft is straight and has a circular cross-section
2. The material is homogeneous and linearly elastic
3. Plane cross-sections remain plane after twisting
4. Radial lines remain straight during deformation

### Shear Stress Distribution

The shear stress varies linearly from zero at the center to a maximum at the outer surface:

$$\tau = \frac{T\rho}{J}$$

where:
- $\tau$ = shear stress at radial distance $\rho$
- $T$ = applied internal torque
- $\rho$ = radial distance from the center
- $J$ = polar moment of inertia of the cross-section

**Maximum shear stress** (at the outer surface, $\rho = c$):

$$\tau_{max} = \frac{Tc}{J}$$

where $c$ is the outer radius of the shaft.

## Angle of Twist

The angle of twist for a shaft of constant cross-section under constant torque:

$$\phi = \frac{TL}{GJ}$$

where:
- $\phi$ = angle of twist (radians)
- $T$ = applied torque
- $L$ = length of the shaft
- $G$ = shear modulus of elasticity
- $J$ = polar moment of inertia

For a shaft with varying torque or cross-section:

$$\phi = \int_0^L \frac{T(x)}{G(x) J(x)} \, dx$$

For multiple segments:

$$\phi = \sum_{i=1}^{n} \frac{T_i L_i}{G_i J_i}$$

## Polar Moment of Inertia

### Solid Circular Shaft

$$J = \frac{\pi c^4}{2} = \frac{\pi d^4}{32}$$

where $c$ is the radius and $d$ is the diameter.

### Hollow Circular Shaft

$$J = \frac{\pi}{2}(c_o^4 - c_i^4) = \frac{\pi}{32}(d_o^4 - d_i^4)$$

where subscripts $o$ and $i$ denote outer and inner dimensions, respectively.

**Advantage of hollow shafts:** The material near the center of a solid shaft contributes little to torsional resistance. A hollow shaft provides a higher strength-to-weight ratio. For example, a hollow shaft with $d_i/d_o = 0.8$ has 59% of the polar moment of a solid shaft of the same outer diameter but only 36% of the weight.

## Power Transmission

The primary function of most shafts is to transmit power. The relationship between power, torque, and rotational speed is:

$$P = T\omega$$

where:
- $P$ = power (watts)
- $T$ = torque (N·m)
- $\omega$ = angular velocity (rad/s)

In terms of rotational speed in revolutions per minute (rpm):

$$P = \frac{2\pi n T}{60}$$

where $n$ is the speed in rpm.

**Design equation** — solving for the required shaft diameter:

$$T = \frac{60 P}{2\pi n}$$

Then, from the torsion formula with an allowable shear stress $\tau_{allow}$:

$$\frac{Tc}{J} \leq \tau_{allow} \implies \frac{T}{\frac{\pi d^3}{16}} \leq \tau_{allow}$$

$$d \geq \left(\frac{16T}{\pi \tau_{allow}}\right)^{1/3}$$

## Statically Indeterminate Shafts

When a shaft is fixed at both ends or supported by redundant constraints, equilibrium alone is insufficient to determine the internal torques.

### Solution Procedure

1. **Equilibrium**: Sum of torques equals zero
2. **Compatibility**: Total angle of twist between fixed supports is zero
3. **Torque–twist relation**: $\phi_i = T_i L_i / (G_i J_i)$
4. **Solve** the system of equations

**Example — shaft fixed at both ends with applied torque $T_0$ at an intermediate point:**

Equilibrium:
$$T_A + T_B = T_0$$

Compatibility (no net rotation):
$$\frac{T_A L_1}{GJ} - \frac{T_B L_2}{GJ} = 0$$

Solving:
$$T_A = T_0 \frac{L_2}{L_1 + L_2}, \quad T_B = T_0 \frac{L_1}{L_1 + L_2}$$

## Example Problems

### Example 1: Solid Shaft Design

A motor delivers 50 kW at 1500 rpm through a solid steel shaft. The allowable shear stress is 80 MPa.

**Given:**
- $P = 50$ kW, $n = 1500$ rpm
- $\tau_{allow} = 80$ MPa

**Find:** Required shaft diameter.

**Solution:**

**Torque:**
$$T = \frac{60P}{2\pi n} = \frac{60 \times 50\,000}{2\pi \times 1500} = 318.3 \text{ N·m}$$

**Required diameter:**
$$d \geq \left(\frac{16T}{\pi \tau_{allow}}\right)^{1/3} = \left(\frac{16 \times 318.3}{\pi \times 80 \times 10^6}\right)^{1/3}$$

$$d \geq \left(\frac{5093}{251.3 \times 10^6}\right)^{1/3} = (2.027 \times 10^{-5})^{1/3} = 0.0273 \text{ m} = 27.3 \text{ mm}$$

Select a standard shaft diameter of $d = 30$ mm.

### Example 2: Hollow vs. Solid Shaft Comparison

Compare a solid shaft of diameter 60 mm with a hollow shaft of outer diameter 70 mm and inner diameter 50 mm.

**Given:**
- Solid: $d = 60$ mm
- Hollow: $d_o = 70$ mm, $d_i = 50$ mm

**Find:** Ratio of maximum shear stress and weight.

**Solution:**

**Polar moments of inertia:**
$$J_{solid} = \frac{\pi (60)^4}{32} = 1.272 \times 10^6 \text{ mm}^4$$

$$J_{hollow} = \frac{\pi}{32}(70^4 - 50^4) = \frac{\pi}{32}(24.01 \times 10^6 - 6.25 \times 10^6) = 1.743 \times 10^6 \text{ mm}^4$$

**Stress ratio (for the same torque):**
$$\frac{\tau_{solid}}{\tau_{hollow}} = \frac{T \times 30 / J_{solid}}{T \times 35 / J_{hollow}} = \frac{30 / 1.272 \times 10^6}{35 / 1.743 \times 10^6} = \frac{23.58}{20.08} = 1.17$$

The solid shaft has 17% higher stress for the same torque.

**Weight ratio:**
$$\frac{A_{solid}}{A_{hollow}} = \frac{\pi(60)^2/4}{\pi(70^2 - 50^2)/4} = \frac{2827}{1885} = 1.50$$

The solid shaft weighs 50% more. The hollow shaft is both lighter and stronger.

### Example 3: Angle of Twist

A steel shaft ($G = 80$ GPa) has two segments: segment AB ($d = 40$ mm, $L = 0.6$ m, $T = 500$ N·m) and segment BC ($d = 30$ mm, $L = 0.4$ m, $T = 200$ N·m).

**Given:**
- Segment AB: $d_1 = 40$ mm, $L_1 = 0.6$ m, $T_1 = 500$ N·m
- Segment BC: $d_2 = 30$ mm, $L_2 = 0.4$ m, $T_2 = 200$ N·m
- $G = 80$ GPa

**Find:** Total angle of twist at C relative to A.

**Solution:**

$$J_1 = \frac{\pi (40)^4}{32} = 2.513 \times 10^5 \text{ mm}^4$$

$$J_2 = \frac{\pi (30)^4}{32} = 7.952 \times 10^4 \text{ mm}^4$$

$$\phi = \frac{T_1 L_1}{G J_1} + \frac{T_2 L_2}{G J_2}$$

$$\phi = \frac{500 \times 600}{80\,000 \times 2.513 \times 10^5} + \frac{200 \times 400}{80\,000 \times 7.952 \times 10^4}$$

$$\phi = 0.01493 + 0.01257 = 0.0275 \text{ rad} = 1.58°$$

## Torsion of Non-Circular Sections

For non-circular cross-sections, plane sections do **not** remain plane — warping occurs. Approximate solutions exist:

**Rectangular cross-section** ($a \times b$, $a > b$):
$$\tau_{max} = \frac{T}{\alpha a b^2}, \quad \phi = \frac{TL}{\beta a b^3 G}$$

where $\alpha$ and $\beta$ are coefficients depending on $a/b$ (tabulated values).

**Thin-walled closed sections** (Bredt–Batho formula):
$$\tau = \frac{T}{2 A_m t}$$

where $A_m$ is the area enclosed by the median line and $t$ is the wall thickness.

## Applications

### Automotive and Machinery
- **Drive shafts**: transmit engine torque to wheels
- **Crankshafts**: convert reciprocating motion with torsional loading
- **Gearbox shafts**: multiple torques at different gear locations

### Industrial Equipment
- **Pump and compressor shafts**: continuous power transmission
- **Mixer shafts**: torsion under variable load conditions
- **Drill strings**: extreme torsional loading in oil and gas

### Aerospace
- **Helicopter rotor shafts**: high-torque, fatigue-critical applications
- **Turbine shafts**: high-speed power transmission at elevated temperatures

## Practical Tips

- Hollow shafts offer a superior strength-to-weight ratio for most applications
- Always check both stress and angle of twist — a shaft may be strong enough but too flexible
- Keyways and splines introduce stress concentrations — apply $K_t$ factors in fatigue analysis
- For non-circular sections, use appropriate formulas — the circular shaft torsion formula does not apply
- Ensure proper alignment to avoid combined bending and torsion

Torsion analysis is essential for the safe and efficient design of rotating machinery and power transmission systems.
