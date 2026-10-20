"""Lattice Boltzmann: lattice isotropy, equilibrium moments, Poiseuille and viscosity."""

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


poiseuille = load_example("algorithms", "lbm_poiseuille_validation")
taylor_green = load_example("algorithms", "lbm_taylor_green_decay")
lattices = load_example("plots", "lattice_velocity_sets")
CS2 = 1.0 / 3.0


def moment_tensors(weights, velocities):
    """Weighted moments of order 0, 1, 2 and 4 of a velocity set."""
    return (
        weights.sum(),
        weights @ velocities,
        np.einsum("i,ia,ib->ab", weights, velocities, velocities),
        np.einsum("i,ia,ib,ic,id->abcd", weights, *[velocities] * 4),
    )


def isotropic_fourth(dimension):
    delta = np.eye(dimension)
    return CS2**2 * (
        np.einsum("ab,cd->abcd", delta, delta)
        + np.einsum("ac,bd->abcd", delta, delta)
        + np.einsum("ad,bc->abcd", delta, delta)
    )


class LatticeTests(unittest.TestCase):
    def check_lattice(self, weights, velocities):
        dimension = velocities.shape[1]
        zeroth, first, second, fourth = moment_tensors(weights, velocities)
        self.assertAlmostEqual(zeroth, 1.0, places=14)
        np.testing.assert_allclose(first, 0.0, atol=1e-15)
        np.testing.assert_allclose(second, CS2 * np.eye(dimension), atol=1e-15)
        np.testing.assert_allclose(fourth, isotropic_fourth(dimension), atol=1e-15)

    def test_d2q9_weights_and_isotropy(self):
        self.check_lattice(poiseuille.WEIGHTS, poiseuille.VELOCITIES)
        self.check_lattice(lattices.D2Q9_WEIGHTS, lattices.D2Q9_VELOCITIES)

    def test_d3q19_weights_and_isotropy(self):
        velocities = lattices.d3q19_velocities()
        self.assertEqual(len(velocities), 19)
        self.check_lattice(lattices.d3q19_weights(velocities), velocities)

    def test_opposite_directions(self):
        for module in (poiseuille, lattices):
            velocities = getattr(module, "VELOCITIES", None)
            if velocities is None:
                velocities = module.D2Q9_VELOCITIES
            opposite = getattr(module, "OPPOSITE", None)
            if opposite is None:
                opposite = module.D2Q9_OPPOSITE
            np.testing.assert_array_equal(velocities[opposite], -velocities)

    def test_equilibrium_reproduces_density_momentum_and_stress(self):
        rng = np.random.default_rng(1)
        rho = 1.0 + 0.1 * rng.standard_normal((5, 7))
        u = 0.1 * rng.standard_normal((2, 5, 7))
        c = poiseuille.VELOCITIES
        for feq in (
            poiseuille.equilibrium(rho, u[0], u[1]),
            taylor_green.equilibrium(rho, u),
        ):
            np.testing.assert_allclose(feq.sum(axis=0), rho, rtol=1e-14)
            momentum = np.einsum("qd,qxy->dxy", c, feq)
            np.testing.assert_allclose(momentum, rho * u, atol=1e-15)
            stress = np.einsum("qa,qb,qxy->abxy", c, c, feq)
            expected = rho * (
                CS2 * np.eye(2)[:, :, None, None] + np.einsum("axy,bxy->abxy", u, u)
            )
            np.testing.assert_allclose(stress, expected, atol=1e-15)


class PoiseuilleTests(unittest.TestCase):
    def test_profile_error_is_small(self):
        _, u, u_exact, _ = poiseuille.simulate_channel(16, 1.0)
        self.assertLess(poiseuille.relative_l2_error(u, u_exact), 2e-3)

    def test_half_way_bounce_back_is_second_order(self):
        widths = (8, 16, 32)
        errors = poiseuille.convergence_study(taus=(0.8,), widths=widths)
        orders = poiseuille.observed_orders(errors, widths)
        np.testing.assert_allclose(orders, 2.0, atol=0.02)

    def test_slip_matches_bgk_prediction(self):
        taus = (0.6, 1.0, 1.5)
        measured = poiseuille.slip_scan(taus=taus, width=12)
        predicted = poiseuille.predicted_slip(
            np.array(taus), 1.0
        ) * poiseuille.viscosity(np.array(taus))
        np.testing.assert_allclose(measured, predicted, atol=1e-7)

    def test_magic_tau_puts_wall_exactly_halfway(self):
        _, u, u_exact, _ = poiseuille.simulate_channel(12, poiseuille.MAGIC_TAU)
        self.assertLess(poiseuille.relative_l2_error(u, u_exact), 1e-8)


class TaylorGreenTests(unittest.TestCase):
    def test_measured_viscosity_matches_tau_minus_half(self):
        for tau in (0.6, 0.8, 1.0):
            measured = taylor_green.measured_viscosity(32, tau)
            self.assertAlmostEqual(measured / ((tau - 0.5) / 3.0), 1.0, delta=5e-3)
            self.assertGreater(abs(measured / (tau / 3.0) - 1.0), 0.3)

    def test_viscosity_error_falls_with_resolution(self):
        errors = [
            abs(
                taylor_green.measured_viscosity(n, 1.5) / taylor_green.viscosity(1.5)
                - 1
            )
            for n in (16, 32)
        ]
        self.assertGreater(errors[0] / errors[1], 3.0)

    def test_mass_is_conserved(self):
        _, _, mass = taylor_green.run_decay(16, 0.8)
        np.testing.assert_allclose(mass, mass[0], rtol=1e-13)


if __name__ == "__main__":
    unittest.main()
