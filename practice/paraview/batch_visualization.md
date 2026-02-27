# Batch Visualization with ParaView Python Scripting

ParaView's Python interface (`pvpython`) lets you automate repetitive visualization tasks — generating screenshots, creating animations, extracting data, and producing publication-quality figures without touching the GUI. This guide covers practical recipes for common batch visualization workflows in CFD.

## Table of Contents

- [Getting Started with pvpython](#getting-started-with-pvpython)
- [Loading Data](#loading-data)
- [Creating Standard CFD Visualizations](#creating-standard-cfd-visualizations)
- [Generating Animations](#generating-animations)
- [Extracting Quantitative Data](#extracting-quantitative-data)
- [Publication-Quality Figures](#publication-quality-figures)
- [Batch Processing Multiple Cases](#batch-processing-multiple-cases)

## Getting Started with pvpython

### Running a Script

```bash
# Use ParaView's Python interpreter
pvpython my_script.py

# Or use the built-in Python shell in the GUI
# Tools → Python Shell
```

### Minimal Example

```python
from paraview.simple import *

# Create a sphere source
sphere = Sphere()
sphere.ThetaResolution = 32
sphere.PhiResolution = 32

# Show and render
Show(sphere)
Render()

# Save screenshot
SaveScreenshot("sphere.png", magnification=2)
```

## Loading Data

### OpenFOAM Cases

```python
from paraview.simple import *

# Method 1: Direct OpenFOAM reader (recommended)
reader = OpenFOAMReader(FileName="/path/to/case/case.foam")
reader.MeshRegions = ["internalMesh"]
reader.CellArrays = ["p", "U"]

# Method 2: After foamToVTK conversion
reader = LegacyVTKReader(FileNames=["VTK/case_500.vtk"])

# Method 3: VTK series
reader = XMLUnstructuredGridReader(FileName=["VTK/case_0.vtu",
                                              "VTK/case_100.vtu",
                                              "VTK/case_200.vtu"])
```

### Navigate Time Steps

```python
# Get animation scene
scene = GetAnimationScene()

# Go to last time step
scene.GoToLast()

# Go to specific time
scene.AnimationTime = 0.5

# Get available time steps
times = reader.TimestepValues
print(f"Available times: {times}")
```

### Other Formats

```python
# VTK files
reader = XMLUnstructuredGridReader(FileName=["mesh.vtu"])

# EnSight
reader = EnSightReader(CaseFileName="results.case")

# CSV data
reader = CSVReader(FileName=["data.csv"])
```

## Creating Standard CFD Visualizations

### Pressure Contour on a Slice

```python
from paraview.simple import *

# Load data
reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["p", "U"]
scene = GetAnimationScene()
scene.GoToLast()

# Create a slice at z = 0 (for 2D-like views)
slice1 = Slice(Input=reader)
slice1.SliceType = "Plane"
slice1.SliceType.Origin = [0, 0, 0]
slice1.SliceType.Normal = [0, 0, 1]

# Display and color by pressure
display = Show(slice1)
ColorBy(display, ("CELLS", "p"))
display.RescaleTransferFunctionToDataRange()

# Customize color bar
color_bar = GetScalarBar(GetColorTransferFunction("p"))
color_bar.Title = "Pressure [Pa]"
color_bar.ComponentTitle = ""

# Set view
view = GetActiveViewOrCreate("RenderView")
view.ViewSize = [1920, 1080]
view.Background = [1, 1, 1]  # white background
ResetCamera()

SaveScreenshot("pressure_slice.png", magnification=2)
```

### Velocity Streamlines

```python
from paraview.simple import *

reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["U"]
scene = GetAnimationScene()
scene.GoToLast()

# Create streamlines
stream = StreamTracerWithCustomSource(Input=reader)

# Create a seed line
line_source = Line()
line_source.Point1 = [-1, -0.5, 0]
line_source.Point2 = [-1, 0.5, 0]
line_source.Resolution = 50

stream.SeedType = "Point Cloud"
stream = StreamTracerWithCustomSource(Input=reader, SeedSource=line_source)
stream.MaximumStreamlineLength = 20.0

display = Show(stream)
ColorBy(display, ("POINTS", "U", "Magnitude"))
display.RescaleTransferFunctionToDataRange()

view = GetActiveViewOrCreate("RenderView")
view.Background = [1, 1, 1]
ResetCamera()

SaveScreenshot("streamlines.png", magnification=2)
```

### Velocity Vector Field (Glyphs)

```python
from paraview.simple import *

reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["U"]
scene = GetAnimationScene()
scene.GoToLast()

# Slice first (glyphs on full 3D domain would be too dense)
slice1 = Slice(Input=reader)
slice1.SliceType.Normal = [0, 0, 1]

# Apply glyph filter
glyph = Glyph(Input=slice1)
glyph.GlyphType = "Arrow"
glyph.OrientationArray = ["CELLS", "U"]
glyph.ScaleArray = ["CELLS", "U"]
glyph.ScaleFactor = 0.05
glyph.GlyphMode = "Every Nth Point"
glyph.Stride = 5

display = Show(glyph)
ColorBy(display, ("CELLS", "U", "Magnitude"))

view = GetActiveViewOrCreate("RenderView")
view.Background = [1, 1, 1]
ResetCamera()

SaveScreenshot("velocity_glyphs.png", magnification=2)
```

### Iso-Surfaces (e.g., Vortex Identification)

```python
from paraview.simple import *

reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["U", "p"]
scene = GetAnimationScene()
scene.GoToLast()

# Compute vorticity (Q-criterion)
calc = Calculator(Input=reader)
calc.Function = "0.5*(mag(curl(U))^2 - mag(strain(U))^2)"
calc.ResultArrayName = "Q_criterion"

# Create iso-surface at Q = 100
iso = Contour(Input=calc)
iso.ContourBy = ["POINTS", "Q_criterion"]
iso.Isosurfaces = [100.0]

display = Show(iso)
ColorBy(display, ("POINTS", "U", "Magnitude"))

view = GetActiveViewOrCreate("RenderView")
view.Background = [0.2, 0.2, 0.3]
ResetCamera()

SaveScreenshot("q_criterion.png", magnification=2)
```

## Generating Animations

### Time-Series Animation

```python
from paraview.simple import *

reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["U"]

display = Show(reader)
ColorBy(display, ("CELLS", "U", "Magnitude"))
display.RescaleTransferFunctionToDataRange()

view = GetActiveViewOrCreate("RenderView")
view.ViewSize = [1920, 1080]
view.Background = [1, 1, 1]
ResetCamera()

# Save as AVI
SaveAnimation("velocity_animation.avi",
              view,
              FrameRate=24,
              FrameWindow=[0, len(reader.TimestepValues) - 1])

# Or save as individual frames (PNG sequence)
SaveAnimation("frames/frame.png",
              view,
              FrameRate=24,
              ImageResolution=[1920, 1080])
```

### Camera Orbit Animation

```python
from paraview.simple import *

reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["p"]
scene = GetAnimationScene()
scene.GoToLast()

display = Show(reader)
ColorBy(display, ("CELLS", "p"))

view = GetActiveViewOrCreate("RenderView")
view.ViewSize = [1920, 1080]

# Create camera orbit
scene.NumberOfFrames = 120
camera = GetActiveCamera()

for i in range(120):
    camera.Azimuth(3)  # 3 degrees per frame = 360 degree orbit
    Render()
    SaveScreenshot(f"orbit/frame_{i:04d}.png", magnification=2)
```

## Extracting Quantitative Data

### Line Probe

```python
from paraview.simple import *

reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["U", "p"]
scene = GetAnimationScene()
scene.GoToLast()

# Create line probe along y-axis
probe = PlotOverLine(Input=reader)
probe.Point1 = [0.05, 0.0, 0.005]
probe.Point2 = [0.05, 0.1, 0.005]
probe.Resolution = 200

# Save to CSV
writer = CreateWriter("centerline_data.csv", proxy=probe)
writer.FieldAssociation = "Point Data"
writer.UpdatePipeline()
del writer
```

### Point Probe

```python
from paraview.simple import *

reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["p", "U"]

# Probe at a specific point
probe = ProbeLocation(Input=reader, ProbeType="Fixed Radius Point Source")
probe.ProbeType.Center = [0.5, 0.0, 0.0]

# Get values at each time step
times = reader.TimestepValues
scene = GetAnimationScene()

p_values = []
for t in times:
    scene.AnimationTime = t
    data = servermanager.Fetch(probe)
    p_val = data.GetPointData().GetArray("p").GetValue(0)
    p_values.append((t, p_val))

# Write to file
import csv
with open("point_probe.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "pressure"])
    writer.writerows(p_values)
```

## Publication-Quality Figures

### Customizing Appearance

```python
from paraview.simple import *

reader = OpenFOAMReader(FileName="case.foam")
reader.CellArrays = ["p"]
scene = GetAnimationScene()
scene.GoToLast()

slice1 = Slice(Input=reader)
slice1.SliceType.Normal = [0, 0, 1]

display = Show(slice1)
ColorBy(display, ("CELLS", "p"))

# Customize color transfer function
lut = GetColorTransferFunction("p")
lut.ApplyPreset("Cool to Warm", True)
lut.RescaleTransferFunction(-100, 100)

# Customize color bar
color_bar = GetScalarBar(lut)
color_bar.Title = "Pressure"
color_bar.ComponentTitle = "[Pa]"
color_bar.TitleFontSize = 18
color_bar.LabelFontSize = 14
color_bar.ScalarBarLength = 0.4
color_bar.Position = [0.85, 0.25]

# View settings for clean output
view = GetActiveViewOrCreate("RenderView")
view.ViewSize = [1600, 1200]
view.Background = [1, 1, 1]
view.OrientationAxesVisibility = 0  # Hide axes widget

# Camera position for 2D-like view
view.CameraPosition = [0, 0, 10]
view.CameraFocalPoint = [0, 0, 0]
view.CameraViewUp = [0, 1, 0]
view.CameraParallelScale = 1.5
view.CameraParallelProjection = True

ResetCamera()
SaveScreenshot("publication_figure.png",
               magnification=2,
               TransparentBackground=1)
```

### Adding Annotations

```python
# Add a text annotation
text = Text()
text.Text = "Re = 1000, t = 5.0 s"
text_display = Show(text)
text_display.FontSize = 18
text_display.Position = [0.02, 0.95]
text_display.Color = [0, 0, 0]
```

## Batch Processing Multiple Cases

### Process All Cases in a Directory

```python
#!/usr/bin/env python3
"""
Batch process multiple OpenFOAM cases and generate comparison screenshots.
"""

import os
import glob
from paraview.simple import *

def process_case(case_dir, output_dir):
    """Generate standard visualizations for one case."""
    case_name = os.path.basename(case_dir)
    foam_file = os.path.join(case_dir, f"{case_name}.foam")

    # Create .foam file if it doesn't exist
    if not os.path.exists(foam_file):
        foam_file = os.path.join(case_dir, "case.foam")
        open(foam_file, "w").close()

    reader = OpenFOAMReader(FileName=foam_file)
    reader.CellArrays = ["p", "U"]

    scene = GetAnimationScene()
    scene.GoToLast()

    # Pressure contour
    slice1 = Slice(Input=reader)
    slice1.SliceType.Normal = [0, 0, 1]
    display = Show(slice1)
    ColorBy(display, ("CELLS", "p"))
    display.RescaleTransferFunctionToDataRange()

    view = GetActiveViewOrCreate("RenderView")
    view.ViewSize = [1920, 1080]
    view.Background = [1, 1, 1]
    ResetCamera()

    output_file = os.path.join(output_dir, f"{case_name}_pressure.png")
    SaveScreenshot(output_file, magnification=2)

    # Clean up for next case
    Delete(slice1)
    Delete(reader)

    print(f"Processed: {case_name}")

# Main
output_dir = "batch_results"
os.makedirs(output_dir, exist_ok=True)

case_dirs = sorted(glob.glob("cavity_Re*"))
for case_dir in case_dirs:
    if os.path.isdir(case_dir):
        process_case(case_dir, output_dir)

print(f"All cases processed. Results in {output_dir}/")
```

Run with:

```bash
pvpython batch_visualize.py
```

### Comparison Layout

```python
from paraview.simple import *

# Create a layout with multiple views for side-by-side comparison
layout = CreateLayout()

# View 1: Low Re
view1 = CreateRenderView()
layout.AssignView(0, view1)

# View 2: High Re  
layout.SplitHorizontal(0, 0.5)
view2 = CreateRenderView()
layout.AssignView(2, view2)

# Load and display case 1 in view1
SetActiveView(view1)
reader1 = OpenFOAMReader(FileName="cavity_Re100/case.foam")
reader1.CellArrays = ["U"]
display1 = Show(reader1, view1)
ColorBy(display1, ("CELLS", "U", "Magnitude"))

# Load and display case 2 in view2
SetActiveView(view2)
reader2 = OpenFOAMReader(FileName="cavity_Re1000/case.foam")
reader2.CellArrays = ["U"]
display2 = Show(reader2, view2)
ColorBy(display2, ("CELLS", "U", "Magnitude"))

# Link cameras so they rotate together
AddCameraLink(view1, view2, "link1")

SaveScreenshot("comparison.png", layout, ImageResolution=[3840, 1080])
```

## Resources

- [ParaView Python API Reference](https://kitware.github.io/paraview-docs/latest/python/)
- [ParaView Trace](https://docs.paraview.org/en/latest/Tutorials/ClassroomTutorials/pythonAndBatchParaViewAndPython.html) — record GUI actions as Python scripts via `Tools → Start Trace`
- [ParaView Examples](https://examples.paraview.org/) — gallery of visualization examples with code
