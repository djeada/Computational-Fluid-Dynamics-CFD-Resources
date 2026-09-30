"""Reusable POD calculations with snapshots stored as columns.

Numerical helpers deliberately have no dependency on plotting or CLI code.
"""

from dataclasses import dataclass

import numpy as np


def create_snapshot_matrix(data: np.ndarray) -> np.ndarray:
    """Flatten spatial axes, preserving the final axis as time."""
    data = np.asarray(data)
    if data.ndim < 2:
        raise ValueError("data needs at least one spatial axis and one time axis")
    return data.reshape(-1, data.shape[-1])


@dataclass(frozen=True)
class PODResult:
    """Orthonormal spatial modes and amplitude-scaled temporal coefficients.

    ``modes @ coefficients`` reconstructs the fluctuations. Adding ``mean``
    reconstructs the original data. Zero-energy inputs have no retained modes.
    """

    mean: np.ndarray
    modes: np.ndarray
    singular_values: np.ndarray
    coefficients: np.ndarray
    n_snapshots: int

    @property
    def eigenvalues(self) -> np.ndarray:
        return self.singular_values**2 / (self.n_snapshots - 1)

    @property
    def energy_fractions(self) -> np.ndarray:
        energy = self.singular_values**2
        return energy / energy.sum() if energy.size else energy

    def reconstruct(self, n_modes: int | None = None) -> np.ndarray:
        """Reconstruct all snapshots, optionally keeping only leading modes."""
        if n_modes is None:
            n_modes = self.singular_values.size
        if not 0 <= n_modes <= self.singular_values.size:
            raise ValueError("n_modes must be between zero and the retained rank")
        return self.mean + self.modes[:, :n_modes] @ self.coefficients[:n_modes]


def compute_pod(snapshots: np.ndarray, method: str = "svd") -> PODResult:
    """Compute POD by thin SVD or the temporal correlation eigensystem.

    Input shape is (spatial points, snapshots), with at least two snapshots.
    Discard numerical null modes rather than normalizing round-off noise.
    """
    snapshots = np.asarray(snapshots, dtype=float)
    if snapshots.ndim != 2 or snapshots.shape[0] == 0 or snapshots.shape[1] < 2:
        raise ValueError(
            "expected a nonempty spatial matrix with at least two snapshots"
        )
    if not np.isfinite(snapshots).all():
        raise ValueError("snapshots must contain only finite values")
    # Center relative to the first snapshot to avoid spurious energy in a
    # constant field when summation rounds its mean (for example, 0.1).
    mean = snapshots[:, :1] + (snapshots - snapshots[:, :1]).mean(axis=1, keepdims=True)
    centered = snapshots - mean
    if method == "svd":
        modes, singular_values, temporal = np.linalg.svd(centered, full_matrices=False)
        threshold = np.finfo(float).eps * max(centered.shape) * singular_values[0]
        keep = singular_values > threshold
        modes = modes[:, keep]
        singular_values = singular_values[keep]
        coefficients = singular_values[:, None] * temporal[keep]
    elif method == "snapshot":
        correlation = centered.T @ centered / (snapshots.shape[1] - 1)
        eigenvalues, eigenvectors = np.linalg.eigh(correlation)
        order = np.argsort(eigenvalues)[::-1]
        eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
        # Forming C squares the condition number: use a tolerance in eigenvalue units.
        threshold = np.finfo(float).eps * max(centered.shape) * max(eigenvalues[0], 0.0)
        keep = eigenvalues > threshold
        singular_values = np.sqrt(eigenvalues[keep] * (snapshots.shape[1] - 1))
        temporal = eigenvectors[:, keep].T
        modes = (centered @ temporal.T) / singular_values
        coefficients = singular_values[:, None] * temporal
    else:
        raise ValueError("method must be 'svd' or 'snapshot'")
    return PODResult(mean, modes, singular_values, coefficients, snapshots.shape[1])


def generate_synthetic_data(
    n_samples: int, n_x: int, n_y: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Shared three-structure field for comparing SVD and snapshot POD."""
    x = np.linspace(1700, 2000, n_x)  # mm
    y = np.linspace(0, 100, n_y)  # mm
    t = np.linspace(0, 4, n_samples)  # s
    X, Y, T = np.meshgrid(x, y, t, indexing="ij")
    data = (
        np.sin(0.02 * X) * np.cos(0.05 * Y) * np.sin(0.5 * T)
        + 0.5 * np.cos(0.04 * X) * np.sin(0.1 * Y) * np.cos(2.0 * T)
        + 0.25 * np.sin(0.06 * X) * np.cos(0.15 * Y) * np.sin(4.0 * T)
    )
    return data, x, y, t
