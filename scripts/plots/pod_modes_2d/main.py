import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate Synthetic Data

# Time vector
t = np.linspace(0.9, 1.1, 1000)

# Generate synthetic velocity data with clear periodic components
U = np.sin(2 * np.pi * t * 10) + 0.5 * np.sin(4 * np.pi * t * 10) + np.random.randn(len(t)) * 0.1
V = np.cos(2 * np.pi * t * 10) + 0.5 * np.cos(4 * np.pi * t * 10) + np.random.randn(len(t)) * 0.1

# Stack velocity data
velocity_data = np.vstack((U, V)).T

# Step 2: Apply SVD for POD

# Perform Singular Value Decomposition (SVD)
U_svd, S, VT = np.linalg.svd(velocity_data, full_matrices=False)

# Extract the modes and singular values
modes = VT.T
singular_values = S

# Calculate the POD modes (Phi) and coefficients (A)
Phi = U_svd
A = np.dot(np.diag(S), VT)

# Number of modes to retain
num_modes = 2

# Truncated POD modes and coefficients
Phi_truncated = Phi[:, :num_modes]
A_truncated = A[:num_modes, :]

# Step 3: Correctly Calculate Mode Contributions

# Calculate contributions over the entire time series
mode1_contribution = np.dot(Phi_truncated[:, 0].reshape(-1, 1), A_truncated[0, :].reshape(1, -1))
mode2_contribution = np.dot(Phi_truncated[:, 1].reshape(-1, 1), A_truncated[1, :].reshape(1, -1))

# Sum contributions for combined effect
combined_contribution = mode1_contribution + mode2_contribution

# Ensure proper alignment
t_aligned = t

# Step 4: Plot Contributions

# Plot the contributions
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(t_aligned, mode1_contribution[:, 0], 'r', label='$\\overline{U}_1$')
plt.plot(t_aligned, mode2_contribution[:, 0], 'b', label='$\\overline{U}_2$')
plt.plot(t_aligned, combined_contribution[:, 0], 'k--', label='$U=\\overline{U}_1+\\overline{U}_2$')
plt.xlabel('t (s)')
plt.ylabel("$u'_a$ (m/s)")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t_aligned, mode1_contribution[:, 0], 'r', label='$\\overline{U}_1$')
plt.plot(t_aligned, mode2_contribution[:, 0], 'b', label='$\\overline{U}_2$')
plt.plot(t_aligned, combined_contribution[:, 0], 'k--', label='$U=\\overline{U}_1+\\overline{U}_2$')
plt.xlabel('t (s)')
plt.ylabel("$u'_b$ (m/s)")
plt.legend()

plt.suptitle("Figure 10. Contributions from modes 1 and 2 to $u'_a$ and $u'_b$")
plt.show()
