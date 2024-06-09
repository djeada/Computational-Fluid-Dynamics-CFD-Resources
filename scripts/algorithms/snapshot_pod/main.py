import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

def generate_synthetic_data(n_samples: int, n_x: int, n_y: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate synthetic spatio-temporal flow data.
    """
    np.random.seed(42)
    x = np.linspace(1700, 2000, n_x)
    y = np.linspace(0, 100, n_y)
    t = np.linspace(0, 4, n_samples)

    X, Y, T = np.meshgrid(x, y, t, indexing='ij')
    data = np.sin(0.02 * X) * np.cos(0.05 * Y) * np.sin(0.5 * T)
    return data, x, y, t

def preprocess_data(data: np.ndarray) -> np.ndarray:
    """
    Preprocess the data by centering it.
    """
    return data - np.mean(data, axis=1, keepdims=True)

def create_snapshot_matrix(data: np.ndarray) -> np.ndarray:
    """
    Reshape data into a snapshot matrix.
    """
    return data.reshape(data.shape[0] * data.shape[1], data.shape[2])

class SnapshotPOD:
    def __init__(self, snapshot_matrix: np.ndarray):
        self.snapshot_matrix = snapshot_matrix
        self.spatial_modes: np.ndarray = None
        self.time_coeffs: np.ndarray = None
        self.eigenvalues: np.ndarray = None

    def run(self) -> None:
        """
        Perform Snapshot Proper Orthogonal Decomposition (POD).
        """
        U = preprocess_data(self.snapshot_matrix)
        C_s = np.dot(U.T, U) / (U.shape[1] - 1)
        eigenvalues, eigenvectors = np.linalg.eig(C_s)

        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        self.time_coeffs = eigenvectors
        self.spatial_modes = np.dot(U, eigenvectors)
        self.eigenvalues = eigenvalues

    def normalize_modes(self):
        """
        Normalize the spatial modes.
        """
        norms = np.linalg.norm(self.spatial_modes, axis=0)
        self.spatial_modes /= norms

def plot_snapshot_modes_and_time_coeffs(pod: SnapshotPOD, x: np.ndarray, y: np.ndarray, t: np.ndarray, num_modes: int = 3) -> None:
    """
    Plot the spatial modes and their corresponding time coefficients.
    """
    modes_reshaped = pod.spatial_modes[:, :num_modes].reshape(x.shape[0], y.shape[0], -1)

    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(num_modes, 2, width_ratios=[1, 1], height_ratios=[1, 1, 1])

    for i in range(num_modes):
        ax = fig.add_subplot(gs[i, 0])
        c = ax.contourf(x, y, modes_reshaped[:, :, i].T, cmap='jet', levels=50)
        fig.colorbar(c, ax=ax)
        ax.set_title(f'Mode {i+1}')
        ax.set_xlabel('x (mm)')
        ax.set_ylabel('y (mm)')

    for i in range(num_modes):
        ax = fig.add_subplot(gs[i, 1])
        ax.plot(t, pod.time_coeffs[:, i])
        ax.set_title(f'Mode {i+1}')
        ax.set_xlabel('t (s)')
        ax.set_ylabel(f'$a_{i+1}$')

    plt.tight_layout()
    plt.show()

# Example Usage
n_samples = 100  # Number of time snapshots
n_x = 50         # Number of spatial points in x-direction
n_y = 30         # Number of spatial points in y-direction

# Generate synthetic data
data, x, y, t = generate_synthetic_data(n_samples, n_x, n_y)

# Create snapshot matrix
snapshot_matrix = create_snapshot_matrix(data)

# Perform Snapshot POD
pod = SnapshotPOD(snapshot_matrix)
pod.run()
pod.normalize_modes()

# Plot results
plot_snapshot_modes_and_time_coeffs(pod, x, y, t, num_modes=3)
