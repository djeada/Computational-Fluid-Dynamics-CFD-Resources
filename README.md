# Computational Fluid Dynamics (CFD) Resources

![CFD Resources Banner](https://github.com/user-attachments/assets/ac0cec05-abb0-4f8e-ae68-3df6bbb53308)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/djeada/Computational-Fluid-Dynamics-CFD-Resources?style=social)](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

### A structured resource for learning, implementing, and applying computational fluid dynamics

This repository provides a structured collection of notes, examples, scripts, tutorials, and references for Computational Fluid Dynamics (CFD). It is designed for learners and practitioners who want to connect the physical theory of fluid flow with numerical methods, software workflows, simulation practice, and modern data-driven techniques.

[Quick Start](#getting-started) • [Documentation](#content-organization) • [Research](#advanced-research-topics) • [Code](#scripts) • [Contribute](#contributing)

---

## Vision and Scope

This repository is a community-driven resource for Computational Fluid Dynamics (CFD) education, implementation, and applied research. It serves as a structured learning environment, a practical implementation reference, and a curated gateway to important CFD literature, workflows, and tools.

### Purpose and Audience

The repository consolidates theory notes, implementation examples, visualization tools, simulation cases, and external references into a coherent progression. It is designed to support several audiences:

- **Students** beginning their study of fluid mechanics and numerical simulation
- **Researchers** developing, comparing, or validating computational methods
- **Engineers** applying CFD to practical design, analysis, and validation problems
- **Machine learning practitioners** exploring physics-informed and data-driven methods
- **Educators** assembling structured teaching material, examples, and exercises

### Educational Philosophy

CFD is not only a collection of equations and algorithms. It is a synthesis of physics, mathematics, numerical analysis, computer science, and engineering judgment. The repository is organized around the following principles:

1. **Theory-practice integration**: Concepts are connected to mathematical foundations, implementation details, and practical consequences.
2. **Iterative learning**: Material is organized so readers can revisit topics at increasing levels of depth.
3. **Interdisciplinary context**: Connections are made between CFD and adjacent fields such as optimization, machine learning, high-performance computing, and applied mechanics.
4. **Modern relevance**: The content includes current topics such as physics-informed learning, surrogate models, reduced-order modeling, and scalable computation.
5. **Community development**: Contributions are welcome from practitioners, researchers, students, and educators.

---

## Repository Statistics

| Category | Count | Description |
|----------|-------|-------------|
| Theory Documents | 103+ | Comprehensive markdown documents covering all aspects of CFD |
| Python Scripts | 57+ | Ready-to-use implementations and visualizations |
| Simulation Examples | 15+ | Complete simulation setups from basic to advanced |
| Algorithm Implementations | 9+ | Core computational algorithms with detailed explanations |
| Visualization Scripts | 30+ | Professional plotting and analysis tools |
| External References | 80+ | Curated links to papers, books, courses, and tools |
| Topics Covered | 50+ | From fundamentals to specialized advanced topics |

---

## How to Use This Repository

This repository can support several workflows:

- **Self-study curriculum:** Follow one of the learning pathways and work through the recommended notes, scripts, and examples in sequence.
- **Course companion:** Use the notes as reference material and the scripts as demonstrations, assignments, or validation exercises.
- **Engineering reference:** Consult the practice guides, numerical method notes, and troubleshooting sections when setting up or reviewing CFD workflows.
- **Research starting point:** Use the advanced topics, references, and algorithms as entry points into areas such as turbulence modeling, model reduction, optimization, and physics-informed machine learning.

The material is intentionally modular. Readers can begin with fundamentals, move directly into simulations, or focus on specific tools such as Gmsh, ParaView, or Python-based analysis.

## Learning Pathways and Navigation

Use the pathways below to choose a route through the material based on your background and goals. The timelines are approximate and can be adapted for course schedules, self-study, or project-driven learning.

### Path 1: Academic Foundation for Students and Researchers
**Timeline: 6-12 months**| **Prerequisites: Calculus, Linear Algebra, Basic Programming**

```
Week 1-4:   Fluid Mechanics Fundamentals → Conservation Laws → Dimensional Analysis
Week 5-8:   Navier-Stokes Equations → Boundary Conditions → Analytical Solutions
Week 9-12:  Finite Difference Methods → Stability Analysis → Basic 1D Problems
Week 13-16: Finite Volume Methods → 2D Simulations → Turbulence Introduction
Week 17-20: Advanced Discretization → Complex Geometries → Mesh Generation
Week 21-24: Turbulence Modeling → RANS/LES → Practical Applications
Beyond:     Specialized Topics → Research Problems → Novel Methods
```

### Path 2: Industrial Practitioner
**Timeline: 3-6 months**| **Prerequisites: Engineering Background, CFD Software Experience**

```
Week 1-2:   Quick Theory Refresh → Key Dimensionless Numbers → Common Pitfalls
Week 3-4:   Meshing Best Practices → Boundary Condition Selection → Solver Settings
Week 5-6:   Turbulence Model Selection → Wall Functions → Y+ Calculations
Week 7-8:   Convergence Strategies → Result Validation → Post-Processing
Week 9-10:  Industry-Specific Applications → Case Studies → Optimization
Week 11-12: Advanced Topics → Custom Functions → Automation Workflows
```

### Path 3: Machine Learning and AI Integration
**Timeline: 4-8 months**| **Prerequisites: Machine Learning, Python, CFD Basics**

```
Week 1-3:   CFD Fundamentals for ML → Data Generation → Feature Engineering
Week 4-6:   Physics-Informed Neural Networks (PINNs) → Implementation → Training
Week 7-9:   Surrogate Modeling → ROM Techniques → POD/DMD Methods
Week 10-12: ML-Enhanced Turbulence → RANS Closures → LES Subgrid Models
Week 13-16: Shape Optimization → Generative Design → Topology Optimization
Beyond:     Research Frontiers → Novel Architectures → Industry Applications
```

### Path 4: Quick Start
**Timeline: 4-8 weeks**| **Prerequisites: Basic Physics, Programming Interest**

```
Week 1: What is CFD? → Simple Examples → Visualization Introduction
Week 2: Basic Equations → Flow Patterns → Hands-on Simulations
Week 3: Software Tools → ParaView/Gmsh → Running Your First Simulation
Week 4: Practical Problems → Learning Resources → Next Steps
```

---

## Advanced Research Topics

### Current Developments in CFD

The repository includes material on advanced and emerging topics that are increasingly relevant in research and industrial practice:

#### Artificial Intelligence and Machine Learning
- **Physics-Informed Neural Networks (PINNs)**: Embedding physical laws directly into neural network architectures for solving PDEs
- **Deep Learning for Turbulence**: Using CNNs and GANs to model subgrid-scale turbulence in LES
- **Reinforcement Learning**: Adaptive flow control and optimization strategies
- **Graph Neural Networks**: For unstructured mesh processing and solution prediction
- **Operator Learning**: Neural operators (DeepONet, FNO) for learning solution operators
- **Generative Models**: VAEs and GANs for design space exploration and flow field generation

#### High-Performance Computing
- **GPU Acceleration**: CUDA-based CFD solvers and acceleration techniques
- **Parallel Computing**: MPI, OpenMP, and hybrid parallelization strategies
- **Cloud Computing**: Scalable CFD workflows on AWS, Azure, and GCP
- **Quantum Computing**: Exploratory quantum algorithms for fluid dynamics
- **Exascale Computing**: Preparing for next-generation supercomputers

#### Numerical Methods
- **Meshless Methods**: SPH, meshless Galerkin, and particle-based approaches
- **High-Order Methods**: Spectral methods, DG, and HDG for accuracy
- **Adaptive Methods**: hp-refinement, AMR, and error-driven adaptation
- **Multiscale Methods**: HMM, heterogeneous multiscale methods
- **Immersed Boundary Methods**: For complex moving geometries
- **Cut-Cell Methods**: Cartesian grid methods for complex boundaries

#### Specialized Flow Phenomena
- **Multiphase Flows**: VOF, Level Set, Phase Field methods
- **Reacting Flows**: Combustion modeling, chemical kinetics coupling
- **Fluid-Structure Interaction**: Two-way coupling, aeroelasticity
- **Microfluidics**: Low Reynolds number phenomena, electrokinetics
- **Rarefied Gas Dynamics**: DSMC, kinetic theory approaches
- **Non-Newtonian Fluids**: Viscoelastic, thixotropic, and complex rheology

#### Data-Driven Approaches
- **Model Order Reduction**: POD, DMD, balanced truncation
- **Sparse Identification**: SINDy for discovering governing equations
- **Bayesian Methods**: Uncertainty quantification and inverse problems
- **Transfer Learning**: Domain adaptation for CFD applications
- **Active Learning**: Intelligent sampling for expensive simulations

---

## Contributing

Contributions are welcome from researchers, engineers, educators, and students. High-quality additions should improve accuracy, clarity, reproducibility, or coverage.

### How to Contribute

1. **Fork** this repository
2. **Create** a feature branch (`git checkout -b feature/YourContribution`)
3. **Make** your changes with clear, descriptive commits
4. **Test** your additions and ensure documentation is updated
5. **Push** to your fork (`git push origin feature/YourContribution`)
6. **Open** a Pull Request with detailed description

### Contribution Guidelines

- **Documentation**: Use clear, technical language with proper mathematical notation (LaTeX where appropriate)
- **Code**: Include comments, validation examples, and performance considerations
- **Formatting**: Follow existing structure and markdown conventions
- **References**: Cite sources and provide links to supporting material
- **Quality**: Ensure accuracy through peer review and testing
- **Accessibility**: Write for international audiences, avoid jargon without explanation

### Types of Contributions Welcome

| Category | Examples | Impact Level |
|----------|----------|--------------|
| **Bug Fixes** | Equation corrections, code errors, broken links | Critical |
| **Content** | New tutorials, expanded explanations, case studies | High |
| **Code** | New algorithms, optimizations, implementations | High |
| **Examples** | Practical demonstrations, validation cases | Medium |
| **Tools** | Scripts, integrations, workflow improvements | Medium |
| **Translations** | Multilingual content, accessibility | Medium |
| **Visualizations** | Plots, diagrams, animations | Medium |
| **References** | New papers, books, courses, resources | Low |

### Quality Standards

Contributions should be technically correct, reproducible, and useful to readers with different backgrounds. When adding new material, include enough context to explain why the topic matters, what assumptions are being made, how the method is implemented, and how the result can be checked. For code contributions, prefer clear structure, documented inputs and outputs, reproducible examples, and validation against analytical solutions, benchmark cases, or trusted references where possible.

### Recognition and Credits

All contributors are acknowledged in our [Contributors](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/graphs/contributors) page. Significant contributions may be highlighted in release notes and documentation.

---

## Content Organization

The repository is organized into notes, practice material, scripts, simulations, and external references. Each section supports a different mode of learning: conceptual study, hands-on implementation, software workflow development, or further reading.

### [Notes](./notes/)
**Theoretical foundations** — More than 103 documents covering CFD theory, applied fluid mechanics, numerical methods, and related computational approaches.

#### [Fluid Mechanics](./notes/fluid_mechanics/)
**Coverage across more than 15 major topic areas**

<details>
<summary><b>Fluid mechanics topics</b></summary>

##### **[Fundamentals](./notes/fluid_mechanics/intro.md)**
- **Continuum Hypothesis**: When and why we treat fluids as continuous media
- **Conservation Principles**: Mass, momentum, and energy in fluid systems
- **Mathematical Framework**: Vector calculus, tensors, and field theory
- **Material vs. Spatial Description**: Lagrangian and Eulerian perspectives
- **Control Volume Analysis**: Integral and differential forms

##### **[Governing Equations](./notes/fluid_mechanics/governing_equations/)**
- **Navier-Stokes Equations**: Complete derivation from first principles
- **Continuity Equation**: Mass conservation in differential form
- **Momentum Equations**: Newton's second law for fluids
- **Energy Equation**: First law of thermodynamics for moving fluids
- **Constitutive Relations**: Stress-strain relationships for various fluids
- **Simplified Forms**: Euler equations, Stokes flow, potential flow

##### **[Dimensional Analysis](./notes/fluid_mechanics/dimensions.md)**
- **Buckingham Pi Theorem**: Systematic approach to dimensionless groups
- **Dimensionless Numbers**: Reynolds, Mach, Froude, Prandtl, and dozens more
- **Similarity Theory**: Physical and mathematical similarity
- **Scaling Laws**: From laboratory to full-scale applications
- **Model Testing**: Wind tunnel and water channel experiments

##### **[Fluid Properties](./notes/fluid_mechanics/fluid_properties/)**
- **Viscosity**: Dynamic and kinematic, temperature dependence
- **Surface Tension**: Capillary effects, wetting phenomena
- **Compressibility**: Equation of state, speed of sound
- **Thermal Properties**: Conductivity, specific heat, expansion
- **Non-Newtonian Behavior**: Shear-thinning, shear-thickening, viscoelasticity

##### **[Fluid Statics](./notes/fluid_mechanics/fluid_statics/)**
- **Hydrostatic Pressure**: Pressure variation in static fluids
- **Buoyancy**: Archimedes' principle and applications
- **Stability**: Floating bodies, metacentric height
- **Pressure Measurement**: Manometers and pressure gauges
- **Surfaces Under Pressure**: Forces on submerged surfaces

##### **[Flow Kinematics](./notes/fluid_mechanics/flow_kinematics/)**
- **Velocity Fields**: Eulerian vs. Lagrangian descriptions
- **Streamlines, Pathlines, Streaklines**: Flow visualization concepts
- **Vorticity and Circulation**: Rotational aspects of flow
- **Deformation Tensor**: Strain rate and rotation rate
- **Reynolds Transport Theorem**: Moving control volumes

##### **[Inviscid Flow](./notes/fluid_mechanics/inviscid_flow/)**
- **Potential Flow Theory**: Velocity potential and stream function
- **Elementary Solutions**: Uniform flow, sources, sinks, doublets, vortices
- **Superposition**: Building complex flows from simple solutions
- **Bernoulli's Equation**: Energy conservation in inviscid flows
- **Airfoil Theory**: Thin airfoil theory, Kutta condition
- **Complex Analysis**: Conformal mapping for 2D flows

##### **[Viscous Flow](./notes/fluid_mechanics/viscous_flow/)**
- **Boundary Layer Theory**: Prandtl's revolutionary concept
- **Laminar Boundary Layers**: Blasius solution, Falkner-Skan flows
- **Boundary Layer Separation**: Adverse pressure gradients
- **Drag Analysis**: Friction drag, pressure drag, form drag
- **Exact Solutions**: Couette flow, Poiseuille flow, Stokes flow
- **Internal Flows**: Fully developed pipe and channel flows

##### **[Compressible Flow](./notes/fluid_mechanics/compressible_flow/)**
- **Gas Dynamics**: Thermodynamics of high-speed flows
- **Shock Waves**: Normal shocks, oblique shocks, expansion waves
- **Isentropic Flow**: Nozzles and diffusers
- **Fanno Flow**: Adiabatic flow with friction
- **Rayleigh Flow**: Frictionless flow with heat transfer
- **Supersonic Aerodynamics**: Mach cones, wave drag

##### **[Turbulence Theory](./notes/fluid_mechanics/turbulence/)**
- **Nature of Turbulence**: Characteristics and causes
- **Reynolds Decomposition**: Mean and fluctuating components
- **Turbulent Kinetic Energy**: Production, transport, dissipation
- **Energy Cascade**: Richardson's concept, Kolmogorov theory
- **Statistical Description**: Correlations, spectra, structure functions
- **Modeling Approaches**: RANS, LES, DNS - when to use each

##### **[Internal Flow](./notes/fluid_mechanics/internal_flow/)**
- **Pipe Flow**: Friction factors, Moody diagram
- **Network Analysis**: Multiple pipes, junctions
- **Minor Losses**: Bends, valves, fittings
- **Pumps and Fans**: Performance curves, system curves
- **Ventilation**: HVAC applications

##### **[Specialized Topics](./notes/fluid_mechanics/specialized_topics/)**
- **Fluid-Structure Interaction**: Vortex-induced vibration, flutter
- **Multiphase Flows**: Gas-liquid, liquid-solid interactions
- **Microfluidics**: Lab-on-a-chip, electrokinetics
- **Geophysical Flows**: Atmospheric and oceanic circulation
- **Biological Flows**: Blood flow, respiratory systems
- **Environmental Flows**: Pollution dispersion, river hydraulics

</details>

#### [Applied Mechanics](./notes/applied_mechanics/)
**Engineering applications and design methodologies**

<details>
<summary><b>Engineering discipline integration</b></summary>

- **Control Systems**: Feedback loops for flow control, active flow management
- **Dynamics**: Vibration analysis, modal testing, dynamic response
- **Fluid Loading**: Pressure distributions, force calculations, moment analysis
- **Mechanical Systems**: Component design, optimization, failure analysis
- **Statics**: Equilibrium, free body diagrams, stress analysis
- **Strength of Materials**: Material selection, fatigue, fracture mechanics
- **Transportation**: Vehicle aerodynamics, marine hydrodynamics, railway applications

</details>

#### [Machine Learning](./notes/machine_learning/)
**Data-driven and physics-informed approaches to fluid mechanics**

<details>
<summary><b>AI and machine learning integration in CFD</b></summary>

- **Physics-Informed Neural Networks (PINNs)**: Embedding PDEs in loss functions
- **Neural Network Architectures**: CNNs for spatial data, RNNs for temporal sequences
- **Flow Pattern Recognition**: Unsupervised learning for turbulent structures
- **Geometry Optimization**: AI-driven shape optimization and generative design
- **Reduced Order Modeling**: Autoencoders, variational autoencoders
- **Automotive Aerodynamics**: ML for drag reduction and downforce optimization
- **Surrogate Modeling**: Fast approximations of expensive simulations
- **Active Learning**: Intelligent sampling strategies for parameter spaces

</details>

#### [Numerical Methods](./notes/numerical/)
**Computational methods and algorithm implementation**

<details>
<summary><b>Numerical methods coverage</b></summary>

##### **[CFD Methods Overview](./notes/numerical/cfd/)**
Comparative analysis of major discretization approaches, when to use each method, advantages and limitations

##### **[Finite Difference Methods (FDM)](./notes/numerical/fdm/)**
- Grid generation and stencil operations
- Central, forward, backward differences
- Accuracy and stability analysis
- Explicit vs. implicit schemes
- Applications to simple geometries

##### **[Finite Element Methods (FEM)](./notes/numerical/fem/)**
- Variational formulations and weak forms
- Element types and shape functions
- Assembly of global matrices
- Galerkin and Petrov-Galerkin methods
- Applications to complex geometries

##### **[Finite Volume Methods (FVM)](./notes/numerical/fvm/)**
- Conservation-based discretization
- Flux calculation and reconstruction
- SIMPLE, SIMPLER, PISO algorithms
- Pressure-velocity coupling
- Industry-standard approach in CFD

##### **[Lattice Boltzmann Methods (LBM)](./notes/numerical/lattice_boltzmann/)**
- Kinetic theory foundations
- Collision and streaming steps
- Boundary conditions in LBM
- Advantages for complex geometries
- Parallel implementation

##### **[Proper Orthogonal Decomposition (POD)](./notes/numerical/pod/)**
- SVD-based mode extraction
- Energy-optimal basis functions
- Modal decomposition of flow fields
- Reduced order model construction

##### **[Reduced Order Models (ROM)](./notes/numerical/rom/)**
- Galerkin projection methods
- POD-Galerkin approach
- Dynamic mode decomposition (DMD)
- Real-time simulation capabilities

##### **[Surrogate Models](./notes/numerical/surrogates/)**
- Gaussian processes and kriging
- Radial basis functions
- Response surface methodologies
- Uncertainty quantification

</details>

---

### [Practice](./practice/)
**Tutorials, software guides, and implementation examples**

The practice section connects theory to implementation through tutorials for standard CFD and scientific computing tools.

#### [Gmsh: Mesh Generation](./practice/gmsh/)

<details>
<summary><b>Computational meshing topics</b></summary>

- **[Introduction to Gmsh](./practice/gmsh/intro.md)**: Installation, interface overview, basic concepts
- **[Volume Mesh Generation](./practice/gmsh/generate_volume_mesh.md)**: Tetrahedral, hexahedral, hybrid meshes
- **Mesh Quality Metrics**: Skewness, aspect ratio, orthogonality
- **Advanced Techniques**: Boundary layers, refinement regions, anisotropic meshing
- **Scripting**: Automating mesh generation with .geo files
- **Integration**: Exporting meshes for OpenFOAM, Fluent, SU2

</details>

#### [ParaView: Scientific Visualization](./practice/paraview/)

<details>
<summary><b>Post-processing topics</b></summary>

- **[ParaView Introduction](./practice/paraview/intro.md)**: Interface navigation, basic operations
- **[External Package Integration](./practice/paraview/import_external_packages.md)**: Custom filters and plugins
- **Advanced Visualization**: Streamlines, isosurfaces, volume rendering
- **Quantitative Analysis**: Line plots, histogram, statistical tools
- **Animation**: Time-series visualization, camera paths
- **Python Scripting**: Automating visualization workflows
- **High-Quality Rendering**: Publication-ready images

</details>

#### [Manual Projects](./practice/manual_projects/)

Detailed end-to-end project implementations, from problem definition to validated results:
- Flow over cylinders with vortex shedding analysis
- Lid-driven cavity benchmark validation
- Airfoil analysis at various angles of attack
- Heat exchanger optimization studies
- Turbulent pipe flow comparisons

#### [OpenFOAM Tutorials](./practice/openfoam/)

Step-by-step guides for the world's most popular open-source CFD software (coming soon)

#### [CFD Tools Ecosystem](./practice/cfd_tools/)

Comprehensive guide to the CFD software landscape (coming soon)

---

### [Scripts](./scripts/)
**Computational tools, algorithms, simulations, and visualizations**

The scripts provide reusable implementations and examples for numerical methods, post-processing, visualization, and complete simulation workflows.

#### [Algorithms](./scripts/algorithms/)
**Mathematical and computational implementations**

<details>
<summary><b>Available algorithms</b></summary>

| Algorithm | Description | Applications |
|-----------|-------------|--------------|
| **[Correlation Functions](./scripts/algorithms/correlation_functions/)** | Spatial and temporal correlations | Turbulence statistics, pattern analysis |
| **[Kriging Interpolation](./scripts/algorithms/kriging_interpolation/)** | Gaussian process regression | Surrogate modeling, optimization |
| **[SVD Image Compression](./scripts/algorithms/image_compression_using_svd/)** | Singular value decomposition | Data compression, feature extraction |
| **[POD Analysis](./scripts/algorithms/pod/)** | Proper orthogonal decomposition | Modal analysis, ROM construction |
| **[Snapshot POD](./scripts/algorithms/snapshot_pod/)** | Efficient POD for large datasets | Flow field decomposition |
| **[Radial Basis Functions](./scripts/algorithms/radial_basis_functions/)** | RBF interpolation and approximation | Mesh morphing, optimization |
| **[Condition Number Analysis](./scripts/algorithms/condition_number_of_the_correlation_matrix/)** | Matrix conditioning assessment | Numerical stability, kriging | Each algorithm includes:
- Theoretical background and mathematical formulation
- Well-commented, modular implementation
- Validation against analytical/benchmark solutions
- Visualization of results
- Performance considerations and optimization tips

</details>

#### [Visualization Scripts](./scripts/plots/)
**Plotting and analysis tools with more than 30 scripts**

<details>
<summary><b>Visualization suite</b></summary>

**Aerodynamics & External Flows:**
- [Airfoil Profile Analysis](./scripts/plots/airfoil_profile/) - Geometry and pressure distribution
- [Airfoil Angle of Attack Studies](./scripts/plots/airfoil_angle_attack/) - Performance curves
- [Drag Coefficient Prediction](./scripts/plots/drag_coefficient_prediction/) - Validation cases
- [Mean Pressure Coefficient](./scripts/plots/mean_pressure_coefficient/) - Surface pressure plots

**Boundary Layer Phenomena:**
- [Boundary Layer Velocity Profiles](./scripts/plots/boundary_layer_velocity_profile/) - u+ vs y+
- [Laminar vs Turbulent Boundary Layers](./scripts/plots/laminar_vs_turbulent_boundary_layer/) - Comparison
- [Flow Separation Analysis](./scripts/plots/flow_separation_boundary_layer/) - Separation prediction
- [Boundary Layer Problems](./scripts/plots/boundary_layer_problem/) - Classic solutions

**Internal Flows:**
- [Laminar vs Turbulent Pipe Flow](./scripts/plots/laminar_vs_turbulent_pipe/) - Friction factors
- [Flow Rate in Pipes](./scripts/plots/flow_rate_pipe/) - Moody diagram applications

**Turbulence Analysis:**
- [Turbulent Flow Statistics](./scripts/plots/turbulent_flow/) - Reynolds stresses
- [POD Modes Visualization](./scripts/plots/pod_modes_2d/) - Energy-ranked modes
- [POD Modes and Temporal Coefficients](./scripts/plots/pod_modes_and_temporal_coefficients/) - Time evolution
- [POD Analysis for Flow Fields](./scripts/plots/pod_analysis_for_flow_fields/) - Complete workflow
- [Time-Averaged Velocity Field](./scripts/plots/time_averaged_velocity_field/) - Mean flow extraction
- [Longitudinal Velocity Fluctuations](./scripts/plots/longitudinal_velocity_fluctuations_and_projections/) - Turbulence intensity

**Compressible Flows:**
- [Compressible vs Incompressible](./scripts/plots/compressible_vs_incompressible/) - Mach number effects
- [Nozzle Flow Analysis](./scripts/plots/nozzle_flow/) - Isentropic relations

**Multiphase & Surface Tension:**
- [Meniscus Behavior](./scripts/plots/meniscus_behavior/) - Capillary effects
- [Pressure Difference Across Droplet](./scripts/plots/pressure_difference_across_spherical_droplet/) - Young-Laplace
- [Ship Hull in Water](./scripts/plots/ship_hull_in_water/) - Wave resistance

**Fundamentals & Dimensionless Numbers:**
- [Froude Number Analysis](./scripts/plots/froude_number/) - Free surface flows
- [Velocity Layers and Viscosity](./scripts/plots/velocity_layers_viscosity/) - Rheology
- [Archimedes Principle](./scripts/plots/archimedes_principle/) - Buoyancy demonstration

**Flow Visualization & Kinematics:**
- [Eulerian vs Lagrangian Flows](./scripts/plots/eulerian_lagrangian_flows/) - Description comparison
- [Mean Velocity Magnitude](./scripts/plots/mean_velocity_magnitude/) - Vector field visualization

**Numerical Methods:**
- [Grid Convergence Studies](./scripts/plots/comparing_grid_convergence/) - Mesh independence
- [Residual Variation](./scripts/plots/variation_of_residual/) - Convergence monitoring

**Statistical & Molecular:**
- [Probability Distribution of N₂ Molecules](./scripts/plots/probability_distribution_function_of_nitrogen_molecules/) - Kinetic theory

**Design Space Exploration:**
- [Design Space Distribution](./scripts/plots/design_space_distribution/) - Parameter studies

</details>

#### [Simulations](./scripts/simulations/)
**Complete simulation setups from problem definition to results**

<details>
<summary><b>Simulation cases</b></summary>

**Classical CFD Benchmarks:**
- **[Lid-Driven Cavity](./scripts/simulations/lid_driven_cavity/)**: The CFD "Hello World" - Validation of incompressible solvers
- **[Backward-Facing Step](./scripts/simulations/backward_facing_step_simple/)**: Flow separation and reattachment

**External Flow Problems:**
- **[Flow Past Cylinder (Eulerian)](./scripts/simulations/eulerian_cylinder_flow/)**: Vortex shedding, Strouhal number
- **[Cylinder Flow (Lattice Boltzmann)](./scripts/simulations/lattice_boltzmann_cylinder_flow/)**: LBM implementation

**Complex Phenomena:**
- **[Kelvin-Helmholtz Instability](./scripts/simulations/kelvin_helmholtz_instability/)**: Shear layer instabilities
- **[Rayleigh-Bénard Convection](./scripts/simulations/rayleigh_benard_convection/)**: Natural convection, pattern formation
- **[Vortex Shedding & Pathlines](./scripts/simulations/steady_and_unsteady_pathlines_with_vortex_shedding/)**: Unsteady visualization

**Heat Transfer:**
- **[1D Heat & Wave Equations](./scripts/simulations/1d_heat_and_wave_equations/)**: Fundamental PDE solutions
- **[2D Wave Simulation](./scripts/simulations/2d_wave_simulation/)**: Wave propagation

**Fluid Dynamics Simulator:**
- **[Real-Time Fluid Simulator](./scripts/simulations/simplified_real_time_fluid_dynamics_simulator/)**: Interactive visualization

**Interdisciplinary Applications:**
- **[Charged Particle in Magnetic Field](./scripts/simulations/charged_particle_dynamics_in_a_magnetic_field_using_runge_kutta_methods/)**: Runge-Kutta methods
- **[Schrödinger Equation](./scripts/simulations/schroedinger_equation/)**: Quantum mechanics analogy

**Statistical Physics:**
- **[Ising Model](./scripts/simulations/ising_model/)**: Phase transitions
- **[Bak-Tang-Wiesenfeld Sandpile](./scripts/simulations/bak_tang_wiesenfeld_sandpile_model_3d/)**: Self-organized criticality

**Creative Applications:**
- **[Laplace Equation Maze Solver](./scripts/simulations/laplace_equation_maze_solver/)**: Potential flow in complex domains

Each simulation includes:
- Problem description and physical significance
- Learning objectives
- Setup instructions and parameter files
- Numerical method details
- Post-processing scripts
- Validation data and expected results
- Extensions and research directions

</details>

---

## Getting Started

### Prerequisites and Skill Assessment

<details>
<summary><b>Core knowledge requirements</b></summary>

**Mathematics (Essential):**
- Vector Calculus: Gradients, divergence, curl, line/surface integrals
- Differential Equations: ODEs, PDEs, classification of PDEs
- Linear Algebra: Matrices, eigenvalues, SVD, norms
- Numerical Analysis: Truncation error, stability, convergence

**Physics (Essential):**
- Classical Mechanics: Newton's laws, conservation principles
- Thermodynamics: First/second laws, equations of state
- Fluid Mechanics: Basic concepts, Bernoulli, viscosity

**Programming (Recommended):**
- Python: NumPy, SciPy, Matplotlib basics
- MATLAB: Or compatible alternatives (Octave, Julia)
- Version Control: Git fundamentals for collaboration

**Software (Will Learn):**
- ParaView: Scientific visualization (we'll teach you)
- Gmsh: Mesh generation (tutorials provided)
- Text Editor/IDE: VS Code, PyCharm, or similar

</details>

### Quick Start Guide: First Two Weeks

#### **Week 1: Foundation Building**

**Day 1-2: Understanding the Basics**
```
 Read: Fluid Mechanics Fundamentals (./notes/fluid_mechanics/intro.md)
 Learn: What is CFD? When do we need it? What can it do?
 Goal: Understand continuum hypothesis and conservation laws
```

**Day 3-4: Mathematical Framework**
```
 Read: Governing Equations introduction
 Learn: Navier-Stokes equations conceptually
 Goal: Recognize the equations, understand each term physically
 Exercise: Identify terms in simple flow problems
```

**Day 5-7: First Computational Experience**
```
 Install: Python, NumPy, Matplotlib
 Run: Simple 1D heat equation script (./scripts/simulations/1d_heat_and_wave_equations/)
 Visualize: Temperature evolution over time
 Goal: See how equations become code become solutions
```

#### **Week 2: Hands-On Application**

**Day 8-9: Visualization Tools**
```
 Install: ParaView (free, powerful)
 Follow: ParaView Introduction (./practice/paraview/intro.md)
 Load: Example dataset, create streamlines
 Goal: Visualize flow fields professionally
```

**Day 10-12: Your First Complete Simulation**
```
 Run: Lid-driven cavity (./scripts/simulations/lid_driven_cavity/)
 Understand: Problem setup, boundary conditions
 Analyze: Velocity profiles, vortex formation
 Goal: Complete simulation start-to-finish
 Validate: Compare against benchmark data
```

**Day 13-14: Consolidation & Next Steps**
```
 Review: What you've learned
 Plan: Choose your learning pathway
 Engage: Join CFD communities, ask questions
 Document: Your learning journey
```

### Recommended Learning Sequence

**For Complete Beginners:**
1. Start with [Fluid Mechanics Fundamentals](./notes/fluid_mechanics/intro.md)
2. Read [Dimensional Analysis](./notes/fluid_mechanics/dimensions.md) - understand Reynolds number
3. Run [1D Heat Equation](./scripts/simulations/1d_heat_and_wave_equations/) to see numerics in action
4. Try [Lid-Driven Cavity](./scripts/simulations/lid_driven_cavity/) as first CFD problem
5. Learn [ParaView](./practice/paraview/intro.md) for visualization
6. Explore [Finite Volume Methods](./notes/numerical/fvm/) for industry-standard approach

**For Students with Fluid Mechanics Background:**
1. Review [Governing Equations](./notes/fluid_mechanics/governing_equations/)
2. Deep dive into [Turbulence Theory](./notes/fluid_mechanics/turbulence/)
3. Study [Finite Volume Methods](./notes/numerical/fvm/) in detail
4. Implement [Backward-Facing Step](./scripts/simulations/backward_facing_step_simple/)
5. Analyze results with [Visualization Scripts](./scripts/plots/)
6. Explore [POD Analysis](./scripts/algorithms/pod/) for data-driven methods

**For Practicing Engineers:**
1. Review [CFD Methods Overview](./notes/numerical/cfd/) to understand solver internals
2. Master [Gmsh](./practice/gmsh/) for custom geometries
3. Study industry-relevant cases in [Manual Projects](./practice/manual_projects/)
4. Automate workflows with [Scripts](./scripts/)
5. Learn [Advanced Turbulence Modeling](./notes/fluid_mechanics/turbulence/)
6. Explore [Optimization Methods](./notes/machine_learning/) for design

**For ML/AI Practitioners:**
1. Quick CFD overview: [Fundamentals](./notes/fluid_mechanics/intro.md)
2. Understand [Navier-Stokes Equations](./notes/fluid_mechanics/governing_equations/)
3. Learn [POD/ROM](./notes/numerical/pod/) for dimensionality reduction
4. Study [Machine Learning Notes](./notes/machine_learning/)
5. Implement [Physics-Informed Neural Networks](./notes/machine_learning/)
6. Apply to [Optimization Problems](./scripts/algorithms/)

---

## Key Features and Differentiators

### Comprehensive Coverage
- **103+ Theory Documents**: Every concept explained from first principles to advanced applications
- **57+ Python Scripts**: Production-ready, validated implementations
- **30+ Visualization Tools**: Professional-quality plots and animations
- **15+ Complete Simulations**: From setup to validated results
- **9+ Core Algorithms**: Mathematical implementations with theory

### Educational Design
- **Progressive Complexity**: Carefully ordered from basics to cutting-edge research
- **Multiple Learning Styles**: Theory, code, visualizations, hands-on projects
- **Cross-Referenced**: Navigate seamlessly between related concepts
- **Validated Content**: Benchmarked against literature and standard cases
- **Active Maintenance**: Regular updates with latest developments

### Practical Applicability
- **Industry-Standard Tools**: ParaView, Gmsh, OpenFOAM integration
- **Real-World Problems**: Not just toy examples, actual engineering challenges
- **Performance Optimized**: Efficient implementations with profiling
- **Reproducible Results**: Complete documentation for every script
- **Extensible Codebase**: Modular design for easy customization

### Research-Grade Content
- **Latest Developments**: ML/AI integration, modern numerical methods
- **Literature Connected**: 80+ references to papers, books, courses
- **Novel Methods**: Cutting-edge techniques not in textbooks
- **Open Problems**: Guidance on current research frontiers
- **Citation Ready**: Properly formatted, academically rigorous

### Community Focus
- **Open Source**: MIT license, use anywhere for any purpose
- **Collaborative**: Contributions welcome from all skill levels
- **Diverse Perspectives**: Global community of contributors
- **Supportive**: Detailed docs, examples, troubleshooting guides
- **Growing**: New content added regularly based on community needs

---

## Troubleshooting and FAQ

<details>
<summary><b>Common issues and solutions</b></summary>

### Getting Started Problems

**Q: I'm overwhelmed. Where should I actually start?**
A: Begin with the [Fundamentals](./notes/fluid_mechanics/intro.md), then run the [Lid-Driven Cavity](./scripts/simulations/lid_driven_cavity/) simulation. This provides a manageable first step before deeper study.

**Q: I don't have a strong math background. Can I still learn CFD?**
A: Yes, but it will take more time. Start with the fundamentals and use online resources (Khan Academy, MIT OpenCourseWare) to fill gaps as needed. Focus on physical understanding first.

**Q: What programming language should I use?**
A: Python is recommended for beginners (used in this repo). MATLAB is also common in academia. For production CFD, C/C++ and Fortran are standard but not necessary for learning.

### Technical Issues

**Q: My simulation diverges. What should I check?**
A: Common causes (in order of frequency):
1. Time step too large (reduce by 10x and try)
2. Boundary conditions incorrect or conflicting
3. Initial conditions far from solution
4. Mesh quality poor (high skewness, aspect ratio)
5. Numerical scheme inappropriate for the problem

**Q: Results don't match theory/experiments. Why?**
A: Systematic debugging:
1. Verify geometry and mesh are correct
2. Check boundary conditions carefully
3. Ensure proper units and scaling
4. Verify convergence (residuals, monitors)
5. Compare turbulence model predictions
6. Assess if flow regime matches assumptions

**Q: Simulation runtime is too long. How can I improve performance?**
A:
1. Start with coarser mesh, refine only where needed
2. Use symmetry to reduce domain size
3. Choose efficient solver settings (multigrid, etc.)
4. Parallelize (MPI) if available
5. Consider steady-state instead of transient if appropriate
6. Use better initial guess (from similar case)

### Conceptual Questions

**Q: What's the difference between RANS, LES, and DNS?**
A:
- **DNS** (Direct Numerical Simulation): Resolves all relevant turbulence scales. It is highly accurate for appropriate problem settings, but computationally expensive and primarily used in research.
- **LES** (Large Eddy Simulation): Resolves large eddies and models smaller scales. It can provide detailed unsteady information, but generally requires substantially more computation than RANS.
- **RANS** (Reynolds-Averaged Navier-Stokes): Models turbulence effects through averaged equations. It is widely used in industry because it balances accuracy, robustness, and cost.

**Q: Which turbulence model should I use?**
A: Quick guide:
- **k-ε**: General purpose, external flows, high Reynolds number
- **k-ω SST**: Boundary layers, separation, most versatile
- **Spalart-Allmaras**: Aerospace, external aerodynamics
- **LES**: Unsteady, complex geometries, when RANS fails
When in doubt, start with k-ω SST.

**Q: How do I know if my mesh is good enough?**
A: Perform mesh independence study:
1. Run simulation on your mesh
2. Refine mesh (2x points in each direction)
3. Compare key results (drag, pressure, etc.)
4. If <1-2% difference, original mesh is acceptable
5. Always check mesh quality metrics (skewness < 0.85, aspect ratio < 100)

**Q: What's Y+ and why does everyone talk about it?**
A: Y+ is a dimensionless wall distance. Critical for turbulence modeling:
- **Y+ < 1**: Resolve viscous sublayer (best accuracy, expensive)
- **30 < Y+ < 300**: Use wall functions (industry standard)
- **1 < Y+ < 30**: "Buffer layer" - avoid this range!

</details>

---

## References and Further Reading

**A curated, categorized collection of more than 80 resources spanning textbooks, research papers, online courses, code repositories, and visualization tools.**

### Essential Online Resources

**Interactive Learning Platforms:**
- [CFD Python: 12 Steps to Navier-Stokes by Lorena Barba](https://lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/) - A widely used hands-on introduction to CFD through Python, structured in incremental steps.
- [CFD General Principles by CFD Direct](https://doc.cfd.direct/notes/cfd-general-principles/) - Fundamental concepts explained by the makers of OpenFOAM
- [Scientific Computing by Chasnov](https://math.libretexts.org/Bookshelves/Scientific_Computing_Simulations_and_Modeling/Scientific_Computing_(Chasnov)/III%3A_Computational_Fluid_Dynamics/14%3A_The_Governing_Equations) - Complete theoretical foundations with clear explanations

**Validation & Benchmark Databases:**
- [NASA Turbulence Modeling Resource](https://turbmodels.larc.nasa.gov/) - A major database for turbulence model validation cases
- [Wall-Modeled Large Eddy Simulation Resource](https://wmles.umd.edu/) - Comprehensive WMLES database and guidelines
- [Airfoil Tools Database](http://www.airfoiltools.com/) - Extensive airfoil geometry and performance data
- [NWTF Experimental Database](https://www.nwtf.ac.uk/dataset/2687/) - Airbus Wind Tunnel Dataset on RAE2822 transonic aerofoil

**Academic Repositories:**
- [DepositOnce - TU Berlin](https://depositonce.tu-berlin.de/) - Academic repository with cutting-edge CFD research
- [National Committee for Fluid Mechanics Film Series](https://youtube.com/playlist?list=PL0EC6527BE871ABA3) - Classic educational films, timeless fluid mechanics visualization

---

### Essential Textbooks

**Foundational CFD Theory** *(Start Here)*

| Book | Authors | Best For | Level |
|------|---------|----------|-------|
| [**Computational Fluid Dynamics: The Basics with Applications**](https://amzn.to/42iuJNV) | **John D. Anderson** | Comprehensive introduction, aerospace emphasis | Beginner-Intermediate |
| [**An Introduction to Computational Fluid Dynamics: The Finite Volume Method**](https://amzn.to/3EbEMfG) | **H.K. Versteeg & W. Malalasekera** | Industry-standard FVM approach, very clear | Beginner-Intermediate |
| [**Computational Methods for Fluid Dynamics**](https://amzn.to/3FSZ9iq) | **Ferziger, Peric & Street** | Advanced, comprehensive, graduate-level | Advanced | **Numerical Methods & Implementation**

| Book | Authors | Best For | Level |
|------|---------|----------|-------|
| [**Numerical Heat Transfer and Fluid Flow**](https://amzn.to/42qd0o1) | **Suhas V. Patankar** | Classic text, SIMPLE algorithm, still relevant | Intermediate |
| [**Computational Fluid Dynamics: Principles and Applications**](https://amzn.to/4j7adqY) | **J. Blazek** | Industrial CFD, practical guidelines | Intermediate-Advanced | **Modern Data-Driven Approaches**

| Book | Authors | Best For | Level |
|------|---------|----------|-------|
| [**Data-Driven Science and Engineering**](https://amzn.to/3RHJncw) | **J. Nathan Kutz** | ML for dynamical systems, POD, DMD | Intermediate-Advanced |
| [**Machine Learning Control**](https://amzn.to/4jeggJC) | **Steven L. Brunton & Bernd R. Noack** | ML for flow control, cutting-edge | Advanced |

---

### Key Research Papers

**Machine Learning in CFD** *(The Future)*

- [**Machine Learning for Fluid Dynamics: An Overview**](https://arxiv.org/abs/1905.11075)
  *Comprehensive review of ML applications in fluid mechanics. Essential reading for anyone entering the field.*

- [**Machine Learning-Based CFD Simulations: A Review**](https://link.springer.com/article/10.1007/s00521-022-07838-6)
  *State-of-the-art analysis, models, open threats, and future tactics. 2022 comprehensive survey.*

- [**Physics-Informed Neural Networks: A Deep Learning Framework for Solving Forward and Inverse Problems**](https://www.brown.edu/research/projects/crunch/sites/brown.edu.research.projects.crunch/files/uploads/Physics-informed%20neural%20networks_A%20deep%20learning%20framwork%20fir%20solving%20forward%20and%20inverse%20probelms%20involving%20nonlinear%20partial%20differential%20equations.pdf)
  *The foundational PINN paper by Raissi, Perdikaris & Karniadakis. Revolutionized scientific ML.*

- [**Machine Learning in CFD - Recent Advances**](https://www.tandfonline.com/doi/full/10.1080/10618562.2023.2175788)
  *2023 update on ML integration in computational fluid dynamics.*

- [**Nature Reviews - GK**](https://www.brown.edu/research/projects/crunch/sites/brown.edu.research.projects.crunch/files/uploads/Nature-REviews_GK.pdf)
  *High-impact review paper on computational methods*

**Future Directions & Vision**

- [**CFD of the Future: Year 2025 and Beyond**](https://www.researchgate.net/publication/339808378_CFD_of_the_Future_Year_2025_and_Beyond)
  *Expert perspectives on where the field is heading. Insightful predictions on AI, HPC, uncertainty quantification.*

**Historical & Classical References**

- [**Pratt & Whitney: The Aircraft Engine and Its Operation (1949)**](https://www.scribd.com/document/307072703/Pratt-Whitney-The-Aircraft-Engine-and-Its-Operation-Rev1949-BZ)
  *Classic engineering reference showing the foundations of aerospace CFD applications.*

---

### Code Repositories and Open Source Projects

**Educational Implementations** *(Learn by Doing)*

- [**Machine Learning and Simulation by Ceyron**](https://github.com/Ceyron/machine-learning-and-simulation)
  *Excellent integration of ML techniques with physics simulations. Clean code, great documentation.*

- [**NVIDIA Modulus Airfoil Optimization**](https://github.com/neo-fetch/nvidia-modulus-airfoil-optimisation)
  *Modern GPU-accelerated CFD with AI. Shows the cutting edge of physics-informed ML.*
  - [Dr. Yang's LDC 2D Implementation](https://github.com/neo-fetch/nvidia-modulus-airfoil-optimisation/blob/master/Dr-Yang_ldc_2d.py)

**Finite Element Resources**

- [**Introductory Finite Elements - EAFIT**](https://github.com/AppliedMechanics-EAFIT/Introductory-Finite-Elements)
  *Comprehensive FEM course materials with Python implementations.*

- [**Dolfin X FEM Tutorial**](https://jsdokken.com/dolfinx-tutorial/fem.html)
  *Modern FEM with FEniCS/DolfinX. Excellent for complex geometries and multiphysics.*

**Project Showcases**

- [**David Penner's CFD Projects**](https://davidpenner74.wixsite.com/davidpenner/projects)
  *Inspiring portfolio of practical CFD applications and visualizations.*

---

### Video Learning Resources

**University-Level Courses** *(Structured Learning)*

- [**MIT Lecture Series on CFD**](https://www.youtube.com/@AeroCFD)
  *Academic-level instruction from one of the world's premier aerospace programs.*

- [**Computational Fluid Dynamics - ME615 IIT Mandi**](https://youtube.com/playlist?list=PLOUcBDsCNnMweTuft1qq25CQbyyKqZKvI)
  *Complete university CFD course. Theory, numerics, applications - all covered systematically.*

- [**Qiqi Wang's CFD Lectures**](https://www.youtube.com/c/QiqiWangGG)
  *MIT professor's extensive collection. Advanced numerical analysis, deep mathematical insights.*

- [**The Perić Lectures on CFD**](https://youtu.be/8a0j2DQiTVQ)
  *Industry perspective from a leading contributor to commercial CFD development.*

**Numerical Methods Fundamentals**

- [**Numerical Methods by Hand**](https://youtube.com/playlist?list=PL5_Bm_WH1i3fAQP6G2_SaazjNIy3m8QbH)
  *Understanding algorithms by working through them manually. Builds deep intuition.*

- [**Mechanics Problems Solved by Hand**](https://youtube.com/playlist?list=PL7FF084F8C414D602)
  *Analytical problem-solving techniques. Valuable for validation and understanding.*

- [**Postcard Professor's Solution Methods**](https://www.youtube.com/c/PostcardProfessor/playlists)
  *Step-by-step problem solving across various mechanics topics.*

- [**Additional Hand Solutions**](https://www.youtube.com/watch?v=PPt_FfoUqBQ&list=PLD45F0FD958B864AD)
  *More worked examples across fluid mechanics and applied mathematics.*

- [**Theoretical Mechanics and Numerical Methods Channel**](https://www.youtube.com/channel/UCcqQi9LT0ETkRoUu8eYaEkg)
  *Various topics from theoretical mechanics to computational methods.*

**Specialized Topics**

- [**Data-Driven Methods for Science and Engineering Seminar**](https://youtube.com/playlist?list=PLWL3MaEZQ5I0x5SoN-whc6wfxvZr4E5v9)
  *Cutting-edge seminars on ML, ROM, and modern computational methods.*

- [**Gentle Introduction to Fluid Concepts**](https://www.youtube.com/watch?v=zGuVWSKBc4Y&list=PLyYlZ2ZyWpnh6Xy8xsqIFQKPiMzVkUkdG)
  *Visual, intuitive explanations of complex fluid phenomena. Excellent for beginners.*

---

## License

This project is licensed under the **[MIT License](LICENSE)** - see the LICENSE file for full details.

**What this means:**
- **Free to use** for any purpose (personal, educational, commercial)
- **Free to modify** and create derivative works
- **Free to distribute** original or modified versions
- **Attribution required**: Credit the original authors
- **No warranty**: Provided "as is" without guarantees

This ensures the content remains **open and accessible** for educational and research purposes worldwide.

---

## Acknowledgments

This repository stands on the shoulders of giants. We are deeply grateful to:

- **The Global CFD Community**: Researchers, engineers, and educators who generously share knowledge
- **Academic Institutions**: Universities worldwide advancing CFD science and educating future practitioners
- **Open-Source Contributors**: Developers of OpenFOAM, ParaView, Python scientific stack, and countless other tools
- **Textbook Authors**: Who have distilled complex concepts into accessible learning materials
- **Pioneering Researchers**: From Navier and Stokes to modern ML practitioners, advancing the field
- **Direct Contributors**: Everyone who has submitted PRs, reported issues, or suggested improvements

**Special recognition to foundational works:**
- Ludwig Prandtl's boundary layer theory (1904)
- The SIMPLE algorithm by Patankar & Spalding (1972)
- Direct Numerical Simulation pioneers (1970s-1980s)
- Large Eddy Simulation development (1980s-1990s)
- Recent Physics-Informed Neural Networks revolution (2017-present)

This repository builds upon **decades of collective research and development** in computational fluid dynamics. Every concept, method, and insight has a rich history we strive to honor and preserve.

---

## Contact and Support

**Questions, suggestions, or collaboration requests**

- **Bug Reports**: [Open an issue](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/issues) with details
- **Feature Requests**: [Propose enhancements](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/issues) with use cases
- **Collaboration**: [Open a discussion](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/discussions) for projects
- **Direct Contact**: Create an issue for private matters (will move to email if needed)

---

## Support This Project

**If this repository has helped you**, please:
- **Star the repository** to show support and boost visibility
- **Share with colleagues** and students
- **Provide feedback** through issues or discussions
- **Contribute back** to help others on their journey

### Building a comprehensive CFD learning resource

*Maintained by the global CFD community*

**Last Updated**: December 2024
**Content**: 103+ theory docs, 57+ scripts, 15+ simulations, 80+ references
**Global Reach**: Used by students and professionals worldwide

[Back to Top](#computational-fluid-dynamics-cfd-resources)

---

*"In CFD, as in engineering practice, mastery develops through consistent work across theory, implementation, validation, and interpretation. This repository is intended to support that process."*
