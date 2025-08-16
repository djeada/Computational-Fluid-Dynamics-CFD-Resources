import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

# Extracted data points (estimated from the plot)
x = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
y = np.array([0.0, 0.5, -0.5, -1.0, -0.5, 0.0, 1.0, 2.0, 4.0, 10.0, 20.0])

# Plot the original points
plt.plot(x, y, "ks", label="Original points")

# Create RBF interpolation function
rbf = Rbf(x, y, function="multiquadric")

# Generate new x values for interpolation
x_new = np.linspace(0, 1, 100)
y_new = rbf(x_new)

# Plot the interpolated function
plt.plot(x_new, y_new, "b-", label="RBF interpolation")

# Plot settings
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title(r"RBF Interpolation $\tilde{y}(x)$")
plt.show()
