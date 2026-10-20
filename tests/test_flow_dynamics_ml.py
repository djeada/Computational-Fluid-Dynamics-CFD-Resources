"""Data-driven flow models: DMD, SINDy, k-means clustering and a learned closure."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(category, name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dmd_example = load_example("algorithms", "dynamic_mode_decomposition")
sindy = load_example("algorithms", "sindy_lorenz")
clustering = load_example("plots", "flow_regime_clustering")
closure = load_example("algorithms", "learned_mixing_length_closure")


class DMDTests(unittest.TestCase):
    def test_exact_eigenvalues_of_linear_system(self):
        rng = np.random.default_rng(3)
        true = np.array([0.95 + 0.2j, 0.95 - 0.2j, 0.8, 1.01, 0.5 + 0.5j, 0.5 - 0.5j])
        # Real block-diagonal form of the spectrum, then a random similarity.
        blocks = np.zeros((6, 6))
        blocks[0:2, 0:2] = [[0.95, -0.2], [0.2, 0.95]]
        blocks[2, 2], blocks[3, 3] = 0.8, 1.01
        blocks[4:6, 4:6] = [[0.5, -0.5], [0.5, 0.5]]
        basis = rng.standard_normal((40, 6))
        lift = np.linalg.qr(basis)[0]
        similarity = rng.standard_normal((6, 6)) + 3 * np.eye(6)
        A = similarity @ blocks @ np.linalg.inv(similarity)
        z = rng.standard_normal(6)
        states = [z]
        for _ in range(30):
            states.append(A @ states[-1])
        X = lift @ np.array(states).T  # 40-dimensional observations of rank 6
        eigenvalues, modes, amplitudes = dmd_example.dmd(X, 6)
        np.testing.assert_allclose(
            np.sort_complex(eigenvalues), np.sort_complex(true), atol=1e-9
        )
        reconstruction = dmd_example.dmd_predict(eigenvalues, modes, amplitudes, 31)
        np.testing.assert_allclose(reconstruction.real, X, atol=1e-8)

    def test_noise_free_wave_field_recovers_frequencies_and_growth(self):
        x = np.linspace(dmd_example.X_MIN, dmd_example.X_MAX, dmd_example.N_X)
        t = dmd_example.DT * np.arange(dmd_example.N_TRAIN)
        clean, _ = dmd_example.make_field(x, t, noise_std=0.0)
        eigenvalues, _, _ = dmd_example.dmd(clean, dmd_example.RANK)
        omega = np.log(eigenvalues) / dmd_example.DT
        true = dmd_example.true_continuous_eigenvalues()
        np.testing.assert_allclose(
            np.sort_complex(omega),
            np.sort_complex(np.concatenate([true, true.conj()])),
            atol=1e-8,
        )


class SINDyTests(unittest.TestCase):
    def test_library_has_twenty_cubic_monomials(self):
        exponents = sindy.library_exponents()
        self.assertEqual(len(exponents), 20)
        self.assertEqual(len(set(exponents)), 20)

    def test_recovers_lorenz_coefficients(self):
        Xi, exponents = sindy.fit_lorenz()
        Xi_true = sindy.true_coefficients(exponents)
        np.testing.assert_array_equal(Xi != 0, Xi_true != 0)
        np.testing.assert_allclose(Xi, Xi_true, rtol=5e-3, atol=1e-12)

    def test_stlsq_returns_least_squares_on_exact_sparse_problem(self):
        rng = np.random.default_rng(0)
        Theta = rng.standard_normal((200, 8))
        Xi_true = np.zeros((8, 2))
        Xi_true[[1, 4], 0] = [2.0, -0.5]
        Xi_true[[0, 7], 1] = [1.0, 3.0]
        Xi = sindy.stlsq(Theta, Theta @ Xi_true, threshold=0.1)
        np.testing.assert_allclose(Xi, Xi_true, atol=1e-12)


class KMeansTests(unittest.TestCase):
    def test_objective_is_non_increasing(self):
        rng = np.random.default_rng(5)
        points = np.vstack(
            [rng.normal(centre, 1.0, size=(60, 4)) for centre in (-3.0, 0.0, 4.0)]
        )
        for seed in range(5):
            _, _, history = clustering.kmeans(points, 3, np.random.default_rng(seed))
            self.assertTrue(np.all(np.diff(history) <= 1e-9 * history[0]))

    def test_regimes_are_recovered_from_pod_coefficients(self):
        snapshots, true_labels, _ = clustering.make_snapshots()
        pod = clustering.compute_pod(snapshots)
        coeffs = pod.coefficients[: clustering.N_POD].T
        labels, _, _ = clustering.best_kmeans(coeffs, clustering.N_CLUSTERS)
        mapped, mapping = clustering.relabel_by_majority(
            labels, true_labels, clustering.N_CLUSTERS
        )
        self.assertEqual(sorted(mapping), [0, 1, 2])
        clean = true_labels >= 0
        self.assertGreater(np.mean(mapped[clean] == true_labels[clean]), 0.99)

    def test_transition_matrix_is_row_stochastic(self):
        matrix = clustering.transition_matrix(np.array([0, 0, 1, 1, 2, 0, 1, 2, 2]), 3)
        np.testing.assert_allclose(matrix.sum(axis=1), 1.0)
        np.testing.assert_allclose(matrix[0], [1 / 3, 2 / 3, 0.0])


class LearnedClosureTests(unittest.TestCase):
    def setUp(self):
        self.y = np.geomspace(0.1, closure.Y_PLUS_MAX, 200)
        self.u_ref = closure.reference_u_plus(self.y)

    def test_reference_inverts_spalding_law(self):
        np.testing.assert_allclose(
            closure.spalding_y_plus(self.u_ref), self.y, rtol=1e-12
        )

    def test_solver_with_implied_closure_reproduces_reference(self):
        y_table = np.geomspace(1e-3, closure.Y_PLUS_MAX, 4000)
        damping_table = closure.implied_closure(y_table)[2]

        def damping(y):
            return np.interp(np.log(y), np.log(y_table), damping_table)

        u = closure.solve_rans(damping, self.y)
        np.testing.assert_allclose(u, self.u_ref, atol=2e-3)

    def test_learned_closure_matches_reference(self):
        _, _, a_plus, closures = closure.build_closures()
        self.assertTrue(20.0 < a_plus < 30.0)
        names = list(closures)
        plain = closure.solve_rans(closures[names[0]], self.y)
        learned = closure.solve_rans(closures[names[1]], self.y)
        self.assertLess(np.abs(learned - self.u_ref).max(), 0.3)
        self.assertGreater(np.abs(plain - self.u_ref).max(), 5.0)
        np.testing.assert_allclose(learned[-1], self.u_ref[-1], rtol=0.02)


if __name__ == "__main__":
    unittest.main()
