# Laplace Equation Maze Solver

This simulation generates a random perfect maze, solves Laplace's equation over the maze interior to produce a smooth potential field, and traces the solution path by following the potential gradient from entrance to exit. Watch it in action: [![YouTube](https://img.youtube.com/vi/kyYcME2sBws/maxresdefault.jpg)](https://youtu.be/kyYcME2sBws)

## Overview

- **Depth-first maze generation**: recursive backtracker produces a perfect $N\times N$ maze with exactly one path between any two cells.
- **Laplace's equation** $\nabla^2\phi=0$ solved over open cells with Dirichlet BCs: entrance $\phi=0$, exit $\phi=1$, walls $\phi=-1$.
- **Gradient ascent**: path traced by stepping to the neighbor with the highest potential.
- **Pygame rendering**: walls in black, open cells color-mapped by $\phi$, solution path highlighted in gold.

## Mathematical Background

### Laplace's Equation for Potential

Interior open cells satisfy:

$$\nabla^2\phi = 0$$

with boundary conditions $\phi=0$ at the entrance, $\phi=1$ at the exit, and walls fixed at $\phi=-1$ (excluded from relaxation).

### Finite-Difference Relaxation

The discrete Laplacian is iterated via Gauss–Seidel relaxation:

$$\phi_{i,j}^{\text{new}} = \phi_{i,j} + \Delta t\!\left(\frac{1}{4}\sum_{(k,\ell)\in\mathcal{N}(i,j)}\phi_{k,\ell} - \phi_{i,j}\right)$$

where $\mathcal{N}(i,j)$ denotes the four orthogonal neighbors. Iteration stops when $\max|\Delta\phi| < \varepsilon$ or after a fixed iteration cap.

### Path Extraction via Gradient Ascent

Starting at the entrance, move greedily to the open neighbor with the largest potential:

$$\text{next cell} = \arg\max_{(k,\ell)\in\mathcal{N}(i,j)} \phi_{k,\ell}$$

Continue until the exit is reached, backtracking if no unvisited neighbor has higher $\phi$.

### Color Mapping

Open cells are colored proportionally to their potential, mapping $[-1,+1]$ to the blue–green range:

$$\text{color} \propto \left(\frac{\phi+1}{2}\right)$$

## Implementation

1. Build a perfect maze on an $N\times N$ grid using a depth-first recursive backtracker; mark walls and passages.
2. Assign boundary potentials: $\phi=0$ (entrance), $\phi=1$ (exit), $\phi=-1$ (walls).
3. Iteratively apply the finite-difference relaxation stencil to all open interior cells until convergence ($\max|\Delta\phi|<10^{-6}$) or 5000 iterations.
4. Perform gradient ascent from the entrance: at each step move to the open neighbor with the largest $\phi$.
5. Each frame: extend the visible gold path by one step and redraw the full maze with current $\phi$ colors.
6. Continue until the path reaches the exit or the window is closed.

## Output

The Pygame window displays the maze and potential field rendered in real time:

- **Potential gradient**: a smooth color ramp from blue (entrance, $\phi=0$) to green (exit, $\phi=1$) reveals how the solution flows through maze passages.
- **Gold path**: the traced solution route is incrementally revealed frame by frame.
- **Start/End markers**: entrance in red, exit in green.
