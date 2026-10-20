"""Automotive dataset scripts: GCI order recovery, sampling designs, surrogate fits."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_script(category, name):
    spec = importlib.util.spec_from_file_location(
        f"{category}_{name}", ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gci = load_script("algorithms", "grid_convergence_index")
sampling = load_script("plots", "sampling_strategies_comparison")
cross = load_script("plots", "cross_design_generalization")
design = load_script("plots", "design_space_distribution")


class GridConvergenceIndexTests(unittest.TestCase):
    def manufactured(self, h, p, exact=0.32, c=0.05):
        """phi(h) = exact + c h^p: Richardson extrapolation is exact for this."""
        return [exact + c * hk**p for hk in h]

    def test_constant_ratio_recovers_order_and_limit(self):
        h = [0.01, 0.02, 0.04]
        for p_true in (1.0, 1.7, 2.0, 3.0):
            with self.subTest(p=p_true):
                res = gci.gci_study(self.manufactured(h, p_true), h)
                self.assertAlmostEqual(res["p"], p_true, places=8)
                self.assertAlmostEqual(res["phi_ext"], 0.32, places=12)
                self.assertEqual(res["s"], 1.0)

    def test_unequal_ratios_recover_order(self):
        h = [0.010, 0.0137, 0.0191]  # r21 = 1.37, r32 = 1.39
        res = gci.gci_study(self.manufactured(h, 1.8), h)
        self.assertAlmostEqual(res["p"], 1.8, places=8)
        self.assertAlmostEqual(res["phi_ext"], 0.32, places=10)

    def test_gci_matches_closed_form(self):
        # Constant r = 2: p = ln(3.5)/ln 2 and GCI = 1.25 |e_a| / (r^p - 1).
        res = gci.gci_study([0.3170, 0.3210, 0.3350], [1.0, 2.0, 4.0])
        self.assertAlmostEqual(res["p"], np.log(3.5) / np.log(2.0), places=12)
        self.assertAlmostEqual(res["gci_fine"], 1.25 * (0.004 / 0.317) / 2.5, places=12)

    def test_oscillatory_convergence_is_flagged(self):
        _, s = gci.observed_order(1.00, 1.02, 0.99, 2.0, 2.0)
        self.assertEqual(s, -1.0)

    def test_model_problem_converges_at_second_order(self):
        exact = gci.exact_wall_gradient()
        n = (256, 512, 1024)
        phi = [gci.wall_gradient(k) for k in n[::-1]]
        res = gci.gci_study(phi, [1.0 / k for k in n[::-1]])
        self.assertGreater(res["p"], 1.9)
        self.assertLess(res["p"], 2.1)
        # The extrapolated value is closer to the exact one than the fine mesh.
        self.assertLess(abs(res["phi_ext"] - exact), abs(phi[0] - exact) / 10)
        # The GCI bounds the true error of the fine mesh.
        self.assertLess(abs(phi[0] - exact) / exact, res["gci_fine"])

    def test_discrete_solution_satisfies_boundary_conditions(self):
        x, u = gci.solve_advection_diffusion(64)
        self.assertEqual(u[0], 0.0)
        self.assertEqual(u[-1], 1.0)
        pe = gci.ADVECTION_SPEED / gci.DIFFUSIVITY
        exact = np.expm1(pe * x) / np.expm1(pe)
        self.assertLess(np.max(np.abs(u - exact)), 5e-3)


class SamplingTests(unittest.TestCase):
    def test_latin_hypercube_has_one_point_per_stratum(self):
        for n in (8, 32, 100):
            pts = sampling.sample("Latin hypercube", n, dimension=3, seed=4)
            np.testing.assert_array_equal(sampling.stratum_counts(pts, n), 1)

    def test_sobol_power_of_two_is_balanced(self):
        pts = sampling.sample("Scrambled Sobol", 64)
        np.testing.assert_array_equal(sampling.stratum_counts(pts, 64), 1)
        with self.assertRaises(ValueError):
            sampling.sample("Scrambled Sobol", 48)

    def test_discrepancy_ordering(self):
        n = 256
        cd = {
            m: np.mean(
                [
                    sampling.centred_l2_discrepancy(sampling.sample(m, n, seed=s))
                    for s in range(5)
                ]
            )
            for m in sampling.METHODS
        }
        self.assertLess(cd["Scrambled Sobol"], cd["Latin hypercube"])
        self.assertLess(cd["Latin hypercube"], cd["Random"])

    def test_random_discrepancy_decays_like_root_n(self):
        ns, disc = sampling.discrepancy_study(range(5, 10), n_seeds=10)
        slope = sampling.fitted_slope(ns, disc["Random"])
        self.assertAlmostEqual(slope, -0.5, delta=0.1)
        self.assertLess(sampling.fitted_slope(ns, disc["Scrambled Sobol"]), -0.8)

    def test_design_space_sobol_marginals_are_uniform(self):
        pts = design.generate_design()
        for k in range(pts.shape[1]):
            counts, _ = np.histogram(pts[:, k], bins=design.N_BINS, range=(0, 1))
            np.testing.assert_array_equal(counts, len(pts) // design.N_BINS)


class CrossDesignTests(unittest.TestCase):
    def test_ridge_interpolates_representable_function_without_noise(self):
        rng = np.random.default_rng(0)
        p = rng.random((80, 2))
        w = rng.normal(size=2 + cross.RBF_GRID**2)
        y = 0.3 + cross.rbf_features(p, 0.25) @ w * 1e-3
        model = cross.RidgeRBF(1e-12, 0.25).fit(p, y)
        np.testing.assert_allclose(model.predict(p), y, atol=1e-8)

    def test_cross_design_error_exceeds_in_distribution_error(self):
        data = cross.make_datasets()
        _, table = cross.train_models(data)
        m1, m2, m3 = (table[name] for name in cross.MODELS)
        self.assertGreater(m1["Y"], 3 * m1["X"])
        self.assertGreater(m2["X"], 3 * m2["Y"])
        # Training on both families removes most of the cross-design error.
        self.assertLess(m3["Y"], 0.5 * m1["Y"])
        self.assertLess(m3["X"], 0.5 * m2["X"])


if __name__ == "__main__":
    unittest.main()
