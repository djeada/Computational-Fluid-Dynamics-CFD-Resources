# ML-CFD Surrogate Workflow

This script draws a schematic of the workflow for building a machine-learning surrogate of CFD results, from the design of experiments to deployment in an optimisation loop. The eight steps are coloured by stage (data generation, learning, deployment), connected by arrows in the order they are carried out, and labelled with the note in `notes/machine_learning/` that covers each step. A dashed arrow from deployment back to the design of experiments marks the active-learning loop, in which new CFD samples are added where the model is uncertain or where the optimiser is searching.

## Overview

- Lists the eight steps in `STEPS`, each with a title, a one-line description, the covering note, a stage and a grid position.
- Draws each step as a rounded box (`matplotlib.patches.FancyBboxPatch`) filled and outlined in its stage colour.
- Connects consecutive steps with arrows: left to right along the top row, down the right-hand side and right to left along the bottom row.
- Adds the curved, dashed active-learning arrow and its label, and a legend of the three stages.

## Mathematical Background

The figure contains no computation. It summarises the surrogate-modelling problem treated in the automotive notes: given $N$ CFD solutions $`\mathcal{D} = \{(\mathbf{p}_i, \mathbf{y}_i)\}_{i=1}^N`$ for design parameters $`\mathbf{p}_i`$ chosen by a design of experiments, find a model $f_{\boldsymbol\theta}$ with $`f_{\boldsymbol\theta}(\mathbf{p}) \approx \mathbf{y}(\mathbf{p})`$ for new designs, where $`\mathbf{y}`$ holds force coefficients and surface or volume fields. Steps 1 to 5 produce $`\mathcal{D}`$, steps 6 and 7 fit and assess $`f_{\boldsymbol\theta}`$, and step 8 uses it in place of CFD.

## Implementation

- `STAGES` maps each stage to a light fill colour and a tab10 edge colour (blue, orange, green).
- `BOX_W`, `BOX_H`, `ROW_Y` and `COL_X` set the box size and the two-row, four-column layout.
- `draw_box(ax, step)` draws one box with its title, description and note name.
- `connect(ax, a, b)` draws a straight arrow between facing edges of two boxes; `arrow` wraps `FancyArrowPatch`.
- `make_figure()` assembles the boxes, arrows, feedback loop and legend on an axis without ticks.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Schematic of the CFD surrogate-modelling workflow, coloured by stage](ml_cfd_workflow.png)

Blue boxes produce the training data (design space, morphing, meshing, CFD, post-processing), orange boxes fit and test the model, and the green box uses it. The note file names in each box correspond to `notes/machine_learning/automotive_aerodynamics/` except `training_and_validation.md`, which is in `notes/machine_learning/fundamentals/`.

## Related Notes

- [Automotive Aerodynamics Case Study: Overview](../../../notes/machine_learning/automotive_aerodynamics/ml_process.md)
- [Deformation Parameters](../../../notes/machine_learning/automotive_aerodynamics/deformation_parameters.md)
- [Output Data](../../../notes/machine_learning/automotive_aerodynamics/output_data.md)
