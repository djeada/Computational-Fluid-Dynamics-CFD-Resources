"""Check the finite-volume Euler solver of the forward-facing step example.

The solver is compared with the exact solution of Sod's shock tube, must keep
uniform flow and gas at rest unchanged, conserve mass, momentum and energy in
periodic and closed boxes, and reproduce the Rayleigh pitot pressure at the
stagnation point in front of the step.
"""

import dataclasses
import importlib.util
import math
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


step = load_example("supersonic_forward_facing_step")
GAMMA = step.GAMMA


def exact_riemann(left, right, xi, gamma=GAMMA):
    """Exact solution of the 1D Riemann problem for an ideal gas.

    ``left`` and ``right`` are (rho, u, p); returns rho, u and p at the
    similarity coordinates xi = (x - x0) / t, following Toro, Riemann Solvers
    and Numerical Methods for Fluid Dynamics (3rd ed., 2009), chapter 4.
    """
    (rl, ul, pl), (rr, ur, pr) = left, right
    cl, cr = math.sqrt(gamma * pl / rl), math.sqrt(gamma * pr / rr)

    def wave(p, rho, pk, ck):
        """Velocity jump across a shock (p > pk) or rarefaction, and its derivative."""
        if p > pk:
            a, b = 2.0 / ((gamma + 1.0) * rho), (gamma - 1.0) / (gamma + 1.0) * pk
            root = math.sqrt(a / (p + b))
            return (p - pk) * root, root * (1.0 - 0.5 * (p - pk) / (p + b))
        ratio = p / pk
        jump = 2.0 * ck / (gamma - 1.0) * (ratio ** ((gamma - 1.0) / (2 * gamma)) - 1)
        return jump, ratio ** (-(gamma + 1.0) / (2.0 * gamma)) / (rho * ck)

    p_star = 0.5 * (pl + pr)
    for _ in range(50):  # Newton iteration for the pressure between the waves
        fl, dl = wave(p_star, rl, pl, cl)
        fr, dr = wave(p_star, rr, pr, cr)
        change = (fl + fr + ur - ul) / (dl + dr)
        p_star = max(p_star - change, 1e-12)
        if abs(change) < 1e-14 * p_star:
            break
    u_star = 0.5 * (ul + ur) + 0.5 * (
        wave(p_star, rr, pr, cr)[0] - wave(p_star, rl, pl, cl)[0]
    )

    def sample(s, rho, u, p, c, sign):
        """State at x/t = s on the left (sign -1) or right (sign +1) of the contact."""
        g = (gamma - 1.0) / (gamma + 1.0)
        if p_star > p:  # shock
            speed = u + sign * c * math.sqrt(
                (gamma + 1) / (2 * gamma) * p_star / p + (gamma - 1) / (2 * gamma)
            )
            if sign * (s - speed) > 0:
                return rho, u, p
            return rho * (p_star / p + g) / (g * p_star / p + 1.0), u_star, p_star
        c_star = c * (p_star / p) ** ((gamma - 1.0) / (2.0 * gamma))
        if sign * (s - (u + sign * c)) > 0:  # ahead of the rarefaction
            return rho, u, p
        if sign * (s - (u_star + sign * c_star)) < 0:  # behind it
            return rho * (p_star / p) ** (1.0 / gamma), u_star, p_star
        u_fan = 2.0 / (gamma + 1.0) * (-sign * c + 0.5 * (gamma - 1.0) * u + s)
        c_fan = 2.0 / (gamma + 1.0) * (c - sign * 0.5 * (gamma - 1.0) * (u - s))
        ratio = c_fan / c
        return (
            rho * ratio ** (2 / (gamma - 1)),
            u_fan,
            p * ratio ** (2 * gamma / (gamma - 1)),
        )

    states = [
        sample(s, rl, ul, pl, cl, -1.0)
        if s < u_star
        else sample(s, rr, ur, pr, cr, 1.0)
        for s in xi
    ]
    return np.array(states).T


SOD_LEFT, SOD_RIGHT = (1.0, 0.0, 1.0), (0.125, 0.0, 0.1)


def sod_tube(n, axis="x", end_time=0.2):
    """Sod's shock tube along x or y, two cells wide, with reflecting side walls."""
    if axis == "x":
        domain = step.Domain(n, 2, 1 / n, 1 / n, x_boundary="outflow")
        position = np.broadcast_to((np.arange(n) + 0.5) / n, (2, n))
    else:
        domain = step.Domain(2, n, 1 / n, 1 / n, x_boundary="wall")
        position = np.broadcast_to(((np.arange(n) + 0.5) / n)[:, None], (n, 2))
    left = position < 0.5
    state = step.conservative(
        np.where(left, SOD_LEFT[0], SOD_RIGHT[0]),
        0.0,
        0.0,
        np.where(left, SOD_LEFT[2], SOD_RIGHT[2]),
    )
    for _ in range(40):  # 40 output intervals, each split to keep CFL <= 0.45
        state = step.advance_cfl(state, end_time / 40, domain)[0]
    return state, domain


def totals(state, domain):
    """Integrals of mass, x and y momentum and energy over the fluid cells."""
    fluid = ~domain.solid
    return state[:, fluid].sum(axis=1) * domain.dx * domain.dy


class ExactRiemannTests(unittest.TestCase):
    def test_sod_star_state(self):
        # The standard star-region values of Sod's shock tube.
        rho, u, p = exact_riemann(SOD_LEFT, SOD_RIGHT, [0.5, 1.2])
        np.testing.assert_allclose(p, 0.30313, atol=1e-5)
        np.testing.assert_allclose(u, 0.92745, atol=1e-5)
        np.testing.assert_allclose(rho, [0.42632, 0.26557], atol=1e-5)


class EulerSolverTests(unittest.TestCase):
    def test_sod_shock_tube_matches_exact_solution(self):
        errors = {}
        for n in (100, 200):
            state, _ = sod_tube(n)
            rho, u, v, p = step.primitive(state)[:, 0]
            x = (np.arange(n) + 0.5) / n
            exact = exact_riemann(SOD_LEFT, SOD_RIGHT, (x - 0.5) / 0.2)
            errors[n] = [np.mean(np.abs(q - e)) for q, e in zip((rho, u, p), exact)]
            np.testing.assert_array_equal(v, 0.0)
        # Density L1 error: 0.0049 on 100 cells and 0.0025 on 200 cells.
        self.assertLess(errors[200][0], 0.003)
        self.assertLess(errors[200][1], 0.006)
        self.assertLess(errors[200][2], 0.002)
        for before, after in zip(errors[100], errors[200]):
            self.assertLess(after, 0.6 * before)  # converges with the grid

    def test_sod_along_y_equals_sod_along_x(self):
        along_x, _ = sod_tube(64)
        along_y, _ = sod_tube(64, axis="y")
        swapped = along_y[[0, 2, 1, 3]].transpose(0, 2, 1)
        np.testing.assert_allclose(swapped, along_x, rtol=0, atol=1e-13)

    def test_uniform_supersonic_flow_is_preserved(self):
        domain = step.Domain(30, 12, 0.1, 0.1)  # tunnel without the step
        state = step.conservative(*(np.full((12, 30), q) for q in step.INFLOW))
        initial = state.copy()
        for _ in range(20):
            state = step.ssp_rk2_step(state, 0.01, domain)[0]
        np.testing.assert_array_equal(state, initial)  # bit for bit

    def test_gas_at_rest_around_the_step_stays_at_rest(self):
        domain = dataclasses.replace(step.make_tunnel(10), x_boundary="wall")
        state = step.conservative(
            *(np.full((domain.ny, domain.nx), q) for q in (1.4, 0, 0, 1))
        )
        initial = state.copy()
        for _ in range(20):
            state = step.ssp_rk2_step(state, 0.01, domain)[0]
        np.testing.assert_allclose(state, initial, rtol=0, atol=1e-13)

    def random_state(self, domain, seed=0):
        rng = np.random.default_rng(seed)
        shape = (domain.ny, domain.nx)
        rho = 1.0 + 0.5 * rng.random(shape)
        u, v = rng.standard_normal(shape), rng.standard_normal(shape)
        p = 1.0 + rng.random(shape)
        return step.conservative(rho, u, v, p)

    def test_periodic_box_conserves_mass_momentum_and_energy(self):
        domain = step.Domain(
            24, 16, 1 / 24, 1 / 16, x_boundary="periodic", y_boundary="periodic"
        )
        state = self.random_state(domain)
        before = totals(state, domain)
        for _ in range(10):
            state, _, cfl, floored = step.advance_cfl(state, 0.01, domain)
        self.assertEqual(floored, 0)
        np.testing.assert_allclose(
            totals(state, domain), before, rtol=1e-13, atol=1e-14
        )
        self.assertGreater(np.abs(state - self.random_state(domain)).max(), 0.1)

    def test_closed_tunnel_with_step_conserves_mass_and_energy(self):
        domain = dataclasses.replace(step.make_tunnel(10), x_boundary="wall")
        state = self.random_state(domain, seed=1)
        state[:, domain.solid] = step.conservative(1.4, 0.0, 0.0, 1.0)[:, None]
        before = totals(state, domain)
        for _ in range(10):
            state, _, _, floored = step.advance_cfl(state, 0.01, domain)
        self.assertEqual(floored, 0)
        after = totals(state, domain)
        np.testing.assert_allclose(after[[0, 3]], before[[0, 3]], rtol=1e-13)


class ForwardStepTests(unittest.TestCase):
    def test_stagnation_pressure_matches_rayleigh_pitot_formula(self):
        # Behind the normal part of the bow shock the flow comes to rest in
        # the corner in front of the step: p0 / p = 12.06 at Mach 3.
        mach, g = 3.0, GAMMA
        pitot = ((g + 1) ** 2 * mach**2 / (4 * g * mach**2 - 2 * (g - 1))) ** (
            g / (g - 1)
        ) * ((1 - g + 2 * g * mach**2) / (g + 1))
        self.assertAlmostEqual(pitot, 12.061, places=3)
        simulation = step.ForwardStepSimulation(cells_per_unit=40, dt=0.01)
        simulation.advance(100)  # t = 1: the bow shock has settled
        corner = []  # reflected waves make it oscillate by a few percent
        for _ in range(40):
            simulation.advance(5)
            p = step.primitive(simulation.state)[3]
            corner.append(p[0, simulation.domain.step_i - 1])
        self.assertAlmostEqual(simulation.time, 3.0)
        # The mean over 1 <= t <= 3 is 0.8 % below p0 on this grid.
        self.assertLess(abs(np.mean(corner) / pitot - 1.0), 0.02)
        self.assertEqual(simulation.floored_cells, 0)
        self.assertLessEqual(simulation.cfl, step.CFL)

    def test_bow_shock_stands_off_the_step(self):
        simulation = step.ForwardStepSimulation(cells_per_unit=40, dt=0.01)
        simulation.advance(200)  # t = 2
        p = step.primitive(simulation.state)[3]
        shock = np.argmax(p[0] > 2.0) / 40  # first cell behind the bow shock
        self.assertTrue(0.25 < shock < 0.4, shock)
        np.testing.assert_allclose(p[0, :8], 1.0, rtol=1e-12)  # undisturbed inflow

    def test_schlieren_ignores_walls_in_uniform_flow(self):
        simulation = step.ForwardStepSimulation(cells_per_unit=10)
        image = simulation.schlieren()
        fluid = ~simulation.domain.solid
        np.testing.assert_array_equal(image[fluid], 1.0)
        self.assertTrue(np.isnan(image[simulation.domain.solid]).all())


if __name__ == "__main__":
    unittest.main()
