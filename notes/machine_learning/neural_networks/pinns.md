# Physics-Informed Neural Networks

A physics-informed neural network (PINN) represents the solution of a differential equation by a neural network $u_{\boldsymbol\theta}(\mathbf{x}, t)$ and trains it so that the equation, the boundary conditions and any available measurements are satisfied in a least-squares sense. No mesh is needed: the residual is evaluated at scattered points using exact derivatives of the network obtained by automatic differentiation. The idea goes back to Lagaris, Likas and Fotiadis (1998) and was popularised by Raissi, Perdikaris and Karniadakis (2019).

For CFD the method is most useful where classical solvers are awkward: inverse problems that combine sparse, noisy data with the governing equations (unknown viscosity, inflow profile or pressure field), and problems where data and physics must be merged in one model. For a standard forward problem on a known geometry, a PINN is usually slower and less accurate than a finite-difference or finite-volume solver; this note explains why, and how PINNs fail.

## Problem Statement

Let $\Omega \subset \mathbb{R}^d$ be the spatial domain, $t \in [0, T]$ the time interval, and $\mathbf{x} \in \Omega$ the spatial coordinate. The unknown field $u(\mathbf{x}, t)$ (scalar or vector, for example $`(\mathbf{u}, p)`$) satisfies

```math
\mathcal{N}[u;\,\boldsymbol\lambda](\mathbf{x}, t) = 0 \quad \text{in } \Omega \times (0, T], \qquad
\mathcal{B}[u](\mathbf{x}, t) = g(\mathbf{x}, t) \quad \text{on } \partial\Omega \times (0, T], \qquad
u(\mathbf{x}, 0) = u_0(\mathbf{x}),
```

where $\mathcal{N}$ is a (possibly nonlinear) differential operator with physical parameters $\boldsymbol\lambda$ (such as $\nu$), $\mathcal{B}$ is a boundary operator (Dirichlet, Neumann, periodic) and $u_0$ is the initial condition. Optionally, $N_d$ measurements $`\mathcal{D} = \{(\mathbf{x}_i, t_i, y_i)\}_{i=1}^{N_d}`$ of $u$ or of a derived quantity are available.

Approximate $u$ by a network $u_{\boldsymbol\theta}$ with parameters $\boldsymbol\theta$, and choose three point sets: $N_r$ collocation points $(\mathbf{x}_k^r, t_k^r)$ in the interior, $N_b$ points on the boundary and $N_0$ points at $t = 0$. The PINN solves

```math
\min_{\boldsymbol\theta,\,\boldsymbol\lambda} \;
\mathcal{L}(\boldsymbol\theta, \boldsymbol\lambda) =
\frac{w_r}{N_r} \sum_{k=1}^{N_r} \left| \mathcal{N}[u_{\boldsymbol\theta};\,\boldsymbol\lambda](\mathbf{x}_k^r, t_k^r) \right|^2
+ \frac{w_b}{N_b} \sum_{k=1}^{N_b} \left| \mathcal{B}[u_{\boldsymbol\theta}](\mathbf{x}_k^b, t_k^b) - g(\mathbf{x}_k^b, t_k^b) \right|^2
+ \frac{w_0}{N_0} \sum_{k=1}^{N_0} \left| u_{\boldsymbol\theta}(\mathbf{x}_k^0, 0) - u_0(\mathbf{x}_k^0) \right|^2
+ \frac{w_d}{N_d} \sum_{i=1}^{N_d} \left| u_{\boldsymbol\theta}(\mathbf{x}_i, t_i) - y_i \right|^2
```

with weights $w_r, w_b, w_0, w_d \ge 0$. In a forward problem $\boldsymbol\lambda$ is known and $w_d$ is usually zero; in an inverse problem $\boldsymbol\lambda$ is unknown and the data term is what determines it.

Three things make this hard. The loss is a non-convex function of $\boldsymbol\theta$ whose terms can differ in scale by orders of magnitude. A small loss at the collocation points does not imply a small error, because the residual is only enforced at those points and the network can do anything in between. And for stiff, convection-dominated or chaotic problems the optimisation landscape is badly conditioned, so gradient-based training may stall at a wrong solution.

## Network and Automatic Differentiation

A fully connected network with $L$ hidden layers maps the input $\mathbf{z}_0 = (\mathbf{x}, t)$ to

$$
\mathbf{z}_\ell = \sigma\left(W_\ell \mathbf{z}_{\ell-1} + \mathbf{b}_\ell\right), \quad
\ell = 1, \dots, L,
\qquad u_{\boldsymbol\theta} = W_{L+1} \mathbf{z}_L + \mathbf{b}_{L+1}
$$

where $W_\ell$ and $\mathbf{b}_\ell$ are the weights and biases and $\sigma$ is the activation function (see [Neural Networks](../fundamentals/neural_networks.md)). The activation must be smooth enough for the highest derivative in $\mathcal{N}$: $\tanh$, $\sin$ and swish are common, while ReLU has a zero second derivative almost everywhere and cannot represent a diffusion term.

The derivatives $\partial u_{\boldsymbol\theta}/\partial x$, $\partial^2 u_{\boldsymbol\theta}/\partial x^2$, ... are computed by automatic differentiation (AD), the same chain-rule machinery used for backpropagation, but applied with respect to the inputs instead of the parameters. AD is exact to rounding error, unlike finite differences, and needs no mesh. For one hidden layer, $u_{\boldsymbol\theta}(x) = \sum_j v_j \tanh(w_j x + b_j) + c$, the derivatives can be written out by hand. With $t_j = \tanh(w_j x + b_j)$ and $s_j = 1 - t_j^2$,

$$
u_{\boldsymbol\theta}' = \sum_j v_j w_j s_j,
\qquad u_{\boldsymbol\theta}'' = -2 \sum_j v_j w_j^2 t_j s_j
$$

Training then needs the gradient of the loss with respect to $\boldsymbol\theta$ of these input derivatives, which a framework obtains by differentiating the AD graph again. The cost of evaluating a $k$-th derivative grows with $k$ and with the number of input dimensions, so a residual with second derivatives in three space dimensions and time costs several times a plain forward pass at each collocation point.

## Forward and Inverse Problems

In a forward problem the equation, the parameters, the geometry and the boundary and initial conditions are all known, and the PINN is an unusual numerical solver. The network is a global, meshless trial function and the loss is a least-squares collocation residual. Lagaris et al. (1998) solved ODEs and PDEs this way with small networks.

In an inverse problem some of $\boldsymbol\lambda$, $g$ or $u_0$ is unknown and measurements are available. The PINN treats the unknowns as extra trainable variables and fits the data while satisfying the equation. This is the strongest use case, for three reasons:

1. The same code handles forward and inverse problems: adding an unknown parameter means adding one entry to the optimisation vector, while a classical approach needs an adjoint solver or many forward solves.
2. The data need not lie on a grid and may observe only some components of the solution.
3. The PDE term regularises the reconstruction between measurements and propagates information to unobserved quantities, such as the pressure when only velocity is measured.

Raissi et al. (2019) recovered the two coefficients of the Navier–Stokes equations for a cylinder wake from scattered velocity samples. Raissi, Yazdani and Karniadakis (2020) went further with hidden fluid mechanics: from snapshots of a passive scalar concentration $c$ (dye or smoke), they inferred velocity and pressure by enforcing the transport equation $c_t + \mathbf{u} \cdot \nabla c = \mathrm{Pe}^{-1} \nabla^2 c$ together with the incompressible Navier–Stokes equations, without any velocity measurements.

Identifiability still has to be checked. If the data never excite the term that contains a parameter (no velocity gradients, so no viscous stress), that parameter cannot be determined, and the PINN will return some value without complaint.

## Worked Formulations

### Viscous Burgers Equation

The benchmark of Raissi et al. (2019) is

$$
u_t + u u_x - \nu u_{xx} = 0, \quad x \in [-1, 1], \quad t \in [0, 1],
\qquad u(x, 0) = -\sin(\pi x), \quad u(\pm 1, t) = 0
$$

with $\nu = 0.01/\pi$. The solution develops a steep internal layer at $x = 0$ near $t \approx 0.4$. A network $u_{\boldsymbol\theta}(x, t)$ is trained with the residual

$$
r(x, t) = \frac{\partial u_{\boldsymbol\theta}}{\partial t} + u_{\boldsymbol\theta}
\frac{\partial u_{\boldsymbol\theta}}{\partial x} - \nu
\frac{\partial^2 u_{\boldsymbol\theta}}{\partial x^2}
$$

at $`N_r = 10\,000`$ collocation points, plus $N_b + N_0 = 100$ points on the initial and boundary data. In the inverse version, $\nu$ (and the coefficient of $u u_x$) become trainable and the data term uses samples of $u$ inside the domain.

### Incompressible Navier–Stokes Equations

For two-dimensional incompressible flow with velocity $\mathbf{u} = (u, v)$, kinematic pressure $p$ (pressure divided by density) and kinematic viscosity $\nu$, a network with outputs $(u_{\boldsymbol\theta}, v_{\boldsymbol\theta}, p_{\boldsymbol\theta})$ has the residuals

```math
\begin{aligned}
r_c &= \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y}, \\
r_x &= \frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} + \frac{\partial p}{\partial x} - \nu \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right), \\
r_y &= \frac{\partial v}{\partial t} + u \frac{\partial v}{\partial x} + v \frac{\partial v}{\partial y} + \frac{\partial p}{\partial y} - \nu \left( \frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2} \right),
\end{aligned}
```

and the PDE loss is the mean of $r_c^2 + r_x^2 + r_y^2$ over the collocation points (see [Navier–Stokes Equations](../../fluid_mechanics/governing_equations/navier_stokes.md)). The pressure appears only through its gradient, so it is determined up to a constant; a single pressure datum or a zero-mean condition fixes it.

The continuity residual can be removed altogether. Let the network output a stream function $\psi_{\boldsymbol\theta}$ and the pressure, and define

$$
u = \frac{\partial \psi_{\boldsymbol\theta}}{\partial y},
\qquad v = -\frac{\partial \psi_{\boldsymbol\theta}}{\partial x}
$$

Then $\partial u/\partial x + \partial v/\partial y = \psi_{yx} - \psi_{xy} = 0$ identically, for any parameters. This is how Raissi et al. (2019) set up the cylinder-wake problem. The price is one more derivative order: the momentum residual now contains third derivatives of $\psi_{\boldsymbol\theta}$. In three dimensions the analogue is a vector potential, $\mathbf{u} = \nabla \times \mathbf{A}$.

For turbulent flows the residual of the RANS equations needs a closure; a PINN does not remove that modelling choice (see [Turbulence Modeling](../../numerical/cfd/turbulence_modeling.md)).

## Boundary Conditions: Soft and Hard Enforcement

Soft enforcement adds boundary and initial misfits to the loss, as in the problem statement. It works for any condition and any geometry, but the conditions are only satisfied approximately, and the balance between $w_b$ and $w_r$ affects the result.

Hard enforcement builds the conditions into the trial function. For a Dirichlet condition $u = g$ on $\partial\Omega$, use

```math
u_{\boldsymbol\theta}(\mathbf{x}) = G(\mathbf{x}) + \phi(\mathbf{x})\,
N_{\boldsymbol\theta}(\mathbf{x})
```

where $N_{\boldsymbol\theta}$ is the network, $G$ is any smooth extension of $g$ into $\Omega$ and $\phi$ is a function that vanishes on $\partial\Omega$ and is positive inside, ideally an approximate distance function to the boundary. The boundary term then disappears from the loss. For $u(0) = 0$, $u(1) = 1$ on $[0, 1]$ one can take $G = x$ and $\phi = x(1 - x)$. For a time-dependent problem, $`u_{\boldsymbol\theta}(\mathbf{x}, t) = u_0(\mathbf{x}) + t\, N_{\boldsymbol\theta}(\mathbf{x}, t)`$ satisfies the initial condition exactly. Periodic conditions can be imposed exactly by feeding the network $\sin(2\pi x/L)$ and $\cos(2\pi x/L)$ instead of $x$. On complex geometries, constructing $\phi$ is itself a task; Sukumar and Srivastava (2022) build it from R-functions and approximate distance functions.

## Collocation Sampling

The residual is enforced only where it is sampled, so the choice of collocation points is part of the discretization.

| Strategy | Description | When to use |
| --- | --- | --- |
| Uniform grid | Tensor-product grid | Low dimension, smooth solutions |
| Uniform random | Independent uniform samples, often redrawn each epoch | Simple default; redrawing acts as stochastic quadrature |
| Latin hypercube or Sobol | Space-filling designs with lower discrepancy than random samples | Higher dimension, fixed budget |
| Residual-adaptive (RAR) | Evaluate $\lvert r \rvert$ on a large candidate set, add or resample points where it is largest | Layers, shocks, singularities |
| Importance by density | Draw points with probability proportional to $\lvert r \rvert^k$ | As above, with smoother point distribution |

Space-filling designs are discussed in [One-Stage Sampling](../../numerical/surrogates/one_stage_sampling.md) and adaptive refinement in [Adaptive Sampling](../../numerical/surrogates/adaptive_sampling.md). Lu et al. (DeepXDE, SIAM Review 2021) introduced residual-based adaptive refinement for PINNs; Wu et al. (2023) compare the strategies systematically.

Whatever the sampling, always evaluate the residual and, if possible, the error on a dense independent point set after training. The failure shown in the next section is invisible at the collocation points.

## Training and Failure Modes

PINNs are usually trained with Adam for tens of thousands of iterations, often followed by L-BFGS. For small networks, a Gauss–Newton method such as Levenberg–Marquardt on the residual vector converges much faster, which is what the example script does.

### A Boundary-Layer Example

The figure below comes from a PINN for $\varepsilon u'' - u' = 0$ on $[0, 1]$ with $u(0) = 0$ and $u(1) = 1$, whose exact solution $u = (e^{x/\varepsilon} - 1)/(e^{1/\varepsilon} - 1)$ has a layer of width about $\varepsilon$ at $x = 1$. The network has one hidden layer of 10 tanh neurons and is trained on 50 uniform collocation points.

![PINN solutions, dense-grid residuals, errors and loss histories for epsilon = 0.1, 0.02 and 0.01](../../../scripts/algorithms/pinn_boundary_layer/pinn_boundary_layer.png)

At $\varepsilon = 0.1$ the maximum error is $1.2 \times 10^{-6}$ and at $\varepsilon = 0.02$ it is $5.4 \times 10^{-4}$. At $\varepsilon = 0.01$ the network converges to $u \approx 1$ with a jump between $x = 0$ and the first collocation point: a constant satisfies the PDE, the jump satisfies $u(0) = 0$, and the training loss ($2.5 \times 10^{-11}$) is the lowest of the three runs while the error is 1. Only the residual on a dense grid (bottom left, peak about 400) reveals the failure. With 200 collocation points the same network and initialisation train correctly (maximum error $1.5 \times 10^{-5}$).

### Loss Imbalance and Gradient Pathologies

The loss terms have different physical units and scales. In the example above, $\varepsilon u''$ inside the layer is of order $1/\varepsilon$, so the residual term is larger than the boundary term by a factor that grows as $\varepsilon \to 0$. Wang, Teng and Perdikaris (2021) showed that the gradients of the residual term then dominate the update, the boundary terms are learned slowly, and the stiffness of the gradient flow forces a small learning rate. Their remedy adapts the weights during training:

```math
\hat w_b = \frac{\max_{\boldsymbol\theta} \left| \nabla_{\boldsymbol\theta} \mathcal{L}_r \right|}{\overline{\left| \nabla_{\boldsymbol\theta} \mathcal{L}_b \right|}},
\qquad w_b \leftarrow (1 - \alpha)\, w_b + \alpha\, \hat w_b
```

where the maximum and the mean (overbar) are over the components of the gradient vectors and $\alpha \approx 0.1$. Related schemes balance the terms using the eigenvalues of the neural tangent kernel, or use self-adaptive per-point weights. Non-dimensionalising the equations before training is the first and cheapest step.

### Spectral Bias

Gradient descent fits low-frequency components of a target much faster than high-frequency ones (Rahaman et al., ICML 2019). A PINN therefore learns the smooth part of a solution first and struggles with sharp layers, high wavenumbers or multi-scale fields. Fourier feature embeddings, which feed the network $[\cos(2\pi B \mathbf{x}), \sin(2\pi B \mathbf{x})]$ with a random matrix $B$, and domain decomposition both shift the representable frequencies upward.

### Causality in Time

For a time-dependent problem the residual at late times is minimised from the start, before the solution at early times is correct. The network can satisfy the PDE at late times with a solution that is not connected to the initial condition, for example a trivial steady state. Wang, Sankaran and Perdikaris (2024) split $[0, T]$ into $M$ slabs with residual losses $\mathcal{L}_r(t_i)$ and weight each slab by

$$
\omega_i = \exp\left(-\epsilon \sum_{j=1}^{i-1} \mathcal{L}_r(t_j)\right)
$$

so that a slab contributes only once the earlier ones are resolved; $\epsilon$ is a causality parameter. Time marching (training on successive windows, each initialised by the previous one) achieves the same effect.

### Characterised Failure Modes

Krishnapriyan et al. (NeurIPS 2021) showed that a standard PINN fails on the one-dimensional convection equation $u_t + \beta u_x = 0$ for $\beta$ of order 30 and above, and on reaction and reaction-diffusion problems with large reaction rates, although the network is expressive enough to represent the solution. The PDE term makes the loss landscape ill-conditioned. Two remedies worked: curriculum regularisation, which starts with a small $\beta$ and increases it gradually, and sequence-to-sequence learning in short time windows. The lesson is that failure to train is a property of the optimisation problem, not of the network size.

## Cost Compared With Classical Solvers

A forward PINN is a nonlinear least-squares problem in $\boldsymbol\theta$, solved by thousands of gradient steps, each of which evaluates high-order derivatives at every collocation point. A finite-difference or finite-volume method solves a sparse system whose cost is close to linear in the number of unknowns and whose error decreases at a known rate under refinement.

For the boundary-layer example, a second-order central-difference solve on the same 50 points takes about $4 \times 10^{-5}$ s with a tridiagonal solver; the PINN takes about 0.13 s for 1000 Levenberg–Marquardt evaluations, roughly 3000 times longer. At $\varepsilon = 0.1$ the PINN is more accurate ($1.2 \times 10^{-6}$ against $1.3 \times 10^{-3}$), because a smooth network behaves like a high-order global basis. At $\varepsilon = 0.01$ the finite-difference error on 50 points is 0.14 and falls to $8 \times 10^{-3}$ on 200 points, while the PINN result is simply wrong and refinement offers no guarantee. Benchmarks on standard problems (Grossmann et al., 2024) reach the same conclusion in more dimensions: the finite element method is faster and more accurate for forward solves, while the PINN's advantages lie in evaluating the solution at arbitrary points, in inverse problems, and in high-dimensional or parameterised settings where meshes are impractical.

## Variants

| Variant | Idea | Reference |
| --- | --- | --- |
| cPINN | Split the domain into subdomains, each with its own network, and enforce flux continuity at the interfaces; suited to conservation laws | Jagtap, Kharazmi and Karniadakis, CMAME 2020 |
| XPINN | Space-time domain decomposition with generalised interface conditions, for any PDE; subdomains train in parallel | Jagtap and Karniadakis, Commun. Comput. Phys. 2020 |
| hp-VPINN | Weak (variational) form with test functions on a decomposition of the domain; fewer derivatives of the network, $h$- and $p$-refinement | Kharazmi, Zhang and Karniadakis, CMAME 2021 |
| Hard-constraint PINN | Trial function satisfies boundary and initial conditions exactly | Sukumar and Srivastava (2022) |
| Parametric PINN | Network takes physical parameters (for example $\nu$ or a shape parameter) as extra inputs and learns a family of solutions | Survey by Cuomo et al. (2022) |

When the goal is many solves for different inputs, a parametric PINN competes with [neural operators](neural_operators.md), which learn the map from input functions to solutions directly from data.

## Key Takeaways

- A PINN minimises a weighted sum of PDE residual, boundary, initial and data misfits for a network trial function, with derivatives from automatic differentiation.
- Inverse problems (unknown parameters, fields or boundary data recovered from sparse measurements) are where PINNs are most useful; forward solves of standard problems are faster and more reliable with classical methods.
- The stream-function form makes the velocity divergence-free by construction; a distance-function ansatz satisfies Dirichlet conditions exactly.
- Loss imbalance, spectral bias, violation of temporal causality and ill-conditioning cause failures that more training does not fix.
- A small training loss does not certify the solution: check the residual on a dense independent grid, and the error against a reference where one exists.

## Related Scripts

- [PINN for a 1D Boundary Layer](../../../scripts/algorithms/pinn_boundary_layer/): This script trains a physics-informed neural network (PINN) on the steady advection–diffusion problem $\varepsilon u'' - u' = 0$, $u(0) = 0$, $u(1) = 1$, whose solution has a boundary layer of width about $\varepsilon$ at $x = 1$.

## Exercises

1. For the one-neuron network $u_{\boldsymbol\theta}(x) = v \tanh(w x + b)$ with $v = 1.5$, $w = 2$ and $b = 0.5$, compute $u_{\boldsymbol\theta}'(0)$ and $u_{\boldsymbol\theta}''(0)$ from the formulas in the text.

<details><summary>Answer</summary>

With $t = \tanh(0.5) = 0.46212$ and $s = 1 - t^2 = 0.78645$:

```math
u_{\boldsymbol\theta}'(0) = v w s = 1.5 \times 2 \times 0.78645 = 2.3593,
\qquad
u_{\boldsymbol\theta}''(0) = -2 v w^2 t s = -2 \times 1.5 \times 4 \times 0.46212 \times 0.78645 = -4.3612
```

A finite-difference check with step $10^{-5}$ gives the same values to five digits.

</details>

2. For $\varepsilon u'' - u' = 0$ with $u(0) = 0$, $u(1) = 1$ and $\varepsilon = 0.01$, find the point where $u = 0.01$, which marks the start of the boundary layer. How many of 50 uniform collocation points lie in the layer, and what uniform spacing would put 10 intervals across it?

<details><summary>Answer</summary>

For small $\varepsilon$, $u \approx e^{(x-1)/\varepsilon}$, so $u = 0.01$ at $x = 1 + \varepsilon \ln 0.01 = 1 - 0.0461 = 0.9539$. The layer width is $4.6\varepsilon = 0.0461$. With 50 points the spacing is $1/49 = 0.0204$, and only three points ($x = 0.959$, $0.980$, $1$) lie in the layer. Ten intervals across it need $h = 0.0046$, that is about 218 intervals on $[0, 1]$. Clustering points near $x = 1$ achieves the same with far fewer points.

</details>

3. Inverse problem. Samples $u(x_k)$ of the exact solution with unknown $\varepsilon$ are given at 101 uniform points. (a) Since the residual $\varepsilon u'' - u'$ is linear in $\varepsilon$, derive the least-squares estimate of $\varepsilon$ when $u'$ and $u''$ are known at the points. (b) With central differences for $u'$ and $u''$ and true value $\varepsilon = 0.05$, the estimate is 0.05017. With Gaussian noise of standard deviation $10^{-3}$ added to the samples it becomes 0.0429. Explain the difference, and why a PINN is less affected.

<details><summary>Answer</summary>

(a) Minimising $\sum_k (\varepsilon u_k'' - u_k')^2$ over $\varepsilon$ gives

```math
\hat\varepsilon = \frac{\sum_k u_k' u_k''}{\sum_k (u_k'')^2}
```

(b) Without noise the only error is the $O(h^2)$ truncation error of the differences (0.3 %; with 1001 points the estimate is 0.0500017). The second difference divides the noise by $h^2 = 10^{-4}$, so noise of $10^{-3}$ produces errors with standard deviation $\sqrt{6} \times 10^{-3}/10^{-4} \approx 25$ in $u''$, larger than $u''$ itself over most of the domain, and the estimate is biased by 14 %. A PINN never differentiates the data: it fits a smooth network to the samples through the data term and differentiates the network, while the PDE term constrains its derivatives. The noise then enters the estimate roughly like noise in a least-squares fit, not amplified by $1/h^2$.

</details>

4. Show that the stream-function parameterisation $u = \psi_y$, $v = -\psi_x$ satisfies continuity for any smooth $\psi$, and count the derivatives of $\psi_{\boldsymbol\theta}$ the steady $x$-momentum residual needs. For $\psi = \sin(\pi x) \sin(\pi y)$ on the unit square, evaluate $u$ and $v$ at $(0.25, 0.5)$.

<details><summary>Answer</summary>

$u_x + v_y = \psi_{yx} - \psi_{xy} = 0$ because mixed partial derivatives of a smooth function commute. The residual $u u_x + v u_y + p_x - \nu(u_{xx} + u_{yy})$ needs $\psi_y$, $\psi_x$, $\psi_{xy}$, $\psi_{yy}$, $\psi_{xxy}$ and $\psi_{yyy}$, so third derivatives of the network; the primitive-variable form needs only second derivatives but adds the continuity residual.

For the given $\psi$: $u = \pi \sin(\pi x) \cos(\pi y)$ and $v = -\pi \cos(\pi x) \sin(\pi y)$. At $(0.25, 0.5)$, $\cos(\pi/2) = 0$, so $u = 0$ and $v = -\pi \cos(\pi/4) = -2.221$.

</details>

5. In the boundary-layer figure the $\varepsilon = 0.01$ run reaches a smaller training loss than the correct $\varepsilon = 0.1$ run. Two fixes are proposed: (a) the hard boundary-condition ansatz $u_{\boldsymbol\theta} = x + x(1-x) N_{\boldsymbol\theta}(x)$ with the same 50 points, and (b) soft boundary conditions with 200 uniform points. Which one removes the wrong solution, and why?

<details><summary>Answer</summary>

Only (b). Running both from three random initialisations (seeds 0, 1, 2), with up to 3000 Levenberg–Marquardt evaluations for (a) and 1000 for (b), gives maximum errors of about 1 for every run of (a), and $1.5 \times 10^{-5}$, $1.3 \times 10^{-4}$ and $3.4 \times 10^{-4}$ for (b). The wrong solution exists because the residual is only checked at the collocation points: any function that is constant at all of them and jumps in between has zero PDE loss. The hard ansatz enforces $u(0) = 0$ and $u(1) = 1$ exactly, but $x(1-x) N_{\boldsymbol\theta}$ can still rise steeply between $x = 0$ and $x = 0.0204$, so the spurious minimum survives. With 200 points the spacing is 0.005, half of $\varepsilon$, and the steep transitions are seen by the loss. Clustering points near $x = 1$ or residual-adaptive resampling achieve the same with fewer points. The general lesson is that the collocation set is the discretization: it must resolve the smallest scale of the solution, as a mesh must.

</details>

## References

- Lagaris, I. E., Likas, A., and Fotiadis, D. I. "Artificial neural networks for solving ordinary and partial differential equations." *IEEE Transactions on Neural Networks* 9(5), 987–1000, 1998.
- Raissi, M., Perdikaris, P., and Karniadakis, G. E. "Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations." *Journal of Computational Physics* 378, 686–707, 2019.
- Raissi, M., Yazdani, A., and Karniadakis, G. E. "Hidden fluid mechanics: Learning velocity and pressure fields from flow visualizations." *Science* 367(6481), 1026–1030, 2020.
- Karniadakis, G. E., Kevrekidis, I. G., Lu, L., Perdikaris, P., Wang, S., and Yang, L. "Physics-informed machine learning." *Nature Reviews Physics* 3, 422–440, 2021.
- Wang, S., Teng, Y., and Perdikaris, P. "Understanding and mitigating gradient flow pathologies in physics-informed neural networks." *SIAM Journal on Scientific Computing* 43(5), A3055–A3081, 2021.
- Krishnapriyan, A. S., Gholami, A., Zhe, S., Kirby, R. M., and Mahoney, M. W. "Characterizing possible failure modes in physics-informed neural networks." *Advances in Neural Information Processing Systems* 34, 2021.
- Wang, S., Sankaran, S., and Perdikaris, P. "Respecting causality for training physics-informed neural networks." *Computer Methods in Applied Mechanics and Engineering* 421, 116813, 2024.
- Sukumar, N., and Srivastava, A. "Exact imposition of boundary conditions with distance functions in physics-informed deep neural networks." *Computer Methods in Applied Mechanics and Engineering* 389, 114333, 2022.
- Cuomo, S., Di Cola, V. S., Giampaolo, F., Rozza, G., Raissi, M., and Piccialli, F. "Scientific machine learning through physics-informed neural networks: Where we are and what's next." *Journal of Scientific Computing* 92, 88, 2022.
- Grossmann, T. G., Komorowska, U. J., Latz, J., and Schönlieb, C.-B. "Can physics-informed neural networks beat the finite element method?" *IMA Journal of Applied Mathematics* 89(1), 143–174, 2024.
