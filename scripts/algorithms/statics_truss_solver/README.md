# Plane Truss Solver

This script solves a plane pin-jointed truss by the method of joints and by the direct stiffness method. The method of joints is assembled for all joints at once into a square linear system in the member forces and reactions, which is solvable only for a determinate truss; the stiffness method solves for the joint displacements and works for indeterminate trusses as well. The example is a six-panel Pratt truss under five equal bottom-chord loads, checked three ways, and a cross-braced version of it that is six times indeterminate.

## Overview

- Builds a rectangular Pratt truss of `N_PANELS = 6` panels, 3 m wide and 3 m deep, with a pin at the left end, a roller at the right end and 20 kN downward at each interior bottom joint.
- Classifies the truss from the count $m + r - 2j$ and the rank of the equilibrium matrix as determinate, indeterminate or unstable.
- Solves the joint equilibrium equations for the 25 member forces and 3 reactions with one `numpy.linalg.solve`.
- Assembles the global stiffness matrix from bar elements with $E = 200$ GPa and $A = 2000$ mm², solves for the free displacements and recovers member forces and reactions.
- Checks the midspan deflection with the unit-load (virtual work) method, $\Delta = \sum N n L/(EA)$.
- Adds the second diagonal to every panel and solves the resulting indeterminate truss by the stiffness method only.
- Draws the member forces with a diverging colormap and line widths scaled by magnitude, the deflected shape, and the cross-braced truss.

## Mathematical Background

### Joint Equilibrium

With $\mathbf{u}_{e,i}$ the unit vector along member $e$ pointing away from joint $i$, equilibrium of every joint reads

```math
\sum_{e \ni i} N_e\,\mathbf{u}_{e,i} + \mathbf{R}_i + \mathbf{P}_i = \mathbf{0}
\quad\Longleftrightarrow\quad
\mathbf{A}\begin{bmatrix}\mathbf{N}\\ \mathbf{R}\end{bmatrix} = -\mathbf{P}
```

$\mathbf{A}$ has $2j$ rows and $m + r$ columns. The truss is determinate when $\mathbf{A}$ is square and has full rank, unstable when its rank is below $2j$, and indeterminate to degree $m + r - 2j$ otherwise.

### Direct Stiffness Method

A bar of length $L$, rigidity $EA$ and unit vector $\mathbf{c}$ from joint $i$ to $j$ has the element stiffness matrix

```math
\mathbf{k}_e = \frac{EA}{L}\begin{bmatrix} \mathbf{c}\mathbf{c}^{\mathsf{T}} & -\mathbf{c}\mathbf{c}^{\mathsf{T}} \\ -\mathbf{c}\mathbf{c}^{\mathsf{T}} & \mathbf{c}\mathbf{c}^{\mathsf{T}} \end{bmatrix}
```

The global matrix $\mathbf{K}$ is the sum of the element matrices placed at the degrees of freedom of their joints. With the restrained degrees of freedom set to zero, $\mathbf{K}_{ff}\mathbf{d}_f = \mathbf{p}_f$ gives the displacements, $`N_e = (EA/L)\,\mathbf{c}\cdot(\mathbf{d}_j - \mathbf{d}_i)`$ the member forces, and $\mathbf{R} = (\mathbf{K}\mathbf{d} - \mathbf{p})_r$ the reactions.

### Unit-Load Method

For a determinate truss the displacement of joint $k$ in direction $d$ is

```math
\Delta = \sum_e \frac{N_e\,n_e\,L_e}{E A}
```

where $N_e$ are the member forces under the real loads and $n_e$ those under a unit load at joint $k$ in direction $d$. It is the principle of complementary virtual work and must agree with the stiffness method.

## Implementation

- `pratt_truss(n_panels, panel, height, load, cross_braced)` returns the joint coordinates, the member list, the support dictionary `{joint: (fix_x, fix_y)}` and the joint loads.
- `member_geometry(nodes, members)` returns member lengths and unit vectors; `restrained_dofs(supports)` lists the global degrees of freedom held by supports.
- `equilibrium_matrix(nodes, members, supports)` assembles $\mathbf{A}$ and `classify_truss(...)` returns the degree $m + r - 2j$, the rank deficiency and the classification.
- `method_of_joints(nodes, members, supports, loads)` solves the determinate system and raises `ValueError` otherwise.
- `element_stiffness(unit, length, ea)` and `direct_stiffness(nodes, members, supports, loads, ea)` implement the stiffness method.
- `unit_load_deflection(nodes, members, supports, loads, joint, direction, ea)` applies the unit-load method using two calls of `method_of_joints`.
- `make_figure(...)` draws the three panels; `draw_forces` dashes members whose force is zero to round-off.
- Constants `N_PANELS`, `PANEL_WIDTH`, `TRUSS_HEIGHT`, `JOINT_LOAD`, `YOUNG_MODULUS` and `MEMBER_AREA` set the example.

## Usage

```bash
python main.py                          # print the results and show the figure
python main.py --no-show --output .     # save statics_truss_solver.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints:

```text
Pratt truss: j = 14, m = 25, r = 3, determinate
reactions (kN): A_x = 0.0, A_y = 50.0, B_y = 50.0
largest tension 80.0 kN, largest compression -90.0 kN, zero-force members 3
max |N_joints - N_stiffness| = 3.49e-10 N
midspan deflection: stiffness -7.759 mm, unit load -7.759 mm
cross-braced: m = 31, indeterminate (degree 6), midspan deflection -5.904 mm, largest diagonal 37.9 kN
```

![Pratt truss member forces, deflected shape and cross-braced version](statics_truss_solver.png)

Panel (a) labels every member force in kN: the chords carry the bending of the truss as a couple and peak at midspan ($-90$ kN top, $+80$ kN bottom), the diagonals are in tension and the verticals in compression, as in every Pratt truss under gravity load. The end bottom-chord members and the midspan vertical are zero-force members. Panel (b) shows the deflected shape from the stiffness method magnified 46 times over the undeformed truss. Panel (c) is the cross-braced truss: the shear in each panel is now shared by two diagonals, one in tension and one in compression, so the largest diagonal force drops from 70.7 kN to 37.9 kN and the midspan deflection from 7.76 mm to 5.90 mm.

## Related Notes

- [Trusses, Frames and Machines](../../../notes/applied_mechanics/statics/trusses_frames.md)
- [Structural Analysis](../../../notes/applied_mechanics/statics/structural_analysis.md)
- [Virtual Work and Stability of Equilibrium](../../../notes/applied_mechanics/statics/virtual_work.md)
- [Rigid Body Equilibrium](../../../notes/applied_mechanics/statics/rigid_body_equilibrium.md)
- [The Finite Element Method](../../../notes/numerical/fem/intro.md)
