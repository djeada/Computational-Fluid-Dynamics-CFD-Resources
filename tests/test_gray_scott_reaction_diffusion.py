"""Gray-Scott solver: steady states, discrete Laplacian, stability and growth."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / "simulations" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gray_scott = load_example("gray_scott_reaction_diffusion")


def fourier_mode(n, mode_x, mode_y):
    i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    return np.cos(2 * np.pi * (mode_y * i + mode_x * j) / n)


class GrayScottTests(unittest.TestCase):
    def test_unreacted_state_is_an_exact_steady_state(self):
        for pattern in gray_scott.PATTERNS:
            simulation = gray_scott.GrayScottSimulation(n=24, pattern=pattern)
            simulation.u = np.ones((24, 24))
            simulation.v = np.zeros((24, 24))
            simulation.advance(200)
            np.testing.assert_array_equal(simulation.u, 1.0)
            np.testing.assert_array_equal(simulation.v, 0.0)

    def test_periodic_laplacian_sums_to_zero(self):
        rng = np.random.default_rng(1)
        field = rng.uniform(0.0, 1.0, (32, 24))
        lap = gray_scott.laplacian(field)
        self.assertLess(abs(lap.sum()), 1e-12 * np.abs(lap).sum())

    def test_laplacian_eigenvalue_of_fourier_modes(self):
        n, h = 32, gray_scott.GRID_SPACING
        for mode_x, mode_y in ((1, 0), (3, 5), (16, 16), (7, 16)):
            with self.subTest(mode=(mode_x, mode_y)):
                mode = fourier_mode(n, mode_x, mode_y)
                expected = gray_scott.laplacian_eigenvalue(mode_x, mode_y, n, h)
                np.testing.assert_allclose(
                    gray_scott.laplacian(mode, h),
                    expected * mode,
                    atol=1e-9 * abs(expected),
                )
        # The checkerboard is the most negative eigenvalue, -8 / h^2.
        self.assertAlmostEqual(
            gray_scott.laplacian_eigenvalue(16, 16, n, h) * h**2 / -8, 1.0
        )

    def test_pure_diffusion_conserves_mass(self):
        simulation = gray_scott.GrayScottSimulation(n=32)
        simulation.feed = simulation.kill = 0.0  # no feed, no removal
        simulation.v = np.zeros((32, 32))  # no reaction either: u_t = D_u lap(u)
        simulation.u = np.random.default_rng(2).uniform(0.0, 1.0, (32, 32))
        mass = simulation.u.sum()
        variance = simulation.u.var()
        simulation.advance(500)
        self.assertAlmostEqual(simulation.u.sum() / mass, 1.0, places=12)
        self.assertLess(simulation.u.var(), 0.01 * variance)

    def test_small_mode_decays_at_the_discrete_rate(self):
        # Near (1, 0) with v = 0 the U equation is linear: u_t = D_u lap(u) - F (u - 1).
        n, steps, amplitude = 32, 40, 1e-3
        simulation = gray_scott.GrayScottSimulation(n=n)
        mode = fourier_mode(n, 3, 2)
        simulation.u = 1.0 + amplitude * mode
        simulation.v = np.zeros((n, n))
        simulation.advance(steps)
        rate = (
            gray_scott.DIFFUSIVITY_U * gray_scott.laplacian_eigenvalue(3, 2, n)
            - simulation.feed
        )
        factor = (1.0 + gray_scott.TIME_STEP * rate) ** steps
        np.testing.assert_allclose(
            simulation.u - 1.0, amplitude * factor * mode, atol=1e-13
        )
        np.testing.assert_array_equal(simulation.v, 0.0)

    def test_time_step_respects_the_stability_limit(self):
        h, n = gray_scott.GRID_SPACING, 16
        checkerboard = fourier_mode(n, n // 2, n // 2)
        for pattern, (feed, kill) in gray_scott.PATTERNS.items():
            with self.subTest(pattern):
                limit = gray_scott.stability_limit(feed, kill)
                self.assertLess(gray_scott.TIME_STEP, limit)
                self.assertLessEqual(
                    gray_scott.TIME_STEP * gray_scott.DIFFUSIVITY_U / h**2, 0.25
                )
                # Just above the limit the checkerboard grows, at dt it decays.
                for dt, grows in ((gray_scott.TIME_STEP, False), (1.02 * limit, True)):
                    u, v = 1.0 + 1e-6 * checkerboard, np.zeros((n, n))
                    for _ in range(200):
                        u, v = gray_scott.euler_step(u, v, feed, kill, dt=dt)
                    self.assertEqual(np.abs(u - 1.0).max() > 1e-6, grows)

    def test_nontrivial_homogeneous_states_balance_the_reactions(self):
        self.assertEqual(gray_scott.homogeneous_states(0.0367, 0.0649), [(1.0, 0.0)])
        for feed, kill in ((0.0545, 0.062), (0.06, 0.05), (0.04, 0.03)):
            states = gray_scott.homogeneous_states(feed, kill)
            self.assertEqual(len(states), 3)
            for u, v in states:
                reaction_u, reaction_v = gray_scott.reaction(u, v, feed, kill)
                self.assertAlmostEqual(reaction_u, 0.0, places=14)
                self.assertAlmostEqual(reaction_v, 0.0, places=14)
                self.assertTrue(0.0 <= u <= 1.0 and 0.0 <= v <= 1.0)

    def test_seed_grows_into_a_bounded_reproducible_pattern(self):
        runs = []
        for _ in range(2):
            simulation = gray_scott.GrayScottSimulation(n=64, seed=3)
            start = simulation.covered_fraction
            simulation.advance(3000)
            runs.append(simulation.v.copy())
            self.assertGreater(simulation.covered_fraction, 2 * start)
            self.assertTrue(np.all((simulation.u >= 0) & (simulation.u <= 1)))
            self.assertTrue(np.all((simulation.v >= 0) & (simulation.v < 0.5)))
        np.testing.assert_array_equal(runs[0], runs[1])


if __name__ == "__main__":
    unittest.main()
