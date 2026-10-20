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
| Theory notes | 152 | [`notes/`](notes/) |
| Notes with exercises | 152 | [`notes/`](notes/) |
| Practice guides | 14 | [`practice/`](practice/) |
| Algorithm scripts | 69 | [`scripts/algorithms/`](scripts/algorithms/) |
| Plot scripts | 75 | [`scripts/plots/`](scripts/plots/) |
| Simulations | 26 | [`scripts/simulations/`](scripts/simulations/) |

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
python main.py --reel cavity.mp4                # vertical video for Shorts/Reels
```

Every script accepts `--no-show` and `--output DIR`. Time-stepping and interactive scripts also accept `--steps N`. Every simulation can also render itself as a 1080 × 1920 video with `--reel FILE`, and `python tools/make_reels.py` renders all of them at once (see [`scripts/README.md`](scripts/README.md#shorts-and-reels)). Each script folder has a README explaining the maths, the implementation, and the output.

## Learning paths

Each path is a suggested reading order through material that exists in this repository.

### 1. First steps in CFD

*Prerequisites: calculus, basic physics, some Python.*

1. [Introduction to fluid mechanics](notes/fluid_mechanics/intro.md) and [dimensional analysis](notes/fluid_mechanics/dimensions.md)
2. [Navier–Stokes equations](notes/fluid_mechanics/governing_equations/navier_stokes.md)
3. [Why CFD is needed](notes/numerical/cfd/intro.md) and [the strategy of CFD](notes/numerical/cfd/cfd_process.md)
4. [Finite difference method](notes/numerical/fdm/intro.md), then run the [1D heat and wave equations](scripts/simulations/1d_heat_and_wave_equations/)
5. [Numerical stability](notes/numerical/cfd/numerical_stability.md) and [boundary conditions](notes/numerical/cfd/boundary_conditions.md)
6. Run the [lid-driven cavity](scripts/simulations/lid_driven_cavity/) and read the [lid-driven cavity tutorial](practice/manual_projects/lid_driven_cavity.md)

### 2. Numerical methods in depth

*Prerequisites: path 1, linear algebra.*

1. [Finite-difference stencils](notes/numerical/fdm/discretization.md) and [time integration](notes/numerical/cfd/time_integration.md)
2. [Finite volume method](notes/numerical/fvm/intro.md), [finite-volume discretization](notes/numerical/fvm/discretization.md) and [convection schemes](notes/numerical/fvm/convection_schemes.md), with the [1D convection–diffusion](scripts/algorithms/fvm_convection_diffusion_1d/) and [TVD limiter](scripts/algorithms/tvd_limiters_advection/) scripts
3. [Pressure–velocity coupling](notes/numerical/fvm/pressure_velocity_coupling.md) and [Riemann solvers](notes/numerical/fvm/riemann_solvers.md), then run the [Sod shock tube](scripts/simulations/sod_shock_tube/)
4. [Finite element method](notes/numerical/fem/intro.md), [weak formulations](notes/numerical/fem/weak_formulation_pde.md) and [high-order methods](notes/numerical/high_order/intro.md)
5. [Dealing with nonlinearity](notes/numerical/cfd/dealing_with_nonlinearity.md), [direct and iterative solvers](notes/numerical/cfd/direct_and_iterative_solvers.md), and [iterative convergence](notes/numerical/cfd/iterative_convergence.md)
6. [Verification and validation](notes/numerical/cfd/verification_and_validation.md), with the [method of manufactured solutions](scripts/algorithms/method_of_manufactured_solutions/) script
7. [Lattice Boltzmann method](notes/numerical/lattice_boltzmann/intro.md), then run the [lattice Boltzmann cylinder flow](scripts/simulations/lattice_boltzmann_cylinder_flow/)

### 3. Engineering practice

*Prerequisites: an engineering background.*

1. [Boundary layers](notes/fluid_mechanics/viscous_flow/boundary_layers.md) and [turbulence](notes/fluid_mechanics/turbulence/)
2. [Turbulence modeling in CFD](notes/numerical/cfd/turbulence_modeling.md)
3. [Mesh quality](practice/mesh_generation/mesh_quality.md) and [boundary-layer meshing](practice/mesh_generation/boundary_layers.md)
4. [Gmsh](practice/gmsh/intro.md), [OpenFOAM](practice/openfoam/getting_started.md), and [ParaView](practice/paraview/intro.md)
5. [Flow over a cylinder](practice/manual_projects/flow_over_cylinder.md) end to end
6. [Solver comparison](practice/cfd_tools/solver_comparison.md) and [workflow automation](practice/cfd_tools/automation.md)
7. From flow to structure: [fluid loading](notes/applied_mechanics/fluid_loading/intro.md), [flow-induced vibrations](notes/applied_mechanics/fluid_loading/flow_induced_vibrations.md) and [fluid–structure interaction](notes/applied_mechanics/fluid_loading/fluid_structure_interaction.md), with the [surface force integration](scripts/algorithms/fluid_loading_surface_force_integration/) and [partitioned FSI](scripts/algorithms/fluid_loading_partitioned_fsi/) scripts

### 4. Data-driven methods

*Prerequisites: linear algebra, Python, CFD basics.*

1. [Proper orthogonal decomposition](notes/numerical/pod/pod_intro.md), [POD and the SVD](notes/numerical/pod/pod_vs_svd.md), and [snapshot POD](notes/numerical/pod/snapshot_pod.md), with the [POD](scripts/algorithms/pod/) and [snapshot POD](scripts/algorithms/snapshot_pod/) scripts
2. [Reduced-order modeling](notes/numerical/rom/rom.md), [POD–Galerkin projection](notes/numerical/rom/pod_galerkin_projection.md), [reduced basis approximation](notes/numerical/rom/reduced_basis_approximation.md) and [dynamic mode decomposition](notes/numerical/rom/dmd.md), with the [POD–Galerkin Burgers](scripts/algorithms/pod_galerkin_burgers/) and [reduced basis](scripts/algorithms/reduced_basis_thermal_block/) scripts
3. [Surrogate models](notes/numerical/surrogates/intro.md), [kriging](notes/numerical/surrogates/kriging.md), and [radial basis functions](notes/numerical/surrogates/radial_basis_functions.md), with the [kriging](scripts/algorithms/kriging_interpolation/) and [RBF](scripts/algorithms/radial_basis_functions/) scripts
4. [Machine learning for CFD](notes/machine_learning/intro.md), then [neural networks](notes/machine_learning/fundamentals/neural_networks.md) and [training and validation](notes/machine_learning/fundamentals/training_and_validation.md)
5. [Neural-network surrogates](notes/machine_learning/neural_networks/intro.md), [physics-informed neural networks](notes/machine_learning/neural_networks/pinns.md), and [neural operators](notes/machine_learning/neural_networks/neural_operators.md), with the [MLP](scripts/algorithms/mlp_regression/), [PINN](scripts/algorithms/pinn_boundary_layer/) and [Fourier neural operator](scripts/algorithms/fourier_neural_operator_1d/) scripts
6. [Flow dynamics](notes/machine_learning/flow/flow_dynamics.md) with the [DMD](scripts/algorithms/dynamic_mode_decomposition/) and [SINDy](scripts/algorithms/sindy_lorenz/) scripts, then [machine-learned turbulence closures](notes/machine_learning/flow/ml_turbulence_closures.md)
7. The [automotive aerodynamics case study](notes/machine_learning/automotive_aerodynamics/), which follows one project from design space to trained model

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
| [CFD fundamentals](notes/numerical/cfd/) | [Why CFD](notes/numerical/cfd/intro.md), [strategy of CFD](notes/numerical/cfd/cfd_process.md), [governing equations](notes/numerical/cfd/governing_equations.md), [boundary conditions](notes/numerical/cfd/boundary_conditions.md), [verification and validation](notes/numerical/cfd/verification_and_validation.md), [turbulence modeling](notes/numerical/cfd/turbulence_modeling.md) |
| [Solving the discrete equations](notes/numerical/cfd/) | [Nonlinearity](notes/numerical/cfd/dealing_with_nonlinearity.md), [direct and iterative solvers](notes/numerical/cfd/direct_and_iterative_solvers.md), [iterative convergence](notes/numerical/cfd/iterative_convergence.md), [numerical stability](notes/numerical/cfd/numerical_stability.md), [time integration](notes/numerical/cfd/time_integration.md) |
| [Finite differences](notes/numerical/fdm/) | [Introduction](notes/numerical/fdm/intro.md), [stencils and modified wavenumber](notes/numerical/fdm/discretization.md) |
| [Finite volumes](notes/numerical/fvm/) | [Introduction](notes/numerical/fvm/intro.md), [discretization on general meshes](notes/numerical/fvm/discretization.md), [convection schemes and TVD](notes/numerical/fvm/convection_schemes.md), [pressure–velocity coupling](notes/numerical/fvm/pressure_velocity_coupling.md), [Riemann solvers](notes/numerical/fvm/riemann_solvers.md) |
| [Finite elements](notes/numerical/fem/) | [Introduction](notes/numerical/fem/intro.md), [weak formulation](notes/numerical/fem/weak_formulation_pde.md) |
| [High-order methods](notes/numerical/high_order/) | [Spectral and discontinuous Galerkin methods](notes/numerical/high_order/intro.md) |
| [Lattice Boltzmann](notes/numerical/lattice_boltzmann/) | [Introduction](notes/numerical/lattice_boltzmann/intro.md), [from Newton to Navier–Stokes](notes/numerical/lattice_boltzmann/from_newton_to_nse.md), [Boltzmann equation](notes/numerical/lattice_boltzmann/boltzmann_equation.md), [from Boltzmann to lattice Boltzmann](notes/numerical/lattice_boltzmann/from_boltzmann_to_lattice_boltzmann.md), [algorithm](notes/numerical/lattice_boltzmann/lattice_boltzmann_algorithm.md), [in practice](notes/numerical/lattice_boltzmann/practical_lbm.md) |
| [Proper orthogonal decomposition](notes/numerical/pod/) | [Introduction](notes/numerical/pod/pod_intro.md), [derivation in 2D](notes/numerical/pod/derivation_in_2d.md), [derivation in N dimensions](notes/numerical/pod/derivation_in_n_dim.md), [POD and SVD](notes/numerical/pod/pod_vs_svd.md), [snapshot POD](notes/numerical/pod/snapshot_pod.md), [gappy POD](notes/numerical/pod/gappy_pod.md) |
| [Reduced-order models](notes/numerical/rom/) | [Overview](notes/numerical/rom/rom.md), [parameterized variational problems](notes/numerical/rom/parameterized_variational_problems.md), [discretization techniques](notes/numerical/rom/discretization_techniques.md), [reduced basis approximation](notes/numerical/rom/reduced_basis_approximation.md), [POD–Galerkin projection](notes/numerical/rom/pod_galerkin_projection.md), [dynamic mode decomposition](notes/numerical/rom/dmd.md) |
| [Surrogate models](notes/numerical/surrogates/) | [Introduction](notes/numerical/surrogates/intro.md), [one-stage sampling](notes/numerical/surrogates/one_stage_sampling.md), [radial basis functions](notes/numerical/surrogates/radial_basis_functions.md), [kriging](notes/numerical/surrogates/kriging.md), [hierarchical kriging](notes/numerical/surrogates/hierarchical_kriging.md), [adaptive sampling](notes/numerical/surrogates/adaptive_sampling.md) |

### [Machine learning](notes/machine_learning/)

| Topic | Notes |
| --- | --- |
| Overview | [Introduction to machine learning for CFD](notes/machine_learning/intro.md) |
| [Fundamentals](notes/machine_learning/fundamentals/) | [Neural networks](notes/machine_learning/fundamentals/neural_networks.md), [training and validation](notes/machine_learning/fundamentals/training_and_validation.md) |
| [Neural networks](notes/machine_learning/neural_networks/) | [Neural-network surrogates for aerodynamics](notes/machine_learning/neural_networks/intro.md), [graph neural networks](notes/machine_learning/neural_networks/graph_neural_networks.md), [physics-informed neural networks](notes/machine_learning/neural_networks/pinns.md), [neural operators](notes/machine_learning/neural_networks/neural_operators.md) |
| [Flow](notes/machine_learning/flow/) | [Feature extraction](notes/machine_learning/flow/feature_extraction.md), [flow dynamics](notes/machine_learning/flow/flow_dynamics.md), [turbulence closures](notes/machine_learning/flow/ml_turbulence_closures.md), [particle image velocimetry](notes/machine_learning/flow/particle_image_velocimetry.md), [super-resolution and flow cleansing](notes/machine_learning/flow/superresolution_and_flow_cleansing.md), [optimization](notes/machine_learning/flow/optimization.md) |
| [Geometry](notes/machine_learning/geometry/) | [Machine learning on CAD](notes/machine_learning/geometry/ml_on_cad.md), [mesh generation and adaptation](notes/machine_learning/geometry/ml_with_meshes.md) |
| [Automotive aerodynamics](notes/machine_learning/automotive_aerodynamics/) | [Case-study overview](notes/machine_learning/automotive_aerodynamics/ml_process.md), [deformation parameters](notes/machine_learning/automotive_aerodynamics/deformation_parameters.md), [design of experiments](notes/machine_learning/automotive_aerodynamics/datasets.md), [generating CFD training data](notes/machine_learning/automotive_aerodynamics/generating_cfd_datasets.md), [mesh dataset](notes/machine_learning/automotive_aerodynamics/dataset_of_meshes.md), [output data](notes/machine_learning/automotive_aerodynamics/output_data.md), [model training](notes/machine_learning/automotive_aerodynamics/model_training.md) |

### [Applied mechanics](notes/applied_mechanics/)

| Topic | Notes |
| --- | --- |
| [Fundamentals](notes/applied_mechanics/fundamentals/) | [Introduction](notes/applied_mechanics/fundamentals/intro.md), [vector analysis](notes/applied_mechanics/fundamentals/vector_analysis.md), [force systems](notes/applied_mechanics/fundamentals/force_systems.md), [moments and couples](notes/applied_mechanics/fundamentals/moments_couples.md), [free body diagrams](notes/applied_mechanics/fundamentals/free_body_diagrams.md) |
| [Statics](notes/applied_mechanics/statics/) | [Particle equilibrium](notes/applied_mechanics/statics/particle_equilibrium.md), [rigid-body equilibrium](notes/applied_mechanics/statics/rigid_body_equilibrium.md), [structural analysis](notes/applied_mechanics/statics/structural_analysis.md), [trusses, frames and machines](notes/applied_mechanics/statics/trusses_frames.md), [friction](notes/applied_mechanics/statics/friction.md), [centroids](notes/applied_mechanics/statics/center_of_mass.md), [virtual work](notes/applied_mechanics/statics/virtual_work.md) |
| [Dynamics](notes/applied_mechanics/dynamics/) | [Particle kinematics](notes/applied_mechanics/dynamics/kinematics_particles.md), [particle kinetics](notes/applied_mechanics/dynamics/kinetics_particles.md), [rigid-body kinematics](notes/applied_mechanics/dynamics/rigid_body_kinematics.md), [rigid-body kinetics](notes/applied_mechanics/dynamics/rigid_body_kinetics.md), [work and energy](notes/applied_mechanics/dynamics/work_energy.md), [impulse and momentum](notes/applied_mechanics/dynamics/impulse_momentum.md), [vibrations](notes/applied_mechanics/dynamics/vibrations.md), [Lagrangian mechanics](notes/applied_mechanics/dynamics/lagrangian_mechanics.md) |
| [Strength of materials](notes/applied_mechanics/strength_materials/) | [Stress and strain](notes/applied_mechanics/strength_materials/stress_strain.md), [material properties](notes/applied_mechanics/strength_materials/material_properties.md), [axial loading](notes/applied_mechanics/strength_materials/axial_loading.md), [torsion](notes/applied_mechanics/strength_materials/torsion.md), [shear and moment diagrams](notes/applied_mechanics/strength_materials/shear_moment.md), [beam bending](notes/applied_mechanics/strength_materials/beam_bending.md), [combined loading](notes/applied_mechanics/strength_materials/combined_loading.md), [buckling](notes/applied_mechanics/strength_materials/buckling.md), [fatigue](notes/applied_mechanics/strength_materials/fatigue.md) |
| [Fluid loading](notes/applied_mechanics/fluid_loading/) | [Introduction](notes/applied_mechanics/fluid_loading/intro.md), [pressure forces](notes/applied_mechanics/fluid_loading/pressure_forces.md), [wind loading](notes/applied_mechanics/fluid_loading/wind_loading.md), [wave loading](notes/applied_mechanics/fluid_loading/wave_loading.md), [flow-induced vibrations](notes/applied_mechanics/fluid_loading/flow_induced_vibrations.md), [hydroelasticity](notes/applied_mechanics/fluid_loading/hydroelastic_applications.md), [fluid–structure interaction](notes/applied_mechanics/fluid_loading/fluid_structure_interaction.md) |
| [Control systems](notes/applied_mechanics/control_systems/) | [Introduction](notes/applied_mechanics/control_systems/intro.md), [system modeling](notes/applied_mechanics/control_systems/system_modeling.md), [stability analysis](notes/applied_mechanics/control_systems/stability_analysis.md), [frequency response](notes/applied_mechanics/control_systems/frequency_response.md), [feedback control](notes/applied_mechanics/control_systems/feedback_control.md), [PID controllers](notes/applied_mechanics/control_systems/pid_controllers.md) |
| [Mechanical systems](notes/applied_mechanics/mechanical_systems/) | [Mechanisms](notes/applied_mechanics/mechanical_systems/mechanisms.md), [gears](notes/applied_mechanics/mechanical_systems/gears.md), [bearings](notes/applied_mechanics/mechanical_systems/bearings.md), [rotating machinery](notes/applied_mechanics/mechanical_systems/rotating_machinery.md), [hydraulics and pneumatics](notes/applied_mechanics/mechanical_systems/hydraulic_pneumatic.md) |
| [Airplanes](notes/applied_mechanics/transportation/airplanes/) | [How airplanes fly](notes/applied_mechanics/transportation/airplanes/how_airplanes_work.md), [airfoil design](notes/applied_mechanics/transportation/airplanes/airfoil_design.md), [reading airfoil polars](notes/applied_mechanics/transportation/airplanes/airfoil_tools_walkthrough.md), [Reynolds number](notes/applied_mechanics/transportation/airplanes/reynolds_number.md), [airplane stability](notes/applied_mechanics/transportation/airplanes/airplane_stability.md), [static and dynamic stability](notes/applied_mechanics/transportation/airplanes/pecking.md), [inertial navigation](notes/applied_mechanics/transportation/airplanes/inertial_navigation_systems.md), [design and manufacturing](notes/applied_mechanics/transportation/airplanes/manufacturing_and_design_process.md) |
| [Cars](notes/applied_mechanics/transportation/cars/) | [How cars work](notes/applied_mechanics/transportation/cars/how_cars_work.md), [design and manufacturing](notes/applied_mechanics/transportation/cars/manufacturing_and_design_process.md) |

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
| [Adaptive Mesh Sizing](scripts/algorithms/adaptive_mesh_sizing/) | This script learns a mesh-size field for a one-dimensional convection-diffusion boundary layer from optimally adapted training cases and uses it to mesh Peclet numbers it has not seen. |
| [Adaptive Sampling with Kriging](scripts/algorithms/adaptive_sampling_kriging/) | This script grows a kriging surrogate of a two-dimensional test function from an 8-point Latin hypercube to 40 samples by adding one point at a time, once by maximizing the kriging mean squared error and once by maximizing a leave-one-out cross-validation error indicator times the kriging standard deviation, and compares both with one-shot maximin Latin hypercubes of the same size. |
| [Airfoil Shape PCA](scripts/algorithms/airfoil_shape_pca/) | This script builds a linear shape space for NACA 4-digit airfoils by principal component analysis (PCA) of their surface coordinates and shows how few modes are needed to describe the family. |
| [Longitudinal Modes of a Light Aircraft](scripts/algorithms/airplane_longitudinal_modes/) | This script finds the short-period and phugoid modes of a representative 1100 kg light aircraft from its linearized longitudinal equations, compares them with the classical two-mode approximations, and shows how a pilot with a reaction delay can turn the well-damped short period into a pilot-induced oscillation. |
| [Thin-Airfoil Theory, Panel Method and Drag Polar](scripts/algorithms/airplane_thin_airfoil_and_polar/) | This script computes the lift of a NACA 4-digit airfoil with thin-airfoil theory and with a Hess–Smith panel method, then turns the section result into a finite-wing lift curve, a parabolic drag polar and the power-required curve of a light aircraft. |
| [Bayesian Optimization](scripts/algorithms/bayesian_optimization/) | This script minimizes a one-dimensional drag-like test function and the two-dimensional Branin function by Bayesian optimization: a Gaussian-process (GP) surrogate with a squared-exponential kernel, hyperparameters fitted by maximum marginal likelihood, and the expected-improvement (EI) acquisition function of the EGO algorithm. |
| [Shear and Moment Diagrams of Beams](scripts/algorithms/beams_shear_moment_diagrams/) | This script solves statically determinate and indeterminate beams with Euler–Bernoulli finite elements and draws the load, shear-force, bending-moment and deflection diagrams with their extreme values. |
| [Journal Bearing Reynolds Equation](scripts/algorithms/bearings_journal_reynolds/) | This script solves the Reynolds equation of a hydrodynamic journal bearing by finite differences and reproduces the classical load-capacity results: the closed-form full-Sommerfeld solution of the long bearing, the effect of film rupture under the Reynolds cavitation condition, and the Raimondi–Boyd design table for a bearing with $L/D = 1$. |
| [Car Road Load and Quarter-Car Ride](scripts/algorithms/car_road_load_and_quarter_car/) | This script computes the road-load power and energy demand of a mid-size car and the ride response of a quarter-car suspension model. |
| [Condition Number of the Correlation Matrix](scripts/algorithms/condition_number_of_the_correlation_matrix/) | This script plots how the condition number of a kriging correlation matrix changes with the correlation parameter $\theta$ for the linear, exponential, Gaussian and cubic spline correlation functions. |
| [Bode and Nyquist Margins](scripts/algorithms/control_bode_nyquist/) | This script computes the Bode magnitude and phase with straight-line asymptotes, the gain, phase and delay margins, the Nyquist plot and its encirclements of $-1$, the sensitivity functions and the closed-loop step response of a tank level loop with and without a transport delay. |
| [PID Tuning and Windup](scripts/algorithms/control_pid_tuning/) | This script tunes a PID controller for a first-order-plus-dead-time process with the Ziegler–Nichols and SIMC rules, compares the set-point and load responses and the stability margins, and shows integrator windup under actuator saturation with and without back-calculation. |
| [Root Locus and Routh–Hurwitz](scripts/algorithms/control_root_locus/) | This script computes the root locus of a third-order position servo by sweeping the gain, marks the asymptotes, breakaway point and damping-ratio design point, and checks that the gain where the locus crosses the imaginary axis equals the Routh–Hurwitz critical gain. |
| [Second-Order Step Response](scripts/algorithms/control_second_order_response/) | This script simulates the step response of the standard second-order system for six damping ratios, measures rise time, peak time, overshoot and settling time, and compares them with the closed-form formulas and the pole locations. |
| [Correlation Functions](scripts/algorithms/correlation_functions/) | This script plots six correlation functions used in kriging surrogate models (linear, exponential, Matérn 3/2, Matérn 5/2, cubic spline and Gaussian) for several values of the correlation parameter $\theta$. |
| [Discontinuous Galerkin Linear Advection](scripts/algorithms/dg_linear_advection/) | This script solves the 1D periodic linear advection equation $`u_t + a\,u_x = 0`$ with the discontinuous Galerkin (DG) method, using Legendre polynomials of degree $p = 0$ to 3 in every element, an upwind numerical flux and the three-stage SSP Runge–Kutta method, and confirms that the error falls as $h^{p+1}$. |
| [Dynamic Mode Decomposition (DMD)](scripts/algorithms/dynamic_mode_decomposition/) | This script applies exact dynamic mode decomposition to a noisy synthetic 1D wave field built from three wave packets whose frequencies and growth rates are known, and checks how well DMD recovers them. |
| [Double Pendulum from Lagrange's Equations](scripts/algorithms/dynamics_double_pendulum_lagrange/) | This script integrates the Lagrange equations of a planar double pendulum and compares its small-amplitude motion with the normal modes of the linearized equations. |
| [Projectile with Quadratic Drag](scripts/algorithms/dynamics_projectile_drag/) | This script integrates Newton's second law for a projectile with quadratic air drag and compares it with the drag-free parabola. |
| [SDOF Vibration Response](scripts/algorithms/dynamics_sdof_response/) | This script computes the free and forced response of a single-degree-of-freedom mass–spring–damper and checks the Newmark-β integrator against the closed-form free response. |
| [Slider-Crank Kinematics](scripts/algorithms/dynamics_slider_crank_kinematics/) | This script solves the velocity and acceleration of a slider-crank mechanism with the rigid-body relative-motion equations and checks the results against finite differences of the exact slider position. |
| [Torque-Free Rigid Body Rotation](scripts/algorithms/dynamics_torque_free_rigid_body/) | This script integrates Euler's equations for a rigid box spinning with no applied moment and shows that rotation about the axis of intermediate moment of inertia is unstable. |
| [Two-DOF Normal Modes and Tuned Mass Damper](scripts/algorithms/dynamics_two_dof_modes/) | This script solves the generalized eigenproblem of a two-degree-of-freedom spring–mass chain and uses it to explain the tuned mass damper. |
| [Variable-Mass Rocket](scripts/algorithms/dynamics_variable_mass_rocket/) | This script integrates the momentum balance of a vertically launched rocket and splits its burnout speed into the ideal rocket-equation increment, the gravity loss and the drag loss. |
| [1D Poisson Equation With Finite Elements](scripts/algorithms/fem_1d_poisson/) | This script solves the 1D Poisson equation $-u'' = f$ on $(0, 1)$ with homogeneous Dirichlet conditions by the Galerkin finite element method with linear (P1) and quadratic (P2) Lagrange elements, and confirms the a priori error estimates: the $L^2$ error falls as $h^{p+1}$ and the $H^1$ error as $h^p$. |
| [Finite-Difference Stencils](scripts/algorithms/finite_difference_stencils/) | This script computes finite-difference weights for any set of stencil offsets by solving the Taylor-series (Vandermonde) system, then measures how the error of each stencil depends on the grid spacing and how well it represents each Fourier wavenumber. |
| [Flow Super-Resolution](scripts/algorithms/flow_superresolution/) | This script reconstructs a $128 \times 128$ velocity field from its $4\times$ block average with cubic-spline (bicubic) interpolation and with a learned linear patch model, then denoises noisy vortex-street snapshots by truncating their proper orthogonal decomposition (POD). |
| [Morison Wave Force on a Vertical Pile](scripts/algorithms/fluid_loading_morison_wave_force/) | This script computes the wave force on a vertical pile by integrating the Morison equation over the depth with linear (Airy) wave kinematics. |
| [Partitioned Fluid–Structure Coupling and the Added-Mass Instability](scripts/algorithms/fluid_loading_partitioned_fsi/) | This script couples a structure solver and a fluid solver through their interface in the Dirichlet–Neumann way used by partitioned FSI codes, and shows that explicit coupling becomes unstable once the added mass of the fluid exceeds the structural mass, whatever the time step, while implicit coupling with Aitken relaxation converges to the monolithic solution. |
| [Surface Force Integration over Boundary Faces](scripts/algorithms/fluid_loading_surface_force_integration/) | This script integrates a surface pressure and wall-shear field over the flat faces of a body into a force and a moment, the same face sum a CFD code uses to report drag, lift and moment coefficients. |
| [Vortex-Induced Vibration with a Wake Oscillator](scripts/algorithms/fluid_loading_viv_wake_oscillator/) | This script models vortex-induced vibration of an elastically mounted cylinder with the coupled structure and van der Pol wake oscillators of Facchinetti, de Langre and Biolley (2004). |
| [Fourier Neural Operator Layer in 1D](scripts/algorithms/fourier_neural_operator_1d/) | This script learns the solution operator $G: f \mapsto u$ of the periodic problem $-\nu u'' + u = f$ from 200 random forcing–solution pairs with a single spectral convolution, the linear part of a Fourier neural operator (FNO) layer, fitted by least squares. |
| [Moment of a Force About a Point and an Axis](scripts/algorithms/fundamentals_moment_about_axis/) | This script computes the moment of a 3D force about a point as a cross product and about an axis as a scalar triple product, and shows numerically which of the two depends on the choice of reference point. |
| [1D Finite-Volume Convection–Diffusion](scripts/algorithms/fvm_convection_diffusion_1d/) | This script solves steady 1D convection–diffusion with the finite volume method using central, upwind, hybrid, power-law and QUICK face values, and compares each with the exponential exact solution. |
| [Gappy POD Reconstruction](scripts/algorithms/gappy_pod_reconstruction/) | This script reconstructs complete flow fields from incomplete data with gappy POD: a POD basis built from complete snapshots of a synthetic cylinder wake is fitted by least squares to held-out snapshots of which only 50% of the points, or a few point sensors, are known. |
| [Ghost-Cell Boundary Conditions](scripts/algorithms/ghost_cell_boundary_conditions/) | This script compares first-order and second-order ways of imposing Neumann and Robin boundary conditions in finite-difference and finite-volume discretizations of a 1D diffusion problem. |
| [Grid Convergence Index](scripts/algorithms/grid_convergence_index/) | This script estimates discretization error from three meshes with Richardson extrapolation and the grid convergence index (GCI), following the procedure of Celik et al. (2008). |
| [Hierarchical Kriging for Multi-Fidelity Data](scripts/algorithms/hierarchical_kriging_multifidelity/) | This script fits a hierarchical kriging model to the one-dimensional Forrester test case, using a kriging model of 11 cheap low-fidelity samples as the trend of a kriging model of a few expensive high-fidelity samples, and compares it with ordinary kriging of the high-fidelity samples alone. |
| [Image Compression Using SVD](scripts/algorithms/image_compression_using_svd/) | This script compresses a grayscale image by keeping only its $r$ largest singular values and the matching singular vectors, then compares the rank-$`r`$ reconstructions with the original. |
| [INS Dead-Reckoning Errors](scripts/algorithms/ins_dead_reckoning_errors/) | This script simulates a two-dimensional strapdown inertial navigation system and shows how accelerometer bias, gyro bias and sensor noise turn into position error, and how a Kalman filter that fuses GNSS fixes keeps that error bounded. |
| [Iterative Linear Solvers on the Poisson Equation](scripts/algorithms/iterative_linear_solvers/) | This script solves the 2D Poisson equation on an $N \times N$ grid with Jacobi, Gauss–Seidel, SOR with the optimal relaxation factor, conjugate gradients and a geometric multigrid V-cycle, and compares how many iterations each needs as the grid is refined. |
| [Kriging Interpolation](scripts/algorithms/kriging_interpolation/) | This script builds an ordinary kriging model of the Forrester function $y(x) = (6x-2)^2 \sin(12x-4)$ from nine equally spaced samples with a compactly supported cubic correlation function, estimates the correlation parameter $\theta$ by maximum likelihood, and compares the predictor and its $\pm 2\hat{s}$ band for $\theta$ below, at and above the estimate. |
| [LBM Poiseuille Validation](scripts/algorithms/lbm_poiseuille_validation/) | This script validates a D2Q9 BGK lattice Boltzmann solver against the exact solution for body-force-driven channel flow with half-way bounce-back walls. |
| [LBM Taylor–Green Decay](scripts/algorithms/lbm_taylor_green_decay/) | This script measures the viscosity of the D2Q9 BGK lattice Boltzmann scheme from the decay of a Taylor–Green vortex and compares it with $\nu = c_s^2(\tau - 1/2)$. |
| [Learned Mixing-Length Closure](scripts/algorithms/learned_mixing_length_closure/) | This script learns a near-wall correction to Prandtl's mixing length from reference velocity data, then inserts the learned closure into a 1D RANS solver to check whether a good fit to the closure data also gives a good velocity profile. |
| [Axial Bar Finite Elements](scripts/algorithms/materials_axial_bar_fem/) | This script solves statically indeterminate axial bars with two-node finite elements and checks them against the hand solution from equilibrium and compatibility. |
| [Mohr's Circle for Plane Stress](scripts/algorithms/materials_mohr_circle/) | This script transforms a 2D plane-stress state and draws Mohr's circle with the given, rotated, principal and maximum-shear stress elements. |
| [Four-Bar Linkage Kinematics](scripts/algorithms/mechanisms_four_bar_linkage/) | This script solves the position, velocity and acceleration of a four-bar linkage over a full crank revolution by vector loop closure, using the Freudenstein equation for position and two linear 2 × 2 systems for the velocities and accelerations. |
| [Method of Manufactured Solutions](scripts/algorithms/method_of_manufactured_solutions/) | This script verifies a second-order finite-difference Poisson solver with the method of manufactured solutions (MMS) and shows how the same test exposes a first-order boundary treatment. |
| [MLP Regression](scripts/algorithms/mlp_regression/) | A two-hidden-layer tanh network written in numpy, with hand-coded backpropagation and Adam, learns a lift curve with stall from 60 noisy samples. |
| [Picard Iteration and Newton's Method for Steady Burgers](scripts/algorithms/picard_vs_newton/) | This script solves the discretized steady viscous Burgers equation, a 1D model of the convective nonlinearity in the Navier–Stokes equations, with Picard iteration and Newton's method and compares their convergence. |
| [PINN for a 1D Boundary Layer](scripts/algorithms/pinn_boundary_layer/) | This script trains a physics-informed neural network (PINN) on the steady advection–diffusion problem $\varepsilon u'' - u' = 0$, $u(0) = 0$, $u(1) = 1$, whose solution has a boundary layer of width about $\varepsilon$ at $x = 1$. |
| [PIV Cross-Correlation](scripts/algorithms/piv_cross_correlation/) | This script measures a known vortex displacement field from a synthetic pair of particle images with the standard particle image velocimetry (PIV) pipeline: FFT cross-correlation in interrogation windows, a three-point Gaussian sub-pixel peak fit, iterative window deformation, and the normalized median test for spurious vectors. |
| [Proper Orthogonal Decomposition (POD)](scripts/algorithms/pod/) | This script performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix. |
| [POD-Galerkin Reduced-Order Model of the Burgers Equation](scripts/algorithms/pod_galerkin_burgers/) | This script builds a POD-Galerkin reduced-order model (ROM) of the 1D viscous Burgers equation from snapshots of a 2000-point finite-difference solution, precomputes the reduced constant, linear and quadratic operators offline, and compares ROMs of 1 to 30 modes with the full-order model (FOM) inside the training window, in a later time window and at a new viscosity. |
| [Radial Basis Functions](scripts/algorithms/radial_basis_functions/) | This script interpolates eight samples of the Forrester function $y(x) = (6x-2)^2 \sin(12x-4)$ with six radial basis function (RBF) kernels, written directly in numpy, and plots the interpolants and their pointwise errors. |
| [Certified Reduced Basis Method for a Thermal Block](scripts/algorithms/reduced_basis_thermal_block/) | This script builds a certified reduced basis model of steady heat conduction in a 2D thermal block with three parametrized conductivities, using a weak greedy algorithm driven by the residual-based error bound $`\lVert r(\mu) \rVert_{X'}/\alpha_{\mathrm{LB}}(\mu)`$. |
| [Residual Monitoring During an Iterative Solve](scripts/algorithms/residual_monitoring/) | This script follows a Gauss–Seidel solve of the 2D Poisson equation sweep by sweep and records everything a CFD user might look at to decide whether the run has converged: the residual with two normalisations, the change between iterates, the true iterative error, and an integral quantity (the flux through a wall). |
| [Riemann Solver Comparison](scripts/algorithms/riemann_solver_comparison/) | This script compares five Riemann solvers inside the same first-order Godunov finite-volume scheme for the 1D Euler equations: the exact solver, Rusanov (local Lax–Friedrichs), HLL, HLLC and Roe with Harten's entropy fix. |
| [Jeffcott Rotor and Campbell Diagram](scripts/algorithms/rotor_jeffcott_campbell/) | This script computes the unbalance response of a Jeffcott rotor, amplitude and phase against speed for several damping ratios, and the Campbell diagram of an overhung disk whose gyroscopic moment splits each whirl mode into a forward and a backward branch. |
| [SIMPLE in a 1D Converging Nozzle](scripts/algorithms/simple_1d_nozzle/) | This script solves steady, incompressible, frictionless flow through a converging nozzle with the SIMPLE and SIMPLEC pressure–velocity coupling algorithms on a staggered grid, and compares the converged mass flow and pressure with Bernoulli's equation. |
| [SINDy on the Lorenz System](scripts/algorithms/sindy_lorenz/) | This script identifies the Lorenz equations from a noisy simulated trajectory with sparse identification of nonlinear dynamics (SINDy), using sequential thresholded least squares over a library of cubic polynomials. |
| [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](scripts/algorithms/snapshot_pod/) | This script computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one. |
| [Sobol Sensitivity Analysis](scripts/algorithms/sobol_sensitivity_analysis/) | This script estimates first-order and total Sobol sensitivity indices of a synthetic five-parameter drag model with the Saltelli sampling scheme and checks them against the exact values. |
| [Spectral vs Finite-Difference Differentiation](scripts/algorithms/spectral_vs_finite_difference/) | This script differentiates a smooth periodic function with the Fourier spectral method and with second- and fourth-order central finite differences, and shows that the spectral error falls exponentially with the number of points while the finite-difference errors fall algebraically. |
| [Plane Truss Solver](scripts/algorithms/statics_truss_solver/) | This script solves a plane pin-jointed truss by the method of joints and by the direct stiffness method. |
| [Stability Regions of Time Integrators](scripts/algorithms/time_integrator_stability/) | This script draws the absolute-stability regions of explicit Euler, RK2, RK3, RK4, AB2 and BDF2 and overlays the eigenvalues of semi-discrete advection and diffusion operators, so the stable pairings of a spatial scheme and a time integrator can be read off directly. |
| [TVD Limiters for Linear Advection](scripts/algorithms/tvd_limiters_advection/) | This script advects a Gaussian, a square wave and a triangle once around a periodic domain with first-order upwind, Lax–Wendroff and flux-limited TVD schemes, and shows the trade-off that Godunov's theorem forces on linear schemes. |
| [Von Neumann Amplification Factors](scripts/algorithms/von_neumann_amplification/) | This script computes the von Neumann amplification factor $G(\theta)$ of the classic finite-difference schemes for linear advection and diffusion and checks the predictions by marching a square wave with each scheme. |

### Plots

| Script | Description |
| --- | --- |
| [Aircraft Design Constraint Diagram](scripts/plots/aircraft_design_constraint_diagram/) | This script draws the constraint diagram of conceptual aircraft design, the thrust-to-weight ratio each performance requirement demands as a function of wing loading, and picks the design point with the lowest thrust inside the feasible region. |
| [Airfoil Angle of Attack](scripts/plots/airfoil_angle_attack/) | This script draws a NACA 2412 airfoil pitched nose-up about its leading edge to several angles of attack, $0^\circ$, $8^\circ$ and $16^\circ$ by default, relative to a free stream flowing left to right. |
| [NACA 4-Digit Airfoil Profile](scripts/plots/airfoil_profile/) | This script draws an annotated NACA 4-digit airfoil profile (NACA 4412 by default) from its four-digit designation, marking the chord line, the mean camber line, the maximum camber and thickness and the leading-edge radius, and compares it with sections of different camber and thickness. |
| [Forces on an Aircraft in a Steady Climb](scripts/plots/airplane_four_forces/) | This script draws the free-body diagram of a 1100 kg light aircraft in a steady climb, with lift, drag, weight and thrust computed from the equilibrium conditions and drawn to scale, and checks that the four forces close into a polygon. |
| [Reynolds Numbers of Flyers](scripts/plots/airplane_reynolds_number_scale/) | This script computes the chord Reynolds number $Re_c = Vc/\nu$ of fourteen flyers, from a fruit fly to an airliner at cruise, and draws them on one logarithmic axis next to the flat-plate skin-friction laws for laminar, turbulent and transitional boundary layers. |
| [Static and Dynamic Stability Classification](scripts/plots/airplane_stability_classification/) | This script draws the static picture of stability (a ball in a bowl, on a hill and on a flat surface) and the five free responses of a second-order system, from non-oscillatory convergence to monotonic divergence, together with their eigenvalues in the complex plane. |
| [Archimedes' Principle Visualisation](scripts/plots/archimedes_principle/) | This script draws a block in a tank of fluid with its weight and buoyant force shown as arrows, and states whether the block floats or sinks according to Archimedes' principle. |
| [Column Buckling Curves](scripts/plots/beams_buckling_curves/) | This script plots the Euler, Johnson, AISC and secant-formula column curves for a structural steel, computes the buckled modes and effective-length factors of four end conditions with a finite-element eigenvalue analysis, and fits a Southwell plot to synthetic test readings. |
| [Failure Envelopes in the Principal-Stress Plane](scripts/plots/beams_failure_envelopes/) | This script draws the Tresca, von Mises, maximum-normal-stress and Coulomb–Mohr envelopes in the plane-stress principal-stress plane and computes the safety factor of example load points under each criterion. |
| [Bias-Variance Trade-off](scripts/plots/bias_variance_tradeoff/) | Polynomial fits of increasing degree to 20 noisy samples show underfitting, overfitting, a U-shaped validation curve and the Monte Carlo split of the error into bias², variance and noise. |
| [Generating Synthetic Data for Boundary Layer Simulation](scripts/plots/boundary_layer_problem/) | This script generates noisy synthetic velocity samples across a boundary layer from a simple square-root profile, saves them to a CSV file and plots them against the wall-normal distance. |
| [Turbulent Boundary Layer Velocity Profile](scripts/plots/boundary_layer_velocity_profile/) | This script plots the one-seventh power-law velocity profile of a turbulent boundary layer in normalised form, $u/U_\infty$ against $y/\delta$. |
| [Checkerboard Pressure on a Collocated Grid](scripts/plots/checkerboard_pressure/) | This script shows why a collocated finite-volume grid with linearly interpolated face pressures cannot see a checkerboard pressure field: the cell pressure gradient and the pressure equation built from it both vanish for $p_i = (-1)^i$. |
| [Grid Convergence Comparison](scripts/plots/comparing_grid_convergence/) | This script illustrates grid convergence by plotting the model numerical solutions $u_N(x) = e^{-x(1 + x/N)}$ for $N = 4, 8, 16$ against the exact solution $u(x) = e^{-x}$ on $[0, 1]$. |
| [Compressible vs. Incompressible Duct Flow](scripts/plots/compressible_vs_incompressible/) | This script draws prescribed incompressible and compressible velocity fields in a 2D duct side by side, so the constant downstream profile of the first can be compared with the accelerating profile of the second. |
| [Continuous vs Discrete Domain](scripts/plots/continuous_vs_discrete_domain/) | This script illustrates the central step of CFD, replacing a field defined at every point of a continuous domain by values stored at a finite set of grid points, and measures the error this introduces for the model problem $du/dx + u = 0$, $u(0) = 1$. |
| [Control Loop Block Diagram](scripts/plots/control_block_diagram/) | This script draws the standard single-loop feedback structure with reference, controller, actuator, input disturbance, plant, sensor and measurement noise, and names the matching parts of a car cruise control. |
| [Control-Volume Stencil](scripts/plots/control_volume_stencil/) | This script draws the notation of the finite volume method: a 1D cell-centred grid with nodes W, P, E and faces w, e, and two unstructured 2D cells with the face area vector, the vector between the cell centroids and the split of the face area vector used to correct the diffusion flux on non-orthogonal meshes. |
| [Cross-Design Generalization](scripts/plots/cross_design_generalization/) | This script is a synthetic illustration of why a surrogate trained on one design family can fail on another: three ridge-regression models trained on family X, family Y and both are tested on held-out designs of each family. |
| [Design Space Distribution via Sobol Sequences](scripts/plots/design_space_distribution/) | This script draws a four-dimensional scrambled Sobol design of 512 geometry variants and shows all of its 2D projections and 1D marginals in a scatter matrix, with the discrepancy of each projection compared against a random design of the same size. |
| [Drag Coefficient Prediction](scripts/plots/drag_coefficient_prediction/) | This script compares two synthetic drag-coefficient surrogates with held-out CFD values in a parity plot and an error plot, and shows that a high $R^2$ can hide errors of ten drag counts. |
| [Path, Polar and Rotating-Frame Coordinates](scripts/plots/dynamics_path_coordinates/) | This script draws the acceleration of three moving particles resolved in the coordinate system that suits each of them: normal–tangential components along a projectile path, radial–transverse components for a bead on a rotating rod, and Coriolis and centrifugal terms for a puck seen from a rotating turntable. |
| [Eigenvector Projection of Velocity Fluctuations](scripts/plots/eigenvector_projection/) | This script finds the principal directions of correlated 2D velocity fluctuations from the eigenvectors of their covariance matrix and projects the data onto them. |
| [Eulerian and Lagrangian Flow Descriptions](scripts/plots/eulerian_lagrangian_flows/) | This script contrasts the Eulerian and Lagrangian descriptions of fluid motion using the time-dependent Double Gyre flow. |
| [Fatigue: S–N Curve, Haigh Diagram and Miner's Rule](scripts/plots/fatigue_sn_and_goodman/) | This script builds the S–N curve of a machined steel shaft from Marin factors, draws the Goodman, Gerber and Soderberg lines with an operating point, and sums the Miner damage of a rainflow-counted random stress history. |
| [Flow Rate Through a Circular Pipe](scripts/plots/flow_rate_pipe/) | This script computes the volumetric flow rate $Q = \pi r^2 v$ of a circular pipe and draws a labelled side view of the pipe with flow arrows. |
| [Flow Regime Clustering with POD and k-means](scripts/plots/flow_regime_clustering/) | This script groups the snapshots of a synthetic wake that switches between three flow regimes into clusters, by projecting them onto their leading POD modes and running k-means on the POD coefficients. |
| [Flow Separation in a Boundary Layer](scripts/plots/flow_separation_boundary_layer/) | This script draws a schematic of boundary-layer separation: an attached layer that thickens downstream, a separation point, and a recirculation region under the separated shear layer. |
| [Pierson–Moskowitz and JONSWAP Wave Spectra](scripts/plots/fluid_loading_wave_spectra/) | This script plots the Pierson–Moskowitz and JONSWAP spectra of an irregular sea with the same significant wave height and peak period, and synthesises a random-phase time series of the surface elevation from the JONSWAP spectrum. |
| [Wind Profiles and Velocity Pressure over Four Terrains](scripts/plots/fluid_loading_wind_profile/) | This script plots log-law mean wind profiles over open sea, open country, suburbs and a city centre, the power-law exponent that best fits each profile, and the resulting mean and peak velocity pressure with height. |
| [Froude Number vs. Flow Velocity](scripts/plots/froude_number/) | This script plots the length-based Froude number $Fr = U/\sqrt{gL}$ against speed for hulls of 5, 10, 15, and 20 m, with reference lines at hull speed and at the approximate start of planing. |
| [Coordinate Rotation of a Force Vector](scripts/plots/fundamentals_coordinate_rotation/) | This script transforms the components of a force from one Cartesian frame to a rotated one with a rotation matrix and shows that the components depend on the frame while the vector does not. |
| [Coplanar Force Resultant](scripts/plots/fundamentals_force_resultant/) | This script reduces a coplanar system of forces and a couple acting on a plate to an equivalent force–couple system at a point and then to a single resultant force on its line of action. |
| [Free-Body Diagram of a Beam](scripts/plots/fundamentals_free_body_diagram/) | This script turns a loaded, supported beam into its free-body diagram and solves the three planar equilibrium equations for the support reactions. |
| [Support Reactions in 2D](scripts/plots/fundamentals_support_reactions/) | This script draws the standard planar supports and connections next to the reactions they exert on a body, as a reference chart for drawing free-body diagrams. |
| [Involute Gear Geometry](scripts/plots/gears_involute_profile/) | This script draws the involute construction, a standard 20° spur pinion and gear in mesh with their line of action and path of contact, and the smallest pinion that can mesh without interference as a function of gear ratio. |
| [GNN Message Passing on a Cylinder Mesh](scripts/plots/gnn_message_passing/) | This script shows how far information travels through a graph neural network on an unstructured CFD mesh, and that a linear message-passing layer with the right weights is a finite-volume diffusion scheme. |
| [Pump and System Curves](scripts/plots/hydraulics_pump_system_curve/) | This script plots the head–flow curves of a centrifugal pump at four speeds from the affinity laws, the curve of the pipe system it feeds, and the operating points where they meet. |
| [Laminar vs. Turbulent Boundary Layer Profiles](scripts/plots/laminar_vs_turbulent_boundary_layer/) | This script plots normalised laminar and turbulent boundary-layer velocity profiles on the same axes to show how much fuller the turbulent profile is. |
| [Laminar vs Turbulent Pipe Flow](scripts/plots/laminar_vs_turbulent_pipe/) | This script plots laminar and turbulent radial velocity profiles of pipe flow in side-by-side panels to show how much flatter the turbulent profile is. |
| [Lattice Velocity Sets](scripts/plots/lattice_velocity_sets/) | This script draws the D2Q9 and D3Q19 velocity sets with their indices and weights, the streaming step on a small lattice, and half-way bounce-back at a wall. |
| [Longitudinal Velocity Fluctuations and Projections](scripts/plots/longitudinal_velocity_fluctuations_and_projections/) | This script plots synthetic two-point velocity fluctuations as time traces, as a scatter cloud, and projected onto a unit vector, which are the first steps of the two-point POD example. |
| [Kirsch Stress Field Around a Hole](scripts/plots/materials_kirsch_hole/) | This script plots the closed-form Kirsch stress field around a circular hole in a plate under uniaxial tension and shows the stress concentration factor of 3 at the hole edge. |
| [Stress-Strain Curves](scripts/plots/materials_stress_strain_curves/) | This script draws model engineering and true stress–strain curves of a ductile and a brittle material. |
| [Torsional Shear Stress Distribution](scripts/plots/materials_torsion_shear_distribution/) | This script plots torsional shear stress in solid, hollow, rectangular and thin-walled closed sections. |
| [Mean Pressure Coefficient Along Vehicle Centreline](scripts/plots/mean_pressure_coefficient/) | This script plots a mock validation figure of mean pressure coefficient $C_P$ against streamwise position, comparing "experimental" data with a "CFD SRS" (scale-resolving simulation) curve that under-predicts a separation plateau. |
| [Mean Velocity Magnitude: Experiment vs CFD Comparison](scripts/plots/mean_velocity_magnitude/) | This script plots a mock experimental profile and a mock CFD scale-resolving simulation (SRS) profile of the normalised mean velocity magnitude $\|U\|/U_0$ along an under-body centreline. |
| [Meniscus Behavior](scripts/plots/meniscus_behavior/) | This script sketches the meniscus of water and of mercury in a glass tube, showing how wetting determines whether the free surface curves up or down at the wall. |
| [Microscopic vs. Macroscopic View of a Fluid](scripts/plots/microscopic_view/) | This script draws two side-by-side panels that contrast the microscopic (molecular) and macroscopic (continuum) views of a fluid. |
| [ML-CFD Surrogate Workflow](scripts/plots/ml_cfd_workflow/) | This script draws a schematic of the workflow for building a machine-learning surrogate of CFD results, from the design of experiments to deployment in an optimisation loop. |
| [Learning Paradigms on Flow Data](scripts/plots/ml_learning_paradigms/) | Three panels contrast supervised regression, supervised classification and unsupervised clustering on synthetic flow data, each computed in numpy. |
| [Converging-Diverging Nozzle Flow](scripts/plots/nozzle_flow/) | This script plots quasi-one-dimensional isentropic flow through a converging-diverging (de Laval) nozzle, with streamlines coloured by Mach number. |
| [Numerical vs. Exact Solution Comparison](scripts/plots/numerical_vs_exact_solution/) | This script solves $du/dx + u = 0$ with $u(0) = 1$ by a first-order finite-difference scheme and compares the result with the exact solution $u(x) = e^{-x}$, plotting the pointwise error. |
| [POD Analysis for Flow Fields](scripts/plots/pod_analysis_for_flow_fields/) | This script performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode. |
| [POD Energy and Truncation](scripts/plots/pod_energy_and_truncation/) | This script computes the POD of a synthetic cylinder-wake velocity field on a stretched mesh and shows how the number of retained modes $r$ follows from the eigenvalue spectrum, with the 90% and 99% energy thresholds and reconstructions of one snapshot with $r = 1, 2, 5$ and $10$ modes. |
| [POD Modes of a Two-Point Velocity Signal](scripts/plots/pod_modes_2d/) | This script applies Proper Orthogonal Decomposition to velocity signals measured at two points, a and b, and plots how much each of the two POD modes contributes to each signal. |
| [POD Spatial Modes and Temporal Coefficients](scripts/plots/pod_modes_and_temporal_coefficients/) | This script extracts the first three POD spatial modes and their temporal coefficients from a synthetic two-dimensional, time-dependent field and plots them. |
| [Pressure Difference Across a Spherical Droplet](scripts/plots/pressure_difference_across_spherical_droplet/) | This script draws an annotated schematic of the Young-Laplace pressure jump across the surface of a spherical droplet. |
| [Pressure Variation with Depth](scripts/plots/pressure_variation_with_depth/) | This script plots how hydrostatic pressure increases linearly with depth below the free surface of a fluid at rest. |
| [Maxwell-Boltzmann Speed Distribution of N₂ Molecules](scripts/plots/probability_distribution_function_of_nitrogen_molecules/) | This script plots the Maxwell-Boltzmann speed distribution of nitrogen (N₂) molecules at 300 K, 600 K, 900 K and 1200 K, and marks the most probable, mean and root-mean-square speed on each curve. |
| [RBF Shape Parameter Trade-Off](scripts/plots/rbf_shape_parameter_tradeoff/) | This script sweeps the shape parameter $\varepsilon$ of Gaussian and multiquadric radial basis function interpolants of Franke's 2D test function and plots the true error, Rippa's leave-one-out cross-validation (LOOCV) estimate of it, and the condition number of the interpolation matrix. |
| [Kolmogorov n-Width of Diffusing and Translating Solutions](scripts/plots/rom_n_width_decay/) | This script compares how fast linear subspaces can approximate three parametrized solution families, a diffusing pulse, a translating pulse and a translating step, by plotting the singular values of their snapshot matrices and the worst-case error of projecting the samples onto the best $N$-dimensional subspace. |
| [Sampling Strategies Comparison](scripts/plots/sampling_strategies_comparison/) | This script compares random, Latin hypercube and scrambled Sobol designs of the same size in a 2D design space, showing their point layouts, their 1D marginal histograms and how their centred $L_2$ discrepancy falls with the number of samples. |
| [Ship Hull in Water](scripts/plots/ship_hull_in_water/) | This script draws a side-view sketch of a ship hull sitting in a sinusoidal free-surface wave and annotates it with the Froude number $Fr = U/\sqrt{gL}$. |
| [Cable Force Polygon](scripts/plots/statics_cable_force_polygon/) | This script solves the tensions of a mass held by two cables, draws its free-body diagram and closed force polygon to scale, and plots how the tension of a sagging cable grows as the sag angle shrinks. |
| [Composite Centroid](scripts/plots/statics_composite_centroid/) | This script computes the centroids of a T-section and of a plate with a hole and a notch from a table of parts, checks them against the polygon formula for the exact boundary, and gives the centroidal second moment of the T-section. |
| [Friction Curves](scripts/plots/statics_friction_curves/) | This script plots the friction force on a block as the push grows through impending motion to sliding, the capstan ratio $e^{\mu\beta}$ against wrap angle, and the efficiency of a square-threaded screw against lead angle with its self-locking range. |
| [Support Reactions and Constraint](scripts/plots/statics_support_reactions/) | This script solves the reactions of a simply supported beam from the $3 \times 3$ equilibrium system and classifies support layouts as determinate, indeterminate or improper from the rank of the reaction matrix. |
| [Virtual Work and Stability](scripts/plots/statics_virtual_work_stability/) | This script plots the potential energy of a spring-loaded two-bar linkage for several loads with its stable and unstable equilibria, and its equilibrium path from the virtual-work equation with the snap-through limit point. |
| [Surrogate Input Representations](scripts/plots/surrogate_input_representations/) | This script draws one NACA 2412 airfoil in the four forms a neural-network surrogate can take as input: a parameter vector, a signed distance field on a Cartesian grid, a surface point cloud, and a mesh graph. |
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
| [Decaying 2D Turbulence](scripts/simulations/decaying_2d_turbulence/) | This script simulates freely decaying two-dimensional turbulence in a doubly periodic box and animates how a random vorticity field organises itself into coherent vortices that merge into ever larger ones. |
| [Double Gyre Chaotic Mixing](scripts/simulations/double_gyre_chaotic_mixing/) | This script advects 720 000 passive dye tracers through the time-periodic double gyre and animates how the flow stretches and folds them into ever finer filaments. |
| [Eulerian Cylinder Flow](scripts/simulations/eulerian_cylinder_flow/) | This script simulates 2D incompressible, inviscid flow past a circular cylinder on a fixed Eulerian grid and animates a dye tracer with Matplotlib. |
| [Gray-Scott Reaction-Diffusion Simulation](scripts/simulations/gray_scott_reaction_diffusion/) | This script simulates the Gray-Scott reaction-diffusion system, in which two chemicals that react and diffuse on a periodic square turn a small seeded square into self-replicating spots or branching coral, and animates the concentration of one of them with Matplotlib. |
| [Ising Model Simulation](scripts/simulations/ising_model/) | This script simulates the two-dimensional Ising model with the Metropolis Monte Carlo algorithm and animates the spin lattice together with its magnetization and energy. |
| [Kelvin-Helmholtz Instability Simulation](scripts/simulations/kelvin_helmholtz_instability/) | This script simulates the Kelvin-Helmholtz instability, the rolling-up of a shear layer between fluid streams moving in opposite directions, in a periodic 2D incompressible flow animated with Matplotlib. |
| [Laplace Equation Maze Solver](scripts/simulations/laplace_equation_maze_solver/) | This script solves a randomly generated maze by computing a potential that satisfies Laplace's equation in the maze passages and then following the potential uphill from the entrance to the exit. |
| [Lattice Boltzmann Cylinder Flow Simulation](scripts/simulations/lattice_boltzmann_cylinder_flow/) | This script simulates 2D flow past a circular cylinder with the lattice Boltzmann method (D2Q9 lattice, BGK collision operator) and animates the velocity magnitude and the vorticity with Matplotlib. |
| [Lid-Driven Cavity Flow Simulation](scripts/simulations/lid_driven_cavity/) | This script solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field. |
| [Lorenz Attractor Simulation](scripts/simulations/lorenz_attractor/) | This script integrates the Lorenz equations, a three-mode model of convection in a fluid layer heated from below, for 60 trajectories that start within $10^{-5}$ of one another and animates how they fan out over the butterfly-shaped attractor. |
| [Mach Cone of a Moving Sound Source](scripts/simulations/mach_cone_moving_source/) | This script simulates the sound of a small source that accelerates from rest to twice the speed of sound and animates its pressure field, from the Doppler-compressed wavefronts of a subsonic source through the pile-up at Mach 1 to the Mach cone of a supersonic one. |
| [Leapfrogging Vortex Pairs](scripts/simulations/point_vortex_leapfrogging/) | This script simulates two coaxial vortex pairs, four point vortices in all, that leapfrog: the rear pair contracts, speeds up and slips through the front pair, which widens and slows down, and then the two swap roles again and again. |
| [Rayleigh-Bénard Convection Simulation](scripts/simulations/rayleigh_benard_convection/) | This script simulates Rayleigh-Bénard convection, the buoyancy-driven flow in a fluid layer heated from below and cooled from above, and animates the temperature field with Matplotlib. |
| [Rayleigh-Taylor Instability](scripts/simulations/rayleigh_taylor_instability/) | This script simulates the Rayleigh-Taylor instability of heavy fluid resting on light fluid in a tall 2D box and animates how a rippled interface grows into rising bubbles and falling mushroom-shaped spikes. |
| [2D Schrödinger Equation Simulation](scripts/simulations/schroedinger_equation/) | This script solves the time-dependent Schrödinger equation for a free particle in two dimensions with the split-step Fourier method and animates the probability density of the spreading wavepacket as a 3D surface. |
| [Raindrops on a Pond: Shallow-Water Ripples](scripts/simulations/shallow_water_ripples/) | This script simulates raindrops falling on a square basin of still water by solving the 2D shallow-water equations with a conservative finite-volume scheme, and animates the free surface as shaded relief. |
| [Simplified Real-Time Fluid Dynamics Simulator](scripts/simulations/simplified_real_time_fluid_dynamics_simulator/) | This script is an interactive 2D smoke simulation that uses Jos Stam's Stable Fluids algorithm (1999) to approximate the incompressible Navier-Stokes equations fast enough to run in real time in a Matplotlib window. |
| [Sod Shock Tube](scripts/simulations/sod_shock_tube/) | This script animates Sod's shock tube, the standard test of compressible-flow solvers, computed with a first-order Godunov scheme and a second-order MUSCL–Hancock scheme and compared with the exact Riemann solution at every frame. |
| [SPH Dam Break](scripts/simulations/sph_dam_break/) | This script simulates the collapse of a water column in a closed tank, the classic dam-break problem, with weakly compressible smoothed particle hydrodynamics (SPH), and animates the water particles coloured by their speed. |
| [Steady and Unsteady Pathlines Around a Cylinder with Vortex Shedding](scripts/simulations/steady_and_unsteady_pathlines_with_vortex_shedding/) | This script compares streamlines and particle pathlines for steady potential flow past a cylinder with circulation and for an unsteady version of the same flow with a kinematic vortex-shedding model. |
| [Supersonic Forward-Facing Step](scripts/simulations/supersonic_forward_facing_step/) | This script solves the 2D compressible Euler equations for a Mach 3 stream that meets a forward-facing step in a wind tunnel, the benchmark of Woodward and Colella (1984), and animates the shock pattern that forms. |

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
