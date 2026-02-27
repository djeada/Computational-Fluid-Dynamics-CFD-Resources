# OpenFOAM Practice Guide

OpenFOAM (Open Field Operation and Manipulation) is a powerful, open-source CFD toolbox widely used in academia and industry for simulating fluid flow, heat transfer, turbulence, and multiphase flows.

## Table of Contents

- [Installation Guide](#installation-guide)
- [Basic Tutorials](#basic-tutorials)
- [Case Structure](#case-structure)
- [Solvers Overview](#solvers-overview)
- [Meshing with blockMesh](#meshing-with-blockmesh)
- [Meshing with snappyHexMesh](#meshing-with-snappyhexmesh)
- [Boundary Conditions](#boundary-conditions)
- [Turbulence Models](#turbulence-models)
- [Function Objects](#function-objects)
- [Post-Processing](#post-processing)
- [Advanced Topics](#advanced-topics)

## Installation Guide

### Linux Installation (Ubuntu/Debian)
```bash
# Add OpenFOAM repository
sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key | apt-key add -"
sudo add-apt-repository http://dl.openfoam.org/ubuntu

# Install OpenFOAM
sudo apt-get update
sudo apt-get install openfoam11

# Source the environment
echo "source /opt/openfoam11/etc/bashrc" >> ~/.bashrc
source ~/.bashrc
```

### Docker Installation
```bash
# Pull OpenFOAM Docker image
docker pull openfoam/openfoam11-paraview510

# Run container
docker run -it --rm -v $(pwd):/workspace openfoam/openfoam11-paraview510
```

### Verification
```bash
# Check installation
foamInstallationTest
```

## Case Structure

Every OpenFOAM case follows a standard directory structure:

```
case/
├── 0/          # Initial and boundary conditions
├── constant/   # Physical properties and mesh
├── system/     # Solution controls and schemes
└── [time]/     # Solution data at different times
```

### Essential Files

- **0/**: Contains field files (U, p, T, etc.)
- **constant/transportProperties**: Fluid properties
- **constant/polyMesh/**: Mesh data
- **system/controlDict**: Time controls and output
- **system/fvSchemes**: Numerical schemes
- **system/fvSolution**: Linear solvers and algorithms

## Basic Solvers

### Incompressible Flow Solvers

| Solver | Description | Applications |
|--------|-------------|--------------|
| `icoFoam` | Laminar, incompressible, transient | Simple flows, validation |
| `simpleFoam` | Steady-state RANS turbulence | External aerodynamics |
| `pimpleFoam` | Transient RANS turbulence | Unsteady flows |
| `pisoFoam` | Transient laminar/turbulent | Time-dependent flows |

### Compressible Flow Solvers

| Solver | Description | Applications |
|--------|-------------|--------------|
| `rhoCentralFoam` | Density-based, high-speed | Supersonic flows |
| `rhoSimpleFoam` | Pressure-based, steady | Subsonic compressible |
| `sonicFoam` | Transient compressible | Shock tubes |

## Meshing with blockMesh

### Basic blockMeshDict Structure
```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

convertToMeters 1;

vertices
(
    (0 0 0)    // vertex 0
    (1 0 0)    // vertex 1
    (1 1 0)    // vertex 2
    (0 1 0)    // vertex 3
    (0 0 1)    // vertex 4
    (1 0 1)    // vertex 5
    (1 1 1)    // vertex 6
    (0 1 1)    // vertex 7
);

blocks
(
    hex (0 1 2 3 4 5 6 7) (10 10 10) simpleGrading (1 1 1)
);

edges
(
);

boundary
(
    inlet
    {
        type patch;
        faces
        (
            (0 4 7 3)
        );
    }
    outlet
    {
        type patch;
        faces
        (
            (2 6 5 1)
        );
    }
    walls
    {
        type wall;
        faces
        (
            (1 5 4 0)
            (3 7 6 2)
            (0 3 2 1)
            (4 5 6 7)
        );
    }
);

mergePatchPairs
(
);
```

## Common Workflow

### 1. Case Setup
```bash
# Copy tutorial case
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily .
cd pitzDaily
```

### 2. Mesh Generation
```bash
# Generate mesh
blockMesh

# Check mesh quality
checkMesh
```

### 3. Run Simulation
```bash
# Run solver
simpleFoam

# Run in parallel (4 cores)
decomposePar
mpirun -np 4 simpleFoam -parallel
reconstructPar
```

### 4. Post-Processing
```bash
# Launch ParaView
paraFoam

# Sample data along line
sample

# Calculate wall forces
simpleFoam -postProcess -func forceCoeffs
```

## Boundary Conditions

### Velocity Boundary Conditions

```cpp
// Fixed value
inlet
{
    type            fixedValue;
    value           uniform (1 0 0);
}

// Zero gradient (outflow)
outlet
{
    type            zeroGradient;
}

// No-slip wall
wall
{
    type            noSlip;
}

// Slip wall
symmetry
{
    type            symmetryPlane;
}
```

### Pressure Boundary Conditions

```cpp
// Fixed value
outlet
{
    type            fixedValue;
    value           uniform 0;
}

// Zero gradient
inlet
{
    type            zeroGradient;
}
```

## Turbulence Models

### RANS Models
- **k-ε**: Standard, realizable, RNG variants
- **k-ω**: Standard, SST variants
- **Reynolds Stress Models**: Full RSM

### LES Models
- **Smagorinsky**: Classic SGS model
- **Dynamic models**: Dynamic Smagorinsky
- **Wall-adapting**: WALE model

For detailed turbulence model setup, inlet conditions, wall treatment, and worked examples, see [Turbulence Modeling Guide](turbulence_modeling.md).

## Meshing with snappyHexMesh

`snappyHexMesh` is OpenFOAM's utility for generating complex 3D meshes around arbitrary geometries defined by STL surfaces. It works by starting from a background hex mesh (from `blockMesh`) and iteratively refining, snapping to surfaces, and adding boundary layers.

### Workflow

```bash
# 1. Create background hex mesh
blockMesh

# 2. Place STL files in constant/triSurface/
cp geometry.stl constant/triSurface/

# 3. Run snappyHexMesh
snappyHexMesh

# 4. Check final mesh quality
checkMesh -latestTime
```

### Minimal snappyHexMeshDict

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      snappyHexMeshDict;
}

castellatedMesh true;
snap            true;
addLayers       true;

geometry
{
    body.stl
    {
        type triSurfaceMesh;
        name body;
    }
}

castellatedMeshControls
{
    maxLocalCells   100000;
    maxGlobalCells  2000000;
    minRefinementCells 10;
    nCellsBetweenLevels 3;

    features
    (
        { file "body.eMesh"; level 2; }
    );

    refinementSurfaces
    {
        body
        {
            level (2 3);
        }
    }

    refinementRegions
    {
        // Optional: add volume refinement
    }

    locationInMesh (0 0 0);    // Point inside the fluid domain
    allowFreeStandingZoneFaces true;
}

snapControls
{
    nSmoothPatch    3;
    tolerance       2.0;
    nSolveIter      100;
    nRelaxIter      5;
}

addLayersControls
{
    relativeSizes   true;
    layers
    {
        "body.*"
        {
            nSurfaceLayers 3;
        }
    }
    expansionRatio      1.2;
    finalLayerThickness 0.5;
    minThickness        0.1;
}

meshQualityControls
{
    maxNonOrtho     65;
    maxBoundarySkewness 20;
    maxInternalSkewness 4;
    maxConcave      80;
    minVol          1e-13;
    minTetQuality   1e-15;
    minArea         -1;
    minTwist        0.05;
    minDeterminant  0.001;
    minFaceWeight   0.05;
    minVolRatio     0.01;
    minTriangleTwist -1;
}
```

### Feature Edge Extraction

Before running snappyHexMesh, extract feature edges for better refinement:

```bash
surfaceFeatureExtract
```

This requires a `system/surfaceFeatureExtractDict`:

```cpp
body.stl
{
    extractionMethod    extractFromSurface;
    extractFromSurfaceCoeffs
    {
        includedAngle   150;
    }
}
```

## Function Objects

Function objects allow you to compute and write additional quantities during or after a simulation without modifying the solver.

### Common Function Objects

Add these to the `functions` block in `system/controlDict`:

```cpp
functions
{
    // Calculate and write y+ values
    yPlus
    {
        type            yPlus;
        libs            ("libfieldFunctionObjects.so");
        writeControl    writeTime;
    }

    // Calculate force coefficients on a patch
    forceCoeffs
    {
        type            forceCoeffs;
        libs            ("libforces.so");
        writeControl    timeStep;
        writeInterval   1;

        patches         (body);
        rho             rhoInf;
        rhoInf          1.225;
        CofR            (0 0 0);
        liftDir         (0 1 0);
        dragDir         (1 0 0);
        pitchAxis       (0 0 1);
        magUInf         10.0;
        lRef            1.0;
        Aref            1.0;
    }

    // Monitor a field at specific points
    probes
    {
        type            probes;
        libs            ("libsampling.so");
        writeControl    timeStep;
        writeInterval   1;

        fields          (p U);
        probeLocations
        (
            (1.0 0.0 0.0)
            (2.0 0.0 0.0)
        );
    }

    // Calculate vorticity field
    vorticity
    {
        type            vorticity;
        libs            ("libfieldFunctionObjects.so");
        writeControl    writeTime;
    }

    // Write residuals
    residuals
    {
        type            residuals;
        libs            ("libutilityFunctionObjects.so");
        writeControl    timeStep;
        writeInterval   1;
        fields          (p U k omega);  // Adjust to match your solved fields
    }
}
```

### Running Function Objects Post-Simulation

```bash
# Run all function objects on existing results
simpleFoam -postProcess

# Run a specific function object
simpleFoam -postProcess -func yPlus
simpleFoam -postProcess -func "forceCoeffs"
```

## Best Practices

1. **Mesh Quality**
   - Keep aspect ratios < 100
   - Ensure orthogonality > 30°
   - Maintain smooth transitions

2. **Solver Settings**
   - Start with loose tolerances
   - Monitor residuals
   - Use appropriate relaxation factors

3. **Parallel Processing**
   - Decompose domain efficiently
   - Balance load across processors
   - Use appropriate number of cores

4. **Convergence**
   - Monitor residuals and forces
   - Check mass conservation
   - Validate against experimental data

## Troubleshooting

### Common Issues
- **Divergence**: Check mesh quality, boundary conditions
- **Slow convergence**: Adjust relaxation factors, improve mesh
- **Mass imbalance**: Check boundary conditions, mesh quality

### Debugging Tools
```bash
# Check mesh
checkMesh -allTopology -allGeometry

# Monitor residuals
foamLog log.simpleFoam

# Check boundary conditions
boundaryFoam
```
