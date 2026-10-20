# Graph Neural Networks for CFD

Industrial CFD runs on unstructured meshes with strong clustering near walls, and grid-based networks need the solution interpolated onto a Cartesian grid first. A graph neural network (GNN) instead treats the mesh as a graph and learns on it directly, so it predicts fields at the solver's own nodes for meshes of any size and topology. This note sets up the learning problem on a mesh graph, derives the encode-process-decode architecture and its message-passing equations, relates message passing to finite-volume fluxes, and covers the receptive-field limit, invariances, autoregressive rollout, losses and memory cost.

## Problem Statement

A mesh defines a graph $G = (V, E)$ with nodes $v \in V$ (mesh vertices or cells) and directed edges $(u, v) \in E$ joining neighbours; every undirected mesh edge appears in both directions. Each node carries a feature vector $`\mathbf{x}_v`$ and each edge a feature vector $`\mathbf{e}_{uv}`$:

- node features: a one-hot node type (fluid, wall, inlet, outlet, far field), boundary-condition values, global operating conditions such as $Re$ or the free-stream vector, and, for unsteady problems, the current state $\mathbf{q}_v^n$ (velocity $\mathbf{u}$, pressure $p$, turbulence variables);
- edge features: the relative displacement $\mathbf{x}_u - \mathbf{x}_v$ and the distance $`\|\mathbf{x}_u - \mathbf{x}_v\|`$, so that no absolute position enters the model.

Two tasks are common. In the steady task the network predicts the converged fields $`\hat{\mathbf{y}}_v = f_{\boldsymbol\theta}(G)_v`$ at every node, from which forces follow by surface integration. In the unsteady task it predicts the state increment over one time step,

```math
\hat{\mathbf{q}}_v^{n+1} = \mathbf{q}_v^{n} + \Delta t\, f_{\boldsymbol\theta}\bigl(G, \mathbf{q}^{n}\bigr)_v
```

and is applied repeatedly to produce a trajectory. The data are $N$ solutions or trajectories $`\mathcal{D} = \{(G_i, \mathbf{y}_i)\}_{i=1}^N`$, each on its own mesh, and the parameters $\boldsymbol\theta$ minimise the node-weighted error

```math
\mathcal{L}(\boldsymbol\theta) = \frac{1}{N}\sum_{i=1}^{N} \frac{\sum_{v \in V_i} w_v \bigl\| f_{\boldsymbol\theta}(G_i)_v - \mathbf{y}_{i,v} \bigr\|^2}{\sum_{v \in V_i} w_v}
```

with $w_v$ the cell volume or face area of node $v$ (or $w_v = 1$), applied to normalised targets.

The difficulties are specific to meshes. Graph sizes vary between samples and reach $10^6$ to $10^8$ nodes in 3D. The pressure field of incompressible flow depends on the whole domain, but a GNN layer only moves information one edge. Rollouts feed the model its own errors. Memory grows with the number of edges times the number of layers.

## From Mesh to Graph

There are two natural graphs on a mesh, and the choice should follow how the CFD data are stored.

| Choice | Nodes | Edges | Matches | Remarks |
| --- | --- | --- | --- | --- |
| Vertex graph | Mesh vertices | Element edges | Vertex-centred and finite-element solvers, surface meshes | Average degree about 6 on triangle meshes and about 14 on tetrahedral meshes |
| Cell-centred (dual) graph | Cells | Shared faces | Cell-centred finite-volume solvers such as OpenFOAM and Fluent | Degree equals the number of faces (3, 4 or 6); face normal and area are natural edge features |

For surface quantities ($C_p$, $C_f$) a surface mesh is enough and much smaller than the volume mesh. Wall nodes should be flagged so that the network can treat them differently, and the free-stream direction should enter as a feature rather than through absolute coordinates. Very large meshes are usually coarsened or subsampled for training, which changes the mesh density the model sees; see [machine learning on meshes](../geometry/ml_with_meshes.md).

## Encode-Process-Decode Architecture

Most mesh GNNs for CFD, including MeshGraphNets (Pfaff et al., 2021) and the particle simulator of Sanchez-Gonzalez et al. (2020), follow the encode-process-decode scheme of the graph-network framework (Battaglia et al., 2018).

The encoder embeds node and edge features into a latent space of width $d$ with two MLPs:

```math
\mathbf{h}_v^{0} = \varepsilon^{V}(\mathbf{x}_v), \qquad \mathbf{e}_{uv}^{0} = \varepsilon^{E}(\mathbf{e}_{uv})
```

The processor applies $L$ message-passing layers. Layer $\ell$ first updates every edge from its two end nodes, then sums the incoming edges at each node, then updates the node:

```math
\mathbf{e}_{uv}^{\ell+1} = \mathbf{e}_{uv}^{\ell} + \phi^{E}_{\ell}\bigl(\mathbf{e}_{uv}^{\ell}, \mathbf{h}_u^{\ell}, \mathbf{h}_v^{\ell}\bigr)
```

```math
\mathbf{m}_v^{\ell+1} = \bigoplus_{u \in \mathcal{N}(v)} \mathbf{e}_{uv}^{\ell+1}
```

```math
\mathbf{h}_v^{\ell+1} = \mathbf{h}_v^{\ell} + \phi^{V}_{\ell}\bigl(\mathbf{h}_v^{\ell}, \mathbf{m}_v^{\ell+1}\bigr)
```

Here $\mathcal{N}(v)$ is the set of nodes with an edge into $v$, $\bigoplus$ is a permutation-invariant aggregation (sum, mean or max), and $`\phi^{E}_{\ell}`$, $`\phi^{V}_{\ell}`$ are MLPs, typically with two hidden layers and layer normalisation. The residual form keeps deep stacks trainable. MeshGraphNets uses a latent width of 128 and about 15 processor layers with unshared weights.

The decoder maps the final node state to the output, $\hat{\mathbf{y}}_v = \delta(\mathbf{h}_v^{L})$, for example the pressure and velocity at the node or their time derivatives. A global quantity such as $C_d$ is better obtained by integrating predicted surface $C_p$ and $C_f$ than by pooling node states into a single vector, because the integral is exact given the fields and the fields provide many training targets per simulation.

Earlier formulations are special cases. The message-passing neural network of Gilmer et al. (2017) has a message function, a vertex update and a readout, the same three steps without persistent edge states. The graph convolutional network of Kipf and Welling (2017) uses a fixed linear message,

```math
H^{\ell+1} = \sigma\bigl(\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2} H^{\ell} W^{\ell}\bigr)
```

where $\tilde{A} = A + I$ is the adjacency matrix with self-loops, $\tilde{D}$ its degree matrix, $H^{\ell}$ the matrix of node states and $W^{\ell}$ a weight matrix. GCN ignores edge features, so it cannot use the relative positions that carry the mesh geometry, and it is rarely used for flow prediction. GraphSAGE (Hamilton et al., 2017) samples a fixed number of neighbours per node, which bounds the cost on high-degree graphs.

## Message Passing as a Learned Flux

A cell-centred finite-volume scheme updates cell $v$ of volume $V_v$ from fluxes through its faces:

```math
V_v \frac{d\mathbf{q}_v}{dt} = -\sum_{u \in \mathcal{N}(v)} \mathbf{F}\bigl(\mathbf{q}_v, \mathbf{q}_u, \mathbf{n}_{vu}\bigr) A_{vu}
```

with face normal $`\mathbf{n}_{vu}`$, face area $`A_{vu}`$ and numerical flux $\mathbf{F}$ (Versteeg and Malalasekera, 2007). This has exactly the structure of one message-passing layer: the edge update computes a flux from the two adjacent states and the face geometry, the aggregation sums the fluxes, and the node update integrates in time. A GNN layer can therefore be read as a learned flux and update, and a stack of $L$ layers as $L$ substeps of a learned explicit scheme.

The analogy also shows what a generic GNN lacks. A finite-volume flux is antisymmetric, $`\mathbf{F}(\mathbf{q}_v, \mathbf{q}_u, \mathbf{n}_{vu}) = -\mathbf{F}(\mathbf{q}_u, \mathbf{q}_v, \mathbf{n}_{uv})`$, so whatever leaves one cell enters its neighbour and the total is conserved. The learned edge function $\phi^{E}$ has no such property. Conservation can be built in by using the antisymmetric message $`\mathbf{g}(\mathbf{h}_u, \mathbf{h}_v, \mathbf{e}_{uv}) - \mathbf{g}(\mathbf{h}_v, \mathbf{h}_u, \mathbf{e}_{vu})`$, whose sum over all directed edges is zero.

The figure shows the linear case. With messages $w_{uv}(h_u - h_v)$, where $w_{uv}$ are the cotangent weights of the piecewise-linear Laplacian, and the update $`h_v \leftarrow h_v + (\Delta t\,\kappa / A_v) \sum_u w_{uv}(h_u - h_v)`$ with control-volume area $A_v$ and diffusivity $\kappa$, message passing is a vertex-centred finite-volume scheme for $\partial h/\partial t = \kappa \nabla^2 h$. The integral $\sum_v A_v h_v$ changes only by round-off ($2 \times 10^{-16}$ relative over 438 steps), and the spread of a Gaussian follows the exact $\sigma_0^2 + 2\kappa t$ until it reaches the no-flux cylinder wall.

![Message-passing diffusion of a Gaussian blob on the cylinder mesh](../../../scripts/plots/gnn_message_passing/gnn_message_passing_diffusion.png)

## Receptive Field and Multi-Scale Graphs

After $k$ layers, node $v$ depends only on the nodes within $k$ hops, its receptive field. The first figure shows this on a graded cylinder mesh with 1326 nodes: 8 layers reach 148 nodes (11 %) and cover less than one diameter, because the mesh is finest exactly where the flow is most interesting. Half of the nodes are reached after 19 hops and all of them after 35, and the hop map shows that information from the near wake reaches the upstream region only by travelling around the body.

![Receptive field of a wake node after 1, 2, 4 and 8 message-passing steps](../../../scripts/plots/gnn_message_passing/gnn_message_passing.png)

Two physical arguments bound the number of layers needed. In an unsteady problem, a disturbance travels about $`a\,\Delta t`$ in one model step, with $a$ the fastest signal speed, so the processor needs $`L \gtrsim a\,\Delta t / \Delta x_{\min}`$ layers, a CFL condition for the network. For steady incompressible flow the pressure satisfies an elliptic equation, every node depends on the whole domain, and $L$ would have to be of the order of the graph diameter, hundreds of layers on a fine 3D mesh. Memory grows linearly with $L$, so the remedy is a hierarchy of graphs instead of a deeper stack. A multi-scale GNN coarsens the graph by a factor $r$ in edge length per level, passes messages on each level, and interpolates back with skip connections, like a graph U-Net (Gao and Ji, 2019) or a multigrid cycle. A hop at level $l$ covers $r^l$ fine-level edge lengths.

Deep message-passing stacks also suffer from over-smoothing: repeated averaging drives node states towards each other, as diffusion does in the figure. Residual updates, normalisation and multi-scale hierarchies limit it.

## Invariances

A flow surrogate should not depend on where the mesh sits in space or on how the nodes are numbered.

- Permutation equivariance holds by construction, because the aggregation is symmetric and the same MLPs are applied to every node and edge.
- Translation invariance follows from using only relative displacements in the edge features and leaving absolute coordinates out of the node features.
- Rotation is not handled by relative displacements alone, since they rotate with the mesh. The usual remedies are random rotations of the training graphs (data augmentation), local coordinate frames attached to each edge or face, or rotation-equivariant layers. When gravity or the free stream defines a preferred direction, that vector is passed as a feature and rotated with the mesh.
- Scale changes are handled by non-dimensionalising lengths by a reference length and fields by free-stream values, so that $Re$ rather than the mesh units is the input.

## Autoregressive Rollout and Error Accumulation

An unsteady GNN is trained on pairs $(\mathbf{q}^n, \mathbf{q}^{n+1})$ from the reference trajectories and then rolled out from an initial state for $T$ steps. If the one-step error is at most $\varepsilon$ and the learned map has Lipschitz constant $\rho$ in the state, the error after $n$ steps is bounded by

```math
\|\mathbf{e}^{n}\| \le \varepsilon \sum_{k=0}^{n-1}\rho^{k} = \varepsilon\,\frac{\rho^{n} - 1}{\rho - 1}
```

which grows linearly for $\rho = 1$ and exponentially for $\rho > 1$. A second problem is distribution shift: during rollout the input is the model's own prediction, which drifts away from the states seen in training. Sanchez-Gonzalez et al. (2020) and Pfaff et al. (2021) inject Gaussian noise of a chosen variance into the input state during training and keep the target at the clean next state, so the network learns to remove the perturbation and the rollout stays close to the data. Training through several unrolled steps does the same more directly at a higher memory cost, the approach of solver-in-the-loop training described in the [surrogates note](intro.md#hybrid-solver-network-methods). Rollout quality is judged on long horizons, for example the shedding frequency and the time-averaged fields, not on the one-step error.

## Training Losses

- The one-step loss is the mean squared error of the predicted increment, with inputs and targets normalised per feature by statistics accumulated over the training set.
- For steady fields the area- or volume-weighted loss of the problem statement stops the boundary layer, where most nodes are, from dominating.
- A physics penalty adds a discrete residual, for example the divergence $`\sum_u (\mathbf{u}_u + \mathbf{u}_v)/2 \cdot \mathbf{n}_{vu} A_{vu}`$ at each cell, evaluated with the mesh operators; see [physics-informed neural networks](pinns.md).
- A force loss adds the error of the integrated $C_d$ and $C_l$, which weights the surface errors that actually change the forces (Exercise 5).

## Cost and Memory

One processor layer evaluates $\phi^{E}$ once per directed edge and $\phi^{V}$ once per node. For MLPs of width $d$ the cost is $`O\bigl((|E| + |V|)\,d^2\bigr)`$ per layer, linear in the mesh size, and the number of parameters does not depend on the mesh at all. Training needs the activations of every layer for backpropagation, at least $`L(|E| + |V|)\,d`$ numbers. For a tetrahedral mesh with $|V| = 10^6$ vertices and about $14 \times 10^6$ directed edges, $d = 128$ and $L = 15$, that is $15 \times 15 \times 10^6 \times 128 \times 4$ bytes $\approx 115$ GB in float32, more than one GPU holds. Large cases are trained on subgraphs or coarsened meshes, with gradient checkpointing, or across several GPUs with the graph partitioned like a domain decomposition, and inference can run on the full mesh because it stores only the current layer.

PyTorch Geometric (Fey and Lenssen, 2019) and the Deep Graph Library (Wang et al., 2019) provide sparse scatter-gather operations, standard layers (GCN, GraphSAGE, graph attention, generic message passing) and mini-batching of graphs of different sizes. Mesh conversion is a few lines: read the cells, build the edge index from element connectivity, and compute the edge features.

## Key Takeaways

- A mesh is a graph with node types, boundary flags and state as node features and relative displacements as edge features; vertex graphs suit vertex-centred data, dual graphs suit cell-centred finite-volume data.
- Encode-process-decode GNNs alternate edge updates, permutation-invariant aggregation and node updates; the parameter count is independent of the mesh size.
- One message-passing layer has the structure of a finite-volume update with a learned flux; antisymmetric messages make it conservative.
- $L$ layers see $L$ hops, which on a graded mesh is a small neighbourhood, so elliptic and long-range effects need multi-scale graphs.
- Autoregressive rollouts accumulate error; noise injection or multi-step training keeps them stable.
- Training memory scales with layers times edges times width and limits single-GPU training to meshes of about $10^5$ to $10^6$ nodes.

## Related Scripts

- [GNN Message Passing on a Cylinder Mesh](../../../scripts/plots/gnn_message_passing/): This script shows how far information travels through a graph neural network on an unstructured CFD mesh, and that a linear message-passing layer with the right weights is a finite-volume diffusion scheme.
- [Surrogate Input Representations](../../../scripts/plots/surrogate_input_representations/): This script draws one NACA 2412 airfoil in the four forms a neural-network surrogate can take as input: a parameter vector, a signed distance field on a Cartesian grid, a surface point cloud, and a mesh graph.

## Exercises

**Exercise 1.** In the message-passing layer the latent width is 64, the edge features have 3 components, and $\phi^{E}$ and $\phi^{V}$ are each a single linear layer with bias. $\phi^{E}$ takes $`(\mathbf{h}_v, \mathbf{h}_u, \mathbf{e}_{uv})`$ and returns a 64-dimensional message; $\phi^{V}$ takes $\mathbf{h}_v$ and the 64-dimensional aggregate. Count the parameters per layer and for $L = 10$ layers with unshared weights.

<details>
<summary>Answer</summary>

$\phi^{E}$: input $64 + 64 + 3 = 131$, output 64, so $131 \times 64 + 64 = 8{,}448$ parameters.

$\phi^{V}$: input $64 + 64 = 128$, output 64, so $128 \times 64 + 64 = 8{,}256$ parameters.

That is 16,704 per layer and 167,040 for 10 layers. Real models use small MLPs for both functions, which multiplies these numbers, but the count still does not depend on the number of nodes or edges.

</details>

**Exercise 2.** A volume mesh has a typical edge length of 5 mm near a car, and the wake extends about 2 m downstream. How many message-passing layers would information need to cross 2 m on this mesh? A multi-scale graph coarsens the edge length by a factor of 4 per level. What edge length does the fourth level have?

<details>
<summary>Answer</summary>

$2/0.005 = 400$ hops, so 400 layers; a 10-layer GNN reaches only about $10 \times 0.005 = 0.05$ m.

After four coarsening levels the edge length is $0.005 \times 4^4 = 1.28$ m, so two hops on that level span the wake. This is why multi-scale graphs are used instead of deeper processors.

</details>

**Exercise 3.** A node receives the messages 1, 4 and 2 from its neighbours. Compute the sum, mean and max aggregations. After mesh refinement every neighbour's message appears twice. Which aggregations change, and what does that imply for training on meshes of varying resolution?

<details>
<summary>Answer</summary>

Before refinement: sum 7, mean 2.33, max 4. After duplication: sum 14, mean 2.33, max 4.

The sum depends on the node degree, and so on the local mesh density, so a model trained with sum aggregation at one resolution can fail at another. Mean and max do not change. The finite-volume analogy shows why a sum can still be right: fluxes add over faces, but they are weighted by face areas, which shrink when the mesh is refined. Area-weighted sums, or mean aggregation with the degree as an extra feature, are robust to resolution changes.

</details>

**Exercise 4.** A closed, triangulated car surface has $V = 500{,}000$ vertices. Use Euler's formula to find the number of undirected edges, then compute the memory for the directed edges with 3 float32 features each and an int64 edge index of two rows.

<details>
<summary>Answer</summary>

For a closed genus-0 triangulation, $V - E + F = 2$ and $3F = 2E$, so $E = 3V - 6 = 1{,}499{,}994 \approx 1.5 \times 10^6$ undirected edges and about $3 \times 10^6$ directed edges.

Edge features: $3 \times 10^6 \times 3 \times 4$ bytes $= 36$ MB. Edge index: $3 \times 10^6 \times 2 \times 8$ bytes $= 48$ MB.

These are inputs only. The latent edge states of a $d = 128$, $L = 15$ processor need $15 \times 3 \times 10^6 \times 128 \times 4$ bytes $\approx 23$ GB for training, which is why large meshes are subsampled or partitioned.

</details>

**Exercise 5.** The pressure drag coefficient is $`C_{D,p} = -\frac{1}{A_{\mathrm{ref}}}\oint C_p\, n_x \, dA`$, with outward normal $\mathbf{n}$ and flow in the $+x$ direction. A GNN predicts nodal $C_p$ with (a) a uniform bias of $+0.02$ over the whole surface, or (b) a bias of $+0.02$ only on the front-facing surfaces, whose projected frontal area equals $A_{\mathrm{ref}}$. What error in $C_{D,p}$ does each case cause? Express (b) relative to $C_D = 0.31$.

<details>
<summary>Answer</summary>

(a) For a closed surface $`\oint \mathbf{n}\, dA = \mathbf{0}`$, so

```math
\Delta C_{D,p} = -\frac{0.02}{A_{\mathrm{ref}}}\oint n_x\, dA = 0
```

A uniform bias cancels exactly.

(b) On the front-facing surfaces $n_x < 0$ and $`\int n_x\, dA = -A_{\mathrm{ref}}`$, so

```math
\Delta C_{D,p} = -\frac{0.02}{A_{\mathrm{ref}}}\left(-A_{\mathrm{ref}}\right) = +0.02
```

That is about 6.5 % of $C_D = 0.31$, or 200 drag counts. The mean nodal error is the same in both cases; what matters for forces is how the error correlates with the surface normal. This is why integrated forces should be part of the validation, and possibly of the loss.

</details>

## References

- Battaglia, P. W., Hamrick, J. B., Bapst, V., et al., "Relational inductive biases, deep learning, and graph networks", arXiv:1806.01261, 2018.
- Gilmer, J., Schoenholz, S. S., Riley, P. F., Vinyals, O., & Dahl, G. E., "Neural Message Passing for Quantum Chemistry", *Proceedings of the 34th International Conference on Machine Learning (ICML)*, PMLR 70, pp. 1263–1272, 2017.
- Kipf, T. N., & Welling, M., "Semi-Supervised Classification with Graph Convolutional Networks", *International Conference on Learning Representations (ICLR)*, 2017.
- Hamilton, W. L., Ying, R., & Leskovec, J., "Inductive Representation Learning on Large Graphs", *Advances in Neural Information Processing Systems* 30, 2017.
- Sanchez-Gonzalez, A., Godwin, J., Pfaff, T., Ying, R., Leskovec, J., & Battaglia, P. W., "Learning to Simulate Complex Physics with Graph Networks", *Proceedings of the 37th International Conference on Machine Learning (ICML)*, PMLR 119, pp. 8459–8468, 2020.
- Pfaff, T., Fortunato, M., Sanchez-Gonzalez, A., & Battaglia, P. W., "Learning Mesh-Based Simulation with Graph Networks", *International Conference on Learning Representations (ICLR)*, 2021.
- Gao, H., & Ji, S., "Graph U-Nets", *Proceedings of the 36th International Conference on Machine Learning (ICML)*, PMLR 97, pp. 2083–2092, 2019.
- Fey, M., & Lenssen, J. E., "Fast Graph Representation Learning with PyTorch Geometric", ICLR Workshop on Representation Learning on Graphs and Manifolds, 2019.
- Wang, M., Zheng, D., Ye, Z., et al., "Deep Graph Library: A Graph-Centric, Highly-Performant Package for Graph Neural Networks", arXiv:1909.01315, 2019.
- Versteeg, H. K., & Malalasekera, W., *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd edition, Pearson Education, 2007.
