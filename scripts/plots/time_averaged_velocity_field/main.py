import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic instantaneous longitudinal velocity field data
x = np.linspace(1750, 1900, 200)
y = np.linspace(0, 60, 60)
X, Y = np.meshgrid(x, y)
instantaneous_velocity_field = 10 * np.sin(0.02 * X) * np.cos(
    0.1 * Y
) + 5 * np.random.randn(*X.shape)

# Calculate the time-averaged velocity field by averaging the instantaneous field along the x-axis
time_averaged_field = np.mean(instantaneous_velocity_field, axis=1)

# Create the figure and plot
plt.figure(figsize=(10, 10))

# Plot the instantaneous velocity field (top plot)
plt.subplot(2, 1, 1)
plt.imshow(
    instantaneous_velocity_field, extent=[1750, 1900, 0, 60], aspect="auto", cmap="jet"
)
plt.colorbar(label="U (m/s)")
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.title("Instantaneous longitudinal velocity field")

# Plot the time-averaged velocity field (bottom plot)
plt.subplot(2, 1, 2)
plt.contourf(
    X, Y, np.tile(time_averaged_field, (X.shape[1], 1)).T, levels=50, cmap="jet"
)
plt.colorbar(label="U (m/s)")
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.title("Time-averaged longitudinal velocity field")

plt.tight_layout()
plt.show()
