# Neural Networks

A neural network is a parametric function built by composing affine maps with elementwise nonlinearities. In CFD it serves as a surrogate for force coefficients or fields, as a closure term inside a solver, or as the trial function of a physics-informed method. This note defines the multilayer perceptron, derives backpropagation, states the optimisers and initialisations used in practice, and explains the preprocessing and the spectral bias that decide whether a network trains well on flow data. Training protocols, validation and error metrics are covered in [Training and Validation](training_and_validation.md).

## Problem Statement

Given a dataset $`\mathcal{D} = \{(\mathbf{x}_i, \mathbf{y}_i)\}_{i=1}^N`$ with inputs $\mathbf{x}_i \in \mathbb{R}^{n_0}$ (design parameters, flow conditions, coordinates) and outputs $`\mathbf{y}_i \in \mathbb{R}^{n_L}`$ (force coefficients, field values), find the parameters $`\boldsymbol\theta`$ of a network $`f_{\boldsymbol\theta}: \mathbb{R}^{n_0} \to \mathbb{R}^{n_L}`$ that minimise

$$
\mathcal{L}(\boldsymbol\theta) = \frac{1}{N} \sum_{i=1}^{N}
\ell\big(f_{\boldsymbol\theta}(\mathbf{x}_i), \mathbf{y}_i\big) + \lambda
R(\boldsymbol\theta)
$$

where $\ell$ is a pointwise loss and $R$ a regulariser with weight $\lambda \ge 0$. The difficulties are that $\mathcal{L}$ is nonconvex in $\boldsymbol\theta$, that $\boldsymbol\theta$ often has far more entries than there are samples, and that the network must be accurate on inputs it was not trained on. The architecture, the initialisation, the scaling of the data and the optimiser all affect which of the many minimisers is found.

## The Multilayer Perceptron

A multilayer perceptron (MLP) with $L$ layers of widths $n_0, n_1, \dots, n_L$ computes

$$
\mathbf{a}^{(0)} = \mathbf{x},
\qquad \mathbf{z}^{(l)} = W^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)},
\qquad \mathbf{a}^{(l)} = \sigma\big(\mathbf{z}^{(l)}\big),
\qquad l = 1, \dots, L - 1
$$

$$
f_{\boldsymbol\theta}(\mathbf{x}) = \mathbf{z}^{(L)} = W^{(L)} \mathbf{a}^{(L-1)} +
\mathbf{b}^{(L)}
$$

with weight matrices $W^{(l)} \in \mathbb{R}^{n_l \times n_{l-1}}$, bias vectors $\mathbf{b}^{(l)} \in \mathbb{R}^{n_l}$, pre-activations $\mathbf{z}^{(l)}$, activations $\mathbf{a}^{(l)}$ and an activation function $\sigma$ applied elementwise. For regression the output layer is linear, so the network can produce any real value. The parameter vector $\boldsymbol\theta$ stacks all $W^{(l)}$ and $\mathbf{b}^{(l)}$, and its length is

```math
P = \sum_{l=1}^{L} (n_{l-1} + 1)\, n_l
```

A network with $L - 1$ hidden layers is said to have depth $L - 1$ and width $\max_l n_l$. For a mini-batch of $B$ samples stored as columns of $A^{(l-1)} \in \mathbb{R}^{n_{l-1} \times B}$, one layer is a matrix product $Z^{(l)} = W^{(l)} A^{(l-1)} + \mathbf{b}^{(l)} \mathbf{1}^T$, which is why networks run efficiently on GPUs. Code often stores samples as rows instead and writes $Z = A W + \mathbf{1}\mathbf{b}^T$ with $W \in \mathbb{R}^{n_{l-1} \times n_l}$; the [MLP regression script](../../../scripts/algorithms/mlp_regression/) uses that convention.

## Activation Functions

Without a nonlinear $\sigma$ the composition of affine layers is affine. The common choices are:

| Name | $\sigma(z)$ | $\sigma'(z)$ | Range | Remarks |
| --- | --- | --- | --- | --- |
| Logistic sigmoid | $s(z) = 1/(1 + e^{-z})$ | $s(z)(1 - s(z))$ | $(0, 1)$ | Saturates; $\sigma' \le 1/4$, so gradients shrink through many layers |
| Hyperbolic tangent | $\tanh z$ | $1 - \tanh^2 z$ | $(-1, 1)$ | Zero-centred and smooth; standard for small regression networks and PINNs |
| ReLU | $\max(0, z)$ | $1$ for $z > 0$, $0$ for $z < 0$ | $[0, \infty)$ | Cheap, does not saturate for $z > 0$; second derivative is zero almost everywhere |
| Leaky ReLU | $\max(\alpha z, z)$, $0 < \alpha \ll 1$ | $1$ for $z > 0$, $\alpha$ for $z < 0$ | $\mathbb{R}$ | Avoids units that output zero for every input |
| Softplus | $\log(1 + e^{z})$ | $s(z)$ | $(0, \infty)$ | Smooth ReLU; useful as an output activation for positive quantities such as $\nu_t$ or $k$ |
| SiLU (swish) | $`z\, s(z)`$ | $s(z)\big(1 + z(1 - s(z))\big)$ | $(-0.28, \infty)$ | Smooth, non-monotonic; common in modern architectures |
| GELU | $`z\, \Phi(z)`$ | $`\Phi(z) + z\, \phi(z)`$ | $(-0.17, \infty)$ | $\Phi$ and $\phi$ are the standard normal CDF and PDF |

Physics-informed networks differentiate $f_{\boldsymbol\theta}$ with respect to its inputs, often twice for viscous terms. ReLU networks are piecewise linear, so their second derivatives vanish and the viscous residual carries no information; smooth activations such as $\tanh$ or SiLU are used there. The $\tanh$ and sigmoid derivatives can be written in terms of the activation itself, so backpropagation needs only the stored $\mathbf{a}^{(l)}$.

## Universal Approximation

Cybenko (1989) proved that one hidden layer suffices to approximate any continuous function on a compact set. Let $\sigma$ be continuous and sigmoidal ($\sigma(z) \to 1$ as $z \to \infty$ and $\sigma(z) \to 0$ as $z \to -\infty$). Then for every continuous $g$ on $[0, 1]^{n_0}$ and every $\varepsilon > 0$ there exist a width $n$ and parameters $\alpha_j, b_j \in \mathbb{R}$, $\mathbf{w}_j \in \mathbb{R}^{n_0}$ such that

```math
G(\mathbf{x}) = \sum_{j=1}^{n} \alpha_j\,
\sigma\big(\mathbf{w}_j^T \mathbf{x} + b_j\big) \quad \text{satisfies} \quad
\sup_{\mathbf{x} \in [0,1]^{n_0}} \lvert G(\mathbf{x}) - g(\mathbf{x}) \rvert <
\varepsilon
```

Hornik (1991) extended the result to any bounded, nonconstant activation (density in $L^p(\mu)$ for finite measures $\mu$, and in $C(K)$ on compact $K$ for continuous activations), showing that it is the layered structure and not the specific $\sigma$ that matters. Leshno et al. (1993) showed that a continuous activation gives this property if and only if it is not a polynomial, which covers ReLU.

The theorem guarantees existence only. It gives no bound on the width needed, no way to find the parameters by gradient descent, and no statement about accuracy away from the training samples. Barron (1993) gave a rate: for functions whose Fourier transform has a finite first moment $C_g$, a one-hidden-layer network with $n$ units achieves a squared $L^2$ error of order $C_g^2 / n$, independent of the input dimension, although $C_g$ itself may grow with dimension. In practice, deeper networks represent the compositional structure of physical responses with far fewer parameters than a single wide layer.

## Loss Functions for Regression

| Loss | Per-sample definition | Use |
| --- | --- | --- |
| Mean-squared error (MSE) | $\lVert \hat{\mathbf{y}} - \mathbf{y} \rVert_2^2$ | Default; maximum likelihood under Gaussian noise of constant variance |
| Mean absolute error (MAE) | $\lVert \hat{\mathbf{y}} - \mathbf{y} \rVert_1$ | Robust to outliers (e.g. a few unconverged cases); gradient does not shrink near the optimum |
| Huber, threshold $\delta$ | $\tfrac{1}{2} e^2$ for small residuals $e$, $\delta(\lvert e \rvert - \tfrac{1}{2}\delta)$ beyond $\delta$ | Quadratic near zero, linear for outliers |
| Relative $L^2$ field error | $\lVert \hat{\mathbf{u}} - \mathbf{u} \rVert_2 / \lVert \mathbf{u} \rVert_2$ | Fields of very different magnitude across cases |
| Gaussian negative log-likelihood | $\tfrac{1}{2}\log \hat\sigma^2 + (\hat y - y)^2 / (2\hat\sigma^2)$ | Network predicts a mean $\hat y$ and a variance $\hat\sigma^2$ |

For fields on a nonuniform mesh, an unweighted sum over nodes overweights the refined near-wall region. A volume-weighted loss $`\sum_j V_j (\hat u_j - u_j)^2 / \sum_j V_j`$, with cell volumes $V_j$, approximates the continuous $L^2$ norm instead. When several output variables are predicted together, each must be scaled (see below) or their losses weighted, otherwise the variable with the largest numerical range dominates.

## Backpropagation

Gradient-based training needs $`\nabla_{\boldsymbol\theta}\, \ell`$ for every sample. Backpropagation computes it with one forward and one backward pass, at a cost of a small multiple of the forward pass, by applying the chain rule from the output towards the input.

Define the error signal of layer $l$ as $\boldsymbol\delta^{(l)} = \partial \ell / \partial \mathbf{z}^{(l)} \in \mathbb{R}^{n_l}$. For the linear output layer and $\ell = \tfrac{1}{2}\lVert \mathbf{z}^{(L)} - \mathbf{y} \rVert^2$,

$$
\boldsymbol\delta^{(L)} = \mathbf{z}^{(L)} - \mathbf{y}
$$

Since $\mathbf{z}^{(l+1)} = W^{(l+1)} \sigma(\mathbf{z}^{(l)}) + \mathbf{b}^{(l+1)}$, its Jacobian with respect to $\mathbf{z}^{(l)}$ is $W^{(l+1)} \mathrm{diag}\big(\sigma'(\mathbf{z}^{(l)})\big)$. The chain rule then gives the backward recursion

$$
\boldsymbol\delta^{(l)} = \left(\frac{\partial \mathbf{z}^{(l+1)}}{\partial \mathbf{z}^{(l)}} \right)^T \boldsymbol\delta^{(l+1)} = \sigma'\big(\mathbf{z}^{(l)}\big) \odot \Big(\big(W^{(l+1)}\big)^T \boldsymbol\delta^{(l+1)} \Big),
\qquad l = L - 1, \dots, 1
$$

where $\odot$ is the elementwise product. Because $`z^{(l)}_i = \sum_j W^{(l)}_{ij} a^{(l-1)}_j + b^{(l)}_i`$, the parameter gradients are

$$
\frac{\partial \ell}{\partial W^{(l)}} = \boldsymbol\delta^{(l)}
\big(\mathbf{a}^{(l-1)}\big)^T,
\qquad \frac{\partial \ell}{\partial \mathbf{b}^{(l)}} = \boldsymbol\delta^{(l)}
$$

For a batch, the per-sample outer products sum to $\Delta^{(l)} (A^{(l-1)})^T$, with $\Delta^{(l)}$ holding the $\boldsymbol\delta^{(l)}$ of all samples as columns. For the mean over the batch, the output error carries the factor $1/B$.

The forward pass must store every $\mathbf{a}^{(l)}$, so memory grows with depth times batch size. Backpropagation is reverse-mode automatic differentiation specialised to this graph; frameworks such as PyTorch and JAX apply the same idea to arbitrary code, including the input derivatives needed by PINNs.

A hand-written backward pass should be checked against central finite differences,

$$
\frac{\partial \mathcal{L}}{\partial \theta_k} \approx
\frac{\mathcal{L}(\boldsymbol\theta + h\mathbf{e}_k) - \mathcal{L}(\boldsymbol\theta - h\mathbf{e}_k)}{2h}
$$

whose truncation error is $O(h^2)$. A relative mismatch below about $10^{-6}$ with $h \approx 10^{-6}$ in double precision indicates a correct implementation. The unit test of the MLP script performs this check for every weight and bias.

## Optimisers

Gradient descent with learning rate $\eta$ updates

```math
\boldsymbol\theta_{k+1} = \boldsymbol\theta_k - \eta\, \nabla
\mathcal{L}(\boldsymbol\theta_k)
```

Stochastic gradient descent (SGD) replaces the full gradient by the mean over a random mini-batch $\mathcal{B}_k$ of size $B$, $`\mathbf{g}_k = \frac{1}{B} \sum_{i \in \mathcal{B}_k} \nabla \ell_i(\boldsymbol\theta_k)`$, an unbiased estimate whose variance falls as $1/B$. One epoch is one pass through the data. The gradient noise helps escape sharp minima, and the cost per step is independent of $N$.

Momentum accumulates a velocity $\mathbf{v}$ with decay $\beta \in [0, 1)$:

```math
\mathbf{v}_{k+1} = \beta\, \mathbf{v}_k + \mathbf{g}_k,
\qquad \boldsymbol\theta_{k+1} = \boldsymbol\theta_k - \eta\, \mathbf{v}_{k+1}
```

which damps oscillation across narrow valleys of $\mathcal{L}$ and speeds up progress along them; $\beta = 0.9$ is typical.

Adam (Kingma and Ba, 2015) keeps exponential averages of the gradient and of its elementwise square, corrects their bias towards zero at the start, and scales each parameter's step individually:

```math
\mathbf{m}_k = \beta_1 \mathbf{m}_{k-1} + (1 - \beta_1)\, \mathbf{g}_k,
\qquad \mathbf{v}_k = \beta_2 \mathbf{v}_{k-1} + (1 - \beta_2)\, \mathbf{g}_k \odot
\mathbf{g}_k
```

```math
\hat{\mathbf{m}}_k = \frac{\mathbf{m}_k}{1 - \beta_1^k},
\qquad \hat{\mathbf{v}}_k = \frac{\mathbf{v}_k}{1 - \beta_2^k},
\qquad \boldsymbol\theta_k = \boldsymbol\theta_{k-1} - \eta\,
\frac{\hat{\mathbf{m}}_k}{\sqrt{\hat{\mathbf{v}}_k} + \epsilon}
```

with $\mathbf{m}_0 = \mathbf{v}_0 = \mathbf{0}$ and defaults $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$. The step size is roughly $\eta$ per parameter, whatever the gradient scale, which makes Adam forgiving of poorly scaled problems. A constant $\eta$ leaves the iterates bouncing around the minimum; a schedule that decays $\eta$ (step, exponential or cosine) removes this. AdamW decouples weight decay from the adaptive scaling.

For small, full-batch problems such as PINNs, the quasi-Newton method L-BFGS often reaches a lower loss after Adam has found the right basin.

## Initialisation

Weights are drawn randomly so that hidden units differ; biases start at zero. The variance must keep the signals neither vanishing nor exploding through the layers. If the inputs to a layer have variance $\mathrm{Var}(a)$ and the weights are independent with zero mean, then

```math
\mathrm{Var}\big(z^{(l)}_i\big) = n_{l-1}\, \mathrm{Var}\big(W^{(l)}\big)\,
\mathrm{Var}\big(a^{(l-1)}\big)
```

Glorot and Bengio (2010) balanced the forward and backward passes for symmetric activations such as $\tanh$, which gives Xavier initialisation:

$$
\mathrm{Var}\big(W^{(l)}\big) = \frac{2}{n_{l-1} + n_l}
$$

ReLU sets half of its inputs to zero, which halves the variance; He et al. (2015) compensated with

$$
\mathrm{Var}\big(W^{(l)}\big) = \frac{2}{n_{l-1}}
$$

With a variance much larger than these, $\tanh$ units saturate at $\pm 1$, $\sigma' \approx 0$ and training stalls. With a much smaller one, the activations and gradients shrink geometrically with depth.

## Input and Output Scaling

Networks train well when inputs and outputs are of order one. A common map for inputs with known bounds is the min-max map onto $[-1, 1]$, $x' = 2(x - x_{\min})/(x_{\max} - x_{\min}) - 1$; otherwise standardisation $x' = (x - \mu_x)/s_x$ with the training mean $\mu_x$ and standard deviation $s_x$. Outputs are standardised the same way, the network is trained in scaled units, and predictions are mapped back.

Scaling matters for three reasons. A raw Reynolds number of $10^6$ fed into $\tanh$ saturates the first layer for any reasonable initial weight. Badly scaled inputs make the loss surface elongated, which slows every first-order optimiser. And with several outputs (pressure in Pa, velocity in m/s, $k$ in m²/s²) the unscaled MSE is dominated by whichever has the largest numbers. Nondimensional inputs ($Re$, $Ma$, $\alpha$ in radians) and outputs ($C_p$, $\mathbf{u}/U_\infty$) are better still, and quantities spanning decades ($Re$, $\nu_t$) should be log-transformed first. The scaling statistics must come from the training set only, or information from the test set leaks into the model.

## Spectral Bias

Networks trained by gradient descent fit low-frequency components of the target first and high-frequency components much later (Rahaman et al., 2019). The early epochs in the figure below show this: the network first fits a smooth S-curve and resolves the sharp stall peak only after several hundred epochs. Spectral bias acts as a useful implicit regulariser against noise, but it makes shocks, thin shear layers and boundary layers slow to learn when a network represents a field as a function of coordinates. A common remedy maps the inputs through random Fourier features before the first layer (Tancik et al., 2020),

$$
\gamma(\mathbf{x}) = \big[\cos(2\pi B\mathbf{x}),\ \sin(2\pi B\mathbf{x})\big],
\qquad B_{jk} \sim \mathcal{N}(0, s^2)
$$

where the scale $s$ sets the highest frequency the network can easily represent. Other options are adaptive or multiscale sampling and domain decomposition.

## Worked Example: A Lift Curve with Stall

The [MLP regression script](../../../scripts/algorithms/mlp_regression/) fits a 1-32-32-1 $\tanh$ network ($P = 64 + 1056 + 33 = 1153$ parameters) to 60 noisy samples of a synthetic lift curve: the thin-airfoil slope $2\pi\alpha$ blended into the flat-plate value $\sin 2\alpha$ around $14^\circ$, with Gaussian noise of standard deviation 0.03. Twenty further samples form a validation set. Inputs are mapped to $[-1, 1]$, outputs are standardised, weights use Xavier initialisation, and full-batch Adam runs for 2000 epochs with $\eta$ decaying exponentially from $10^{-2}$ to $10^{-4}$.

![MLP prediction of a lift curve at several epochs and the training and validation loss history](../../../scripts/algorithms/mlp_regression/mlp_regression.png)

In the left panel, the prediction after 30 epochs is almost linear. By epoch 150 the network has the right overall shape, but the stall peak is still flattened. By epoch 500 the peak is resolved, and later epochs change little. In the right panel the training MSE falls below the noise variance $\sigma^2 = 9 \times 10^{-4}$ (final RMSE 0.023), while the validation RMSE levels off at 0.038. A training error below the noise level means the network has begun to fit noise; with 1153 parameters and 60 samples this is expected, and [Training and Validation](training_and_validation.md) discusses how regularisation and early stopping control it.

## Other Building Blocks

An MLP treats its input as an unordered vector. Flow data have structure, and the specialised architectures build it in:

- Convolutional neural networks (CNNs) apply the same small kernel $K$ at every grid point, $`(K \ast u)_{ij} = \sum_{m,n} K_{mn}\, u_{i+m,\,j+n}`$. Weight sharing makes the layer equivariant to translation and makes the parameter count independent of grid size. Encoder-decoder CNNs such as the U-Net map a geometry mask or a coarse field to a fine field on a Cartesian grid. They are used for super-resolution, PIV processing and field surrogates ([Neural Networks in Aerodynamics](../neural_networks/intro.md), [Super-Resolution](../flow/superresolution_and_flow_cleansing.md)).
- Autoencoders compress a field into a latent vector, $\mathbf{x} \approx h_{\boldsymbol\psi}(g_{\boldsymbol\phi}(\mathbf{x}))$. A linear autoencoder trained with the MSE spans the same subspace as POD (Baldi and Hornik, 1989), so nonlinear autoencoders are the nonlinear generalisation of [POD](../../numerical/pod/pod_intro.md) ([Flow Feature Extraction](../flow/feature_extraction.md)).
- Recurrent networks propagate a hidden state through time, $`\mathbf{h}_t = \tanh(W_h \mathbf{h}_{t-1} + W_x \mathbf{x}_t + \mathbf{b})`$. Gated variants such as the long short-term memory (LSTM) unit keep gradients usable over long sequences. They serve as time-steppers for reduced coordinates ([Flow Dynamics](../flow/flow_dynamics.md)).
- Graph neural networks pass messages along mesh edges and work directly on unstructured meshes ([Graph Neural Networks](../neural_networks/graph_neural_networks.md)).
- Neural operators learn maps between function spaces, such as from a boundary condition to a solution field, independently of the discretisation ([Neural Operators](../neural_networks/neural_operators.md)).
- Physics-informed networks add the PDE residual to the loss ([PINNs](../neural_networks/pinns.md)).

## Key Takeaways

- An MLP alternates affine maps and elementwise nonlinearities; its parameter count is $\sum_l (n_{l-1} + 1) n_l$ and is often dominated by the output layer when the output is a field.
- Universal approximation guarantees that a wide enough network exists, but it says nothing about finding the network or about generalisation.
- Backpropagation computes all gradients with the recursion $`\boldsymbol\delta^{(l)} = \sigma'(\mathbf{z}^{(l)}) \odot (W^{(l+1)})^T \boldsymbol\delta^{(l+1)}`$ at a cost comparable to the forward pass; check it against central differences.
- Adam with a decaying learning rate is a robust default; L-BFGS can finish small full-batch problems.
- Use Xavier initialisation for $\tanh$ and He initialisation for ReLU, and scale inputs and outputs to order one using training-set statistics only.
- Spectral bias makes networks learn smooth components first; sharp flow features need more training, Fourier features or local refinement.

## Related Scripts

- [MLP Regression](../../../scripts/algorithms/mlp_regression/): A two-hidden-layer tanh network written in numpy, with hand-coded backpropagation and Adam, learns a lift curve with stall from 60 noisy samples.
- [PINN for a 1D Boundary Layer](../../../scripts/algorithms/pinn_boundary_layer/): trains a physics-informed neural network (PINN) on the steady advection–diffusion problem $\varepsilon u'' - u' = 0$, $u(0) = 0$, $u(1) = 1$, whose solution has a boundary layer of width about $\varepsilon$ at $x = 1$.

## Exercises

**Exercise 1.** A surrogate maps 6 shape parameters to $C_d$ through two hidden layers of 64 units. A second network maps the same 6 parameters through two hidden layers of 128 units to the pressure at 10,000 surface nodes. Count the parameters of each.

<details>
<summary>Answer</summary>

Using $P = \sum_l (n_{l-1} + 1) n_l$:

```math
P_1 = 7 \times 64 + 65 \times 64 + 65 \times 1 = 448 + 4160 + 65 = 4673,
```

```math
P_2 = 7 \times 128 + 129 \times 128 + 129 \times 10\,000 = 896 + 16\,512 + 1\,290\,000 = 1\,307\,408 .
```

The output layer holds 99 % of the second network's parameters. This is why field surrogates usually predict a few POD coefficients, or use convolutional or graph decoders, instead of a dense output layer.

</details>

**Exercise 2.** A 1-2-1 network with $\tanh$ hidden units has $W^{(1)} = (0.5, -1)^T$, $\mathbf{b}^{(1)} = (0, 0.5)^T$, $W^{(2)} = (1, 2)$ and $b^{(2)} = 0$. For the sample $x = 1$, $y = 0.5$ and loss $\ell = \tfrac{1}{2}(\hat y - y)^2$, compute the forward pass, all gradients, and the loss after one gradient-descent step with $\eta = 0.1$.

<details>
<summary>Answer</summary>

The forward pass gives $\mathbf{z}^{(1)} = (0.5, -0.5)^T$, $\mathbf{a}^{(1)} = (0.4621, -0.4621)^T$, $\hat y = 0.4621 - 2 \times 0.4621 = -0.4621$, and $\ell = \tfrac{1}{2}(-0.9621)^2 = 0.4628$.

For the output layer, $\delta^{(2)} = \hat y - y = -0.9621$. This gives $\partial\ell/\partial W^{(2)} = \delta^{(2)} (\mathbf{a}^{(1)})^T = (-0.4446, 0.4446)$ and $\partial\ell/\partial b^{(2)} = -0.9621$.

For the hidden layer, $1 - \tanh^2(\pm 0.5) = 0.7864$, so

```math
\boldsymbol\delta^{(1)} = 0.7864 \odot \big( (1, 2)^T \times (-0.9621) \big) = (-0.7567, -1.5133)^T .
```

Since $x = 1$, $\partial\ell/\partial W^{(1)} = \partial\ell/\partial \mathbf{b}^{(1)} = (-0.7567, -1.5133)^T$. A central difference on $W^{(1)}_1$ gives $-0.756655$, which agrees.

After one step with $\eta = 0.1$, the loss falls from 0.4628 to 0.0174.

</details>

**Exercise 3.** Compute the size of the first Adam step ($\eta = 10^{-3}$, default $\beta_1, \beta_2, \epsilon$) for a parameter with gradient $g = 200$ and for one with $g = 0.002$. Compare with the SGD steps $\eta g$.

<details>
<summary>Answer</summary>

At $k = 1$: $m_1 = 0.1 g$ and $v_1 = 0.001 g^2$, so $\hat m_1 = g$ and $\hat v_1 = g^2$. The step is $`\eta\, g / (\lvert g \rvert + \epsilon) \approx \eta\, \mathrm{sign}(g)`$, which is $10^{-3}$ in both cases ($0.99999999 \times 10^{-3}$ and $0.999995 \times 10^{-3}$).

SGD would step $0.2$ and $2 \times 10^{-6}$, a ratio of $10^5$. Adam's per-parameter normalisation is what makes it tolerant of badly scaled gradients, and also why its first steps have size $\eta$ regardless of how close the parameter already is to its optimum.

</details>

**Exercise 4.** A $\tanh$ layer has 64 inputs of unit variance and 64 outputs. (a) What weight standard deviation do Xavier and He initialisation prescribe? (b) If the weights instead have unit variance, what is the standard deviation of the pre-activations, and what fraction of units have $\lvert z \rvert > 2$, where $1 - \tanh^2 z < 0.071$?

<details>
<summary>Answer</summary>

(a) Xavier gives $\sqrt{2/(64 + 64)} = 0.125$. He gives $\sqrt{2/64} = 0.177$ (intended for ReLU).

(b) $\mathrm{Var}(z) = 64 \times 1 \times 1 = 64$, so the standard deviation is 8. Then $P(\lvert z \rvert > 2) = 2(1 - \Phi(2/8)) = 2(1 - \Phi(0.25)) = 0.80$: 80 % of the units are saturated and pass almost no gradient. With Xavier weights $\mathrm{Var}(z) = 1$ and only $`2(1 - \Phi(2)) = 4.6\,\%`$ are saturated.

</details>

**Exercise 5.** Check $\frac{d}{dz}\tanh z$ at $z = 0.5$ with the forward difference $(f(z + h) - f(z))/h$ and the central difference $(f(z + h) - f(z - h))/(2h)$ for $h = 10^{-2}$ and $10^{-3}$. What orders of accuracy do you observe, and why is $h = 10^{-12}$ a bad choice?

<details>
<summary>Answer</summary>

The exact value is $1 - \tanh^2(0.5) = 0.786448$.

| $h$ | Forward | Error | Central | Error |
| --- | --- | --- | --- | --- |
| $10^{-2}$ | 0.782804 | $-3.6 \times 10^{-3}$ | 0.786438 | $-9.4 \times 10^{-6}$ |
| $10^{-3}$ | 0.786084 | $-3.6 \times 10^{-4}$ | 0.786448 | $-9.4 \times 10^{-8}$ |

The forward error falls by 10 when $h$ falls by 10, so it is first order. The central error falls by 100, so it is second order. The leading terms are $\tfrac{h}{2} f''$ and $\tfrac{h^2}{6} f'''$.

With $h = 10^{-12}$ the subtraction $f(z + h) - f(z - h)$ loses about 12 of the 16 significant digits of double precision. The round-off error, roughly $\epsilon_{\mathrm{mach}}/h \approx 10^{-4}$, then dominates. Gradient checks use $h \approx 10^{-6}$ to $10^{-5}$, where the two errors balance.

</details>

## References

- Goodfellow, I., Bengio, Y., and Courville, A., *Deep Learning*, MIT Press, 2016.
- Cybenko, G., "Approximation by Superpositions of a Sigmoidal Function", *Mathematics of Control, Signals and Systems* 2(4), 303-314, 1989.
- Hornik, K., "Approximation Capabilities of Multilayer Feedforward Networks", *Neural Networks* 4(2), 251-257, 1991.
- Leshno, M., Lin, V. Ya., Pinkus, A., and Schocken, S., "Multilayer Feedforward Networks with a Nonpolynomial Activation Function Can Approximate Any Function", *Neural Networks* 6(6), 861-867, 1993.
- Barron, A. R., "Universal Approximation Bounds for Superpositions of a Sigmoidal Function", *IEEE Transactions on Information Theory* 39(3), 930-945, 1993.
- Kingma, D. P., and Ba, J., "Adam: A Method for Stochastic Optimization", *International Conference on Learning Representations*, 2015.
- Glorot, X., and Bengio, Y., "Understanding the Difficulty of Training Deep Feedforward Neural Networks", *Proceedings of the 13th International Conference on Artificial Intelligence and Statistics*, PMLR 9, 249-256, 2010.
- He, K., Zhang, X., Ren, S., and Sun, J., "Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification", *Proceedings of the IEEE International Conference on Computer Vision*, 1026-1034, 2015.
- Rahaman, N., Baratin, A., Arpit, D., Draxler, F., Lin, M., Hamprecht, F., Bengio, Y., and Courville, A., "On the Spectral Bias of Neural Networks", *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97, 5301-5310, 2019.
- Tancik, M., Srinivasan, P. P., Mildenhall, B., et al., "Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains", *Advances in Neural Information Processing Systems* 33, 2020.
- Baldi, P., and Hornik, K., "Neural Networks and Principal Component Analysis: Learning from Examples without Local Minima", *Neural Networks* 2(1), 53-58, 1989.
