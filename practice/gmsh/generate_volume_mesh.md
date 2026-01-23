Volume meshing is one of those things that sounds simple (“fill the inside”) until you try it on a real STL and the mesher starts complaining. The core idea is straightforward though: an STL is only triangles on the boundary, while most solvers (FEA, CFD, heat, etc.) need elements *inside* the domain so they can represent fields throughout the volume, not just on the skin.

Gmsh is a nice fit for this because it can sit in the middle between “I have a surface mesh” and “I need a usable 3D mesh”, and you can drive it either interactively (GUI) or reproducibly (scripts / CLI). Current stable Gmsh as of late 2025 is 4.15.0. ([gmsh.info][1])

### What “volume meshing from STL” really means

An STL is a *discrete surface mesh*. For volume meshing, Gmsh needs a *closed* surface that it can treat as the boundary of a region. In practice, you usually end up doing three steps:

1. **Make the surface usable as geometry**
   STL triangles don’t come with nice topological structure (edges, curves, “this set of triangles is one face”, etc.). Gmsh typically “classifies” the triangles into surface patches based on feature angles, then builds a parametric representation for those patches. This is exactly what the official tutorial for remeshing STL does. ([gmsh.info][2])

2. **Define a volume from the closed surface**
   Once Gmsh has surface entities, you wrap them into a “surface loop” and then create a volume from that loop.

3. **Generate the 3D mesh + check quality**
   Tetrahedral meshing is usually one command, but quality control is where you decide whether the result is solver-ready.

If you *also* have the original CAD (STEP/IGES), it’s usually better to import that instead of going through STL reparametrization—CAD surfaces tend to be smoother and mesh more cleanly. ([gmsh.info][2])

### Quick GUI workflow (good for one-offs)

If your STL is clean and you just want to get moving:

* **File → Merge** to load the STL.
* If the model is a single “blob” of triangles, you’ll often want to **classify/reparametrize** first so Gmsh can treat it as surfaces instead of a raw triangle soup. (In the CLI this is `-reclassify` / `-reparam`; more on that below.)
* Create a volume (in scripting terms this is “Surface Loop → Volume”), then **Mesh → 3D**.
* Use **Tools → Statistics → Quality** to see if you have nasty elements before exporting.

This is fine for small models. For bigger STLs or anything you want to repeat, it’s worth switching to scripts.

### A minimal `.geo` that actually works on typical STLs

A lot of “minimal examples” online skip the important part: turning the STL into something Gmsh can build a volume from. The Gmsh tutorial `t13` shows the robust version: merge STL, classify surfaces, create geometry, then define the volume. ([gmsh.info][2])

Here’s a starter file you can drop in as `mesh_from_stl.geo`:

```geo
// Load the STL surface mesh
Merge "part.stl";

// Split the triangle soup into surface patches based on feature angle
angle = 40;                    // degrees; tweak if you get too many/few patches
includeBoundary = 1;
forceParametrizablePatches = 0;
curveAngle = 180;

ClassifySurfaces{angle * Pi/180, includeBoundary, forceParametrizablePatches,
                 curveAngle * Pi/180};

// Build a geometry (parametrization) for the classified discrete surfaces
CreateGeometry;

// If the STL is a closed shell, this grabs all surfaces and makes one volume
Surface Loop(1) = Surface{:};
Volume(1) = {1};

// Optional: set a simple global target size (you can replace this with Fields later)
Mesh.CharacteristicLengthMin = 1.0;
Mesh.CharacteristicLengthMax = 1.0;
```

Then run:

```bash
gmsh mesh_from_stl.geo -3 -o part.msh
```

A couple of useful flags you’ll likely reach for:

* `-optimize` or `-optimize_netgen` to smooth/improve tetrahedra quality after generation. ([gmsh.info][2])
* `-format msh2` / `-format msh` etc. to control output format. ([gmsh.info][2])

Example:

```bash
gmsh mesh_from_stl.geo -3 -optimize_netgen -format msh2 -o part.msh
```

(If you’re feeding OpenFOAM or other tools that prefer older MSH variants, forcing `msh2` is common.)

### About “watertight” and other STL reality checks

Most failures come down to the boundary not defining a clean region. Typical issues:

* **Holes / gaps**: even a tiny gap means there’s no well-defined inside.
* **Self-intersections**: triangles crossing each other confuse region detection.
* **Non-manifold edges**: edges shared by more than two triangles are common in messy exports.
* **Scale surprises**: STL has no units; a “1” could be 1 mm or 1 m. If your mesh size feels wrong by 1000×, this is why.

If the surface isn’t closed, Gmsh can still remesh the surface, but volume meshing won’t do what you expect because there is no enclosed volume to fill.

One workflow that helps in practice is: first reparametrize/remesh the STL surface (to clean it up), save that, then volume mesh from the cleaned surface. Gmsh even mentions doing the classify+reparam steps in batch mode with `-reparam`. ([gmsh.info][2])

### Mesh sizing without going down a rabbit hole

A single global size is fine for first attempts, but you’ll often want smaller elements near curvature, sharp features, or thin passages.

Gmsh “Fields” are the usual way to do this. The tutorial example uses a MathEval field just to demonstrate the mechanism. ([gmsh.info][2]) In real work, common patterns are:

* distance-to-surface fields (refine near boundaries),
* curvature-based sizing,
* boundary layers (especially for CFD).

You don’t need to add all of that on day one—just know that if your mesh either explodes in element count or misses details, sizing control is the lever you pull next.

### Quality checks that are worth doing every time

Before exporting to a solver, do at least a quick sanity pass:

* **Look at a cut plane / clipped view** to see if the interior is filled the way you think.
* **Check element quality metrics** (skewness, Jacobian, etc.). In CLI workflows, post-optimization is often the difference between “imports fine” and “solver dies immediately”.

Gmsh exposes tetra optimization thresholds and Netgen-based optimization as options (and as CLI switches). ([gmsh.info][2])

### Partitioning for big meshes (when you outgrow “one file”)

If you’re running parallel solvers or you simply need the mesh split, Gmsh can partition after batch mesh generation using `-part`, and can write separate files with `-part_split`. ([gmsh.info][2])

Example:

```bash
gmsh mesh_from_stl.geo -3 -part 8 -part_split -o part.msh
```

This won’t magically fix a bad mesh, but it’s handy once the mesh is already good and you need it packaged for downstream tooling.

### A corrected “complete” Python API example (STL → volume mesh)

One important fix from your draft: `gmsh.model.mesh.importStl()` is *not* a “load this STL file” function—it imports an STL representation *from the current model* and takes no filename. ([gmsh.info][2])
For loading an STL file in the API, the common approach is to merge it, then classify/create geometry (same logic as the `.geo` script).

Here’s a self-contained example that mirrors the tutorial flow:

```python
import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

gmsh.model.add("stl_volume")

# Load STL triangles
gmsh.merge("part.stl")

# Classify triangles into patches and build a parametric geometry
angle_deg = 40
gmsh.model.mesh.classifySurfaces(angle_deg * 3.1415926535 / 180.0,
                                 includeBoundary=True,
                                 forceParametrizablePatches=False,
                                 curveAngle=3.1415926535)
gmsh.model.mesh.createGeometry()

# Collect all surface entities and create a volume in the built-in CAD kernel
surfs = gmsh.model.getEntities(2)
sl = gmsh.model.geo.addSurfaceLoop([s[1] for s in surfs])
vol = gmsh.model.geo.addVolume([sl])
gmsh.model.geo.synchronize()

# Physical group (helps most solvers)
pg = gmsh.model.addPhysicalGroup(3, [vol])
gmsh.model.setPhysicalName(3, pg, "Domain")

# Mesh size (simple global size to start)
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 1.0)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 1.0)

# Generate and optionally optimize
gmsh.model.mesh.generate(3)
gmsh.model.mesh.optimize("Netgen")  # similar idea to -optimize_netgen

gmsh.write("part.msh")
gmsh.finalize()
```

If you run into “too many tiny surfaces” or “one giant surface that won’t parametrize well”, the first knob to touch is `angle_deg`. Lower angles create more patches (more splitting on features); higher angles keep patches larger.

---

[1]: https://gmsh.info/ "Gmsh: a three-dimensional finite element mesh generator with built-in pre- and post-processing facilities"
[2]: https://gmsh.info/doc/texinfo/gmsh.html "Gmsh 4.15.0"
