# Work-Energy Methods

Work-energy methods provide a powerful scalar approach to dynamics problems, bypassing the need to solve for accelerations directly. These methods relate forces and displacements to changes in kinetic and potential energy, making them especially efficient when velocities at different positions are required.

## Work of a Force

The **work** done by a force $\mathbf{F}$ on a particle as it moves along a path from position 1 to position 2 is:

$$U_{1 \to 2} = \int_1^2 \mathbf{F} \cdot d\mathbf{r}$$

### Work of Common Forces

**Constant force:**
$$U = F \cos\theta \cdot d$$
where $\theta$ is the angle between the force and displacement, and $d$ is the displacement magnitude.

**Weight** (displacement $\Delta y$ upward positive):
$$U_W = -mg\Delta y = -mg(y_2 - y_1)$$

**Spring force** (linear spring, displacement from natural length):
$$U_s = -\left(\frac{1}{2}kx_2^2 - \frac{1}{2}kx_1^2\right)$$

**Friction force** (always opposes motion):
$$U_f = -\mu_k N \cdot d$$

where $d$ is the total distance traveled (not displacement).

**Normal force and forces perpendicular to motion:**
$$U_N = 0$$

## Work of a Couple

For a rigid body, the work done by a couple moment $M$ through an angular displacement is:

$$U_{1 \to 2} = \int_{\theta_1}^{\theta_2} M \, d\theta$$

For a constant couple:
$$U = M(\theta_2 - \theta_1)$$

## Kinetic Energy

### Particle
$$T = \frac{1}{2}mv^2$$

### Rigid Body in Translation
$$T = \frac{1}{2}mv_G^2$$

### Rigid Body in Rotation About Fixed Axis $O$
$$T = \frac{1}{2}I_O\omega^2$$

### Rigid Body in General Plane Motion
$$T = \frac{1}{2}mv_G^2 + \frac{1}{2}I_G\omega^2$$

The first term is the translational kinetic energy of the mass center; the second is the rotational kinetic energy about the mass center.

## Work-Energy Theorem

The work done by all external forces equals the change in kinetic energy:

$$\sum U_{1 \to 2} = T_2 - T_1$$

Or equivalently:

$$T_1 + \sum U_{1 \to 2} = T_2$$

This is a scalar equation — no vector components or coordinate systems are needed for the energy terms.

## Potential Energy

A force is **conservative** if its work depends only on the initial and final positions, not the path. Conservative forces have an associated potential energy.

### Gravitational Potential Energy (Near Surface)

$$V_g = mgy$$

where $y$ is measured upward from a chosen datum.

### Elastic Potential Energy (Linear Spring)

$$V_e = \frac{1}{2}kx^2$$

where $x$ is the deformation from the spring's natural length.

### Gravitational Potential Energy (General)

For two masses separated by distance $r$:

$$V_g = -\frac{GMm}{r}$$

## Conservation of Energy

When **only conservative forces** do work, the total mechanical energy is conserved:

$$T_1 + V_1 = T_2 + V_2$$

This is equivalent to:

$$E = T + V = \text{constant}$$

When non-conservative forces (friction, applied forces) also do work:

$$T_1 + V_1 + U_{1 \to 2}^{nc} = T_2 + V_2$$

where $U_{1 \to 2}^{nc}$ is the work of non-conservative forces.

## Power and Efficiency

**Power** is the rate at which work is done:

$$P = \frac{dU}{dt} = \mathbf{F} \cdot \mathbf{v}$$

For a rotating body:
$$P = M\omega$$

**Units:** 1 W = 1 J/s = 1 N·m/s; 1 hp = 745.7 W

**Efficiency:**
$$\eta = \frac{P_{out}}{P_{in}} = \frac{\text{useful power output}}{\text{total power input}}$$

## Worked Examples

### Example 1: Block-Spring System

A 5 kg block is pushed against a spring ($k = 800$ N/m), compressing it 0.15 m. The block is then released on a frictionless surface.

**Given:**
- $m = 5$ kg, $k = 800$ N/m, $x_0 = 0.15$ m
- Frictionless surface

**Find:** Speed of the block when the spring returns to its natural length.

**Solution:**

Using conservation of energy (datum at spring natural length position):

$$T_1 + V_1 = T_2 + V_2$$

$$0 + \frac{1}{2}kx_0^2 = \frac{1}{2}mv^2 + 0$$

$$\frac{1}{2}(800)(0.15)^2 = \frac{1}{2}(5)v^2$$

$$9 = 2.5v^2$$

$$v = \sqrt{3.6} = 1.90 \text{ m/s}$$

### Example 2: Rolling Cylinder Down a Ramp

A solid cylinder of mass 10 kg and radius 0.3 m starts from rest and rolls without slipping down a 4 m long incline at 30°.

**Given:**
- $m = 10$ kg, $R = 0.3$ m, $L = 4$ m, $\theta = 30°$
- $I_G = \frac{1}{2}mR^2 = 0.45$ kg·m²
- Rolling: $v_G = \omega R$

**Find:** Speed at the bottom.

**Solution:**

Height dropped: $h = L\sin\theta = 4\sin 30° = 2$ m

Friction does no work for rolling without slipping (contact point has zero velocity). Using conservation of energy:

$$0 + mgh = \frac{1}{2}mv_G^2 + \frac{1}{2}I_G\omega^2$$

$$mgh = \frac{1}{2}mv_G^2 + \frac{1}{2}\left(\frac{1}{2}mR^2\right)\frac{v_G^2}{R^2}$$

$$mgh = \frac{1}{2}mv_G^2 + \frac{1}{4}mv_G^2 = \frac{3}{4}mv_G^2$$

$$v_G = \sqrt{\frac{4gh}{3}} = \sqrt{\frac{4(9.81)(2)}{3}} = 5.11 \text{ m/s}$$

### Example 3: Power Required for a Vehicle

A 1500 kg car travels at a constant 90 km/h up a 5% grade. The total drag and rolling resistance is 600 N.

**Given:**
- $m = 1500$ kg, $v = 25$ m/s (90 km/h)
- Grade: $\sin\theta \approx 0.05$
- Resistance: $F_R = 600$ N

**Find:** Required engine power and power in horsepower.

**Solution:**

At constant speed, the engine must overcome gravity and resistance:

$$F_{engine} = mg\sin\theta + F_R = 1500(9.81)(0.05) + 600 = 735.75 + 600 = 1335.75 \text{ N}$$

**Power:**
$$P = F_{engine} \cdot v = 1335.75(25) = 33\,394 \text{ W} = 33.4 \text{ kW}$$

$$P = \frac{33\,394}{745.7} = 44.8 \text{ hp}$$

### Example 4: Pendulum with Friction at Pivot

A uniform rod of mass 2 kg and length 0.8 m swings from horizontal to vertical. A constant friction moment of 0.5 N·m acts at the pivot.

**Given:**
- $m = 2$ kg, $L = 0.8$ m, $M_f = 0.5$ N·m
- $I_O = \frac{1}{3}mL^2 = 0.427$ kg·m²
- Swing angle: $\Delta\theta = 90° = \frac{\pi}{2}$ rad

**Find:** Angular velocity at the vertical position.

**Solution:**

The center of mass drops by $L/2 = 0.4$ m. Using work-energy with non-conservative work:

$$T_1 + V_1 + U_{nc} = T_2 + V_2$$

$$0 + mg\frac{L}{2} - M_f \Delta\theta = \frac{1}{2}I_O\omega^2 + 0$$

$$2(9.81)(0.4) - 0.5\left(\frac{\pi}{2}\right) = \frac{1}{2}(0.427)\omega^2$$

$$7.848 - 0.785 = 0.2133\omega^2$$

$$\omega = \sqrt{\frac{7.063}{0.2133}} = 5.75 \text{ rad/s}$$

## Applications

### Mechanical Design
- Sizing motors and engines based on power requirements
- Flywheel design for energy storage and speed regulation
- Spring selection for mechanisms and vibration isolators

### Vehicle Dynamics
- Fuel economy estimation from resistance forces
- Braking distance calculations using energy dissipation
- Regenerative braking energy recovery

### Structural Engineering
- Impact loading analysis using energy equivalence
- Collapse mechanism analysis using virtual work
- Earthquake energy dissipation in dampers

### Aerospace
- Orbital transfer energy requirements (Hohmann transfers)
- Aircraft climb performance and ceiling calculations
- Rocket staging optimization

## Practical Problem-Solving Tips

### 1. Choose Energy Methods When Appropriate
- Use when you need velocities at specific positions, not at specific times
- Especially useful when the path is complex but endpoints are known
- Avoid for problems asking for acceleration or reaction forces

### 2. Set a Clear Datum for Potential Energy
- Place the datum at the lowest point or the final position to minimize negative terms
- Be consistent throughout the problem
- Gravitational PE is relative; only differences matter

### 3. Account for All Energy Terms
- Include both translational and rotational kinetic energy for rigid bodies
- Check whether springs are compressed or extended at each state
- Include work of non-conservative forces (friction, applied forces)

### 4. Verify Friction and Power Calculations
- Friction work is always negative — use total distance traveled, not displacement
- For rolling without slipping, friction does zero work
- At constant velocity, driving force equals resistance; $P = Fv$

Work-energy methods complement Newton's second law by providing an efficient alternative for velocity-related problems and are the foundation for Lagrangian mechanics and advanced analytical dynamics.
