# Surface Force Integration over Boundary Faces

This script integrates a surface pressure and wall-shear field over the flat faces of a body into a force and a moment, the same face sum a CFD code uses to report drag, lift and moment coefficients. It applies the sum to a circular cylinder with three analytic pressure fields and a hydrostatic field, so each integrated load can be compared with a known answer: zero drag in potential flow, the Kutta–Joukowski lift with circulation, Archimedes' buoyancy, and a drag coefficient near 1.1 for an illustrative separated-flow pressure distribution.

## Overview

- Represents the cylinder of radius 0.5 m by $N$ flat faces of an inscribed polygon, with face centroids, outward unit normals and face lengths (areas per unit span).
- Integrates the traction $-p\mathbf{n} + \boldsymbol{\tau}_w$ over the faces to obtain the force and the moment about the centre.
- Pressure fields: potential flow, potential flow with a clockwise circulation $\Gamma = -0.5 \times 2\pi aU$, a separated-flow model in which the potential-flow $C_p$ is cut off at a base pressure $C_{pb} = -1.2$, and hydrostatic pressure $-\rho g y$.
- Repeats the integration for $N = 8$ to 512 faces and plots the error of buoyancy and lift and the change of the separated-flow $C_d$.

## Mathematical Background

The force and moment of the fluid on a body with surface $S$ and outward normal $\mathbf{n}$ are

```math
\mathbf{F} = \oint_S \left(-p\,\mathbf{n} + \boldsymbol{\tau}_w\right) dA,
\qquad
\mathbf{M} = \oint_S \mathbf{r} \times \left(-p\,\mathbf{n} + \boldsymbol{\tau}_w\right) dA
```

and on a mesh they become sums over faces with the face-centre values. A constant pressure contributes nothing on a closed surface, so gauge pressure can be used. On a circle of radius $a$ in a uniform stream $U$ along $+x$, potential flow with circulation $\Gamma$ gives the surface speed $u_\varphi = -2U\sin\varphi + \Gamma/(2\pi a)$ and $C_p = 1 - (u_\varphi/U)^2$. The exact loads are zero drag and lift $L = -\rho U\Gamma$ per unit span. For hydrostatic pressure the divergence theorem gives $`\oint -p\,\mathbf{n}\,dA = \int_V -\nabla p\,dV = \rho g V\,\hat{\mathbf{y}}`$; on the polygon the face sum of this linear field reproduces $\rho g$ times the polygon area exactly, so the error with respect to $\rho g\pi a^2$ is purely geometric and falls as $N^{-2}$. The drag coefficient per unit span is $C_d = F_x/(\tfrac12\rho U^2\cdot 2a)$, which for a pressure distribution in terms of the angle $\theta$ from the front stagnation point is $`C_d = \tfrac12\oint C_p\cos\theta\,d\theta`$.

## Implementation

- `cylinder_faces(n)` returns the polygon vertices, face centroids, outward normals and face lengths.
- `integrate_loads(centroids, normals, areas, pressure, shear=None, origin=(0, 0))` is the face sum for force and moment and accepts an optional array of wall-shear vectors.
- `potential_cp(phi, circulation)` and `separated_cp(phi, base_cp)` are the pressure models.
- `loads_for(n, case)` evaluates one case on $n$ faces and `coefficients(force)` converts to $C_d$ and $C_l$.
- Constants `RADIUS`, `U_INF`, `RHO`, `CIRCULATION_FRACTION`, `BASE_PRESSURE_COEFF`, `N_FIGURE` and `N_SEQUENCE` set the case.

## Usage

```bash
python main.py                         # print the face-sum table and show the figure
python main.py --no-show --output .    # save fluid_loading_surface_force_integration.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

On every mesh the potential-flow drag, the drag with circulation and the moment are below $10^{-12}$ N/m, round-off. With 8 faces the buoyancy is 6937 N/m against the exact 7705 N/m and the lift 6123 N/m against $\rho U|\Gamma| = 6283$ N/m; with 512 faces the errors are 0.003% and 0.0006%, both falling as $N^{-2}$. The separated-flow model gives $C_d = 1.14$ on 8 faces and $C_d = 1.088$ on 128 or more, close to the measured drag coefficient of a cylinder at subcritical Reynolds numbers; its convergence is irregular because $C_p$ has a kink where the base pressure starts.

![Surface pressure distributions, face tractions on a 36-face cylinder and convergence of the integrated loads with the number of faces](fluid_loading_surface_force_integration.png)

Panel (a) shows the three pressure distributions against the angle from the front stagnation point. Panel (b) shows the separated-flow model on 36 faces, coloured by $C_p$, with the traction $-C_p\mathbf{n}$ on each face: pressure pushes on the front, suction pulls on the sides and rear, and the imbalance between front and rear is the pressure drag. Panel (c) shows the second-order convergence of the face sums.

## Related Notes

- [Pressure Forces on Structures](../../../notes/applied_mechanics/fluid_loading/pressure_forces.md)
- [Fluid Loading on Structures](../../../notes/applied_mechanics/fluid_loading/intro.md)
