# Reduced Order Modeling (ROM) in CFD

Reduced Order Modeling (ROM) has become a critical tool in computational fluid dynamics (CFD) for tackling complex, parameterized simulations at a fraction of the original computational cost. Instead of solving large-scale PDE problems repeatedly for different conditions, ROM provides a low-dimensional approximation that can be evaluated rapidly, facilitating tasks like real-time simulation, design optimization, uncertainty quantification, and control.

## What Is ROM?

At its core, ROM reduces the dimensionality of a high-fidelity model by identifying a small set of modes (basis functions) that approximate the solution space of the parameterized PDE. For fluid dynamics, where full simulations may involve millions of degrees of freedom (DOFs), ROM can bring the problem down to a system with tens or hundreds of DOFs while maintaining good accuracy.

## Typical Inputs and Outputs of a ROM Algorithm

**Inputs to ROM**:

I. **High-Fidelity (HF) Model**:  

- A CFD solver (e.g., finite volume, finite element, spectral method) that accurately solves the Navier-Stokes equations (or related PDEs) for given parameters $\mu \in \mathcal{P}$.
- The parameter set $\mathcal{P}$ can include geometric parameters, boundary conditions, Reynolds numbers, Mach numbers, material properties, or forcing terms.

II. **Snapshots**:

- A collection of solution fields (e.g., velocity, pressure) computed at various parameter values and/or time instances. These snapshots form a dataset representing the solution manifold.
- Each snapshot is typically a vector of dimension $N_h$, corresponding to the DOFs of the HF discretization.

III. **Choice of Reduction Method**:

- POD (Proper Orthogonal Decomposition), greedy algorithms, or other model reduction techniques.
- Possibly a posteriori error estimators and sampling strategies (e.g., adaptive selection of parameter points).

**Outputs from ROM**:

I. **Reduced Basis**:

- A small set of modes (basis vectors) $\{\xi_1, \ldots, \xi_N\}$ that represent the solution space efficiently.
- Each mode is a vector of length $N_h$, but only $N \ll N_h$ modes are kept, drastically reducing complexity.

II. **Reduced-Order Model (ROM) Equations**:

- A low-dimensional system of ODEs or algebraic equations involving only $N$ unknowns.
- Parameter-dependent reduced operators (matrices, vectors) of size $N \times N$, computed offline.

III. **Reduced Predictions**:

- For new parameter values $\mu^*$, the ROM yields an approximate solution $u_{N}(\mu^*)$ at low cost.
- Can quickly evaluate outputs of interest $s(\mu^*)$ related to lift, drag, flux, or integrated quantities without re-running the HF simulation.

## The ROM Algorithm: Step-by-Step

I. **Offline Phase** (Computationally Intense, Done Once):

**Step A: Construct the HF Model**:  

Solve the full-order PDE discretized by, for example, a finite volume method (FVM) or finite element method (FEM). This step uses the original large-dimensional system with $N_h$ DOFs.

**Step B: Sampling the Parameter Space**:  

Choose parameter points $\{\mu_1, \ldots, \mu_{N_s}\}$ and possibly time instances. Run the HF model at each sampled point to produce snapshots:

$$u_h(\mu_1), u_h(\mu_2), \ldots, u_h(\mu_{N_s}) \in \mathbb{R}^{N_h}.$$

**Step C: Snapshot Matrix and POD**:  

Arrange snapshots into a matrix $X \in \mathbb{R}^{N_h \times N_s}$. Apply POD:

- Compute correlation matrix $C = X^T X$.
- Perform SVD or eigenvalue decomposition to find eigenvectors and eigenvalues.
- Select the top $N$ eigenmodes with the largest eigenvalues to form the reduced basis $\{\xi_i\}_{i=1}^N$.

**Step D: Galerkin Projection**:  

Insert the reduced basis into the PDE (weak) formulation to derive reduced operators. Precompute:

$$A^r(\mu) = B^T A^{\mu} B, \quad f^r(\mu) = B^T f^\mu,$$

where $A^\mu, f^\mu$ are the high-fidelity system matrices and vectors, and $B \in \mathbb{R}^{N_h \times N}$ contains the basis modes. Store these reduced operators (or parametric components for efficient online assembly).

II. **Online Phase** (Cheap, Repeated):

- Given a new parameter $\mu^*$,
- Assemble the reduced system $A^r(\mu^*) u_N^{\mu^*} = f^r(\mu^*)$ of size $N \times N$.
- Solve this small system for $u_N^{\mu^*}$.
- Evaluate outputs $s(\mu^*) = l(u_N^{\mu^*};\mu^*)$.

This separation of offline/online computations is a hallmark of ROM, allowing near real-time responses in the online stage.

## Beyond POD: Advanced Methods and A Posteriori Error Estimates

While POD is a mainstay approach, other methods like greedy algorithms have emerged. These require error estimators to guide snapshot selection:

- **Greedy Algorithms**:  

Start with an empty basis. Iteratively add the snapshot that maximizes the error (predicted by a posteriori error estimators) until a desired accuracy is met.  
Advantages:
- Efficient handling of large parameter spaces $\mathcal{P}$.
- Automatic discovery of "difficult" parameter regions that require more modes.
- **Error Estimators**:
- A posteriori error bounds ensure that the ROM predictions are reliable.
- These estimators depend on coercivity and continuity constants of the bilinear forms and often leverage offline computations.

Combining POD or greedy algorithms with a posteriori error estimators yields robust ROM frameworks that guarantee solution quality and adapt the basis as needed.

## Extending to Nonlinear, Time-Dependent, and Turbulent Flows

ROM initially found success in linear, elliptic PDEs, but the approach has matured:

**Nonlinear Problems (e.g., Navier-Stokes)**:

- Nonlinear terms require additional strategies: Empirical interpolation or hyper-reduction techniques approximate nonlinear operators efficiently.

**Time-Dependent Problems**:
  
- Treat snapshots as a temporal sequence. Time discretization is done once in the HF model. The ROM solves a much smaller ODE system in time, allowing fast parametric sweeps.

**Turbulent Flows**:
  
- Including turbulence models (RANS, LES) in ROM is challenging due to nonlinearity and complex dynamics.  
- Approaches like eddy viscosity modeling in ROM or calibration strategies ensure reduced models still capture main turbulent features.

## ROM in Finite Volume Discretizations

While ROMs were first popularized with finite element frameworks, they have since been adapted to finite volume discretizations (FVM)—common in industrial CFD codes (e.g., OpenFOAM):

**FVM-RBM Integration**:

- The finite volume method provides cell-based discretization and flux computations.
- ROM must approximate the flux terms and residuals in the reduced space. This can be non-trivial due to nonlinearities and flux reconstructions.
- Techniques: Projection of fluxes onto the reduced basis, hyper-reduction methods (e.g., empirical cubature) to reduce complexity in evaluating nonlinear terms at runtime.

## Practical Considerations and Challenges

I. **Choice of Parameter Sampling**:

- The offline cost and final model quality depend heavily on selecting parameter samples. Poor sampling can miss crucial dynamics.
- Adaptive or model-based sampling strategies guide snapshot selection.

II. **Model Fidelity vs. Reduction**:

- A trade-off exists between how many modes are kept (accuracy) and how small $N$ must be (speed).
- For highly non-linear or strongly parameter-dependent flows, more modes might be needed, increasing ROM dimension and reducing speed gains.

III. **Stability Issues**:

Ensuring stability in ROM is crucial. Even if the HF model is stable, truncating modes can lead to instabilities. Stabilization techniques or enriching the basis with additional stabilizing modes may be required.

### Further Reading and Resources

I. **Books**:

- "Model Reduction and Approximation: Theory and Algorithms" by Peter Benner, Albert Cohen, Mario Ohlberger, and Karen Willcox.
- "Reduced Order Methods for Modeling and Computational Reduction" by Alfio Quarteroni and Gianluigi Rozza.

II. **Research Papers**:

- Berkooz, Holmes, and Lumley: Foundational works applying POD to fluid dynamics.
- Rowley, Taira et al.: Comparing and contrasting reduced-order modeling techniques for fluid flows.
- Rozza, Hesthaven: Parameterized PDEs and RBMs with rigor in a posteriori error estimates.

III. **Software and Tutorials**:

- OpenFOAM and related user communities discussing ROM interfaces.
- RBmatlab and other research codes for reduced basis methods.
- Online video lectures and MOOC content from universities and institutes focusing on ROM.
