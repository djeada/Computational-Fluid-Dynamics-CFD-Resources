# Gmsh Practice Guides

Gmsh is a versatile open-source 3D finite element mesh generator with a built-in CAD engine, scripting language, and post-processing facilities. These guides cover everything from basic mesh generation to advanced volume meshing workflows.

## Table of Contents

| Guide | Description | Level |
|-------|-------------|-------|
| [Introduction to Gmsh](intro.md) | Installation, basic workflow, scripting fundamentals, and the `.geo` language | Beginner |
| [Volume Mesh Generation](generate_volume_mesh.md) | Generating 3D volume meshes from STL files, quality control, and Python API usage | Intermediate |
| [Boolean Operations](boolean_operations.md) | Combining, cutting, and fragmenting geometries using OpenCASCADE boolean operations | Intermediate |

## Why Gmsh?

Gmsh stands out among meshing tools for several reasons:

- **Free and open source** under the GPL, with active development since 1997.
- **Built-in CAD engine** plus full OpenCASCADE integration for importing STEP/IGES files.
- **Scriptable** via the `.geo` language or through Python, C++, and Julia APIs.
- **Cross-platform** support for Linux, macOS, and Windows.
- **1D/2D/3D meshing** with Delaunay, frontal, and hybrid algorithms.
- **Boundary layer support** for CFD applications requiring anisotropic near-wall meshes.

## Quick Start

```bash
# Install on Ubuntu/Debian
sudo apt-get install gmsh

# Verify installation
gmsh --version

# Generate a 3D mesh from a .geo file
gmsh geometry.geo -3 -o mesh.msh

# Launch the GUI
gmsh
```

## Common Workflows

### CAD Import → Mesh → Export

```bash
# Import STEP, mesh in 3D, export for OpenFOAM
gmsh model.step -3 -format msh2 -o model.msh
gmshToFoam model.msh
```

### Parametric Meshing with the Python API

```python
import gmsh

gmsh.initialize()
gmsh.model.add("box")

# Create a box with the OpenCASCADE kernel
gmsh.model.occ.addBox(0, 0, 0, 1, 0.5, 0.3)
gmsh.model.occ.synchronize()

# Set mesh size and generate
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.05)
gmsh.model.mesh.generate(3)

gmsh.write("box.msh")
gmsh.finalize()
```

### STL Repair → Volume Mesh

```bash
# Reclassify an STL surface and generate a volume mesh
gmsh stl_to_volume.geo -3 -optimize_netgen -o part.msh
```

See [Volume Mesh Generation](generate_volume_mesh.md) for a full walkthrough.

## Useful Command-Line Flags

| Flag | Purpose |
|------|---------|
| `-1`, `-2`, `-3` | Generate 1D, 2D, or 3D mesh |
| `-o <file>` | Specify output file |
| `-format msh2` | Force MSH version 2 output (OpenFOAM compatible) |
| `-optimize` | Optimize mesh quality after generation |
| `-optimize_netgen` | Use Netgen-based optimization (often better for tets) |
| `-clscale <factor>` | Scale all characteristic lengths by a factor |
| `-part <N>` | Partition mesh into N parts for parallel solvers |
| `-setnumber <name> <val>` | Set a numeric variable for parametric scripts |
| `-check` | Print mesh statistics and quality info |
| `-v <N>` | Set verbosity level (0–99) |

## Resources

- [Gmsh Homepage](http://gmsh.info) — downloads, documentation, and tutorials
- [Gmsh Reference Manual](http://gmsh.info/doc/texinfo/gmsh.html) — complete command and API reference
- [Gmsh Tutorials](http://gmsh.info/#Tutorials) — official step-by-step examples
- [Gmsh Python API](http://gmsh.info/doc/texinfo/gmsh.html#Gmsh-API) — Python bindings documentation
- [Gmsh GitLab Repository](https://gitlab.onelab.info/gmsh/gmsh) — source code and issue tracker
