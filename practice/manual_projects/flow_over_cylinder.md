# Flow Over Cylinder - Complete CFD Tutorial

This tutorial demonstrates a complete CFD workflow for flow over a circular cylinder, a fundamental benchmark case in fluid mechanics.

## 🎯 Objectives

- Understand vortex shedding phenomena
- Learn complete OpenFOAM workflow
- Validate against experimental data
- Analyze unsteady flow characteristics
- Calculate drag and lift coefficients

## 📋 Problem Description

### Physical Setup
- **Geometry**: Circular cylinder (diameter D = 0.1 m) in cross-flow
- **Domain**: 20D × 10D rectangular domain
- **Reynolds Number**: Re = 100 (based on diameter and inlet velocity)
- **Fluid**: Incompressible viscous flow (air properties)

### Expected Results
- **Strouhal Number**: St ≈ 0.164 for Re = 100
- **Mean Drag Coefficient**: Cd ≈ 1.35
- **RMS Lift Coefficient**: Cl_rms ≈ 0.25

## 🛠️ Prerequisites

```bash
# Required software
- OpenFOAM (v11 or later)
- ParaView for visualization
- Python with matplotlib and numpy
- Gmsh (optional, for advanced meshing)
```

## 📐 Step 1: Geometry and Mesh Generation

### Create Case Directory
```bash
mkdir flow_over_cylinder
cd flow_over_cylinder
mkdir 0 constant system
```

### Mesh Generation with blockMesh

Create `system/blockMeshDict`:
```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

convertToMeters 1;

// Cylinder parameters
D 0.1;          // Cylinder diameter
R #calc "0.5*$D";  // Cylinder radius

// Domain dimensions
xMin -2.0;      // 20D upstream
xMax 8.0;       // 80D downstream  
yMin -2.5;      // 25D width
yMax 2.5;

// Mesh resolution
nx1 40;         // Upstream
nx2 80;         // Downstream
ny 50;          // Cross-stream
nz 1;           // 2D simulation

vertices
(
    ($xMin $yMin 0)     // 0
    (0     $yMin 0)     // 1
    ($xMax $yMin 0)     // 2
    ($xMax $yMax 0)     // 3
    (0     $yMax 0)     // 4
    ($xMin $yMax 0)     // 5
    
    ($xMin $yMin 1)     // 6
    (0     $yMin 1)     // 7
    ($xMax $yMin 1)     // 8
    ($xMax $yMax 1)     // 9
    (0     $yMax 1)     // 10
    ($xMin $yMax 1)     // 11
);

blocks
(
    hex (0 1 4 5 6 7 10 11) ($nx1 $ny $nz) simpleGrading (1 1 1)  // Upstream
    hex (1 2 3 4 7 8 9 10)  ($nx2 $ny $nz) simpleGrading (1 1 1)  // Downstream
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
            (0 6 11 5)
        );
    }
    outlet
    {
        type patch;
        faces
        (
            (2 3 9 8)
        );
    }
    cylinder
    {
        type wall;
        faces ();  // Will be added by topoSet
    }
    sides
    {
        type symmetryPlane;
        faces
        (
            (0 1 7 6)
            (4 5 11 10)
        );
    }
    frontAndBack
    {
        type empty;
        faces
        (
            (0 5 4 1)
            (1 4 3 2)
            (6 7 10 11)
            (7 8 9 10)
        );
    }
);

mergePatchPairs
(
);
```

### Create Cylinder using topoSet

Create `system/topoSetDict`:
```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      topoSetDict;
}

actions
(
    {
        name    cylinderCells;
        type    cellSet;
        action  new;
        source  cylinderToCell;
        sourceInfo
        {
            p1      (0 0 0);
            p2      (0 0 1);
            radius  0.05;
        }
    }
    
    {
        name    cylinder;
        type    faceSet;
        action  new;
        source  cellToFace;
        sourceInfo
        {
            set     cylinderCells;
            option  all;
        }
    }
);
```

### Generate Mesh
```bash
# Generate initial mesh
blockMesh

# Create cylinder
topoSet

# Remove cylinder cells
subsetMesh -overwrite cylinderCells -patch cylinder

# Check mesh
checkMesh
```

## ⚙️ Step 2: Initial and Boundary Conditions

### Velocity Field (0/U)
```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       volVectorField;
    object      U;
}

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (1 0 0);

boundaryField
{
    inlet
    {
        type            fixedValue;
        value           uniform (1 0 0);  // 1 m/s inlet
    }
    
    outlet
    {
        type            zeroGradient;
    }
    
    cylinder
    {
        type            noSlip;
    }
    
    sides
    {
        type            symmetryPlane;
    }
    
    frontAndBack
    {
        type            empty;
    }
}
```

### Pressure Field (0/p)
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
    inlet
    {
        type            zeroGradient;
    }
    
    outlet
    {
        type            fixedValue;
        value           uniform 0;
    }
    
    cylinder
    {
        type            zeroGradient;
    }
    
    sides
    {
        type            symmetryPlane;
    }
    
    frontAndBack
    {
        type            empty;
    }
}
```

### Transport Properties (constant/transportProperties)
```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      transportProperties;
}

// For Re = 100: nu = U*D/Re = 1*0.1/100 = 0.001
nu              [0 2 -1 0 0 0 0] 0.001;
```

## 🔧 Step 3: Solver Configuration

### Control Dictionary (system/controlDict)
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
endTime         20;         // Sufficient for multiple shedding cycles
deltaT          0.005;      // Small time step for stability

writeControl    timeStep;
writeInterval   20;         // Write every 0.1 time units

purgeWrite      0;
writeFormat     ascii;
writePrecision  6;
writeCompression off;

timeFormat      general;
timePrecision   6;

runTimeModifiable true;

// Function objects for force calculation
functions
{
    forceCoeffsIncompressible
    {
        type            forceCoeffs;
        libs            ("libforces.so");
        
        writeControl    timeStep;
        writeInterval   1;
        
        patches         (cylinder);
        
        rho             rhoInf;
        rhoInf          1.0;        // Reference density
        
        CofR            (0 0 0);    // Center of rotation
        liftDir         (0 1 0);
        dragDir         (1 0 0);
        pitchAxis       (0 0 1);
        
        magUInf         1.0;        // Reference velocity
        lRef            0.1;        // Reference length (diameter)
        Aref            0.1;        // Reference area (D*1 for 2D)
    }
    
    probes
    {
        type            probes;
        libs            ("libsampling.so");
        
        writeControl    timeStep;
        writeInterval   1;
        
        fields          (p U);
        
        probeLocations
        (
            (0.1  0.0  0.5)   // Wake probe
            (0.2  0.0  0.5)   // Further downstream
            (0.5  0.0  0.5)   // Far wake
        );
    }
}
```

### Numerical Schemes (system/fvSchemes)
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
    default         Euler;      // First-order time scheme
}

gradSchemes
{
    default         Gauss linear;
}

divSchemes
{
    default         none;
    div(phi,U)      Gauss upwind;  // Stable for this Re
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

### Solution Controls (system/fvSolution)
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
}
```

## 🚀 Step 4: Run Simulation

```bash
# Run the simulation
icoFoam > log.icoFoam 2>&1 &

# Monitor progress
tail -f log.icoFoam

# Or monitor residuals
foamLog log.icoFoam
gnuplot -e "plot 'logs/Ux_0' with lines, 'logs/Uy_0' with lines, 'logs/p_0' with lines"
```

## 📊 Step 5: Post-Processing and Analysis

### Visualization with ParaView
```bash
# Generate ParaView files
foamToVTK

# Launch ParaView
paraview --data=VTK/
```

### Force Analysis
```python
#!/usr/bin/env python3
"""
Analyze force coefficients and calculate Strouhal number
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq

def analyze_forces(force_file):
    """Analyze force coefficient data"""
    
    # Read force coefficients
    data = np.loadtxt(force_file, comments='#')
    time = data[:, 0]
    cd = data[:, 1]
    cl = data[:, 2]
    
    # Skip initial transient (first 5 time units)
    start_idx = np.where(time >= 5.0)[0][0]
    time = time[start_idx:]
    cd = cd[start_idx:]
    cl = cl[start_idx:]
    
    # Calculate statistics
    cd_mean = np.mean(cd)
    cl_rms = np.sqrt(np.mean(cl**2))
    
    # Frequency analysis of lift coefficient
    dt = time[1] - time[0]
    frequencies = fftfreq(len(cl), dt)
    cl_fft = fft(cl - np.mean(cl))
    
    # Find dominant frequency
    positive_freq_idx = frequencies > 0
    power_spectrum = np.abs(cl_fft[positive_freq_idx])**2
    dominant_freq_idx = np.argmax(power_spectrum)
    dominant_freq = frequencies[positive_freq_idx][dominant_freq_idx]
    
    # Calculate Strouhal number
    U_inf = 1.0  # m/s
    D = 0.1      # m
    strouhal = dominant_freq * D / U_inf
    
    print(f"Mean drag coefficient: {cd_mean:.3f}")
    print(f"RMS lift coefficient: {cl_rms:.3f}")
    print(f"Dominant frequency: {dominant_freq:.3f} Hz")
    print(f"Strouhal number: {strouhal:.3f}")
    
    # Plotting
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    
    # Time series
    ax1.plot(time, cd, 'b-', linewidth=1)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Cd')
    ax1.set_title('Drag Coefficient')
    ax1.grid(True)
    
    ax2.plot(time, cl, 'r-', linewidth=1)
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Cl')
    ax2.set_title('Lift Coefficient')
    ax2.grid(True)
    
    # Power spectrum
    ax3.loglog(frequencies[positive_freq_idx], power_spectrum)
    ax3.axvline(dominant_freq, color='r', linestyle='--', 
                label=f'f = {dominant_freq:.3f} Hz')
    ax3.set_xlabel('Frequency [Hz]')
    ax3.set_ylabel('Power Spectrum')
    ax3.set_title('Lift Coefficient Spectrum')
    ax3.legend()
    ax3.grid(True)
    
    # Phase plot
    ax4.plot(cd, cl, 'g-', alpha=0.7, linewidth=0.5)
    ax4.set_xlabel('Cd')
    ax4.set_ylabel('Cl')
    ax4.set_title('Drag-Lift Phase Plot')
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig('force_analysis.png', dpi=300)
    plt.show()
    
    return cd_mean, cl_rms, strouhal

if __name__ == "__main__":
    force_file = "postProcessing/forceCoeffsIncompressible/0/forceCoeffs.dat"
    analyze_forces(force_file)
```

### Vorticity Visualization
```python
#!/usr/bin/env python3
"""
Calculate and visualize vorticity field
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def calculate_vorticity(u_file, v_file, x_file, y_file):
    """Calculate vorticity from velocity components"""
    
    # Load velocity and coordinate data
    u = np.loadtxt(u_file)
    v = np.loadtxt(v_file)
    x = np.loadtxt(x_file)
    y = np.loadtxt(y_file)
    
    # Calculate gradients (simplified finite difference)
    dudx, dudy = np.gradient(u)
    dvdx, dvdy = np.gradient(v)
    
    # Vorticity = dv/dx - du/dy
    vorticity = dvdx - dudy
    
    # Plotting
    plt.figure(figsize=(12, 6))
    
    # Vorticity contours
    levels = np.linspace(-10, 10, 21)
    contour = plt.contourf(x, y, vorticity, levels=levels, cmap='RdBu_r')
    plt.colorbar(contour, label='Vorticity [1/s]')
    
    # Add cylinder
    cylinder = Circle((0, 0), 0.05, color='black', fill=True)
    plt.gca().add_patch(cylinder)
    
    # Streamlines
    plt.streamplot(x, y, u, v, density=1, color='black', linewidth=0.5)
    
    plt.xlim(-0.5, 2.0)
    plt.ylim(-1.0, 1.0)
    plt.xlabel('x/D')
    plt.ylabel('y/D')
    plt.title('Vorticity Field and Streamlines')
    plt.axis('equal')
    plt.savefig('vorticity_field.png', dpi=300)
    plt.show()

# Usage (requires extracted field data)
# calculate_vorticity('U_x.dat', 'U_y.dat', 'x.dat', 'y.dat')
```

## ✅ Step 6: Validation

### Comparison with Literature
```python
#!/usr/bin/env python3
"""
Compare results with experimental/numerical data
"""

import matplotlib.pyplot as plt
import numpy as np

# Literature values for Re = 100
literature_data = {
    'Strouhal': {'value': 0.164, 'source': 'Williamson (1996)'},
    'Cd_mean': {'value': 1.35, 'source': 'Rajani et al. (2009)'},
    'Cl_rms': {'value': 0.25, 'source': 'Rajani et al. (2009)'}
}

# Your simulation results (to be filled)
simulation_results = {
    'Strouhal': 0.0,    # Fill from force analysis
    'Cd_mean': 0.0,     # Fill from force analysis  
    'Cl_rms': 0.0       # Fill from force analysis
}

def validate_results(sim_results, lit_data):
    """Compare simulation with literature"""
    
    parameters = list(lit_data.keys())
    lit_values = [lit_data[p]['value'] for p in parameters]
    sim_values = [sim_results[p] for p in parameters]
    
    # Calculate relative errors
    errors = [(sim - lit)/lit * 100 for sim, lit in zip(sim_values, lit_values)]
    
    # Create comparison plot
    x = np.arange(len(parameters))
    width = 0.35
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Values comparison
    ax1.bar(x - width/2, lit_values, width, label='Literature', alpha=0.7)
    ax1.bar(x + width/2, sim_values, width, label='Simulation', alpha=0.7)
    ax1.set_xlabel('Parameters')
    ax1.set_ylabel('Values')
    ax1.set_title('Simulation vs Literature')
    ax1.set_xticks(x)
    ax1.set_xticklabels(parameters)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Error plot
    colors = ['green' if abs(e) < 5 else 'orange' if abs(e) < 10 else 'red' 
              for e in errors]
    bars = ax2.bar(parameters, errors, color=colors, alpha=0.7)
    ax2.set_xlabel('Parameters')
    ax2.set_ylabel('Relative Error [%]')
    ax2.set_title('Validation Errors')
    ax2.axhline(y=5, color='orange', linestyle='--', alpha=0.7, label='±5%')
    ax2.axhline(y=-5, color='orange', linestyle='--', alpha=0.7)
    ax2.axhline(y=10, color='red', linestyle='--', alpha=0.7, label='±10%')
    ax2.axhline(y=-10, color='red', linestyle='--', alpha=0.7)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, error in zip(bars, errors):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1 if height >= 0 else height - 0.3,
                f'{error:.1f}%', ha='center', va='bottom' if height >= 0 else 'top')
    
    plt.tight_layout()
    plt.savefig('validation_comparison.png', dpi=300)
    plt.show()
    
    # Print validation summary
    print("\n=== VALIDATION SUMMARY ===")
    for param in parameters:
        lit_val = lit_data[param]['value']
        sim_val = sim_results[param]
        error = (sim_val - lit_val) / lit_val * 100
        source = lit_data[param]['source']
        
        print(f"{param}:")
        print(f"  Literature: {lit_val:.3f} ({source})")
        print(f"  Simulation: {sim_val:.3f}")
        print(f"  Error: {error:+.1f}%")
        print()

# Usage
# validate_results(simulation_results, literature_data)
```

## 📖 Expected Learning Outcomes

After completing this tutorial, you will have:

1. **Practical CFD Skills**:
   - Complete OpenFOAM workflow
   - Mesh generation and quality assessment
   - Boundary condition setup
   - Unsteady flow simulation

2. **Physical Understanding**:
   - Vortex shedding mechanisms
   - Reynolds number effects
   - Force coefficient interpretation
   - Strouhal number significance

3. **Analysis Capabilities**:
   - Time series analysis
   - Frequency domain analysis
   - Flow visualization techniques
   - Validation methodologies

4. **Best Practices**:
   - Case organization
   - Documentation standards
   - Result verification
   - Error quantification

## 🔍 Troubleshooting

### Common Issues:

1. **Convergence Problems**:
   - Reduce time step
   - Check mesh quality
   - Verify boundary conditions

2. **Unphysical Results**:
   - Check Reynolds number calculation
   - Verify reference values in force calculation
   - Ensure adequate domain size

3. **Mesh Quality Issues**:
   - Refine near cylinder
   - Improve aspect ratios
   - Check orthogonality

## 📚 Further Extensions

1. **Different Reynolds Numbers**: Re = 40, 200, 1000
2. **3D Simulation**: Add spanwise direction
3. **Turbulent Flow**: Use RANS models for high Re
4. **Moving Cylinder**: VIV (Vortex-Induced Vibration)
5. **Heat Transfer**: Add temperature equation

This tutorial provides a comprehensive foundation for CFD analysis of bluff body flows and can be adapted for various engineering applications.
