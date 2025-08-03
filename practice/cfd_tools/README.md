# Open Source CFD Tools Comprehensive Guide

This directory contains detailed information about open-source computational fluid dynamics (CFD) tools, their capabilities, installation procedures, and usage examples.

## Table of Contents

- [Solver Comparison](#solver-comparison)
- [Pre-Processing Tools](#pre-processing-tools)
- [Post-Processing Tools](#post-processing-tools)
- [Meshing Tools](#meshing-tools)
- [Specialized Tools](#specialized-tools)
- [Workflow Integration](#workflow-integration)
- [Performance Comparison](#performance-comparison)

## Solver Comparison

### Major Open Source CFD Solvers

| Solver | License | Language | Strengths | Applications |
|--------|---------|----------|-----------|--------------|
| **OpenFOAM** | GPL | C++ | General purpose, large community | All CFD applications |
| **SU2** | LGPL | C++ | Optimization, adjoint methods | Design optimization |
| **Code_Saturne** | GPL | C/Fortran | Industrial applications | Power, nuclear, HVAC |
| **Nek5000/NekRS** | BSD | Fortran/C++ | High-order methods, HPC | DNS, LES, research |
| **FEniCS** | LGPL | Python/C++ | Finite elements, multiphysics | Research, coupled problems |
| **deal.II** | LGPL | C++ | Advanced FEM, adaptive | Research, education |

### Detailed Solver Profiles

#### OpenFOAM
```yaml
Website: https://www.openfoam.org/
Repository: https://github.com/OpenFOAM/OpenFOAM-dev
Community: Very large (100k+ users)
Learning Curve: Moderate
Documentation: Excellent

Capabilities:
  - Incompressible/compressible flows
  - Multiphase flows
  - Turbulence (RANS, LES, DNS)
  - Heat transfer
  - Chemical reactions
  - Particle tracking
  - Electromagnetics

Solvers:
  - simpleFoam: Steady incompressible
  - pimpleFoam: Transient incompressible
  - rhoCentralFoam: Compressible
  - interFoam: Multiphase VOF
  - reactingFoam: Combustion
```

#### SU2
```yaml
Website: https://su2code.github.io/
Repository: https://github.com/su2code/SU2
Community: Medium (academic focus)
Learning Curve: Moderate
Documentation: Good

Capabilities:
  - Compressible/incompressible flows
  - Adjoint-based optimization
  - Shape optimization
  - Fluid-structure interaction
  - Heat transfer
  - Turbomachinery

Strengths:
  - Automatic differentiation
  - Design optimization
  - High-performance computing
  - Multiple physics coupling
```

#### Code_Saturne
```yaml
Website: https://www.code-saturne.org/
Developer: EDF (Électricité de France)
License: GPL v2
Community: Industrial focus
Learning Curve: Steep
Documentation: Industrial quality

Capabilities:
  - Incompressible/compressible flows
  - Heat transfer with radiation
  - Turbomachinery
  - Atmospheric flows
  - Conjugate heat transfer
  - Lagrangian particle tracking

Applications:
  - Nuclear reactor thermal hydraulics
  - Power plant flows
  - HVAC systems
  - Environmental flows
```

## Installation Guides

### OpenFOAM Installation

#### Ubuntu/Debian
```bash
# Official repository method
sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key | apt-key add -"
sudo add-apt-repository http://dl.openfoam.org/ubuntu
sudo apt-get update
sudo apt-get install openfoam11

# Source environment
echo "source /opt/openfoam11/etc/bashrc" >> ~/.bashrc
source ~/.bashrc
```

#### Docker Installation
```bash
# Pull image
docker pull openfoam/openfoam11-paraview510

# Run container
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd):/workspace openfoam/openfoam11-paraview510
```

#### Compilation from Source
```bash
# Dependencies
sudo apt-get install build-essential cmake git ca-certificates
sudo apt-get install libopenmpi-dev openmpi-bin
sudo apt-get install libboost-system-dev libboost-thread-dev
sudo apt-get install libcgal-dev

# Download source
git clone https://github.com/OpenFOAM/OpenFOAM-dev.git
cd OpenFOAM-dev

# Compile
source etc/bashrc
./Allwmake -j 4
```

### SU2 Installation

```bash
# Dependencies
sudo apt-get install build-essential python3-dev python3-numpy
sudo apt-get install libopenmpi-dev openmpi-bin

# Download and compile
git clone https://github.com/su2code/SU2.git
cd SU2
./meson.py build --prefix=/usr/local
./ninja -C build install

# Python modules
pip3 install mpi4py
```

### Code_Saturne Installation

```bash
# Dependencies
sudo apt-get install gfortran gcc g++ python3-dev
sudo apt-get install libopenmpi-dev libhdf5-dev libcgns-dev
sudo apt-get install libmed-dev libmetis-dev

# Download
wget https://www.code-saturne.org/releases/code_saturne-7.0.3.tar.gz
tar xzf code_saturne-7.0.3.tar.gz
cd code_saturne-7.0.3

# Configure and compile
./configure --prefix=/usr/local/code_saturne
make
sudo make install
```

## Pre-Processing Tools

### Geometry and CAD

#### FreeCAD
```yaml
Purpose: Parametric 3D CAD modeler
License: LGPL
Installation: sudo apt install freecad
Formats: STEP, IGES, STL, OBJ
CFD Integration: Direct export to mesh generators
```

#### OpenSCAD
```yaml
Purpose: Script-based 3D CAD
License: GPL
Installation: sudo apt install openscad
Strength: Parametric, version control friendly
Usage: Geometric primitives via scripting
```

#### Salome Platform
```yaml
Purpose: Complete CAD-to-simulation platform
License: LGPL
Features: 
  - GEOM: Geometry creation/import
  - MESH: Advanced meshing
  - YACS: Workflow orchestration
Installation: Download from salome-platform.org
```

### Meshing Tools Detailed

#### Gmsh
```bash
# Installation
sudo apt install gmsh

# Basic usage
gmsh geometry.geo -3 -o mesh.msh

# Python API
python3 -c "
import gmsh
gmsh.initialize()
gmsh.open('model.step')
gmsh.model.mesh.generate(3)
gmsh.write('mesh.msh')
gmsh.finalize()
"
```

#### Netgen
```bash
# Installation
sudo apt install netgen

# Python usage
python3 -c "
import netgen.csg as csg
from netgen.meshing import *

geo = csg.CSGeometry()
sphere = csg.Sphere((0,0,0), 1)
geo.Add(sphere)

mesh = geo.GenerateMesh(maxh=0.1)
mesh.Export('sphere.msh', 'Gmsh2 Format')
"
```

## Post-Processing Tools

### ParaView
```yaml
Installation: sudo apt install paraview
Capabilities:
  - Large dataset visualization
  - Parallel rendering
  - Custom filters
  - Animation
  - Python scripting

OpenFOAM Integration:
  - paraFoam: Native reader
  - foamToVTK: Export utility
  - reconstructPar: Parallel reconstruction
```

### VisIt
```yaml
Installation: Download from visit.llnl.gov
Strengths:
  - Extremely large datasets
  - Advanced visualization
  - Remote visualization
  - Scripting interface

Usage:
  visit -cli -s script.py
```

### Matplotlib (Python)
```python
# CFD-specific plotting
import matplotlib.pyplot as plt
import numpy as np

# Residual plotting
def plot_residuals(logfile):
    data = np.loadtxt(logfile, skiprows=1)
    plt.semilogy(data[:, 0], data[:, 1], label='Ux')
    plt.semilogy(data[:, 0], data[:, 2], label='Uy')
    plt.semilogy(data[:, 0], data[:, 3], label='p')
    plt.xlabel('Iteration')
    plt.ylabel('Residual')
    plt.legend()
    plt.show()
```

## Workflow Automation

### Python Workflow Framework
```python
#!/usr/bin/env python3
"""
CFD Workflow Automation Framework
"""

import os
import subprocess
import numpy as np
from pathlib import Path

class CFDWorkflow:
    def __init__(self, case_name):
        self.case_name = case_name
        self.case_dir = Path(case_name)
        
    def setup_case(self, template_dir):
        """Copy template case"""
        import shutil
        if self.case_dir.exists():
            shutil.rmtree(self.case_dir)
        shutil.copytree(template_dir, self.case_dir)
        
    def generate_mesh(self, mesh_size=0.1):
        """Generate mesh with specified size"""
        os.chdir(self.case_dir)
        
        # Modify blockMeshDict
        self.modify_mesh_size(mesh_size)
        
        # Generate mesh
        subprocess.run(['blockMesh'], check=True)
        subprocess.run(['checkMesh'], check=True)
        
    def run_simulation(self, solver='simpleFoam', parallel=False, np=4):
        """Run CFD simulation"""
        os.chdir(self.case_dir)
        
        if parallel:
            subprocess.run(['decomposePar'], check=True)
            subprocess.run(['mpirun', '-np', str(np), solver, '-parallel'], 
                         check=True)
            subprocess.run(['reconstructPar'], check=True)
        else:
            subprocess.run([solver], check=True)
            
    def post_process(self):
        """Extract results"""
        os.chdir(self.case_dir)
        
        # Sample data
        subprocess.run(['sample'], check=True)
        
        # Calculate forces
        subprocess.run([solver, '-postProcess', '-func', 'forceCoeffs'], 
                      check=True)
        
    def extract_forces(self):
        """Extract force coefficients"""
        force_file = self.case_dir / 'postProcessing/forceCoeffs/0/forceCoeffs.dat'
        if force_file.exists():
            data = np.loadtxt(force_file, comments='#')
            return data[-1, 1], data[-1, 2]  # Cd, Cl
        return None, None

# Usage example
if __name__ == "__main__":
    # Mesh convergence study
    mesh_sizes = [0.1, 0.05, 0.025]
    results = []
    
    for size in mesh_sizes:
        workflow = CFDWorkflow(f'case_mesh_{size}')
        workflow.setup_case('template_case')
        workflow.generate_mesh(size)
        workflow.run_simulation()
        workflow.post_process()
        
        cd, cl = workflow.extract_forces()
        results.append((size, cd, cl))
        
    # Plot convergence
    import matplotlib.pyplot as plt
    sizes, cds, cls = zip(*results)
    
    plt.figure()
    plt.semilogx(sizes, cds, 'o-', label='Cd')
    plt.semilogx(sizes, cls, 's-', label='Cl')
    plt.xlabel('Mesh Size')
    plt.ylabel('Force Coefficient')
    plt.legend()
    plt.grid(True)
    plt.savefig('mesh_convergence.png')
```

### Bash Automation Scripts

#### Parametric Study Script
```bash
#!/bin/bash
# parametric_study.sh

# Parameters to vary
VELOCITIES=(1 2 5 10 20)
VISCOSITIES=(0.001 0.01 0.1)

# Template case
TEMPLATE="template_case"

for vel in "${VELOCITIES[@]}"; do
    for visc in "${VISCOSITIES[@]}"; do
        # Create case name
        CASE="case_U${vel}_nu${visc}"
        
        echo "Running case: $CASE"
        
        # Copy template
        cp -r $TEMPLATE $CASE
        cd $CASE
        
        # Modify boundary conditions
        sed -i "s/VELOCITY_VALUE/$vel/g" 0/U
        sed -i "s/VISCOSITY_VALUE/$visc/g" constant/transportProperties
        
        # Run simulation
        blockMesh > log.blockMesh 2>&1
        simpleFoam > log.simpleFoam 2>&1
        
        # Extract results
        sample > log.sample 2>&1
        
        # Calculate Reynolds number
        RE=$(echo "scale=0; $vel * 1.0 / $visc" | bc)
        echo "Re = $RE, Cd = $(tail -1 postProcessing/forceCoeffs/*/forceCoeffs.dat | awk '{print $2}')" >> ../results.dat
        
        cd ..
    done
done

# Plot results
python3 plot_results.py
```

## Performance Optimization

### OpenFOAM Performance Tips

#### Parallel Scaling
```bash
# Domain decomposition methods
decomposePar -method scotch        # Good load balancing
decomposePar -method simple        # Simple geometric
decomposePar -method hierarchical  # Hierarchical
decomposePar -method manual        # Manual specification
```

#### Linear Solver Settings
```cpp
// system/fvSolution - optimized for performance
solvers
{
    p
    {
        solver          GAMG;
        tolerance       1e-06;
        relTol          0.1;
        smoother        GaussSeidel;
        nPreSweeps      0;
        nPostSweeps     2;
        cacheAgglomeration on;
        agglomerator    faceAreaPair;
        nCellsInCoarsestLevel 10;
        mergeLevels     1;
    }
    
    U
    {
        solver          smoothSolver;
        smoother        GaussSeidel;
        tolerance       1e-05;
        relTol          0.1;
    }
}
```

### Memory Optimization
```bash
# Reduce memory usage
export FOAM_SIGFPE=false           # Disable floating point exceptions
export WM_COMPILE_OPTION=Opt       # Optimized compilation
ulimit -s unlimited                # Unlimited stack size
```

## Integration Examples

### OpenFOAM + Python Integration
```python
# PyFoam integration
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Field
from PyFoam.Applications.Runner import Runner

# Run simulation
case = SolutionDirectory("cavity")
runner = Runner(argv=["simpleFoam", "-case", "cavity"])
runner.start()

# Read results
sol = SolutionDirectory("cavity")
latest_time = sol.getLast()
p_field = Field(sol[latest_time]["p"])
print(f"Max pressure: {p_field.max()}")
```

### Automated Optimization Loop
```python
import scipy.optimize as opt

def objective_function(params):
    """Objective function for optimization"""
    inlet_velocity, viscosity = params
    
    # Setup and run CFD case
    workflow = CFDWorkflow('optimization_case')
    workflow.setup_case('template')
    workflow.modify_parameters(inlet_velocity, viscosity)
    workflow.run_simulation()
    
    # Extract objective (e.g., drag coefficient)
    cd, _ = workflow.extract_forces()
    return cd

# Optimization bounds
bounds = [(0.1, 10.0), (1e-6, 1e-3)]  # velocity, viscosity

# Optimize
result = opt.minimize(objective_function, x0=[1.0, 1e-5], bounds=bounds)
print(f"Optimal parameters: {result.x}")
```

This comprehensive guide provides the foundation for working with open-source CFD tools effectively, from basic usage to advanced workflow automation.
