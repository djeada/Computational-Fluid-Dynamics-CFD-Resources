# Roadmap

Topics that are planned but not written yet. Section READMEs used to link to these pages before they existed; the links were removed so that every link in the repository resolves. If you want to write one, open an issue or a draft pull request so work isn't duplicated, and follow [CONTRIBUTING.md](CONTRIBUTING.md). Suggested file paths are given so new pages slot into the existing structure.

## Fluid mechanics (`notes/fluid_mechanics/`)

### Governing equations and properties

- [ ] General conservation form of the governing equations: `governing_equations/conservation_form.md`
- [ ] Thermodynamic properties of fluids: `fluid_properties/thermodynamic_properties.md`

### Inviscid flow

- [ ] Euler equations: `inviscid_flow/euler_equations.md`
- [ ] Circulation, vorticity and Kelvin's theorem: `inviscid_flow/circulation_vorticity.md`
- [ ] Conformal mapping and the Joukowski transform: `inviscid_flow/conformal_mapping.md`

### Viscous flow

- [ ] Exact solutions of the Navier–Stokes equations (Couette, Poiseuille, Stokes problems): `viscous_flow/exact_solutions.md`
- [ ] Lubrication theory: `viscous_flow/lubrication_theory.md`
- [ ] Stokes (creeping) flow: `viscous_flow/stokes_flow.md`

### Dimensional analysis

- [ ] Buckingham Pi theorem in depth: `dimensional_analysis/pi_theorem.md`
- [ ] Similarity and scaling laws: `dimensional_analysis/similarity.md`
- [ ] Model testing and scaling: `dimensional_analysis/model_testing.md`

### Internal flow

- [ ] Duct flow and non-circular conduits: `internal_flow/duct_flow.md`
- [ ] Flow in porous media: `internal_flow/porous_media.md`
- [ ] Pipe network analysis: `internal_flow/network_analysis.md`

### Hydrodynamic stability

- [ ] Linear stability analysis: `stability/linear_stability.md`
- [ ] Kelvin–Helmholtz instability: `stability/kelvin_helmholtz.md`
- [ ] Rayleigh–Taylor instability: `stability/rayleigh_taylor.md`
- [ ] Transition to turbulence: `stability/transition.md`

### Heat and mass transfer

- [ ] Heat transfer in fluids: `heat_mass_transfer/heat_transfer.md`
- [ ] Mass transfer and diffusion: `heat_mass_transfer/mass_transfer.md`
- [ ] Convective transport: `heat_mass_transfer/convective_transport.md`
- [ ] Analogies between heat, mass and momentum transfer: `heat_mass_transfer/transport_analogies.md`

### Multiphase flow

- [ ] Two-phase flow theory: `multiphase/two_phase_flow.md`
- [ ] Bubble dynamics: `multiphase/bubble_dynamics.md`
- [ ] Droplet formation and dynamics: `multiphase/droplet_dynamics.md`
- [ ] Particle-laden flows: `multiphase/particle_laden_flows.md`

### Specialized topics

- [ ] Magnetohydrodynamics: `specialized_topics/magnetohydrodynamics.md`
- [ ] Microfluidics: `specialized_topics/microfluidics.md`
- [ ] Non-Newtonian fluids: `specialized_topics/non_newtonian.md`
- [ ] Geophysical fluid dynamics: `specialized_topics/geophysical_fluids.md`
- [ ] Biological fluid mechanics: `specialized_topics/biological_fluids.md`
- [ ] Astrophysical fluid dynamics: `specialized_topics/astrophysical_fluids.md`
- [ ] Environmental fluid mechanics: `specialized_topics/environmental_fluids.md`

### Mathematical methods

- [ ] Vector calculus in fluid mechanics: `mathematical_methods/vector_calculus.md`
- [ ] Complex analysis applications: `mathematical_methods/complex_analysis.md`
- [ ] Perturbation methods: `mathematical_methods/perturbation_methods.md`
- [ ] Green's functions: `mathematical_methods/greens_functions.md`
- [ ] Variational methods: `mathematical_methods/variational_methods.md`

## Numerical methods (`notes/numerical/`)

- [ ] Dynamic mode decomposition (DMD): `rom/dmd.md`
- [ ] High-order methods (spectral, discontinuous Galerkin): `high_order/intro.md`
- [ ] Immersed boundary and cut-cell methods: `immersed_boundary/intro.md`
- [ ] Pressure–velocity coupling (SIMPLE, PISO) in depth: `fvm/pressure_velocity_coupling.md`

## Machine learning (`notes/machine_learning/`)

- [ ] Physics-informed neural networks (PINNs): `neural_networks/pinns.md`
- [ ] Neural operators (DeepONet, Fourier neural operator): `neural_networks/neural_operators.md`
- [ ] Machine-learning-augmented turbulence closures: `flow/ml_turbulence_closures.md`

## Applied mechanics (`notes/applied_mechanics/`)

### Transportation

- [ ] Ships and marine vehicles: `transportation/ships/`
- [ ] Railways: `transportation/railways/`
- [ ] Spacecraft: `transportation/spacecraft/`

### Structural engineering

- [ ] Building structures: `structural/buildings.md`
- [ ] Bridges: `structural/bridges.md`
- [ ] Towers and masts: `structural/towers.md`
- [ ] Earthquake engineering: `structural/earthquake.md`
- [ ] Wind engineering: `structural/wind_engineering.md`

### Energy systems

- [ ] Wind turbines: `energy/wind_turbines.md`
- [ ] Hydroelectric systems: `energy/hydroelectric.md`
- [ ] Solar tracking systems: `energy/solar_tracking.md`
- [ ] Energy storage systems: `energy/energy_storage.md`

### Robotics and automation

- [ ] Robot kinematics: `robotics/kinematics.md`
- [ ] Robot dynamics: `robotics/dynamics.md`
- [ ] Control of robotic systems: `robotics/control.md`
- [ ] Mobile robotics: `robotics/mobile_robotics.md`

### Biomedical applications

- [ ] Biomechanics: `biomedical/biomechanics.md`
- [ ] Prosthetics and orthotics: `biomedical/prosthetics.md`
- [ ] Cardiovascular mechanics: `biomedical/cardiovascular.md`
- [ ] Sports biomechanics: `biomedical/sports_biomechanics.md`

### Advanced topics

- [ ] Nonlinear mechanics: `advanced/nonlinear_mechanics.md`
- [ ] Computational mechanics: `advanced/computational_mechanics.md`
- [ ] Multibody dynamics: `advanced/multibody_dynamics.md`
- [ ] Continuum mechanics: `advanced/continuum_mechanics.md`

## Practice (`practice/`)

- [ ] Manual project: airfoil analysis at several angles of attack: `manual_projects/airfoil_analysis.md`
- [ ] Manual project: turbulent pipe flow compared with correlations: `manual_projects/turbulent_pipe_flow.md`
- [ ] Manual project: heat exchanger study: `manual_projects/heat_exchanger.md`

## Scripts (`scripts/`)

- [ ] Validation cases that compare against published benchmark data and report error norms
- [ ] Dynamic mode decomposition example: `algorithms/dmd/`
- [ ] Shock tube (Sod problem) with a finite-volume Godunov scheme: `simulations/sod_shock_tube/`
