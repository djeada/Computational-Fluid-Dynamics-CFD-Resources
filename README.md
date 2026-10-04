# Computational Fluid Dynamics (CFD) Resources

![CFD Resources Banner](https://github.com/user-attachments/assets/ac0cec05-abb0-4f8e-ae68-3df6bbb53308)

[![CI](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/actions/workflows/ci.yml/badge.svg)](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/djeada/Computational-Fluid-Dynamics-CFD-Resources?style=social)](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/stargazers)

Notes, runnable Python scripts, tool guides, and curated references for learning computational fluid dynamics. The material connects the physics of fluid flow with the numerical methods used to simulate it, the software used in practice, and data-driven techniques such as reduced-order models and machine learning.

[Quick start](#quick-start) • [Learning paths](#learning-paths) • [Notes](#notes) • [Practice](#practice) • [Scripts](#scripts) • [References](#references) • [Contributing](#contributing)

## What's here

<!-- BEGIN GENERATED: stats -->

| Content | Count | Location |
| --- | --: | --- |
| Theory notes | 134 | [`notes/`](notes/) |
| Notes with exercises | 134 | [`notes/`](notes/) |
| Practice guides | 14 | [`practice/`](practice/) |
| Algorithm scripts | 7 | [`scripts/algorithms/`](scripts/algorithms/) |
| Plot scripts | 35 | [`scripts/plots/`](scripts/plots/) |
| Simulations | 15 | [`scripts/simulations/`](scripts/simulations/) |

<!-- END GENERATED: stats -->

Every script runs headless in CI, and every relative link in the repository is checked. Topics that are planned but not written yet are tracked in the [roadmap](ROADMAP.md).

## Quick start

```bash
git clone https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources.git
cd Computational-Fluid-Dynamics-CFD-Resources
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cd scripts/simulations/lid_driven_cavity
python main.py                                  # interactive window
python main.py --no-show --output figures       # save the figure instead
```

Every script accepts `--no-show` and `--output DIR`. Time-stepping and interactive scripts also accept `--steps N`. Each script folder has a README explaining the maths, the implementation, and the output.

## Learning paths

Each path is a suggested reading order through material that exists in this repository.

### 1. First steps in CFD

*Prerequisites: calculus, basic physics, some Python.*

1. [Introduction to fluid mechanics](notes/fluid_mechanics/intro.md) and [dimensional analysis](notes/fluid_mechanics/dimensions.md)
2. [Navier–Stokes equations](notes/fluid_mechanics/governing_equations/navier_stokes.md)
3. [Why CFD is needed](notes/numerical/cfd/intro.md) and [the strategy of CFD](notes/numerical/cfd/cfd_process.md)
4. [Finite difference method](notes/numerical/fdm/intro.md), then run the [1D heat and wave equations](scripts/simulations/1d_heat_and_wave_equations/)
5. [Numerical stability](notes/numerical/cfd/numerical_stability.md)
6. Run the [lid-driven cavity](scripts/simulations/lid_driven_cavity/) and read the [lid-driven cavity tutorial](practice/manual_projects/lid_driven_cavity.md)

### 2. Numerical methods in depth

*Prerequisites: path 1, linear algebra.*

1. [Finite-difference discretization](notes/numerical/fdm/discretization.md)
2. [Finite volume method](notes/numerical/fvm/intro.md) and [finite-volume discretization](notes/numerical/fvm/discretization.md)
3. [Finite element method](notes/numerical/fem/intro.md) and [weak formulations](notes/numerical/fem/weak_formulation_pde.md)
4. [Dealing with nonlinearity](notes/numerical/cfd/dealing_with_nonlinearity.md), [direct and iterative solvers](notes/numerical/cfd/direct_and_iterative_solvers.md), and [iterative convergence](notes/numerical/cfd/iterative_convergence.md)
5. [Lattice Boltzmann method](notes/numerical/lattice_boltzmann/intro.md), then run the [lattice Boltzmann cylinder flow](scripts/simulations/lattice_boltzmann_cylinder_flow/)

### 3. Engineering practice

*Prerequisites: an engineering background.*

1. [Boundary layers](notes/fluid_mechanics/viscous_flow/boundary_layers.md) and [turbulence](notes/fluid_mechanics/turbulence/)
2. [Turbulence modeling in CFD](notes/numerical/cfd/turbulence_modeling.md)
3. [Mesh quality](practice/mesh_generation/mesh_quality.md) and [boundary-layer meshing](practice/mesh_generation/boundary_layers.md)
4. [Gmsh](practice/gmsh/intro.md), [OpenFOAM](practice/openfoam/getting_started.md), and [ParaView](practice/paraview/intro.md)
5. [Flow over a cylinder](practice/manual_projects/flow_over_cylinder.md) end to end
6. [Solver comparison](practice/cfd_tools/solver_comparison.md) and [workflow automation](practice/cfd_tools/automation.md)

### 4. Data-driven methods

*Prerequisites: linear algebra, Python, CFD basics.*

1. [Proper orthogonal decomposition](notes/numerical/pod/pod_intro.md), [POD and the SVD](notes/numerical/pod/pod_vs_svd.md), and [snapshot POD](notes/numerical/pod/snapshot_pod.md), with the [POD](scripts/algorithms/pod/) and [snapshot POD](scripts/algorithms/snapshot_pod/) scripts
2. [Reduced-order modeling](notes/numerical/rom/rom.md) and [POD–Galerkin projection](notes/numerical/rom/pod_galerkin_projection.md)
3. [Surrogate models](notes/numerical/surrogates/intro.md), [kriging](notes/numerical/surrogates/kriging.md), and [radial basis functions](notes/numerical/surrogates/radial_basis_functions.md), with the [kriging](scripts/algorithms/kriging_interpolation/) and [RBF](scripts/algorithms/radial_basis_functions/) scripts
4. [Machine learning for CFD](notes/machine_learning/intro.md), [neural networks in aerodynamics](notes/machine_learning/neural_networks/intro.md), and [machine learning on meshes](notes/machine_learning/geometry/ml_with_meshes.md)

## Notes

Theory notes are grouped by subject. Most notes end with exercises (with worked answers) and references.

### [Fluid mechanics](notes/fluid_mechanics/)

| Topic | Notes |
| --- | --- |
| Fundamentals | [Introduction](notes/fluid_mechanics/intro.md), [dimensional analysis](notes/fluid_mechanics/dimensions.md) |
| [Governing equations](notes/fluid_mechanics/governing_equations/) | [Continuity](notes/fluid_mechanics/governing_equations/continuity.md), [Navier–Stokes](notes/fluid_mechanics/governing_equations/navier_stokes.md), [energy](notes/fluid_mechanics/governing_equations/energy.md), [equation of state](notes/fluid_mechanics/governing_equations/equation_of_state.md) |
| [Fluid properties](notes/fluid_mechanics/fluid_properties/) | [Viscosity](notes/fluid_mechanics/fluid_properties/viscosity.md), [pressure and compressibility](notes/fluid_mechanics/fluid_properties/pressure_and_compressibility.md), [surface tension](notes/fluid_mechanics/fluid_properties/surface_tension.md) |
| [Flow kinematics](notes/fluid_mechanics/flow_kinematics/) | [Flow kinematics](notes/fluid_mechanics/flow_kinematics/flow_kinematics.md), [Eulerian and Lagrangian descriptions](notes/fluid_mechanics/flow_kinematics/eulerian_lagrangian_flows.md) |
| [Fluid statics](notes/fluid_mechanics/fluid_statics/) | [Hydrostatics](notes/fluid_mechanics/fluid_statics/hydrostatics.md) |
| [Inviscid flow](notes/fluid_mechanics/inviscid_flow/) | [Bernoulli's equation](notes/fluid_mechanics/inviscid_flow/bernoulli.md), [potential flow](notes/fluid_mechanics/inviscid_flow/potential_flow.md) |
| [Viscous flow](notes/fluid_mechanics/viscous_flow/) | [Boundary layers](notes/fluid_mechanics/viscous_flow/boundary_layers.md), [drag](notes/fluid_mechanics/viscous_flow/drag.md) |
| [Internal flow](notes/fluid_mechanics/internal_flow/) | [Pipe flow](notes/fluid_mechanics/internal_flow/pipes.md) |
| [Compressible flow](notes/fluid_mechanics/compressible_flow/) | [Thermodynamics](notes/fluid_mechanics/compressible_flow/thermodynamics.md), [speed of sound](notes/fluid_mechanics/compressible_flow/speed_of_sound.md), [isentropic flow](notes/fluid_mechanics/compressible_flow/isentropic_flow.md), [shock waves](notes/fluid_mechanics/compressible_flow/shock_waves.md), [Rayleigh and Fanno flow](notes/fluid_mechanics/compressible_flow/rayleigh_fanno.md) |
| [Turbulence](notes/fluid_mechanics/turbulence/) | [Reynolds decomposition](notes/fluid_mechanics/turbulence/reynolds_decomposition.md), [statistics](notes/fluid_mechanics/turbulence/statistics.md), [energy cascade](notes/fluid_mechanics/turbulence/energy_cascade.md), [RANS equations](notes/fluid_mechanics/turbulence/rans_equations.md), [modeling](notes/fluid_mechanics/turbulence/modeling.md) |
| [Specialized topics](notes/fluid_mechanics/specialized_topics/) | [Fluid–structure interaction](notes/fluid_mechanics/specialized_topics/fluid_structure_interaction.md) |

### [Numerical methods](notes/numerical/)

| Topic | Notes |
| --- | --- |
| [CFD fundamentals](notes/numerical/cfd/) | [The need for CFD](notes/numerical/cfd/intro.md), [strategy of CFD](notes/numerical/cfd/cfd_process.md), [governing equations](notes/numerical/cfd/governing_equations.md), [nonlinearity](notes/numerical/cfd/dealing_with_nonlinearity.md), [direct and iterative solvers](notes/numerical/cfd/direct_and_iterative_solvers.md), [iterative convergence](notes/numerical/cfd/iterative_convergence.md), [numerical stability](notes/numerical/cfd/numerical_stability.md), [turbulence modeling](notes/numerical/cfd/turbulence_modeling.md) |
| [Finite differences](notes/numerical/fdm/) | [Introduction](notes/numerical/fdm/intro.md), [discretization](notes/numerical/fdm/discretization.md) |
| [Finite volumes](notes/numerical/fvm/) | [Introduction](notes/numerical/fvm/intro.md), [discretization](notes/numerical/fvm/discretization.md) |
| [Finite elements](notes/numerical/fem/) | [Introduction](notes/numerical/fem/intro.md), [weak formulation](notes/numerical/fem/weak_formulation_pde.md) |
| [Lattice Boltzmann](notes/numerical/lattice_boltzmann/) | [Introduction](notes/numerical/lattice_boltzmann/intro.md), [Boltzmann equation](notes/numerical/lattice_boltzmann/boltzmann_equation.md), [from Newton to Navier–Stokes](notes/numerical/lattice_boltzmann/from_newton_to_nse.md), [from Boltzmann to lattice Boltzmann](notes/numerical/lattice_boltzmann/from_boltzmann_to_lattice_boltzmann.md), [algorithm](notes/numerical/lattice_boltzmann/lattice_boltzmann_algorithm.md), [in practice](notes/numerical/lattice_boltzmann/practical_lbm.md) |
| [Proper orthogonal decomposition](notes/numerical/pod/) | [Introduction](notes/numerical/pod/pod_intro.md), [POD and SVD](notes/numerical/pod/pod_vs_svd.md), [derivation in 2D](notes/numerical/pod/derivation_in_2d.md), [derivation in N dimensions](notes/numerical/pod/derivation_in_n_dim.md), [snapshot POD](notes/numerical/pod/snapshot_pod.md), [gappy POD](notes/numerical/pod/gappy_pod.md) |
| [Reduced-order models](notes/numerical/rom/) | [Overview](notes/numerical/rom/rom.md), [discretization techniques](notes/numerical/rom/discretization_techniques.md), [parameterized variational problems](notes/numerical/rom/parameterized_variational_problems.md), [reduced basis approximation](notes/numerical/rom/reduced_basis_approximation.md), [POD–Galerkin projection](notes/numerical/rom/pod_galerkin_projection.md) |
| [Surrogate models](notes/numerical/surrogates/) | [Introduction](notes/numerical/surrogates/intro.md), [kriging](notes/numerical/surrogates/kriging.md), [hierarchical kriging](notes/numerical/surrogates/hierarchical_kriging.md), [radial basis functions](notes/numerical/surrogates/radial_basis_functions.md), [one-stage sampling](notes/numerical/surrogates/one_stage_sampling.md), [adaptive sampling](notes/numerical/surrogates/adaptive_sampling.md) |

### [Machine learning](notes/machine_learning/)

| Topic | Notes |
| --- | --- |
| Overview | [Introduction to machine learning for CFD](notes/machine_learning/intro.md) |
| [Neural networks](notes/machine_learning/neural_networks/) | [Neural networks in aerodynamics](notes/machine_learning/neural_networks/intro.md), [datasets](notes/machine_learning/neural_networks/datasets.md), [generating CFD datasets](notes/machine_learning/neural_networks/generating_cfd_datasets.md), [model training](notes/machine_learning/neural_networks/model_training.md), [graph neural network example](notes/machine_learning/neural_networks/example_work_for_gnn.md) |
| [Flow](notes/machine_learning/flow/) | [Feature extraction](notes/machine_learning/flow/feature_extraction.md), [flow dynamics](notes/machine_learning/flow/flow_dynamics.md), [optimization](notes/machine_learning/flow/optimization.md), [particle image velocimetry](notes/machine_learning/flow/particle_image_velocimetry.md), [superresolution and flow cleansing](notes/machine_learning/flow/superresolution_and_flow_cleansing.md) |
| [Geometry](notes/machine_learning/geometry/) | [Machine learning on CAD](notes/machine_learning/geometry/ml_on_cad.md), [machine learning on meshes](notes/machine_learning/geometry/ml_with_meshes.md) |
| [Automotive aerodynamics](notes/machine_learning/automotive_aerodynamics/) | [ML process](notes/machine_learning/automotive_aerodynamics/ml_process.md), [dataset of meshes](notes/machine_learning/automotive_aerodynamics/dataset_of_meshes.md), [deformation parameters](notes/machine_learning/automotive_aerodynamics/deformation_parameters.md), [output data](notes/machine_learning/automotive_aerodynamics/output_data.md) |

### [Applied mechanics](notes/applied_mechanics/)

| Topic | Notes |
| --- | --- |
| [Fundamentals](notes/applied_mechanics/fundamentals/) | Force systems, moments and couples, free body diagrams, vector analysis |
| [Statics](notes/applied_mechanics/statics/) | Particle and rigid-body equilibrium, structural analysis, trusses and frames, friction, centroids |
| [Dynamics](notes/applied_mechanics/dynamics/) | Kinematics and kinetics of particles and rigid bodies, work–energy, impulse–momentum, vibrations |
| [Strength of materials](notes/applied_mechanics/strength_materials/) | Stress and strain, material properties, axial loading, torsion, bending, shear and moment diagrams, combined loading, buckling |
| [Fluid loading](notes/applied_mechanics/fluid_loading/) | Pressure forces, wind loading, wave loading, flow-induced vibrations, hydroelasticity |
| [Control systems](notes/applied_mechanics/control_systems/) | System modeling, stability analysis, feedback control, PID controllers |
| [Mechanical systems](notes/applied_mechanics/mechanical_systems/) | Mechanisms, gears, bearings, rotating machinery, hydraulics and pneumatics |
| [Transportation](notes/applied_mechanics/transportation/) | [Airplanes](notes/applied_mechanics/transportation/airplanes/) (airfoils, stability, inertial navigation, Reynolds number, design process) and [cars](notes/applied_mechanics/transportation/cars/) |

## Practice

Guides for the tools used in day-to-day CFD work. See the [practice overview](practice/README.md) for a suggested order.

| Area | Guides |
| --- | --- |
| [Gmsh](practice/gmsh/) | [Introduction](practice/gmsh/intro.md), [volume meshes from STL](practice/gmsh/generate_volume_mesh.md), [boolean operations](practice/gmsh/boolean_operations.md) |
| [Mesh generation](practice/mesh_generation/) | [Boundary-layer meshing](practice/mesh_generation/boundary_layers.md), [mesh quality](practice/mesh_generation/mesh_quality.md) |
| [OpenFOAM](practice/openfoam/) | [Getting started](practice/openfoam/getting_started.md), [turbulence modeling](practice/openfoam/turbulence_modeling.md) |
| [ParaView](practice/paraview/) | [ParaView and OpenFOAM](practice/paraview/intro.md), [external Python packages](practice/paraview/import_external_packages.md), [batch visualization](practice/paraview/batch_visualization.md) |
| [CFD tools](practice/cfd_tools/) | [Solver comparison](practice/cfd_tools/solver_comparison.md), [workflow automation](practice/cfd_tools/automation.md) |
| [Manual projects](practice/manual_projects/) | [Lid-driven cavity](practice/manual_projects/lid_driven_cavity.md), [flow over a cylinder](practice/manual_projects/flow_over_cylinder.md) |

## Scripts

Each script lives in its own folder with a `main.py` and a README covering the mathematical background, the implementation, and the output. The index below is generated from those READMEs by [`tools/generate_index.py`](tools/generate_index.py).

<!-- BEGIN GENERATED: scripts -->

### Algorithms

| Script | Description |
| --- | --- |
| [Condition Number of the Correlation Matrix](scripts/algorithms/condition_number_of_the_correlation_matrix/) | This script plots how the condition number of a kriging correlation matrix changes with the correlation parameter $\theta$ for the linear, exponential, Gaussian and cubic spline correlation functions. |
| [Correlation Functions](scripts/algorithms/correlation_functions/) | This script plots four correlation functions used in kriging surrogate models (linear, exponential, Gaussian and cubic spline) for several values of the correlation parameter $\theta$. |
| [Image Compression Using SVD](scripts/algorithms/image_compression_using_svd/) | This script compresses a grayscale image by keeping only its $r$ largest singular values and the matching singular vectors, then compares the rank-$`r`$ reconstructions with the original. |
| [Kriging Interpolation](scripts/algorithms/kriging_interpolation/) | This script interpolates 11 samples of $y(x) = (3x-3)^2 \sin(2x-10)$ with a kriging-type predictor built on the cubic spline correlation function, for four values of the correlation parameter $\theta$. |
| [Proper Orthogonal Decomposition (POD)](scripts/algorithms/pod/) | This script performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix. |
| [Radial Basis Functions](scripts/algorithms/radial_basis_functions/) | This script fits a multiquadric radial basis function (RBF) interpolant through 11 data points on $[0, 1]$ using SciPy's `Rbf` class and plots it on a fine grid. |
| [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](scripts/algorithms/snapshot_pod/) | This script computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one. |

### Plots

| Script | Description |
| --- | --- |
| [Airfoil Angle of Attack](scripts/plots/airfoil_angle_attack/) | This script draws a NACA 2412 airfoil pitched nose-up about its leading edge to several angles of attack, $10^\circ$ and $60^\circ$ by default, relative to a free stream flowing left to right. |
| [NACA 4-Digit Airfoil Profile](scripts/plots/airfoil_profile/) | This script draws an annotated NACA 4-digit airfoil profile (NACA 4412 by default) from its four-digit designation, labelling the leading edge, trailing edge, chord line and mean camber line. |
| [Archimedes' Principle Visualisation](scripts/plots/archimedes_principle/) | This script draws a block in a tank of fluid with its weight and buoyant force shown as arrows, and states whether the block floats or sinks according to Archimedes' principle. |
| [Generating Synthetic Data for Boundary Layer Simulation](scripts/plots/boundary_layer_problem/) | This script generates noisy synthetic velocity samples across a boundary layer from a simple square-root profile, saves them to a CSV file and plots them against the wall-normal distance. |
| [Turbulent Boundary Layer Velocity Profile](scripts/plots/boundary_layer_velocity_profile/) | This script plots the one-seventh power-law velocity profile of a turbulent boundary layer in normalised form, $u/U_\infty$ against $y/\delta$. |
| [Grid Convergence Comparison](scripts/plots/comparing_grid_convergence/) | This script illustrates grid convergence by plotting the model numerical solutions $u_N(x) = e^{-x(1 + x/N)}$ for $N = 4, 8, 16$ against the exact solution $u(x) = e^{-x}$ on $[0, 1]$. |
| [Compressible vs. Incompressible Duct Flow](scripts/plots/compressible_vs_incompressible/) | This script draws prescribed incompressible and compressible velocity fields in a 2D duct side by side, so the constant downstream profile of the first can be compared with the accelerating profile of the second. |
| [Design Space Distribution via Sobol Sequences](scripts/plots/design_space_distribution/) | This script draws a four-dimensional scrambled Sobol design of 512 geometry variants and plots two 2D projections of it, showing how evenly a low-discrepancy sequence covers a design space. |
| [Drag Coefficient Prediction](scripts/plots/drag_coefficient_prediction/) | This script compares two synthetic drag-coefficient predictors with reference values in a predicted-vs-reference plot, adding a regression line and $R^2$ for each. |
| [Eigenvector Projection of Velocity Fluctuations](scripts/plots/eigenvector_projection/) | This script finds the principal directions of correlated 2D velocity fluctuations from the eigenvectors of their covariance matrix and projects the data onto them. |
| [Eulerian and Lagrangian Flow Descriptions](scripts/plots/eulerian_lagrangian_flows/) | This script contrasts the Eulerian and Lagrangian descriptions of fluid motion using the time-dependent Double Gyre flow. |
| [Flow Rate Through a Circular Pipe](scripts/plots/flow_rate_pipe/) | This script computes the volumetric flow rate $Q = \pi r^2 v$ of a circular pipe and draws a labelled side view of the pipe with flow arrows. |
| [Flow Separation in a Boundary Layer](scripts/plots/flow_separation_boundary_layer/) | This script draws a schematic of boundary-layer separation: an attached layer that thickens downstream, a separation point, and a recirculation region under the separated shear layer. |
| [Froude Number vs. Flow Velocity](scripts/plots/froude_number/) | This script plots the length-based Froude number $Fr = U/\sqrt{gL}$ against speed for hulls of 5, 10, 15, and 20 m, with reference lines at hull speed and at the approximate start of planing. |
| [Laminar vs. Turbulent Boundary Layer Profiles](scripts/plots/laminar_vs_turbulent_boundary_layer/) | This script plots normalised laminar and turbulent boundary-layer velocity profiles on the same axes to show how much fuller the turbulent profile is. |
| [Laminar vs Turbulent Pipe Flow](scripts/plots/laminar_vs_turbulent_pipe/) | This script plots laminar and turbulent radial velocity profiles of pipe flow in side-by-side panels to show how much flatter the turbulent profile is. |
| [Longitudinal Velocity Fluctuations and Projections](scripts/plots/longitudinal_velocity_fluctuations_and_projections/) | This script plots synthetic two-point velocity fluctuations as time traces, as a scatter cloud, and projected onto a unit vector, which are the first steps of the two-point POD example. |
| [Mean Pressure Coefficient Along Vehicle Centreline](scripts/plots/mean_pressure_coefficient/) | This script plots a mock validation figure of mean pressure coefficient $C_P$ against streamwise position, comparing "experimental" data with a "CFD SRS" (scale-resolving simulation) curve that under-predicts a separation plateau. |
| [Mean Velocity Magnitude: Experiment vs CFD Comparison](scripts/plots/mean_velocity_magnitude/) | This script plots a mock experimental profile and a mock CFD scale-resolving simulation (SRS) profile of the normalised mean velocity magnitude $\|U\|/U_0$ along an under-body centreline. |
| [Meniscus Behavior](scripts/plots/meniscus_behavior/) | This script sketches the meniscus of water and of mercury in a glass tube, showing how wetting determines whether the free surface curves up or down at the wall. |
| [Microscopic vs. Macroscopic View of a Fluid](scripts/plots/microscopic_view/) | This script draws two side-by-side panels that contrast the microscopic (molecular) and macroscopic (continuum) views of a fluid. |
| [Converging-Diverging Nozzle Flow](scripts/plots/nozzle_flow/) | This script plots quasi-one-dimensional isentropic flow through a converging-diverging (de Laval) nozzle, with streamlines coloured by Mach number. |
| [Numerical vs. Exact Solution Comparison](scripts/plots/numerical_vs_exact_solution/) | This script solves $du/dx + u = 0$ with $u(0) = 1$ by a first-order finite-difference scheme and compares the result with the exact solution $u(x) = e^{-x}$, plotting the pointwise error. |
| [POD Analysis for Flow Fields](scripts/plots/pod_analysis_for_flow_fields/) | This script performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode. |
| [POD Modes of a Two-Point Velocity Signal](scripts/plots/pod_modes_2d/) | This script applies Proper Orthogonal Decomposition to velocity signals measured at two points, a and b, and plots how much each of the two POD modes contributes to each signal. |
| [POD Spatial Modes and Temporal Coefficients](scripts/plots/pod_modes_and_temporal_coefficients/) | This script extracts the first three POD spatial modes and their temporal coefficients from a synthetic two-dimensional, time-dependent field and plots them. |
| [Pressure Difference Across a Spherical Droplet](scripts/plots/pressure_difference_across_spherical_droplet/) | This script draws an annotated schematic of the Young-Laplace pressure jump across the surface of a spherical droplet. |
| [Pressure Variation with Depth](scripts/plots/pressure_variation_with_depth/) | This script plots how hydrostatic pressure increases linearly with depth below the free surface of a fluid at rest. |
| [Maxwell-Boltzmann Speed Distribution of N₂ Molecules](scripts/plots/probability_distribution_function_of_nitrogen_molecules/) | This script plots the Maxwell-Boltzmann speed distribution of nitrogen (N₂) molecules at 300 K, 600 K, 900 K and 1200 K, and marks the most probable, mean and root-mean-square speed on each curve. |
| [Ship Hull in Water](scripts/plots/ship_hull_in_water/) | This script draws a side-view sketch of a ship hull sitting in a sinusoidal free-surface wave and annotates it with the Froude number $Fr = U/\sqrt{gL}$. |
| [Time-Averaged Velocity Field](scripts/plots/time_averaged_velocity_field/) | This script generates a synthetic noisy longitudinal velocity field on a 200 × 60 grid and compares it with its mean field, the first step of a Reynolds decomposition. |
| [Turbulent Flow: Reynolds Decomposition](scripts/plots/turbulent_flow/) | This script splits a synthetic velocity signal into its time mean and fluctuation, following the Reynolds decomposition used in turbulence modelling. |
| [Variation of Residual with Iteration](scripts/plots/variation_of_residual/) | This script solves the 1D Laplace equation with Gauss-Seidel iteration on a 100-point grid and plots the normalised residual against iteration number on a logarithmic scale. |
| [Velocity Layers and Viscosity](scripts/plots/velocity_layers_viscosity/) | This script draws a schematic of three stacked fluid layers moving at different speeds to illustrate Newton's law of viscosity, $`\tau = \mu\, du/dy`$. |
| [Wall Shear in Pipe Cross-Section](scripts/plots/wall_shear_pipe_cross_section/) | This script sketches fully developed laminar (Hagen-Poiseuille) flow in a circular pipe, with velocity arrows whose lengths follow the parabolic profile $u(r) = u_{max}(1 - (r/R)^2)$. |

### Simulations

| Script | Description |
| --- | --- |
| [1D Heat and Wave Equation Simulations](scripts/simulations/1d_heat_and_wave_equations/) | This script solves the 1D heat equation with the implicit Crank–Nicolson scheme and the 1D wave equation with the explicit leapfrog scheme, animating both from the same initial Gaussian pulse. |
| [2D Wave Equation Simulation](scripts/simulations/2d_wave_simulation/) | This script solves the 2D scalar wave equation on a square domain with an explicit leapfrog finite difference scheme and animates the result as a 3D surface. |
| [Backward-Facing Step Flow (SIMPLE Algorithm)](scripts/simulations/backward_facing_step_simple/) | This script solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm. |
| [Bak–Tang–Wiesenfeld Sandpile Model (3D)](scripts/simulations/bak_tang_wiesenfeld_sandpile_model_3d/) | This script simulates the two-dimensional Bak–Tang–Wiesenfeld (BTW) sandpile on a 20×20 lattice and animates its height field as a 3D surface. |
| [Charged Particle Dynamics in a Magnetic Field](scripts/simulations/charged_particle_dynamics_in_a_magnetic_field_using_runge_kutta_methods/) | This script integrates the motion of a charged particle in a uniform magnetic field with the classical fourth-order Runge–Kutta (RK4) method and animates the resulting helical trajectory in 3D. |
| [Eulerian Cylinder Flow](scripts/simulations/eulerian_cylinder_flow/) | This script simulates 2D incompressible, inviscid flow past a circular cylinder on a fixed Eulerian grid and renders a dye tracer in real time with Pygame. |
| [Ising Model Simulation](scripts/simulations/ising_model/) | This script simulates the two-dimensional Ising model with the Metropolis Monte Carlo algorithm and animates the spin lattice together with its magnetization and energy. |
| [Kelvin-Helmholtz Instability Simulation](scripts/simulations/kelvin_helmholtz_instability/) | This script simulates the Kelvin-Helmholtz instability, the rolling-up of a shear layer between fluid streams moving in opposite directions, in a periodic 2D incompressible flow drawn in real time with Pygame. |
| [Laplace Equation Maze Solver](scripts/simulations/laplace_equation_maze_solver/) | This script solves a randomly generated maze by computing a potential that satisfies Laplace's equation in the maze passages and then following the potential uphill from the entrance to the exit. |
| [Lattice Boltzmann Cylinder Flow Simulation](scripts/simulations/lattice_boltzmann_cylinder_flow/) | This script simulates 2D flow past a circular cylinder with the lattice Boltzmann method (D2Q9 lattice, BGK collision operator) and animates the velocity magnitude with Matplotlib. |
| [Lid-Driven Cavity Flow Simulation](scripts/simulations/lid_driven_cavity/) | This script solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field. |
| [Rayleigh-Bénard Convection Simulation](scripts/simulations/rayleigh_benard_convection/) | This script simulates Rayleigh-Bénard convection, the buoyancy-driven flow in a fluid layer heated from below and cooled from above, and draws the temperature field in real time with Pygame. |
| [2D Schrödinger Equation Simulation](scripts/simulations/schroedinger_equation/) | This script solves the time-dependent Schrödinger equation for a free particle in two dimensions with the split-step Fourier method and animates the probability density of the spreading wavepacket as a 3D surface. |
| [Simplified Real-Time Fluid Dynamics Simulator](scripts/simulations/simplified_real_time_fluid_dynamics_simulator/) | This script is an interactive 2D smoke simulation that uses Jos Stam's Stable Fluids algorithm (1999) to approximate the incompressible Navier-Stokes equations fast enough to run in real time in a Pygame window. |
| [Steady and Unsteady Pathlines Around a Cylinder with Vortex Shedding](scripts/simulations/steady_and_unsteady_pathlines_with_vortex_shedding/) | This script compares streamlines and particle pathlines for steady potential flow past a cylinder with circulation and for an unsteady version of the same flow with a kinematic vortex-shedding model. |

<!-- END GENERATED: scripts -->

## FAQ

<details>
<summary><b>My simulation diverges. What should I check?</b></summary>

Common causes, roughly in order of frequency:

1. Time step too large for the stability limit (reduce it and retry)
2. Boundary conditions that are incorrect or conflicting
3. Initial conditions far from the solution
4. Poor mesh quality (high skewness or aspect ratio)
5. A numerical scheme unsuited to the problem

See [numerical stability](notes/numerical/cfd/numerical_stability.md) and [iterative convergence](notes/numerical/cfd/iterative_convergence.md).

</details>

<details>
<summary><b>How do I know if my mesh is fine enough?</b></summary>

Run a mesh independence study: solve on at least three systematically refined meshes, compare the quantities you care about (drag, pressure drop, reattachment length), and estimate the discretization error, for example with Richardson extrapolation. Also check mesh quality metrics. See [mesh quality](practice/mesh_generation/mesh_quality.md) and the [grid convergence](scripts/plots/comparing_grid_convergence/) script.

</details>

<details>
<summary><b>What is the difference between DNS, LES, and RANS?</b></summary>

- **DNS** resolves all turbulent scales. It is accurate but its cost grows steeply with Reynolds number, so it is mainly a research tool.
- **LES** resolves the large eddies and models the smaller ones. It gives unsteady detail at considerably higher cost than RANS.
- **RANS** solves time-averaged equations and models all turbulence through a closure. It is the workhorse of industrial CFD.

See [turbulence modeling](notes/fluid_mechanics/turbulence/modeling.md).

</details>

<details>
<summary><b>What is y+ and why does it matter?</b></summary>

$y^+$ is the wall distance of the first cell centre in viscous units. It decides how the near-wall region must be treated:

- $y^+ \lesssim 1$: the viscous sublayer is resolved (low-Reynolds-number models)
- $30 \lesssim y^+ \lesssim 300$: wall functions bridge the log layer
- $5 < y^+ < 30$: the buffer layer, where neither approach is accurate

See [RANS equations](notes/fluid_mechanics/turbulence/rans_equations.md) and [boundary-layer meshing](practice/mesh_generation/boundary_layers.md).

</details>

## References

### Online courses and resources

- [CFD Python: 12 Steps to Navier-Stokes](https://lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/) by Lorena Barba: a hands-on introduction to CFD in Python, built up in small steps
- [CFD General Principles](https://doc.cfd.direct/notes/cfd-general-principles/) by CFD Direct: fundamental concepts from the maintainers of OpenFOAM
- [Scientific Computing (Chasnov): Computational Fluid Dynamics](https://math.libretexts.org/Bookshelves/Scientific_Computing_Simulations_and_Modeling/Scientific_Computing_\(Chasnov\)/III%3A_Computational_Fluid_Dynamics/14%3A_The_Governing_Equations): governing equations and numerical methods
- [National Committee for Fluid Mechanics Films](https://youtube.com/playlist?list=PL0EC6527BE871ABA3): classic educational films on fluid phenomena

### Validation and benchmark data

- [NASA Turbulence Modeling Resource](https://turbmodels.larc.nasa.gov/): verification and validation cases for turbulence models
- [Wall-Modeled LES Resource](https://wmles.umd.edu/): WMLES database and guidelines
- [Airfoil Tools](http://www.airfoiltools.com/): airfoil geometry and performance data
- [NWTF Experimental Database](https://www.nwtf.ac.uk/dataset/2687/): Airbus wind tunnel dataset for the RAE2822 transonic aerofoil
- [DepositOnce (TU Berlin)](https://depositonce.tu-berlin.de/): research data repository

### Textbooks

| Book | Authors | Best for | Level |
| --- | --- | --- | --- |
| [Computational Fluid Dynamics: The Basics with Applications](https://amzn.to/42iuJNV) | John D. Anderson | Introduction with an aerospace emphasis | Beginner–intermediate |
| [An Introduction to Computational Fluid Dynamics: The Finite Volume Method](https://amzn.to/3EbEMfG) | H. K. Versteeg & W. Malalasekera | Clear introduction to the finite volume method | Beginner–intermediate |
| [Computational Methods for Fluid Dynamics](https://amzn.to/3FSZ9iq) | J. H. Ferziger, M. Perić & R. L. Street | Comprehensive graduate-level treatment | Advanced |
| [Numerical Heat Transfer and Fluid Flow](https://amzn.to/42qd0o1) | Suhas V. Patankar | The classic text on the SIMPLE algorithm | Intermediate |
| [Computational Fluid Dynamics: Principles and Applications](https://amzn.to/4j7adqY) | J. Blazek | Practical guidance for industrial CFD codes | Intermediate–advanced |
| [Data-Driven Science and Engineering](https://amzn.to/3RHJncw) | S. L. Brunton & J. N. Kutz | Machine learning for dynamical systems, POD, DMD | Intermediate–advanced |
| [Machine Learning Control](https://amzn.to/4jeggJC) | T. Duriez, S. L. Brunton & B. R. Noack | Machine learning for flow control | Advanced |

### Papers

- [Machine Learning for Fluid Mechanics](https://arxiv.org/abs/1905.11075) (Brunton, Noack & Koumoutsakos): review of machine learning in fluid mechanics
- [Machine Learning-Based CFD Simulations: A Review](https://link.springer.com/article/10.1007/s00521-022-07838-6): models, open problems, and future directions (2022)
- [Physics-Informed Neural Networks](https://www.brown.edu/research/projects/crunch/sites/brown.edu.research.projects.crunch/files/uploads/Physics-informed%20neural%20networks_A%20deep%20learning%20framwork%20fir%20solving%20forward%20and%20inverse%20probelms%20involving%20nonlinear%20partial%20differential%20equations.pdf) (Raissi, Perdikaris & Karniadakis): the original PINN paper
- [Machine Learning in CFD: Recent Advances](https://www.tandfonline.com/doi/full/10.1080/10618562.2023.2175788) (2023)
- [Nature Reviews article from the Karniadakis group](https://www.brown.edu/research/projects/crunch/sites/brown.edu.research.projects.crunch/files/uploads/Nature-REviews_GK.pdf): review of physics-informed computational methods
- [CFD of the Future: Year 2025 and Beyond](https://www.researchgate.net/publication/339808378_CFD_of_the_Future_Year_2025_and_Beyond): perspectives on AI, HPC, and uncertainty quantification
- [Pratt & Whitney: The Aircraft Engine and Its Operation (1949)](https://www.scribd.com/document/307072703/Pratt-Whitney-The-Aircraft-Engine-and-Its-Operation-Rev1949-BZ): historical engineering reference

### Code

- [Machine Learning and Simulation](https://github.com/Ceyron/machine-learning-and-simulation) by Ceyron: ML techniques combined with physics simulations
- [NVIDIA Modulus airfoil optimisation](https://github.com/neo-fetch/nvidia-modulus-airfoil-optimisation): GPU-accelerated physics-informed ML, including a [2D lid-driven cavity example](https://github.com/neo-fetch/nvidia-modulus-airfoil-optimisation/blob/master/Dr-Yang_ldc_2d.py)
- [Introductory Finite Elements (EAFIT)](https://github.com/AppliedMechanics-EAFIT/Introductory-Finite-Elements): FEM course material with Python implementations
- [DOLFINx tutorial](https://jsdokken.com/dolfinx-tutorial/fem.html): finite elements with FEniCSx
- [David Penner's CFD projects](https://davidpenner74.wixsite.com/davidpenner/projects): portfolio of applied CFD projects

### Video lectures

- [AeroCFD lecture series](https://www.youtube.com/@AeroCFD): university-level CFD lectures
- [Computational Fluid Dynamics, ME615, IIT Mandi](https://youtube.com/playlist?list=PLOUcBDsCNnMweTuft1qq25CQbyyKqZKvI): a complete university CFD course
- [Qiqi Wang's CFD lectures](https://www.youtube.com/c/QiqiWangGG): numerical analysis for CFD
- [The Perić lectures on CFD](https://youtu.be/8a0j2DQiTVQ): an industry perspective
- [Numerical methods by hand](https://youtube.com/playlist?list=PL5_Bm_WH1i3fAQP6G2_SaazjNIy3m8QbH): algorithms worked through manually
- [Mechanics problems solved by hand](https://youtube.com/playlist?list=PL7FF084F8C414D602)
- [Postcard Professor](https://www.youtube.com/c/PostcardProfessor/playlists): step-by-step mechanics problem solving
- [Additional worked solutions](https://www.youtube.com/watch?v=PPt_FfoUqBQ&list=PLD45F0FD958B864AD)
- [Theoretical mechanics and numerical methods](https://www.youtube.com/channel/UCcqQi9LT0ETkRoUu8eYaEkg)
- [Data-Driven Methods for Science and Engineering seminar](https://youtube.com/playlist?list=PLWL3MaEZQ5I0x5SoN-whc6wfxvZr4E5v9)
- [Gentle introduction to fluid concepts](https://www.youtube.com/watch?v=zGuVWSKBc4Y&list=PLyYlZ2ZyWpnh6Xy8xsqIFQKPiMzVkUkdG)

## Contributing

Corrections, new notes, and new scripts are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the conventions and the checks to run, and see the [roadmap](ROADMAP.md) for topics that still need writing. Bug reports and suggestions go in [issues](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/issues); open-ended ideas can go in [discussions](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/discussions).

## License

Released under the [MIT License](LICENSE).
