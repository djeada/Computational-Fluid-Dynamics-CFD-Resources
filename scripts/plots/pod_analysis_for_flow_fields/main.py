import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate Mock Data
np.random.seed(42)
n_samples = 100  # Number of time snapshots
n_points = 50  # Number of spatial points in each snapshot

# Create synthetic flow data
data = np.random.randn(n_samples, n_points)

# Step 2: Perform POD using SVD
U, S, Vt = np.linalg.svd(data, full_matrices=False)
eigenvalues = S**2 / (n_samples - 1)  # Eigenvalues from the SVD

# Calculate the percentage of TKE for each mode
total_energy = np.sum(eigenvalues)
tke_percentage = (eigenvalues / total_energy) * 100

# Step 3: Plot Eigenvalues and TKE
modes = np.arange(1, len(eigenvalues) + 1)

fig, ax1 = plt.subplots()

# Plot eigenvalues
ax1.plot(modes[:10], eigenvalues[:10], "o-", color="b")
ax1.set_xlabel("Mode #")
ax1.set_ylabel("$\lambda_i$", color="b")
ax1.tick_params(axis="y", labelcolor="b")

# Create a second y-axis for the TKE percentage
ax2 = ax1.twinx()
ax2.plot(modes[:10], tke_percentage[:10], "o-", color="r")
ax2.set_ylabel("% TKE", color="r")
ax2.tick_params(axis="y", labelcolor="r")

plt.title("Eigenvalues and TKE Percentage from POD")
plt.show()
