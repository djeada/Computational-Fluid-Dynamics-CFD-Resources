"""Schematic of the CFD surrogate-modelling workflow used in the automotive notes.

Draws eight boxes (design space and design of experiments, geometry morphing,
meshing, CFD, post-processing, training, validation, deployment) coloured by
stage (data generation, learning, deployment), connects them with arrows and
adds the active-learning feedback arrow from deployment back to the design of
experiments. Each box is labelled with the note that covers that step.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Stage name -> (fill colour, edge colour); edges are tab10 blue/orange/green.
STAGES = {
    "data generation": ("#d6e6f4", "#1f77b4"),
    "learning": ("#fde3c8", "#ff7f0e"),
    "deployment": ("#d5ecd4", "#2ca02c"),
}

BOX_W, BOX_H = 3.6, 1.6  # box size in axes units
ROW_Y = (3.8, 0.9)  # centre heights of the top and bottom rows
COL_X = (2.0, 6.2, 10.4, 14.6)  # centre positions of the four columns

# (title, detail line, note file, stage, column, row); the order is the flow.
STEPS = [
    ("1. Design space & DoE", "parameter ranges, LHS / Sobol", "deformation_parameters.md", "data generation", 0, 0),
    ("2. Geometry morphing", "FFD / RBF on baseline CAD", "deformation_parameters.md", "data generation", 1, 0),
    ("3. Meshing", "surface and volume mesh", "dataset_of_meshes.md", "data generation", 2, 0),
    ("4. CFD", "RANS or hybrid RANS-LES", "generating_cfd_datasets.md", "data generation", 3, 0),
    ("5. Post-processing", r"$C_d$, $C_p$, fields $\to$ dataset", "output_data.md, datasets.md", "data generation", 3, 1),
    ("6. Training", r"fit $f_{\theta}$ on training designs", "model_training.md", "learning", 2, 1),
    ("7. Validation", r"held-out designs, MAE, $R^2$", "training_and_validation.md", "learning", 1, 1),
    ("8. Deployment", "optimisation, screening", "ml_process.md", "deployment", 0, 1),
]  # fmt: skip


def box_centre(step):
    *_, col, row = step
    return COL_X[col], ROW_Y[row]


def draw_box(ax, step):
    title, detail, note, stage, *_ = step
    x, y = box_centre(step)
    fill, edge = STAGES[stage]
    ax.add_patch(
        FancyBboxPatch(
            (x - BOX_W / 2, y - BOX_H / 2),
            BOX_W,
            BOX_H,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            facecolor=fill,
            edgecolor=edge,
            linewidth=2,
        )
    )
    ax.text(x, y + 0.38, title, ha="center", va="center", fontsize=13, weight="bold")
    ax.text(x, y + 0.0, detail, ha="center", va="center", fontsize=11)
    ax.text(
        x,
        y - 0.42,
        note,
        ha="center",
        va="center",
        fontsize=10,
        family="monospace",
        color=edge,
    )


def arrow(ax, start, end, **kwargs):
    style = {"arrowstyle": "-|>", "mutation_scale": 18, "lw": 2, "color": "0.25"}
    style.update(kwargs)
    ax.add_patch(FancyArrowPatch(start, end, **style))


def connect(ax, a, b):
    """Arrow from the edge of box a to the facing edge of box b."""
    (xa, ya), (xb, yb) = box_centre(a), box_centre(b)
    if ya == yb:
        sign = 1 if xb > xa else -1
        arrow(ax, (xa + sign * BOX_W / 2, ya), (xb - sign * BOX_W / 2, yb))
    else:
        sign = 1 if yb > ya else -1
        arrow(ax, (xa, ya + sign * BOX_H / 2), (xb, yb - sign * BOX_H / 2))


def make_figure():
    fig, ax = plt.subplots(figsize=(13, 5.2))
    for step in STEPS:
        draw_box(ax, step)
    for a, b in zip(STEPS[:-1], STEPS[1:]):
        connect(ax, a, b)

    # Active learning: deployment/validation feed new samples back to the DoE.
    (x8, y8), (x1, y1) = box_centre(STEPS[7]), box_centre(STEPS[0])
    arrow(
        ax,
        (x8 - BOX_W / 2, y8),
        (x1 - BOX_W / 2, y1),
        connectionstyle="arc3,rad=-0.5",
        color="#d62728",
        linestyle="--",
    )
    ax.text(
        x1 - BOX_W / 2 + 0.2,
        (y1 + y8) / 2,
        "active learning: add CFD samples where the\nmodel is uncertain or near the optimum",
        ha="left",
        va="center",
        fontsize=11,
        color="#d62728",
    )

    handles = [
        Patch(facecolor=fill, edgecolor=edge, linewidth=2, label=name)
        for name, (fill, edge) in STAGES.items()
    ]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=3,
        frameon=False,
        fontsize=11,
    )
    ax.set_xlim(-0.9, 16.5)
    ax.set_ylim(-0.0, 5.0)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    return create_parser(__doc__).parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    fig = make_figure()
    finish_figures(
        {"ml_cfd_workflow.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
