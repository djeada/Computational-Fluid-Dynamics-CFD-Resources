import numpy as np
import matplotlib.pyplot as plt


def numerical_solution(N, x):
    """Compute a numerical approximation for the given x values and parameter N."""
    return np.exp(-x * (1 + x / N))


# Generate fine grid points for smoother curves
x_fine = np.linspace(0, 1, 100)

# Calculate exact solution
u_exact_fine = np.exp(-x_fine)

# Calculate numerical solutions for different N values
N_values = [4, 8, 16]
u_n_fine = {N: numerical_solution(N, x_fine) for N in N_values}

# Create the plot with corrected numerical solutions
plt.figure(figsize=(8, 6))
plt.plot(x_fine, u_exact_fine, label="Exact solution", color="black")

colors = {4: "r-", 8: "b--", 16: "m:"}
for N, color in colors.items():
    plt.plot(x_fine, u_n_fine[N], color, label=f"N={N}")

# Calculate scatter points for discrete solutions
x_discrete = np.array([0, 0.25, 0.5, 0.75, 1])
u_n_discrete = {N: numerical_solution(N, x_discrete) for N in N_values}

# Plot scatter points
scatter_colors = {4: "red", 8: "blue", 16: "magenta"}
for N, color in scatter_colors.items():
    plt.scatter(x_discrete, u_n_discrete[N], color=color)

plt.xlabel("x")
plt.ylabel("u")
plt.legend()
plt.title("Comparison of Numerical and Exact Solutions")
plt.grid(True)
plt.show()
