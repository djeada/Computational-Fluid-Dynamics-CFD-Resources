import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Step 1: Generate Mock Data
np.random.seed(42)
n_samples = 100  # Number of time snapshots
n_x = 50        # Number of spatial points in x-direction
n_y = 30         # Number of spatial points in y-direction

# Create synthetic flow data (spatio-temporal field)
x = np.linspace(1700, 2000, n_x)
y = np.linspace(0, 100, n_y)
t = np.linspace(0, 4, n_samples)

X, Y, T = np.meshgrid(x, y, t, indexing='ij')
data = np.sin(0.02*X) * np.cos(0.05*Y) * np.sin(0.5*T)

# Reshape data to 2D matrix for SVD (space-time)
data_reshaped = data.reshape(n_x * n_y, n_samples)

# Step 2: Perform POD using SVD
U, S, Vt = np.linalg.svd(data_reshaped, full_matrices=False)
modes = U[:, :3]  # First three spatial modes
time_coeffs = Vt[:3, :]  # Corresponding time coefficients

# Reshape modes to 2D spatial structure
modes_reshaped = modes.reshape(n_x, n_y, 3)

# Step 3: Plot the Modes and Time Coefficients
fig = plt.figure(figsize=(12, 10))
gs = GridSpec(3, 2, width_ratios=[1, 1], height_ratios=[1, 1, 1])

# Plot spatial modes
for i in range(3):
    ax = fig.add_subplot(gs[i, 0])
    c = ax.contourf(x, y, modes_reshaped[:, :, i].T, cmap='jet', levels=50)
    fig.colorbar(c, ax=ax)
    ax.set_title(f'Mode {i+1}')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')

# Plot time coefficients
for i in range(3):
    ax = fig.add_subplot(gs[i, 1])
    ax.plot(t, time_coeffs[i, :])
    ax.set_title(f'Mode {i+1}')
    ax.set_xlabel('t (s)')
    ax.set_ylabel(f'$a_{i+1}$')

plt.tight_layout()
plt.show()
