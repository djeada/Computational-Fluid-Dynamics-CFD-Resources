import numpy as np
import matplotlib.pyplot as plt


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


# Generate h values
h = np.linspace(-2, 2, 400)

# Define theta values
thetas = [0.5, 1.0, 2.0]

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plot linear correlation function
for theta in thetas:
    axs[0, 0].plot(h, linear(h, theta), label=f"$\\theta={theta}$")
axs[0, 0].set_title("linear")
axs[0, 0].set_xlabel("$h$")
axs[0, 0].set_ylabel("$R(h/\\theta)$")
axs[0, 0].legend()

# Plot exponential correlation function
for theta in thetas:
    axs[0, 1].plot(h, exponential(h, theta), label=f"$\\theta={theta}$")
axs[0, 1].set_title("exponential")
axs[0, 1].set_xlabel("$h$")
axs[0, 1].set_ylabel("$R(h/\\theta)$")
axs[0, 1].legend()

# Plot Gaussian correlation function
for theta in thetas:
    axs[1, 0].plot(h, gaussian(h, theta), label=f"$\\theta={theta}$")
axs[1, 0].set_title("Gaussian")
axs[1, 0].set_xlabel("$h$")
axs[1, 0].set_ylabel("$R(h/\\theta)$")
axs[1, 0].legend()

# Plot cubic spline correlation function
for theta in thetas:
    axs[1, 1].plot(h, cubic_spline(h, theta), label=f"$\\theta={theta}$")
axs[1, 1].set_title("cubic spline")
axs[1, 1].set_xlabel("$h$")
axs[1, 1].set_ylabel("$R(h/\\theta)$")
axs[1, 1].legend()

# Adjust layout and show plot
plt.tight_layout()
plt.show()
