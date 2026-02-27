# ParaView Practice Guides

ParaView is an open-source, multi-platform application for interactive and batch visualization of scientific datasets. It is the standard tool for post-processing CFD results from OpenFOAM, SU2, and other solvers.

## Table of Contents

| Guide | Description | Level |
|-------|-------------|-------|
| [Introduction to ParaView](intro.md) | ParaView basics, OpenFOAM integration, Pipeline Browser, filters, glyphs, and state saving | Beginner |
| [Importing External Packages](import_external_packages.md) | Using virtual environments to bring `pandas`, `numpy`, and other packages into ParaView's `pvpython` | Intermediate |
| [Batch Visualization](batch_visualization.md) | Automated screenshot and animation generation using Python scripting | Intermediate |

## Why ParaView?

- **Handles massive datasets** — built for parallel rendering across hundreds of processors and billions of cells.
- **Rich filter library** — over 100 built-in filters for slicing, clipping, contouring, streamlines, glyphs, and more.
- **Python scriptable** — automate every aspect of visualization through `pvpython` or the built-in Python shell.
- **OpenFOAM native support** — read OpenFOAM cases directly via `paraFoam` or the built-in reader, or convert with `foamToVTK`.
- **Cross-platform** — runs on Linux, macOS, and Windows with identical functionality.
- **Free and open source** — developed by Kitware under a permissive BSD license.

## Quick Start

```bash
# Install on Ubuntu/Debian
sudo apt-get install paraview

# Open ParaView GUI
paraview

# Open an OpenFOAM case directly
paraFoam -case /path/to/openfoam/case

# Convert OpenFOAM data to VTK format first
foamToVTK -case /path/to/openfoam/case
paraview --data=/path/to/openfoam/case/VTK/
```

## Common Workflows

### Visualizing an OpenFOAM Simulation

```
1. Run your OpenFOAM solver (e.g., simpleFoam)
2. Launch:  paraFoam  or  foamToVTK && paraview
3. Select fields to display (p, U, k, epsilon, etc.)
4. Apply filters: Slice, Contour, Streamline, Glyph
5. Export screenshots or animations
```

### Automated Post-Processing with pvpython

```python
from paraview.simple import *

# Load OpenFOAM case
reader = OpenFOAMReader(FileName="/path/to/case/case.foam")
reader.MeshRegions = ["internalMesh"]
reader.CellArrays = ["p", "U"]

# Go to last timestep
animationScene = GetAnimationScene()
animationScene.GoToLast()

# Create a slice
slice1 = Slice(Input=reader)
slice1.SliceType.Origin = [0.5, 0.0, 0.0]
slice1.SliceType.Normal = [1, 0, 0]

# Color by pressure
display = Show(slice1)
ColorBy(display, ("CELLS", "p"))
display.RescaleTransferFunctionToDataRange()

# Save screenshot
SaveScreenshot("pressure_slice.png", magnification=2)
```

### Creating Animations

```python
from paraview.simple import *

reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["U"]

display = Show(reader)
ColorBy(display, ("CELLS", "U"))

view = GetActiveView()
view.ViewSize = [1920, 1080]

SaveAnimation("velocity_animation.avi",
              FrameRate=24,
              FrameWindow=[0, 100])
```

## Useful Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Space` | Toggle Apply button |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `R` | Reset camera |
| `+X`, `-X`, `+Y`, `-Y`, `+Z`, `-Z` | Set camera to axis view |
| `Ctrl+S` | Save state |
| `Delete` | Delete selected pipeline object |

## Resources

- [ParaView Homepage](https://www.paraview.org/) — downloads and documentation
- [ParaView Guide (PDF)](https://docs.paraview.org/en/latest/) — comprehensive user manual
- [ParaView Python API](https://kitware.github.io/paraview-docs/latest/python/) — scripting reference
- [ParaView Wiki](https://www.paraview.org/Wiki/ParaView) — community guides and tips
- [ParaView Discourse Forum](https://discourse.paraview.org/) — official support forum
