# Time-Averaged Velocity Field

This script generates a synthetic instantaneous longitudinal velocity field over a 200×60 spatial grid, computes its time (spatial) average, and visualises both the instantaneous and mean fields side-by-side. The workflow illustrates the Reynolds decomposition procedure that underpins turbulence modelling in CFD.

## Overview

- Constructs a synthetic velocity field $u(x,y) = 10\sin(0.02x)\cos(0.1y) + \text{noise}$
- Averages the field along the x-direction to obtain the mean profile $\bar{u}(y)$
- Derives the fluctuation field $u'(x,y) = u - \bar{u}$
- Renders colour maps of the instantaneous field and the mean profile on separate subplots

## Mathematical Background

### Reynolds Decomposition

$$u(x,y) = \bar{u}(y) + u'(x,y)$$

### Time-Averaged (Streamwise-Averaged) Velocity

$$\bar{u}(y) = \langle u(x,y) \rangle_x = \frac{1}{N_x}\sum_{i=1}^{N_x} u(x_i,\,y)$$

### Velocity Fluctuation

$$u'(x,y) = u(x,y) - \bar{u}(y)$$

By construction, $\langle u' \rangle_x = 0$ at every wall-normal position $y$.

## Implementation

1. Create a 200×60 mesh of $(x, y)$ coordinates.
2. Evaluate the synthetic velocity field using the sine-cosine formula plus Gaussian noise.
3. Compute the streamwise mean $\bar{u}(y)$ by averaging over all $x$ at each $y$.
4. Subtract the mean to obtain the fluctuation field $u'(x,y)$.
5. Plot the instantaneous field as a filled colour map and the mean profile as a line plot.

## Output

The script displays two panels: a 2D colour map of the instantaneous velocity field and a 1D line plot of the time-averaged profile $\bar{u}(y)$. The comparison clearly shows how the mean captures the large-scale structure while the fluctuations represent turbulent content.

![output(8)](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/de29d473-ec6c-4376-91a8-5653bb1b80ff)
