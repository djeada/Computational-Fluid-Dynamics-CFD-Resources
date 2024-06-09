import numpy as np
import matplotlib.pyplot as plt

# Seed for reproducibility
np.random.seed(0)

# Generate synthetic data for the plots
u_prime_a = np.random.normal(0, 2, 1000)
u_prime_b = 0.7 * u_prime_a + np.random.normal(0, 2, 1000)  # Shifted diagonally

# Calculate the covariance matrix and its eigenvalues and eigenvectors
cov_matrix = np.cov(u_prime_a, u_prime_b)
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# Eigenvector directions
ev1 = eigenvectors[:, 0]
ev2 = eigenvectors[:, 1]

# Project data onto eigenvectors
u_proj_ev1 = u_prime_a * ev1[0] + u_prime_b * ev1[1]
u_proj_ev2 = u_prime_a * ev2[0] + u_prime_b * ev2[1]

# Rotate the projections back to the original space for visualization
u_proj_ev1_rot = u_proj_ev1 * ev1[0]
u_proj_ev2_rot = u_proj_ev2 * ev2[1]

# Function to plot the raw data with eigenvectors
def plot_raw_data_with_eigenvectors(u_prime_a, u_prime_b, ev1, ev2):
    plt.figure(figsize=(10, 8))
    plt.scatter(u_prime_a, u_prime_b, s=10, alpha=0.6, label='Data')
    plt.quiver(0, 0, ev1[0], ev1[1], angles='xy', scale_units='xy', scale=1, color='black', label='EV 1')
    plt.quiver(0, 0, ev2[0], ev2[1], angles='xy', scale_units='xy', scale=1, color='gray', linestyle='-', label='EV 2')
    plt.xlabel(r"$u'_a\ (m/s)$")
    plt.ylabel(r"$u'_b\ (m/s)$")
    plt.title("Raw Data with Directions of Eigenvectors (EVs) of the Covariance Matrix")
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to plot projections on the eigenvectors
def plot_projections_on_eigenvectors(u_prime_a, u_prime_b, u_proj_ev1_rot, u_proj_ev2_rot, ev1, ev2):
    plt.figure(figsize=(10, 8))
    plt.scatter(u_prime_a, u_prime_b, s=10, alpha=0.3, label='Data')
    plt.scatter(u_proj_ev1_rot, u_proj_ev1_rot * (ev1[1] / ev1[0]), s=10, alpha=0.6, color='red', label='Proj on EV1')
    plt.scatter(u_proj_ev2_rot * (ev2[0] / ev2[1]), u_proj_ev2_rot, s=10, alpha=0.6, color='blue', label='Proj on EV2')
    plt.quiver(0, 0, ev1[0], ev1[1], angles='xy', scale_units='xy', scale=1, color='black', label='EV 1')
    plt.quiver(0, 0, ev2[0], ev2[1], angles='xy', scale_units='xy', scale=1, color='gray', linestyle='-', label='EV 2')
    plt.xlabel(r"$u'_a\ (m/s)$")
    plt.ylabel(r"$u'_b\ (m/s)$")
    plt.title("Projection of Data Points on Eigenvectors of the Covariance Matrix")
    plt.legend()
    plt.grid(True)
    plt.show()

# Plotting the figures
plot_raw_data_with_eigenvectors(u_prime_a, u_prime_b, ev1, ev2)
plot_projections_on_eigenvectors(u_prime_a, u_prime_b, u_proj_ev1_rot, u_proj_ev2_rot, ev1, ev2)
