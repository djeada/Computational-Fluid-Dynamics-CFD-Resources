# Flow Rate Through a Circular Pipe

This script computes the volumetric flow rate $Q = \pi r^2 v$ of a circular pipe and draws a labelled side view of the pipe with flow arrows. It takes the pipe radius, a uniform (plug) velocity, and the pipe length. From these it computes the cross-sectional area and flow rate and lists all of them on the diagram. It is meant as an introductory illustration of flow rate and continuity.

## Overview

- Takes the pipe radius $r$ (0.1 m), velocity $v$ (2 m/s), and length $L$ (5 m) as function arguments
- Computes the cross-sectional area $A = \pi r^2$ and the flow rate $Q = A\,v$
- Draws the pipe as a grey rectangle of height $2r$ and length $L$, labelled "Inlet" and "Outlet" at its ends
- Fills the pipe with a grid of blue arrows (8 columns × 5 rows) whose length is proportional to $v$
- Lists $r$, $L$, $v$, $A$, and $Q$ in a text block below the pipe

## Mathematical Background

### Cross-Sectional Area

$$
A = \pi r^2
$$

### Volumetric Flow Rate

$$
Q = A\, v = \pi r^2 v \quad [\text{m}^3/ \text{s}]
$$

For the defaults, $A = \pi (0.1)^2 = 0.0314\ \text{m}^2$ and $Q = 0.0628\ \text{m}^3/\text{s}$.

### Uniform Velocity Assumption

The script treats $v$ as the same across the whole section:

$$
u(r') = v \quad \text{for } 0 \le r' \le r
$$

For a real, non-uniform profile the same formula holds if $v$ is the area-averaged velocity $\bar{u} = \frac{1}{A}\int_A u\, dA$. A laminar Hagen–Poiseuille profile, for example, has $\bar{u} = u_{\max}/2$. If the density $\rho$ is known, the mass flow rate is $\dot{m} = \rho Q$; the script does not compute it.

## Implementation

- `flow_rate(pipe_radius, velocity)` returns `(area, Q)`.
- `plot_flow_rate(pipe_radius, velocity, length)` draws the pipe with `plt.Rectangle` and the arrows with `ax.annotate`, each of length `velocity * ARROW_TIME` (`ARROW_TIME = 0.2` s). It also adds the inlet and outlet labels and the text block, and returns the figure.
- `main(argv=None)` handles the flags; the defaults are the constants `PIPE_RADIUS`, `VELOCITY`, and `PIPE_LENGTH`.

## Usage

```bash
python main.py                          # open the figure window
python main.py --no-show --output out   # save flow_rate_pipe.png into out/
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

A side view of the pipe (axes hidden, equal scale) with rows of identical blue arrows pointing from inlet to outlet. Below the pipe, the text block reads $r = 0.1$ m, $L = 5$ m, $v = 2$ m/s, $A = 0.0314\ \text{m}^2$, and $Q = 0.0628\ \text{m}^3/\text{s}$.

![Flow rate through a pipe](flow_rate_pipe.png)

## Related Notes

- [Pipe Flow](../../../notes/fluid_mechanics/internal_flow/pipes.md)
- [Continuity Equation](../../../notes/fluid_mechanics/governing_equations/continuity.md)
