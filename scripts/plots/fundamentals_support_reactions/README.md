# Support Reactions in 2D

This script draws the standard planar supports and connections next to the reactions they exert on a body, as a reference chart for drawing free-body diagrams. Each cell shows a support as it appears on a space diagram, and the same body after the support has been removed and replaced by its unknown forces and couples, with the number of unknowns in the caption.

## Overview

- Covers eight supports: cable, weightless link, roller, smooth surface, pinned collar on a smooth rod, smooth pin or hinge, fixed collar on a smooth rod, and fixed support.
- Stores each support's name, reaction symbols and a one-line description in `SUPPORTS`; the captions and the printed table are generated from it.
- Draws every support with matplotlib patches (rectangles, circles, polygons and hatched ground lines) and the reactions as red arrows and curved moment arrows.
- Prints the number of unknowns for each support.

## Mathematical Background

A support prevents certain motions of the body it holds, and it does so by exerting a force in each direction of translation it prevents and a couple about each axis of rotation it prevents. In a plane a rigid body has three degrees of freedom (two translations and one rotation), so a support contributes one, two or three unknowns:

| Support | Prevents | Reactions | Unknowns |
| --- | --- | --- | --- |
| Cable | Motion away from the anchor along the cable | Tension $T$ along the cable, pulling | 1 |
| Weightless link | Motion along the link | Force along the link, sense unknown | 1 |
| Roller, smooth surface, pinned collar on smooth rod | Motion normal to the surface or rod | Normal force | 1 |
| Smooth pin or hinge | Both translations | $A_x$, $A_y$ | 2 |
| Fixed collar on smooth rod | Motion normal to the rod and rotation | Normal force and couple $M$ | 2 |
| Fixed support | Both translations and rotation | $A_x$, $A_y$, $M_A$ | 3 |

The reactions from all supports, together with the three equilibrium equations, decide whether a planar body is statically determinate.

## Implementation

- `SUPPORTS` holds `(key, name, reactions, description)` for each support and `unknown_count(key)` returns the number of reaction components.
- `DRAWERS` maps each key to a drawing function (`draw_cable`, `draw_link`, `draw_roller`, `draw_smooth`, `draw_collar`, `draw_pin`, `draw_fixed`); the fixed collar reuses `draw_collar(ax, fixed=True)`.
- Helpers `ground`, `wall`, `beam`, `pin_symbol`, `arrow` and `moment_arrow` draw the common parts. `OFFSET` places the free-body sketch to the right of the support sketch in each cell.
- `make_figure` lays out the eight cells on a 4 × 2 grid.

## Usage

```bash
python main.py                          # print the table and show the chart
python main.py --no-show --output .     # save fundamentals_support_reactions.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints one line per support, for example `Smooth pin or hinge  2 unknown(s): A_x, A_y` and `Fixed support  3 unknown(s): A_x, A_y, M_A`.

![Standard 2D supports and their reactions](fundamentals_support_reactions.png)

In each cell the left sketch is the support and the right sketch is what goes on the free-body diagram. The arrow directions on the right are assumed senses; equilibrium gives the actual signs. The cable is the only support whose sense is known in advance, because a cable can only pull.

## Related Notes

- [Free-Body Diagrams](../../../notes/applied_mechanics/fundamentals/free_body_diagrams.md)
- [Force Systems and Resultants](../../../notes/applied_mechanics/fundamentals/force_systems.md)
