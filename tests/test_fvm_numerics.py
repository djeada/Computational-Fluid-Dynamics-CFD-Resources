"""Finite-volume convection schemes: accuracy, conservation, boundedness and TVD."""

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


cd1d = load_example("algorithms", "fvm_convection_diffusion_1d")
tvd = load_example("algorithms", "tvd_limiters_advection")
stencil = load_example("plots", "control_volume_stencil")


def orders(module, n_values, velocity, scheme):
    errors = np.array([module.rms_error(n, velocity, scheme) for n in n_values])
    return module.observed_orders(np.array(n_values), errors)


class ConvectionDiffusionTests(unittest.TestCase):
    def test_reproduces_versteeg_malalasekera_tables(self):
        # Example 5.1 case (i) and (ii), Example 5.2 case (ii), N = 5.
        _, central_i, _ = cd1d.solve(5, 0.1, "central")
        np.testing.assert_allclose(
            central_i, [0.9421, 0.8006, 0.6276, 0.4163, 0.1579], atol=5e-5
        )
        _, central_ii, _ = cd1d.solve(5, 2.5, "central")
        np.testing.assert_allclose(
            central_ii, [1.0356, 0.8694, 1.2573, 0.3521, 2.4644], atol=5e-5
        )
        _, upwind_ii, _ = cd1d.solve(5, 2.5, "upwind")
        np.testing.assert_allclose(
            upwind_ii, [0.9998, 0.9987, 0.9921, 0.9524, 0.7143], atol=5e-5
        )

    def test_central_is_second_order_at_low_peclet(self):
        p = orders(cd1d, (10, 20, 40, 80, 160), 0.1, "central")
        np.testing.assert_allclose(p[-2:], 2.0, atol=0.05)
        x, phi, _ = cd1d.solve(160, 0.1, "central")
        self.assertLess(np.max(np.abs(phi - cd1d.exact_solution(x, 0.1))), 2e-5)

    def test_upwind_is_first_order(self):
        p = orders(cd1d, (160, 320, 640, 1280), 2.5, "upwind")
        np.testing.assert_allclose(p[-1], 1.0, atol=0.05)

    def test_quick_and_hybrid_reach_second_order(self):
        for scheme in ("QUICK", "hybrid"):
            p = orders(cd1d, (160, 320, 640), 2.5, scheme)
            np.testing.assert_allclose(p[-1], 2.0, atol=0.1)

    def test_central_wiggles_only_above_cell_peclet_two(self):
        for n, wiggles in ((5, True), (20, False)):  # Pe_cell = 5 and 1.25
            _, phi, _ = cd1d.solve(n, 2.5, "central")
            outside = np.any(phi > 1.0 + 1e-12) or np.any(phi < -1e-12)
            self.assertEqual(outside, wiggles)

    def test_bounded_schemes_stay_within_boundary_values(self):
        for scheme in ("upwind", "hybrid", "power law"):
            for n in (5, 10, 20):
                _, phi, _ = cd1d.solve(n, 2.5, scheme)
                self.assertTrue(np.all(phi <= 1.0 + 1e-12))
                self.assertTrue(np.all(phi >= -1e-12))
                # Monotone decreasing like the exact solution.
                self.assertTrue(np.all(np.diff(phi) <= 1e-12))

    def test_face_fluxes_telescope(self):
        # Steady, source-free: the same total flux crosses every face.
        for scheme in cd1d.SCHEMES:
            for velocity, n in ((0.1, 5), (2.5, 5), (2.5, 40)):
                _, phi, _ = cd1d.solve(n, velocity, scheme)
                j = cd1d.face_fluxes(n, velocity, scheme, phi)
                np.testing.assert_allclose(j, j[0], atol=1e-10)


class TvdAdvectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.phi0, cls.n_steps, cls.results = tvd.profile_test(n=100)

    def test_integral_is_conserved_to_round_off(self):
        for res in self.results.values():
            self.assertLess(res["mass_drift"], 1e-13)

    def test_tvd_schemes_never_increase_total_variation(self):
        for name in ("upwind", *tvd.TVD_LIMITERS):
            self.assertLessEqual(self.results[name]["max_tv_increase"], 1e-12)

    def test_lax_wendroff_increases_total_variation(self):
        tv = self.results["Lax-Wendroff"]["tv"]
        self.assertGreater(tv[-1], 1.1 * tv[0])

    def test_tvd_schemes_create_no_new_extrema(self):
        lo, hi = self.phi0.min(), self.phi0.max()
        for name in ("upwind", *tvd.TVD_LIMITERS):
            phi = self.results[name]["phi"]
            self.assertGreaterEqual(phi.min(), lo - 1e-12)
            self.assertLessEqual(phi.max(), hi + 1e-12)

    def test_orders_on_smooth_data(self):
        n_values, errors = tvd.convergence_test(n_values=(100, 200, 400))
        p = {k: tvd.observed_order(n_values, e) for k, e in errors.items()}
        self.assertAlmostEqual(p["upwind"], 1.0, delta=0.05)
        self.assertAlmostEqual(p["Lax-Wendroff"], 2.0, delta=0.05)
        for name in tvd.TVD_LIMITERS:
            self.assertGreater(p[name], 1.8)

    def test_limiters_satisfy_sweby_bounds(self):
        r = np.concatenate((np.linspace(-5.0, 0.0, 101), np.geomspace(1e-4, 1e4, 801)))
        for name in tvd.TVD_LIMITERS:
            psi = tvd.LIMITERS[name](r)
            neg = r <= 0
            np.testing.assert_array_equal(psi[neg], 0.0)
            pos = ~neg
            self.assertTrue(np.all(psi[pos] >= 0.0))
            self.assertTrue(np.all(psi[pos] <= np.minimum(2.0 * r[pos], 2.0) + 1e-12))
            # Second-order region: between minmod and superbee.
            lower = np.minimum(r[pos], 1.0)
            upper = np.maximum(np.minimum(2 * r[pos], 1.0), np.minimum(r[pos], 2.0))
            self.assertTrue(np.all(psi[pos] >= lower - 1e-12), name)
            self.assertTrue(np.all(psi[pos] <= upper + 1e-12), name)
            self.assertAlmostEqual(float(tvd.LIMITERS[name](np.array(1.0))), 1.0)
            # Symmetry psi(r)/r = psi(1/r): forward and backward profiles agree.
            np.testing.assert_allclose(
                psi[pos] / r[pos], tvd.LIMITERS[name](1.0 / r[pos]), rtol=1e-10
            )


class StencilGeometryTests(unittest.TestCase):
    def test_over_relaxed_decomposition(self):
        g = stencil.face_geometry()
        s, d, delta, k = g["s_f"], g["d"], g["delta"], g["k"]
        np.testing.assert_allclose(delta + k, s)
        self.assertAlmostEqual(abs(d[0] * delta[1] - d[1] * delta[0]), 0.0)
        self.assertAlmostEqual(np.dot(delta, s), np.dot(s, s))
        self.assertAlmostEqual(np.dot(k, s), 0.0)
        # f' lies on both the face and the line P -> N.
        a, b = np.array(stencil.FACE_A), np.array(stencil.FACE_B)
        t = b - a
        rel = g["x_fp"] - a
        self.assertAlmostEqual(t[0] * rel[1] - t[1] * rel[0], 0.0)

    def test_polygon_centroid_of_unit_square(self):
        c, area = stencil.polygon_centroid(((0, 0), (1, 0), (1, 1), (0, 1)))
        np.testing.assert_allclose(c, [0.5, 0.5])
        self.assertAlmostEqual(area, 1.0)


if __name__ == "__main__":
    unittest.main()
