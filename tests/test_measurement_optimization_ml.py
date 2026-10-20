"""Check the PIV, super-resolution and Bayesian-optimization example scripts."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_algorithm(name):
    spec = importlib.util.spec_from_file_location(
        f"algorithm_{name}", ROOT / "scripts" / "algorithms" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


piv = load_algorithm("piv_cross_correlation")
sr = load_algorithm("flow_superresolution")
bo = load_algorithm("bayesian_optimization")


class PIVTests(unittest.TestCase):
    def test_gaussian_peak_fit_is_exact_for_a_gaussian(self):
        offset = 0.37
        values = np.exp(-((np.array([-1.0, 0.0, 1.0]) - offset) ** 2) / 1.3)
        self.assertAlmostEqual(piv.gaussian_subpixel(*values), offset, places=12)

    def test_uniform_shift_is_recovered_to_a_tenth_of_a_pixel(self):
        shift = (2.3, -1.7)  # [px]
        rng = np.random.default_rng(5)
        frame1, frame2 = piv.make_image_pair(
            lambda x, y: (shift[0] + 0 * x, shift[1] + 0 * y), rng
        )
        dx, dy = piv.run_piv(frame1, frame2)["final"]
        error = np.hypot(dx - shift[0], dy - shift[1])
        self.assertLess(abs(dx.mean() - shift[0]), 0.05)
        self.assertLess(abs(dy.mean() - shift[1]), 0.05)
        self.assertLess(error[1:-1, 1:-1].max(), 0.1)

    def test_normalized_median_test_flags_injected_outliers(self):
        y, x = np.mgrid[0:20, 0:20].astype(float)
        dx, dy = 0.2 * y - 1.0, 0.1 * x + 0.5  # smooth shear field [px]
        rng = np.random.default_rng(2)
        dx = dx + 0.03 * rng.standard_normal(dx.shape)
        dy = dy + 0.03 * rng.standard_normal(dy.shape)
        nodes = [(3, 4), (8, 15), (12, 9), (16, 2), (10, 10)]
        for r, c in nodes:
            dx[r, c] += rng.choice([-1, 1]) * rng.uniform(3, 8)
            dy[r, c] += rng.uniform(-8, 8)
        flagged = piv.normalized_median_test(dx, dy)
        for node in nodes:
            self.assertTrue(flagged[node], node)
        self.assertLessEqual(flagged.sum() - len(nodes), 2)
        fixed_dx, _ = piv.replace_outliers(dx, dy, flagged)
        for r, c in nodes:
            self.assertLess(abs(fixed_dx[r, c] - (0.2 * r - 1.0)), 0.2)

    def test_example_flags_every_decorrelated_window(self):
        frame1, frame2, true, bad_nodes, _ = piv.make_case()
        result = piv.run_piv(frame1, frame2)
        for node in bad_nodes:
            self.assertTrue(result["flagged"][node], node)
        self.assertLess(piv.rms_error(result["final"], true), 0.15)


class SuperResolutionTests(unittest.TestCase):
    def test_velocity_field_is_divergence_free(self):
        u, v = sr.random_velocity_field(np.random.default_rng(0), n=64)
        k = sr.wavenumbers(64)
        kx, ky = np.meshgrid(k, k)
        div = np.fft.ifft2(1j * kx * np.fft.fft2(u) + 1j * ky * np.fft.fft2(v))
        self.assertLess(np.abs(div).max(), 1e-10)

    def test_block_average_preserves_the_mean_and_bicubic_is_consistent(self):
        field = np.random.default_rng(1).standard_normal((32, 32))
        coarse = sr.block_average(field)
        self.assertAlmostEqual(coarse.mean(), field.mean())
        self.assertEqual(sr.bicubic_upsample(coarse).shape, field.shape)
        rows = sr.block_targets(field)
        np.testing.assert_array_equal(sr.assemble_blocks(rows, field.shape), field)

    def test_ridge_patch_model_beats_bicubic_on_held_out_field(self):
        case = sr.super_resolution_case()
        err_bicubic = sr.relative_l2(case["bicubic"], case["truth"])
        err_ridge = sr.relative_l2(case["ridge"], case["truth"])
        self.assertLess(err_ridge, 0.95 * err_bicubic)
        # Neither can recover what lies beyond the input Nyquist wavenumber.
        self.assertGreater(
            err_ridge, 0.98 * sr.relative_l2(case["lowpass"], case["truth"])
        )

    def test_pod_truncation_denoises(self):
        case = sr.cleansing_case()
        self.assertLess(case["errors"].min(), 0.4 * case["noisy_error"])
        self.assertLess(case["errors"][case["rank_gd"]], 1.1 * case["errors"].min())


class BayesianOptimizationTests(unittest.TestCase):
    def test_expected_improvement_matches_monte_carlo(self):
        rng = np.random.default_rng(0)
        for mean, std, f_best in ((0.300, 0.002, 0.302), (0.305, 0.010, 0.302)):
            samples = rng.normal(mean, std, 2_000_000)
            mc = np.mean(np.maximum(f_best - samples, 0.0))
            exact = bo.expected_improvement(np.array(mean), np.array(std), f_best)
            self.assertAlmostEqual(float(exact), mc, delta=3e-3 * mc + 1e-7)

    def test_gp_interpolates_and_likelihood_gradient_is_correct(self):
        rng = np.random.default_rng(3)
        x = rng.uniform(size=(10, 2))
        y = bo.branin_2d(x)
        gp = bo.GaussianProcess([0.3, 0.4], 1.2).fit(x, y)
        mean, std = gp.predict(x)
        np.testing.assert_allclose(mean, y, rtol=1e-3, atol=1e-3)
        self.assertLess(std.max(), 1e-2 * y.std())
        theta = np.log([0.3, 0.4, 1.2])
        step = 1e-6
        numeric = []
        for j in range(3):
            plus, minus = theta.copy(), theta.copy()
            plus[j] += step
            minus[j] -= step
            lp = bo.GaussianProcess(np.exp(plus[:2]), np.exp(plus[2])).fit(x, y)
            lm = bo.GaussianProcess(np.exp(minus[:2]), np.exp(minus[2])).fit(x, y)
            numeric.append(
                (lp.log_marginal_likelihood() - lm.log_marginal_likelihood())
                / (2 * step)
            )
        np.testing.assert_allclose(
            gp.log_marginal_likelihood_gradient(), numeric, rtol=1e-4, atol=1e-6
        )

    def test_bo_finds_the_global_minimum_of_the_1d_function(self):
        x, y, _ = bo.bayesian_optimization(
            bo.drag_like_1d, 1, 3, 15, np.random.default_rng(bo.SEED)
        )
        best = np.argmin(y)
        self.assertLess(abs(x[best, 0] - 0.75725), 0.01)
        self.assertLess(y[best] - bo.DRAG_1D_MIN, 1e-4)


if __name__ == "__main__":
    unittest.main()
