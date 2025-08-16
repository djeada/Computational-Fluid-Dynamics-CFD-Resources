import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import cond


# Define the correlation functions
def linear(h, theta):
    return np.maximum(0, 1 - theta * np.abs(h))


def exponential(h, theta):
    return np.exp(-theta * np.abs(h))


def gaussian(h, theta):
    return np.exp(-theta * (h**2))


def cubic_spline(h, theta):
    abs_h = np.abs(h)
    return np.where(
        abs_h <= 1,
        1 - 1.5 * abs_h**2 + 0.75 * abs_h**3,
        np.where(abs_h <= 2, 0.25 * (2 - abs_h) ** 3, 0),
    )


# Generate x values
x = np.linspace(0, 1, 10)

# Generate h matrix
H = x[:, None] - x[None, :]

# Define theta values
theta_values = np.logspace(-2, 1, 100)

# Initialize condition number storage
cond_numbers = {"linear": [], "exponential": [], "gaussian": [], "cubic_spline": []}

# Calculate condition numbers for each theta
for theta in theta_values:
    cond_numbers["linear"].append(cond(linear(H, theta)))
    cond_numbers["exponential"].append(cond(exponential(H, theta)))
    cond_numbers["gaussian"].append(cond(gaussian(H, theta)))
    cond_numbers["cubic_spline"].append(cond(cubic_spline(H, theta)))

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plot linear correlation function
axs[0, 0].plot(theta_values, cond_numbers["linear"], "b-")
axs[0, 0].set_title("linear")
axs[0, 0].set_xlabel("$\\theta$")
axs[0, 0].set_ylabel("cond(R)")
axs[0, 0].set_xscale("log")
axs[0, 0].set_yscale("log")

# Plot exponential correlation function
axs[0, 1].plot(theta_values, cond_numbers["exponential"], "b-")
axs[0, 1].set_title("exponential")
axs[0, 1].set_xlabel("$\\theta$")
axs[0, 1].set_ylabel("cond(R)")
axs[0, 1].set_xscale("log")
axs[0, 1].set_yscale("log")

# Plot Gaussian correlation function
axs[1, 0].plot(theta_values, cond_numbers["gaussian"], "b-")
axs[1, 0].set_title("Gaussian")
axs[1, 0].set_xlabel("$\\theta$")
axs[1, 0].set_ylabel("cond(R)")
axs[1, 0].set_xscale("log")
axs[1, 0].set_yscale("log")

# Plot cubic spline correlation function
axs[1, 1].plot(theta_values, cond_numbers["cubic_spline"], "b-")
axs[1, 1].set_title("cubic spline")
axs[1, 1].set_xlabel("$\\theta$")
axs[1, 1].set_ylabel("cond(R)")
axs[1, 1].set_xscale("log")
axs[1, 1].set_yscale("log")

# Adjust layout and show plot
plt.tight_layout()
plt.show()
