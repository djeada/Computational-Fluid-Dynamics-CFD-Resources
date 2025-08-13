# Computational Fluid Dynamics (CFD) Resources

A comprehensive, open-source repository of educational materials, theoretical foundations, and practical resources for## 🤝 Contributing

We welcome contributions from the CFD community! Whether you're fixing documentation, adding new content, improving algorithms, or sharing insights, your contributions help make this a better resource for everyone.

### How to Contribute

1. **🍴 Fork** this repository
2. **🌿 Create** a feature branch (`git checkout -b feature/YourContribution`)
3. **✏️ Make** your changes with clear, descriptive commits
4. **🧪 Test** your additions and ensure documentation is updated
5. **📤 Push** to your fork (`git push origin feature/YourContribution`)
6. **🔄 Open** a Pull Request with detailed description

### Contribution Guidelines

- **📖 Documentation**: Use clear, technical language with proper mathematical notation
- **🔢 Code**: Include comments, validation examples, and performance considerations  
- **🎨 Formatting**: Follow existing structure and markdown conventions
- **🔗 References**: Cite sources and provide links to supporting material
- **✅ Quality**: Ensure accuracy through peer review and testing

### Types of Contributions Welcome

- **🐛 Bug fixes** and error corrections
- **📚 Educational content** improvements and expansions  
- **💻 New algorithms** and computational methods
- **🎯 Practical examples** and case studies
- **🔧 Tool integrations** and workflow improvements
- **🌐 Translations** and accessibility enhancements

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details. This ensures the content remains open and accessible for educational and research purposes.

## 🌟 Acknowledgments

Special thanks to the CFD community, academic institutions, and open-source contributors who make this field accessible to everyone. This repository builds upon decades of research and development in computational fluid dynamics.

## 📚 References and Further Readingd dynamics engineers, researchers, and students. This repository provides systematically organized content covering fundamental theory through advanced applications.

![cfd_resources](https://github.com/user-attachments/assets/ac0cec05-abb0-4f8e-ae68-3df6bbb53308)

## 🎯 Repository Overview

This repository serves as a complete educational ecosystem for CFD, featuring:

- **📚 Comprehensive theoretical foundations** with rigorous mathematical derivations
- **🔧 Practical implementation guides** and computational methods
- **📊 Visualization tutorials** for ParaView, Gmsh, and other CFD tools
- **💻 Custom scripts and algorithms** for streamlined workflows
- **🧮 Numerical methods** from fundamentals to advanced techniques
- **🌊 Fluid mechanics theory** from basic principles to specialized applications

## 📖 Content Organization

### 📝 [Notes](./notes/)
Comprehensive theoretical foundations organized by discipline:

#### 🌊 [Fluid Mechanics](./notes/fluid_mechanics/)
**Complete theoretical framework covering 15+ major areas:**

- **[Fundamentals](./notes/fluid_mechanics/intro.md)**: Continuum hypothesis, conservation laws, mathematical foundations
- **[Governing Equations](./notes/fluid_mechanics/governing_equations/)**: Navier-Stokes, continuity, energy, and constitutive relations
- **[Dimensional Analysis](./notes/fluid_mechanics/dimensions.md)**: Buckingham Pi theorem and dimensionless numbers
- **[Fluid Properties](./notes/fluid_mechanics/fluid_properties/)**: Viscosity, surface tension, and material behavior
- **[Fluid Statics](./notes/fluid_mechanics/fluid_statics/)**: Hydrostatics, buoyancy, and pressure systems
- **[Flow Kinematics](./notes/fluid_mechanics/flow_kinematics/)**: Eulerian/Lagrangian descriptions and flow visualization
- **[Inviscid Flow](./notes/fluid_mechanics/inviscid_flow/)**: Potential theory, Bernoulli's equation, and complex analysis
- **[Viscous Flow](./notes/fluid_mechanics/viscous_flow/)**: Boundary layers, drag analysis, and real fluid effects
- **[Compressible Flow](./notes/fluid_mechanics/compressible_flow/)**: High-speed phenomena, shock waves, and gas dynamics
- **[Turbulence Theory](./notes/fluid_mechanics/turbulence/)**: Reynolds decomposition, energy cascade, and modeling approaches
- **[Internal Flow](./notes/fluid_mechanics/internal_flow/)**: Pipe flow, duct systems, and network analysis
- **[Specialized Topics](./notes/fluid_mechanics/specialized_topics/)**: Fluid-structure interaction, multiphase flows, and advanced applications

#### ⚙️ [Applied Mechanics](./notes/applied_mechanics/)
**Practical engineering applications and design methodologies:**

- **Control Systems**: Feedback control and system design
- **Dynamics**: Motion analysis and vibration theory
- **Fluid Loading**: Pressure distribution and force analysis
- **Mechanical Systems**: Component design and optimization
- **Statics**: Equilibrium analysis and structural mechanics
- **Strength of Materials**: Stress analysis and material behavior
- **Transportation**: Vehicle dynamics and aerodynamics

#### 🤖 [Machine Learning](./notes/machine_learning/)
**Modern data-driven approaches to fluid mechanics:**

- **Neural Networks**: Physics-informed neural networks (PINNs)
- **Flow Analysis**: Pattern recognition in turbulent flows
- **Geometry Optimization**: AI-driven design methods
- **Automotive Aerodynamics**: ML applications in vehicle design

#### 🔢 [Numerical Methods](./notes/numerical/)
**Computational techniques and algorithm implementation:**

- **[CFD Methods](./notes/numerical/cfd/)**: Finite volume, finite element, and finite difference
- **[Finite Difference](./notes/numerical/fdm/)**: Grid-based numerical schemes
- **[Finite Element](./notes/numerical/fem/)**: Variational methods and mesh-based solutions
- **[Finite Volume](./notes/numerical/fvm/)**: Conservation-based discretization
- **[Lattice Boltzmann](./notes/numerical/lattice_boltzmann/)**: Kinetic theory approaches
- **[Proper Orthogonal Decomposition](./notes/numerical/pod/)**: Model reduction techniques
- **[Reduced Order Models](./notes/numerical/rom/)**: Efficient approximation methods
- **[Surrogate Models](./notes/numerical/surrogates/)**: Data-driven modeling approaches

### 🛠️ [Practice](./practice/)
**Hands-on tutorials and implementation guides:**

#### 📐 [Gmsh](./practice/gmsh/)
- **[Introduction](./practice/gmsh/intro.md)**: Getting started with mesh generation
- **[Volume Mesh Generation](./practice/gmsh/generate_volume_mesh.md)**: 3D meshing techniques

#### 📊 [ParaView](./practice/paraview/)
- **[Introduction](./practice/paraview/intro.md)**: Visualization fundamentals
- **[External Packages](./practice/paraview/import_external_packages.md)**: Custom plugin integration

#### 🔧 [Manual Projects](./practice/manual_projects/)
Detailed project implementations and case studies

### 📜 [Scripts](./scripts/)
**Ready-to-use computational tools and algorithms:**

#### 🔍 [Algorithms](./scripts/algorithms/)
**Mathematical implementations:**
- Correlation functions and kriging interpolation
- SVD-based image compression
- Proper orthogonal decomposition (POD)
- Radial basis functions
- Condition number analysis

#### 📈 [Visualization](./scripts/plots/)
**Comprehensive plotting and analysis scripts:**
- Airfoil analysis and design space visualization
- Boundary layer profiles and flow separation
- Turbulence analysis and POD modes
- Compressible flow phenomena
- Heat transfer and pressure distributions

#### 🖥️ [Simulations](./scripts/simulations/)
Complete simulation setups and case studies

## 🚀 Getting Started

### Prerequisites
- **Mathematics**: Vector calculus, differential equations, linear algebra
- **Programming**: Python, MATLAB, or similar computational environment
- **Software**: ParaView, Gmsh (installation guides provided)

### Quick Start Guide

1. **📖 Begin with Theory**: Start with [Fluid Mechanics Fundamentals](./notes/fluid_mechanics/intro.md)
2. **🔢 Learn Numerical Methods**: Explore [CFD Methods](./notes/numerical/cfd/)
3. **🛠️ Practice Implementation**: Follow [Gmsh Tutorials](./practice/gmsh/)
4. **📊 Visualize Results**: Use [ParaView Guides](./practice/paraview/)
5. **🔧 Apply Scripts**: Implement ready-made [algorithms](./scripts/algorithms/)

### Learning Pathways

#### 🎓 **Beginner Path**
1. Fluid mechanics fundamentals and dimensional analysis
2. Basic numerical methods (finite difference)
3. Simple visualization with ParaView
4. Elementary scripting examples

#### 🎯 **Intermediate Path**
1. Navier-Stokes equations and boundary conditions
2. Finite volume and finite element methods
3. Turbulence modeling basics
4. Advanced visualization techniques

#### 🏆 **Advanced Path**
1. Specialized flow phenomena and multiphase systems
2. Machine learning integration
3. Custom algorithm development
4. Research-level applications

## ✨ Key Features

### 📚 **Comprehensive Coverage**
- **500+ pages** of detailed theoretical content
- **Mathematical rigor** with complete derivations
- **Physical interpretations** alongside mathematical formulations
- **Engineering applications** for each theoretical concept

### 🎯 **Educational Excellence**
- **Progressive complexity** from basics to advanced topics
- **Clear prerequisites** and learning objectives
- **Cross-references** between theory and applications
- **Problem-solving strategies** and design methodologies

### 💻 **Practical Implementation**
- **Ready-to-use scripts** for common CFD tasks
- **Detailed tutorials** for professional software
- **Custom algorithms** with explanation and validation
- **Industry-standard practices** and workflows

### 🔄 **Continuous Updates**
- **Modern approaches** including machine learning integration
- **Current computational methods** and best practices
- **Active maintenance** and community contributions
- **Peer-reviewed content** ensuring accuracy and relevance

## How to Contribute

Got something useful to share? Found a mistake or a better way to do something? Contributions of all kinds are welcome—whether it’s fixing a typo, adding a script, or sharing your own CFD tips.

Here’s how to get started:

1. Fork this repo.
2. Create a new branch (`git checkout -b feature/YourAwesomeThing`).
3. Make your changes and commit them (`git commit -m 'Add YourAwesomeThing'`).
4. Push to your fork (`git push origin feature/YourAwesomeThing`).
5. Open a Pull Request—we'll take it from there.

Thanks for helping make this a better resource for the CFD community!

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## References

### 🌐 General Resources
- [DepositOnce - TU Berlin](https://depositonce.tu-berlin.de/) - Academic repository with CFD research
- [CFD Python: 12 Steps to Navier-Stokes by Lorena Barba](https://lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/) - Interactive CFD learning
- [National Committee for Fluid Mechanics Series](https://youtube.com/playlist?list=PL0EC6527BE871ABA3) - Educational video series
- [CFD General Principles by CFD Direct](https://doc.cfd.direct/notes/cfd-general-principles/) - Fundamental concepts
- [NASA Turbulence Modeling Resource](https://turbmodels.larc.nasa.gov/) - Validation cases and methods
- [Wall-Modeled Large Eddy Simulation Resource](https://wmles.umd.edu/) - Advanced turbulence modeling
- [Airfoil Tools Database](http://www.airfoiltools.com/) - Comprehensive airfoil analysis
- https://www.nwtf.ac.uk/dataset/2687/  The Airbus Wind Tunnel Dataset on the RAE2822 transonic aerofoil is now publicly available on the NWTF Experimental Database.


### 📖 Essential Textbooks

#### **Fundamental CFD Theory**
- **Anderson, John D.** - *Computational Fluid Dynamics: The Basics with Applications* ([Amazon](https://amzn.to/42iuJNV))
- **Versteeg, H. K.; Malalasekera, W.** - *An Introduction to Computational Fluid Dynamics: The Finite Volume Method* ([Amazon](https://amzn.to/3EbEMfG))
- **Ferziger, Joel H.; Peric, Milovan; Street, Robert L.** - *Computational Methods for Fluid Dynamics* ([Amazon](https://amzn.to/3FSZ9iq))

#### **Numerical Methods**
- **Patankar, Suhas V.** - *Numerical Heat Transfer and Fluid Flow* ([Amazon](https://amzn.to/42qd0o1))
- **Blazek, J.** - *Computational Fluid Dynamics: Principles and Applications* ([Amazon](https://amzn.to/4j7adqY))

#### **Modern Approaches**
- **Kutz, J. Nathan** - *Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control* ([Amazon](https://amzn.to/3RHJncw))
- **Brunton, Steven L.; Noack, Bernd R.** - *Machine Learning Control – Taming Nonlinear Dynamics and Turbulence* ([Amazon](https://amzn.to/4jeggJC))

### 📄 Key Research Papers

#### **Machine Learning in CFD**
- [Machine Learning for Fluid Dynamics: An Overview](https://arxiv.org/abs/1905.11075) - Comprehensive review of ML applications
- [ML-Based CFD Simulations: Review and Future Tactics](https://link.springer.com/article/10.1007/s00521-022-07838-6) - State-of-the-art analysis
- [Physics-Informed Neural Networks for PDEs](https://www.brown.edu/research/projects/crunch/sites/brown.edu.research.projects.crunch/files/uploads/Physics-informed%20neural%20networks_A%20deep%20learning%20framwork%20fir%20solving%20forward%20and%20inverse%20probelms%20involving%20nonlinear%20partial%20differential%20equations.pdf) - PINN methodology

#### **Future of CFD**
- [CFD of the Future: Year 2025 and Beyond](https://www.researchgate.net/publication/339808378_CFD_of_the_Future_Year_2025_and_Beyond) - Vision for CFD development
- [Machine Learning in CFD](https://www.tandfonline.com/doi/full/10.1080/10618562.2023.2175788) - Recent advances and applications

#### **Historical References**
- [Pratt & Whitney Aircraft Engine Operation (1949)](https://www.scribd.com/document/307072703/Pratt-Whitney-The-Aircraft-Engine-and-Its-Operation-Rev1949-BZ) - Classic engineering reference

### 💻 Code Repositories and Open Source Projects

#### **Educational Implementations**
- [NVIDIA Modulus Airfoil Optimization](https://github.com/neo-fetch/nvidia-modulus-airfoil-optimisation) - Modern GPU-accelerated CFD
- [Machine Learning and Simulation by Ceyron](https://github.com/Ceyron/machine-learning-and-simulation) - Educational ML+CFD examples
- [Scientific Computing by Chasnov](https://math.libretexts.org/Bookshelves/Scientific_Computing_Simulations_and_Modeling/Scientific_Computing_(Chasnov)/III%3A_Computational_Fluid_Dynamics/14%3A_The_Governing_Equations) - Theoretical foundations

#### **Finite Element Resources**
- [Introductory Finite Elements](https://github.com/AppliedMechanics-EAFIT/Introductory-Finite-Elements) - FEM fundamentals
- [Dolfin X FEM Tutorial](https://jsdokken.com/dolfinx-tutorial/fem.html) - Modern FEM implementation
- [David Penner's CFD Projects](https://davidpenner74.wixsite.com/davidpenner/projects) - Practical applications

### 🎥 Video Learning Resources

#### **University Courses**
- [MIT Lecture Series on CFD](https://www.youtube.com/@AeroCFD) - Academic-level instruction
- [CFD Course - ME615 IIT Mandi](https://youtube.com/playlist?list=PLOUcBDsCNnMweTuft1qq25CQbyyKqZKvI) - Comprehensive curriculum
- [Numerical Methods by Hand](https://youtube.com/playlist?list=PL5_Bm_WH1i3fAQP6G2_SaazjNIy3m8QbH) - Fundamental understanding

#### **Specialized Topics**
- [Data-driven Methods Seminar](https://youtube.com/playlist?list=PLWL3MaEZQ5I0x5SoN-whc6wfxvZr4E5v9) - Modern approaches
- [CFD Lectures by Qiqi Wang](https://www.youtube.com/c/QiqiWangGG) - Advanced numerical analysis
- [The Perić Lectures on CFD](https://youtu.be/8a0j2DQiTVQ) - Industry perspective

#### **Practical Problem Solving**
- [Fluid Concepts Introduction](https://www.youtube.com/watch?v=zGuVWSKBc4Y&list=PLyYlZ2ZyWpnh6Xy8xsqIFQKPiMzVkUkdG) - Conceptual understanding
- [Mechanics Problems by Hand](https://youtube.com/playlist?list=PL7FF084F8C414D602) - Analytical solutions
- [Postcard Professor Solutions](https://www.youtube.com/c/PostcardProfessor/playlists) - Step-by-step methods

---

**📧 Contact**: For questions, suggestions, or collaboration opportunities, please open an issue or submit a pull request.

**🌟 Star this repository** if you find it useful for your CFD learning or research!### Books
- **Anderson, John D.**  
  *Computational Fluid Dynamics: The Basics with Applications*  
  [Amazon Link](https://amzn.to/42iuJNV)

- **Versteeg, H. K.; Malalasekera, W.**  
  *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*  
  [Amazon Link](https://amzn.to/3EbEMfG)

- **Ferziger, Joel H.; Peric, Milovan; Street, Robert L.**  
  *Computational Methods for Fluid Dynamics*  
  [Amazon Link](https://amzn.to/3FSZ9iq)

- **Patankar, Suhas V.**  
  *Numerical Heat Transfer and Fluid Flow*  
  [Amazon Link](https://amzn.to/42qd0o1)

- **Blazek, J.**  
  *Computational Fluid Dynamics: Principles and Applications*  
  [Amazon Link](https://amzn.to/4j7adqY)

- **Kutz, J. Nathan**  
  *Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control*  
  [Amazon Link](https://amzn.to/3RHJncw)

- **Brunton, Steven L.; Noack, Bernd R.**  
  *Machine Learning Control – Taming Nonlinear Dynamics and Turbulence*  
  [Amazon Link](https://amzn.to/4jeggJC)

- **Machine Learning for Fluid Dynamics**  
  *An overview of applying machine learning techniques to fluid dynamics*  
  [View Paper](https://arxiv.org/abs/1905.11075)

- **Machine Learning-Based CFD Simulations: A Review, Models, Open Threats, and Future Tactics**  
  *A comprehensive review of machine learning approaches in CFD simulations*  
  [View Article](https://link.springer.com/article/10.1007/s00521-022-07838-6)

- **Pratt & Whitney**  
  *The Aircraft Engine and Its Operation - Rev1949*  
  [View Document](https://www.scribd.com/document/307072703/Pratt-Whitney-The-Aircraft-Engine-and-Its-Operation-Rev1949-BZ)

### Academic Papers
- [Physics-Informed Neural Networks: A Deep Learning Framework for Solving Forward and Inverse Problems Involving Nonlinear Partial Differential Equations](https://www.brown.edu/research/projects/crunch/sites/brown.edu.research.projects.crunch/files/uploads/Physics-informed%20neural%20networks_A%20deep%20learning%20framwork%20fir%20solving%20forward%20and%20inverse%20probelms%20involving%20nonlinear%20partial%20differential%20equations.pdf)
- [Nature Reviews - GK](https://www.brown.edu/research/projects/crunch/sites/brown.edu.research.projects.crunch/files/uploads/Nature-REviews_GK.pdf)
- [CFD of the Future: Year 2025 and Beyond](https://www.researchgate.net/publication/339808378_CFD_of_the_Future_Year_2025_and_Beyond)  
- [Machine Learning in CFD](https://www.tandfonline.com/doi/full/10.1080/10618562.2023.2175788)  

### Code Repositories and Projects
- [NVIDIA Modulus Airfoil Optimization - Dr. Yang's LDC 2D](https://github.com/neo-fetch/nvidia-modulus-airfoil-optimisation/blob/master/Dr-Yang_ldc_2d.py)
- [Scientific Computing by Chasnov: Computational Fluid Dynamics](https://math.libretexts.org/Bookshelves/Scientific_Computing_Simulations_and_Modeling/Scientific_Computing_(Chasnov)/III%3A_Computational_Fluid_Dynamics/14%3A_The_Governing_Equations)
- [Machine Learning and Simulation by Ceyron](https://github.com/Ceyron/machine-learning-and-simulation)
- [Introductory Finite Elements - FEM Notes and Code](https://github.com/AppliedMechanics-EAFIT/Introductory-Finite-Elements)
- [Dolfin X FEM Tutorial](https://jsdokken.com/dolfinx-tutorial/fem.html)
- [David Penner's Interesting Projects](https://davidpenner74.wixsite.com/davidpenner/projects)

### Video Tutorials
- [MIT Lecture on CFD](https://www.youtube.com/@AeroCFD)
- [Numerical Methods by Hand on YouTube](https://youtube.com/playlist?list=PL5_Bm_WH1i3fAQP6G2_SaazjNIy3m8QbH&si=QrtwsLAQpWKeQKA8)
- [Computational Fluid Dynamics (CFD) - ME615 IIT Mandi](https://youtube.com/playlist?list=PLOUcBDsCNnMweTuft1qq25CQbyyKqZKvI&si=prjJr4J0GVZFWgLa)
- [Data-driven Methods for Science and Engineering Seminar](https://youtube.com/playlist?list=PLWL3MaEZQ5I0x5SoN-whc6wfxvZr4E5v9&si=sj8mXSdq_FynCsUz)
- [Many CFD and Numerical Analysis Lectures by Qiqi Wang](https://www.youtube.com/c/QiqiWangGG)
- [Gentle Introduction to Various Fluid Concepts](https://www.youtube.com/watch?v=zGuVWSKBc4Y&list=PLyYlZ2ZyWpnh6Xy8xsqIFQKPiMzVkUkdG)
- [Various Mechanics Problems Solved by Hand](https://youtube.com/playlist?list=PL7FF084F8C414D602&si=WVUmaxodRYiBP6ue)
- [More Problems Solved by Hand by Postcard Professor](https://www.youtube.com/c/PostcardProfessor/playlists)
- [Other Problems Solved by Hand](https://www.youtube.com/watch?v=PPt_FfoUqBQ&list=PLD45F0FD958B864AD)
- [Various Topics from Theoretical Mechanics and Numerical Methods](https://www.youtube.com/channel/UCcqQi9LT0ETkRoUu8eYaEkg)
- [The Perić Lectures on CFD](https://youtu.be/8a0j2DQiTVQ?si=UX6ThBBVHhmAX6qD)
