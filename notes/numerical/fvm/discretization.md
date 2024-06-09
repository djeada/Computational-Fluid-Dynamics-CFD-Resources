# Discretization Using The Finite-Volume Method

In the finite-volume method, the computational domain is divided into cells (e.g., quadrilaterals in 2D or hexahedrals in 3D). A grid point is referred to as a "node," and each cell defines a control volume for which conservation equations are applied.

## Integral Form of the Conservation Equations

The integral form of the continuity equation for steady, incompressible flow is:
$$ 
\int_S \vec{V} \cdot \hat{n} \, dS = 0 
$$
where:
- $ S $ is the surface of the control volume.
- $ \hat{n} $ is the outward normal at the surface.

This equation implies that the net volume flow into the control volume is zero.

## Example: Rectangular Cell

Consider a rectangular cell with dimensions $ \Delta x $ and $ \Delta y $:
# Discretization Using The Finite-Volume Method

In the finite-volume method, the computational domain is divided into cells (e.g., quadrilaterals in 2D or hexahedrals in 3D). A grid point is referred to as a "node," and each cell defines a control volume for which conservation equations are applied.

## Integral Form of the Conservation Equations

The integral form of the continuity equation for steady, incompressible flow is:
$$ 
\int_S \vec{V} \cdot \hat{n} \, dS = 0 
$$
where:
- $ S $ is the surface of the control volume.
- $ \hat{n} $ is the outward normal at the surface.

This equation implies that the net volume flow into the control volume is zero.

## Example: Rectangular Cell

Consider a rectangular cell with dimensions $ \Delta x $ and $ \Delta y $:


```
                Δx
           |---------|
           |         |  (u₄',v₄') face 4
           |         |
(u₁',v₁')  |         |
---------  ___________
|         |           |
| Δy      |           |
|         |           |
---------  ___________
```


### Applying Mass Conservation

The velocity at face $i$ is given by $\vec{V_i} = u_i \hat{i} + v_i \hat{j}$. Applying the mass conservation equation to the control volume defined by the cell yields:
$$ 
-u_1 \Delta y - v_2 \Delta x + u_3 \Delta y + v_4 \Delta x = 0 
$$

This discrete form of the continuity equation ensures that the net mass flow into the cell is zero, preserving mass conservation for the cell.

### Solving the Discrete System

- The values at the cell centers are solved directly by inverting the discrete system.
- The face values $u_1, v_2$, etc., are obtained by interpolating the cell-center values of adjacent cells.

## Conservation of Momentum and Energy

- Discrete equations for the conservation of momentum and energy can be derived similarly.
- These principles can be extended to any general cell shape in 2D or 3D and any conservation equation.

## Comparison with Finite-Difference Method

- **Finite-Volume Method:** Applies integral conservation laws to control volumes, ensuring conservation properties directly.
- **Finite-Difference Method:** Uses Taylor series expansions to approximate derivatives, leading to algebraic equations.

