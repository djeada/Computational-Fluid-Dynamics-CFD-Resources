## Machine Learning in Particle Image Velocimetry (PIV)

Traditional PIV processing relies on **cross-correlation algorithms** that can be slow, sensitive to noise, and require careful manual tuning of parameters like interrogation window size and seeding density. As experimental setups become more complex and real-time feedback is demanded, these limitations create bottlenecks. Machine learning automates and accelerates PIV processing—from feature detection and velocity reconstruction to noise removal and uncertainty quantification—enabling faster, more reliable, and more insightful flow measurements.

Integrating **machine learning (ML)** with **particle image velocimetry (PIV)** enhances the ability to measure and interpret fluid flows. PIV traditionally relies on analyzing tracer particles in fluids illuminated by lasers and recorded in high-speed images. ML steps in to streamline processing, reduce noise, extract subtle features, and even aid in experimental setup. By combining PIV’s well-established measurement techniques with data-driven models, researchers can gain deeper insights into complex flows faster and with higher reliability.

```
ASCII Diagram: Traditional vs. ML-Augmented PIV Workflow

   Traditional PIV:
     Laser Illumination -> Capture Particle Images -> Cross-Correlation -> Velocity Fields
         (Time-consuming, manual adjustments, noise-sensitive)

   ML-Augmented PIV:
     Laser Illumination -> Capture Particle Images -> ML Model Processes Images -> Velocity Fields & Insights
         (Faster, automated feature extraction, improved accuracy)
```

### Feature Detection and Tracking

**Objective:** Identify and follow evolving fluid structures, like **vortices**, **shear layers**, or **coherent patterns**, as they move through the flow field.

**Approach:**\
Automated detection techniques use ML algorithms trained to recognize characteristic flow features in sequential PIV images. These algorithms learn to distinguish meaningful structures from background noise or random particle distributions. Once a structure is identified, the algorithm can track it over time, revealing patterns in how it moves, forms, and dissipates.

**Benefit:**\
This automation saves researchers from manually inspecting large volumes of data and provides a richer picture of flow dynamics, allowing for quick identification of phenomena like vortex shedding or boundary layer development.

```
ASCII Diagram: Feature Tracking in PIV

     Frame t=1:   * *    vortex forming
     Frame t=2:     * *   vortex moves right
     Frame t=3:       * * vortex tracked via ML

   * = tracer particles
   ML detects pattern continuity and movement
```

### Velocity Field Reconstruction

**Objective:** Retrieve **velocity fields** directly from raw particle images without following traditional cross-correlation steps.

**Approach:**\
ML models, often deep neural networks, are trained on pairs of input images and their known velocity fields. Once trained, these networks can infer velocity fields from new images in a fraction of the time required by classical methods. This approach sidesteps traditional multi-step correlation analysis, potentially improving robustness and speed.

In conventional PIV, the displacement between two successive images is estimated by computing the cross-correlation function $R(\mathbf{s})$ over interrogation windows:

$$
R(\mathbf{s}) = \int_{\Omega} I_1(\mathbf{x}) \, I_2(\mathbf{x} + \mathbf{s}) \,
d\mathbf{x}
$$

where $I_1$ and $I_2$ are the image intensity fields from two frames separated by a known time interval $\Delta t$, and $\mathbf{s}$ is the displacement vector. The peak of $R$ gives the most probable particle displacement $\mathbf{s}^*$, and the local velocity is then $\mathbf{u} = \mathbf{s}^*/\Delta t$. ML-based approaches learn to approximate this mapping end-to-end, predicting $\mathbf{u}$ directly from the image pair without explicit correlation computation.

**Benefit:**\
Faster reconstruction enables near-instantaneous flow analysis, paving the way for real-time feedback and control in experimental setups.

```
ASCII Diagram: Direct Velocity Prediction

  Input: PIV Image Pair
     | (no manual cross-correlation)
     v
   Trained Neural Network
     |
     v
  Predicted Velocity Field (Color-coded vectors)
```

### Uncertainty Quantification

**Objective:** Provide **uncertainty estimates** for each vector in the velocity field, informing researchers about the reliability of measurements.

**Approach:**\
By training ML models to predict both velocities and their corresponding confidence levels, scientists know which regions are measured accurately and which might be less reliable. This might involve probabilistic layers in neural networks or ensembles of models that gauge variability.

**Benefit:**\
Understanding uncertainty guides more cautious interpretation of results and helps optimize measurement strategies.

### Optimization of PIV Parameters

**Objective:** Choose optimal **experimental parameters**, like interrogation window size or particle density, to improve measurement quality.

**Approach:**\
ML can analyze historical data to learn what parameter settings yield the best velocity fields under given conditions. For instance, if certain window sizes reduce noise in high-speed flows, the model suggests those settings from the outset.

**Benefit:**\
Experimenters save time and resources, achieving better data on the first try and reducing trial-and-error efforts.

```
ASCII Diagram: Parameter Tuning

   Parameters: Window Size, Seeding Density, Laser Intensity
       |
       v
   ML Recommends Settings
       |
       v
   Improved PIV Images -> Better Velocity Fields
```

### Data Fusion with Other Sensors

**Objective:** Combine PIV data with measurements from other instruments (e.g., temperature, pressure probes) to form a **multi-modal view** of the flow.

**Approach:**\
ML algorithms learn correlations between PIV data and signals from other sensors. They integrate diverse data sources, helping uncover complex relationships, like how temperature gradients influence vortex strength or how pressure fluctuations correlate with velocity distributions.

**Benefit:**\
A holistic picture of fluid dynamics emerges, enabling more comprehensive studies of flow behavior.

### Noise Reduction and Error Correction

**Objective:** Improve data quality by removing **noise and spurious vectors**, common issues in PIV analysis.

**Approach:**\
ML models trained on labeled datasets (where some vectors are known to be incorrect) learn to detect and correct these errors. They can distinguish real flow structures from camera artifacts, outliers, or random particle clustering that may skew results.

**Benefit:**\
Cleaner data leads to more accurate velocity fields and more reliable conclusions.

```
ASCII Diagram: Noise and Error Filtering

   Raw Vectors: Some are random or incorrect
      |
      v
   ML-Based Filter
      |
      v
   Cleaned Velocity Field (no spurious vectors)
```

### Real-time Data Analysis

**Objective:** Enable **real-time analysis** and visualization of velocity fields during experiments, helping researchers adjust setups on the fly.

**Approach:**\
Efficient ML algorithms, possibly running on GPUs or parallel architectures, process incoming PIV data streams and deliver immediate velocity maps. This allows experimenters to change parameters mid-experiment, like altering flow speed or adjusting seeding density, to focus on particular phenomena.

**Benefit:**\
Adaptive experimentation saves time and can lead to deeper insights with fewer trial runs.

### Advanced Flow Pattern Recognition

**Objective:** Identify and categorize **complex flow patterns** beyond simple vortices or jets.

**Approach:**\
ML can cluster and classify intricate flow topologies, recognizing patterns like swirling motions, turbulent eddies, or mixing layers. By learning from large datasets, ML can help categorize flow states that may be too subtle or complicated for manual classification.

**Benefit:**\
Deeper understanding of complex and previously hard-to-describe fluid phenomena supports advanced fluid dynamics research and engineering design.

```
ASCII Diagram: Pattern Recognition

   Different Flow Patterns:
     - Kelvin-Helmholtz Instability
     - Turbulent Eddies
     - Recirculation Zones

   ML Classifier:
     Input: Velocity Fields
     Output: Flow Pattern Category
```

### Setting Up the Problem

1. **Build a labeled dataset** by generating synthetic PIV image pairs with known velocity fields (e.g., from DNS or validated CFD simulations) or by pairing experimental images with conventional cross-correlation results as ground truth.
2. **Choose an appropriate ML architecture.** Convolutional neural networks (CNNs) map image pairs directly to velocity fields; probabilistic models (e.g., Bayesian neural networks or ensemble methods) additionally quantify prediction uncertainty.
3. **Define training objectives** that go beyond pixel-wise error—incorporate physical consistency losses such as divergence-free constraints for incompressible flows or smoothness regularization to suppress unphysical gradients.
4. **Integrate with existing PIV pipelines.** The ML model should accept standard image formats and output velocity fields compatible with established post-processing and visualization tools.
5. **Validate against conventional results** by comparing ML-predicted fields with traditional cross-correlation outputs on held-out test cases, checking metrics like mean absolute error, outlier fraction, and spatial resolution.
6. **Iterate on data quality and model accuracy.** Augment training data with varied seeding densities, noise levels, and flow regimes; retrain and fine-tune until the model generalizes across the conditions encountered in practice.

### Key Takeaways

- **ML accelerates PIV processing** by replacing or augmenting iterative cross-correlation with trained models that predict velocity fields in a single forward pass.
- **Noise reduction and error correction** benefit from data-driven filtering, producing cleaner velocity fields than traditional median or threshold-based outlier removal.
- **Uncertainty quantification** adds a confidence layer to every measurement, guiding researchers toward regions that need closer inspection.
- **Real-time analysis** becomes feasible when lightweight models run on GPUs, enabling adaptive experiments with on-the-fly parameter adjustments.
- **Multi-modal data fusion** enriches flow understanding by combining PIV with temperature, pressure, or concentration measurements through learned correlations.
- **Physical consistency** must be enforced during training to ensure that ML predictions respect conservation laws and produce physically meaningful results.

### Exercises

**Exercise 1.** The correlation peak in an interrogation window is at $\mathbf{s}^* = (6.4, -1.2)$ pixels. The magnification is 25 µm per pixel and the frames are 500 µs apart. Compute the velocity components.

<details>
<summary>Answer</summary>

Convert pixels to metres, then divide by $\Delta t = 5 \times 10^{-4}$ s:

```math
u = \frac{6.4 \times 25 \times 10^{-6}}{5 \times 10^{-4}} = 0.32 \text{ m/s},
\qquad v = \frac{-1.2 \times 25 \times 10^{-6}}{5 \times 10^{-4}} = -0.06 \text{ m/s}
```

</details>

**Exercise 2.** A common PIV guideline (the "one-quarter rule") keeps the particle displacement below one quarter of the interrogation window. For 32-pixel windows, 25 µm per pixel and a maximum flow speed of 2 m/s, what is the largest allowed $\Delta t$? With that $\Delta t$, a slow region moves at 0.2 m/s. If the correlation peak can be located to about 0.1 px, what is the relative velocity error there?

<details>
<summary>Answer</summary>

The maximum displacement is $32/4 = 8$ px, or $2 \times 10^{-4}$ m, so $\Delta t_{\max} = 2 \times 10^{-4} / 2 = 1.0 \times 10^{-4}$ s (100 µs).

In the slow region the displacement is only 0.8 px, so a 0.1 px uncertainty is a 12.5% velocity error.

This dynamic-range trade-off is one of the parameter choices the note suggests ML could help optimize, for example by using adaptive windows or different time separations in different regions.

</details>

**Exercise 3.** A 1D version of the correlation integral uses intensity profiles $I_1 = (0, 1, 3, 1, 0, 0, 0, 0, 0)$ and $I_2 = (0, 0, 0, 1, 2.5, 2, 0.5, 0, 0)$. Compute $R(s) = \sum_i I_1(i)\, I_2(i + s)$ for $s = 0, \dots, 4$, find the integer peak, and refine it with the three-point Gaussian estimator $\varepsilon = \frac{\ln R_{-} - \ln R_{+}}{2(\ln R_{-} - 2\ln R_0 + \ln R_{+})}$.

<details>
<summary>Answer</summary>

$R(0) = 1.0$, $R(1) = 5.5$, $R(2) = 10.5$, $R(3) = 9.0$, $R(4) = 3.5$. The integer peak is at $s = 2$.

With $R_- = 5.5$, $R_0 = 10.5$ and $R_+ = 9.0$:

```math
\varepsilon = \frac{\ln 5.5 - \ln 9.0}{2(\ln 5.5 - 2\ln 10.5 + \ln 9.0)} \approx 0.31
```

so $s^* \approx 2.31$ px.

The sub-pixel shift towards $s = 3$ reflects the skewed particle image in $I_2$. An ML model trained end-to-end has to learn this kind of sub-pixel accuracy from data.

</details>

**Exercise 4.** A CNN predicts a planar PIV field on a 1 mm grid. Around one node the neighbouring values are $u_{i+1,j} = 0.52$, $u_{i-1,j} = 0.48$, $v_{i,j+1} = 0.11$ and $v_{i,j-1} = 0.13$ m/s. Compute the in-plane divergence with central differences. Should a divergence-free penalty force it to zero?

<details>
<summary>Answer</summary>

$\partial u/\partial x \approx (0.52 - 0.48)/0.002 = 20$ s$^{-1}$ and $\partial v/\partial y \approx (0.11 - 0.13)/0.002 = -10$ s$^{-1}$, so the in-plane divergence is $10$ s$^{-1}$, about a third of the gradient magnitudes.

For planar (2D2C) PIV of a three-dimensional flow, incompressibility only requires $\partial u/\partial x + \partial v/\partial y = -\partial w/\partial z$, and the out-of-plane gradient is not measured. A hard 2D divergence-free constraint is only appropriate for genuinely two-dimensional flows. Otherwise it should be a weak penalty, or the constraint should be applied to stereo or volumetric data where all three components are available.

</details>

**Exercise 5.** An ensemble of five networks predicts $u = 0.31, 0.33, 0.30, 0.34, 0.32$ m/s at one vector location. Report the ensemble estimate and its spread, and state which sources of uncertainty the spread does not capture.

<details>
<summary>Answer</summary>

The mean is $0.32$ m/s. The sample standard deviation is $\sqrt{\sum (u_i - 0.32)^2 / 4} = \sqrt{0.001/4} \approx 0.016$ m/s, about 4.9% of the mean.

The spread measures model (epistemic) disagreement only. It misses bias shared by all members (for example, from synthetic training images that differ from the real optics), random measurement noise in the images, and errors from out-of-distribution seeding densities that all members handle equally badly. It should be calibrated against cases with known ground truth.

</details>

### References

- Raffel, M., Willert, C. E., Wereley, S. T., & Kompenhans, J., *Particle Image Velocimetry: A Practical Guide*, 2nd ed., Springer, 2007.
- Adrian, R. J., & Westerweel, J., *Particle Image Velocimetry*, Cambridge University Press, 2011.
- Willert, C. E., & Gharib, M., "Digital particle image velocimetry", *Experiments in Fluids* 10(4), 1991.
- Keane, R. D., & Adrian, R. J., "Theory of cross-correlation analysis of PIV images", *Applied Scientific Research* 49(3), 1992.
- Brunton, S. L., Noack, B. R., & Koumoutsakos, P., "Machine Learning for Fluid Mechanics", *Annual Review of Fluid Mechanics* 52, 2020.
