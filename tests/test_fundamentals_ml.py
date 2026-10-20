"""Check the ML-fundamentals scripts: backprop gradients, Adam, classical learners."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_script(category, name):
    spec = importlib.util.spec_from_file_location(
        f"{name}_main", ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mlp = load_script("algorithms", "mlp_regression")
paradigms = load_script("plots", "ml_learning_paradigms")
bias_variance = load_script("plots", "bias_variance_tradeoff")


class MLPTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        self.params = mlp.init_params((2, 5, 4, 3), rng)
        # Non-zero biases so their gradients are exercised too.
        self.params = [(w, 0.1 * rng.standard_normal(b.shape)) for w, b in self.params]
        self.x = rng.standard_normal((7, 2))
        self.y = rng.standard_normal((7, 3))

    def loss(self, params):
        return mlp.mse_loss(mlp.forward(params, self.x)[0], self.y)

    def test_backprop_matches_central_differences(self):
        _, activations = mlp.forward(self.params, self.x)
        grads = mlp.backward(self.params, activations, self.y)
        step = 1e-6
        for layer, (weight, bias) in enumerate(self.params):
            for which, array in ((0, weight), (1, bias)):
                numeric = np.zeros_like(array)
                for index in np.ndindex(array.shape):
                    shifted = []
                    for sign in (1.0, -1.0):
                        perturbed = [(w.copy(), b.copy()) for w, b in self.params]
                        perturbed[layer][which][index] += sign * step
                        shifted.append(self.loss(perturbed))
                    numeric[index] = (shifted[0] - shifted[1]) / (2.0 * step)
                with self.subTest(layer=layer, which=which):
                    np.testing.assert_allclose(
                        grads[layer][which], numeric, rtol=1e-6, atol=1e-9
                    )

    def test_xavier_initialisation_variance(self):
        params = mlp.init_params((400, 600), np.random.default_rng(0))
        self.assertAlmostEqual(params[0][0].var(), 2.0 / 1000.0, delta=2e-4)
        np.testing.assert_array_equal(params[0][1], 0.0)

    def test_adam_fits_linear_map(self):
        rng = np.random.default_rng(1)
        x = rng.uniform(-1, 1, (50, 1))
        y = 0.7 * x - 0.2
        params = mlp.init_params((1, 1), rng)  # no hidden layer: linear model
        params, history, _ = mlp.train(params, x, y, epochs=1500, lr=0.05)
        np.testing.assert_allclose(params[0][0], [[0.7]], atol=1e-4)
        np.testing.assert_allclose(params[0][1], [-0.2], atol=1e-4)
        self.assertLess(history["train"][-1], 1e-8)

    def test_lift_curve_slope_and_fit(self):
        alpha = np.array([-1e-3, 1e-3])
        slope = np.diff(mlp.lift_coefficient(alpha))[0] / np.radians(2e-3)
        self.assertAlmostEqual(slope, 2.0 * np.pi, delta=1e-3)
        result = mlp.fit_lift_curve()
        history = result["history"]
        self.assertLess(np.sqrt(history["train"][-1]), mlp.NOISE_STD)
        self.assertLess(np.sqrt(history["val"][-1]), 2.0 * mlp.NOISE_STD)
        self.assertLess(history["train"][-1], 1e-2 * history["train"][0])


class ParadigmTests(unittest.TestCase):
    def test_logistic_regression_recovers_boundary_direction(self):
        rng = np.random.default_rng(0)
        x = rng.uniform(-1, 1, (400, 2))
        labels = (x[:, 0] + 2.0 * x[:, 1] - 0.3 > 0).astype(float)
        flip = rng.random(400) < 0.05  # some label noise keeps the MLE finite
        labels[flip] = 1.0 - labels[flip]
        weights, bias = paradigms.fit_logistic_regression(x, labels)
        direction = np.append(weights, bias) / weights[0]
        np.testing.assert_allclose(direction, [1.0, 2.0, -0.3], atol=0.15)

    def test_kmeans_recovers_separated_regimes(self):
        rng = np.random.default_rng(5)
        points = paradigms.make_clustering_data(rng)
        labels, centroids, _ = paradigms.kmeans(points, 3, rng)
        truth = np.repeat(np.arange(3), paradigms.N_PER_REGIME)
        for regime in range(3):
            values, counts = np.unique(labels[truth == regime], return_counts=True)
            self.assertGreater(counts.max() / counts.sum(), 0.95)
        order = np.argsort(centroids[:, 0])
        np.testing.assert_allclose(
            centroids[order],
            paradigms.REGIME_CENTRES[np.argsort(paradigms.REGIME_CENTRES[:, 0])],
            atol=0.03,
        )

    def test_gp_interpolates_with_small_noise(self):
        x = np.linspace(0.0, 40.0, 9)
        y = paradigms.drag_coefficient(x)
        mean, half_width = paradigms.gp_regression(x, y, x, noise_std=1e-5)
        np.testing.assert_allclose(mean, y, atol=1e-6)
        self.assertTrue(np.all(half_width < 1e-3))


class BiasVarianceTests(unittest.TestCase):
    def test_decomposition_identity(self):
        rng = np.random.default_rng(3)
        x_test = np.linspace(0.1, 0.9, 50)
        bias2, variance, predictions = bias_variance.bias_variance(
            5, rng, n_datasets=50, x_test=x_test
        )
        mse = np.mean((predictions - bias_variance.true_function(x_test)) ** 2)
        self.assertAlmostEqual(mse, bias2 + variance, places=12)

    def test_ols_variance_at_design_points(self):
        # For least squares, mean_i Var[f_hat(x_i)] = sigma^2 (d + 1) / N.
        x = bias_variance.training_locations()
        rng = np.random.default_rng(4)
        degree = 4
        _, variance, _ = bias_variance.bias_variance(
            degree, rng, n_datasets=4000, x_test=x
        )
        expected = bias_variance.NOISE_STD**2 * (degree + 1) / x.size
        self.assertAlmostEqual(variance, expected, delta=0.05 * expected)

    def test_leave_one_out_matches_hat_matrix(self):
        rng = np.random.default_rng(6)
        x = bias_variance.training_locations()
        y = bias_variance.sample_data(x, rng)
        degree = 3
        loo = bias_variance.kfold_cv(x, y, degree, x.size, rng)
        design = np.polynomial.legendre.legvander(2 * x - 1, degree)
        hat = design @ np.linalg.pinv(design)
        residual = y - hat @ y
        expected = np.sqrt(np.mean((residual / (1.0 - np.diag(hat))) ** 2))
        self.assertAlmostEqual(loo, expected, places=10)

    def test_folds_partition_indices(self):
        folds = bias_variance.kfold_indices(23, 5, np.random.default_rng(0))
        np.testing.assert_array_equal(np.sort(np.concatenate(folds)), np.arange(23))
        self.assertEqual(sorted(len(f) for f in folds), [4, 4, 5, 5, 5])


if __name__ == "__main__":
    unittest.main()
