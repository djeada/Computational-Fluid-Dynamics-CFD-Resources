# Mesh Quality Assessment Guide

Mesh quality directly determines the accuracy, convergence, and stability of CFD simulations. A beautiful geometry with a poor mesh will produce unreliable results. This guide covers the metrics, tools, and workflows for assessing and improving mesh quality.

## Table of Contents

- [Why Mesh Quality Matters](#why-mesh-quality-matters)
- [Key Quality Metrics](#key-quality-metrics)
- [Assessment Tools](#assessment-tools)
- [OpenFOAM checkMesh In-Depth](#openfoam-checkmesh-in-depth)
- [Gmsh Quality Checks](#gmsh-quality-checks)
- [Visualizing Mesh Quality in ParaView](#visualizing-mesh-quality-in-paraview)
- [Automated Quality Reporting](#automated-quality-reporting)
- [Fixing Common Quality Problems](#fixing-common-quality-problems)
- [Quality Requirements by Application](#quality-requirements-by-application)

## Why Mesh Quality Matters

Poor mesh quality leads to:

- **Numerical diffusion** — smears out gradients and under-predicts flow features.
- **Solver divergence** — extremely skewed or inverted cells cause the solver to blow up.
- **Slow convergence** — low-quality cells force smaller time steps and more iterations.
- **Inaccurate results** — even if the solver converges, the solution may be far from the true answer.

A mesh that passes basic quality checks is a prerequisite — not a guarantee — of good results. Always combine quality checks with a mesh independence study.

## Key Quality Metrics

### Aspect Ratio

The ratio of the longest edge (or dimension) to the shortest in a cell.

```
Aspect Ratio = longest edge / shortest edge
```

| Range | Quality |
|-------|---------|
| 1–5 | Excellent |
| 5–20 | Good for most solvers |
| 20–100 | Acceptable in boundary layers (intentionally stretched) |
| > 100 | Problematic unless in structured BL regions |

High aspect ratios are expected and acceptable in boundary layer meshes where cells are deliberately thin in the wall-normal direction. In the bulk flow, high aspect ratios indicate problems.

### Skewness

Measures how far a cell deviates from its ideal shape (equilateral triangle, regular tetrahedron, etc.).

```
Skewness = (ideal_size - actual_size) / ideal_size
```

| Range | Quality |
|-------|---------|
| 0–0.25 | Excellent |
| 0.25–0.50 | Good |
| 0.50–0.75 | Acceptable |
| 0.75–0.85 | Poor (may cause convergence issues) |
| 0.85–1.00 | Unacceptable (will likely cause divergence) |

**Rule of thumb**: Keep maximum skewness below 0.85 for finite volume solvers.

### Non-Orthogonality

The angle between the line connecting two cell centers and the face normal vector between them.

```
Non-orthogonality = angle between face normal and cell-center connection
```

| Range | Quality |
|-------|---------|
| 0°–40° | Good (standard corrections sufficient) |
| 40°–65° | Requires non-orthogonal correction (increase `nNonOrthogonalCorrectors`) |
| 65°–85° | Poor (multiple correction steps needed, slow convergence) |
| > 85° | Severe (likely divergence) |

Non-orthogonality is the most common source of convergence problems in unstructured meshes.

### Cell Volume Ratio

The ratio of the largest neighboring cell volume to the smallest.

```
Volume Ratio = max(V_neighbor) / min(V_neighbor)
```

| Range | Quality |
|-------|---------|
| 1–5 | Good |
| 5–20 | Acceptable with care |
| > 20 | Will cause numerical errors at the interface |

**Rule of thumb**: Neighboring cells should not differ by more than a factor of 5 in volume, except in structured boundary layer regions where grading is intentional.

### Jacobian (Determinant)

The determinant of the Jacobian matrix of the element mapping. A positive Jacobian means the cell is valid; negative means it is inverted.

| Value | Meaning |
|-------|---------|
| > 0 | Valid cell |
| = 0 | Degenerate cell (zero volume) |
| < 0 | Inverted cell (inside-out) — **must be fixed** |

### Face Warpage

For non-planar faces (common in hexahedral meshes), warpage measures how far the face deviates from a flat plane.

| Range | Quality |
|-------|---------|
| < 5° | Good |
| 5°–30° | Acceptable |
| > 30° | May cause numerical errors |

## Assessment Tools

### OpenFOAM

```bash
# Basic check
checkMesh

# Comprehensive check (recommended)
checkMesh -allTopology -allGeometry

# Write quality fields for ParaView visualization
checkMesh -writeAllFields
```

### Gmsh

```bash
# Print mesh statistics
gmsh mesh.msh -info

# Check mesh quality
gmsh mesh.msh -check

# Open in GUI and check Tools → Statistics
gmsh mesh.msh
```

### ParaView

```
Filters → Alphabetical → Mesh Quality
```

Select the quality metric (aspect ratio, skewness, Jacobian, etc.) and visualize it as a color-mapped field.

### Python (meshio)

```python
import meshio
import numpy as np

mesh = meshio.read("mesh.msh")

# Basic statistics
print(f"Points: {len(mesh.points)}")
for cell_type, cells in mesh.cells:
    print(f"{cell_type}: {len(cells)} cells")
```

## OpenFOAM checkMesh In-Depth

### Running checkMesh

```bash
$ checkMesh -allTopology -allGeometry
```

### Interpreting Output

A typical checkMesh output looks like:

```
Checking geometry...
    Overall domain bounding box (0 0 0) (1 1 0.1)
    Mesh has 2 geometric (non-empty/wedge) directions (0 1 0)
    Mesh has 2 solution (non-empty) directions (0 1 0)
    All edges aligned with or perpendicular to non-empty directions.
    Boundary openness (1.23e-17 4.56e-18 -2.34e-17) OK.
    Max cell openness = 2.34e-16 OK.
    Max aspect ratio = 12.3 OK.
    Minimum face area = 4.56e-06. Maximum face area = 1.23e-04. OK.
    Min volume = 2.34e-08. Max volume = 6.78e-06. OK.
    Mesh non-orthogonality Max: 45.2 average: 12.3
    Non-orthogonality check OK.
    Face pyramids OK.
    Max skewness = 0.78 OK.
    Min/max face weight = 0.123 0.567 OK.
    Min/max face interpolation weight = 0.234 0.678 OK.
    Min determinant = 0.234. Max determinant = 0.987 OK.

Mesh OK.
```

### Key Lines to Watch

| Output | What It Means | Action If Bad |
|--------|---------------|---------------|
| `Max aspect ratio` | Highest cell stretch | > 1000: refine or restructure mesh |
| `Max skewness` | Worst cell distortion | > 0.85: remesh affected region |
| `Mesh non-orthogonality Max` | Worst face non-orthogonality | > 65: add non-orthogonal correctors |
| `***` markers | Severe quality issues | Must be fixed before solving |
| `Min determinant` | Lowest Jacobian determinant | < 0: inverted cells, must fix |
| `Face pyramids` | Cell convexity check | "FAILED": cells are non-convex |

### Writing Quality Fields

```bash
checkMesh -writeAllFields
```

This writes fields like `cellAspectRatio`, `faceNonOrthogonality`, `cellSkewness` etc. into the `0/` directory, which you can then open in ParaView to see exactly where the bad cells are.

## Gmsh Quality Checks

### In the GUI

1. After meshing, go to **Tools → Statistics**.
2. Review the element quality histogram.
3. Elements with quality < 0.1 (on Gmsh's 0–1 scale where 1 is perfect) need attention.

### Using the CLI

```bash
# Show detailed statistics
gmsh mesh.msh -info 2>&1 | grep -i "quality\|elements\|nodes"
```

### Post-Mesh Optimization

```bash
# Optimize tetrahedral mesh
gmsh mesh.msh -optimize -o optimized.msh

# Use Netgen optimizer (usually better)
gmsh mesh.msh -optimize_netgen -o optimized.msh

# Set optimization threshold (optimize elements worse than this)
gmsh -optimize_threshold 0.5 mesh.msh -o optimized.msh
```

### Python API Quality Query

```python
import gmsh

gmsh.initialize()
gmsh.open("mesh.msh")

# Get element quality (SICN metric by default)
element_types, element_tags, node_tags = gmsh.model.mesh.getElements(3)
for etype, etags in zip(element_types, element_tags):
    qualities = gmsh.model.mesh.getElementQualities(etags)
    print(f"Element type {etype}:")
    print(f"  Min quality: {min(qualities):.4f}")
    print(f"  Max quality: {max(qualities):.4f}")
    print(f"  Mean quality: {sum(qualities)/len(qualities):.4f}")
    print(f"  Elements below 0.1: {sum(1 for q in qualities if q < 0.1)}")

gmsh.finalize()
```

## Visualizing Mesh Quality in ParaView

### Step 1: Load Mesh Quality Fields

If using OpenFOAM:

```bash
checkMesh -writeAllFields
paraFoam
```

If using a standalone mesh file:

```
1. Open mesh in ParaView
2. Filters → Alphabetical → Mesh Quality
3. Select quality metric from the dropdown
4. Apply
```

### Step 2: Identify Problem Regions

- Use the **Threshold** filter to isolate cells with quality below your threshold.
- Color the mesh by the quality metric to see the spatial distribution.
- Use **Extract Selection** to select and examine individual bad cells.

### Useful ParaView Filters for Mesh Quality

| Filter | Use |
|--------|-----|
| **Mesh Quality** | Compute per-cell quality metrics |
| **Threshold** | Isolate cells by quality range |
| **Histogram** | Show distribution of quality values |
| **Extract Surface** | View only the surface mesh |
| **Feature Edges** | Highlight sharp edges and non-manifold geometry |
| **Shrink** | Shrink cells to see individual elements |

## Automated Quality Reporting

### Python Script for Mesh Quality Report

```python
#!/usr/bin/env python3
"""
Generate a mesh quality report from OpenFOAM checkMesh output.
"""

import re
import sys

def parse_checkmesh(log_file):
    """Parse checkMesh output and extract metrics."""
    report = {}

    with open(log_file, 'r') as f:
        content = f.read()

    # Extract key metrics
    patterns = {
        'cells': r'cells:\s+(\d+)',
        'faces': r'faces:\s+(\d+)',
        'points': r'points:\s+(\d+)',
        'max_aspect_ratio': r'Max aspect ratio = ([\d.e+-]+)',
        'max_skewness': r'Max skewness = ([\d.e+-]+)',
        'max_non_ortho': r'non-orthogonality Max: ([\d.e+-]+)',
        'avg_non_ortho': r'non-orthogonality.*average: ([\d.e+-]+)',
        'min_volume': r'Min volume = ([\d.e+-]+)',
        'max_volume': r'Max volume = ([\d.e+-]+)',
        'min_determinant': r'Min determinant = ([\d.e+-]+)',
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            report[key] = match.group(1)

    # Check for failures
    report['failed'] = '***' in content
    report['mesh_ok'] = 'Mesh OK' in content

    return report

def print_report(report):
    """Print formatted quality report."""
    print("=" * 50)
    print("MESH QUALITY REPORT")
    print("=" * 50)

    print(f"\nMesh size:")
    print(f"  Cells:  {report.get('cells', 'N/A')}")
    print(f"  Faces:  {report.get('faces', 'N/A')}")
    print(f"  Points: {report.get('points', 'N/A')}")

    print(f"\nQuality metrics:")
    print(f"  Max aspect ratio:      {report.get('max_aspect_ratio', 'N/A')}")
    print(f"  Max skewness:          {report.get('max_skewness', 'N/A')}")
    print(f"  Max non-orthogonality: {report.get('max_non_ortho', 'N/A')}°")
    print(f"  Avg non-orthogonality: {report.get('avg_non_ortho', 'N/A')}°")
    print(f"  Min cell volume:       {report.get('min_volume', 'N/A')}")
    print(f"  Min determinant:       {report.get('min_determinant', 'N/A')}")

    print(f"\nOverall: {'PASS ✓' if report.get('mesh_ok') else 'FAIL ✗'}")

    if report.get('failed'):
        print("  WARNING: checkMesh reported severe issues (***)")

    print("=" * 50)

if __name__ == "__main__":
    log_file = sys.argv[1] if len(sys.argv) > 1 else "log.checkMesh"
    report = parse_checkmesh(log_file)
    print_report(report)
```

Usage:

```bash
checkMesh > log.checkMesh 2>&1
python3 mesh_quality_report.py log.checkMesh
```

## Fixing Common Quality Problems

### High Skewness

| Cause | Fix |
|-------|-----|
| Poor surface mesh transitions | Improve surface mesh grading |
| Complex geometry corners | Add local refinement or smooth geometry |
| Automatic mesher artifacts | Try different meshing algorithm or adjust parameters |

### High Non-Orthogonality

| Cause | Fix |
|-------|-----|
| Unstructured tets on curved surfaces | Refine mesh; use hex-dominant meshing |
| Large cell size transitions | Reduce growth ratio between zones |
| Boundary layer meeting bulk mesh | Improve BL-to-bulk transition |

**Short-term workaround** in OpenFOAM:

```cpp
// system/fvSolution
SIMPLE
{
    nNonOrthogonalCorrectors 2;  // Increase to 2-3 for non-orthogonal meshes
}
```

### Inverted Cells (Negative Volume)

This is a critical failure — the mesh cannot be used.

| Cause | Fix |
|-------|-----|
| snappyHexMesh layer addition failure | Relax layer settings; reduce nLayers |
| Boolean operation artifacts | Increase geometry tolerance; heal CAD model |
| Extrusion through tight spaces | Reduce BL thickness or number of layers |

### Large Volume Ratio

| Cause | Fix |
|-------|-----|
| Refinement region boundaries | Add buffer zones with intermediate sizing |
| Mesh hanging nodes | Use proper refinement (not ad-hoc splitting) |

## Quality Requirements by Application

### By Solver Type

| Application | Max Skewness | Max Non-Ortho | Max Aspect Ratio | Notes |
|-------------|-------------|---------------|-------------------|-------|
| OpenFOAM (general) | < 0.85 | < 65° | < 1000 | Add non-ortho correctors > 40° |
| OpenFOAM (LES) | < 0.50 | < 40° | < 100 | Stricter for accuracy |
| SU2 | < 0.90 | N/A | < 1000 | More tolerant of skewed cells |
| FEniCS/deal.II (FEM) | < 0.60 | N/A | < 50 | FEM is more sensitive to distortion |

### By Physics

| Physics | Key Requirement |
|---------|----------------|
| Boundary layers | High aspect ratio OK (stretched cells); y+ must match turbulence model |
| Heat transfer | Fine mesh at solid-fluid interface; smooth transitions |
| Multiphase (VOF) | Uniform cells at interface; avoid high aspect ratios near free surface |
| Compressible/shocks | Align mesh with expected shock direction; fine cells at shock location |
| Combustion | Fine cells in flame region; smooth transitions to avoid numerical diffusion |

## Mesh Independence Study

Quality checks ensure the mesh is valid, but a **mesh independence study** ensures the mesh is sufficient. The procedure:

1. Create 3–5 meshes with increasing resolution (e.g., coarse → fine, doubling cell count each time).
2. Run the same simulation on each mesh.
3. Plot a key quantity (drag coefficient, pressure drop, etc.) versus mesh size.
4. The solution is mesh-independent when further refinement changes the result by less than 1–2%.

```python
import numpy as np
import matplotlib.pyplot as plt

# Example mesh independence data
cells = np.array([10000, 40000, 160000, 640000, 2560000])
cd_values = np.array([1.52, 1.41, 1.37, 1.355, 1.352])

plt.figure(figsize=(8, 5))
plt.semilogx(cells, cd_values, 'o-', linewidth=2, markersize=8)
plt.xlabel('Number of Cells')
plt.ylabel('Drag Coefficient (Cd)')
plt.title('Mesh Independence Study')
plt.grid(True, alpha=0.3)
plt.axhline(y=cd_values[-1], color='r', linestyle='--', alpha=0.5,
            label=f'Finest mesh: Cd = {cd_values[-1]:.3f}')
plt.legend()
plt.tight_layout()
plt.savefig('mesh_independence.png', dpi=150)
plt.show()
```

## Resources

- [OpenFOAM checkMesh Documentation](https://doc.openfoam.com/2306/tools/pre-processing/mesh/check-mesh/)
- [Gmsh Mesh Quality](http://gmsh.info/doc/texinfo/gmsh.html#Mesh-quality)
- [ParaView Mesh Quality Filter](https://docs.paraview.org/en/latest/ReferenceManual/meshQualityFilter.html)
- Ferziger, J.H. & Perić, M. (2002). *Computational Methods for Fluid Dynamics*. Springer — Chapter 3 on mesh quality.
