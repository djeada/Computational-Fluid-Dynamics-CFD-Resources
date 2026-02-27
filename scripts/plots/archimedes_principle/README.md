# Archimedes' Principle Visualisation

This script provides an interactive visualisation of Archimedes' principle by computing and displaying the gravitational weight and buoyant force acting on a submerged object. Given the object density, fluid density, and object volume, it calculates both forces and renders a diagram showing the object either floating or sinking, with annotated force arrows indicating the magnitude and direction of each force. The visualisation makes the balance—or imbalance—between weight and buoyancy immediately apparent.

## Overview

- Accepts object density, fluid density (default 1000 kg/m³), and object volume (default 1 m³) as inputs
- Computes gravitational weight $W$ and buoyant force $F_b$ from first principles
- Determines whether the object floats or sinks based on the density ratio
- Renders labeled force arrows for both weight and buoyancy on a fluid diagram
- Annotates numerical force values and the floating/sinking outcome

## Mathematical Background

### Gravitational Weight

The downward gravitational force on the object is:

$$W = \rho_{\text{obj}}\, V\, g$$

where $\rho_{\text{obj}}$ is the object density (kg/m³), $V$ is the object volume (m³), and $g = 9.81$ m/s² is gravitational acceleration.

### Buoyant Force

By Archimedes' principle, the upward buoyant force equals the weight of displaced fluid:

$$F_b = \rho_{\text{fluid}}\, V\, g$$

### Floating Condition

The object floats when the buoyant force is at least equal to its weight:

$$F_b \geq W \iff \rho_{\text{obj}} \leq \rho_{\text{fluid}}$$

When $\rho_{\text{obj}} > \rho_{\text{fluid}}$ the net downward force $W - F_b > 0$ and the object sinks.

## Implementation

1. Accept `object_density`, `fluid_density`, and `object_volume` as parameters.
2. Compute $W = \rho_{\text{obj}} \cdot V \cdot g$ and $F_b = \rho_{\text{fluid}} \cdot V \cdot g$.
3. Compare the two forces to classify the outcome as floating or sinking.
4. Draw a rectangular fluid region and place the object at the appropriate vertical position.
5. Render downward arrow for $W$ and upward arrow for $F_b$, scaled to their relative magnitudes.
6. Label each arrow with its numerical value and annotate the floating/sinking verdict.

## Output

The script produces a figure depicting the fluid container with the object partially or fully submerged. Two annotated arrows show the gravitational weight pointing downward and the buoyant force pointing upward. The title or annotation states whether the object floats or sinks, and the force magnitudes are printed alongside each arrow.

![archimedes_principle](https://github.com/user-attachments/assets/e776665c-a2c8-4220-9f31-dcfc4d3bae12)
