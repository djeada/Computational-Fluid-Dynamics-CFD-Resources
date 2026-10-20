"""Check the Sod shock-tube simulation against the exact Riemann solution.

The exact solver must reproduce Toro's tabulated star states, both schemes must
conserve mass and energy and change momentum only by the boundary pressure
force, the second-order scheme must be more accurate than the first-order one
and both must converge under refinement, and a fixed time step that would
violate the CFL limit must be split into stable sub-steps.
"""

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


sod = load_example("simulations", "sod_shock_tube")

# Toro (2009), Table 4.1 / 4.2: left state, right state, p*, u*, rho*_L, rho*_R.
TORO_TESTS = [
    ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 0.30313, 0.92745, 0.42632, 0.26557),
    ((1.0, -2.0, 0.4), (1.0, 2.0, 0.4), 0.00189, 0.0, 0.02185, 0.02185),
    ((1.0, 0.0, 1000.0), (1.0, 0.0, 0.01), 460.894, 19.5975, 0.57506, 5.99924),
    ((1.0, 0.0, 0.01), (1.0, 0.0, 100.0), 46.0950, -6.19633, 5.99242, 0.57511),
    (
        (5.99924, 19.5975, 460.894),
        (5.99242, -6.19633, 46.0950),
        1691.64,
        8.68975,
        14.2823,
        31.0426,
    ),
]


def totals(simulation, scheme):
    return simulation.states[scheme].sum(axis=1) * simulation.dx


class ExactSolverTests(unittest.TestCase):
    def test_star_states_match_toro_tables(self):
        for left, right, p_star, u_star, rho_left, rho_right in TORO_TESTS:
            with self.subTest(left=left, right=right):
                p, u = sod.star_state(left, right)
                # The tables give five significant figures (three for test 2).
                self.assertAlmostEqual(p, p_star, delta=5e-4 * p_star + 5e-6)
                self.assertAlmostEqual(u, u_star, delta=5e-4 * max(1.0, abs(u_star)))
                # Densities just left and right of the contact.
                eps = 1e-9
                rho = sod.exact_solution(
                    np.array([u - eps, u + eps]), 1.0, left, right, x0=0.0
                )[0]
                self.assertAlmostEqual(rho[0] / rho_left, 1.0, delta=5e-4)
                self.assertAlmostEqual(rho[1] / rho_right, 1.0, delta=5e-4)

    def test_sod_solution_has_the_expected_waves(self):
        x = np.linspace(0.0, 1.0, 2001)
        rho, u, p = sod.exact_solution(x, 0.2)
        # Undisturbed states ahead of the rarefaction and the shock.
        self.assertEqual(rho[0], 1.0)
        self.assertEqual(p[-1], 0.1)
        # Shock speed from the Rankine-Hugoniot relations: 1.75216.
        shock = x[np.nonzero(p > 0.2)[0].max()]
        self.assertAlmostEqual(shock, 0.5 + 1.75216 * 0.2, delta=1e-3)
        # The rarefaction is isentropic: p / rho^gamma stays at its left value.
        fan = (x > 0.27) & (x < 0.48)
        np.testing.assert_allclose(p[fan] / rho[fan] ** sod.GAMMA, 1.0, rtol=1e-12)
        # The velocity is continuous across the contact and equals u*.
        self.assertAlmostEqual(u[np.argmin(np.abs(x - 0.6))], 0.92745, places=5)

    def test_vacuum_is_rejected(self):
        with self.assertRaises(ValueError):
            sod.star_state((1.0, -10.0, 0.4), (1.0, 10.0, 0.4))


class SchemeTests(unittest.TestCase):
    def test_hllc_is_consistent(self):
        U = sod.conservative(
            np.array([0.7, 1.3]), np.array([-0.4, 2.0]), np.array([0.5, 3.0])
        )
        np.testing.assert_allclose(
            sod.hllc_flux(U, U), sod.physical_flux(U), atol=1e-13
        )

    def test_conservation_before_waves_reach_the_ends(self):
        simulation = sod.SodSimulation(n_cells=100)
        before = {s: totals(simulation, s) for s in sod.SCHEMES}
        simulation.advance(150)  # t = 0.15: shock at x = 0.76, fan head at 0.32
        t = simulation.time
        for scheme in sod.SCHEMES:
            with self.subTest(scheme=scheme):
                after = totals(simulation, scheme)
                self.assertAlmostEqual(after[0], before[scheme][0], places=13)
                self.assertAlmostEqual(after[2], before[scheme][2], places=12)
                # Momentum grows by the net pressure force (p_L - p_R) t.
                expected = before[scheme][1] + (sod.LEFT[2] - sod.RIGHT[2]) * t
                self.assertAlmostEqual(after[1], expected, places=12)

    def test_second_order_is_more_accurate_and_both_converge(self):
        errors = {}
        for n in (100, 200, 400):
            simulation = sod.SodSimulation(n_cells=n, dt=0.2 * 0.5 / n)
            simulation.advance(round(0.2 / simulation.dt))
            self.assertAlmostEqual(simulation.time, 0.2, places=12)
            errors[n] = simulation.l1_errors()
            for scheme in sod.SCHEMES:
                rho, _, p, _ = simulation.fields(scheme)
                self.assertGreater(rho.min(), 0.0)
                self.assertGreater(p.min(), 0.0)
        for n in (100, 200, 400):
            self.assertLess(errors[n]["muscl"], 0.5 * errors[n]["godunov"])
        for scheme in sod.SCHEMES:
            ratio = errors[100][scheme] / errors[400][scheme]
            # Discontinuities limit both schemes to less than first order in L1.
            self.assertGreater(ratio, 2.0, scheme)
        self.assertLess(errors[400]["muscl"], 2e-3)

    def test_cfl_violating_step_is_split(self):
        simulation = sod.SodSimulation(n_cells=1000, dt=1e-3)  # CFL about 2.2
        simulation.advance(5)
        self.assertLessEqual(simulation.cfl, sod.MAX_CFL + 1e-12)
        self.assertTrue(np.all(np.isfinite(simulation.states["muscl"])))

    def test_initial_state_and_status(self):
        simulation = sod.SodSimulation(n_cells=40)
        rho, u, p, e = simulation.fields("godunov")
        np.testing.assert_array_equal(rho[:20], 1.0)
        np.testing.assert_array_equal(p[20:], 0.1)
        np.testing.assert_array_equal(u, 0.0)
        np.testing.assert_allclose(e[:20], 2.5)
        self.assertEqual(simulation.l1_errors(), {"godunov": 0.0, "muscl": 0.0})
        figure = sod.ANIMATION.offscreen_figure((8, 6))
        view = sod.SodView(simulation, figure)
        view.draw()
        self.assertIn("t = 0.000", view.status())
        self.assertEqual(simulation.steps, 0)


if __name__ == "__main__":
    unittest.main()
