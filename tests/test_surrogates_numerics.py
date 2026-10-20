"""Surrogate models: kriging, hierarchical kriging, RBF LOOCV and LHS designs."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_script(category, name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hk = load_script("algorithms", "hierarchical_kriging_multifidelity")
ok1d = load_script("algorithms", "kriging_interpolation")
adaptive = load_script("algorithms", "adaptive_sampling_kriging")
rbf = load_script("algorithms", "radial_basis_functions")
shape = load_script("plots", "rbf_shape_parameter_tradeoff")


class KrigingInterpolationTests(unittest.TestCase):
    def test_kriging_without_nugget_interpolates_data(self):
        x = np.linspace(0.0, 1.0, 7)
        y = hk.f_high(x)
        model = hk.Kriging(x, y, theta=20.0, nugget=0.0)
        np.testing.assert_allclose(model.predict(x), y, atol=1e-9)

    def test_mse_is_zero_at_samples_and_positive_between(self):
        x = np.linspace(0.0, 1.0, 6)
        model = hk.Kriging(x, hk.f_high(x), theta=20.0, nugget=0.0)
        _, mse_samples = model.predict(x, return_mse=True)
        _, mse_mid = model.predict(0.5 * (x[1:] + x[:-1]), return_mse=True)
        self.assertLess(np.max(mse_samples), 1e-9 * model.sigma2)
        self.assertTrue(np.all(mse_mid > 1e-3 * model.sigma2))

    def test_2d_ordinary_kriging_interpolates_and_has_zero_mse(self):
        rng = np.random.default_rng(4)
        x = adaptive.latin_hypercube(12, 2, rng)
        y = adaptive.test_function(x)
        model = adaptive.OrdinaryKriging(x, y, theta=np.array([5.0, 8.0]))
        y_hat, mse = model.predict(x, return_mse=True)
        np.testing.assert_allclose(y_hat, y, atol=1e-5)
        self.assertLess(np.max(mse), 1e-6 * model.sigma2)

    def test_cubic_correlation_is_continuous_and_compact(self):
        theta = 2.5
        for xi, value in ((0.5, 0.25), (1.0, 0.0)):
            h = xi / theta
            left = ok1d.cubic_correlation(h - 1e-9, theta)
            right = ok1d.cubic_correlation(h + 1e-9, theta)
            self.assertAlmostEqual(float(left), value, places=6)
            self.assertAlmostEqual(float(right), value, places=6)
        self.assertEqual(float(ok1d.cubic_correlation(0.5, theta)), 0.0)

    def test_worked_example_mle_and_interpolation(self):
        x = np.linspace(0.0, 1.0, ok1d.N_SAMPLES)
        y = ok1d.test_function(x)
        _, _, best = ok1d.maximum_likelihood_theta(x, y)
        self.assertAlmostEqual(best, 2.03, delta=0.01)
        model = ok1d.fit(x, y, best)
        y_hat, mse = ok1d.predict(x, x, model)
        np.testing.assert_allclose(y_hat, y, atol=1e-10)
        self.assertLess(np.max(mse), 1e-10 * model["sigma2"])

    def test_ordinary_kriging_closed_form_loo_matches_refitting(self):
        x = np.linspace(0.0, 1.0, ok1d.N_SAMPLES)
        y = ok1d.test_function(x)
        theta = 2.5
        n = len(x)
        corr = ok1d.cubic_correlation(x[:, None] - x[None, :], theta)
        bordered = np.block([[corr, np.ones((n, 1))], [np.ones((1, n)), 0.0]])
        inv = np.linalg.inv(bordered)
        closed = (inv @ np.append(y, 0.0))[:n] / np.diag(inv)[:n]
        brute = []
        for i in range(n):
            keep = np.arange(n) != i
            model = ok1d.fit(x[keep], y[keep], theta)
            y_hat, _ = ok1d.predict(x[i : i + 1], x[keep], model)
            brute.append(y[i] - y_hat[0])
        np.testing.assert_allclose(closed, brute, atol=1e-9)


class HierarchicalKrigingTests(unittest.TestCase):
    def test_hk_beats_hf_only_kriging_on_forrester_case(self):
        x_lf = np.linspace(0.0, 1.0, hk.N_LF)
        x_test = np.linspace(0.0, 1.0, 401)
        hf_only, _, model = hk.fit_models(x_lf, hk.X_HF_CLASSIC)
        self.assertLess(hk.rmse(model, x_test), 0.1 * hk.rmse(hf_only, x_test))
        self.assertAlmostEqual(model.beta, 1.0 / hk.A, delta=0.05)
        np.testing.assert_allclose(
            model.predict(hk.X_HF_CLASSIC), hk.f_high(hk.X_HF_CLASSIC), atol=1e-6
        )

    def test_hk_beats_hf_only_kriging_on_random_designs(self):
        rng = np.random.default_rng(7)
        x_lf = np.linspace(0.0, 1.0, hk.N_LF)
        x_test = np.linspace(0.0, 1.0, 401)
        lf_model = hk.Kriging(x_lf, hk.f_low(x_lf))
        for n_hf in (5, 8):
            x_hf = hk.latin_hypercube_1d(n_hf, rng)
            plain = hk.Kriging(x_hf, hk.f_high(x_hf))
            multi = hk.Kriging(x_hf, hk.f_high(x_hf), trend=lf_model.predict)
            self.assertLess(hk.rmse(multi, x_test), hk.rmse(plain, x_test))

    def test_scaled_low_fidelity_data_are_reproduced_exactly(self):
        x = np.linspace(0.0, 1.0, 5)
        model = hk.Kriging(
            x,
            3.0 * np.sin(4.0 * x),
            trend=lambda s: np.sin(4.0 * s),
            theta=10.0,
            nugget=0.0,
        )
        self.assertAlmostEqual(model.beta, 3.0, places=10)
        x_new = np.linspace(0.0, 1.0, 37)
        np.testing.assert_allclose(
            model.predict(x_new), 3.0 * np.sin(4.0 * x_new), atol=1e-10
        )


class RadialBasisFunctionTests(unittest.TestCase):
    def test_rippa_loocv_equals_brute_force(self):
        centres, values, *_ = shape.make_data()
        r = shape.distance_matrix(centres, centres)
        for kernel in shape.KERNELS.values():
            for eps in (3.0, 8.0):
                a = kernel(r, eps)
                np.testing.assert_allclose(
                    shape.rippa_loocv(a, values),
                    shape.brute_force_loocv(a, values),
                    rtol=1e-6,
                    atol=1e-10,
                )

    def test_interpolants_pass_through_data(self):
        x = np.linspace(0.0, 1.0, rbf.N_SAMPLES)
        y = rbf.test_function(x)
        results = rbf.interpolate_all(x, y, x)
        for s in results.values():
            np.testing.assert_allclose(s, y, atol=1e-8)

    def test_polynomial_tail_reproduces_linear_data(self):
        x = np.linspace(0.0, 1.0, 6)
        y = 2.0 * x
        phi = rbf.KERNELS["cubic + linear"][0]
        w, c = rbf.fit_rbf(x, y, phi, degree=1)
        np.testing.assert_allclose(w, 0.0, atol=1e-10)
        np.testing.assert_allclose(c, [0.0, 2.0], atol=1e-10)
        w0, c0 = rbf.fit_rbf(x, y, phi, degree=-1)
        s0 = rbf.evaluate_rbf(np.array([0.1]), x, w0, c0, phi, degree=-1)
        self.assertAlmostEqual(float(s0[0]), 0.2421, places=4)

    def test_condition_number_grows_as_kernel_flattens(self):
        centres, *_ = shape.make_data()
        r = shape.distance_matrix(centres, centres)
        gauss = shape.KERNELS["Gaussian"]
        conds = [np.linalg.cond(gauss(r, eps)) for eps in (20.0, 5.0, 2.0)]
        self.assertTrue(conds[0] < conds[1] < conds[2])


class SamplingTests(unittest.TestCase):
    def test_latin_hypercube_is_stratified_in_every_coordinate(self):
        rng = np.random.default_rng(0)
        for n, d in ((10, 3), (25, 2)):
            x = adaptive.latin_hypercube(n, d, rng)
            self.assertTrue(np.all((x >= 0.0) & (x < 1.0)))
            for k in range(d):
                np.testing.assert_array_equal(
                    np.sort(np.floor(x[:, k] * n)), np.arange(n)
                )
        x1 = hk.latin_hypercube_1d(9, rng)
        np.testing.assert_array_equal(np.floor(x1 * 9), np.arange(9))

    def test_maximin_lhs_improves_minimum_distance(self):
        rng = np.random.default_rng(1)
        plain = np.mean(
            [
                adaptive.min_distance(adaptive.latin_hypercube(20, 2, rng))
                for _ in range(20)
            ]
        )
        best = adaptive.min_distance(adaptive.maximin_lhs(20, 2, rng))
        self.assertGreater(best, plain)

    def test_max_mse_picks_the_midpoint_between_two_samples(self):
        x = np.array([[0.0, 0.5], [1.0, 0.5]])
        model = adaptive.OrdinaryKriging(
            x, np.array([1.0, 3.0]), theta=np.array([2.0, 2.0])
        )
        line = np.column_stack([np.linspace(0, 1, 101), np.full(101, 0.5)])
        _, mse = model.predict(line, return_mse=True)
        self.assertAlmostEqual(line[np.argmax(mse), 0], 0.5, places=6)
        self.assertAlmostEqual(mse.max() / model.sigma2, 0.3546, places=3)


if __name__ == "__main__":
    unittest.main()
