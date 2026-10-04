"""Shallow-water ripples: conservation, rest state, dam break and wave speed."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np
from scipy.optimize import brentq

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / "simulations" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


swe = load_example("shallow_water_ripples")
G = swe.GRAVITY


def stoker_depth(x, t, h_left, h_right, g=G):
    """Exact depth of the wet-bed dam break (Stoker, 1957), dam at x = 0.

    A rarefaction runs into the deep side and a bore into the shallow side;
    the middle state has the same velocity behind both.
    """
    c_left = np.sqrt(g * h_left)

    def velocity_mismatch(h):
        behind_rarefaction = 2 * (c_left - np.sqrt(g * h))
        behind_bore = (h - h_right) * np.sqrt(0.5 * g * (h + h_right) / (h * h_right))
        return behind_rarefaction - behind_bore

    h_mid = brentq(velocity_mismatch, h_right, h_left)
    u_mid = 2 * (c_left - np.sqrt(g * h_mid))
    bore_speed = h_mid * u_mid / (h_mid - h_right)
    xi = x / t
    fan = (2 * c_left - xi) ** 2 / (9 * g)
    return np.select(
        [xi < -c_left, xi < u_mid - np.sqrt(g * h_mid), xi < bore_speed],
        [h_left, fan, h_mid],
        h_right,
    )


def run_channel(h, dx, dt, steps):
    """Advance a 1D depth profile at rest as two identical rows of cells."""
    q = np.zeros((3, 2, h.size))
    q[0] = h
    for _ in range(steps):
        q = swe.ssp_rk2_step(q, dx, dt)
    np.testing.assert_array_equal(q[0, 0], q[0, 1])  # stays exactly 1D
    np.testing.assert_array_equal(q[2], 0.0)
    return q[0, 0]


class ShallowWaterRipplesTests(unittest.TestCase):
    def test_volume_changes_only_by_the_drops(self):
        drops = [(0.0, 0.5, 0.7, 5e-3), (0.2, 1.3, 1.1, 4e-3), (0.4, 1.0, 1.5, 6e-3)]
        simulation = swe.ShallowWaterSimulation(n=50, drops=drops)
        simulation.advance(50)  # steps up to t = 0.196 s: the second drop is next
        self.assertEqual(simulation.drops_landed, 1)
        simulation.advance(250)
        self.assertEqual(simulation.drops_landed, 3)
        self.assertGreater(simulation.added_volume, 0.0)
        error = (
            simulation.volume() - simulation.initial_volume - simulation.added_volume
        )
        self.assertLess(abs(error) / simulation.initial_volume, 1e-13)

    def test_lake_at_rest_stays_exactly_at_rest(self):
        simulation = swe.ShallowWaterSimulation(n=32, drops=[])
        simulation.advance(100)
        np.testing.assert_array_equal(simulation.q[0], swe.DEPTH)
        np.testing.assert_array_equal(simulation.q[1:], 0.0)

    def test_centred_drop_keeps_the_square_symmetry(self):
        drops = [(0.0, 1.0, 1.0, 0.005)]
        simulation = swe.ShallowWaterSimulation(n=40, drops=drops)
        simulation.advance(200)  # the ring has reflected from all four walls
        h, hu, hv = simulation.q
        np.testing.assert_allclose(h, h.T, rtol=0, atol=1e-15)
        np.testing.assert_allclose(h, h[::-1], rtol=0, atol=1e-15)
        np.testing.assert_allclose(hu, hv.T, rtol=0, atol=1e-15)
        np.testing.assert_allclose(hu, -hu[:, ::-1], rtol=0, atol=1e-15)

    def test_dam_break_converges_to_stoker_solution(self):
        h_left, h_right, t_end = 1.0, 0.25, 0.2  # [m], [m], [s]
        errors = []
        for n in (200, 400):
            dx = 2.0 / n  # channel -1 m < x < 1 m, dam at x = 0
            x = (np.arange(n) + 0.5) * dx - 1.0
            steps = n  # dt = t_end / n: Courant number about 0.4
            h = run_channel(np.where(x < 0, h_left, h_right), dx, t_end / steps, steps)
            exact = stoker_depth(x, t_end, h_left, h_right)
            errors.append(np.mean(np.abs(h - exact)) / (h_left - h_right))
        self.assertLess(errors[1], 0.002)  # 0.15 % of the dam height
        self.assertLess(errors[1], 0.6 * errors[0])  # first order at the bore

    def test_small_pulse_travels_at_shallow_water_speed(self):
        n, dx, dt, steps = 400, 0.01, 0.004, 750  # 4 m channel, t = 3 s
        x = (np.arange(n) + 0.5) * dx
        amplitude, start = 1e-6 * swe.DEPTH, 1.0
        pulse = amplitude * np.exp(-0.5 * ((x - start) / 0.1) ** 2)
        eta = run_channel(swe.DEPTH + pulse, dx, dt, steps) - swe.DEPTH
        # d'Alembert: two halves move apart at sqrt(g H). The left one has
        # reflected from the wall at x = 0 but is still behind x = 1.6 m. The
        # centroid is used because the limiter flattens and delays the peak.
        right = x > 1.6
        centroid = np.sum(x[right] * eta[right]) / np.sum(eta[right])
        speed = (centroid - start) / (dt * steps)
        self.assertAlmostEqual(speed / np.sqrt(G * swe.DEPTH), 1.0, delta=1e-3)
        half = np.sum(eta[right]) / np.sum(pulse)
        self.assertAlmostEqual(half, 0.5, delta=1e-4)
        self.assertAlmostEqual(eta[right].max() / amplitude, 0.5, delta=0.02)

    def test_rain_schedule_is_seeded_and_inside_the_basin(self):
        first = swe.rain_schedule(np.random.default_rng(3))
        np.testing.assert_array_equal(
            first, swe.rain_schedule(np.random.default_rng(3))
        )
        times, x, y, amplitude = first.T
        self.assertEqual(times[0], swe.FIRST_DROP_TIME)
        self.assertTrue(np.all(np.diff(times) > 0))
        self.assertLess(times[-1], swe.RAIN_DURATION)
        span = swe.RAIN_DURATION - swe.FIRST_DROP_TIME
        expected = span * (swe.RAIN_RATE_START + swe.RAIN_RATE_END) / 2
        self.assertEqual(len(times), int(expected))
        for position in (x, y):
            self.assertTrue(np.all(position >= swe.DROP_MARGIN))
            self.assertTrue(np.all(position <= swe.BASIN_SIZE - swe.DROP_MARGIN))
        self.assertTrue(np.all(amplitude <= 1.25 * swe.DROP_AMPLITUDE))

    def test_largest_drop_respects_the_courant_limit(self):
        drops = [(0.0, 1.0, 1.0, 1.25 * swe.DROP_AMPLITUDE)]
        simulation = swe.ShallowWaterSimulation(drops=drops)
        largest = 0.0
        for _ in range(40):  # the mound collapses into a ring in 0.1 s
            courant = swe.courant_number(simulation.q, simulation.dx, simulation.dt)
            largest = max(largest, courant)
            simulation.advance(1)
        self.assertLess(largest, 0.5)


if __name__ == "__main__":
    unittest.main()
