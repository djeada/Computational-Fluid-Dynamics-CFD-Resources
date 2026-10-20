"""POD notes: eigen/singular value relations, weighted POD, gappy POD and sensors."""

import importlib.util
import sys
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _numerics import compute_pod  # noqa: E402


def load_example(category, name):
    spec = importlib.util.spec_from_file_location(
        f"{category}_{name}", ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gappy = load_example("algorithms", "gappy_pod_reconstruction")
truncation = load_example("plots", "pod_energy_and_truncation")
two_point = load_example("plots", "eigenvector_projection")


def orthonormal_basis(n, r, rng):
    q, _ = np.linalg.qr(rng.standard_normal((n, r)))
    return q


class EigenAndSingularValueTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(3)
        self.data = rng.standard_normal((30, 12)) @ rng.standard_normal((12, 12))

    def test_eigenvalues_are_squared_singular_values_over_m_minus_one(self):
        result = compute_pod(self.data)
        centered = self.data - self.data.mean(axis=1, keepdims=True)
        covariance = centered @ centered.T / (self.data.shape[1] - 1)
        eigenvalues = np.sort(np.linalg.eigvalsh(covariance))[::-1]
        rank = result.singular_values.size
        self.assertEqual(rank, self.data.shape[1] - 1)  # mean removal costs one
        np.testing.assert_allclose(result.eigenvalues, eigenvalues[:rank], rtol=1e-10)
        np.testing.assert_allclose(eigenvalues[rank:], 0.0, atol=1e-10)
        # Left singular vectors are eigenvectors of the spatial covariance.
        np.testing.assert_allclose(
            covariance @ result.modes, result.modes * result.eigenvalues, atol=1e-10
        )
        snapshot = compute_pod(self.data, method="snapshot")
        np.testing.assert_allclose(snapshot.eigenvalues, result.eigenvalues, rtol=1e-8)

    def test_truncation_error_is_the_discarded_energy(self):
        result = compute_pod(self.data)
        centered = self.data - result.mean
        for r in (1, 3, 6):
            error = centered - result.modes[:, :r] @ result.coefficients[:r]
            self.assertAlmostEqual(
                np.sum(error**2), np.sum(result.singular_values[r:] ** 2), places=8
            )
        fractions = result.energy_fractions
        r90 = truncation.modes_for_energy(fractions, 0.9)
        self.assertGreaterEqual(fractions[:r90].sum(), 0.9 - 1e-12)
        self.assertLess(fractions[: r90 - 1].sum(), 0.9)

    def test_two_point_example_principal_axes(self):
        data = two_point.generate_fluctuations()
        cov, eigenvalues, eigenvectors = two_point.principal_directions(data)
        self.assertAlmostEqual(eigenvalues.sum(), np.trace(cov))
        coefficients = eigenvectors.T @ data
        np.testing.assert_allclose(
            coefficients @ coefficients.T / (data.shape[1] - 1),
            np.diag(eigenvalues),
            atol=1e-10,
        )
        # Sample covariance near the exact [[5, 2.8], [2.8, 5]] of the model.
        exact = np.array([[5.0, 2.8], [2.8, 5.0]])
        np.testing.assert_allclose(cov, exact, rtol=0.1)


class WeightedPODTests(unittest.TestCase):
    def setUp(self):
        self.x, self.y = truncation.stretched_mesh(n_x=30, n_y=16)
        t = truncation.DT * np.arange(40)
        self.data = truncation.wake_snapshots(self.x, self.y, t)
        self.weights = truncation.area_weights(self.x, self.y)

    def test_area_weights_integrate_constants_exactly(self):
        area = (self.x[-1] - self.x[0]) * (self.y[-1] - self.y[0])
        self.assertAlmostEqual(self.weights.sum(), area)

    def test_modes_are_orthonormal_in_the_weighted_inner_product(self):
        pod = truncation.weighted_pod(self.data, self.weights)
        gram = pod.modes.T @ (self.weights[:, None] * pod.modes)
        np.testing.assert_allclose(gram, np.eye(gram.shape[0]), atol=1e-10)
        np.testing.assert_allclose(pod.reconstruct(), self.data, atol=1e-10)
        # Coefficients are weighted projections, a = Phi^T W u'.
        projected = pod.modes.T @ (self.weights[:, None] * (self.data - pod.mean))
        np.testing.assert_allclose(projected, pod.coefficients, atol=1e-10)
        # Modes solve C W phi = lambda phi, and the energies sum to the
        # area-weighted variance.
        centered = self.data - pod.mean
        cov = centered @ centered.T / (self.data.shape[1] - 1)
        np.testing.assert_allclose(
            cov @ (self.weights[:, None] * pod.modes[:, :5]),
            pod.modes[:, :5] * pod.eigenvalues[:5],
            atol=1e-9,
        )
        variance = np.var(self.data, axis=1, ddof=1)
        self.assertAlmostEqual(pod.eigenvalues.sum(), (self.weights * variance).sum())


class GappyPODTests(unittest.TestCase):
    def test_exact_recovery_when_the_field_lies_in_the_span(self):
        rng = np.random.default_rng(0)
        modes = orthonormal_basis(200, 5, rng)
        mean = rng.standard_normal(200)
        coeffs = rng.standard_normal(5)
        field = mean + modes @ coeffs
        for observed in (rng.random(200) < 0.1, gappy.qr_sensors(modes, 5)):
            np.testing.assert_allclose(
                gappy.gappy_coefficients(modes, mean, field, observed),
                coeffs,
                atol=1e-10,
            )
            np.testing.assert_allclose(
                gappy.gappy_reconstruct(modes, mean, field, observed),
                field,
                atol=1e-10,
            )

    def test_full_mask_reduces_to_orthogonal_projection(self):
        rng = np.random.default_rng(1)
        modes = orthonormal_basis(80, 4, rng)
        field = rng.standard_normal(80)
        mean = np.zeros(80)
        coeffs = gappy.gappy_coefficients(modes, mean, field, np.ones(80, bool))
        np.testing.assert_allclose(coeffs, modes.T @ field, atol=1e-12)

    def test_qr_sensors_are_distinct_and_start_with_the_qr_pivots(self):
        from scipy.linalg import qr

        rng = np.random.default_rng(2)
        modes = orthonormal_basis(150, 6, rng)
        sensors = gappy.qr_sensors(modes, 15)
        self.assertEqual(len(set(sensors.tolist())), 15)
        _, _, pivots = qr(modes.T, mode="economic", pivoting=True)
        np.testing.assert_array_equal(sensors[:6], pivots[:6])
        # Each greedy step can only increase det(Theta^T Theta).
        dets = [
            np.linalg.det(modes[sensors[:p]].T @ modes[sensors[:p]])
            for p in range(6, 16)
        ]
        self.assertTrue(np.all(np.diff(dets) > 0))

    def test_qr_placement_no_worse_than_random_on_average(self):
        rng = np.random.default_rng(4)
        x = np.linspace(*gappy.X_RANGE, 60)
        y = np.linspace(*gappy.Y_RANGE, 24)
        train = gappy.wake_snapshots(x, y, gappy.DT * np.arange(120))
        test = gappy.wake_snapshots(x, y, np.linspace(41.0, 55.0, 8), noise_seed=9)
        pod = compute_pod(train)
        modes = pod.modes[:, :8]
        for p in (8, 12, 16):
            sensors = gappy.qr_sensors(modes, p)
            qr_error = gappy.relative_error(
                gappy.reconstruct_all(modes, pod.mean, test, sensors), test, pod.mean
            )
            random_errors = [
                gappy.relative_error(
                    gappy.reconstruct_all(
                        modes,
                        pod.mean,
                        test,
                        gappy.random_sensors(modes.shape[0], p, rng),
                    ),
                    test,
                    pod.mean,
                )
                for _ in range(30)
            ]
            self.assertLessEqual(qr_error, np.mean(random_errors))
            random_cond = np.median(
                [
                    np.linalg.cond(modes[gappy.random_sensors(modes.shape[0], p, rng)])
                    for _ in range(30)
                ]
            )
            self.assertLess(np.linalg.cond(modes[sensors]), random_cond)

    def test_everson_sirovich_filling_recovers_low_rank_data(self):
        rng = np.random.default_rng(5)
        modes = orthonormal_basis(120, 3, rng)
        mean = rng.standard_normal(120)[:, None]
        truth = mean + modes @ (rng.standard_normal((3, 40)) * [[5.0], [2.0], [1.0]])
        observed = rng.random(truth.shape) >= 0.2
        filled, _, errors = gappy.iterative_gappy_pod(
            np.where(observed, truth, np.nan), observed, 3, 30, truth=truth
        )
        self.assertLess(errors[-1], 1e-6)
        self.assertLess(errors[-1], errors[0])
        np.testing.assert_allclose(filled, truth, atol=1e-5)


if __name__ == "__main__":
    unittest.main()
