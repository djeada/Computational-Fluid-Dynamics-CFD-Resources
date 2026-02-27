# Longitudinal Velocity Fluctuations and Projections

This script produces three plots from synthetic turbulent velocity fluctuation data. The first shows time series of two fluctuating velocity components $u'_a(t)$ and $u'_b(t)$. The second is a scatter plot of the joint $(u'_a, u'_b)$ data cloud, revealing the statistical structure of the turbulence. The third overlays the data cloud with its projection onto a unit vector $\boldsymbol{\phi} = (0.894, 0.447)$, illustrating the Proper Orthogonal Decomposition (POD) concept of extracting the most energetic mode.

![Figure_1](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/8714451d-6864-40f3-9abd-c2e11ba4c9b8)

![Figure_2](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/75d6ea38-85f5-4fb8-896f-c4e684b5f890)

![Figure_3](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/b0e26fc6-7aaa-4b10-9d28-2d405197af2c)

## Overview

- Time series of two synthetic velocity fluctuations $u'_a(t)$ and $u'_b(t)$
- Scatter plot of the joint $(u'_a, u'_b)$ data cloud representing the joint PDF
- Projection of the data cloud onto a chosen unit direction vector $\boldsymbol{\phi}$
- Motivates POD as the optimal basis for representing turbulent kinetic energy

## Mathematical Background

### Reynolds Decomposition

Any instantaneous velocity is decomposed into a time-mean and a fluctuation:

$$u = \bar{u} + u', \qquad \bar{u'} = 0$$

### Joint Velocity Statistics

The scatter of $(u'_a, u'_b)$ samples approximates the joint probability density function $P(u'_a, u'_b)$. The shape of the cloud encodes correlations between the two components.

### Projection onto a Direction

The scalar projection of each data point $\mathbf{u}'_i = (u'_{a,i},\, u'_{b,i})$ onto unit vector $\boldsymbol{\phi} = (\phi_1, \phi_2)$ is:

$$p_i = \mathbf{u}'_i \cdot \boldsymbol{\phi} = u'_{a,i}\phi_1 + u'_{b,i}\phi_2$$

### Proper Orthogonal Decomposition (POD)

In POD, the optimal direction $\boldsymbol{\phi}$ maximises the projected variance and is the leading eigenvector of the covariance matrix $\mathbf{C}$:

$$\mathbf{C} = \frac{1}{N}\sum_{i=1}^{N}\mathbf{u}'_i \mathbf{u}^{\prime\top}_i, \qquad \mathbf{C}\boldsymbol{\phi} = \lambda\boldsymbol{\phi}$$

## Implementation

1. Generate synthetic time series $u'_a(t)$ and $u'_b(t)$ using correlated Gaussian noise.
2. Plot both time series on a shared time axis (Figure 1).
3. Scatter-plot the $(u'_a, u'_b)$ pairs to visualise the data cloud (Figure 2).
4. Compute scalar projections $p_i$ onto $\boldsymbol{\phi} = (0.894, 0.447)$ and overlay the projection axis on the scatter plot (Figure 3).
5. Save all three figures.

## Output

The script produces three figures: (1) velocity fluctuation time series, (2) the joint $(u'_a, u'_b)$ scatter cloud, and (3) the same cloud annotated with the unit projection vector and the projected data distribution, illustrating the POD principle of variance maximisation.

