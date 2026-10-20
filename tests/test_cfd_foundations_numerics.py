"""CFD foundations: manufactured-solution verification, boundary treatments, 1D model."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(category, name):
    spec = importlib.util.spec_from_file_location(
        f"cfd_foundations_{name}", ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mms = load_example("algorithms", "method_of_manufactured_solutions")
ghost = load_example("algorithms", "ghost_cell_boundary_conditions")
domain = load_example("plots", "continuous_vs_discrete_domain")


class ManufacturedSolutionTests(unittest.TestCase):
    def test_source_term_is_minus_laplacian_of_manufactured_solution(self):
        # Fourth-order finite-difference Laplacian of phi_m at interior points.
        h = 1e-3
        rng = np.random.default_rng(0)
        x, y = rng.uniform(0.1, 0.9, size=(2, 20))
        f = mms.manufactured
        lap = (
            -f(x + 2 * h, y)
            + 16 * f(x + h, y)
            - 30 * f(x, y)
            + 16 * f(x - h, y)
            - f(x - 2 * h, y)
            - f(x, y + 2 * h)
            + 16 * f(x, y + h)
            - 30 * f(x, y)
            + 16 * f(x, y - h)
            - f(x, y - 2 * h)
        ) / (12 * h**2)
        np.testing.assert_allclose(-lap, mms.manufactured_source(x, y), atol=1e-6)

    def test_neumann_data_is_x_derivative(self):
        h = 1e-6
        y = np.linspace(0.0, 1.0, 11)
        fd = (mms.manufactured(1.0 + h, y) - mms.manufactured(1.0 - h, y)) / (2 * h)
        np.testing.assert_allclose(mms.manufactured_dx(1.0, y), fd, atol=1e-6)

    def test_correct_solver_is_second_order_in_both_norms(self):
        n, results = mms.convergence_study((16, 32, 64))
        for norm in ("l2", "linf"):
            p = mms.observed_orders(results[2][norm])
            np.testing.assert_allclose(p, 2.0, atol=0.05)

    def test_bugged_boundary_drops_the_order_to_one(self):
        n, results = mms.convergence_study((64, 128, 256))
        for norm in ("l2", "linf"):
            p = mms.observed_orders(results[1][norm])
            self.assertLess(p[-1], 1.15)
            self.assertGreater(p[-1], 0.9)

    def test_dirichlet_values_are_imposed_exactly(self):
        x, y, phi = mms.solve_poisson(8)
        np.testing.assert_allclose(phi[0, :], mms.manufactured(0.0, y))
        np.testing.assert_allclose(phi[:, 0], mms.manufactured(x, 0.0))
        np.testing.assert_allclose(phi[:, -1], mms.manufactured(x, 1.0))


class GhostCellTests(unittest.TestCase):
    def test_exact_solution_satisfies_equation_and_boundary_conditions(self):
        m, q, bi = ghost.FIN_PARAMETER, ghost.BASE_FLUX, ghost.TIP_BIOT
        h = 1e-4
        x = np.linspace(0.1, 0.9, 9)
        t = ghost.exact_solution
        second = (t(x + h) - 2 * t(x) + t(x - h)) / h**2
        np.testing.assert_allclose(second, m**2 * t(x), rtol=1e-5)
        d0 = (t(h) - t(-h)) / (2 * h)
        d1 = (t(1 + h) - t(1 - h)) / (2 * h)
        self.assertAlmostEqual(-d0, q, places=6)
        self.assertAlmostEqual(-d1, bi * t(1.0), places=6)

    def test_observed_orders_of_the_four_variants(self):
        errors = ghost.convergence_study((64, 128, 256))
        expected = {("fd", 1): 1, ("fd", 2): 2, ("fv", 1): 1, ("fv", 2): 2}
        for key, order in expected.items():
            p = ghost.observed_orders(errors[key])
            np.testing.assert_allclose(p, order, atol=0.03, err_msg=str(key))

    def test_finite_volume_energy_balance(self):
        # Heat in at the base = heat lost along the fin + heat lost at the tip.
        n = 32
        h = 1.0 / n
        x, theta = ghost.solve_fv(n, 2)
        side_loss = ghost.FIN_PARAMETER**2 * np.sum(theta) * h
        tip_loss = theta[-1] / (1.0 / ghost.TIP_BIOT + 0.5 * h)
        self.assertAlmostEqual(side_loss + tip_loss, ghost.BASE_FLUX, places=12)


class DiscreteDomainTests(unittest.TestCase):
    def test_four_point_solution_matches_hand_calculation(self):
        x, u = domain.solve_backward_difference(4)
        np.testing.assert_allclose(u, [1.0, 0.75, 9 / 16, 27 / 64])
        a, b = domain.assemble_system(4)
        np.testing.assert_allclose(np.linalg.solve(a, b), u)

    def test_backward_difference_is_first_order(self):
        dx, err = domain.outlet_errors((64, 128, 256))
        np.testing.assert_allclose(domain.observed_orders(dx, err), 1.0, atol=0.02)


if __name__ == "__main__":
    unittest.main()
