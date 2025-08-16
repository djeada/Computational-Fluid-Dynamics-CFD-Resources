import numpy as np
import matplotlib.pyplot as plt

# Parameters
N = 100  # Number of grid points
max_iterations = 20  # Maximum number of iterations
convergence_criterion = 1e-9

# Initial guess for u
u = np.ones(N)
u_new = np.zeros_like(u)


# Compute the residual as described
def compute_residual(u, u_old):
    return np.sqrt(np.mean((u - u_old) ** 2)) / np.mean(u_old)


# Store residuals
residuals = []

# Iterative update process
for iteration in range(max_iterations):
    u_old = u.copy()
    for i in range(1, N - 1):
        u_new[i] = 0.5 * (u[i - 1] + u[i + 1])  # Simple update rule for demonstration
    u = u_new.copy()

    residual = compute_residual(u, u_old)
    residuals.append(residual)

    if residual < convergence_criterion:
        break

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(residuals) + 1), residuals, marker="o", color="r")
plt.yscale("log")
plt.xlabel("Iteration number")
plt.ylabel("Residual")
plt.title("Variation of the residual with iterations")
plt.grid(True)
plt.show()
