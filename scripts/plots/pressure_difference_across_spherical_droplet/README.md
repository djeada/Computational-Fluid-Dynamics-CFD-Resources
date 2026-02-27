# Pressure Difference Across a Spherical Droplet

This script visualises the Young-Laplace pressure difference across a spherical droplet by drawing an annotated circle diagram. The interior of the droplet is labelled with the higher pressure $p_{in}$ and the exterior with $p_{out}$, and the governing equation $\Delta p = 2\sigma/R$ is displayed prominently. The visualisation conveys the physical intuition that surface tension creates a pressure jump at the interface, with smaller droplets producing larger pressure differences.

## Overview

- Draws a filled circle representing the spherical droplet cross-section
- Annotates interior and exterior regions with pressure labels
- Displays the Young-Laplace formula as a text annotation on the figure
- Shows a representative radius arrow with the symbol R
- Highlights the inverse relationship between droplet size and pressure jump

## Mathematical Background

### Young-Laplace Equation for a Sphere

$$\Delta p = p_{in} - p_{out} = \frac{2\sigma}{R}$$

where $\sigma$ is the surface tension of the liquid (N/m) and $R$ is the droplet radius (m).

### Surface Tension of Water

At room temperature (~20 °C):

$$\sigma_{\text{water}} \approx 0.0728 \text{ N/m}$$

### Pressure–Radius Relationship

$$\Delta p \propto \frac{1}{R}$$

Halving the droplet radius doubles the pressure difference across the interface, which is why small aerosol droplets sustain very large internal pressures.

## Implementation

1. Create a matplotlib figure with equal-aspect axes and no tick marks.
2. Draw a filled circle (patch) to represent the droplet; colour the interior distinctly.
3. Add a text label "$p_{in}$" at the centre and "$p_{out}$" outside the circle.
4. Draw an arrow from the centre to the edge and label it $R$.
5. Annotate the figure with the formula $\Delta p = 2\sigma/R$ in a prominent position.
6. Set the title, remove axis spines, and display the figure.

## Output

The script displays a schematic diagram of a spherical droplet with clearly annotated internal and external pressure regions and the Young-Laplace formula. The figure serves as a concise visual reference for the pressure jump caused by surface tension and its dependence on droplet radius.
