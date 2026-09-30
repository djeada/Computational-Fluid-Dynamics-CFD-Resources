"""POD contracts: reconstruction, energy, rank, and independent formulations."""

import unittest

import numpy as np

from scripts._numerics import (
    compute_pod,
    create_snapshot_matrix,
    generate_synthetic_data,
)


class PODTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(7)
        self.data = rng.normal(size=(8, 12)) + np.arange(8)[:, None]

    def test_reconstruction_and_orthonormality(self):
        for method in ("svd", "snapshot"):
            with self.subTest(method=method):
                result = compute_pod(self.data, method)
                np.testing.assert_allclose(result.reconstruct(), self.data, atol=1e-12)
                np.testing.assert_allclose(
                    result.modes.T @ result.modes, np.eye(8), atol=1e-12
                )
                self.assertAlmostEqual(result.energy_fractions.sum(), 1.0)
                expected_variance = np.var(self.data, axis=1, ddof=1).sum()
                self.assertAlmostEqual(result.eigenvalues.sum(), expected_variance)

    def test_svd_and_snapshot_subspaces_agree(self):
        direct = compute_pod(self.data)
        snapshot = compute_pod(self.data, "snapshot")
        np.testing.assert_allclose(
            direct.singular_values, snapshot.singular_values, atol=1e-12
        )
        # Comparing outer products avoids dependence on arbitrary eigenvector signs.
        for index in range(3):
            np.testing.assert_allclose(
                np.outer(direct.modes[:, index], direct.modes[:, index]),
                np.outer(snapshot.modes[:, index], snapshot.modes[:, index]),
                atol=1e-12,
            )

    def test_synthetic_field_has_three_modes(self):
        field, *_ = generate_synthetic_data(40, 12, 9)
        for method in ("svd", "snapshot"):
            result = compute_pod(create_snapshot_matrix(field), method)
            self.assertEqual(result.singular_values.size, 3)
            np.testing.assert_allclose(
                result.reconstruct(), create_snapshot_matrix(field), atol=1e-12
            )

    def test_constant_field_has_zero_modes_and_reconstructs_mean(self):
        for method in ("svd", "snapshot"):
            result = compute_pod(np.full((5, 13), 0.1), method)
            self.assertEqual(result.singular_values.size, 0)
            self.assertEqual(result.energy_fractions.size, 0)
            np.testing.assert_allclose(result.reconstruct(), np.full((5, 13), 0.1))

    def test_truncation_error_is_discarded_energy(self):
        result = compute_pod(self.data)
        error = np.linalg.norm(self.data - result.reconstruct(3)) ** 2
        self.assertAlmostEqual(error, np.sum(result.singular_values[3:] ** 2))
        np.testing.assert_allclose(
            result.reconstruct(0), np.broadcast_to(result.mean, self.data.shape)
        )
        with self.assertRaises(ValueError):
            result.reconstruct(-1)
        with self.assertRaises(ValueError):
            result.reconstruct(100)

    def test_invalid_inputs_fail_explicitly(self):
        for data in ([], np.ones(3), np.ones((0, 5)), np.ones((3, 1)), [[1, np.nan]]):
            with self.subTest(data=data), self.assertRaises(ValueError):
                compute_pod(data)
        with self.assertRaises(ValueError):
            compute_pod(self.data, method="invalid")

    def test_flatten_preserves_time_and_spatial_order(self):
        field = np.arange(24).reshape(2, 3, 4)
        flattened = create_snapshot_matrix(field)
        np.testing.assert_array_equal(flattened[4], field[1, 1])
