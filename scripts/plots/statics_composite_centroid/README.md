# Composite Centroid

This script computes the centroids of a T-section and of a plate with a hole and a notch from a table of parts, checks them against the polygon formula for the exact boundary, and gives the centroidal second moment of the T-section. Holes and cut-outs enter the parts table with negative area, which is the standard hand method; the polygon check integrates the actual boundary with Green's theorem.

## Overview

- T-section: a $120 \times 20$ mm flange on a $20 \times 80$ mm web. Computes the area, the centroid height and $I_x$ about the centroidal axis with the parallel-axis theorem.
- Plate: a $200 \times 120$ mm rectangle with a semicircular end of radius 60 mm, a 40 mm hole at the centre of the semicircle and a right-triangular notch with 60 mm legs cut from the lower-left corner.
- Prints the parts table and compares its centroid with the centroid of the boundary polygon, whose arcs are divided into 4000 segments.
- Draws both shapes with the parts shaded, negative parts hatched, part centroids as dots and the composite centroid as a cross.

## Mathematical Background

For parts with signed areas $A_i$ and centroids $(\bar{x}_i, \bar{y}_i)$:

```math
\bar{x} = \frac{\sum_i A_i\bar{x}_i}{\sum_i A_i}, \qquad \bar{y} = \frac{\sum_i A_i\bar{y}_i}{\sum_i A_i}, \qquad
I_x = \sum_i \left[I_{c,i} + A_i(\bar{y}_i - \bar{y})^2\right]
```

For a polygon with vertices $(x_k, y_k)$ listed counter-clockwise and $a_k = x_k y_{k+1} - x_{k+1}y_k$, Green's theorem gives

```math
A = \frac{1}{2}\sum_k a_k, \qquad
\bar{x} = \frac{1}{6A}\sum_k (x_k + x_{k+1})\,a_k, \qquad
\bar{y} = \frac{1}{6A}\sum_k (y_k + y_{k+1})\,a_k
```

The plate's centroid is the area-weighted combination of the outer polygon and the hole polygon, with the hole subtracted.

## Implementation

- `composite_centroid(parts)` returns $(A, \bar{x}, \bar{y})$ from rows whose first three entries are area and centroid.
- `polygon_centroid(vertices)` implements the shoelace formulas.
- `t_section_parts()` and `plate_parts()` return the parts tables; `second_moment(parts, y_bar)` applies the parallel-axis theorem.
- `plate_boundary()` builds the outer and hole polygons and `plate_centroid_exact()` combines them.
- `make_figure()` draws the two panels; constants `FLANGE`, `WEB`, `PLATE`, `HOLE_DIAMETER`, `NOTCH_LEG` and `ARC_POINTS` set the geometry in mm.

## Usage

```bash
python main.py                          # print the tables and show the figure
python main.py --no-show --output .     # save statics_composite_centroid.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The T-section has $A = 4000$ mm², $\bar{y} = 70.00$ mm above the bottom of the web and $`I_x = 3\,333\,333`$ mm⁴. The plate's parts table gives $`A = 26\,598.2`$ mm² and the centroid $(127.364, 62.707)$ mm, the same to all printed digits as the boundary polygon.

![T-section and plate with part and composite centroids](statics_composite_centroid.png)

## Related Notes

- [Center of Mass and Centroids](../../../notes/applied_mechanics/statics/center_of_mass.md)
- [Rigid Body Equilibrium](../../../notes/applied_mechanics/statics/rigid_body_equilibrium.md)
