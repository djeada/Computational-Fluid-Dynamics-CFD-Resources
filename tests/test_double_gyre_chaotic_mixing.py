"""Double gyre: incompressibility, impermeable walls, RK4 order, area preservation."""

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


gyre = load_example("double_gyre_chaotic_mixing")


class DoubleGyreTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(1)
        self.x = rng.uniform(0.0, gyre.WIDTH, 200)
        self.y = rng.uniform(0.0, gyre.HEIGHT, 200)
        self.t = rng.uniform(0.0, 2 * gyre.PERIOD, 200)

    def test_velocity_is_divergence_free(self):
        h = 1e-5
        u_right, _ = gyre.velocity(self.x + h, self.y, self.t)
        u_left, _ = gyre.velocity(self.x - h, self.y, self.t)
        _, v_up = gyre.velocity(self.x, self.y + h, self.t)
        _, v_down = gyre.velocity(self.x, self.y - h, self.t)
        divergence = (u_right - u_left + v_up - v_down) / (2 * h)
        scale = np.pi**2 * gyre.AMPLITUDE  # size of each velocity gradient
        self.assertLess(np.abs(divergence).max(), 1e-8 * scale)

    def test_velocity_matches_stream_function(self):
        def psi(x, y, t):
            a = gyre.EPSILON * np.sin(gyre.OMEGA * t)
            f = a * x**2 + (1 - 2 * a) * x
            return gyre.AMPLITUDE * np.sin(np.pi * f) * np.sin(np.pi * y)

        x, y, t, h = self.x, self.y, self.t, 1e-5
        u, v = gyre.velocity(x, y, t)
        dpsi_dy = (psi(x, y + h, t) - psi(x, y - h, t)) / (2 * h)
        dpsi_dx = (psi(x + h, y, t) - psi(x - h, y, t)) / (2 * h)
        np.testing.assert_allclose(u, -dpsi_dy, atol=1e-9)
        np.testing.assert_allclose(v, dpsi_dx, atol=1e-9)

    def test_walls_are_impermeable(self):
        zeros, ones = np.zeros_like(self.x), np.ones_like(self.x)
        u_left, _ = gyre.velocity(zeros, self.y, self.t)
        u_right, _ = gyre.velocity(gyre.WIDTH * ones, self.y, self.t)
        _, v_bottom = gyre.velocity(self.x, zeros, self.t)
        _, v_top = gyre.velocity(self.x, gyre.HEIGHT * ones, self.t)
        for normal in (u_left, u_right, v_bottom, v_top):
            self.assertLess(np.abs(normal).max(), 1e-15)
        # The tangential velocity along the walls is not zero.
        _, v_left = gyre.velocity(zeros, self.y, self.t)
        self.assertGreater(np.abs(v_left).max(), 0.1)

    def test_rk4_converges_at_fourth_order(self):
        x0, y0 = self.x[:50], self.y[:50]
        reference = gyre.flow_map(x0, y0, 1.0, 5.0, max_step=1 / 1024)
        errors = []
        for step in (0.2, 0.1, 0.05):
            x_end, y_end = gyre.flow_map(x0, y0, 1.0, 5.0, max_step=step)
            errors.append(np.hypot(x_end - reference[0], y_end - reference[1]).max())
        orders = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(orders, 4.0, atol=0.25)

    def test_flow_map_preserves_area(self):
        # Jacobian determinant of the one-period flow map by central differences.
        x, y = np.meshgrid(np.linspace(0.1, 1.9, 19), np.linspace(0.1, 0.9, 9))
        h = 1e-7  # the map stretches by up to 1000, so differences need a small h
        maps = {
            offset: gyre.flow_map(x + offset[0], y + offset[1], 0.0, gyre.PERIOD, 0.01)
            for offset in ((h, 0), (-h, 0), (0, h), (0, -h))
        }
        dx = [(a - b) / (2 * h) for a, b in zip(maps[(h, 0)], maps[(-h, 0)])]
        dy = [(a - b) / (2 * h) for a, b in zip(maps[(0, h)], maps[(0, -h)])]
        determinant = dx[0] * dy[1] - dy[0] * dx[1]
        np.testing.assert_allclose(determinant, 1.0, atol=1e-4)
        self.assertGreater(np.abs(dx[0]).max(), 100)  # yet it stretches strongly

    def test_tracers_stay_in_the_box_and_mix(self):
        simulation = gyre.DoubleGyreSimulation(
            tracers=(200, 100), image_shape=(20, 40), ftle_shape=(8, 16)
        )
        self.assertEqual(simulation.mixed_fraction(), 0.0)
        np.testing.assert_array_equal(simulation.dye()[:, :20], 0.0)
        np.testing.assert_array_equal(simulation.dye()[:, 20:], 1.0)
        simulation.advance(round(2 * gyre.PERIOD / simulation.dt))
        self.assertTrue(np.all((simulation.x >= 0) & (simulation.x <= gyre.WIDTH)))
        self.assertTrue(np.all((simulation.y >= 0) & (simulation.y <= gyre.HEIGHT)))
        self.assertGreater(simulation.mixed_fraction(), 0.2)
        counts = simulation.counts((10, 20))
        self.assertEqual(counts.sum(), 200 * 100)
        self.assertEqual(counts[1].sum(), 100 * 100)

    def test_ftle_of_a_linear_saddle(self):
        # The flow map of u = (s x, -s y) over T has FTLE exactly s.
        rate, duration = 0.3, 4.0
        x, y = np.meshgrid(np.linspace(-1, 1, 21), np.linspace(-1, 1, 11))
        sigma = gyre.ftle_from_flow_map(
            x * np.exp(rate * duration), y * np.exp(-rate * duration),
            (0.1, 0.2), duration,
        )  # fmt: skip
        np.testing.assert_allclose(sigma, rate, rtol=1e-12)

    def test_ftle_is_periodic_and_has_ridges(self):
        shape = (40, 80)
        first = gyre.ftle_field(2.0, shape=shape)
        later = gyre.ftle_field(2.0 + gyre.PERIOD, shape=shape)
        np.testing.assert_allclose(first, later, atol=1e-9)
        self.assertGreater(first.max(), 0.25)  # strong attracting ridges ...
        self.assertLess(np.mean(first > 0.25), 0.1)  # ... that are thin lines


if __name__ == "__main__":
    unittest.main()
