# Bak–Tang–Wiesenfeld Sandpile Model (3D)

This script animates the three-dimensional Bak–Tang–Wiesenfeld (BTW) sandpile model on a 20×20 grid with a critical height of 8. At each frame a single grain is added to a randomly chosen cell. When a cell's grain count meets or exceeds the critical threshold, it topples: it loses grains equal to the threshold and each of its four cardinal neighbours receives one grain. Boundary cells lose grains off the edge, providing the open-boundary dissipation required for self-organised criticality (SOC). The evolving height field is rendered as an animated 3D surface with the plasma colormap on a dark background.

## Overview

- 20×20 lattice with critical threshold $z_c = 8$ and open (dissipative) boundaries
- One grain added per animation frame to a uniformly random cell
- Iterative toppling loop redistributes grains until the lattice is stable
- Real-time 3D surface plot with plasma colormap on a dark background
- Demonstrates self-organised criticality emerging from simple local rules

## Mathematical Background

### Toppling Rule

A cell $(i, j)$ is unstable when its height $z_{ij}$ reaches the critical threshold $z_c$. The toppling update is:

$$z_{ij} \geq z_c \;\Rightarrow\; z_{ij} \to z_{ij} - z_c, \quad z_{i\pm1,j},\, z_{i,j\pm1} \to z_{i\pm1,j} + 1,\; z_{i,j\pm1} + 1$$

### Open Boundary Conditions

Grains that would be distributed to cells outside the grid are simply discarded, making the boundary dissipative. This energy loss is essential for the system to reach a stationary critical state.

### Power-Law Avalanche Distribution

Repeated addition and toppling drives the system to a critical state where avalanche sizes $s$ (total number of topplings per added grain) follow a power-law probability distribution:

$$P(s) \sim s^{-\tau}, \qquad \tau \approx 1.2 \text{ (2D BTW)}$$

### Self-Organised Criticality

Unlike conventional critical phenomena, SOC requires no external tuning of a control parameter. The system self-organises to the critical state through the competition between slow driving (grain addition) and fast relaxation (avalanche toppling).

## Implementation

1. Initialise a 20×20 integer array of grain heights to zero.
2. At each animation frame, increment a random cell by one grain.
3. Enter a toppling loop: scan for unstable cells ($z_{ij} \geq z_c$), apply the toppling rule, and repeat until no unstable cells remain.
4. Update the 3D surface plot with the new height field using `plot_surface` and the plasma colormap.
5. Repeat for the desired number of frames to produce the animation.

## Output

The script produces an interactive animated 3D surface plot of the sandpile height field, updated frame by frame as grains are added and avalanches propagate. The plasma colormap maps grain height to colour, and the dark background emphasises the evolving topographic structure of the critical sandpile.

