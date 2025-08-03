# OpenFOAM Getting Started Tutorial

This tutorial will guide you through your first OpenFOAM simulation - the classic cavity flow case.

## Prerequisites

- OpenFOAM installed and environment sourced
- Basic understanding of CFD concepts
- Familiarity with terminal/command line

## Tutorial: Lid-Driven Cavity Flow

The lid-driven cavity is a benchmark case in CFD, featuring a square cavity with a moving top wall that drives the flow.

### Step 1: Copy Tutorial Case

```bash
# Navigate to your working directory
mkdir ~/OpenFOAM-cases
cd ~/OpenFOAM-cases

# Copy the cavity tutorial
cp -r $FOAM_TUTORIALS/incompressible/icoFoam/cavity/cavity .
cd cavity
```

### Step 2: Examine Case Structure

```bash
# View directory structure
tree
```

You should see:
```
cavity/
├── 0/
│   ├── p
│   └── U
├── constant/
│   ├── polyMesh/
│   └── transportProperties
└── system/
    ├── blockMeshDict
    ├── controlDict
    ├── fvSchemes
    └── fvSolution
```

### Step 3: Understanding Initial Conditions

#### Velocity Field (0/U)
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
        value           uniform (1 0 0);  // Moving at 1 m/s in x-direction
    }
    fixedWalls
    {
        type            noSlip;
    }
    frontAndBack
    {
        type            empty;  // 2D case
    }
}
```

#### Pressure Field (0/p)
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

### Step 4: Physical Properties

#### Transport Properties (constant/transportProperties)
```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      transportProperties;
}

nu              [0 2 -1 0 0 0 0] 0.01;  // Kinematic viscosity
```

### Step 5: Mesh Generation

#### View Mesh Dictionary (system/blockMeshDict)
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
    hex (0 1 2 3 4 5 6 7) (20 20 1) simpleGrading (1 1 1)
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

#### Generate Mesh
```bash
# Create mesh
blockMesh

# Check mesh quality
checkMesh
```

### Step 6: Solution Control

#### Control Dictionary (system/controlDict)
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

### Step 7: Numerical Schemes

#### Schemes (system/fvSchemes)
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

### Step 8: Run Simulation

```bash
# Run the icoFoam solver
icoFoam

# Monitor progress
tail -f log.icoFoam
```

### Step 9: Post-Processing

#### Launch ParaView
```bash
# Generate ParaView files
paraFoam

# Or use foamToVTK for newer ParaView versions
foamToVTK
```

#### Sample Data Along Line
Create `system/sampleDict`:
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
    lineX1
    {
        type    uniform;
        axis    y;
        start   (0.5 0 0.05);
        end     (0.5 1 0.05);
        nPoints 100;
    }
);

fields
(
    U
    p
);
```

Run sampling:
```bash
sample
```

### Step 10: Analysis and Visualization

#### Key Results to Examine:
1. **Velocity vectors**: Show flow circulation
2. **Pressure contours**: Pressure distribution
3. **Streamlines**: Flow patterns
4. **Velocity profiles**: Compare with literature

#### Expected Flow Features:
- Primary vortex in the center
- Secondary vortices in corners
- Boundary layer near walls
- Steady-state solution after t ≈ 0.5s

### Step 11: Parameter Studies

Try modifying these parameters to see their effects:

#### Reynolds Number
```bash
# Edit constant/transportProperties
# Change nu to vary Re = UL/nu
```

#### Mesh Resolution
```bash
# Edit system/blockMeshDict
# Change (20 20 1) to (40 40 1) for finer mesh
blockMesh
```

#### Time Step
```bash
# Edit system/controlDict
# Reduce deltaT for better accuracy
```

## Common Issues and Solutions

### Courant Number Too High
```
Solution: Reduce time step in controlDict
deltaT          0.001;  // Reduce from 0.005
```

### Mesh Quality Warning
```
Solution: Improve mesh in blockMeshDict
- Increase resolution
- Check vertex ordering
- Ensure proper boundary definitions
```

### Slow Convergence
```
Solution: 
- Check boundary conditions
- Verify initial conditions
- Ensure mesh quality
```

## Next Steps

After completing this tutorial, try:

1. **Different Reynolds numbers**: Modify viscosity
2. **3D cavity**: Extend mesh in z-direction
3. **Turbulent flow**: Use simpleFoam with turbulence
4. **Heat transfer**: Add temperature equation
5. **Moving mesh**: Try dynamic mesh cases

## Validation Data

Compare your results with benchmark data:
- Ghia et al. (1982) velocity profiles
- Stream function contours
- Vorticity distributions

This tutorial provides a solid foundation for OpenFOAM usage and can be extended to more complex cases.
