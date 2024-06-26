# Modeling Flow Dynamics

Modeling aims to strike a perfect balance between efficiency and accuracy, which is a central goal. However, when it comes to modeling physical systems, it becomes crucial to also take into account interpretability and generalizability. These factors play a significant role in ensuring the effectiveness and applicability of the models.

## Linear models through nonlinear embeddings: dynamic mode decomposition and Koopman analysis

- Numerous classical techniques utilized in system identification can be categorized as machine learning (ML) methods due to their ability to generate models that extend beyond the training data.

- Dynamic mode decomposition (DMD), introduced by Schmid in 2010 and further developed by Kutz et al. in 2016, represents a contemporary approach for extracting spatiotemporal coherent structures from time series data of fluid flows. This technique yields a low-dimensional linear model that describes the evolution of these dominant coherent structures. DMD relies on data-driven regression and is applicable to both time-resolved experimental and numerical data. It shares a close connection with the Koopman operator, as established by Rowley et al. in 2009 and Mezic in 2013.

- The Koopman operator is an infinite-dimensional linear operator that characterizes the temporal evolution of all measurement functions within the system. However, it is important to note that the DMD algorithm, which is based on linear flow field measurements such as direct measurements of fluid velocity or vorticity, may not effectively capture nonlinear transients. In recent times, there has been a collective endeavor to discover a coordinate system that can effectively portray nonlinear dynamics in a linear manner.

- The utilization of the extended Dynamic Mode Decomposition (DMD) and the variational approach of conformation dynamics enhances the model by incorporating nonlinear measurements, employing kernel methods and dictionary learning techniques. These particular nonlinear measurements pose a significant challenge in terms of representation, and as a result, deep learning architectures are now being employed to identify nonlinear Koopman coordinate systems.

- This identification process involves the use of a time-lagged autoencoder and a customized variational score to determine Koopman coordinates, as demonstrated impressively in the context of protein folding. Considering the impressive performance of VAMPnet, it is plausible that neighboring fields, such as molecular dynamics, which encounter similar modeling complexities including stochasticity, coarse-grained dynamics, and separation of timescales, could also benefit from its application in fluid dynamics.

Let me break down the various methods and terminology for you, step by step, once more, so you can understand how to understand and learn to use them correctly:
DMD and Koopman Analysis are powerful methods employed to extract linear models from complex dynamical systems. These techniques enable us to identify coherent structures within the system and accurately capture their evolution over time.

1. **Dynamic Mode Decomposition (DMD):**
   - DMD is a data-driven technique used to analyze the dynamic behavior of complex systems. It can be applied to both experimental and computational data.
   
   - **Technique:**
     - **Snapshot Collection:** Snapshots of the system's state are collected over time.
     - **Data Matrix Construction:** These snapshots are arranged into a data matrix.
     - **Singular Value Decomposition (SVD):** The SVD of the data matrix is computed, and the DMD modes are extracted.
     - **Dynamics Extraction:** The DMD modes represent the dynamic structures or coherent patterns in the system. The associated eigenvalues provide information about the temporal evolution.

   - **Linear Model:** Despite being a technique applied to nonlinear systems, the resulting DMD modes often form a linear approximation that captures the dominant linear dynamics.
   - **Applications:** DMD has been successfully applied in fluid mechanics, neuroscience, and other fields to identify coherent structures and characterize their evolution over time.

2. **Koopman Analysis:**
   - Koopman Analysis is a mathematical framework that provides a linear representation of the dynamics of a nonlinear system by expressing it in an infinite-dimensional linear space.

   - **Technique:**
     - **Koopman Operator Construction:** The Koopman operator is an infinite-dimensional linear operator that acts on observable functions of the system's state.
     - **Eigenfunctions and Eigenvalues:** Koopman Analysis seeks eigenfunctions and eigenvalues of the Koopman operator, which, when analyzed, reveal the underlying linear dynamics.
     - **Mode Reconstruction:** The modes associated with the dominant eigenvalues provide a linear representation of the system's dynamics.

   - **Linear Model:** Koopman Analysis aims to find a linear model that represents the evolution of observables, making it a powerful tool for understanding and predicting the behavior of nonlinear systems.
   - **Applications:** Koopman Analysis has been applied in fields such as fluid dynamics, biology, and climate science to uncover hidden linear structures in complex systems.

---

DMD and Koopman Analysis are two data-driven techniques that have the ability to extract linear representations from systems that are inherently nonlinear. These methods prove to be especially valuable when dealing with complex and high-dimensional dynamical systems, where traditional linearization approaches may not yield effective results. The linear models derived from DMD and Koopman Analysis offer valuable insights into the primary coherent structures and their temporal evolution within the nonlinear dynamics that underlie the system. In the field of fluid mechanics, these techniques find applications in various areas such as identifying coherent structures in turbulent flows, analyzing vortex dynamics, and comprehending the spatiotemporal behavior of intricate fluid systems.

## Neural network modeling

- Over the past thirty years, neural networks (NNs) have been extensively utilized in the modeling of dynamical systems and fluid mechanics problems.

- Initially, NNs were employed to acquire knowledge about the solutions of ordinary and partial differential equations. However, it is important to highlight that the full potential of these applications has not yet been fully explored.

- In recent years, there have been significant advancements in this field, including the development of discrete and continuous-in-time networks.

- These advancements have opened up new possibilities, such as using NNs to uncover latent variables and minimize the need for extensive parametric studies that are typically associated with partial differential equations. Additionally, NNs are frequently employed in nonlinear system identification techniques like NARMAX, which are commonly used to model fluid systems. In the realm of fluid mechanics, NNs have found wide-ranging applications in modeling heat transfer, turbomachinery, turbulent flows, and other aeronautical problems.

- RNNs utilizing LSTMs have brought about a significant transformation in the realm of speech recognition, establishing themselves as a noteworthy achievement in the field of artificial intelligence. Presently, they are being employed to effectively represent dynamic systems and make data-based forecasts regarding exceptional occurrences.

- An intriguing revelation from these investigations is that the amalgamation of data-driven approaches with reduced-order models proves to be a formidable technique, surpassing the individual capabilities of each method across various studies.

- Furthermore, GANs are also being harnessed to comprehend the intricacies of physics. Although the application of GANs in the modeling and simulation of turbulence is still in its early stages, it holds immense potential for future advancements.

- Despite the widespread use and potential of neural networks (NNs) in dynamical systems, there are still several challenges that need to be addressed.

- One fundamental limitation of NNs is their interpolative nature, meaning that they can only approximate the function well within the range of the sampled data used for training. Therefore, caution should be exercised when using NN models for extrapolation tasks.

- In certain domains like computer vision and speech recognition, the training data are often extensive, allowing future tasks to be seen as interpolations on the training data.

- However, achieving such a scale of training data in fluid mechanics has not been accomplished thus far. It is crucial to note that NN models are susceptible to overfitting, where they become too specialized to the training data and perform poorly on new data.

- To mitigate this, it is essential to cross-validate models using a carefully chosen test set, following best practices outlined by Goodfellow et al. (2016).

- Furthermore, it is important to explicitly incorporate known physics into NN models, such as symmetries, constraints, and conserved quantities. By incorporating these principles, the models can better capture the underlying physical behavior and improve their predictive capabilities.

**Let's dive into the various strategies and terminology, step by step, once more, to ensure you understand how to effectively apply them:**

## 1. Evolution of Neural Networks in Modeling:
- NNs have been widely utilized in the modeling of dynamical systems and fluid mechanics problems for the past three decades.
- Originally employed to gain insights into the solutions of ordinary and partial differential equations, they have proven to be an invaluable tool in these domains.

## 2. Advancements in Neural Network Modeling:
- Recent progress has been made in the field, with the emergence of discrete and continuous-in-time networks, which have paved the way for novel opportunities.
- Neural networks (NNs) are employed to reveal hidden variables, thereby reducing the necessity for comprehensive parametric investigations linked to partial differential equations.

## 3. Applications in Fluid Mechanics:
- Neural networks (NNs) have found diverse applications in the field of fluid mechanics, including the modeling of heat transfer, turbomachinery, turbulent flows, and various aeronautical problems. These applications demonstrate the versatility and effectiveness of NNs in tackling complex problems within fluid mechanics.

## 4. Recurrent Neural Networks (RNNs) with LSTMs:
- LSTM networks, a type of RNNs, have revolutionized the field of speech recognition and are currently being utilized to model dynamic systems and generate data-driven predictions.
- The combination of data-driven approaches with reduced-order models has been recognized as a potent technique.

## 5. Generative Adversarial Networks (GANs):
- GANs are employed to grasp the complexities of physics, despite the fact that their utilization in the modeling and simulation of turbulence is still in its nascent phases.
- Regarded for its tremendous potential in propelling future developments.

## 6. Challenges and Limitations:
- NNs have a limitation in their interpolative nature, which restricts their effectiveness to the range of sampled data utilized during training.
- Exercising caution is recommended when undertaking extrapolation tasks, and it is crucial to cross-validate models in order to prevent overfitting.
- One of the difficulties faced in the field of fluid mechanics is the limited availability of comprehensive training data. This scarcity of data poses a challenge when developing neural network models. Additionally, another obstacle is the requirement to integrate established principles of physics into these models.

## 7. Incorporating Physics into Neural Network Models:
- Incorporating well-established principles of physics, such as symmetries, constraints, and conserved quantities, explicitly into a system can greatly enhance its predictive capabilities.
- The models are designed to guarantee the accurate representation of the fundamental physical behavior and improve their ability to adapt to novel data.
