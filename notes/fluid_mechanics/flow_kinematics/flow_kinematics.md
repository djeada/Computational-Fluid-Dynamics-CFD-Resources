## Flow Kinematics

Flow kinematics focuses on describing the motion of fluids without directly considering the forces that cause that motion. It is a geometric and mathematical viewpoint, centered on how fluid particles move, deform, and change position over time. By examining velocity fields, acceleration, deformation rates, and vorticity, flow kinematics provides the language and tools to describe fluid motion in space and time. It is the foundation on which more complex fluid dynamics concepts are built, as it helps establish a clear picture of the fluid’s movement before considering the detailed balance of forces and energy.

Kinematics in fluid mechanics is somewhat analogous to describing the paths and patterns of dancers on a stage without worrying about why they are dancing that way. The focus remains on identifying trajectories, understanding how shapes within the fluid change, and clarifying how fluid elements translate, rotate, and stretch. Once these geometric descriptions are in place, one can add in forces, pressure gradients, viscosity, and other factors to get the full story.

```
Visualizing Flow Kinematics
---------------------------
 
   Consider a fluid flowing past a stationary object:
 
       Velocity Field Lines (Streamlines):
 
             --->   --->   --->   --->   --->
         --->   --->   --->   --->   --->   --->
      --->   --->  [  Object  ]  --->   --->  --->
         --->   --->   --->   --->   --->   --->
             --->   --->   --->   --->   --->
 
   Each arrow represents the fluid’s velocity at a point.
   Flow kinematics involves describing how these velocity 
   vectors change in space and time.

```

### Lagrangian and Eulerian Descriptions

In kinematics, there are two primary ways to describe fluid motion: the Lagrangian and Eulerian perspectives. The Lagrangian approach follows individual fluid particles as they move, much like tracking a single floating leaf down a river. The Eulerian approach focuses on specific points in space and observes how the fluid passes through them, more like installing sensors at fixed locations along the river bank.

The Lagrangian viewpoint helps understand particle paths, whereas the Eulerian viewpoint is convenient for describing flow fields and working with field equations. In practice, most theoretical and computational fluid mechanics is done in the Eulerian framework, but switching between the two can offer insights into complex flows.

### Velocity and Acceleration Fields

The fundamental starting point in flow kinematics is the velocity field $\vec{v}(x,y,z,t)$, which tells how fast and in which direction fluid moves at any point and time. Once velocity is known, it is possible to find acceleration by taking the substantial (or material) derivative of the velocity field.

The material derivative links Eulerian and Lagrangian views. For any property $\phi$ (such as velocity), its material derivative $D\phi/Dt$ represents the rate of change experienced by a fluid particle moving with the flow. If $\vec{v} = (u,v,w)$ in Cartesian coordinates:

$$
\frac{D\phi}{Dt} = \frac{\partial \phi}{\partial t} + u
\frac{\partial \phi}{\partial x} + v \frac{\partial \phi}{\partial y} + w
\frac{\partial \phi}{\partial z}
$$

For velocity itself, the material derivative gives the particle acceleration:

$$
\frac{D\vec{v}}{Dt} = \frac{\partial \vec{v}}{\partial t} + (\vec{v}\cdot\nabla)\vec{v}
$$

This expression shows how fluid particles accelerate both because of local changes in velocity over time and because they move to regions with different velocities.

```
Material Derivative Concept:
----------------------------

Think of a small fluid parcel:

 At time t0: Parcel at (x0,y0)
 Moves to (x1,y1) at time t1.

 Property φ may vary in space and time.
 As parcel moves, it "feels" changes in φ.

The material derivative tracks changes 
that the parcel itself experiences, 
combining local and convective effects.
```

### Deformation, Rotation, and Strain Rates

Flow kinematics also characterizes how fluid elements deform. Consider a small fluid element initially shaped like a cube. As it moves through the flow, it may change shape due to velocity gradients. Deformation can be broken down into three categories:

1. Translation: The fluid element moves as a whole without changing shape or orientation.
2. Rotation: The fluid element spins as it moves, like a tiny gear in the flow.
3. Deformation or Straining: The fluid element’s shape changes, possibly stretching or compressing in different directions.

The velocity gradients $\partial u/\partial x$, $\partial v/\partial y$, etc., determine these deformation characteristics. By examining the velocity gradient tensor $\nabla \vec{v}$, one can split it into symmetric and antisymmetric parts. The antisymmetric part relates to rotation (vorticity), while the symmetric part relates to strain rates.

Vorticity $\vec{\omega} = \nabla \times \vec{v}$ measures the fluid’s local spinning motion. Regions of high vorticity often correspond to vortices, which are common flow structures. The strain rate tensor measures how fluid elements stretch or compress. For instance, a flow accelerating in the $x$-direction and decelerating in the $y$-direction would stretch fluid elements in one direction and compress them in another.

```
Deformation of a Fluid Element:
--------------------------------

Initial fluid element:
 +-----+
 |     |
 |     |
 +-----+

After passing through a region with velocity gradients:
 Shear might tilt the element:
   +------\
   |       \
   |        \
   +---------\

Rotation might make it spin,
stretching might elongate one side.

Analysis of these changes 
quantifies strain rates and vorticity.
```

### Streamlines, Pathlines, and Streaklines

Flow kinematics offers different concepts for visualizing fluid motion:

- **Streamlines** are the curves that are everywhere tangent to the velocity field at a given instant. They provide a snapshot of the flow pattern at one moment in time.
- **Pathlines** are the actual trajectories followed by individual fluid particles. They show the history of a single particle’s journey through the flow field.
- **Streaklines** are the lines formed by all particles that have passed through a particular point in space. Imagine continuously injecting dye at one point; the streakline is the pattern that emerges from that injection point over time.

These concepts often coincide in steady flows, where the flow pattern does not change with time. In unsteady flows, streamlines, pathlines, and streaklines can differ, providing insights into how the flow evolves and how particles navigate through it.

![steady_vs_unsteady_flow](https://github.com/user-attachments/assets/10e6d8fa-2f8b-4a24-97fa-63ae9ac01f14)

### Related Scripts

- [Eulerian and Lagrangian Flow Descriptions](../../../scripts/plots/eulerian_lagrangian_flows/): contrasts the Eulerian and Lagrangian descriptions of fluid motion using the time-dependent Double Gyre flow.
- [Steady and Unsteady Pathlines Around a Cylinder with Vortex Shedding](../../../scripts/simulations/steady_and_unsteady_pathlines_with_vortex_shedding/): compares streamlines and particle pathlines for steady potential flow past a cylinder with circulation and for an unsteady version of the same flow with a kinematic vortex-shedding model.

### Exercises

**Exercise 1.** Explain why streamlines, pathlines and streaklines coincide in a steady flow, and give an everyday example where they differ.

<details>
<summary>Answer</summary>

In a steady flow the velocity field does not change with time. A particle therefore keeps following the instantaneous streamline through its current position, so its pathline is that streamline. Every particle released from the same point follows the same path, so the streakline coincides too.

In an unsteady flow they differ. One example is smoke from a chimney when the wind keeps changing direction: the smoke plume (the streakline) curls, while the streamline pattern at any one instant looks quite different.

</details>

**Exercise 2.** For the steady two-dimensional field $u = x^2$, $v = -2xy$: (a) check that it satisfies $\partial u/\partial x + \partial v/\partial y = 0$; (b) compute the particle acceleration $D\vec{v}/Dt$ at the point $(1, 2)$.

<details>
<summary>Answer</summary>

(a) $\partial u/\partial x = 2x$ and $\partial v/\partial y = -2x$. They sum to zero.

(b) The flow is steady, so only the convective terms remain:

```math
a_x = u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} = x^2(2x) +
(-2xy)(0) = 2x^3
```

```math
a_y = u \frac{\partial v}{\partial x} + v \frac{\partial v}{\partial y} = x^2(-2y) +
(-2xy)(-2x) = 2x^2 y
```

At $(1,2)$: $\vec{a} = (2, 4)$ in the units of the field.

</details>

**Exercise 3.** For simple shear, $u = \dot{\gamma} y$ and $v = 0$. Split the velocity gradient tensor into its symmetric part (strain rate) and antisymmetric part (rotation), and find the vorticity.

<details>
<summary>Answer</summary>

The only nonzero velocity gradient is $\partial u/\partial y = \dot{\gamma}$. Write $\nabla \vec{v} = \mathbf{S} + \mathbf{W}$, with $S_{ij} = \frac{1}{2}(\partial u_i/\partial x_j + \partial u_j/\partial x_i)$ and $W_{ij} = \frac{1}{2}(\partial u_i/\partial x_j - \partial u_j/\partial x_i)$:

- Strain rate: $S_{xy} = S_{yx} = \dot{\gamma}/2$, and $S_{xx} = S_{yy} = 0$.
- Rotation: $W_{xy} = \dot{\gamma}/2$ and $W_{yx} = -\dot{\gamma}/2$.

The vorticity is $\omega_z = \partial v/\partial x - \partial u/\partial y = -\dot{\gamma}$, so fluid elements spin clockwise at the angular velocity $\omega_z/2 = -\dot{\gamma}/2$. At the same time they are stretched along the $45^\circ$ diagonal and compressed along the other diagonal.

</details>

**Exercise 4.** Consider the unsteady flow $u = 1$, $v = t$ (nondimensional units). (a) Find the streamlines at time $t$. (b) Find the pathline of the particle that is at the origin when $t = 0$. (c) Compare the two.

<details>
<summary>Answer</summary>

(a) Streamlines satisfy $dy/dx = v/u = t$. At a fixed instant they are straight lines $y = t x + C$ with slope $t$.

(b) $dx/dt = 1$ and $dy/dt = t$ with $x(0) = y(0) = 0$ give $x = t$ and $y = t^2/2$. Eliminating $t$, the pathline is the parabola $y = x^2/2$.

(c) The particle moves along a parabola, but every instantaneous streamline is a straight line. At each instant the particle's path is tangent to the streamline through its current position, yet the two curves differ, as expected in unsteady flow.

</details>

### References

- P. K. Kundu, I. M. Cohen, D. R. Dowling, *Fluid Mechanics*, 6th ed., Academic Press, 2016.
- R. L. Panton, *Incompressible Flow*, 4th ed., Wiley, 2013.
- R. Aris, *Vectors, Tensors, and the Basic Equations of Fluid Mechanics*, Prentice-Hall, 1962.
