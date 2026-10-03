## Example Function in Graph Neural Networks for CFD

Traditional grid-based neural networks struggle with the irregular, unstructured meshes used in industrial CFD. Graph neural networks (GNNs) address this by representing the computational domain as a graph, where nodes correspond to mesh points and edges encode connectivity. This enables learning directly on the native mesh structure, preserving local geometric relationships and capturing flow phenomena that grid-based methods may miss.

Graph neural networks (GNNs) offer a novel approach to predictive modeling in computational fluid dynamics (CFD), moving beyond conventional matrix-based neural architectures. By representing a geometry and its flow domain as a graph of nodes and edges, GNNs can naturally capture local connectivity and complicated geometric features that are often lost in traditional grid-based methods. This graph-based representation is particularly advantageous for unstructured meshes typical in CFD, where local relationships between neighboring cells or nodes play a important role in accurately predicting flow phenomena.

Researchers are rapidly expanding the range of GNN applications by combining open-source tools, diverse datasets, and innovative training strategies. The following sections outline several key focus areas, illustrating current progress in the field, including motivations, practical steps, and typical workflows.

### Extending GNN Applications for CFD

- Enhanced Local Predictions:\
  Early GNN applications in CFD focused on predicting global aerodynamic coefficients, such as drag or lift. However, a current trend is to extend these capabilities to capture finer local flow details, including velocity gradients, boundary layer behavior, shear stress distribution, and the evolution of vortical structures. These local predictions can help identify regions prone to flow separation or recirculation, offering insights for improved turbulence modeling and design optimization.

- Broader Physical Applicability:\
  By capturing localized flow features, GNN-based models may be extended to address multiphase flows, fluid-structure interactions, or even reactive flows where spatial heterogeneities are important. The inherent locality of graph representations makes them a natural candidate for such complicated physical phenomena.

Practical Steps

I. Local Feature Prediction

- Node-Level Learning:\
  Instead of focusing solely on global aerodynamic metrics, the GNN is trained to predict node- or cell-based quantities such as local pressure $p$, wall shear stress $\tau_w$, and turbulent kinetic energy $k$. At each message-passing layer $\ell$, the hidden state of node $v$ is updated by aggregating features from its neighbors:

$$
\mathbf{h}_v^{(\ell+1)} = \phi\!\left(\mathbf{h}_v^{(\ell)},\;
\bigoplus_{u \in \mathcal{N}(v)} \psi\!\left(\mathbf{h}_v^{(\ell)},\,
\mathbf{h}_u^{(\ell)},\, \mathbf{e}_{vu}\right)\right)
$$

where $\phi$ and $\psi$ are learnable functions (typically small MLPs), $\bigoplus$ is a permutation-invariant aggregation (sum, mean, or max), $\mathcal{N}(v)$ denotes the neighbors of $v$, and $\mathbf{e}_{vu}$ are edge features (e.g., relative position and distance). After $L$ layers, the final node embeddings $\mathbf{h}_v^{(L)}$ are passed through a readout network to predict the target field variables. This approach provides a detailed map of the flow field over the entire domain, which can then be integrated to compute global performance metrics.

II. Hybridization with Traditional CFD

- Adaptive Refinement Strategy:\
  A promising hybrid approach involves running coarse CFD simulations to obtain preliminary flow fields and then using the GNN to identify regions with high error or significant flow structures. The CFD solver can then refine only those flagged regions. This focused refinement reduces overall computational cost while maintaining high accuracy where it matters most.

III. Flow Feature Detection

- Classification Tasks:\
  GNNs can be trained to classify or localize specific flow phenomena such as separation zones, recirculation areas, or shear layers. For instance, by labeling regions where flow separation occurs in the training data, the network learns to predict these features automatically, enabling rapid diagnostic analysis during the design phase.

A simplified ASCII illustration of a hybrid pipeline is provided below:

```
         Geometry + Mesh
         +----------+
         |  Points, |
         |  Edges   |
         +-----+----+
               |
               v
+-----------------------------------+
| GNN Model (Graph-based Inference) |
|  Predicts pressure, shear, etc.   |
+-----------+-----------------------+
          |
          v
 Traditional CFD Solver
 Focused on regions flagged
 by the GNN for refinement
```

### Utilizing Open-Source Software

Motivation

- Rapid Prototyping and Community Innovation:\
  Open-source libraries such as PyTorch Geometric, TensorFlow GNN, and the Deep Graph Library (DGL) have revolutionized the way researchers develop and deploy GNN models. Their flexibility and ease of integration allow for quick experimentation with various architectures, while also enabling reproducible research through community-shared codebases.

Practical Steps

I. Graph Data Construction

- Mesh Conversion:\
  The process begins by converting a vehicle surface or volumetric CFD mesh into a graph structure. Each node in the graph represents a spatial point (e.g., a vertex of the mesh), and edges encode the connectivity between these points. Additional features—such as boundary condition flags, turbulence intensity, or local Reynolds numbers—can be attached as node or edge attributes.

II. Model Definition

- Standard GNN Layers:\
  Researchers commonly start with well-set up GNN layers such as Graph Convolutional Networks (GCN), GraphSAGE, or Message Passing Neural Networks (MPNN). These layers are often extended or modified to incorporate domain-specific constraints (e.g., physical symmetries or conservation laws) or to better capture boundary-layer phenomena.

III. Training and Deployment

- Integration with HPC and Containerization:\
  Python-based frameworks help integration with high-performance computing (HPC) clusters, making it easier to monitor training losses and evaluate model performance on large datasets. Once trained, models can be containerized (e.g., via Docker) and integrated into existing Computer-Aided Engineering (CAE) pipelines, making sure smooth deployment in real-world scenarios.

IV. Custom Extensions

- Physics-Informed Enhancements:\
  Advanced applications might incorporate physically inspired loss functions, similar to Physics-Informed Neural Networks (PINNs), which add penalty terms to enforce conservation laws. Additionally, real-world sensor data may be incorporated to update the model periodically, making sure its predictions remain accurate as operational conditions change.

### Experimenting with Various Training Datasets

Motivation

- Generalization Across Diverse Scenarios:\
  A single dataset, regardless of its size, may not capture all the necessary geometric variations, boundary conditions, or operating regimes encountered in practice. Expanding the dataset to include different vehicle classes, multiple angles of attack, and diverse flow conditions boosts the robustness and generalization capability of GNN models.

Practical Steps

I. Dataset Acquisition

- Diverse Geometries:\
  Gather surface or volumetric meshes from a variety of vehicles—including sedans, SUVs, race cars, and concept vehicles—to make sure that the training data covers a wide range of design geometries.

- Varied Flow Conditions:\
  Incorporate multiple simulation cases that vary Reynolds numbers, inlet velocities, turbulence intensities, and even yaw angles for crosswind scenarios.

II. Dataset Partition

- Training, Validation, and Testing:\
  Typically, 80–90% of the data is reserved for training, with the remaining 10–20% used for validation and testing. Some researchers adopt k-fold cross-validation to further assess the variance in model performance.

III. Hardware Constraints

- Memory Management:\
  Large 3D datasets can consist of millions of nodes spread across dozens of geometries, which can be challenging for GPU memory. Strategies such as region sampling or decimation of non-important areas help manage the computational load.

IV. Avoiding Overfitting

- Regularization Techniques:\
  Carry out regularization methods like dropout and weight decay, along with data augmentation strategies (e.g., introducing small geometric perturbations), to improve the model’s generalization. Regular performance checks on withheld or unseen shapes and flow conditions are necessary to detect and mitigate overfitting early.

### GNN Configurations and Setups

Motivation

- Balancing Complexity and Computational Cost:\
  Designing a strong GNN architecture for CFD involves balancing the network's depth and width to capture the complicated relationships between geometry and flow while avoiding issues like overfitting or vanishing gradients. The architecture must also be efficient enough to process large graphs typical of CFD meshes.

Practical Steps

I. Depth and Width

- Trade-Offs:\
  Shallower networks train faster and are less prone to overfitting, but they may lack the capacity to capture subtle 3D flow interactions. Conversely, deeper networks are more expressive but require careful tuning to prevent issues like vanishing gradients and increased computational cost.

II. Message-Passing Schemes

- Aggregation Methods:\
  Carry out message-passing schemes where each node aggregates information from its neighbors. Simple schemes might use uniform averaging, while more advanced methods incorporate attention mechanisms to weigh the importance of different edges, emphasizing key flow features.

III. Hyperparameter Tuning

- Batch Size and Learning Rate:\
  The choice of batch size can influence gradient noise and training stability, while the learning rate must be carefully tuned to make sure steady convergence. Additionally, controlling the number of neighbors each node samples can help moderate training costs, especially in dense graphs.

IV. Residual Connections

- Skip Connections:\
  Incorporating residual connections (inspired by ResNet architectures) helps alleviate vanishing gradient issues and speeds up convergence by allowing information to bypass one or more layers.

V. Pooling and Readout Layers

- Global vs. Local Outputs:\
  Pooling layers (using summation, averaging, or max operations) aggregate node-level features to predict global aerodynamic properties, such as total drag or lift. For tasks requiring detailed local predictions, unpooling layers or maintaining node-level outputs is necessary.

A simple ASCII diagram of a typical GNN architecture for CFD might be:

```
Input Graph (nodes, edges) 
  -> [GraphConv Layer] -> [Activation]  
  -> [GraphConv Layer] -> [Activation]
  -> [Pooling / Summation]
  -> [Dense Layers] -> Output
```

### Efficiency and Accuracy Assessment

Motivation

- Balancing Prediction Speed with Fidelity:\
  While GNNs can offer near real-time predictions once trained, the upfront computational cost in GPU hours can be substantial. Balancing prediction accuracy (e.g., achieving errors within 2–5% compared to high-fidelity CFD) with training efficiency is necessary for practical deployment.

Practical Steps

I. Performance Metrics

- Quantitative Comparison:\
  Evaluate the GNN’s predictions by comparing nodal pressure and velocity fields with reference CFD solutions. Global metrics such as drag coefficient $C_d$ and lift coefficient $C_l$ are also important, along with qualitative assessments of predicted vortex trajectories, flow separation locations, and boundary-layer thickness.

II. Computational Cost Analysis

- Training vs. Inference:\
  While training a GNN may take several hours to days depending on dataset size and model complexity, inference (i.e., making predictions) can be achieved in seconds to minutes, representing a significant speedup over full CFD runs that might take hours.

III. Validation Protocols

- Benchmarking:\
  Many research groups validate their GNN models on standard test cases, such as simplified automotive shapes (e.g., the Ahmed body) or canonical flow cases (e.g., cylinder flows at various Reynolds numbers). These benchmarks provide standardized comparisons and help make sure the model generalizes well.

IV. Error Propagation Analysis

- Local vs. Global Errors:\
  Local prediction inaccuracies can accumulate and lead to larger errors in integrated quantities. Visualization of error fields helps diagnose whether discrepancies occur systematically (e.g., near geometric corners or boundary layers) or randomly, guiding further model refinement.

### Looking Ahead

The collection of efforts outlined above points to a growing convergence between advanced data-driven methods and traditional CFD practices. Graph neural networks, with their natural ability to represent unstructured data and local interactions, are particularly well suited to the inherent challenges of CFD mesh representations. Researchers are actively exploring several exciting avenues, including:

- Hybrid GNN-PINN Approaches:\
  Embedding partial differential equation (PDE) residuals directly into the training loss of GNNs can further enforce physical constraints and improve predictive reliability.

- Coupled Multiphysics Modeling:\
  Extending GNNs to handle coupled problems, such as aero-thermal interactions or fluid-structure dynamics, offers the potential for more comprehensive simulation frameworks.

- Real-Time Design Optimization:\
  Deploying GNN-based surrogates in real-time sensitivity analyses or shape optimization loops can drastically shorten design cycles, enabling faster iterations and more innovative designs.

### Setting Up the Problem

1. **Mesh-to-Graph Conversion:** Use libraries such as PyTorch Geometric or DGL to convert CFD surface and volumetric meshes into graph structures. Each mesh vertex becomes a node, and element connectivity defines the edges.
2. **Feature Definition:** Assign node features from flow variables (pressure, velocity components, turbulence quantities) and geometric attributes (surface normals, curvature). Edge features can encode distances and relative positions between connected nodes.
3. **Architecture Selection:** Choose a GNN backbone suited to the task—GCN for simple diffusion-like problems, GraphSAGE for inductive learning across unseen geometries, or MPNN for richer edge-level message passing.
4. **Dataset Preparation:** Assemble training data spanning diverse vehicle shapes (sedans, SUVs, trucks), Reynolds numbers, yaw angles, and turbulence intensities. Ensure a balanced split across training, validation, and test sets.
5. **Training Strategy:** Train with physics-aware loss functions combining mean squared error on nodal quantities with penalty terms for conservation law residuals. Use learning rate schedulers and early stopping to avoid overfitting.
6. **Benchmarking:** Validate predictions against high-fidelity CFD reference solutions on standard test cases (e.g., Ahmed body, DrivAer model). Compare drag and lift coefficients as well as local pressure and shear stress distributions.

### Key Takeaways

- GNNs operate directly on unstructured CFD meshes, eliminating the need for costly interpolation onto regular grids.
- Graph-based representations naturally preserve local connectivity and geometric detail critical for accurate flow prediction.
- Open-source frameworks (PyTorch Geometric, DGL) accelerate prototyping, while containerized deployment integrates trained models into existing CAE pipelines.
- Diverse training datasets covering a wide range of geometries and flow conditions are essential for robust generalization.
- Hybrid GNN–CFD workflows, where coarse simulations are selectively refined using GNN guidance, balance computational cost with prediction fidelity.
- Careful architecture design—including message-passing scheme selection, residual connections, and pooling strategy—directly impacts both accuracy and scalability.

### Exercises

**Exercise 1.** In the message-passing update from the note, the hidden size is 64, the edge features $\mathbf{e}_{vu}$ have 3 components, and $\psi$ and $\phi$ are each a single linear layer with bias. $\psi$ takes $(\mathbf{h}_v, \mathbf{h}_u, \mathbf{e}_{vu})$; $\phi$ takes $\mathbf{h}_v$ and the 64-dimensional aggregated message. Count the parameters per layer and for $L = 10$ layers with unshared weights.

<details>
<summary>Answer</summary>

$\psi$: input $64 + 64 + 3 = 131$, output 64, so $131 \times 64 + 64 = 8{,}448$ parameters.

$\phi$: input $64 + 64 = 128$, output 64, so $128 \times 64 + 64 = 8{,}256$ parameters.

That is 16,704 per layer and 167,040 for 10 layers. Real models use small MLPs for $\psi$ and $\phi$, which multiplies these numbers, but the count still does not depend on the mesh size.

</details>

**Exercise 2.** A volume mesh has a typical edge length of 5 mm near the car, and wake effects extend about 2 m downstream. How many message-passing layers would information need to cross 2 m? A multi-scale graph coarsens the edge length by a factor of 4 per level. What edge length does the fourth level have?

<details>
<summary>Answer</summary>

$2/0.005 = 400$ hops, so 400 layers. A 10-layer GNN only reaches about 5 cm.

After four coarsening levels the edge length is $0.005 \times 4^4 = 1.28$ m, so a few layers at that level span the whole wake. This is the motivation for the multi-scale graphs mentioned in the note.

</details>

**Exercise 3.** A node receives the messages 1, 4 and 2 from its neighbours. Compute the sum, mean and max aggregations. After mesh refinement every neighbour's message appears twice. Which aggregations change, and what does that imply for training on meshes of varying resolution?

<details>
<summary>Answer</summary>

Before refinement: sum 7, mean 2.33, max 4.

After duplication: sum 14, mean 2.33, max 4.

Sum aggregation depends on node degree, and so on local mesh density, so a model trained on one resolution can fail on another. Mean and max do not change. Sum keeps information about how many neighbours there are, which can be useful, but mean or max (or normalized sums) are more robust to changes in resolution.

</details>

**Exercise 4.** A closed, triangulated car surface has $V = 500{,}000$ vertices. Use Euler's formula to estimate the number of undirected edges, then compute the memory for directed edges with 3 float32 features each and an int64 edge index.

<details>
<summary>Answer</summary>

For a closed genus-0 triangulation, $V - E + F = 2$ and $3F = 2E$, so $E = 3V - 6 \approx 1.5 \times 10^6$ undirected edges.

Message passing uses both directions, about $3 \times 10^6$ directed edges.

Edge features: $3 \times 10^6 \times 3 \times 4$ bytes $= 36$ MB. Edge index: $3 \times 10^6 \times 2 \times 8$ bytes $= 48$ MB.

Volume meshes with tens of millions of cells multiply this, which is why the note recommends region sampling or decimation.

</details>

**Exercise 5.** The pressure drag coefficient is $C_{D,p} = -\frac{1}{A_{\text{ref}}}\oint C_p\, n_x \, dA$, with outward normal $\mathbf{n}$ and flow in the $+x$ direction. A GNN predicts nodal $C_p$ with (a) a uniform bias of $+0.02$ over the whole surface, or (b) a bias of $+0.02$ only on the front-facing surfaces, whose projected frontal area equals $A_{\text{ref}}$. What error in $C_{D,p}$ does each case cause? Express (b) relative to $C_D = 0.31$.

<details>
<summary>Answer</summary>

(a) $\Delta C_{D,p} = -\frac{0.02}{A_{\text{ref}}}\oint n_x\, dA = 0$, because $\oint \mathbf{n}\, dA = 0$ for any closed surface. A uniform bias cancels exactly.

(b) On the front-facing surfaces $\int n_x\, dA = -A_{\text{ref}}$, so $\Delta C_{D,p} = -\frac{0.02}{A_{\text{ref}}}(-A_{\text{ref}}) = +0.02$. That is about 6.5% of $C_D = 0.31$.

Local error maps matter more than average nodal error. Errors that are correlated with the direction of the surface normal cause the errors in integrated forces.

</details>

### References

- Gilmer, J., Schütt, K. T., Riley, P. F., Vinyals, O., & Dahl, G. E., "Neural Message Passing for Quantum Chemistry", International Conference on Machine Learning (ICML), 2017.
- Battaglia, P. W., et al., "Relational inductive biases, deep learning, and graph networks", arXiv:1806.01261, 2018.
- Kipf, T. N., & Welling, M., "Semi-Supervised Classification with Graph Convolutional Networks", International Conference on Learning Representations (ICLR), 2017.
- Hamilton, W. L., Ying, R., & Leskovec, J., "Inductive Representation Learning on Large Graphs", *Advances in Neural Information Processing Systems* 30, 2017.
- Pfaff, T., Fortunato, M., Sanchez-Gonzalez, A., & Battaglia, P. W., "Learning Mesh-Based Simulation with Graph Networks", International Conference on Learning Representations (ICLR), 2021.
