# Reduced Basis Approximation

The reduced basis (RB) method builds a reduced-order model of a parametrized PDE from a few truth solutions, solves a Galerkin problem of size $N$ in their span, and certifies every online answer with a computable bound on its error. For linear, affinely parametrized, coercive problems the whole procedure runs online at a cost independent of the truth dimension. This note covers the solution manifold, the construction of the reduced space by POD or by a weak greedy algorithm, the offline–online decomposition, residual-based error and output bounds, and the convergence that makes the method work. It builds on [Parametrized Variational Problems](parameterized_variational_problems.md) and [Truth Discretization](discretization_techniques.md); the general context is in [Reduced-Order Modeling](rom.md).

## Problem Statement

The truth model is the affinely parametrized linear system

```math
A_h(\mu)\,\mathbf{u}_h(\mu) = \mathbf{f}_h(\mu), \qquad A_h(\mu) = \sum_{q=1}^{Q_a}\theta_q^a(\mu)A_q, \qquad \mathbf{f}_h(\mu) = \sum_{q=1}^{Q_f}\theta_q^f(\mu)\mathbf{f}_q, \qquad \mu \in \mathcal{P}
```

with $\mathbf{u}_h \in \mathbb{R}^{N_h}$, coercive with constant $\alpha_h(\mu)$ in the norm $`\lVert \mathbf{v} \rVert_X = \sqrt{\mathbf{v}^TX\mathbf{v}}`$ of the inner-product matrix $X$, and an output $s_h(\mu) = \boldsymbol{\ell}^T\mathbf{u}_h(\mu)$. The task is to find a reduced space $V_N = \mathrm{span}(Z) \subset \mathbb{R}^{N_h}$, $Z \in \mathbb{R}^{N_h \times N}$, a reduced solution $\mathbf{u}_N(\mu) \in V_N$ and an error bound $\Delta_N(\mu)$ with

```math
\lVert \mathbf{u}_h(\mu) - \mathbf{u}_N(\mu) \rVert_X \le \Delta_N(\mu) \quad \text{for every } \mu \in \mathcal{P},
\qquad
\max_{\mu \in \Xi_{\mathrm{train}}} \Delta_N(\mu) \le \varepsilon_{\mathrm{tol}}
```

over a training set $`\Xi_{\mathrm{train}} \subset \mathcal{P}`$, where computing $\mathbf{u}_N(\mu)$ and $\Delta_N(\mu)$ costs a number of operations that depends on $N$ and $Q$ but not on $N_h$. The difficulties are to choose $V_N$ from a finite sample with few truth solves, to bound the error rigorously without knowing $\mathbf{u}_h$, which requires a lower bound of the coercivity constant, and to evaluate that bound accurately when it becomes small.

## Solution Manifold

The set of all truth solutions,

```math
\mathcal{M}_h = \{\mathbf{u}_h(\mu) : \mu \in \mathcal{P}\} \subset \mathbb{R}^{N_h}
```

is the image of the $p$-dimensional parameter set under the solution map, a curved $p$-dimensional manifold in a space of dimension $N_h$. A linear reduced space can approximate it well only if it lies close to a low-dimensional subspace, which the Kolmogorov $n$-width $d_N(\mathcal{M}_h)$ measures: it is the smallest worst-case error achievable by any $N$-dimensional subspace ([Reduced-Order Modeling](rom.md)). When the solution depends smoothly (analytically) on $\mu$, as for diffusion problems with coefficients bounded away from zero, $d_N$ decays exponentially and a few tens of basis functions reach engineering accuracy. When the solution has features that move with $\mu$, it decays slowly and the RB method in its linear form is not the right tool.

Error bounds are taken with respect to the truth $\mathbf{u}_h$, not the exact solution. The truth error must be made negligible separately by the choice of mesh ([Truth Discretization](discretization_techniques.md)).

## Reduced Galerkin Problem

Given an $X$-orthonormal basis $Z$ ($Z^TXZ = I$), the reduced solution is $\mathbf{u}_N(\mu) = Z\mathbf{u}_r(\mu)$ with

```math
A_N(\mu)\,\mathbf{u}_r(\mu) = \mathbf{f}_N(\mu),
\qquad A_N(\mu) = \sum_q\theta_q^a(\mu)\, Z^TA_qZ,
\qquad \mathbf{f}_N(\mu) = \sum_q\theta_q^f(\mu)\, Z^T\mathbf{f}_q
```

Céa's lemma holds in the reduced space with the truth constants, $`\lVert \mathbf{u}_h - \mathbf{u}_N \rVert_X \le (\gamma_h/\alpha_h)\min_{\mathbf{v} \in V_N}\lVert \mathbf{u}_h - \mathbf{v} \rVert_X`$, and for symmetric $A_h$ the reduced solution is the best approximation in the energy norm $`\lVert \cdot \rVert_{A_h(\mu)}`$ (Exercise 4). The basis must be orthonormalized: raw snapshots become nearly collinear as $N$ grows, and $A_N$ built from them is ill-conditioned, whereas with $X$-orthonormal $Z$ the condition number of $A_N$ is bounded by $\gamma_h/\alpha_h$.

## Constructing the Reduced Space

### POD

Proper orthogonal decomposition computes truth solutions at all $N_{\mathrm{train}}$ training parameters and takes the leading $N$ left singular vectors of the snapshot matrix $`S = [\mathbf{u}_h(\mu_1), \dots, \mathbf{u}_h(\mu_{N_{\mathrm{train}}})]`$, computed in the $X$ inner product. The resulting space minimizes the mean squared projection error over the snapshots,

```math
\frac{1}{N_{\mathrm{train}}}\sum_{j=1}^{N_{\mathrm{train}}}\left\lVert \mathbf{u}_h(\mu_j) - \Pi_N\mathbf{u}_h(\mu_j) \right\rVert_X^2 = \frac{1}{N_{\mathrm{train}}}\sum_{k > N}\sigma_k^2
```

where $\Pi_N$ is the $X$-orthogonal projection and $\sigma_k$ are the singular values ([POD Introduction](../pod/pod_intro.md), [POD and SVD](../pod/pod_vs_svd.md)). POD needs every training snapshot, so its offline cost is $N_{\mathrm{train}}$ truth solves. It is the natural choice for time-dependent problems, where each solve produces many snapshots anyway, and for one or two parameters.

### Weak Greedy Algorithm

The greedy algorithm (Veroy, Prud'homme, Rovas and Patera 2003) builds the space one truth solve at a time, always adding the solution at the parameter where the current reduced model is worst according to the error bound:

1. Choose a training set $`\Xi_{\mathrm{train}}`$, a tolerance $\varepsilon_{\mathrm{tol}}$, a maximum size $N_{\max}$ and a first parameter $\mu^{(1)}$. Set $N = 1$.
2. Solve the truth problem at $\mu^{(N)}$, orthonormalize $\mathbf{u}_h(\mu^{(N)})$ against the current basis in the $X$ product (twice, for numerical orthogonality), and append it to $Z$.
3. Update the offline data: the reduced matrices $Z^TA_qZ$, $Z^T\mathbf{f}_q$ and the data of the error bound.
4. Evaluate $\Delta_N(\mu)$, or the relative bound $`\Delta_N(\mu)/\lVert \mathbf{u}_N(\mu) \rVert_X`$, at every $`\mu \in \Xi_{\mathrm{train}}`$ by the online procedure.
5. If $`\max_{\Xi_{\mathrm{train}}}\Delta_N < \varepsilon_{\mathrm{tol}}`$ or $N = N_{\max}$, stop. Otherwise set $`\mu^{(N+1)} = \arg\max_{\Xi_{\mathrm{train}}}\Delta_N(\mu)`$, increase $N$ and go to step 2.

The algorithm is called weak because it maximizes the bound rather than the true error, which would need a truth solve at every training point (the strong greedy). Since $\Delta_N$ is within the effectivity factor of the true error, the weak greedy selects a parameter whose error is within that factor of the largest. It needs only $N$ truth solves, can use training sets of $10^3$ to $10^5$ points, and stops with a certificate on the training set. Binev et al. (2011) and Buffa et al. (2012) proved that it is rate-optimal: if $d_N$ decays exponentially or algebraically, so does the greedy error, with modified constants.

|  | POD | Weak greedy |
| --- | --- | --- |
| Truth solves offline | $N_{\mathrm{train}}$ | $N$ |
| Optimality | mean-square over the snapshots | worst case, up to the effectivity factor, rate-optimal |
| Needs an error estimator | no | yes |
| Typical use | time-dependent problems, few parameters | many parameters, steady problems; POD-greedy in time-dependent problems |

For time-dependent problems the two are combined in the POD-greedy algorithm (Haasdonk and Ohlberger 2008): the greedy loop selects a parameter, and the new trajectory is compressed by POD after its projection onto the current space has been subtracted.

## Offline–Online Decomposition

With affine dependence every quantity needed online splits into parameter-independent pieces computed once and parameter-dependent coefficients evaluated at each query.

| Stage | Computation | Cost |
| --- | --- | --- |
| Offline | $N$ truth solves; orthonormalization; $Z^TA_qZ$ and $Z^T\mathbf{f}_q$; Riesz representers $X^{-1}\mathbf{f}_q$ and $X^{-1}A_q\mathbf{z}_n$ and their inner products | depends on $N_h$ |
| Online, solution | evaluate $\theta_q(\mu)$; assemble $A_N(\mu)$ and $\mathbf{f}_N(\mu)$; solve | $O(Q_aN^2 + N^3)$ |
| Online, output | $s_N = \boldsymbol{\ell}_N^T\mathbf{u}_r$ with $\boldsymbol{\ell}_N = Z^T\boldsymbol{\ell}$ precomputed | $O(N)$ |
| Online, error bound | dual norm of the residual from precomputed inner products; $\alpha_{\mathrm{LB}}(\mu)$ | $O((Q_f + Q_aN)^2)$ |

The full field $Z\mathbf{u}_r$ is formed only when it is needed for visualization, at a cost of $O(N_hN)$.

## A Posteriori Error Bounds

### Error Equation

The residual of the reduced solution is $\mathbf{r}(\mu) = \mathbf{f}_h(\mu) - A_h(\mu)\mathbf{u}_N(\mu)$, and the error $\mathbf{e} = \mathbf{u}_h - \mathbf{u}_N$ satisfies the error equation $A_h(\mu)\mathbf{e} = \mathbf{r}(\mu)$. The residual's dual norm is the $X$-norm of its Riesz representer $\hat{\mathbf{e}} = X^{-1}\mathbf{r}$,

```math
\lVert \mathbf{r} \rVert_{X'} = \sup_{\mathbf{v} \ne \mathbf{0}}\frac{\mathbf{v}^T\mathbf{r}}{\lVert \mathbf{v} \rVert_X} = \sqrt{\mathbf{r}^TX^{-1}\mathbf{r}} = \lVert \hat{\mathbf{e}} \rVert_X
```

### Energy-Norm and Output Bounds

Let $\alpha_{\mathrm{LB}}(\mu) \le \alpha_h(\mu)$ be a computable lower bound of the coercivity constant. Testing the error equation with $\mathbf{e}$ gives $`\alpha_h\lVert \mathbf{e} \rVert_X^2 \le \mathbf{e}^TA_h\mathbf{e} = \mathbf{e}^T\mathbf{r} \le \lVert \mathbf{r} \rVert_{X'}\lVert \mathbf{e} \rVert_X`$, so

$$
\lVert \mathbf{u}_h(\mu) - \mathbf{u}_N(\mu) \rVert_X \le
\Delta_N(\mu) = \frac{\lVert \mathbf{r}(\mu) \rVert_{X'}}{\alpha_{\mathrm{LB}}(\mu)}
$$

The quality of the bound is measured by its effectivity $`\eta_N(\mu) = \Delta_N(\mu)/\lVert \mathbf{e} \rVert_X`$. The bound is rigorous, $\eta_N \ge 1$, and it is sharp up to the condition number: from $`\lVert \mathbf{r} \rVert_{X'} = \lVert A_h\mathbf{e} \rVert_{X'} \le \gamma_h\lVert \mathbf{e} \rVert_X`$,

$$
1 \le \eta_N(\mu) \le \frac{\gamma_h(\mu)}{\alpha_{\mathrm{LB}}(\mu)}
$$

independent of $N$. For a compliant output ($A_h$ symmetric, $\boldsymbol{\ell} = \mathbf{f}_h$), Galerkin orthogonality gives $s_h - s_N = \mathbf{f}_h^T\mathbf{e} = \mathbf{e}^TA_h\mathbf{e} \ge 0$, so the reduced output is a lower bound and

$$
0 \le s_h(\mu) - s_N(\mu) \le
\Delta_N^s(\mu) = \frac{\lVert \mathbf{r}(\mu) \rVert_{X'}^2}{\alpha_{\mathrm{LB}}(\mu)}
$$

The output error converges like the square of the energy error. For a non-compliant output, a dual (adjoint) reduced problem for $\boldsymbol{\ell}$ is solved alongside the primal one; the output is corrected with the dual solution and the bound becomes the product of the primal and dual residual norms divided by $\alpha_{\mathrm{LB}}$, which keeps the squared convergence.

### Coercivity Lower Bound

If every $A_q$ is symmetric positive semi-definite, every $\theta_q(\mu) > 0$, and $X = \sum_q\theta_q(\bar{\mu})A_q$ is the energy matrix at a reference parameter $\bar{\mu}$, the problem is called parametrically coercive and

$$
\alpha_{\mathrm{LB}}(\mu) = \min_q \frac{\theta_q(\mu)}{\theta_q(\bar{\mu})}
$$

is a rigorous bound, free to evaluate (the thermal block is an example; see [Parametrized Variational Problems](parameterized_variational_problems.md)). In general, the successive constraint method (Huynh, Rozza, Sen and Patera 2007) computes $\alpha_{\mathrm{LB}}(\mu)$ online from a small linear program whose constraints come from generalized eigenvalue problems solved offline at selected parameters. A cheaper but non-rigorous alternative interpolates $\alpha_h(\mu)$ from offline eigenvalue computations.

### Evaluating the Dual Norm Online

By linearity the Riesz representer of the residual is

```math
X^{-1}\mathbf{r}(\mu) = \sum_{q=1}^{Q_f}\theta_q^f(\mu)\,X^{-1}\mathbf{f}_q - \sum_{q=1}^{Q_a}\sum_{n=1}^{N}\theta_q^a(\mu)\,(\mathbf{u}_r)_n\,X^{-1}A_q\mathbf{z}_n = W\mathbf{c}(\mu)
```

The $Q_f + Q_aN$ columns of $W$ are computed offline with one solve with $X$ each; the coefficient vector $\mathbf{c}(\mu)$ is formed online. The textbook formula $`\lVert \mathbf{r} \rVert_{X'}^2 = \mathbf{c}^T(W^TXW)\mathbf{c}`$ uses a precomputed Gram matrix and costs $O((Q_f + Q_aN)^2)$ online, but it computes a small number as the difference of large ones: once $`\lVert \mathbf{r} \rVert_{X'}/\lVert \mathbf{f} \rVert_{X'}`$ falls to about $\sqrt{\varepsilon_{\mathrm{mach}}} \approx 10^{-8}$, round-off dominates and the bound stalls or becomes meaningless. Factoring $W = OR$ with $X$-orthonormal $O$ offline and evaluating $`\lVert \mathbf{r} \rVert_{X'} = \lVert R\mathbf{c}(\mu) \rVert_2`$ online costs the same and is accurate to machine precision (Casenave, Ern and Lelièvre 2014 discuss this and other remedies).

## Example: The Thermal Block

The [thermal block script](../../../scripts/algorithms/reduced_basis_thermal_block/) applies the method to steady conduction in a unit square of $2 \times 2$ blocks with conductivities $(1, \mu_1, \mu_2, \mu_3)$, $\mu_i \in [0.1, 10]$, a unit flux on the bottom edge and $u = 0$ on the top edge, discretized by linear finite elements with $N_h = 4160$. The greedy runs on 1000 log-uniform training parameters with the min-theta bound $\alpha_{\mathrm{LB}} = \min(1, \mu_1, \mu_2, \mu_3)$ and the factored residual norm.

![Thermal block: truth solution, greedy decay of bound and error, effectivity and online cost](../../../scripts/algorithms/reduced_basis_thermal_block/reduced_basis_thermal_block.png)

Panel (b) shows the exponential decay: the largest relative bound over the training set falls from 32 at $N = 1$ to $1.6 \times 10^{-7}$ at $N = 25$, and the largest true error over 50 test parameters from 0.91 to $1.0 \times 10^{-8}$. The same bound evaluated with the Gram-matrix formula (grey) stalls near $10^{-6}$. Panel (c) shows the effectivity between 1.10 and 39, inside the guaranteed range $[1, 100]$, with a median of 2 to 4; the output bound has effectivity at least 1.12. Panel (d) shows that a certified online query (reduced solve and bound) at $N = 25$ takes about 0.024 ms, roughly 250 times faster than a truth assembly and sparse solve in this small 2D problem; the ratio grows with $N_h$.

## Practical Choices

- Sample the training set log-uniformly when parameters span orders of magnitude, and make it large enough that adding points no longer changes the selected parameters; the bound is certified only on the training set.
- Use the relative bound $`\Delta_N/\lVert \mathbf{u}_N \rVert_X`$ in the greedy when solution magnitudes vary strongly across $\mathcal{P}$.
- Start the greedy at the centre or a corner of $\mathcal{P}$; the choice has little influence after a few steps, and the greedy soon picks the corners, where the problem is hardest.
- Stop on the tolerance, and set $N_{\max}$ so that the online cost stays acceptable; if the tolerance cannot be met with a moderate $N$, split $\mathcal{P}$ into subdomains with separate bases.
- Check effectivities on a test set with truth solutions; effectivities below 1 indicate a bug or an invalid $\alpha_{\mathrm{LB}}$, and very large ones a poor coercivity bound.

## Key Takeaways

- The reduced basis method solves a Galerkin problem in the span of $N$ truth snapshots; for coercive problems it is quasi-optimal with the truth constants and, for symmetric ones, optimal in the energy norm.
- The weak greedy algorithm needs one truth solve per basis function and selects the next parameter by maximizing a cheap rigorous bound; it converges at the rate of the Kolmogorov $n$-width.
- With affine dependence, the reduced solution, output and error bound cost $O(QN^2 + N^3 + (QN)^2)$ online, independent of $N_h$.
- The bound $`\Delta_N = \lVert \mathbf{r} \rVert_{X'}/\alpha_{\mathrm{LB}}`$ has effectivity between 1 and $\gamma/\alpha_{\mathrm{LB}}$; compliant outputs have error bounds $`\lVert \mathbf{r} \rVert_{X'}^2/\alpha_{\mathrm{LB}}`$ and converge quadratically.
- Evaluate the residual norm from an orthonormalized factor rather than a Gram matrix, or the bound stalls at about $10^{-8}$ relative.

## Related Scripts

- [Certified Reduced Basis Method for a Thermal Block](../../../scripts/algorithms/reduced_basis_thermal_block/): builds a certified reduced basis model of steady heat conduction in a 2D thermal block with three parametrized conductivities, using a weak greedy algorithm driven by the residual-based error bound $`\lVert r(\mu) \rVert_{X'}/\alpha_{\mathrm{LB}}(\mu)`$.
- [Kolmogorov n-Width of Diffusing and Translating Solutions](../../../scripts/plots/rom_n_width_decay/): compares how fast linear subspaces can approximate three parametrized solution families, a diffusing pulse, a translating pulse and a translating step, by plotting the singular values of their snapshot matrices and the worst-case error of projecting the samples onto the best $N$-dimensional subspace.
- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.

## Exercises

**Exercise 1.** A snapshot matrix has singular values $\sigma = (10, 4, 1.5, 0.5, 0.2)$. Choose $N$ so that $\sum_{i \le N}\sigma_i^2$ is at least 99% and at least 99.9% of $\sum_i\sigma_i^2$.

<details>
<summary>Answer</summary>

The squares are $100, 16, 2.25, 0.25, 0.04$, with total $118.54$. The cumulative fractions are $0.8436, 0.9786, 0.9976, 0.9997, 1$. So $N = 3$ for 99% and $N = 4$ for 99.9%.

</details>

**Exercise 2.** Consider the affine truth problem $A(\mu)\mathbf{u} = \mathbf{f}$ with $A(\mu) = A_1 + \mu I$, where

```math
A_1 = \begin{pmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{pmatrix}, \qquad \mathbf{f} = (1, 1, 1)^T
```

and the one-vector basis $Z = (1, 1, 1)^T/\sqrt{3}$ (orthonormal in the Euclidean product). Precompute $Z^TA_1Z$, $Z^TZ$ and $\mathbf{f}_N = Z^T\mathbf{f}$. Find the reduced solution at $\mu = 1$ and compare it with the truth.

<details>
<summary>Answer</summary>

$A_1Z = (1, 0, 1)^T/\sqrt{3}$, so $Z^TA_1Z = 2/3$. Also $Z^TZ = 1$ and $\mathbf{f}_N = \sqrt{3}$. Online, $A_N(\mu) = 2/3 + \mu$, so at $\mu = 1$ the coefficient is $\sqrt{3}/(5/3) \approx 1.0392$ and $\mathbf{u}_N = (0.6, 0.6, 0.6)$.

The truth is $(A_1 + I)^{-1}\mathbf{f} = (4/7, 5/7, 4/7) \approx (0.5714, 0.7143, 0.5714)$. The error norm is $0.1212$, about 11% relative. A constant vector cannot represent the peak in the middle.

</details>

**Exercise 3.** Build a two-vector basis from the snapshots at $\mu = 0$ and $\mu = 10$ of Exercise 2, orthonormalize it, and solve the reduced problem at $\mu = 1$. Explain why the error is zero to machine precision.

<details>
<summary>Answer</summary>

The snapshots are $\mathbf{u}(0) = A_1^{-1}\mathbf{f} = (1.5, 2, 1.5)$ and $\mathbf{u}(10) = (13/142, 7/71, 13/142) \approx (0.0915, 0.0986, 0.0915)$. After Gram–Schmidt the Galerkin system gives $\mathbf{u}_N(1) = (4/7, 5/7, 4/7)$, equal to the truth.

$A(\mu)$ and $\mathbf{f}$ are unchanged by reversing the node order, so every truth solution is symmetric, $\mathbf{u} = (p, q, p)$. These vectors form a two-dimensional subspace, which the two independent snapshots span. The solution manifold lies entirely in $V_N$, and by quasi-optimality the Galerkin error is bounded by the best-approximation error, which is zero.

</details>

**Exercise 4.** Let $A(\mu)$ be symmetric positive definite and let $\mathbf{a}$ solve the Galerkin system $Z^TAZ\mathbf{a} = Z^T\mathbf{f}$. Prove that $Z\mathbf{a}$ minimizes the energy-norm error, $`\lVert \mathbf{u}_h - Z\mathbf{a} \rVert_A \le \lVert \mathbf{u}_h - Z\mathbf{b} \rVert_A`$ for all $\mathbf{b}$, where $`\lVert \mathbf{v} \rVert_A^2 = \mathbf{v}^TA\mathbf{v}`$.

<details>
<summary>Answer</summary>

Galerkin orthogonality: $Z^TA(\mathbf{u}_h - Z\mathbf{a}) = Z^T\mathbf{f} - Z^TAZ\mathbf{a} = \mathbf{0}$. For any $\mathbf{b}$, write $\mathbf{u}_h - Z\mathbf{b} = (\mathbf{u}_h - Z\mathbf{a}) + Z(\mathbf{a} - \mathbf{b})$. Then

```math
\lVert \mathbf{u}_h - Z\mathbf{b} \rVert_A^2 = \lVert \mathbf{u}_h - Z\mathbf{a} \rVert_A^2 + 2(\mathbf{a} - \mathbf{b})^TZ^TA(\mathbf{u}_h - Z\mathbf{a}) + \lVert Z(\mathbf{a} - \mathbf{b}) \rVert_A^2 = \lVert \mathbf{u}_h - Z\mathbf{a} \rVert_A^2 + \lVert Z(\mathbf{a} - \mathbf{b}) \rVert_A^2
```

The last term is non-negative, which proves the claim. This is Céa's lemma with constant 1 in the energy norm, and it explains why the reduced solution in Exercise 3 is exact.

</details>

**Exercise 5.** For $A = A_1 + I$ and $\mathbf{f}$ of Exercise 2, with $X = I$, evaluate the error bound $`\Delta = \lVert \mathbf{r} \rVert_2/\alpha`$ for the reduced solution $`\mathbf{u}_N = (0.6, 0.6, 0.6)`$ of Exercise 2, using the exact coercivity constant $`\alpha = \lambda_{\min}(A)`$. Compare with the true error and compute the effectivity and its upper limit $\gamma/\alpha$.

<details>
<summary>Answer</summary>

$\mathbf{r} = \mathbf{f} - A\mathbf{u}_N = (1, 1, 1) - (1.2, 0.6, 1.2) = (-0.2, 0.4, -0.2)$, so $`\lVert \mathbf{r} \rVert_2 = \sqrt{0.24} \approx 0.490`$. The eigenvalues of $A_1$ are $2 - \sqrt{2}$, $2$ and $2 + \sqrt{2}$, so $\alpha = 3 - \sqrt{2} \approx 1.586$ and $\gamma = 3 + \sqrt{2} \approx 4.414$. The bound is $0.490/1.586 = 0.309$ and the true error $0.121$, an effectivity of 2.55, below $\gamma/\alpha = 2.78$. The bound needed only the residual of the reduced solution and $\alpha$, not a new truth solve.

</details>

## References

- A. Quarteroni, A. Manzoni and F. Negri, *Reduced Basis Methods for Partial Differential Equations: An Introduction*, Springer, 2016.
- J. S. Hesthaven, G. Rozza and B. Stamm, *Certified Reduced Basis Methods for Parametrized Partial Differential Equations*, SpringerBriefs in Mathematics, Springer, 2016.
- K. Veroy, C. Prud'homme, D. V. Rovas and A. T. Patera, "A posteriori error bounds for reduced-basis approximation of parametrized noncoercive and nonlinear elliptic partial differential equations", 16th AIAA Computational Fluid Dynamics Conference, AIAA Paper 2003-3847, 2003.
- G. Rozza, D. B. P. Huynh and A. T. Patera, "Reduced basis approximation and a posteriori error estimation for affinely parametrized elliptic coercive partial differential equations", *Archives of Computational Methods in Engineering* 15(3), 229–275, 2008.
- D. B. P. Huynh, G. Rozza, S. Sen and A. T. Patera, "A successive constraint linear optimization method for lower bounds of parametric coercivity and inf-sup stability constants", *Comptes Rendus Mathématique* 345(8), 473–478, 2007.
- P. Binev, A. Cohen, W. Dahmen, R. DeVore, G. Petrova and P. Wojtaszczyk, "Convergence rates for greedy algorithms in reduced basis methods", *SIAM Journal on Mathematical Analysis* 43(3), 1457–1472, 2011.
- A. Buffa, Y. Maday, A. T. Patera, C. Prud'homme and G. Turinici, "A priori convergence of the greedy algorithm for the parametrized reduced basis method", *ESAIM: Mathematical Modelling and Numerical Analysis* 46(3), 595–603, 2012.
- B. Haasdonk and M. Ohlberger, "Reduced basis method for finite volume approximations of parametrized linear evolution equations", *ESAIM: Mathematical Modelling and Numerical Analysis* 42(2), 277–302, 2008.
- F. Casenave, A. Ern and T. Lelièvre, "Accurate and online-efficient evaluation of the a posteriori error bound in the reduced basis method", *ESAIM: Mathematical Modelling and Numerical Analysis* 48(1), 207–229, 2014.
