# Froude Number vs. Flow Velocity

This script plots the Froude number as a function of flow velocity for four different hull lengths (L = 5, 10, 15, and 20 m). The Froude number is a dimensionless parameter central to naval architecture and open-channel hydraulics, governing whether gravity waves travel faster or slower than the flow. By visualising multiple hull lengths on the same axes, the plot highlights how larger vessels reach the hull-speed regime at higher absolute velocities.

## Overview

- Computes Froude number over a range of velocities for L = 5, 10, 15, 20 m
- Draws a horizontal reference line at Fr = 0.4 (practical hull-speed limit)
- Annotates sub-critical (Fr < 1) and super-critical (Fr > 1) regimes
- Uses distinct colours and a legend to differentiate each hull length
- Axes are labelled with physical units; grid is enabled for readability

## Mathematical Background

### Froude Number Definition

$$Fr = \frac{U}{\sqrt{gL}}$$

where $U$ is the flow velocity (m/s), $g = 9.81$ m/s$^2$ is gravitational acceleration, and $L$ is the characteristic hull length (m).

### Flow Regimes

$$Fr < 1 \quad \text{sub-critical: gravity waves propagate faster than the flow}$$

$$Fr > 1 \quad \text{super-critical: bow wave forms, wave drag rises sharply}$$

### Hull Speed

Naval architects target an economic operating point near:

$$Fr \approx 0.4$$

Beyond this, wave-making resistance increases rapidly with speed.

## Implementation

1. Define velocity array `U = np.linspace(0, 20, 200)` in m/s.
2. For each hull length L in {5, 10, 15, 20}, compute `Fr = U / sqrt(g * L)`.
3. Plot Fr vs. U for each L with a unique colour and label.
4. Add a horizontal dashed line at Fr = 0.4 labelled "Hull speed".
5. Shade or annotate the sub-critical (Fr < 1) and super-critical (Fr > 1) regions.
6. Set axis labels, title, legend, and grid; display the figure.

## Output

The script displays a single figure with four curves of Froude number versus velocity. A dashed reference line at Fr = 0.4 marks the practical hull-speed limit. The plot makes clear that shorter hulls reach super-critical conditions at much lower speeds than longer hulls.
