import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.qmc import Sobol

# Set up Sobol sequence generator
dimension = 2
num_samples = 500
sobol = Sobol(d=dimension, scramble=True)

# Generate Sobol sequence samples
samples = sobol.random(n=num_samples)

# Mock meshes generation
# In actual implementation, samples would be used to generate 3D mesh geometries
mock_meshes = samples  # Just for demonstration

# Plotting the results
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Plot for Approach_Angle
axes[0].scatter(mock_meshes[:, 0], mock_meshes[:, 1], color="blue")
axes[0].set_title("2D design space distribution")
axes[0].set_xlabel("Approach_Angle")
axes[0].set_ylabel("Variable_1")

# Plot for Decklid_Height
axes[1].scatter(mock_meshes[:, 0], mock_meshes[:, 1], color="blue")
axes[1].set_title("2D design space distribution")
axes[1].set_xlabel("Decklid_Height")
axes[1].set_ylabel("Variable_2")

plt.suptitle("500 geometry variants generated (1st 20 shown here)")
plt.show()
