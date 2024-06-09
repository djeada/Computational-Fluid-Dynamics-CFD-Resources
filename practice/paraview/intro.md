## Background Info

**ParaView** is a powerful open-source software developed since 2002 by Kitware Inc. and Los Alamos National Laboratory (USA). It enables parallel visualization of large meshes (exceeding 1 billion cells) and supports plotting, meshing, probing, vector analysis, and volumetric visualization. ParaView is scriptable with Python, making it highly versatile for automation tasks.

ParaView serves as a graphical user interface (GUI) to the **VTK (The Visualization Toolkit)**, an open-source system for 3D computer graphics, image processing, and visualization. VTK is written in C++ and has wrappers for Java, Tcl, and Python.

## ParaView and OpenFOAM

ParaView can be integrated with OpenFOAM in several ways:

- **Using paraFoam (included in the OpenFOAM distribution)**
  - *Pros*: Easy to use as it is a wrapper script around ParaView.
  - *Cons*: Uses an older version of ParaView.

- **Using ParaView from www.paraview.org**
  - *Pros*: Easy to use.
  - *Cons*: Requires running `foamToVTK` each time to convert OpenFOAM data to VTK format.

- **Compiling ParaView from source (www.paraview.org)**
  - *Pros*: Directly read foam files using a reader from the foam mailing list. Offers better animations (e.g., DivX).
  - *Cons*: Requires more effort to set up.

## Workflow Example

To display the pressure field of the elbow tutorial and output the result to an image file, follow these steps:

1. **Run the case:**
   ```sh
   icoFoam . elbow
   ```

2. Convert OpenFOAM data to VTK format:

```sh
 foamToVTK . elbow
```
    This creates a VTK-folder in the elbow directory.

3.    Run the Python script on the output.

## Pipeline Browser

The Pipeline Browser is central to ParaView's functionality. All visualizations are based on it, starting with reading data (the first filter) and adding more filters sequentially. Each filter has properties shown in the widget below.

![Pipeline Browser](https://user-images.githubusercontent.com/37275728/194718395-26f65365-70fd-4256-8f92-e537b6f218cf.png)

## Example

1. **Choose a source:**
   - Go to the top menu: `Sources`.
   - Select a source, e.g., `Sphere`.
   - The sphere will appear in the central widget.

2. **Modify properties:**
   - Change the representation to see the wireframe and points of the sphere.
   - Adjust opacity to make it transparent.
   - Configure lighting to show light sources.
   - Enable Data Axes Grid to display the axes.

![Sphere Example](https://user-images.githubusercontent.com/37275728/194718743-4b3f162f-8042-4a15-a705-87797f8febbd.png)


## Basic principles

ParaView includes example datasets (located in the examples folder where ParaView is installed). For example, load the `disk_out_ref2` dataset from:

```sh
/opt/ParaView-5.10.1/share/paraview-5.10/examples/disk_out_ref.ex2
```

* Make sure all variables are selected (in properties widget).

![Screenshot from 2022-10-08 19-06-19](https://user-images.githubusercontent.com/37275728/194719161-2d4cf093-e8d9-4c7e-ae10-0eed48b79b14.png)

* You can now selected one of the variables to visualize.

![Screenshot from 2022-10-08 19-07-25](https://user-images.githubusercontent.com/37275728/194719727-fc4f8ece-cc51-4015-b6de-803266b0b70b.png)

* Use clip to cut unwanted part of the object. (you get subvolume)

![Screenshot from 2022-10-08 19-13-45](https://user-images.githubusercontent.com/37275728/194719472-e1a040b8-65d5-48a1-a754-a739e45c6fa3.png)


## Filters

Filters in ParaView are essential tools for processing and visualizing data. They allow you to transform your dataset, extract meaningful insights, and create informative visualizations.

- **Adding Filters:** Each time you add a new filter, the previous visualization step is hidden (indicated by the eye symbol). This helps in keeping the workspace organized and focused on the current filter.
- **Applying Filters:** Filters are applied to the currently selected step in the pipeline. Typically, you want to apply filters to the original data to ensure that subsequent operations are based on the unaltered dataset. Make sure to select the appropriate step in the pipeline before applying a filter.
- **Properties:** Each filter comes with a set of properties that can be adjusted to fine-tune the output. These properties are displayed in the properties widget below the pipeline browser.

Common filters include:

- **Clip:** Cuts away parts of the data to focus on specific regions.
- **Contour:** Generates contour lines or surfaces for scalar fields.
- **Slice:** Creates a 2D slice through the 3D data.
- **Threshold:** Displays only the parts of the data that fall within a specified range.

## Glyphs

Glyphs are special filters that visualize vector fields in your dataset. They represent vector data as arrows or other symbols, providing a clear representation of the direction and magnitude of the vectors.

- **Usage:** To use glyphs, apply the Glyph filter to your dataset. Configure the glyph properties to represent the vector field accurately.
- **Customization:** You can customize glyph shapes, scaling, and orientation to match the specific characteristics of your data.

## Saving the Model

ParaView allows you to save your filter pipeline and visualization setup for future use. This is particularly useful for automating repetitive tasks or sharing your workflow with others.

- **Save as Python Script:** You can save your filter pipeline as a Python script. This script can be independently run or modified to adapt to different datasets or visualization needs.
  - To save as a Python script, go to `File > Save State` and choose the Python file format.
  - The saved script will include all the steps and settings from your current pipeline, enabling easy replication of the visualization process.
- **Load Saved Scripts:** You can load saved scripts into ParaView to recreate the visualization setup. This feature ensures that complex workflows can be easily reproduced without manually reconfiguring each step.
