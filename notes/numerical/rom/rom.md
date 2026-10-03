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

$$
u_h(\mu_1), u_h(\mu_2), \ldots, u_h(\mu_{N_s}) \in \mathbb{R}^{N_h}
$$

**Step C: Snapshot Matrix and POD**:

Arrange snapshots into a matrix $X \in \mathbb{R}^{N_h \times N_s}$. Apply POD:

- Compute correlation matrix $C = X^T X$.
- Perform SVD or eigenvalue decomposition to find eigenvectors and eigenvalues.
- Select the top $N$ eigenmodes with the largest eigenvalues to form the reduced basis $\{\xi_i\}_{i=1}^N$.

**Step D: Galerkin Projection**:

Insert the reduced basis into the PDE (weak) formulation to derive reduced operators. Precompute:

$$
A^r(\mu) = B^T A^{\mu} B, \quad f^r(\mu) = B^T f^\mu
$$

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

Start with an empty basis. Iteratively add the snapshot that maximizes the error (predicted by a posteriori error estimators) until a desired accuracy is met.\
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

## Purpose in CFD

ROM replaces expensive full-order CFD solves with low-dimensional approximations. This note gives a complete overview of the ROM workflow: collect high-fidelity snapshots, build a POD basis, project the governing equations (Galerkin projection), and evaluate the resulting ODE system online for new parameters. ROM is essential for design optimization, uncertainty quantification, and real-time control of fluid systems.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | High-fidelity CFD solver, parameter set $\mathcal{P}$, snapshots $\{u_h(\mu_i)\}$, reduction method (POD/greedy), error tolerance |
| **Outputs** | Reduced basis $\{\zeta_n\}_{n=1}^N$, reduced system matrices, fast online evaluation $u_N(\mu)$ for new parameters, a posteriori error estimates |

## Related Scripts

- [POD Analysis for Flow Fields](../../../scripts/plots/pod_analysis_for_flow_fields/): performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode.
- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.
- [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](../../../scripts/algorithms/snapshot_pod/): computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one.

## Exercises

**Exercise 1.** One high-fidelity solve takes 2 hours. The offline phase uses $N_s = 50$ snapshots plus 1 hour for POD and operator assembly, and each online ROM query takes 1 second. After how many parameter queries does the ROM become cheaper in total than running the high-fidelity model for each query?

<details>
<summary>Answer</summary>

The offline cost is $50 \times 2 + 1 = 101$ h. Each query saves $2$ h $- 1$ s. The ROM wins when $q\,(2 - 1/3600) > 101$, i.e. $q > 50.5$, so from 51 queries onward. If the snapshots are also useful results in themselves, the break-even comes earlier.

</details>

**Exercise 2.** For $N_h = 10^6$ and $N = 20$, estimate the double-precision storage of the basis matrix $B \in \mathbb{R}^{N_h \times N}$ and of a reduced operator $A^r \in \mathbb{R}^{N \times N}$. If $A^\mu = \sum_{q=1}^{3}\Theta_q(\mu)A_q$ is affine, what must be stored for the online phase?

<details>
<summary>Answer</summary>

$B$: $10^6 \times 20 \times 8 = 1.6 \times 10^8$ bytes (160 MB). $A^r$: $400 \times 8 = 3.2$ kB. With affine dependence, store the three reduced matrices $B^T A_q B$ (9.6 kB in total), the reduced load vectors, and the functions $\Theta_q$. Online, assemble $A^r(\mu) = \sum_q \Theta_q(\mu)\,B^T A_q B$ without touching any $N_h$-sized object. $B$ itself is needed only to reconstruct full fields.

</details>

**Exercise 3.** Apply Step D to the system

$$
A = \begin{pmatrix} 4 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 4 \end{pmatrix}, \qquad f = (1, 2, 1)^T
$$

with the orthonormal basis $B = [\,(1, 0, 1)^T/\sqrt{2},\ (0, 1, 0)^T\,]$. Compute $A^r = B^T A B$ and $f^r = B^T f$, solve for $u_N$, and compare $B u_N$ with the truth $A^{-1}f$.

<details>
<summary>Answer</summary>

$A b_1 = (4, -2, 4)^T/\sqrt{2}$ and $A b_2 = (-1, 4, -1)^T$, so

$$
A^r = \begin{pmatrix} 4 & -\sqrt{2} \\ -\sqrt{2} & 4 \end{pmatrix}, \qquad f^r = \begin{pmatrix} \sqrt{2} \\ 2 \end{pmatrix}
$$

Solving gives $u_N = (3\sqrt{2}/7, 5/7) \approx (0.6061, 0.7143)$, so $B u_N = (3/7, 5/7, 3/7) \approx (0.4286, 0.7143, 0.4286)$. This equals $A^{-1}f$, as you can check: $4 \cdot 3/7 - 5/7 = 1$ and $-3/7 + 20/7 - 3/7 = 2$. The ROM is exact because the truth solution is symmetric and $B$ spans all symmetric vectors.

</details>

**Exercise 4.** Greedy algorithms need a cheap error estimator. For a symmetric positive definite $A(\mu)$, show that the error $e = u_h - u_{\text{RB}}$ satisfies $\|e\|_2 \le \|r\|_2/\alpha(\mu)$, where $r = f - A u_{\text{RB}}$ and $\alpha(\mu) = \lambda_{\min}(A(\mu))$. Evaluate the bound and the true error for $A = \text{tridiag}(-1, 2, -1) + I$ (size $3 \times 3$), $f = (1, 1, 1)^T$ and the one-vector reduced solution $u_{\text{RB}} = (0.6, 0.6, 0.6)^T$.

<details>
<summary>Answer</summary>

$Ae = r$, so $\alpha\|e\|^2 \le e^T A e = e^T r \le \|e\|\,\|r\|$, which gives $\|e\| \le \|r\|/\alpha$.

Numbers: $r = (1,1,1) - A(0.6, 0.6, 0.6) = (-0.2, 0.4, -0.2)$, so $\|r\| = \sqrt{0.24} \approx 0.490$. The smallest eigenvalue is $\alpha = 3 - \sqrt{2} \approx 1.586$, giving a bound of $0.309$. The truth is $(4/7, 5/7, 4/7)$, and the true error is $0.121$. The effectivity (bound divided by true error) is about 2.5. The bound needs only an $N_h$-sized residual (or, with affine precomputation, an $N$-sized computation) plus a lower bound for $\alpha$, not a new truth solve.

</details>

## References

- P. Benner, S. Gugercin and K. Willcox, "A survey of projection-based model reduction methods for parametric dynamical systems", *SIAM Review* 57(4), 2015.
- J. S. Hesthaven, G. Rozza and B. Stamm, *Certified Reduced Basis Methods for Parametrized Partial Differential Equations*, Springer, 2016.
- A. Quarteroni, A. Manzoni and F. Negri, *Reduced Basis Methods for Partial Differential Equations: An Introduction*, Springer, 2016.
- S. Chaturantabut and D. C. Sorensen, "Nonlinear model reduction via discrete empirical interpolation", *SIAM Journal on Scientific Computing* 32(5), 2010.
