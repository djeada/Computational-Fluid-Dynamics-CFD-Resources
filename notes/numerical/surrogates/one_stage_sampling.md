## Introduction and Conceptual Framework

One-stage sampling refers to the class of methods in which all sample points within a given domain $\Omega$ are chosen before any evaluations of the expensive function $y(x)$ are performed. This is in contrast to adaptive or sequential sampling, where the locations of future sample points depend on the information gleaned from previously computed values. In the setting of deterministic computer experiments—such as expensive physics-based simulations, computational fluid dynamics models, or high-resolution climate models—each evaluation $y(x)$ may be extremely costly. Thus, the design of the sample set $X = \{x^{(1)}, \ldots, x^{(N)}\}$, with $x^{(i)} \in \Omega \subseteq \mathbb{R}^d$, becomes a critical step in building accurate and efficient surrogate models.

The fundamental goal of one-stage (or a-priori) designs is to produce sample sets that can lead to globally accurate surrogate approximations without relying on knowledge of $y(x)$ itself. Since we do not know which regions of $\Omega$ are more complex or which variables are more influential, a natural guiding principle is space-fillingness. A space-filling design distributes points as evenly as possible throughout $\Omega$, minimizing large gaps and preventing excessive clustering. This approach ensures that no large portion of the domain is left unexplored, thereby offering a good initial representation of the unknown function.

## Types of One-Stage Designs

One-stage designs can be categorized along multiple dimensions: deterministic vs. random, model-based vs. model-independent, and grid-based vs. flexible. Some of these categories overlap and can be mixed, depending on the practitioner’s constraints and objectives.

I. Deterministic vs. Random:
- Deterministic designs follow fixed, rule-based patterns (e.g., a structured grid, low-discrepancy sequences).
- Random designs incorporate randomness to avoid structured aliasing and to produce multiple realizations with statistical properties (e.g., random Latin hypercube designs).
II. Model-Based vs. Model-Independent:
- Model-independent methods assume no prior information about $y(x)$. They require only knowledge of the domain $\Omega$ and the desired sample size $N$.
- Model-based approaches might assume a certain model form (e.g., polynomial trends) or rely on correlation structures known a-priori. However, even then, in a purely one-stage framework, the model parameters are not updated from observed data; they remain fixed assumptions.
III. Grid-Based (e.g., Factorial Designs) vs. More Flexible (e.g., Latin Hypercube, Low-Discrepancy):
- Simple approaches like full factorial or uniform grids are easy to understand but suffer from the curse of dimensionality.
- More sophisticated methods—Latin hypercube designs, distance-based optimal designs, or low-discrepancy sequences—offer improved coverage and scalability.

## Mathematical Setup and Notation

We typically assume a $d$-dimensional domain $\Omega = [0,1]^d$ for simplicity. Any rectangular domain can be scaled and shifted to $[0,1]^d$. In higher dimensions, $\Omega$ may be more complicated, but transformations can often reduce it to a unit hypercube.

A design is a set of $N$ points:

$$X = \{ x^{(1)}, x^{(2)}, \ldots, x^{(N)} \} \subset [0,1]^d.$$

The question is: how to choose $X$ so that a surrogate model $\hat{y}(x)$, built solely from $\{x^{(i)}, y(x^{(i)})\}$, achieves good global accuracy?

Without knowledge of $y(x)$, we must rely on geometry and heuristics. Two common strategies are:

I. Ensuring every dimension is well-sampled across the entire range.

II. Attempting to maximize uniformity or minimize discrepancy.

## Space-Filling Criteria and Quality Measures

Different objective functions attempt to quantify what it means for a design to be "space-filling." Some well-known criteria include:

I. **Minimax criterion**: Minimize the largest empty ball in $\Omega$ that does not contain any design point. Formally:

$$X^* = \arg\min_{X \subset \Omega, |X|=N} \max_{x \in \Omega} \text{dist}(x, X),$$
where $\text{dist}(x, X) = \min_{x^{(i)} \in X}\|x - x^{(i)}\|$.

II. **Maximin criterion**: Maximize the minimum distance between any pair of points:

$$X^* = \arg\max_{X \subset \Omega, |X|=N} \min_{i \neq j}\|x^{(i)} - x^{(j)}\|.$$

III. **$\phi_p$-criterion**: Consider an aggregate measure of inter-point distances:

$$\phi_p(X) = \left( \frac{1}{\binom{N}{2}} \sum_{1 \leq i < j \leq N} \|x^{(i)} - x^{(j)}\|^{-p} \right)^{1/p}.$$

Minimizing $\phi_p(X)$ for large $p$ approximates a maximin design, while other choices of $p$ balance local and global spacing.

IV. **Low-discrepancy criteria**: Discrepancy measures how much the empirical distribution of design points deviates from a uniform distribution over $\Omega$:

$$D_N(X) = \sup_{I \in \mathcal{I}} \left|\frac{\#\{X \cap I\}}{N} - \frac{\text{Vol}(I)}{\text{Vol}(\Omega)}\right|,$$
where $\mathcal{I}$ is a family of axis-aligned boxes. Minimizing discrepancy leads to designs with more uniform coverage.

## Classical One-Stage Designs: Factorial and Fractional Factorials

### Full Factorial Designs

One of the oldest and simplest designs is the full factorial grid. Suppose each dimension is divided into $n_k$ evenly spaced levels:

$$x_k \in \left\{ \frac{0}{n_k-1}, \frac{1}{n_k-1}, \frac{2}{n_k-1}, \ldots, \frac{n_k-1}{n_k-1}\right\}.$$

The total number of points:

$$N = \prod_{k=1}^{d} n_k.$$

If $n_k = n$ for all $k$, we have:

$$N = n^d.$$

**Issues**:
- Rapidly grows unmanageable as $d$ increases (curse of dimensionality).
- Very rigid: you must pick $N$ to be a perfect power.

### Fractional Factorial and Plackett-Burman Designs

When $d$ is large, full factorial designs require enormous numbers of samples. Fractional factorial designs reduce the sample size by selecting carefully chosen subsets of the full factorial grid that preserve certain properties of coverage or orthogonality. They are widely used in screening experiments to identify which variables are most important:
- For instance, a $2^{d}$-factorial design picks two levels per dimension, requiring $2^d$ points. For $d=10$, that’s $1024$ points. A fractional factorial might use $2^{5}=32$ points (a 1/32 fraction) to achieve preliminary screening.

While these are historically important, they remain limited in flexibility and dimensional scalability for modern computer experiments.

## Stratification-Based Designs: Latin Hypercube

### Latin Hypercube Designs (LHDs)

Latin hypercube sampling addresses some limitations of factorial designs. For a given $N$ and $d$, each dimension is divided into $N$ equal intervals:

$$I_j = \left[\frac{j-1}{N}, \frac{j}{N}\right], \quad j=1,\ldots,N.$$

A Latin hypercube design ensures that each interval in each dimension contains exactly one point. To construct an LHD:

I. Generate $d$ random permutations $\pi_k$ of $\{1,\ldots,N\}$.

II. For each $i=1,\ldots,N$, define:

$$x_k^{(i)} \in I_{\pi_k(i)}.$$

A common choice is to select the center of each chosen interval:

$$x_k^{(i)} = \frac{\pi_k(i)-1}{N} + \frac{1}{2N}.$$

Alternatively, one can sample uniformly at random within the chosen interval. This ensures that each dimension is "fully represented," preventing the design from collapsing onto a low-dimensional subspace and guaranteeing that removing one dimension results in another valid LHD in $(d-1)$-dimensions.

**Advantages**:
- Flexible: choose any $N$, any $d$.
- Often combined with optimization criteria (e.g., reorder permutations to maximize minimum inter-point distance or minimize discrepancy).
- Widely used in engineering, uncertainty quantification, and surrogate modeling due to their simplicity and good empirical performance.

## Distance-Based and Optimized One-Stage Designs

Rather than relying on heuristics (like LHD), one can numerically optimize a design according to a chosen criterion (minimax, maximin, $\phi_p$, or discrepancy). The optimization problem:

$$X^* = \arg\min_{X \subset \Omega} C(X)$$
where $C(X)$ is a cost function (e.g., $\phi_p$ or discrepancy).

Solving this optimally is often combinatorially hard and computationally expensive, especially in higher dimensions. Thus, heuristics like simulated annealing, genetic algorithms, or gradient-based optimization of continuous representations (like moving points around in $[0,1]^d$) are used.

**Example**:
- Maximin design optimization might start from a random LHD and then iteratively swap rows or columns to increase the minimum inter-point distance. This process yields a "maximin-improved Latin hypercube."
**Complexity**:
- The search space is enormous, even for moderate $N$ and $d$.
- No closed-form solutions for general cases, and optimal known solutions are often tabulated or published as best known results.

## Low-Discrepancy Designs

Low-discrepancy (LD) sequences, such as Sobol, Halton, or Hammersley sets, are deterministic sequences that aim to fill space more uniformly than random points. They achieve a discrepancy $D_N(X)$ on the order of $(\log N)^d / N$, significantly better than the $N^{-1/2}$ rate of pure Monte Carlo sampling.

**Common LD Sequences**:

I. **Halton sequences**: Constructed using a base-prime representation. Good for low to moderate dimensions but can suffer correlation issues in high $d$.

II. **Sobol sequences**: A popular choice for high-dimensional integration. Defined by direction numbers and known to provide good uniformity properties.

III. **Hammersley sets**: Involves pairing a regular sequence in one dimension with a Van der Corput sequence in another.

These sequences require no complex optimization and can be generated for any $N$. They have been widely used in quasi-Monte Carlo (QMC) methods for numerical integration and have found their way into surrogate modeling. The advantage is their strong theoretical properties ensuring better global coverage as $N$ grows.

## Comparisons and Practical Considerations

Each one-stage design method has trade-offs:

| **Design Type**                | **Pros**                                                                                              | **Cons**                                                                                                    |
|--------------------------------|-------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| **Factorial and Fractional Factorial** | Simple, historically understood.                                                                   | Not scalable to high \(d\), limited flexibility in choosing \(N\).                                         |
| **Latin Hypercube Designs**    | Very flexible, easy to generate, can be improved with post-processing.                                | Without optimization, random LHDs might not be optimal; requires refinement if maximal space-filling is desired. |
| **Distance-Based Optimal Designs** | Can produce highly uniform or carefully balanced sets of points.                                     | Computationally expensive, no closed-form solutions, limited to moderate \(N, d\).                         |
| **Low-Discrepancy Designs**    | Strong theoretical guarantees, easily generate large \(N\) sets, good uniformity properties.           | Some sequences degrade in very high dimensions or have subtle correlation patterns.                        |


In practice, many researchers start with a baseline method (e.g., a random LHD) and then refine it by:

- Applying an optimization algorithm to reorder permutations in LHD to achieve a maximin or minimal $\phi_p$ solution.
- Using a known low-discrepancy sequence and, if necessary, rotating or permuting coordinates to reduce unwanted correlations.
- Combining a small initial one-stage design with subsequent adaptive sampling stages to refine the surrogate in promising regions.

## Worked Example: Constructing and Evaluating a One-Stage Design

**Step-by-step Example**:

I. **Setup**:

Suppose $\Omega = [0,1]^2$, $d=2$, and we need $N=9$ samples.

II. **Choice of Method**:

Start with a simple Latin hypercube design. Divide each dimension into 9 equal intervals:  

$$I_j = \left[\frac{j-1}{9}, \frac{j}{9}\right], \quad j=1,\ldots,9.$$

Possible intervals: $I_1 = [0, \frac{1}{9}], I_2 = [\frac{1}{9}, \frac{2}{9}], \ldots, I_9 = [\frac{8}{9},1]$.

III. **Permutations**:

Generate two random permutations of $\{1,\ldots,9\}$:

$$\pi_1 = (2,9,4,1,8,3,7,5,6), \quad \pi_2 = (5,2,1,8,4,9,6,7,3).$$

This means for the first dimension $x_1^{(1)} \in I_2, x_1^{(2)} \in I_9,$ and so forth.

IV. **Assigning Points**:

Take the midpoint of each chosen interval:

$$\text{mid}(I_j) = \frac{j-1}{9} + \frac{1}{18} = \frac{2j-1}{18}.$$

Thus, $\text{mid}(I_2)=\frac{3}{18}=0.1667, \text{mid}(I_9)=\frac{17}{18}=0.9444,$ and so on.

Construct each point $x^{(i)} = (x_1^{(i)}, x_2^{(i)})$ by choosing:

$$x_1^{(i)} = \text{mid}(I_{\pi_1(i)}), \quad x_2^{(i)} = \text{mid}(I_{\pi_2(i)}).$$

After computing all 9 points, we obtain a 9-point LHD.

V. **Evaluate Space-Filling Quality**:

Compute all $\binom{9}{2}=36$ pairwise distances. Find:

$$\delta_{\min} = \min_{i \neq j}\|x^{(i)}-x^{(j)}\|_2.$$

The larger $\delta_{\min}$, the better the maximin criterion. If $\delta_{\min}$ seems small, try permuting intervals or applying an optimization algorithm (like simulated annealing) to increase $\delta_{\min}$.

VI. **Optional Refinement**:

Try multiple random LHDs and choose the one with the best maximin distance. This leads to an improved one-stage design.

## Historical and Theoretical Background

The theory behind one-stage sampling in computer experiments builds on:

- Classical experimental design, which historically focused on regression models and factorial designs.
- Quasi-Monte Carlo literature, which developed low-discrepancy sequences for numerical integration.
- Geometric combinatorics in searching for optimal packing and covering of high-dimensional spaces.

Key references (not cited here explicitly) delve into entropy-based designs, integrated mean squared error (IMSE) criteria from Kriging theory, and model-based criteria like maximum likelihood estimation for Gaussian processes. While these may require partial knowledge of $y(x)$ or assumptions about its correlation structure, they can still be used in a pre-data (one-stage) setting to guess good configurations.

## Practical Tips and Guidance

I. **Dimensionality**:  

If $d$ is small (e.g., $d \leq 5$), more sophisticated optimization for one-stage designs is feasible. For $d > 10$, simpler methods like LHD or low-discrepancy sequences might be preferable due to computational constraints.

II. **Number of Samples (N)**:  

Choose $N$ large enough to cover $\Omega$ but not so large as to be infeasible. One-stage methods are often initial steps; a moderately sized design (e.g., $N = 10d$ to $50d$) is common as a starting point.

III. **Refinement and Sequential Use**:  

The initial one-stage design can serve as a foundation. Once the surrogate is built, if certain regions require more samples, a subsequent adaptive (two-stage or multi-stage) approach can refine the design.

IV. **Computational Tools**:

Many software packages (R, Python, MATLAB) provide routines for generating LHDs, Sobol sequences, and even heuristics to improve designs. For instance, MATLAB’s `lhsdesign` function can generate LHDs with an option to improve space-filling properties. Python’s `pyDOE` package and R’s `lhs` package offer similar functionalities.
