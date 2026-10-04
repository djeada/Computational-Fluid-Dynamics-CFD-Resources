"""Lorenz ensemble: RK4 order, fixed points, volume contraction and chaos."""

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


lorenz = load_example("lorenz_attractor")
ON_ATTRACTOR = lorenz.integrate(lorenz.START, 20.0)


class LorenzTests(unittest.TestCase):
    def test_rk4_global_error_is_fourth_order(self):
        duration = 1.0
        reference = lorenz.integrate(ON_ATTRACTOR, duration, dt=duration / 4000)
        errors = [
            np.linalg.norm(
                lorenz.integrate(ON_ATTRACTOR, duration, dt=duration / n) - reference
            )
            for n in (50, 100, 200)
        ]
        orders = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(orders, 4.0, atol=0.15)

    def test_fixed_points_are_stationary(self):
        origin, c_plus, c_minus = lorenz.fixed_points()
        a = np.sqrt(lorenz.BETA * (lorenz.RHO - 1))
        np.testing.assert_allclose(c_plus, [a, a, lorenz.RHO - 1])
        np.testing.assert_allclose(c_minus, [-a, -a, lorenz.RHO - 1])
        for point in (origin, c_plus, c_minus):
            np.testing.assert_allclose(lorenz.lorenz_rhs(point), 0.0, atol=1e-12)
            np.testing.assert_allclose(lorenz.integrate(point, 5.0), point, atol=1e-10)
        self.assertEqual(len(lorenz.fixed_points(rho=0.5)), 1)  # conduction only

    def test_phase_space_volume_contracts_at_the_divergence_rate(self):
        divergence = lorenz.divergence()
        self.assertAlmostEqual(divergence, -(10 + 1 + 8 / 3))
        # The trace of the Jacobian is the same at every point.
        rng = np.random.default_rng(4)
        eps = 1e-3
        for point in rng.uniform(-20, 40, (5, 3)):
            trace = sum(
                (
                    lorenz.lorenz_rhs(point + eps * e)[i]
                    - lorenz.lorenz_rhs(point - eps * e)[i]
                )
                / (2 * eps)
                for i, e in enumerate(np.eye(3))
            )
            self.assertAlmostEqual(trace, divergence, places=9)
        # A small tetrahedron of states shrinks like exp(divergence t).
        for duration in (0.2, 0.5):
            corners = ON_ATTRACTOR + np.vstack([np.zeros(3), 1e-6 * np.eye(3)])
            before = np.linalg.det(corners[1:] - corners[0])
            after_corners = lorenz.integrate(corners, duration)
            after = np.linalg.det(after_corners[1:] - after_corners[0])
            self.assertAlmostEqual(
                after / before / np.exp(divergence * duration), 1.0, places=3
            )

    def test_initial_states_lie_within_the_initial_length(self):
        simulation = lorenz.LorenzSimulation(ghost_time=1.0)
        points = simulation.points
        distances = np.linalg.norm(points[:, None] - points[None], axis=-1)
        self.assertAlmostEqual(distances.max() / lorenz.INITIAL_LENGTH, 1.0)
        n = len(points)
        expected = lorenz.INITIAL_LENGTH * np.sqrt((n + 1) / (12 * (n - 1)))
        self.assertAlmostEqual(simulation.spreads[0] / expected, 1.0)

    def test_early_spread_grows_at_the_lyapunov_rate(self):
        simulation = lorenz.LorenzSimulation(ghost_time=1.0)
        simulation.advance(1200)  # t = 12, before the cloud saturates
        times, spreads = np.array(simulation.times), np.array(simulation.spreads)
        self.assertEqual(len(times), 1201)
        self.assertLess(spreads.max(), 1.0)
        slope = np.polyfit(times, np.log(spreads), 1)[0]
        self.assertLess(abs(slope - lorenz.LYAPUNOV_EXPONENT), 0.2, slope)
        simulation.advance(1300)  # t = 25: spread over the whole attractor
        self.assertGreater(simulation.spreads[-1], 5.0)
        self.assertEqual(len(simulation.trail), lorenz.TRAIL_STEPS + 1)
        np.testing.assert_array_equal(simulation.trail[-1], simulation.points)

    def test_largest_lyapunov_exponent_by_renormalisation(self):
        # Benettin et al.: follow a neighbour 1e-8 away, rescale every 0.1 time.
        separation, interval, n_intervals = 1e-8, 10, 2000
        pair = np.array([ON_ATTRACTOR, ON_ATTRACTOR + [separation, 0.0, 0.0]])
        total = 0.0
        for _ in range(n_intervals):
            for _ in range(interval):
                pair = lorenz.rk4_step(pair)
            distance = np.linalg.norm(pair[1] - pair[0])
            total += np.log(distance / separation)
            pair[1] = pair[0] + (pair[1] - pair[0]) * separation / distance
        exponent = total / (n_intervals * interval * lorenz.TIME_STEP)
        self.assertAlmostEqual(exponent, lorenz.LYAPUNOV_EXPONENT, delta=0.05)


if __name__ == "__main__":
    unittest.main()
