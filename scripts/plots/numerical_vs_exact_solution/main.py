import numpy as np
import matplotlib.pyplot as plt

# Define the given numerical solution points
x_numerical = np.array([0, 0.25, 0.5, 0.75, 1])
u_numerical = np.array([1, 3/4, 9/16, 27/64, 27/64])

# Exact solution
u_exact = np.exp(-x_numerical)

# Generate fine grid points for the exact solution curve
x_fine = np.linspace(0, 1, 100)
u_exact_fine = np.exp(-x_fine)

# Create the plot
plt.figure(figsize=(6, 6))
plt.plot(x_fine, u_exact_fine, label='Exact solution', color='black')
plt.plot(x_numerical, u_numerical, 'ro-', label='Numerical solution', markersize=5)
plt.xlabel('x')
plt.ylabel('u')
plt.legend()
plt.grid(True)
plt.show()
