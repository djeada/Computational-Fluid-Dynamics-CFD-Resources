## Interactive Maze Solver

This simulation generates a random maze, computes a steady-state potential field via the Laplace equation, and then traces a path by following the potential gradient.

## Maze Generation

A perfect maze on an $N\times N$ grid is created using a depth-first “recursive backtracker”:

I. Start at a chosen cell, mark it as open.

II. While there are cells on the stack:

* Look for unvisited neighbors two steps away.
* If any exist, carve a passage to one chosen at random and push it onto the stack.
* Otherwise, pop back to the previous cell.

This yields a maze with exactly one path between any two cells.

## Laplace’s Equation for Potential

We assign boundary potentials at the entrance ($\phi=0$) and exit ($\phi=1$), and walls are set to $\phi=-1$ to exclude them.  The interior potential $\phi(x,y)$ satisfies

$$\nabla^2 \phi = 0$$

Numerically, we iterate

$$\phi_{i,j}^{\mathrm{new}} = \phi_{i,j} + \Delta t\Bigl(\tfrac{1}{4}\sum_{(k,\ell)\in N_{i,j}(i,j)}\phi_{k,\ell} - \phi_{i,j}\Bigr)$$

where the sum runs over the four orthogonal neighbors.  Iteration continues until the maximum change in $\phi$ falls below a tolerance or until a fixed number of steps is reached.

## Path Extraction via Gradient Ascent

Starting from the entrance, the path to the exit is found by:

I. At each cell, examine all available neighbors (including diagonals).

II. Move to the neighbor with the highest potential $\phi$.

III. Continue until the exit is reached or backtrack if no unvisited neighbor has higher $\phi$.

This traces the steepest ascent on the potential field, flexible the maze solution.

## Discretization and Parameters

* **Maze grid**: $N\times N$ cells (e.g.\ $100\times100$).
* **Time step**: $\Delta t$ for relaxation (e.g.\ 0.1).
* **Tolerance**: threshold for $\max|\Delta\phi|$ (e.g.\ $10^{-6}$).
* **Max iterations**: cap on relaxation steps (e.g.\ 5000).

Periodic boundary conditions are applied only for the relaxation stencil; walls remain at fixed potential.

## Visualization

* **Walls**: black
* **Open cells**: color from blue ($\phi=-1$) to green ($\phi=+1$), via

$$\text{color} \propto \bigl(\tfrac{\phi+1}{2}\bigr)$$

* **Path**: highlighted in gold as it is gradually revealed.
* **Start/End**: marked in red and green respectively.
Each frame updates the potential relaxation, extends the visible path, and redraws the maze until the window is closed.
