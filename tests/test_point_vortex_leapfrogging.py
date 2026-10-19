"""Point-vortex leapfrogging: pair speed, invariants, RK4 order, Love's ratio."""

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


vortex = load_example("point_vortex_leapfrogging")
NO_SMOKE = np.zeros(0)


def integrate(x, y, circulation, core, dt, steps):
    """Vortex positions after steps RK4 steps, without tracers."""
    x, y = x.copy(), y.copy()
    for _ in range(steps):
        vortex.rk4_step(x, y, NO_SMOKE, NO_SMOKE.copy(), circulation, core, dt)
    return x, y


def passage_ratio(alpha, core=0.0, dt=1e-3):
    """Half-width ratio when the pairs first pass, interpolated in time."""
    x, y, circulation = vortex.initial_vortices(alpha, perturbation=0.0)
    previous = None
    while True:
        gap = y[2:].mean() - y[:2].mean()
        widths = vortex.half_widths(x)
        ratio = widths.min() / widths.max()
        if previous is not None and gap < 0:
            weight = previous[0] / (previous[0] - gap)
            return previous[1] + weight * (ratio - previous[1])
        previous = (gap, ratio)
        vortex.rk4_step(x, y, NO_SMOKE, NO_SMOKE.copy(), circulation, core, dt)


class LeapfrogTests(unittest.TestCase):
    def test_single_pair_translates_at_gamma_over_2_pi_d(self):
        gamma, d = 2.0, 0.8
        x, y = np.array([-d / 2, d / 2]), np.array([0.3, 0.3])
        circulation = np.array([gamma, -gamma])
        u, v = vortex.vortex_velocities(x, y, circulation, 0.0)
        np.testing.assert_allclose(v, gamma / (2 * np.pi * d), rtol=1e-14)
        np.testing.assert_allclose(u, 0.0, atol=1e-15)
        x_end, y_end = integrate(x, y, circulation, 0.0, 0.01, 500)
        np.testing.assert_allclose(x_end, x, atol=1e-12)
        np.testing.assert_allclose(y_end - y, 5.0 * gamma / (2 * np.pi * d), rtol=1e-12)
        # A Krasny core of radius delta slows the pair to Gamma d / 2 pi (d^2 + delta^2).
        u, v = vortex.vortex_velocities(x, y, circulation, 0.3)
        np.testing.assert_allclose(v, gamma * d / (2 * np.pi * (d**2 + 0.09)))

    def test_invariants_conserved_over_many_leapfrogs(self):
        simulation = vortex.LeapfrogSimulation(smoke_per_vortex=1, dt=0.005)
        start = np.array(simulation.invariants())
        simulation.advance(6000)  # t = 30, about 20 passages
        end = np.array(simulation.invariants())
        self.assertGreaterEqual(simulation.leapfrogs, 18)
        self.assertLess(abs(end[0] - start[0]) / abs(start[0]), 1e-8)  # energy
        np.testing.assert_allclose(end[1:3], start[1:3], atol=1e-10)  # impulse
        self.assertLess(abs(end[3] - start[3]) / abs(start[3]), 1e-8)  # angular

    def test_rk4_converges_at_fourth_order(self):
        x, y, circulation = vortex.initial_vortices()
        core = vortex.CORE_RADIUS
        reference = integrate(x, y, circulation, core, 1 / 1280, 1280)
        errors = []
        for steps in (20, 40, 80):
            x_end, y_end = integrate(x, y, circulation, core, 1 / steps, steps)
            errors.append(np.hypot(x_end - reference[0], y_end - reference[1]).max())
        orders = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(orders, 4.0, atol=0.25)

    def test_initial_gap_gives_loves_passing_ratio(self):
        for alpha in (0.3, 0.4, 0.6):
            with self.subTest(alpha=alpha):
                self.assertAlmostEqual(passage_ratio(alpha), alpha, delta=1e-4)
        with self.assertRaises(ValueError):
            vortex.pair_separation(0.15)  # below 3 - 2 sqrt(2): pairs never pass

    def test_leapfrogging_stable_above_0382_and_unstable_below(self):
        def asymmetry(alpha):
            simulation = vortex.LeapfrogSimulation(
                alpha=alpha, smoke_per_vortex=1, dt=0.01
            )
            simulation.advance(4000)  # t = 40
            return abs(simulation.x.sum()), simulation.leapfrogs

        stable, passages = asymmetry(0.45)
        self.assertLess(stable, 1e-2)  # the 1e-3 perturbation stays small
        self.assertGreater(passages, 30)
        unstable, _ = asymmetry(0.3)
        self.assertGreater(unstable, 0.3)  # the pairs exchange partners

    def test_tracers_follow_the_same_velocity_field(self):
        simulation = vortex.LeapfrogSimulation(smoke_per_vortex=2, dt=0.01)
        # A tracer placed on a vortex moves with it: the smoothed self-induced
        # velocity at the centre is zero.
        simulation.px = simulation.x.copy()
        simulation.py = simulation.y.copy()
        simulation.pair = np.array([0, 0, 1, 1])
        simulation.advance(200)
        np.testing.assert_allclose(simulation.px, simulation.x, atol=1e-12)
        np.testing.assert_allclose(simulation.py, simulation.y, atol=1e-12)
        self.assertEqual(len(simulation.history), 201)


if __name__ == "__main__":
    unittest.main()
