# Rotating Machinery

Rotating machinery encompasses systems with components that spin about an axis, including shafts, flywheels, turbines, engines, and compressors. The design and analysis of these systems requires understanding shaft mechanics, rotordynamics, balancing, and energy storage principles.

## Shaft Design

Shafts are the primary rotating elements that transmit torque and support loads. Proper shaft design ensures adequate strength, acceptable deflection, and avoidance of critical speeds.

### Stress Analysis

#### Combined Loading

Shafts typically experience combined bending and torsion. The bending stress and shear stress are:

$$\sigma_b = \frac{32M}{\pi d^3}, \quad \tau = \frac{16T}{\pi d^3}$$

where $M$ is the bending moment, $T$ is the torque, and $d$ is the shaft diameter.

#### Maximum Shear Stress Theory

$$\tau_{max} = \frac{1}{2}\sqrt{\sigma_b^2 + 4\tau^2} = \frac{16}{\pi d^3}\sqrt{M^2 + T^2}$$

#### Distortion Energy Theory (von Mises)

$$\sigma_{eq} = \sqrt{\sigma_b^2 + 3\tau^2} = \frac{16}{\pi d^3}\sqrt{4M^2 + 3T^2}$$

### ASME Shaft Design Equation

For fluctuating loads with fatigue considerations:

$$d^3 = \frac{16}{\pi}\sqrt{\left(\frac{K_b M}{S_e}\right)^2 + \frac{3}{4}\left(\frac{K_t T}{S_y}\right)^2}$$

where $K_b$ and $K_t$ are fatigue stress concentration factors, $S_e$ is the endurance limit, and $S_y$ is the yield strength.

### Shaft Deflection

Excessive deflection can cause gear misalignment and bearing problems. For a simply supported shaft with a central load $F$:

$$\delta_{max} = \frac{FL^3}{48EI}$$

The slope at the bearings:

$$\theta = \frac{FL^2}{16EI}$$

Recommended limits:
- **Gear shafts**: Slope at gears $< 0.0005$ rad
- **General machinery**: Deflection $< 0.001L$

## Balancing of Rotating Masses

Unbalanced rotating masses generate centrifugal forces that cause vibration, noise, bearing wear, and structural fatigue. Balancing eliminates or minimizes these forces.

### Static Balancing (Single Plane)

For $n$ masses in a single plane rotating at angular velocity $\omega$:

$$\sum_{i=1}^{n} m_i r_i \cos\theta_i = 0$$
$$\sum_{i=1}^{n} m_i r_i \sin\theta_i = 0$$

The balancing mass-radius product is:

$$m_b r_b = \sqrt{\left(\sum m_i r_i \cos\theta_i\right)^2 + \left(\sum m_i r_i \sin\theta_i\right)^2}$$

placed at angle:

$$\theta_b = \pi + \arctan\frac{\sum m_i r_i \sin\theta_i}{\sum m_i r_i \cos\theta_i}$$

### Dynamic Balancing (Multi-Plane)

When masses are distributed along the shaft axis, both force and moment balance are required. Taking moments about plane A:

**Force balance:**
$$\sum m_i r_i e^{j\theta_i} + m_A r_A e^{j\theta_A} + m_B r_B e^{j\theta_B} = 0$$

**Moment balance about plane A:**
$$\sum m_i r_i l_i e^{j\theta_i} + m_B r_B L_{AB} e^{j\theta_B} = 0$$

where $l_i$ is the axial distance from plane A to mass $i$ and $L_{AB}$ is the distance between correction planes.

## Whirling of Shafts

A shaft rotating near its natural frequency of lateral vibration exhibits large amplitude oscillations called **whirling**. The speed at which this occurs is the **critical speed**.

### Single Mass on Shaft (Dunkerley's Model)

For a single disk of mass $m$ at the center of a simply supported shaft:

$$\omega_c = \sqrt{\frac{k}{m}} = \sqrt{\frac{48EI}{mL^3}}$$

The critical speed in rpm:

$$N_c = \frac{60}{2\pi}\omega_c$$

### Dunkerley's Method (Multiple Masses)

For a shaft carrying several masses, Dunkerley's method provides a lower bound estimate:

$$\frac{1}{\omega_c^2} \approx \frac{1}{\omega_1^2} + \frac{1}{\omega_2^2} + \cdots + \frac{1}{\omega_n^2} + \frac{1}{\omega_s^2}$$

where $\omega_i$ is the critical speed considering only mass $i$, and $\omega_s$ accounts for the shaft's distributed mass.

### Rayleigh's Method

Rayleigh's method provides an upper bound estimate by equating maximum kinetic and potential energies:

$$\omega_c^2 = \frac{g \sum m_i \delta_i}{\sum m_i \delta_i^2}$$

where $\delta_i$ is the static deflection at mass $i$ due to all masses acting under gravity. The true critical speed lies between the Dunkerley and Rayleigh estimates.

### Operating Recommendations
- **Rigid rotors**: Operate below 0.7$\omega_c$
- **Flexible rotors**: Operate above 1.4$\omega_c$ with rapid passage through critical speed during run-up

## Flywheels

Flywheels store rotational kinetic energy to smooth out speed fluctuations in machines with intermittent loading or power delivery.

### Energy Storage

$$E = \frac{1}{2}I\omega^2$$

where $I$ is the mass moment of inertia and $\omega$ is the angular velocity.

### Coefficient of Fluctuation

The coefficient of fluctuation measures speed variation:

$$C_f = \frac{\omega_{max} - \omega_{min}}{\omega_{avg}}$$

Typical values:
- **Engines**: $C_f = 0.02$–$0.05$
- **Machine tools**: $C_f = 0.02$
- **Punch presses**: $C_f = 0.10$–$0.20$

### Required Flywheel Inertia

For a given energy fluctuation $\Delta E$ during one cycle:

$$I = \frac{\Delta E}{C_f \cdot \omega_{avg}^2}$$

### Flywheel Stress (Solid Disk)

Maximum stress at the center of a rotating solid disk:

$$\sigma_{max} = \frac{3 + \nu}{8}\rho\omega^2 r^2$$

where $\nu$ is Poisson's ratio, $\rho$ is the density, and $r$ is the outer radius.

## Governors

Governors regulate the speed of prime movers (engines, turbines) by controlling fuel or steam supply in response to load changes.

### Sensitivity

$$\text{Sensitivity} = \frac{2(\omega_{max} - \omega_{min})}{\omega_{max} + \omega_{min}}$$

### Watt Governor (Centrifugal Type)

The height of a simple Watt governor:

$$h = \frac{g}{\omega^2}$$

As speed increases, the arms rise, reducing fuel supply. The equilibrium speed is independent of ball mass but depends only on height.

### Porter Governor

Adds a central dead weight $M$ for improved sensitivity:

$$\omega^2 = \frac{g}{h}\left(1 + \frac{M}{m}\right)$$

where $m$ is the mass of each rotating ball.

## Worked Examples

### Example 1: Shaft Diameter Design

**Given:** A shaft transmits 50 kW at 600 rpm. The maximum bending moment is 800 N·m. Material yield strength is 300 MPa, endurance limit is 150 MPa. Use a safety factor of 2.

**Find:** Minimum shaft diameter using the distortion energy theory.

**Solution:**

Torque:
$$T = \frac{P}{\omega} = \frac{50000}{2\pi \times 600/60} = 795.8 \text{ N·m}$$

Using the ASME equation with $K_b = K_t = 1$ (no stress concentrations):

$$d^3 = \frac{16}{\pi}\sqrt{\left(\frac{800}{150 \times 10^6 / 2}\right)^2 + \frac{3}{4}\left(\frac{795.8}{300 \times 10^6 / 2}\right)^2}$$

$$d^3 = \frac{16}{\pi}\sqrt{(1.067 \times 10^{-5})^2 + 0.75(5.305 \times 10^{-6})^2}$$

$$d^3 = \frac{16}{\pi}\sqrt{1.138 \times 10^{-10} + 2.111 \times 10^{-11}} = \frac{16}{\pi}\sqrt{1.349 \times 10^{-10}}$$

$$d^3 = 5.91 \times 10^{-5} \text{ m}^3 \implies d = 0.039 \text{ m} = 39 \text{ mm}$$

Select standard shaft diameter: **$d = 40$ mm**.

### Example 2: Flywheel Sizing

**Given:** A punch press requires 5 kJ of energy per punch stroke. The flywheel operates at a mean speed of 300 rpm with an allowable coefficient of fluctuation of 0.15.

**Find:** Required flywheel moment of inertia.

**Solution:**

Mean angular velocity:
$$\omega_{avg} = \frac{2\pi \times 300}{60} = 31.42 \text{ rad/s}$$

Required inertia:
$$I = \frac{\Delta E}{C_f \cdot \omega_{avg}^2} = \frac{5000}{0.15 \times 31.42^2} = \frac{5000}{148.1} = 33.8 \text{ kg·m}^2$$

## Applications

### Gas and Steam Turbines
- Multi-stage rotors with precise balancing requirements
- Critical speed analysis essential for flexible rotor designs
- Journal and tilting-pad bearings for high-speed support
- Overspeed governors for safety protection

### Internal Combustion Engines
- Crankshaft balancing for smooth operation
- Flywheel sizing for torque smoothing
- Torsional vibration analysis of crankshaft-flywheel systems

### Compressors and Pumps
- Shaft design for combined bending and torque loads
- Bearing selection for radial and thrust loads
- Balancing of impellers and rotors
- Speed regulation with variable frequency drives

### Electric Motors and Generators
- Rotor balancing to minimize vibration
- Critical speed avoidance in high-speed designs
- Flywheel energy storage systems for grid stabilization

Mastering the principles of rotating machinery is essential for engineers working with any system that converts between rotational and linear energy, from micro-turbines to large power plant generators.
