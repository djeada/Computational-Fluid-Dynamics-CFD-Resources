# Archimedes' Principle Visualisation

This script draws a block in a tank of fluid with its weight and buoyant force shown as arrows, and states whether the block floats or sinks according to Archimedes' principle. From the object density, fluid density and object volume it computes both forces, places a floating block at its equilibrium depth, and scales the arrows to the force magnitudes.

## Overview

- Takes the object density (default 500 kg/m$`^3`$), fluid density (default 1000 kg/m$`^3`$) and object volume (default 1 m$`^3`$) as command-line options.
- Computes the weight $W$ and decides whether the block floats by comparing $W$ with the buoyant force on the fully submerged block.
- Floating block: drawn with the submerged fraction $\rho_{\text{obj}}/\rho_{\text{fluid}}$ below the surface, where the buoyant force equals the weight.
- Sinking block: drawn fully submerged at a fixed depth, with the buoyant force of the whole volume.
- Draws an upward buoyant-force arrow from the top of the block and a downward weight arrow from its bottom. The arrow lengths are proportional to the forces, and each label gives the value in newtons.
- Prints the verdict on the figure: floats (with the submerged percentage) or sinks.

## Mathematical Background

### Weight

```math
W = \rho_{\text{obj}}\, V\, g,
\qquad g = 9.81\ \text{m/s}^2
```

### Buoyant Force

The buoyant force equals the weight of the displaced fluid:

```math
F_b = \rho_{\text{fluid}}\, V_{\text{sub}}\, g
```

where $V_{\text{sub}}$ is the submerged volume.

### Floating Condition

When fully submerged, $F_b = \rho_{\text{fluid}} V g$. The object floats if this is at least its weight:

$$
\rho_{\text{fluid}} V g \geq W \iff \rho_{\text{obj}} \leq \rho_{\text{fluid}}
$$

A floating object settles where $F_b = W$, so its submerged fraction is

$$
\frac{V_{\text{sub}}}{V} = \frac{\rho_{\text{obj}}}{\rho_{\text{fluid}}}
$$

If $\rho_{\text{obj}} > \rho_{\text{fluid}}$, the net downward force $W - \rho_{\text{fluid}} V g$ is positive and the object sinks.

## Implementation

- `buoyancy_state(object_density, fluid_density, object_volume, g)` returns `(weight, buoyant_force, floats, submerged_fraction)`.
- `plot_archimedes_principle(object_density, fluid_density, object_volume)` draws the tank and block with `matplotlib.patches.Rectangle`, the scaled force arrows with `annotate`, and the verdict text.
- The drawing constants `TANK_WIDTH`, `WATER_DEPTH`, `OBJECT_SIZE`, `SUNK_POSITION` and `MAX_ARROW` are in drawing units. The block is not drawn to scale with $V$.

## Usage

```bash
python main.py                                  # 500 kg/m^3 block in water: floats
python main.py --object-density 2700            # aluminium block: sinks
python main.py --fluid-density 1025 --object-volume 0.5
python main.py --no-show --output .             # save the figure as a PNG in the current directory
```

## Output

![Floating block with weight and buoyant force arrows](archimedes_principle.png)

With the defaults the block is half submerged. The buoyant force and the weight are both 4,905 N, so the arrows have equal length. With `--object-density 2700` the block is drawn fully submerged, with a weight of 26,487 N and a buoyant force of 9,810 N.

## Related Notes

- [Hydrostatics](../../../notes/fluid_mechanics/fluid_statics/hydrostatics.md)
