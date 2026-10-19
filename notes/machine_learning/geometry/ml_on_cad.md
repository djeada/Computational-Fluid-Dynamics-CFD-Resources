# Machine Learning on CAD

Creating and modifying CAD models for engineering applications is traditionally a manual, time-intensive process requiring specialized expertise. As design spaces grow larger and more complex, manually exploring geometric variations becomes impractical. Machine learning offers the ability to automate CAD generation, create compressed representations of shapes, and even generate new geometries from textual descriptions, dramatically accelerating the early stages of the design pipeline.

Interacting with **Computer-Aided Design (CAD)** models through machine learning can open doors to faster, more flexible design workflows. While direct simulation remains computationally costly, machine learning models can create **compressed representations** of CAD objects, speeding up tasks like shape classification, similarity searches, and even geometry generation. Achieving this, however, demands extensive training data, often requiring simulation software and large-scale data processing to ensure models capture the full complexity of engineered shapes.

```
Traditional CAD Workflow
        ┌─────────────┐      ┌────────────────┐
        │   Design    │─────►│  Manual Edits  │
        └─────────────┘      └────────────────┘
                                   │
                                   ▼
                            ┌────────────────┐
                            │  Simulation    │
                            └────────────────┘
                                   │
                                   ▼
                            ┌────────────────┐
                            │    Refine      │
                            └────────────────┘
                                   │
                                   ▼
                            ┌────────────────┐
                            │  Final Model   │
                            └────────────────┘

------------------------------------------------

ML-Augmented CAD Workflow
        ┌─────────────────────┐      ┌──────────────┐
        │ Text / Parameters   │─────►│   ML Model   │
        └─────────────────────┘      └──────────────┘
                                      │
                                      ▼
                         ┌────────────────────────────┐
                         │ Suggested CAD Geometry     │
                         └────────────────────────────┘
                                      │
                                      ▼
                         ┌────────────────────────────┐
                         │ Validate / Refine Model    │
                         └────────────────────────────┘

```

## Practical Application: CAD Data Generation from Text

Bridging the gap between textual descriptions and CAD geometries offers enormous potential. Imagine specifying "a car-like shape with a streamlined body and four wheels" and receiving a coarse CAD model ready for refinement. Realizing this vision involves integrating **natural language processing (NLP)** with **3D geometry processing** and **generative models** for shape creation.

### CAD Data Generation Pipeline

1. **Data Mining and Labeling**:\
   Start by collecting a rich database of CAD models representing a variety of shapes, from simple boxes to complex automotive bodies. Each model should come with metadata describing geometric features such as edges, faces, and the **center of gravity (COG)**. Manually annotating these models with relevant **keywords** (e.g., "car," "box," "wing") helps create a training set linking text to geometry.

2. **Feature Extraction**:\
   Once data is annotated, extract **geometric properties** (like volume, surface area), **topological properties** (edge-face connectivity), and possibly **physical properties** (mass distribution) if available. These features, along with any known parameters (e.g., shape complexity), form the input space for ML.

3. **Text-to-Geometry Mapping**:\
   Develop algorithms that translate textual descriptions into geometric constraints. NLP converts text into embeddings, capturing the meaning of phrases like "boxy structure" or "car body." The ML model then maps these embeddings to geometric features, effectively learning a function from language to shape descriptors.

4. **Generative Modeling**:\
   With text embeddings guiding the generation, use **generative models** such as **Generative Adversarial Networks (GANs)** or **Variational Autoencoders (VAEs)** to create new CAD geometries. Over time, the model refines its internal representation, producing shapes that closely align with textual inputs.

```
ASCII Diagram: From Text to CAD Model

  Text Input: "A car-like object with a rounded top and four support points"
       |
       v
   NLP Embedding (Word2Vec, BERT)
       |
       v
   ML Model Maps Embedding -> Geometric Feature Space
       |
       v
   Generative Model (GAN/VAE) produces CAD Shape
       |
       v
  Result: Coarse CAD geometry consistent with description
```

## Detailed Steps for Implementation

**Data Collection and Labeling** involves gathering a large, diverse set of CAD models. Each model might be stored in a standard format (e.g., STEP, IGES) and accompanied by metadata. Annotating them with keywords ensures the model learns meaningful correlations (e.g., "car" often correlates with wheels and curved surfaces).

**Feature Extraction** translates raw CAD files into mathematically digestible formats. This may involve computing **geometric descriptors** (lengths, angles), **topological descriptors** (how faces connect), and even **physical properties** (center of gravity if defined). These features bridge the gap between raw polygon data and the structured input ML models require.

**Training the Model** requires a careful setup. Start by using supervised learning to correlate given text descriptions with known CAD features. Over time, the model learns patterns: words like "rounded" might correlate with a set of curvature descriptors, while "boxy" might correlate with rectangular volumes or sharp edges. Validation with hold-out sets ensures the model can generalize to unseen descriptions and shapes.

**Generating Geometry from Text** uses the trained model to produce new CAD concepts from scratch. Embedding textual input, such as a design brief, into a latent space lets the generative model produce a mesh or a parametric description of geometry that matches the requested characteristics. Additional post-processing might convert a rough initial shape into a fully parametric CAD model.

```
ASCII Diagram: Training and Inference Stages

   Training Phase:
     Annotated CAD & Text -> Extract Features & Embeddings -> Train ML Model -> Validate Accuracy
       (Large datasets, long training times)

   Inference (Usage) Phase:
     New Text Input -> NLP Embedding -> ML Model predicts geometry features -> Generate CAD Model
       (Fast runtime, user-friendly interface)
```

## Recommended Algorithms and Techniques

**Natural Language Processing (NLP)**:\
For handling text, models like **Word2Vec** or **BERT** create vector embeddings capturing semantic meaning. Descriptions like "aerodynamic body" or "sturdy base" become numerical vectors that the model can map to geometric features.

**Neural Networks for Geometry**:\
Convolutional Neural Networks (CNNs) excel at analyzing images or voxelized shapes. For CAD, 3D CNNs or graph-based neural networks might process polygon meshes or point clouds. Some approaches convert CAD models into multi-view images, letting 2D CNNs extract features from multiple rendered viewpoints.

**Generative Models**:\
GANs pit a generator (producing shapes) against a discriminator (judging plausibility), refining geometry iteratively. Variational Autoencoders (VAEs) map shapes to a latent space, enabling smooth interpolation between geometric concepts. Conditional versions of these models use textual embeddings as constraints, steering the generated geometry towards desired characteristics.

**Supervised Learning**:\
Initial mapping from text descriptions to geometric descriptors often involves supervised learning, where models learn from pairs of (text, known geometry). Regression or classification techniques can predict continuous shape parameters (e.g., dimensions) or discrete labels (e.g., presence of certain features).

### Further Reading

Deepen your understanding of how machine learning transforms CAD and geometric modeling through a range of foundational texts, seminal papers, and practical resources:

**Books**

- **Deep Learning** by Ian Goodfellow, Yoshua Bengio, and Aaron Courville\
  A comprehensive introduction covering neural network fundamentals and deep learning architectures, forming the theoretical backbone for ML applications in CAD.
- **Pattern Recognition and Machine Learning** by Christopher Bishop\
  An essential resource for statistical methods and machine learning techniques that underpin many modern approaches to shape analysis and 3D modeling.

**Research Papers**

- **MeshCNN: A Network with an Edge** by Hanocka et al. (2019)\
  Explores novel architectures for learning directly on mesh data, which is crucial for processing and optimizing CAD models.
- **Pixel2Mesh: Generating 3D Mesh Models from Single RGB Images** by Wang et al. (2018)\
  Demonstrates how deep learning can reconstruct 3D CAD models from 2D images, bridging computer vision with CAD model generation.
- **Deep Learning for Geometric Shape Understanding** by Han et al.\
  Provides a thorough survey of deep learning techniques applied to the interpretation and processing of geometric data, offering valuable insights into state-of-the-art methods for CAD applications.

## Setting Up the Problem

Building a text-to-CAD pipeline requires careful preparation at each stage:

1. **Collect and annotate CAD models**: Assemble a diverse library spanning simple primitives to complex assemblies. Store models in standard formats (STEP, IGES) and tag each with descriptive keywords, intended application, and geometric metadata.

2. **Extract geometric and topological features**: Compute surface area, volume, curvature distributions, and edge-face connectivity graphs. Normalize features so models of different scales are comparable.

3. **Choose NLP models for text-to-geometry mapping**: Use pretrained embeddings (Word2Vec, BERT) to encode design descriptions. Fine-tune on domain-specific vocabulary (e.g., "fillet," "chamfer," "draft angle") to improve semantic alignment.

4. **Select a generative architecture**: GANs produce sharp, realistic geometries but can be unstable to train. VAEs offer smoother latent spaces and easier interpolation between shapes. Evaluate both on your dataset before committing.

5. **Set up training pipelines**: Define loss functions that combine reconstruction accuracy (Chamfer distance, Earth Mover's distance) with text-alignment terms. Use learning rate schedules, gradient clipping, and checkpoint saving to stabilize long training runs. The Chamfer distance between two point sets $S_1$ and $S_2$ is defined as:

   ```math
   d_{\text{CD}}(S_1, S_2) = \frac{1}{|S_1|}\sum_{x \in S_1} \min_{y \in S_2} \| x -
   y\|^2 + \frac{1}{|S_2|}\sum_{y \in S_2} \min_{x \in S_1} \| y - x\|^2
   ```

   This bidirectional metric penalizes both missing geometry and spurious additions, making it well suited for evaluating generated CAD shapes against reference models.

6. **Validate generated geometries**: Check outputs against engineering constraints such as watertight meshes, minimum wall thickness, and manufacturability rules. Automate validation with scripted checks before passing models downstream.

## Key Takeaways

- Machine learning can dramatically reduce the time required to go from a design concept to an initial CAD geometry.
- High-quality, well-annotated training data is the single most important factor for model performance.
- Combining NLP embeddings with generative models (GANs, VAEs) enables text-driven CAD generation.
- Feature extraction must capture both geometric properties (volume, curvature) and topological relationships (face connectivity).
- Loss functions should balance geometric fidelity with adherence to textual intent and engineering constraints.
- Automated validation against manufacturability rules is essential before generated models enter production workflows.

## Exercises

**Exercise 1.** A generated 2D shape is sampled as $`S_2 = \{(0, 0.1), (1, 0), (2, 0)\}`$ and the reference as $`S_1 = \{(0, 0), (1, 0)\}`$. Compute the Chamfer distance $d_{\text{CD}}(S_1, S_2)$ as defined in the note, and each one-sided term. Which term detects the spurious point?

<details>
<summary>Answer</summary>

$S_1 \to S_2$: $(0,0)$ is nearest to $(0, 0.1)$ with squared distance 0.01, and $(1,0)$ matches exactly. The mean is 0.005.

$S_2 \to S_1$: $(0, 0.1)$ gives 0.01, $(1, 0)$ gives 0, and $(2, 0)$ is nearest to $(1, 0)$ with squared distance 1. The mean is $1.01/3 \approx 0.337$.

$d_{\text{CD}} \approx 0.342$.

The $S_2 \to S_1$ term penalizes the extra geometry. The one-sided $S_1 \to S_2$ term alone (0.005) would rate the shape as nearly perfect.

</details>

**Exercise 2.** Shapes are voxelized as float32 occupancy grids for a 3D CNN. Compute the memory per shape and for a library of 10,000 shapes at $256^3$ and at $64^3$. For a 5 m long car, what is the voxel size in each case?

<details>
<summary>Answer</summary>

$256^3 \times 4$ bytes $\approx 67.1$ MB (64 MiB) per shape, or about 671 GB for 10,000 shapes. The voxel size is $5/256 \approx 1.95$ cm.

$64^3 \times 4$ bytes $\approx 1.05$ MB per shape, or about 10.5 GB in total. The voxel size is $5/64 \approx 7.8$ cm.

The coarse grid is affordable but cannot resolve mirrors, spoiler edges or gaps. The memory cost is a strong reason to use point clouds, meshes or graph representations instead.

</details>

**Exercise 3.** A CAD model has a bounding-box diagonal of 5 m, a volume of 2.4 m³ and a surface area of 30 m². It is scaled to a unit diagonal before feature extraction. Compute the scaled volume and area, and show that $V/A^{3/2}$ is unchanged.

<details>
<summary>Answer</summary>

The scale factor is $s = 0.2$. Volume scales as $s^3$ and area as $s^2$: $V = 2.4 \times 0.008 = 0.0192$ and $A = 30 \times 0.04 = 1.2$.

$V/A^{3/2}$ is $2.4/30^{1.5} \approx 0.0146$ before scaling and $0.0192/1.2^{1.5} \approx 0.0146$ after.

Dimensionless descriptors like this carry shape information that does not depend on size. Size itself can be supplied as a separate feature if it matters (for example, through the Reynolds number).

</details>

**Exercise 4.** A VAE encoder outputs a Gaussian with mean $\mu = 0.5$ and standard deviation $\sigma = 0.8$ for one latent dimension. Compute the KL divergence to the standard normal prior, $\tfrac{1}{2}(\mu^2 + \sigma^2 - 1 - \ln\sigma^2)$. What is the total for a 32-dimensional latent space with identical values in each dimension, and what happens to interpolation if this term is weighted too weakly?

<details>
<summary>Answer</summary>

$\tfrac{1}{2}(0.25 + 0.64 - 1 - \ln 0.64) = \tfrac{1}{2}(-0.11 + 0.446) \approx 0.168$ nats per dimension, or $32 \times 0.168 \approx 5.38$ nats in total.

If the KL term is weighted too weakly, the encoder places shapes in isolated, spread-out regions of latent space. Points between two encoded shapes then decode to geometry the decoder has never learned, and the smooth interpolation the note attributes to VAEs is lost.

</details>

**Exercise 5.** A library has 5,000 CAD models made up of 200 design families with 25 minor variants each. Why is a random 80/10/10 split of models inappropriate, and how would you split?

<details>
<summary>Answer</summary>

Variants within a family are near-duplicates. A random split puts siblings of each test model into the training set, so test accuracy measures recognition of known families rather than generalization to new designs.

Split by family: 160 families (4,000 models) for training, and 20 families (500 models) each for validation and testing. Also remove exact or near-exact duplicates (for example, the same part exported as both STEP and IGES), for instance by thresholding the Chamfer distance between normalized shapes.

</details>

## References

- Kingma, D. P., & Welling, M., "Auto-Encoding Variational Bayes", International Conference on Learning Representations (ICLR), 2014.
- Goodfellow, I., et al., "Generative Adversarial Nets", *Advances in Neural Information Processing Systems* 27, 2014.
- Fan, H., Su, H., & Guibas, L., "A Point Set Generation Network for 3D Object Reconstruction from a Single Image", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017.
- Qi, C. R., Su, H., Mo, K., & Guibas, L. J., "PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017.
- Koch, S., et al., "ABC: A Big CAD Model Dataset for Geometric Deep Learning", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2019.
