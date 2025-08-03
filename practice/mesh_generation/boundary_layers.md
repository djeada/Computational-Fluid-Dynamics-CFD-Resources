# Boundary Layer Meshing Guide

Boundary layer meshing is crucial for accurately capturing near-wall flow phenomena in CFD simulations. This guide covers theory, implementation, and best practices.

## Theory Background

### Boundary Layer Physics
The boundary layer is the thin region near solid walls where viscous effects dominate. Key characteristics:
- Velocity changes from zero (no-slip) to free-stream value
- Large velocity gradients require fine mesh resolution
- Thickness depends on Reynolds number and distance from leading edge

### y+ Concept
The dimensionless wall distance y+ determines mesh requirements:
```
y+ = (y * u_τ) / ν
```
Where:
- y = distance from wall
- u_τ = friction velocity = √(τ_wall/ρ)
- ν = kinematic viscosity

### y+ Guidelines
| Application | y+ Range | Wall Treatment |
|-------------|----------|----------------|
| DNS | y+ < 1 | Direct resolution |
| Wall-resolved LES | y+ < 1 | Direct resolution |
| Low-Re RANS | y+ < 1 | Integration to wall |
| Wall functions | 30 < y+ < 300 | Logarithmic law |
| Enhanced wall treatment | y+ < 1 or y+ > 30 | Automatic switching |

## First Cell Height Calculation

### Flat Plate Formula
For flow over a flat plate:
```
δ ≈ 5 * x / √(Re_x)
y_first ≈ δ / (n_layers * growth_ratio^(n_layers-1))
```

### Practical Estimation
Quick estimate for y+ = 1:
```
y_first ≈ 74 * ν / √(Re_L)
```
Where Re_L is based on characteristic length.

### Example Calculation
```python
import numpy as np

def calculate_first_cell_height(velocity, length, viscosity, y_plus_target=1.0):
    """
    Calculate first cell height for target y+
    
    Parameters:
    velocity: free-stream velocity (m/s)
    length: characteristic length (m)
    viscosity: kinematic viscosity (m²/s)
    y_plus_target: target y+ value
    
    Returns:
    y_first: first cell height (m)
    """
    Re_L = velocity * length / viscosity
    Cf = 0.664 / np.sqrt(Re_L)  # Flat plate friction coefficient
    tau_wall = 0.5 * Cf * velocity**2  # Assuming rho = 1
    u_tau = np.sqrt(tau_wall)
    
    y_first = y_plus_target * viscosity / u_tau
    return y_first

# Example usage
velocity = 10.0  # m/s
length = 1.0     # m
viscosity = 1e-5 # m²/s (air at standard conditions)

y_first = calculate_first_cell_height(velocity, length, viscosity)
print(f"First cell height: {y_first:.2e} m")
```

## Mesh Generation Tools

### Gmsh Boundary Layer Implementation

#### Method 1: BoundaryLayer Field
```cpp
// In .geo file
Field[1] = BoundaryLayer;
Field[1].EdgesList = {1, 2, 3, 4};      // Wall edges
Field[1].hfar = 0.1;                    // Far-field size
Field[1].hwall_n = 1e-5;                // First layer height
Field[1].thickness = 0.01;              // Total BL thickness
Field[1].ratio = 1.2;                   // Growth ratio
Field[1].Quads = 1;                     // Use quadrilaterals
Field[1].AnisoMax = 10;                 // Anisotropy limit
Background Field = 1;
```

#### Method 2: Extrusion with Layers
```cpp
// Extrude surface with boundary layers
Extrude {0, 0, 1} {
  Surface{1}; 
  Layers{5, 10, 15};         // Number of layers
  Recombine;                 // Create prisms
}
```

### OpenFOAM snappyHexMesh
```cpp
// snappyHexMeshDict - addLayersControls
addLayersControls
{
    relativeSizes true;
    
    layers
    {
        "wall.*"
        {
            nSurfaceLayers 5;
        }
    }
    
    expansionRatio 1.2;
    finalLayerThickness 0.3;
    minThickness 0.1;
    
    nGrow 0;
    featureAngle 30;
    nRelaxIter 3;
    nSmoothSurfaceNormals 1;
    nSmoothNormals 3;
    nSmoothThickness 10;
    maxFaceThicknessRatio 0.5;
    maxThicknessToMedialRatio 0.3;
    minMedianAxisAngle 90;
    nBufferCellsNoExtrude 0;
    nLayerIter 50;
}
```

### Salome Boundary Layer Meshing
```python
# Python script for Salome
import salome
salome.salome_init()

from salome.geom import geomBuilder
from salome.smesh import smeshBuilder

# Create geometry (example: plate)
geompy = geomBuilder.New()
smesh = smeshBuilder.New()

# Create plate geometry
plate = geompy.MakeFaceHW(1.0, 0.1, 1)  # Length, width, height
wall_face = geompy.GetFaceNearPoint(plate, geompy.MakeVertex(0, 0, 0))

# Create mesh
mesh = smesh.Mesh(plate)

# 2D algorithm
mesh.Triangle()

# Boundary layer
mesh.ViscousLayers2D(0.001,    # First layer thickness
                     5,        # Number of layers
                     1.2,      # Growth ratio
                     [wall_face])  # Faces to apply

# Generate mesh
mesh.Compute()
```

## Quality Assessment

### Metrics for Boundary Layer Meshes
1. **Aspect Ratio**: Should be high in normal direction (10-1000)
2. **Orthogonality**: > 15° for prisms
3. **Skewness**: < 0.85
4. **Growth Ratio**: 1.1-1.3 typical
5. **y+ Distribution**: Check uniformity along walls

### OpenFOAM Quality Check
```bash
# Check mesh quality
checkMesh -allGeometry -allTopology

# Calculate y+ values
simpleFoam -postProcess -func yPlus
```

### Python y+ Calculation
```python
import numpy as np
import matplotlib.pyplot as plt

def plot_yplus_distribution(wall_shear_stress, first_cell_height, viscosity):
    """
    Plot y+ distribution along wall
    """
    u_tau = np.sqrt(wall_shear_stress)
    y_plus = first_cell_height * u_tau / viscosity
    
    plt.figure(figsize=(10, 6))
    plt.plot(y_plus)
    plt.axhline(y=1, color='r', linestyle='--', label='y+ = 1')
    plt.axhline(y=30, color='g', linestyle='--', label='y+ = 30')
    plt.xlabel('Wall Cell Index')
    plt.ylabel('y+')
    plt.title('y+ Distribution Along Wall')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    plt.show()
```

## Best Practices

### General Guidelines
1. **Start Coarse**: Begin with fewer layers, refine as needed
2. **Gradual Growth**: Use growth ratios of 1.1-1.3
3. **Sufficient Layers**: 10-20 layers for wall-resolved
4. **Total Thickness**: BL should extend to ~20-30% of boundary layer thickness
5. **Transition Smoothly**: Avoid sudden changes in cell size

### Common Pitfalls
- **Too Aggressive Growth**: High ratios cause quality issues
- **Insufficient Layers**: Missing important physics
- **Poor Surface Definition**: Causes layer generation failures
- **Inadequate Smoothing**: Results in mesh distortion

### Troubleshooting Layer Generation

#### Gmsh Issues
```bash
# Enable verbose output
gmsh -v 5 geometry.geo

# Reduce layer thickness if failing
Field[1].thickness = 0.005;  // Reduce from 0.01

# Improve surface mesh quality first
Mesh.ElementSizeFactor = 0.5;
```

#### OpenFOAM snappyHexMesh Issues
```cpp
// Relaxed settings for difficult geometries
nRelaxIter 5;               // Increase from 3
nSmoothSurfaceNormals 5;    // Increase smoothing
maxFaceThicknessRatio 2.0;  // More permissive
```

## Advanced Techniques

### Anisotropic Mesh Adaptation
```python
# Metric tensor for boundary layer adaptation
def boundary_layer_metric(normal_direction, tangent_directions, 
                         normal_size, tangent_size):
    """
    Create anisotropic metric tensor for boundary layers
    """
    # High resolution normal to wall
    # Coarser resolution tangential to wall
    metric = np.zeros((3, 3))
    
    # Normal direction (fine)
    metric += np.outer(normal_direction, normal_direction) / normal_size**2
    
    # Tangential directions (coarse)
    for tangent in tangent_directions:
        metric += np.outer(tangent, tangent) / tangent_size**2
    
    return metric
```

### Hybrid Meshing Strategy
```
1. Generate structured boundary layer mesh
2. Fill remaining domain with unstructured elements
3. Ensure smooth transition between regions
4. Maintain quality metrics throughout
```

### Automated Layer Height Calculation
```bash
#!/bin/bash
# auto_layer_height.sh

# Input parameters
VELOCITY=$1
LENGTH=$2  
VISCOSITY=$3
Y_PLUS_TARGET=$4

# Calculate Reynolds number
RE=$(echo "scale=0; $VELOCITY * $LENGTH / $VISCOSITY" | bc -l)

# Estimate friction coefficient (flat plate)
CF=$(echo "scale=8; 0.664 / sqrt($RE)" | bc -l)

# Calculate wall shear stress (assuming rho=1)
TAU_WALL=$(echo "scale=8; 0.5 * $CF * $VELOCITY^2" | bc -l)

# Friction velocity
U_TAU=$(echo "scale=8; sqrt($TAU_WALL)" | bc -l)

# First cell height
Y_FIRST=$(echo "scale=8; $Y_PLUS_TARGET * $VISCOSITY / $U_TAU" | bc -l)

echo "Reynolds number: $RE"
echo "Friction coefficient: $CF"
echo "Friction velocity: $U_TAU"
echo "First cell height: $Y_FIRST"

# Update Gmsh field
sed -i "s/Field\[1\].hwall_n = .*/Field[1].hwall_n = $Y_FIRST;/" geometry.geo
```

This comprehensive guide provides the theoretical background and practical implementation details needed for successful boundary layer meshing in CFD applications.
