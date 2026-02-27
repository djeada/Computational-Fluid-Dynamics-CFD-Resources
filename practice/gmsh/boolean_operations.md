# Boolean Operations in Gmsh

Boolean operations allow you to combine, subtract, and intersect geometric shapes to build complex models from simpler primitives. Gmsh supports these operations through the **OpenCASCADE** (OCC) kernel, which provides robust handling of BREP (Boundary Representation) geometry.

## Table of Contents

- [When to Use Boolean Operations](#when-to-use-boolean-operations)
- [Choosing the Geometry Kernel](#choosing-the-geometry-kernel)
- [Core Operations](#core-operations)
- [Practical Examples](#practical-examples)
- [Working with Imported CAD](#working-with-imported-cad)
- [Meshing After Booleans](#meshing-after-booleans)
- [Common Pitfalls](#common-pitfalls)

## When to Use Boolean Operations

Boolean operations are the standard way to:

- **Cut holes** in solid bodies (e.g., bolt holes in a flange, inlet/outlet ports in a manifold).
- **Unite** multiple parts into a single solid (e.g., combining a cylinder with a sphere for a capsule shape).
- **Intersect** volumes to extract the overlap region (e.g., finding the fluid domain between two nested pipes).
- **Fragment** a domain into labeled sub-regions (e.g., splitting a domain at an interface for multi-material simulations).

## Choosing the Geometry Kernel

Gmsh offers two geometry kernels. Boolean operations are only available in the OpenCASCADE kernel:

| Feature | Built-in Kernel | OpenCASCADE Kernel |
|---------|----------------|-------------------|
| Boolean operations | No | Yes |
| STEP/IGES import | No | Yes |
| Fillets and chamfers | No | Yes |
| Parametric surfaces | Limited | Full NURBS support |
| `.geo` prefix | `Point`, `Line`, etc. | `SetFactory("OpenCASCADE");` |
| Python API prefix | `gmsh.model.geo` | `gmsh.model.occ` |

Always start your `.geo` script with:

```geo
SetFactory("OpenCASCADE");
```

Or in the Python API, use `gmsh.model.occ.*` instead of `gmsh.model.geo.*`.

## Core Operations

### BooleanUnion (Fuse)

Combines two or more objects into a single solid, removing internal boundaries.

```geo
SetFactory("OpenCASCADE");

// Create two overlapping boxes
Box(1) = {0, 0, 0, 1, 1, 1};
Box(2) = {0.5, 0.5, 0, 1, 1, 1};

// Fuse them into one solid
BooleanUnion{ Volume{1}; Delete; }{ Volume{2}; Delete; }
```

### BooleanDifference (Cut)

Subtracts one object from another.

```geo
SetFactory("OpenCASCADE");

// Block with a cylindrical hole
Box(1) = {0, 0, 0, 2, 1, 1};
Cylinder(2) = {1, 0.5, 0, 0, 0, 1, 0.2};

// Cut the cylinder from the box
BooleanDifference{ Volume{1}; Delete; }{ Volume{2}; Delete; }
```

### BooleanIntersection

Keeps only the region common to both objects.

```geo
SetFactory("OpenCASCADE");

// Intersection of a sphere and a box
Sphere(1) = {0, 0, 0, 1.0};
Box(2) = {0, 0, 0, 1, 1, 1};

// Keep only the overlap
BooleanIntersection{ Volume{1}; Delete; }{ Volume{2}; Delete; }
```

### BooleanFragments

Splits all input objects at their interfaces without deleting anything. This is especially useful for multi-region meshing (e.g., solid + fluid domains that share a conformal interface).

```geo
SetFactory("OpenCASCADE");

// Inner pipe (fluid) and outer shell (solid)
Cylinder(1) = {0, 0, 0, 0, 0, 5, 0.5};   // inner radius 0.5
Cylinder(2) = {0, 0, 0, 0, 0, 5, 1.0};   // outer radius 1.0

// Fragment: creates conformal mesh at the shared surface
BooleanFragments{ Volume{1}; Volume{2}; Delete; }{}
```

After fragmentation, you get separate volume entities that share boundary surfaces — perfect for coupled simulations.

## Practical Examples

### Example 1: Plate with Multiple Holes

A rectangular plate with a pattern of bolt holes — a common engineering geometry:

```geo
SetFactory("OpenCASCADE");

// Base plate
Box(1) = {0, 0, 0, 10, 5, 0.5};

// Create holes in a 3×2 pattern
hole_radius = 0.3;
For i In {1:3}
    For j In {1:2}
        cx = 2.5 * i;
        cy = 2.5 * j;
        Cylinder(100 + 10*i + j) = {cx, cy, 0, 0, 0, 0.5, hole_radius};
    EndFor
EndFor

// Subtract all holes from the plate
BooleanDifference{ Volume{1}; Delete; }{
    Volume{111}; Volume{112};
    Volume{121}; Volume{122};
    Volume{131}; Volume{132};
    Delete;
}

// Physical groups for boundary conditions
Physical Volume("plate") = {1};
Physical Surface("top") = {/* top face IDs */};
Physical Surface("holes") = {/* hole surface IDs */};
```

### Example 2: Pipe Junction (T-Piece)

```geo
SetFactory("OpenCASCADE");

// Main pipe along x-axis
Cylinder(1) = {-5, 0, 0, 10, 0, 0, 0.5};

// Branch pipe along y-axis
Cylinder(2) = {0, -3, 0, 0, 6, 0, 0.3};

// Fuse into a single fluid domain
BooleanUnion{ Volume{1}; Delete; }{ Volume{2}; Delete; }

// Mesh
Mesh.CharacteristicLengthMax = 0.1;
Mesh 3;
Save "t_piece.msh";
```

### Example 3: Multi-Region Domain (Fluid + Solid)

For conjugate heat transfer where the mesh must be conformal at the interface:

```python
import gmsh

gmsh.initialize()
gmsh.model.add("conjugate_ht")

# Fluid domain (inner cylinder)
fluid = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, 1, 0.05)

# Solid domain (outer cylinder)
solid = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, 1, 0.06)

# Fragment to create shared interface
gmsh.model.occ.fragment([(3, solid)], [(3, fluid)])
gmsh.model.occ.synchronize()

# Get the resulting volumes
volumes = gmsh.model.getEntities(3)
# volumes[0] is the annular solid, volumes[1] is the inner fluid

gmsh.model.addPhysicalGroup(3, [volumes[0][1]], name="solid")
gmsh.model.addPhysicalGroup(3, [volumes[1][1]], name="fluid")

gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.01)
gmsh.model.mesh.generate(3)
gmsh.write("conjugate_ht.msh")
gmsh.finalize()
```

## Working with Imported CAD

Boolean operations are often needed when working with CAD files:

```geo
SetFactory("OpenCASCADE");

// Import an existing part
Merge "part.step";

// Create a bounding box for the fluid domain
Box(100) = {-5, -5, -5, 15, 10, 10};

// Cut the solid part from the fluid domain to get the external flow region
BooleanDifference{ Volume{100}; Delete; }{ Volume{1}; Delete; }
```

In the Python API:

```python
import gmsh

gmsh.initialize()
gmsh.model.add("external_flow")

# Import CAD
gmsh.model.occ.importShapes("part.step")

# Create far-field box
box = gmsh.model.occ.addBox(-5, -5, -5, 15, 10, 10)

# Get imported volumes
vols = gmsh.model.occ.getEntities(3)
imported_tags = [v[1] for v in vols if v[1] != box]

# Cut: fluid = box - solid
gmsh.model.occ.cut([(3, box)], [(3, t) for t in imported_tags])
gmsh.model.occ.synchronize()

gmsh.model.mesh.generate(3)
gmsh.write("external_flow.msh")
gmsh.finalize()
```

## Meshing After Booleans

Boolean operations can create small edges or narrow faces that cause meshing difficulties. Some tips:

### Heal Small Features

```python
# Remove small edges/faces that are below a tolerance
gmsh.option.setNumber("Geometry.Tolerance", 1e-4)
gmsh.option.setNumber("Geometry.ToleranceBoolean", 1e-4)
```

### Local Mesh Refinement at Intersections

```geo
// After boolean, refine near the intersection curves
Field[1] = Distance;
Field[1].CurvesList = {/* intersection curve IDs */};
Field[1].Sampling = 100;

Field[2] = Threshold;
Field[2].InField = 1;
Field[2].SizeMin = 0.01;
Field[2].SizeMax = 0.1;
Field[2].DistMin = 0.05;
Field[2].DistMax = 0.5;

Background Field = 2;
```

### Physical Groups After Booleans

After boolean operations, entity IDs change. Always assign physical groups *after* all boolean operations are complete:

```geo
// Do all boolean operations first
// ...

// Then query and assign physical groups
Physical Volume("domain") = Volume{:};  // all remaining volumes
```

## Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| "No volume created" | Objects don't overlap | Check geometry bounds; ensure objects intersect |
| Tiny slivers after cut | Tangent or near-tangent surfaces | Increase `Geometry.ToleranceBoolean` |
| Meshing fails after boolean | Small edges or degenerate faces | Use `Geometry.OCCFixDegenerated` and increase tolerance |
| Wrong volume deleted | `Delete` flag removes the wrong object | Verify entity IDs before boolean; use `Printf` to debug |
| Slow boolean on complex CAD | Many faces/edges in imported geometry | Simplify CAD first; defeaturing in FreeCAD or Salome |
| Non-conformal interface | Used `BooleanUnion` instead of `BooleanFragments` | Use `BooleanFragments` when you need a shared interface |

## Resources

- [Gmsh Tutorial t16](http://gmsh.info/doc/texinfo/gmsh.html#t16) — constructive solid geometry with OpenCASCADE
- [Gmsh Tutorial t18](http://gmsh.info/doc/texinfo/gmsh.html#t18) — periodic meshes with boolean operations
- [OpenCASCADE Documentation](https://dev.opencascade.org/doc/overview/html/) — underlying boolean engine
