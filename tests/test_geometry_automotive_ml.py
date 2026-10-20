"""Shape PCA, Sobol indices and learned mesh sizing: numerical contracts."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_script(category, name):
    spec = importlib.util.spec_from_file_location(
        f"{name}_under_test", ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pca = load_script("algorithms", "airfoil_shape_pca")
sobol = load_script("algorithms", "sobol_sensitivity_analysis")
sizing = load_script("algorithms", "adaptive_mesh_sizing")


class AirfoilShapePCATests(unittest.TestCase):
    def setUp(self):
        self.x = pca.cosine_stations()
        rng = np.random.default_rng(0)
        self.shapes = pca.build_shape_matrix(self.x, pca.sample_parameters(40, rng))
        self.pod = pca.compute_pod(self.shapes)

    def test_all_modes_reconstruct_training_shapes_exactly(self):
        rank = self.pod.singular_values.size
        np.testing.assert_allclose(
            pca.reconstruct(self.pod, self.shapes, rank), self.shapes, atol=1e-12
        )

    def test_zero_modes_give_the_mean_shape(self):
        mean_only = pca.reconstruct(self.pod, self.shapes, 0)
        np.testing.assert_allclose(mean_only, np.repeat(self.pod.mean, 40, axis=1))

    def test_reconstruction_error_decreases_with_modes(self):
        _, mean_err, _ = pca.reconstruction_errors(self.pod, self.shapes, 8)
        self.assertTrue(np.all(np.diff(mean_err) <= 1e-15))

    def test_naca_thickness_formula(self):
        x = np.linspace(0.0, 1.0, 20001)
        thickness = 2.0 * pca.naca_thickness(x, 0.12)
        # The maximum thickness equals t and sits near 30% chord.
        self.assertAlmostEqual(thickness.max(), 0.12, delta=0.12 * 2e-3)
        self.assertAlmostEqual(x[thickness.argmax()], 0.30, delta=0.01)
        # Open trailing edge: half-thickness 5 t (sum of coefficients) = 0.0105 t.
        self.assertAlmostEqual(pca.naca_thickness(1.0, 0.12), 0.0105 * 0.12, places=12)
        self.assertEqual(pca.naca_thickness(0.0, 0.12), 0.0)

    def test_naca_camber_peak_and_continuity(self):
        x = np.linspace(0.0, 1.0, 10001)
        camber = pca.naca_camber(x, 0.04, 0.4)
        self.assertAlmostEqual(camber.max(), 0.04, places=6)
        self.assertAlmostEqual(x[camber.argmax()], 0.4, delta=1e-3)
        self.assertAlmostEqual(camber[0], 0.0)
        self.assertAlmostEqual(camber[-1], 0.0)

    def test_thickness_only_family_has_one_mode(self):
        params = np.column_stack(
            [np.zeros(10), np.full(10, 0.4), np.linspace(0.06, 0.18, 10)]
        )
        pod = pca.compute_pod(pca.build_shape_matrix(self.x, params))
        self.assertEqual(pod.singular_values.size, 1)


class SobolSensitivityTests(unittest.TestCase):
    def test_analytic_indices_partition_the_variance(self):
        first, total, variance = sobol.analytic_indices()
        interaction = sobol.INTERACTION_13**2 / 9.0 / variance
        self.assertAlmostEqual(first.sum() + interaction, 1.0, places=12)
        np.testing.assert_allclose(total - first, [interaction, 0, interaction, 0, 0])

    def test_analytic_variance_matches_sampling(self):
        rng = np.random.default_rng(1)
        values = sobol.drag_model(rng.random((400_000, 5)))
        _, _, variance = sobol.analytic_indices()
        self.assertAlmostEqual(values.var() / variance, 1.0, delta=0.01)
        self.assertAlmostEqual(values.mean(), sobol.CD_BASE, delta=1e-4)

    def test_estimates_match_analytic_values(self):
        rng = np.random.default_rng(2)
        a, b = sobol.sample_matrices(2**13, 5, rng, "qmc")
        first, total = sobol.saltelli_indices(sobol.drag_model, a, b)
        first_exact, total_exact, _ = sobol.analytic_indices()
        np.testing.assert_allclose(first, first_exact, atol=0.01)
        np.testing.assert_allclose(total, total_exact, atol=0.01)

    def test_inert_parameter_has_exactly_zero_total_index(self):
        rng = np.random.default_rng(3)
        a, b = sobol.sample_matrices(256, 5, rng, "mc")
        _, total = sobol.saltelli_indices(sobol.drag_model, a, b)
        self.assertEqual(total[4], 0.0)


class AdaptiveMeshSizingTests(unittest.TestCase):
    def test_uniform_fem_converges_at_second_order(self):
        errors = []
        for n in (40, 80, 160):
            nodes = np.linspace(0.0, 1.0, n + 1)
            errors.append(sizing.l2_error(nodes, sizing.solve_fem(nodes, 10.0), 10.0))
        rates = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(rates, 2.0, atol=0.1)

    def test_fem_reproduces_boundary_values(self):
        nodes = sizing.equidistribute(
            sizing.reference_grid(300),
            sizing.optimal_density(sizing.reference_grid(300), 300),
            30,
        )
        u = sizing.solve_fem(nodes, 300.0)
        self.assertEqual((u[0], u[-1]), (0.0, 1.0))

    def test_equidistribution_gives_equal_density_mass(self):
        pe = 300.0
        x = sizing.reference_grid(pe)
        rho = sizing.optimal_density(x, pe)
        nodes = sizing.equidistribute(x, rho, 25)
        cumulative = np.concatenate(
            [[0.0], np.cumsum(0.5 * (rho[1:] + rho[:-1]) * np.diff(x))]
        )
        masses = np.diff(np.interp(nodes, x, cumulative))
        np.testing.assert_allclose(masses, 1.0 / 25, rtol=1e-6)
        self.assertAlmostEqual(cumulative[-1], 1.0, places=12)

    def test_adapted_and_learned_meshes_beat_uniform(self):
        phi, y = sizing.training_set(sizing.TRAIN_PECLET)
        coef = sizing.fit_ridge(phi, y)
        curves = sizing.error_curves(300, coef, node_counts=np.array([40]))
        uniform = curves["uniform"][0]
        adapted = curves["adapted (exact $u''$)"][0]
        learned = curves["ML-predicted size field"][0]
        self.assertLess(adapted, uniform / 100)
        self.assertLess(learned, 2.0 * adapted)


if __name__ == "__main__":
    unittest.main()
