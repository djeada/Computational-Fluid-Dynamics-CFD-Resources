# Turbulent Flow — Reynolds Decomposition Visualisation

This script generates a synthetic turbulent velocity signal, decomposes it into mean and fluctuating parts via the Reynolds decomposition, and presents three linked subplots that illuminate the statistical structure of turbulence. It provides a hands-on demonstration of key turbulence quantities used in CFD modelling.

## Overview

- Generates a synthetic signal $u(t) = \sin(t) + \text{Gaussian noise}$
- Computes the time-mean $\bar{u}$ and the fluctuation $u'(t) = u(t) - \bar{u}$
- Produces three vertically stacked subplots: velocity, fluctuation, and squared fluctuation
- Annotates turbulence intensity and turbulent kinetic energy contribution

## Mathematical Background

### Reynolds Decomposition

$$u(t) = \bar{u} + u'(t)$$

### Time Mean

$$\bar{u} = \frac{1}{T}\int_0^T u\,dt$$

### Turbulence Intensity

$$Tu = \frac{u_{rms}}{U_0}, \qquad u_{rms} = \sqrt{\langle u'^2 \rangle}$$

### Turbulent Kinetic Energy (1D Component)

$$k = \frac{1}{2}\langle u'^2 \rangle$$

This represents the contribution of the measured velocity component to the total TKE per unit mass.

## Implementation

1. Define a time vector and generate the synthetic velocity signal with added random noise.
2. Compute the temporal mean $\bar{u}$ over the entire signal.
3. Subtract the mean to obtain the fluctuation $u'(t)$.
4. Square the fluctuation to obtain $u'^2(t)$.
5. Plot all three quantities ($u$, $u'$, $u'^2$) on separate, vertically aligned subplots sharing the time axis.

## Output

The script displays a three-panel figure. The top panel shows the raw velocity signal with the mean indicated, the middle panel shows the zero-mean fluctuation, and the bottom panel shows the squared fluctuation whose average equals twice the 1D TKE contribution.

![Turbulence Modeling](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/84461e4c-8c1a-44c3-a8f6-af1ed51fd49e)
