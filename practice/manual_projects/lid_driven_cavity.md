# Lid-Driven Cavity Flow — Complete Benchmark Tutorial

The lid-driven cavity is the most fundamental benchmark case in CFD. A square (or cubic) cavity has all walls stationary except the top wall, which moves at a constant velocity. Despite its geometric simplicity, this flow produces rich physics including primary and secondary vortices, corner singularities, and Reynolds-number-dependent flow transitions.

This tutorial walks through the complete workflow from mesh generation to quantitative validation against the benchmark data of Ghia et al. (1982).

## Table of Contents

- [Problem Definition](#problem-definition)
- [Physical Setup](#physical-setup)
- [Case Setup in OpenFOAM](#case-setup-in-openfoam)
- [Mesh Generation](#mesh-generation)
- [Running the Simulation](#running-the-simulation)
- [Post-Processing and Visualization](#post-processing-and-visualization)
- [Validation Against Benchmark Data](#validation-against-benchmark-data)
- [Reynolds Number Study](#reynolds-number-study)
- [Mesh Independence Study](#mesh-independence-study)
- [Extensions and Variations](#extensions-and-variations)

## Problem Definition

```
         Moving wall (U = 1 m/s →)
    ┌─────────────────────────────────┐
    │                                 │
    │                                 │
    │          Fluid Domain           │
    │           (square)              │  Fixed
Fixed│                                 │  wall
wall │                                 │
    │                                 │
    │                                 │
    └─────────────────────────────────┘
              Fixed wall
```

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Domain size | 0.1 m × 0.1 m | Square cavity |
| Lid velocity | U = 1 m/s | Constant, in x-direction |
| Kinematic viscosity | ν = 0.01 m²/s | Gives Re = 10 |
| Reynolds number | Re = U·L/ν | Varied from 100 to 10,000 |

### Expected Flow Features

At **Re = 100**:
- Single primary vortex centered slightly right of and above the geometric center.
- Weak secondary vortices in the bottom corners.

At **Re = 1,000**:
- Stronger primary vortex.
- Distinct secondary vortices in all corners.

At **Re = 10,000**:
- Primary vortex nearly centered.
- Strong secondary and tertiary corner vortices.

## Physical Setup

The Reynolds number controls the flow regime:

```
Re = U × L / ν
```

For Re = 100:
```
U = 1 m/s
L = 0.1 m
ν = U × L / Re = 1 × 0.1 / 100 = 0.001 m²/s
```

For Re = 1000:
```
ν = 1 × 0.1 / 1000 = 0.0001 m²/s
```

## Case Setup in OpenFOAM

### Create Case Structure

```bash
mkdir -p lid_driven_cavity/{0,constant,system}
cd lid_driven_cavity
```

### 0/U — Velocity Field

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       volVectorField;
    object      U;
}

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (0 0 0);

boundaryField
{
    movingWall
    {
        type            fixedValue;
        value           uniform (1 0 0);
    }
    fixedWalls
    {
        type            noSlip;
    }
    frontAndBack
    {
        type            empty;
    }
}
```

### 0/p — Pressure Field

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      p;
}

dimensions      [0 2 -2 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    movingWall
    {
        type            zeroGradient;
    }
    fixedWalls
    {
        type            zeroGradient;
    }
    frontAndBack
    {
        type            empty;
    }
}
```

### constant/transportProperties

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      transportProperties;
}

nu              [0 2 -1 0 0 0 0] 0.001;  // Re = 100
```

### system/blockMeshDict

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

convertToMeters 0.1;

vertices
(
    (0 0 0)
    (1 0 0)
    (1 1 0)
    (0 1 0)
    (0 0 0.1)
    (1 0 0.1)
    (1 1 0.1)
    (0 1 0.1)
);

blocks
(
    hex (0 1 2 3 4 5 6 7) (40 40 1) simpleGrading (1 1 1)
);

edges
(
);

boundary
(
    movingWall
    {
        type wall;
        faces
        (
            (3 7 6 2)
        );
    }
    fixedWalls
    {
        type wall;
        faces
        (
            (0 4 7 3)
            (2 6 5 1)
            (1 5 4 0)
        );
    }
    frontAndBack
    {
        type empty;
        faces
        (
            (0 3 2 1)
            (4 5 6 7)
        );
    }
);

mergePatchPairs
(
);
```

### system/controlDict

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      controlDict;
}

application     icoFoam;

startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         0.5;
deltaT          0.005;

writeControl    timeStep;
writeInterval   20;

purgeWrite      0;
writeFormat     ascii;
writePrecision  6;
writeCompression off;

timeFormat      general;
timePrecision   6;

runTimeModifiable true;
```

### system/fvSchemes

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSchemes;
}

ddtSchemes
{
    default         Euler;
}

gradSchemes
{
    default         Gauss linear;
    grad(p)         Gauss linear;
}

divSchemes
{
    default         none;
    div(phi,U)      Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear orthogonal;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         orthogonal;
}
```

### system/fvSolution

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSolution;
}

solvers
{
    p
    {
        solver          PCG;
        preconditioner  DIC;
        tolerance       1e-06;
        relTol          0.05;
    }

    pFinal
    {
        $p;
        relTol          0;
    }

    U
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-05;
        relTol          0;
    }
}

PISO
{
    nCorrectors     2;
    nNonOrthogonalCorrectors 0;
    pRefCell        0;
    pRefValue       0;
}
```

### system/sampleDict — For Extracting Centerline Profiles

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      sampleDict;
}

interpolationScheme cellPoint;

setFormat       raw;

sets
(
    // Vertical line through center (x = 0.05)
    verticalLine
    {
        type    uniform;
        axis    y;
        start   (0.05 0 0.005);
        end     (0.05 0.1 0.005);
        nPoints 200;
    }

    // Horizontal line through center (y = 0.05)
    horizontalLine
    {
        type    uniform;
        axis    x;
        start   (0 0.05 0.005);
        end     (0.1 0.05 0.005);
        nPoints 200;
    }
);

fields
(
    U
    p
);
```

## Mesh Generation

```bash
# Generate mesh
blockMesh

# Check quality
checkMesh
```

Expected output:

```
Mesh stats
    points:           3362
    cells:            1600
    ...
Mesh OK.
```

## Running the Simulation

```bash
# Run solver
icoFoam > log.icoFoam 2>&1

# Check that it completed
tail log.icoFoam
```

Expected final output:

```
Time = 0.5
...
ExecutionTime = X s
End
```

## Post-Processing and Visualization

### Extract Centerline Profiles

```bash
# Sample velocity along centerlines at the final time step
sample -latestTime
```

This creates files in `postProcessing/sets/<latestTime>/`:
- `verticalLine_U.xy` — u(y) along the vertical centerline
- `horizontalLine_U.xy` — v(x) along the horizontal centerline

### Visualize in ParaView

```bash
paraFoam
# Or
foamToVTK && paraview
```

Key visualizations to create:
1. **Velocity magnitude** contour plot
2. **Streamlines** showing vortex structure
3. **Pressure** contour plot
4. **Vorticity** field (apply the Gradient filter to U, then compute curl)

## Validation Against Benchmark Data

The standard benchmark is **Ghia, Ghia, and Shin (1982)**, "High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method", *Journal of Computational Physics*, 48, 387–411.

### Benchmark Data for Re = 100

Horizontal velocity (u) along the vertical centerline (x = 0.5L):

| y/L | u/U (Ghia et al.) |
|-----|-------------------|
| 1.0000 | 1.00000 |
| 0.9766 | 0.84123 |
| 0.9688 | 0.78871 |
| 0.9609 | 0.73722 |
| 0.9531 | 0.68717 |
| 0.8516 | 0.23151 |
| 0.7344 | 0.00332 |
| 0.6172 | -0.13641 |
| 0.5000 | -0.20581 |
| 0.4531 | -0.21090 |
| 0.2813 | -0.15662 |
| 0.1719 | -0.10150 |
| 0.1016 | -0.06434 |
| 0.0703 | -0.04775 |
| 0.0625 | -0.04192 |
| 0.0547 | -0.03717 |
| 0.0000 | 0.00000 |

### Validation Script

```python
#!/usr/bin/env python3
"""
Validate lid-driven cavity results against Ghia et al. (1982).
"""

import numpy as np
import matplotlib.pyplot as plt

# Ghia et al. (1982) benchmark data for Re = 100
# u-velocity along vertical centerline (x = 0.5)
ghia_y = np.array([
    1.0000, 0.9766, 0.9688, 0.9609, 0.9531, 0.8516, 0.7344,
    0.6172, 0.5000, 0.4531, 0.2813, 0.1719, 0.1016, 0.0703,
    0.0625, 0.0547, 0.0000
])
ghia_u = np.array([
    1.00000,  0.84123,  0.78871,  0.73722,  0.68717,  0.23151,  0.00332,
   -0.13641, -0.20581, -0.21090, -0.15662, -0.10150, -0.06434, -0.04775,
   -0.04192, -0.03717,  0.00000
])

# v-velocity along horizontal centerline (y = 0.5)
ghia_x = np.array([
    1.0000, 0.9688, 0.9609, 0.9531, 0.9453, 0.9063, 0.8594,
    0.8047, 0.5000, 0.2344, 0.2266, 0.1563, 0.0938, 0.0781,
    0.0703, 0.0625, 0.0000
])
ghia_v = np.array([
    0.00000, -0.05906, -0.07391, -0.08864, -0.10313, -0.16914, -0.22445,
   -0.24533,  0.05454,  0.17527,  0.17507,  0.16077,  0.12317,  0.10890,
    0.10091,  0.09233,  0.00000
])

def load_openfoam_sample(filename, velocity_component=0):
    """Load OpenFOAM sample data.

    The raw format has columns: coordinate Ux Uy Uz
    """
    data = np.loadtxt(filename)
    coord = data[:, 0]
    vel = data[:, 1 + velocity_component]
    return coord, vel

def validate(sample_dir="postProcessing/sets"):
    """Run validation and generate comparison plots."""
    import glob
    import os

    # Find the latest time directory
    time_dirs = sorted(glob.glob(os.path.join(sample_dir, "*")))
    if not time_dirs:
        print(f"No sample data found in {sample_dir}")
        print("Run: sample -latestTime")
        return
    latest = time_dirs[-1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: u-velocity along vertical centerline
    vert_file = os.path.join(latest, "verticalLine_U.xy")
    if os.path.exists(vert_file):
        y_sim, u_sim = load_openfoam_sample(vert_file, velocity_component=0)
        # Normalize
        L = 0.1  # cavity size
        ax1.plot(u_sim, y_sim / L, 'b-', linewidth=1.5, label='OpenFOAM')

    ax1.plot(ghia_u, ghia_y, 'ro', markersize=6, label='Ghia et al. (1982)')
    ax1.set_xlabel('u / U')
    ax1.set_ylabel('y / L')
    ax1.set_title('u-velocity along vertical centerline')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-0.4, 1.1)

    # Plot 2: v-velocity along horizontal centerline
    horiz_file = os.path.join(latest, "horizontalLine_U.xy")
    if os.path.exists(horiz_file):
        x_sim, v_sim = load_openfoam_sample(horiz_file, velocity_component=1)
        ax2.plot(x_sim / L, v_sim, 'b-', linewidth=1.5, label='OpenFOAM')

    ax2.plot(ghia_x, ghia_v, 'ro', markersize=6, label='Ghia et al. (1982)')
    ax2.set_xlabel('x / L')
    ax2.set_ylabel('v / U')
    ax2.set_title('v-velocity along horizontal centerline')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.35, 0.25)

    plt.tight_layout()
    plt.savefig('validation_ghia.png', dpi=150)
    plt.show()
    print("Validation plot saved as validation_ghia.png")

if __name__ == "__main__":
    validate()
```

## Reynolds Number Study

Explore how flow structure changes with Reynolds number by modifying `constant/transportProperties`:

| Re | ν (m²/s) | Flow Character |
|----|----------|----------------|
| 100 | 0.001 | Single vortex, steady |
| 400 | 0.00025 | Stronger vortex, visible corner eddies |
| 1,000 | 0.0001 | Strong primary vortex, distinct secondary vortices |
| 3,200 | 3.125e-5 | Complex vortex structure |
| 5,000 | 2.0e-5 | Near-transitional (use finer mesh) |
| 10,000 | 1.0e-5 | May become unsteady (use pimpleFoam) |

### Automation Script

```bash
#!/bin/bash
# Run cavity at multiple Reynolds numbers

TEMPLATE="lid_driven_cavity"

for RE in 100 400 1000 3200; do
    NU=$(echo "scale=8; 1.0 * 0.1 / $RE" | bc -l)
    CASE="cavity_Re${RE}"

    echo "Setting up Re = $RE (nu = $NU)"

    cp -r $TEMPLATE $CASE
    cd $CASE

    # Update viscosity
    sed -i "s/nu.*\[0 2 -1 0 0 0 0\].*/nu              [0 2 -1 0 0 0 0] $NU;/" \
        constant/transportProperties

    # For higher Re, use finer mesh and smaller time step
    if [ $RE -ge 1000 ]; then
        sed -i 's/(40 40 1)/(80 80 1)/' system/blockMeshDict
        sed -i 's/deltaT.*0.005/deltaT          0.001/' system/controlDict
        sed -i 's/endTime.*0.5/endTime         1.0/' system/controlDict
    fi

    blockMesh > log.blockMesh 2>&1
    icoFoam > log.icoFoam 2>&1
    sample -latestTime > log.sample 2>&1

    cd ..
    echo "Completed Re = $RE"
done

echo "All cases completed."
```

## Mesh Independence Study

Run the same case (Re = 100) with different mesh resolutions:

| Mesh | Cells | Resolution |
|------|-------|------------|
| Coarse | 20 × 20 | 400 cells |
| Medium | 40 × 40 | 1,600 cells |
| Fine | 80 × 80 | 6,400 cells |
| Very fine | 160 × 160 | 25,600 cells |

Track the minimum u-velocity along the vertical centerline (the core of the primary vortex) to assess convergence.

```python
#!/usr/bin/env python3
"""
Mesh independence study for lid-driven cavity.
"""

import numpy as np
import matplotlib.pyplot as plt

# Results from different mesh resolutions (fill in after running)
mesh_sizes = [20, 40, 80, 160]
cells = [s**2 for s in mesh_sizes]
u_min = []  # minimum u along vertical centerline for each mesh

# Ghia et al. reference value for Re=100
ghia_u_min = -0.21090  # at y/L = 0.4531

for n in mesh_sizes:
    try:
        # Load data from each case
        data = np.loadtxt(f"cavity_{n}x{n}/postProcessing/sets/0.5/verticalLine_U.xy")
        u_min.append(np.min(data[:, 1]))
    except FileNotFoundError:
        u_min.append(np.nan)

plt.figure(figsize=(8, 5))
plt.semilogx(cells, u_min, 'bo-', markersize=8, linewidth=2, label='OpenFOAM')
plt.axhline(y=ghia_u_min, color='r', linestyle='--',
            label=f'Ghia et al.: {ghia_u_min:.5f}')
plt.xlabel('Number of Cells')
plt.ylabel('Minimum u-velocity on centerline')
plt.title('Mesh Independence Study — Lid-Driven Cavity (Re = 100)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('mesh_independence_cavity.png', dpi=150)
plt.show()
```

## Extensions and Variations

After completing the basic tutorial, try these extensions:

### 1. 3D Cavity

Extend the mesh in the z-direction to study three-dimensional effects:

```cpp
// In blockMeshDict, change:
// (40 40 1) to (40 40 40)
// Remove "empty" boundary type for frontAndBack
// Change frontAndBack to type "wall"
```

Use `pisoFoam` or `icoFoam` in 3D — note the significantly higher computational cost.

### 2. Turbulent Cavity (High Re)

For Re > 5,000, consider using RANS turbulence:

```bash
# Switch to simpleFoam with k-omega SST
# See practice/openfoam/turbulence_modeling.md for setup details
```

### 3. Natural Convection (Heated Cavity)

Add a temperature field with a heated left wall and cooled right wall. Use `buoyantBoussinesqSimpleFoam` for natural convection driven by temperature gradients.

### 4. Two-Sided Lid-Driven Cavity

Set both top and bottom walls to move in opposite directions, creating a symmetric flow with two counter-rotating vortices.

### 5. Regularized Lid Velocity

The sharp velocity discontinuity at the top corners (lid velocity vs. zero at the side walls) is a mathematical singularity. For better numerical behavior, use a regularized velocity profile:

```
U(x) = U_lid × 16 × x² × (1-x)²
```

This sets the velocity smoothly to zero at the corners.

## References

- Ghia, U., Ghia, K.N., and Shin, C.T. (1982). "High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method." *Journal of Computational Physics*, 48, 387–411.
- Erturk, E., Corke, T.C., and Gökçöl, C. (2005). "Numerical solutions of 2-D steady incompressible driven cavity flow at high Reynolds numbers." *Int. J. Numer. Methods Fluids*, 48, 747–774.
- Botella, O. and Peyret, R. (1998). "Benchmark spectral results on the lid-driven cavity flow." *Computers & Fluids*, 27, 421–433.
