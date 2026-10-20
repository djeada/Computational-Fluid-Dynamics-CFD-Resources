# Statics

Statics finds the forces in bodies and structures that do not accelerate, from the balance of forces and moments. These notes start with the equilibrium of a particle and of a rigid body, including the supports that make a body determinate or leave it improperly held, then compute centroids for weights and distributed loads, analyse trusses, frames and machines, and introduce the force and stiffness methods that handle indeterminate structures and lead to the finite element method. They end with dry friction and with the principle of virtual work, which gives equilibrium and its stability from the potential energy.

## Table of Contents

### 1. [Particle Equilibrium](./particle_equilibrium.md)

Concurrent forces in 2D and 3D as a linear system for the unknown magnitudes, cables and their tension under transverse load, force polygons and Lami's theorem, springs in series and parallel, and ideal pulleys.

### 2. [Rigid Body Equilibrium](./rigid_body_equilibrium.md)

Force and moment balance in 2D and 3D, distributed loads, support reactions, two- and three-force members, statical determinacy, and improper constraints detected by the rank of the reaction matrix.

### 3. [Center of Mass and Centroids](./center_of_mass.md)

Centers of mass and gravity, centroids by integration and by composite parts with negative areas for holes, the theorems of Pappus and Guldinus, and second moments of area with the parallel-axis theorem.

### 4. [Trusses, Frames and Machines](./trusses_frames.md)

The pin-jointed truss idealization, determinacy of plane and space trusses, the methods of joints and sections in hand and matrix form, zero-force members, space trusses, and the member-by-member analysis of frames and machines.

### 5. [Structural Analysis](./structural_analysis.md)

Structural idealization and load paths, degrees of indeterminacy, cables and arches, influence lines, the force (flexibility) method with the unit-load method, and the direct stiffness method for trusses as the first finite element method.

### 6. [Friction](./friction.md)

Coulomb friction and the angle of friction, inclines, sliding versus tipping, wedges and their self-locking condition, square-threaded screws and their efficiency, the capstan equation for belts and ropes, and rolling resistance.

### 7. [Virtual Work and Stability of Equilibrium](./virtual_work.md)

Virtual displacements and ideal constraints, generalized coordinates and forces, mechanical advantage of linkages and toggles, potential energy, the stability criterion $d^2V/dq^2 > 0$, bifurcation and snap-through, and the link to the unit-load and finite element methods.
