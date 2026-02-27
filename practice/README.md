# Practice Section - CFD Tools and Resources

This directory contains practical tutorials, guides, and resources for computational fluid dynamics (CFD) tools, mesh generation, and open-source software. Each subdirectory focuses on specific tools and workflows commonly used in CFD practice.

## Table of Contents

- [Directory Structure](#directory-structure)
- [Recommended Learning Path](#recommended-learning-path)
- [Useful YouTube Resources](#useful-youtube-resources)
- [Getting Started](#getting-started)
- [Tools Covered](#tools-covered)

## Directory Structure

### 📐 [gmsh/](./gmsh/)
Comprehensive guides for Gmsh mesh generation
- [Introduction to Gmsh](gmsh/intro.md) — fundamentals, workflow, and scripting
- [Volume Mesh Generation](gmsh/generate_volume_mesh.md) — STL to volume mesh workflow
- [Boolean Operations](gmsh/boolean_operations.md) — union, cut, intersect, and fragment geometries

### 📊 [paraview/](./paraview/)
ParaView visualization and post-processing
- [Introduction to ParaView](paraview/intro.md) — GUI basics, filters, and OpenFOAM integration
- [Importing External Packages](paraview/import_external_packages.md) — using pandas/numpy with pvpython
- [Batch Visualization](paraview/batch_visualization.md) — automated screenshots, animations, and data extraction

### 🔧 [openfoam/](./openfoam/)
OpenFOAM CFD solver tutorials and workflows
- [Getting Started](openfoam/getting_started.md) — lid-driven cavity tutorial with validation
- [Turbulence Modeling](openfoam/turbulence_modeling.md) — RANS/LES setup, wall treatment, and worked examples

### 🌊 [mesh_generation/](./mesh_generation/)
3D mesh generation tools and techniques
- [Boundary Layer Meshing](mesh_generation/boundary_layers.md) — y+ calculations and layer generation
- [Mesh Quality Assessment](mesh_generation/mesh_quality.md) — metrics, tools, and automated reporting

### 🚀 [cfd_tools/](./cfd_tools/)
Collection of open-source CFD tools
- [Solver Comparison](cfd_tools/solver_comparison.md) — decision guide for choosing a CFD solver
- [Workflow Automation](cfd_tools/automation.md) — Python/Bash frameworks for parametric studies

### 🎯 [manual_projects/](./manual_projects/)
Hands-on CFD projects and case studies
- [Lid-Driven Cavity](manual_projects/lid_driven_cavity.md) — benchmark tutorial with Ghia et al. validation
- [Flow Over Cylinder](manual_projects/flow_over_cylinder.md) — vortex shedding analysis at Re=100

## Recommended Learning Path

1. **Start with Mesh Generation** - Begin with `gmsh/` to understand mesh fundamentals
2. **Learn Visualization** - Move to `paraview/` for post-processing skills
3. **CFD Solver Basics** - Explore `openfoam/` for simulation workflows
4. **Advanced Topics** - Dive into `cfd_tools/` for specialized applications
5. **Practical Projects** - Apply knowledge with `manual_projects/`

## Useful YouTube Resources

### ParaView and Visualization
* [Paraview Intro](https://www.youtube.com/watch?v=yexB3W2FYM0)
* [Postprocessing using ParaView](https://youtube.com/playlist?list=PL6fjYEpJFi7W6ayU8zKi7G0-EZmkjtbPo)
* [Pull your own data into ParaView](https://www.youtube.com/watch?v=RVgiIBuwpPQ)

### CFD and Mesh Generation
* [OpenFOAM Tutorial Series](https://www.youtube.com/playlist?list=PLcOe4WUSsMkH6DLHpsYyveaqjKxnEnQqB)
* [Gmsh Meshing Techniques](https://www.youtube.com/watch?v=X4pCWkSqSEk)
* [CFD Fundamentals](https://www.youtube.com/playlist?list=PL30F4C5ABCE62CB61)

## Getting Started

Each subdirectory contains detailed README files and tutorials. For beginners, we recommend starting with:

1. `gmsh/intro.md` - Understanding mesh generation basics
2. `paraview/intro.md` - Learning visualization fundamentals
3. `openfoam/getting_started.md` - First CFD simulation

## Tools Covered

- **Gmsh** - 3D finite element mesh generator
- **ParaView** - Data analysis and visualization
- **OpenFOAM** - CFD simulation toolbox
- **Salome** - CAD and meshing platform
- **Code_Saturne** - CFD solver
- **SU2** - Multiphysics simulation suite
- **FEniCS** - Finite element computing platform
- **And many more...**
