import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf


# Define the original function
def y(x):
    return (3 * x - 3) ** 2 * np.sin(2 * x - 10)


# Generate original data points
x_data = np.linspace(0, 1, 11)
y_data = y(x_data)
x_fine = np.linspace(0, 1, 100)


# Define the cubic spline basis function with a fixed epsilon
def make_cubic_spline_basis(epsilon):
    def cubic_spline_basis(r):
        abs_r = epsilon * np.abs(r)
        return np.where(
            abs_r <= 1,
            1 - 1.5 * abs_r**2 + 0.75 * abs_r**3,
            np.where(abs_r <= 2, 0.25 * (2 - abs_r) ** 3, 0),
        )

    return cubic_spline_basis


# Define theta values
theta_values = [0.1, 3, 6.5, 10.0]

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Perform and plot Kriging interpolation for each theta
for ax, theta in zip(axs.ravel(), theta_values):
    cubic_spline = make_cubic_spline_basis(theta)
    rbf = Rbf(x_data, y_data, function=cubic_spline)
    y_fine = rbf(x_fine)

    ax.plot(x_fine, y(x_fine), "k--", label="$y(x)$")
    ax.plot(x_fine, y_fine, "b-", label="$\\tilde{y}(x)$")
    ax.plot(x_data, y_data, "ks")
    ax.set_title(f"$\\theta={theta}$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend()

plt.tight_layout()
plt.show()
