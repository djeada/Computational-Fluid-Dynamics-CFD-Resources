## Introduction to Gmsh

Gmsh is a versatile 3D finite element mesh generator that combines a built-in CAD engine, user-friendly visualization tools, and powerful scripting capabilities. It is used extensively in academia and industry for creating meshes of complex geometries, preprocessing and postprocessing simulation data, and automating large-scale parametric studies.  

### Table of Contents

- [Key Features](#key-features)
- [Installation](#installation)
- [Basic Workflow](#basic-workflow)
- [Scripting with Gmsh](#scripting-with-gmsh)
- [Python API](#python-api)
- [Advanced Topics](#advanced-topics)
- [Resources](#resources)

### Key Features

I. **CAD Integration**  
   - Supports points, lines, curves, surfaces, and volumes.
   - Users can directly define or import geometry, and then apply transformations, extrusions, or Boolean operations.
II. **Meshing Capabilities**  
   - Supports **1D**, **2D**, and **3D** meshing with robust algorithms (e.g., Delaunay, frontal, etc.) for high-quality triangulations and tetrahedral meshes.  
   - Offers structured/recombined quadrilateral meshing when feasible and can generate boundary-layer meshes for CFD applications.
III. **Post-processing**  
   - Gmsh can visualize scalar/vector fields, display isosurfaces, streamlines, etc.  
   - Allows custom rendering options, animations, and color maps. It can also export plots or images for publication.
IV. **Scripting Language**  
   - A built-in *.geo* scripting language automates geometry creation, meshing parameters, and repetitive tasks.  
   - Gmsh can also be controlled via an API (e.g., Python, C++, Julia) for seamless integration into larger workflows.
V. **User Interface**  
   - Intuitive menu-driven environment, enabling direct manipulation of geometry, meshing parameters, and post-processing settings.
   - Ideal for batch processing, large parametric studies, or remote HPC clusters.

### Installation

Gmsh runs on **Windows**, **macOS**, and **Linux**. Below are common installation paths:

I. **Download**  
   - Visit [gmsh.info](http://gmsh.info) to download the latest release.
II. **Installation Steps**  
   - Run the executable (.exe) installer and follow prompts.
   - Mount the disk image (.dmg) and drag Gmsh into your Applications folder.
   - Many distributions include Gmsh in their repositories (`sudo apt-get install gmsh` on Ubuntu/Debian), or compile from source for maximum flexibility.
III. **Verification**  
   - Open a terminal or command prompt and type `gmsh --version` to confirm a successful installation.

### Basic Workflow

A typical workflow in Gmsh comprises: (1) **geometry creation** or import, (2) **meshing**, and (3) **analysis/post-processing**. While many variations exist, the fundamental steps remain consistent.

#### 1. Creating a Geometry

**Points**  
- Fundamental entities in Gmsh, defined by `(x, y, z, characteristic_length)`.  

  ```plaintext
  lc = 0.1;    // characteristic length scale
  Point(1) = {0,   0,   0, lc};
  Point(2) = {1.0, 0,   0, lc};
  Point(3) = {1.0, 1.0, 0, lc};
  Point(4) = {0,   1.0, 0, lc};
  ```
**Lines & Curves**  
- Connect points to form edges or boundaries.

  ```plaintext
  Line(1) = {1, 2};
  Line(2) = {2, 3};
  Line(3) = {3, 4};
  Line(4) = {4, 1};
  ```

**Surfaces & Volumes**  
- Surfaces are formed from closed loops of lines, while volumes are enclosed by one or more surfaces.  

  ```plaintext
  Line Loop(1) = {1, 2, 3, 4};
  Plane Surface(1) = {1};
  ```
#### 2. Meshing the Geometry

I. **Global or Local Mesh Parameters**  
   - Control mesh granularity via characteristic lengths or global scale factors.  
   - For instance, `Mesh.ElementSizeFactor = 1.0;` globally affects the mesh size.
II. **Meshing Commands**  
   - `Mesh 1;` generates a 1D mesh (edges).  
   - `Mesh 2;` generates a 2D mesh (surfaces).  
   - `Mesh 3;` generates a 3D mesh (volumes).  
   - These can be issued in the *.geo* file or via the GUI.
III. **Refinement & Quality Checks**  
   - Gmsh offers advanced options for refining local patches or boundary layers (useful in CFD).  
   - Check mesh statistics (e.g., aspect ratio, skewness) to ensure acceptable quality.
### 3. Post-processing

I. **Loading Simulation Data**  
   - After running an external solver, results can be loaded in Gmsh’s `.pos` format or other compatible data formats.
II. **Visualization**  
   - Inspect scalar fields (pressure, temperature) or vector fields (velocity).  
   - Generate isosurfaces, streamlines, and animations.  
   - Use the Tools $\rightarrow$ Options $\rightarrow$ Post-processing menu (GUI) or script commands to tweak visualization details.

### Scripting with Gmsh

One of Gmsh’s major strengths is its *.geo* scripting language, which automates geometry definitions and meshing steps. Users can combine loops, if-conditions, or parametric expressions to create complex shapes.

#### Example Script

```plaintext
// Define a length scale parameter
lc = 1e-1;

// Define four corner points of a square
Point(1) = {0, 0, 0, lc};
Point(2) = {1, 0, 0, lc};
Point(3) = {1, 1, 0, lc};
Point(4) = {0, 1, 0, lc};

// Create lines
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

// Form a loop and a surface
Line Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

// Adjust global mesh size factor if desired
Mesh.ElementSizeFactor = 0.8;  

// Generate the 2D mesh
Mesh 2;

// Optional: Save mesh to a file
Save "square.msh";
```

You can run this script via command line:  
```
gmsh scriptname.geo -2
```

(The `-2` argument tells Gmsh to perform 2D meshing.)

### Advanced Topics

I. **Geometry Import/Export**  
   - Gmsh can read formats like STEP, IGES, or STL.  
   - Once imported, the geometry can be re-meshed or processed further.
   - For STEP/IGES imports, use the OpenCASCADE kernel: `SetFactory("OpenCASCADE");`
   - Example: `gmsh model.step -3 -o mesh.msh` generates a volume mesh directly from a CAD file.
II. **Extrusions & 3D Lofting**  
   - Gmsh supports sweeping or extruding 2D surfaces into 3D volumes.  
   - For example, `Extrude {0,0,1} { Surface{1}; }` creates a prismatic volume.
   - You can specify the number of layers and grading: `Extrude {0,0,1} { Surface{1}; Layers{10}; Recombine; }` creates a structured hexahedral extrusion with 10 layers.
III. **Boundary Layers**  
   - Vital for CFD analyses. Gmsh can create anisotropic boundary layers near walls to capture flow gradients.
   - Use the `BoundaryLayer` field to control first cell height, growth ratio, and total thickness:
   ```geo
   Field[1] = BoundaryLayer;
   Field[1].EdgesList = {1, 2, 3, 4};
   Field[1].hwall_n = 1e-4;    // First layer height
   Field[1].ratio = 1.2;       // Growth ratio
   Field[1].thickness = 0.01;  // Total BL thickness
   Field[1].Quads = 1;         // Generate quadrilateral layers
   Background Field = 1;
   ```
IV. **Custom Fields & Meshing Constraints**  
   - Define local size fields that adapt the mesh based on geometry proximity or curvature.  
   - This is useful for refining around complex edges or capturing boundary layer transitions.
   - Common field types include `Distance` (refine near a curve/surface), `MathEval` (custom mathematical expressions), and `Threshold` (apply sizes based on distance ranges):
   ```geo
   // Refine near curve 5
   Field[1] = Distance;
   Field[1].CurvesList = {5};

   Field[2] = Threshold;
   Field[2].InField = 1;
   Field[2].SizeMin = 0.01;   // Size at the curve
   Field[2].SizeMax = 0.1;    // Size far from the curve
   Field[2].DistMin = 0.05;   // Start transitioning at this distance
   Field[2].DistMax = 0.5;    // Reach max size at this distance

   Background Field = 2;
   ```
V. **Scripting Extensions**  
   - The [Gmsh API](http://gmsh.info/doc/texinfo/gmsh.html#The-Gmsh-API) provides bindings for Python, C++, and Julia.
   - This is valuable for large optimization loops or parameter sweeps.

### Python API

Beyond the `.geo` scripting language, Gmsh's Python API allows full programmatic control. This is especially useful for integration with optimization frameworks, automated pipelines, or parametric studies.

#### Installation

```bash
pip install gmsh
```

#### Example: Parametric Airfoil Mesh

```python
import gmsh
import math

def create_naca0012(num_points=100, chord=1.0, lc=0.02):
    """Create a NACA 0012 airfoil and generate a 2D mesh."""
    gmsh.initialize()
    gmsh.model.add("naca0012")

    # Generate airfoil points using NACA 0012 thickness formula
    upper_pts = []
    lower_pts = []
    for i in range(num_points + 1):
        x = chord * (1 - math.cos(math.pi * i / num_points)) / 2
        t = 0.12
        yt = 5 * t * (0.2969 * math.sqrt(x/chord)
                       - 0.1260 * (x/chord)
                       - 0.3516 * (x/chord)**2
                       + 0.2843 * (x/chord)**3
                       - 0.1015 * (x/chord)**4)

        if i == 0 or i == num_points:
            # Leading and trailing edge share a single point
            p = gmsh.model.occ.addPoint(x, 0, 0, lc)
            upper_pts.append(p)
            lower_pts.append(p)
        else:
            upper_pts.append(gmsh.model.occ.addPoint(x, yt, 0, lc))
            lower_pts.append(gmsh.model.occ.addPoint(x, -yt, 0, lc))

    # Create splines for upper and lower surfaces
    upper_spline = gmsh.model.occ.addSpline(upper_pts)
    lower_spline = gmsh.model.occ.addSpline(lower_pts)

    # Create far-field boundary (circle)
    center = gmsh.model.occ.addPoint(chord / 2, 0, 0)
    far_field = gmsh.model.occ.addCircle(chord / 2, 0, 0, 10 * chord)

    # Create loop and surface
    airfoil_loop = gmsh.model.occ.addCurveLoop([upper_spline, -lower_spline])
    far_loop = gmsh.model.occ.addCurveLoop([far_field])
    surface = gmsh.model.occ.addPlaneSurface([far_loop, airfoil_loop])

    gmsh.model.occ.synchronize()

    # Physical groups
    gmsh.model.addPhysicalGroup(1, [upper_spline, lower_spline], name="airfoil")
    gmsh.model.addPhysicalGroup(1, [far_field], name="farfield")
    gmsh.model.addPhysicalGroup(2, [surface], name="fluid")

    # Mesh
    gmsh.model.mesh.generate(2)
    gmsh.write("naca0012.msh")
    gmsh.finalize()

create_naca0012()
```

#### Example: Batch Mesh Generation for Parameter Sweep

```python
import gmsh

def generate_mesh(width, height, mesh_size, output_file):
    """Generate a rectangular mesh with specified parameters."""
    gmsh.initialize()
    gmsh.model.add("rectangle")

    gmsh.model.occ.addRectangle(0, 0, 0, width, height)
    gmsh.model.occ.synchronize()

    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)
    gmsh.model.mesh.generate(2)
    gmsh.write(output_file)
    gmsh.finalize()

# Parameter sweep
for size in [0.1, 0.05, 0.025, 0.01]:
    generate_mesh(1.0, 0.5, size, f"rect_mesh_{size}.msh")
    print(f"Generated mesh with size {size}")
```

### Resources

- [http://gmsh.info](http://gmsh.info)
  (Latest releases, documentation, and community links.)  
- [Gmsh Documentation Page](http://gmsh.info/doc/texinfo/gmsh.html)
  (Covers commands, APIs, and example scripts in detail.)  
- [Gmsh Tutorial Page](http://gmsh.info/#Tutorials)
  (Step-by-step guides that provide deeper insight into geometry creation and meshing techniques.)  
- [Gmsh Mailing List](http://gmsh.info/#Mailing_list)
- [Gmsh Mailing List Archive](http://onelab.info/pipermail/gmsh/)
  (Good places for user questions, development discussions, and troubleshooting.)  
- [Gmsh GitLab Repository](https://gitlab.onelab.info/gmsh/gmsh)
- [Gmsh Examples Page](http://gmsh.info/#Example_files)
