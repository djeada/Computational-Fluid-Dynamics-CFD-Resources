# Maxwell-Boltzmann Speed Distribution of N₂ Molecules

This script plots the Maxwell-Boltzmann speed distribution function for nitrogen (N₂) molecules at four temperatures: 300 K, 600 K, 900 K, and 1200 K. It illustrates how increasing temperature broadens the distribution and shifts the most probable speed to higher values, providing a kinetic-theory foundation for understanding molecular transport in CFD applications.

## Overview

- Evaluates the Maxwell-Boltzmann probability density function over a speed range of 0–2000 m/s
- Plots four overlaid distribution curves, one per temperature
- Marks the most probable speed, mean speed, and RMS speed for each temperature
- Uses N₂ molecular mass $m = 4.65\times10^{-26}$ kg and Boltzmann constant $k_B = 1.38\times10^{-23}$ J/K

## Mathematical Background

### Maxwell-Boltzmann Distribution

$$f(v) = 4\pi\left(\frac{m}{2\pi k_B T}\right)^{3/2} v^2 \exp\!\left(-\frac{mv^2}{2k_BT}\right)$$

### Characteristic Speeds

### Most Probable Speed

$$v_p = \sqrt{\frac{2k_BT}{m}}$$

### Mean Speed

$$\bar{v} = \sqrt{\frac{8k_BT}{\pi m}}$$

### Root-Mean-Square Speed

$$v_{rms} = \sqrt{\frac{3k_BT}{m}}$$

### Molecular Parameters for N₂

$$m = 4.65\times10^{-26}\ \text{kg}, \quad k_B = 1.38\times10^{-23}\ \text{J/K}$$

## Implementation

1. Define molecular mass and Boltzmann constant for N₂.
2. Create a speed array from 0 to 2000 m/s with fine resolution.
3. For each temperature (300, 600, 900, 1200 K), evaluate $f(v)$ using the Maxwell-Boltzmann formula.
4. Compute $v_p$, $\bar{v}$, and $v_{rms}$ for each temperature and mark them on the plot.
5. Overlay all four curves on a single axes with a legend indicating temperature.

## Output

The script displays a single figure with four Maxwell-Boltzmann curves coloured by temperature. Vertical markers indicate the most probable, mean, and RMS speeds for each case. The plot demonstrates that higher temperatures yield broader, flatter distributions and greater characteristic speeds.

![probability_distribution_function](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/9821d7ff-d499-45a9-8fdd-3e4d73e6efb9)
