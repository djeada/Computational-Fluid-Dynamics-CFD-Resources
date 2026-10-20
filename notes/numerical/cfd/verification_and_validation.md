# Verification and Validation

A CFD result is useful only if its error is known. Verification asks whether the equations are solved correctly: whether the code is free of mistakes that affect the solution, and how large the numerical error of a particular solution is. Validation asks whether the right equations are solved: how well the mathematical model, with its turbulence model, boundary conditions and simplifications, represents the real flow. This note describes the standard procedures for both, the method of manufactured solutions, Richardson extrapolation and the grid convergence index, and the comparison with experiments defined in ASME V\&V 20, and shows how they combine into an argument for the credibility of a prediction. It comes after a solver has been written or chosen and before its results are used for decisions.

## Problem Statement

Let $D$ be a measured value of a quantity of interest (a drag coefficient, a pressure drop, a reattachment length), $S$ the value predicted by a simulation and $T$ the unknown true value. Following ASME V\&V 20-2009, the comparison error

$$
E = S - D = (S - T) - (D - T) = \delta_{\mathrm{model}} + \delta_{\mathrm{num}} +
\delta_{\mathrm{input}} - \delta_D
$$

is the sum of the modelling error, the numerical error (discretization, iterative and round-off), the error from uncertain simulation inputs (geometry, boundary values, properties) and the experimental error. Only $E$ is known; the others must be estimated or bounded separately.

Three questions follow, and they must be answered in order:

1. Code verification: does the code solve its equations correctly, with the formal order of accuracy of its discretization?
2. Solution verification: how large is $\delta_{\mathrm{num}}$ for this particular calculation?
3. Validation: given estimates of $\delta_{\mathrm{num}}$, $\delta_{\mathrm{input}}$ and $\delta_D$, what does $E$ say about $\delta_{\mathrm{model}}$, and is it acceptable for the intended use?

The difficulty is that errors can cancel. A coarse mesh, a coding mistake and an inadequate turbulence model can combine to give good agreement with one experiment and a poor prediction for the next design. Agreement with data is evidence of credibility only when the numerical error has been shown to be small by verification.

## Overview of the Three Activities

| Activity | Question | Reference | Typical evidence |
| --- | --- | --- | --- |
| Code verification | Is the code a correct implementation of the discrete equations? | Exact solutions of the model equations, often manufactured | Observed order of accuracy equal to the formal order on a sequence of grids |
| Solution verification | How large is the numerical error of this solution? | The solution itself on refined grids and tightened tolerances | Iterative convergence history; Richardson extrapolation; GCI |
| Validation | How accurate is the model for this flow? | Experimental data with stated uncertainty | Comparison error $E$ against the validation uncertainty $u_{\mathrm{val}}$; validation metrics |

Verification is a mathematical exercise and can be completed; validation is a physical one and is always limited to the conditions tested.

## Code Verification

### The Order-of-Accuracy Test

For a discretization of formal order $p_f$, the discretization error on a grid of spacing $h$ in the asymptotic range is

$$
e_h = \lVert \phi_h - \phi \rVert \approx C h^{p_f}
$$

in a chosen norm, typically the discrete $L_2$ norm $`(\frac{1}{N}\sum_i (\phi_{h,i} - \phi(\mathbf{x}_i))^2)^{1/2}`$ and the maximum norm $`L_\infty`$. On grids refined by a constant ratio $r$ the observed order is

$$
p = \frac{\ln(e_{rh}/e_h)}{\ln r}
$$

The code passes when $p$ approaches $p_f$ as $h \to 0$, in every norm and for every variable. This is the most demanding test available: an error in a coefficient, a sign, an index or a boundary treatment almost always lowers $p$ or stops convergence altogether, even when the solution looks plausible. Agreement of the solution with an exact one on a single grid, by contrast, proves little. Roache (2002) and Oberkampf and Roy (2010) treat the order-of-accuracy test as the acceptance criterion for code verification.

### The Method of Manufactured Solutions

The order-of-accuracy test needs exact solutions, and exact solutions of the Navier–Stokes equations on general domains do not exist. The method of manufactured solutions (MMS) turns the problem around: choose the solution first and change the problem to fit it. For an equation $\mathcal{L}(\phi) = 0$:

1. Choose a manufactured solution $\phi_m(\mathbf{x}, t)$. It should be smooth, exercise every term of the equations (so all its relevant derivatives are non-zero and of comparable size), be non-trivial on every boundary, and not be representable exactly by the scheme (a quadratic is differentiated exactly by second-order differences and would hide errors). Trigonometric and exponential functions are standard choices. It need not be physically realistic, but it should respect constraints the code relies on, such as positive density or turbulent kinetic energy.
2. Apply the continuous operator to it to obtain the source term $f = \mathcal{L}(\phi_m)$, usually with computer algebra.
3. Derive the boundary and initial data from $\phi_m$: Dirichlet values, normal derivatives or fluxes on each boundary type to be tested.
4. Solve $\mathcal{L}(\phi) = f$ with that data on at least four systematically refined grids, with iterative errors driven to near round-off.
5. Compute the error norms against $\phi_m$ and the observed order between grids, and compare with the formal order.

Because the source term is added through the code's normal source-term input, the method requires only that the code accept an arbitrary source; the rest of the code is used as it is. Roache (2002) describes the method and its history, Salari and Knupp (2000) set out the procedure in detail for a Navier–Stokes code and demonstrated it on deliberately introduced coding mistakes, and Oberkampf and Roy (2010) give manufactured solutions for the compressible Navier–Stokes and RANS equations.

MMS verifies only what it exercises. Every boundary-condition type, every term, every mesh type (including skewed and stretched cells, on which many mistakes only appear) and every option used in production needs to be covered by some test. MMS does not test whether the equations are the right ones; that is validation.

### Example: Detecting a Boundary-Treatment Mistake

The figure applies the method to a five-point finite-difference solver for $-\nabla^2\phi = f$ on the unit square with Dirichlet conditions on three sides and a Neumann condition $\partial\phi/\partial x = g$ on $x = 1$. The manufactured solution is $\phi_m = e^{x/2}\sin(\pi y + 0.4) + \tfrac{1}{4}\cos(1.25\pi x)$. The correct solver imposes the Neumann condition with a ghost node; the second solver is identical except that it uses the one-sided difference $(\phi_{N,j} - \phi_{N-1,j})/h = g_j$, a common mistake that is only first order.

![Manufactured solution, error fields of the correct and the bugged solver, and error against grid spacing](../../../scripts/algorithms/method_of_manufactured_solutions/method_of_manufactured_solutions.png)

The correct solver gives an observed order of 1.98 to 2.00 in both norms on grids from $8 \times 8$ to $256 \times 256$. The bugged one gives 1.33, 1.19, 1.11, 1.06 and 1.03. Its error field (panel c) peaks at the Neumann boundary but spreads through the whole domain, so a plot of the solution would not reveal the mistake. Note also that on the two coarsest pairs of grids the bugged solver appears to converge at better than first order: an order-of-accuracy test needs enough grids to reach the asymptotic range.

## Solution Verification

Code verification shows that the code can be accurate; solution verification estimates the actual numerical error of a given calculation, whose exact solution is unknown. The numerical error has three parts, which should be estimated in the order below and kept well apart in size.

### Round-Off and Iterative Error

Round-off error is normally negligible in double precision but can grow on very fine or highly stretched meshes. Iterative error is the difference between the current iterate and the exact solution of the discrete equations. It is monitored through the residuals and, more usefully, through the quantities of interest; it should be reduced to at most a tenth, preferably a hundredth, of the discretization error so that it does not contaminate the grid study ([Iterative Convergence](./iterative_convergence.md)).

### Discretization Error by Richardson Extrapolation

In the asymptotic range the solution on a grid of representative spacing $h$ behaves as $\phi_h = \phi_{\mathrm{exact}} + C h^p + O(h^{p+1})$. With solutions $\phi_1$, $\phi_2$, $\phi_3$ on fine, medium and coarse grids of spacing $h_1 < h_2 < h_3$ and a constant refinement ratio $r = h_2/h_1 = h_3/h_2$, the unknowns $C$, $p$ and $\phi_{\mathrm{exact}}$ can be eliminated:

$$
p = \frac{\ln\left(\dfrac{\phi_3 - \phi_2}{\phi_2 - \phi_1}\right)}{\ln r},
\qquad \phi_{\mathrm{ext}} = \phi_1 + \frac{\phi_1 - \phi_2}{r^p - 1}
$$

The extrapolated value $\phi_{\mathrm{ext}}$ estimates the grid-independent solution, and $\phi_1 - \phi_{\mathrm{ext}}$ estimates the discretization error of the fine grid. For unstructured meshes $h = (V/N_{\mathrm{cells}})^{1/3}$ in 3D, and when the ratios differ the observed order is found by fixed-point iteration (Celik et al. 2008), as implemented in the [Grid Convergence Index](../../../scripts/algorithms/grid_convergence_index/) script and described in [Generating CFD Training Data](../../machine_learning/automotive_aerodynamics/generating_cfd_datasets.md).

The estimate is reliable only in the asymptotic range. Warning signs are an observed order far from the formal one, a negative ratio $(\phi_3 - \phi_2)/(\phi_2 - \phi_1)$ (oscillatory convergence), and values of $p$ that change when a fourth grid is added. Grids must be refined systematically: the same topology and the same relative distribution of cells, with the whole mesh refined rather than selected regions.

### The Grid Convergence Index

Roache (1994) proposed the grid convergence index (GCI) to report the result of a grid study as an uncertainty band, in analogy with experimental uncertainties:

$$
\mathrm{GCI}_{\mathrm{fine}} = \frac{F_s}{r^p - 1}\left|
\frac{\phi_1 - \phi_2}{\phi_1}\right|
$$

with a safety factor $F_s = 1.25$ when three or more grids determine $p$ and $F_s = 3$ when only two grids are available and $p$ is assumed. It is intended to contain the exact solution with about 95% confidence. The procedure recommended by Celik et al. (2008) for the editorial policy of the *Journal of Fluids Engineering* is:

1. Compute the representative cell size $h$ of three meshes, with refinement ratios preferably above 1.3.
2. Compute the quantity of interest $\phi$ on each, with negligible iterative error.
3. Compute the observed order $p$, iteratively if the ratios differ.
4. Compute $\phi_{\mathrm{ext}}$, the approximate relative error $e_a = |(\phi_1 - \phi_2)/\phi_1|$, the extrapolated relative error $e_{\mathrm{ext}} = |(\phi_{\mathrm{ext}} - \phi_1)/\phi_{\mathrm{ext}}|$ and the GCI.
5. Report all of them, together with $p$ and whether convergence was monotonic.

For a 1D advection–diffusion problem with a known answer, the [Grid Convergence Index](../../../scripts/algorithms/grid_convergence_index/) script obtains on 16, 32 and 64 cells $p = 1.56$ for a second-order scheme (the boundary layer is only just resolved) and a GCI of 0.84%, while the true error of the fine grid is 0.53%. The GCI band contains the exact value even though the grids are not fully asymptotic, and the extrapolated value is in error by only 0.14%.

Some situations defeat the procedure. Limiters and switches in high-resolution schemes, wall functions whose behaviour changes with $y^+$, and adaptive meshes make the error a non-smooth function of $h$. In LES the filter width is tied to the grid, so refinement changes the model as well as the discretization. The time step must be refined in the same way for unsteady calculations.

## Validation

### Validation Experiments

Experiments carried out to discover physics seldom record everything a simulation needs. A validation experiment is designed jointly with the simulation: geometry as built, inflow profiles and turbulence levels, wall temperatures and all other boundary conditions are measured, with uncertainties, and the quantities compared are those the model is meant to predict (Oberkampf and Roy 2010). Complex systems are validated through a hierarchy of experiments of decreasing complexity: unit problems that isolate one phenomenon (a flat-plate boundary layer, a backward-facing step), benchmark cases that couple a few phenomena, subsystems, and finally the complete system, for which data are scarce and uncertain.

### Comparison Error and Validation Uncertainty

ASME V\&V 20-2009 combines the standard uncertainties of the three known contributions into a validation uncertainty

$$
u_{\mathrm{val}} = \sqrt{u_{\mathrm{num}}^2 + u_{\mathrm{input}}^2 + u_D^2}
$$

assuming the contributions are independent. The modelling error then lies in the interval $\delta_{\mathrm{model}} \in [E - k u_{\mathrm{val}}, E + k u_{\mathrm{val}}]$, with a coverage factor $k \approx 2$ for about 95% confidence when the errors are approximately normal. If $|E| \gg u_{\mathrm{val}}$, the model error is approximately $E$ and the model should be improved. If $|E| \lesssim u_{\mathrm{val}}$, the model error is hidden in the noise of the validation process, and reducing it further requires better experiments or better numerics, not a better model. Here $u_{\mathrm{num}}$ comes from solution verification, $u_{\mathrm{input}}$ from propagating the uncertainty of the simulation inputs (by sensitivity coefficients or sampling), and $u_D$ from the experimental uncertainty analysis.

### Validation Metrics

A validation metric is a quantitative measure of the difference between simulation and experiment that accounts for uncertainty. Simple choices are the pointwise relative difference $(S - D)/D$ along a profile or the root-mean-square difference over many points, each compared with the combined uncertainty. When the experiment is repeated, the confidence-interval metric of Oberkampf and Barone (2006) estimates the model error as the difference between the simulation and the mean of the measurements, with a confidence interval from Student's $t$ distribution of the measurements. When both simulation and experiment are described by probability distributions, the area metric is the area between their cumulative distribution functions, which has the units of the quantity and is zero only when the distributions agree. The choice of metric and of the acceptable level is set by the intended use, not by the validation itself.

Validation establishes accuracy only at the conditions tested. Prediction for a new geometry or Reynolds number is an extrapolation from the validation domain, and its uncertainty grows with the distance from it.

## Credibility Hierarchy

The activities build on one another, and each level is meaningful only if the levels below it have been established:

1. Software quality assurance: version control, regression tests and documented inputs ensure that results can be reproduced.
2. Code verification: the observed order of accuracy matches the formal order for every term, boundary condition and mesh type used.
3. Solution verification: iterative error is negligible and the discretization error of each production calculation is estimated, for example as a GCI.
4. Validation: the model error is quantified against experiments relevant to the application, with $u_{\mathrm{val}}$ known.
5. Prediction: results are used for conditions where no data exist, with an uncertainty that accounts for extrapolation from the validation domain.

Skipping a level is common and dangerous. Tuning a turbulence-model constant to match an experiment on an unverified, under-resolved mesh calibrates the sum of the modelling and numerical errors, and that sum changes when the mesh or the geometry changes.

## Key Takeaways

- Verification is about solving the equations right, validation about solving the right equations; verification comes first.
- The order-of-accuracy test is the most demanding code-verification test: the observed order must approach the formal order on several systematically refined grids.
- The method of manufactured solutions provides exact solutions for any equation by adding a source term; it verifies only the terms, boundary conditions and mesh types it exercises.
- Richardson extrapolation and the GCI estimate the discretization error of a particular solution from three grids, provided they are in the asymptotic range.
- ASME V\&V 20 compares the comparison error $E = S - D$ with the validation uncertainty $u_{\mathrm{val}}$ to bound the modelling error.
- Credibility is built bottom-up, from code verification through solution verification and validation to prediction.

## Related Scripts

- [Method of Manufactured Solutions](../../../scripts/algorithms/method_of_manufactured_solutions/): verifies a second-order finite-difference Poisson solver with the method of manufactured solutions (MMS) and shows how the same test exposes a first-order boundary treatment.
- [Grid Convergence Index](../../../scripts/algorithms/grid_convergence_index/): estimates discretization error from three meshes with Richardson extrapolation and the grid convergence index (GCI), following the procedure of Celik et al. (2008).
- [Ghost-Cell Boundary Conditions](../../../scripts/algorithms/ghost_cell_boundary_conditions/): compares first-order and second-order ways of imposing Neumann and Robin boundary conditions in finite-difference and finite-volume discretizations of a 1D diffusion problem.
- [Continuous vs Discrete Domain](../../../scripts/plots/continuous_vs_discrete_domain/): illustrates the central step of CFD, replacing a field defined at every point of a continuous domain by values stored at a finite set of grid points, and measures the error this introduces for the model problem $du/dx + u = 0$, $u(0) = 1$.

## Exercises

**Exercise 1.** An MMS test of a solver whose formal order is 2 gives $L_2$ errors $2.121 \times 10^{-3}$, $5.348 \times 10^{-4}$ and $1.343 \times 10^{-4}$ on grids with $h = 1/16$, $1/32$ and $1/64$. Compute the observed orders. Does the code pass?

<details>
<summary>Answer</summary>

$p = \log_2(2.121/0.5348) = 1.99$ and $p = \log_2(5.348/1.343) = 1.99$.

Both approach the formal order 2, so this test is passed. The conclusion is limited to the terms, boundary conditions and grid types exercised by the manufactured solution.

</details>

**Exercise 2.** A second solver gives $L_2$ errors of $1.419 \times 10^{-2}$, $6.207 \times 10^{-3}$, $2.885 \times 10^{-3}$ and $1.389 \times 10^{-3}$ on $h = 1/16$ to $1/128$ for the same manufactured solution. Compute the observed orders. What do they suggest, and how would you locate the mistake?

<details>
<summary>Answer</summary>

$p = 1.19$, $1.11$ and $1.05$: the order tends to 1, not 2. The solution converges, so the equations are consistent, but some part of the discretization is only first order.

Since a first-order error at a boundary pollutes the whole field, the error field alone may not locate it. Repeating the test with Dirichlet conditions on every side isolates the boundary treatments: if the order returns to 2, one of the derivative boundary conditions is first order (this is the bugged solver of the example). A manufactured solution that makes one term zero at a time isolates the interior terms in the same way.

</details>

**Exercise 3.** A pressure drop is computed on three meshes with refinement ratio $r = 2$: 105.2 Pa (coarse), 101.6 Pa (medium) and 100.7 Pa (fine). Compute the observed order, the extrapolated value and the fine-grid GCI, and state the result with its uncertainty.

<details>
<summary>Answer</summary>

$p = \ln(3.6/0.9)/\ln 2 = \ln 4/\ln 2 = 2.00$.

$\phi_{\mathrm{ext}} = 100.7 + (100.7 - 101.6)/(2^2 - 1) = 100.7 - 0.3 = 100.4$ Pa.

$`e_a = 0.9/100.7 = 0.894\%`$ and $`\mathrm{GCI}_{\mathrm{fine}} = 1.25 \times 0.894\%/3 = 0.372\%`$, which is $\pm 0.37$ Pa.

The result is $\Delta p = 100.7 \pm 0.4$ Pa (about 95% confidence for the discretization error alone). The observed order equals the formal order of a second-order scheme, which supports the assumption that the meshes are in the asymptotic range.

</details>

**Exercise 4.** Another study gives $C_d = 0.330$, $0.322$ and $0.325$ on the coarse, medium and fine meshes. Can the GCI procedure be applied? What should be done?

<details>
<summary>Answer</summary>

$(\phi_3 - \phi_2)/(\phi_2 - \phi_1) = (0.322 - 0.330)/(0.325 - 0.322) = -0.008/0.003 < 0$: the convergence is oscillatory. The formula for $p$ requires the logarithm of a positive number, and Richardson extrapolation assumes monotonic convergence, so the standard procedure does not apply.

Causes include grids outside the asymptotic range, limiters switching, changes in the flow topology (a separation point moving between cells) or incomplete iterative convergence. Check the iterative convergence first, then add a finer grid. If the oscillation persists, a cautious alternative is to report the spread of the values, here $0.330 - 0.322 = 0.008$, as the discretization uncertainty rather than an extrapolated error.

</details>

**Exercise 5.** A simulation predicts $C_d = 0.320$; the wind tunnel gives $D = 0.310$. The standard uncertainties are $u_{\mathrm{num}} = 0.003$, $u_{\mathrm{input}} = 0.002$ and $u_D = 0.003$. Following ASME V\&V 20, estimate the interval containing the modelling error with about 95% confidence. Is the model error significant?

<details>
<summary>Answer</summary>

$E = 0.320 - 0.310 = 0.010$.

$u_{\mathrm{val}} = \sqrt{0.003^2 + 0.002^2 + 0.003^2} = 0.0047$.

With $k = 2$: $\delta_{\mathrm{model}} \in [0.010 - 0.0094, 0.010 + 0.0094] = [0.0006, 0.0194]$.

The interval just excludes zero, so the model overpredicts the drag by between about 0.2% and 6% of $D$ at 95% confidence. The evidence is marginal: reducing $u_{\mathrm{num}}$ and $u_D$ would sharpen it before the turbulence model is blamed.

</details>

## References

- ASME, *Standard for Verification and Validation in Computational Fluid Dynamics and Heat Transfer*, ASME V\&V 20-2009, American Society of Mechanical Engineers, 2009.
- Roache, P. J., "Perspective: a method for uniform reporting of grid refinement studies," *Journal of Fluids Engineering*, 116(3), 405–413, 1994.
- Roache, P. J., *Verification and Validation in Computational Science and Engineering*, Hermosa Publishers, 1998.
- Roache, P. J., "Code verification by the method of manufactured solutions," *Journal of Fluids Engineering*, 124(1), 4–10, 2002.
- Salari, K., & Knupp, P., *Code Verification by the Method of Manufactured Solutions*, Sandia National Laboratories Report SAND2000-1444, 2000.
- Celik, I. B., Ghia, U., Roache, P. J., Freitas, C. J., Coleman, H., & Raad, P. E., "Procedure for estimation and reporting of uncertainty due to discretization in CFD applications," *Journal of Fluids Engineering*, 130(7), 078001, 2008.
- Oberkampf, W. L., & Roy, C. J., *Verification and Validation in Scientific Computing*, Cambridge University Press, 2010.
- Oberkampf, W. L., & Barone, M. F., "Measures of agreement between computation and experiment: validation metrics," *Journal of Computational Physics*, 217(1), 5–36, 2006.
- AIAA, *Guide for the Verification and Validation of Computational Fluid Dynamics Simulations*, AIAA G-077-1998, American Institute of Aeronautics and Astronautics, 1998.
