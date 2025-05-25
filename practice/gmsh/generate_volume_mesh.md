## Volume Mesh Generation with Gmsh

Volume mesh generation is critical in computational sciences and engineering. While a surface (or “shell”) mesh in formats like STL is perfect for rapid prototyping or visual demonstrations, many numerical simulations—be they structural, thermal, or fluid dynamic—require a **volume mesh** that discretizes the interior domain. This guide explains how Gmsh can convert a surface mesh into a fully 3D volume mesh using both the graphical user interface (GUI) and Gmsh’s scripting capabilities.

### Why Generate a Volume Mesh?

I. **Finite Element Analysis (FEA)**  
- To study stresses, strains, and deformations inside a 3D object, you need volumetric elements (e.g., tetrahedrons or hexahedrons) rather than just the outer shell.
- Internal temperature distribution and conduction paths require interior nodes and elements to solve the governing equations accurately.
II. **Computational Fluid Dynamics (CFD)**  
- For external or internal flow analyses, the fluid domain itself must be volume meshed so solvers (e.g., finite volume or finite element methods) can resolve velocity, pressure, and turbulence quantities within the domain.
III. **Design and Optimization**  
- Solid (volumetric) domains can be parameterized and analyzed for a range of operational conditions.
- Volume meshes support heterogeneous material properties or graded structures in advanced manufacturing simulations.

### Gmsh: A Quick Overview

[Gmsh](http://gmsh.info/) is a robust, open-source mesh generator featuring:

- 1D (lines), 2D (surfaces), 3D (volumes).
- Geometric primitives and Boolean operations for geometry construction.
- A user-friendly graphical interface alongside a powerful *.geo* scripting language that automates complex tasks.
- Control over meshing algorithms, element size fields, boundary-layer meshing, etc.

#### Typical GUI Steps for Volume Meshing

I. **File $\rightarrow$ Open**: Import your surface mesh file (e.g., an STL or an existing Gmsh .msh file).  

II. **Define a Volume**: Under the Physical Groups menu, select “Add $\rightarrow$ Volume” and pick the enclosed surface(s).  

III. **Generate 3D Mesh**: Go to Mesh $\rightarrow$ 3D.  

IV. **Adjust Mesh Settings**: Under Tools $\rightarrow$ Options $\rightarrow$ Mesh, you can configure element size factors or other mesh controls.

* For large or highly detailed surface meshes, the GUI approach may become slow or impractical. This is where Gmsh scripting shines.

### Volume Mesh Generation via Scripting

Scripting automates and accelerates the volume meshing process, especially for large or intricate geometries. Below is a minimal script demonstrating how to generate a 3D volume mesh from an STL surface mesh.

#### Minimal Script

```plaintext
Merge "mesh_file.stl";
Surface Loop(1) = {1};
Volume(1) = {1};
```
I. **Merge**:  
   - `Merge "mesh_file.stl";` imports the external surface mesh (in STL format) into the current Gmsh model.  
   - If you have multiple surfaces or a multi-part geometry, you might see multiple surfaces (Surface(1), Surface(2), etc.). Adjust indices accordingly.
II. **Surface Loop**:  
- e.g., `{1,2,3,4}`.
III. **Volume**:  
   - `Volume(1) = {1};` declares a volume entity from the Surface Loop(1). Once declared, Gmsh knows it should fill this region with 3D elements (e.g., tetrahedra).
#### Running the Script

Save the script in a file named `meshing.geo`. Then run from a terminal or command prompt:

```bash
gmsh meshing.geo -3 -o output.mesh
```

- Tells Gmsh to perform a full 3D mesh generation.
- Specifies the filename for the generated volume mesh. Gmsh supports a variety of output formats such as `.msh`, `.mesh`, `.unv`, etc.

#### Additional Scripting Options

- **Global Element Size**  

    ```plaintext
    Mesh.ElementSizeFactor = 0.5;
    ```
  - This helps control mesh granularity if you need finer or coarser elements overall.
- **Refinement Fields**  
    ```plaintext
    Field[1] = Distance;
    Field[1].NodesList = {1}; // Node 1, for example
    ...
    Background Field = 1;
    ```
  - This advanced topic is useful for controlling mesh size based on geometry proximity or curvature.
- **Multiple Surfaces**  

    ```plaintext
    Merge "complex_geometry.stl";
    // Suppose Gmsh enumerates them as Surfaces 1,2,3
    Surface Loop(1) = {1, 2, 3};
    Volume(1) = {1};
    ```
- **Saving in Different Formats**  
  - The `-o output.msh` syntax writes in the default Gmsh format if `.msh` is used. You can specify other extensions depending on your solver requirements (e.g., `.vtu` for VTK-based solvers).

### Best Practices

To go from a “just-good-enough-for-visualisation” STL to a solver-ready 3-D volume mesh you can treat the process as a short production pipeline—clean → close → fill → mesh → check → export—and automate almost every step with Gmsh’s Python API or its non-interactive command line.
Below I walk through that pipeline in prose form, then give you complete code fragments you can paste into a job script or a notebook. The examples assume the current stable Gmsh 4.13.1 released on 24 May 2024 ([Gmsh][1]).

If the STL contains gaps, inverted facets or self-intersections the very first call to `gmsh.model.mesh.importStl()` raises an error, so before meshing you let OpenCASCADE patch things up for you.  The kernel ships with several auto-healing switches—`Geometry.OCCAutoFix`, `Geometry.OCCMakeSolids`, `Geometry.OCCFixDegenerated`—that are enabled by default, but it is wise to toggle the verbose terminal output (`General.Terminal=1`) so you actually see which faces get sewn or flipped.  After import, call `gmsh.model.occ.synchronize()` and use the graphical path *Tools → Statistics → Surface mesh* to convince yourself that the surface is now watertight; the same information is available head-less through `gmsh.model.mesh.getDuplicateNodes()` and friends, which return empty arrays when the shell is manifold.

Once the shell is closed you still need a volume to seed the tetrahedral algorithm.  In the GUI you press *Add → Volume*; in a script you collect all surface IDs in one line (`surf_loop = gmsh.model.occ.addSurfaceLoop(all_surfaces)`) and wrap them into a volume (`vol = gmsh.model.occ.addVolume([surf_loop])`).  Another `synchronize()` call propagates the topology to the mesh module.  Generation itself is a single command: `gmsh.model.mesh.generate(3)`.  If you prefer a one-liner in batch mode you can accomplish the same with

```bash
gmsh part.stl -3 -optimize_netgen -format msh40 -o part.msh
```

the `-3` switch starts the 3-D generator, while `-optimize_netgen` launches the built-in Netgen smoother for an immediate quality lift.

Quality control is not negotiable when the mesh is destined for a nonlinear Navier-Stokes or structural solver.  In the GUI choose *Tools → Statistics → Quality* and colour the elements by, say, *skewness*; anything red is a candidate for local refinement.  In a batch workflow you query the same metric directly:

```python
quals = gmsh.model.mesh.getElementQualities()
print("min = %.3g,  mean = %.3g" % (min(quals), sum(quals)/len(quals)))
```

`getElementQualities()` is part of the public API .  If the minimum plunges below 0.1 you usually re-run `gmsh.model.mesh.optimize("Netgen")` or apply the high-order optimizer for curved elements.

For meshes that barely fit in memory you gain far more by scripting than by clicking.  Gmsh is fundamentally single-core during topology creation, but you can split and write the mesh into *N* partitions in one pass (`-part N` at the command line ([Manpagez][2]) or the Python call `gmsh.model.mesh.partition(N)` ).  On a cluster you then mesh once on the login node, copy the *N* `.msh` chunks to the working directory and launch the solver in parallel; the mesher’s RAM footprint never grows above a single partition.

When your STL actually holds several independent cavities—think fuel + oxidiser manifolds—you repeat the *surface loop → volume* pattern for each region.  The GUI names them *Volume 1*, *Volume 2*…; in a script you tag each with a physical label so that the downstream solver can assign materials:

```python
gmsh.model.addPhysicalGroup(3, [vol1], tag=1)  # aluminium wall
gmsh.model.setPhysicalName(3, 1, "Solid")
gmsh.model.addPhysicalGroup(3, [vol2], tag=2)  # internal fluid
gmsh.model.setPhysicalName(3, 2, "Fluid")
```

Finally, export uses exactly the format your solver likes.  OpenFOAM expects the binary flavour of *MSH 2*; so call

```bash
gmshToFoam part.msh
```

or, if you wish to stay in Python, rely on `meshio` to re-encode the mesh.  Elmer reads `.msh` directly, SU2 prefers `.cgns`, and most commercial CFD codes can digest the ASCII *UNV* produced by `gmsh -o part.unv -format unv`.

### Complete self-contained Python example

```python
import gmsh, sys, meshio

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

gmsh.model.mesh.importStl("part.stl")       # read + heal
gmsh.model.occ.synchronize()

surfs = gmsh.model.getEntities(2)           # collect STL facets
loop  = gmsh.model.occ.addSurfaceLoop([s[1] for s in surfs])
vol   = gmsh.model.occ.addVolume([loop])
gmsh.model.occ.synchronize()

gmsh.model.addPhysicalGroup(3, [vol], 1)
gmsh.model.setPhysicalName(3, 1, "Domain")

gmsh.model.mesh.generate(3)                 # tetrahedral mesh
gmsh.model.mesh.optimize("Netgen")          # smoothing pass

print("Worst quality :", min(gmsh.model.mesh.getElementQualities()))

gmsh.write("part.msh")                      # native output
gmsh.finalize()

# optional: convert to CGNS for SU2
mesh = meshio.read("part.msh")
meshio.write("part.cgns", mesh)
```

Save the file as `mesh.py`, then run on four cluster cores:

```bash
srun -n4 --mem=4G python mesh.py
```

The script never opens a window, finishes in minutes for tens of millions of tets and leaves you with `part.msh` plus any derivative formats you need.

That’s the whole workflow in practice: an STL goes in, a clean, partitioned, quality-checked volume mesh comes out, ready for OpenFOAM, Elmer, SU2 or your in-house code—with every operation scripted so tomorrow’s bigger model can reuse today’s pipeline unchanged.


