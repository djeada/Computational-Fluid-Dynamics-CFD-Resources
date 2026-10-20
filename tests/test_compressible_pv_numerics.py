"""Numerical checks for the Riemann-solver, checkerboard and SIMPLE examples.

Riemann solvers: the exact solver reproduces Toro's star pressures, every
flux is consistent, the Godunov scheme conserves mass, momentum and energy to
round-off in a periodic box, contact-resolving fluxes keep a stationary
contact exact, and the L1 error decreases with refinement at the rate
expected for discontinuous solutions. Checkerboard: the checkerboard field is
in the null space of the interpolated gradient and of the wide Laplacian but
not of the compact one. SIMPLE: the converged nozzle flow converges to
Bernoulli's solution at first order, independently of the relaxation factors.
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
        f"{category}_{name}", ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


riemann = load_example("algorithms", "riemann_solver_comparison")
checker = load_example("plots", "checkerboard_pressure")
nozzle = load_example("algorithms", "simple_1d_nozzle")
sod = load_example("simulations", "sod_shock_tube")


class ExactRiemannSolverTests(unittest.TestCase):
    def test_sod_star_pressure(self):
        p_star, u_star, iterations = riemann.star_state(
            (1.0, 0.0, 1.0), (0.125, 0.0, 0.1)
        )
        self.assertAlmostEqual(float(p_star), 0.30313, places=5)
        self.assertAlmostEqual(float(u_star), 0.92745, places=5)
        self.assertLess(iterations, 10)

    def test_toro_tests_vectorised(self):
        left = [
            np.array(v)
            for v in ((1.0, 1.0, 1.0), (-2.0, 0.0, 0.0), (0.4, 1000.0, 0.01))
        ]
        right = [
            np.array(v) for v in ((1.0, 1.0, 1.0), (2.0, 0.0, 0.0), (0.4, 0.01, 100.0))
        ]
        p_star, u_star, _ = riemann.star_state(left, right)
        np.testing.assert_allclose(p_star, [0.0018938, 460.894, 46.0950], rtol=5e-5)
        np.testing.assert_allclose(u_star, [0.0, 19.5975, -6.19633], atol=5e-4)

    def test_both_exact_solvers_agree(self):
        x = np.linspace(0.0, 1.0, 501)
        problem = riemann.PROBLEMS["sod"]
        ours = riemann.exact_solution(problem, x, 0.2)
        theirs = sod.exact_solution(x, 0.2)
        for a, b in zip(ours, theirs, strict=True):
            np.testing.assert_allclose(a, b, rtol=1e-12, atol=1e-14)


def random_states(n, rng):
    rho = rng.uniform(0.2, 2.0, n)
    u = rng.uniform(-1.0, 1.0, n)
    p = rng.uniform(0.2, 2.0, n)
    return riemann.conservative(rho, u, p)


class FluxTests(unittest.TestCase):
    def test_fluxes_are_consistent(self):
        U = random_states(50, np.random.default_rng(1))
        for name, flux in riemann.FLUXES.items():
            with self.subTest(name):
                np.testing.assert_allclose(
                    flux(U, U), riemann.physical_flux(U), atol=1e-12
                )

    def test_supersonic_states_give_the_upwind_flux(self):
        rng = np.random.default_rng(2)
        rho, p = rng.uniform(0.5, 1.5, (2, 20))
        UL = riemann.conservative(rho, 3.0 + rng.uniform(0, 1, 20), p)  # M > 2
        UR = riemann.conservative(rho[::-1], 3.0 + rng.uniform(0, 1, 20), p[::-1])
        for name in ("exact", "hll", "hllc", "roe"):
            with self.subTest(name):
                np.testing.assert_allclose(
                    riemann.FLUXES[name](UL, UR), riemann.physical_flux(UL), rtol=1e-10
                )

    def test_stationary_contact_is_exact_for_contact_resolving_fluxes(self):
        UL = riemann.conservative(np.array([1.0]), np.array([0.0]), np.array([1.0]))
        UR = riemann.conservative(np.array([0.1]), np.array([0.0]), np.array([1.0]))
        pressure_only = np.array([[0.0], [1.0], [0.0]])
        for name in ("exact", "hllc", "roe"):
            np.testing.assert_allclose(
                riemann.FLUXES[name](UL, UR), pressure_only, atol=1e-12, err_msg=name
            )
        for name in ("hll", "rusanov"):  # these diffuse mass down the density jump
            mass_flux = riemann.FLUXES[name](UL, UR)[0, 0]
            self.assertGreater(mass_flux, 0.01, name)

    def test_godunov_scheme_conserves_in_a_periodic_box(self):
        rng = np.random.default_rng(3)
        n = 64
        U = random_states(n, rng)
        dx = 1.0 / n
        before = U.sum(axis=1) * dx
        for name, flux in riemann.FLUXES.items():
            with self.subTest(name):
                V = U.copy()
                for _ in range(40):
                    dt = 0.5 * dx / riemann.max_wave_speed(V)
                    V = riemann.godunov_step(V, flux, dt, dx, boundary="periodic")
                np.testing.assert_allclose(
                    V.sum(axis=1) * dx, before, rtol=1e-13, atol=1e-14
                )
                self.assertGreater(np.abs(V - U).max(), 1e-3)  # it did evolve

    def test_l1_error_decreases_with_refinement(self):
        problem = riemann.PROBLEMS["sod"]
        cells = (100, 200, 400)
        for solver in riemann.SOLVERS:
            with self.subTest(solver):
                errors = [riemann.l1_density_error(problem, solver, n) for n in cells]
                self.assertTrue(errors[0] > errors[1] > errors[2], errors)
                rate = riemann.observed_rate(cells, errors)
                # Contact smearing grows like sqrt(dx); shocks converge at first order.
                self.assertGreater(rate, 0.5)
                self.assertLess(rate, 1.0)

    def test_hllc_and_roe_beat_rusanov(self):
        problem = riemann.PROBLEMS["sod"]
        rusanov = riemann.l1_density_error(problem, "rusanov", 200)
        for solver in ("exact", "hllc", "roe"):
            self.assertLess(
                riemann.l1_density_error(problem, solver, 200), 0.7 * rusanov
            )


class CheckerboardTests(unittest.TestCase):
    def test_checkerboard_is_in_the_null_space_of_linear_interpolation(self):
        for n in (8, 16, 30):
            dx = 1.0 / n
            p = checker.checkerboard(n)
            np.testing.assert_allclose(
                checker.central_gradient(n, dx) @ p, 0.0, atol=1e-12
            )
            np.testing.assert_allclose(
                checker.wide_laplacian(n, dx) @ p, 0.0, atol=1e-9
            )
            np.testing.assert_allclose(
                checker.compact_laplacian(n, dx) @ p, -4.0 / dx**2 * p, rtol=1e-12
            )

    def test_zero_eigenvalue_counts(self):
        n, dx = 12, 1.0 / 12
        self.assertEqual(
            checker.count_zero_eigenvalues(checker.wide_laplacian(n, dx), dx)[0], 2
        )
        self.assertEqual(
            checker.count_zero_eigenvalues(checker.compact_laplacian(n, dx), dx)[0], 1
        )
        wide_2d = checker.laplacian_2d(checker.wide_laplacian(n, dx))
        compact_2d = checker.laplacian_2d(checker.compact_laplacian(n, dx))
        self.assertEqual(checker.count_zero_eigenvalues(wide_2d, dx)[0], 4)
        self.assertEqual(checker.count_zero_eigenvalues(compact_2d, dx)[0], 1)
        board = checker.checkerboard(n, 2).ravel()
        np.testing.assert_allclose(wide_2d @ board, 0.0, atol=1e-9)

    def test_spectra_match_the_fourier_symbols(self):
        n, dx = 16, 1.0 / 16
        theta = 2.0 * np.pi * np.arange(n) / n
        for laplacian, symbol in (
            (checker.wide_laplacian, checker.symbol_wide),
            (checker.compact_laplacian, checker.symbol_compact),
        ):
            matrix = laplacian(n, dx)
            values = checker.circulant_eigenvalues(matrix)
            np.testing.assert_allclose(values, symbol(theta, dx), atol=1e-9)
            np.testing.assert_allclose(
                np.sort(values), np.linalg.eigvalsh(matrix), atol=1e-9
            )


class SimpleNozzleTests(unittest.TestCase):
    def test_bernoulli_mass_flow(self):
        self.assertAlmostEqual(nozzle.exact_mass_flow(), 0.1 * np.sqrt(20.0), places=12)

    def test_converged_solution_satisfies_discrete_continuity(self):
        result = nozzle.solve_nozzle(17)
        self.assertTrue(result.converged)
        self.assertLess(np.ptp(result.mass_flow), 1e-5)
        self.assertEqual(result.p[-1], nozzle.P_EXIT)
        # Inlet node pressure follows from the stagnation pressure.
        u_in = result.u[0] * nozzle.area(result.x_u[0]) / nozzle.AREA_IN
        self.assertAlmostEqual(
            result.p[0], nozzle.P_STAGNATION - 0.5 * u_in**2, places=12
        )

    def test_mass_flow_converges_to_bernoulli_at_first_order(self):
        exact = nozzle.exact_mass_flow()
        errors = []
        for n in (33, 65, 129, 257):
            result = nozzle.solve_nozzle(n)
            self.assertTrue(result.converged)
            errors.append(abs(result.mass_flow.mean() - exact) / exact)
        ratios = np.array(errors[:-1]) / np.array(errors[1:])
        np.testing.assert_allclose(ratios, 2.0, atol=0.1)
        self.assertLess(errors[-1], 6e-3)
        # The pressure profile approaches Bernoulli's with the exact mass flow.
        pressure_errors = []
        for n in (65, 257):
            result = nozzle.solve_nozzle(n)
            pressure_errors.append(
                np.abs(result.p - nozzle.exact_pressure(result.x_p)).max()
            )
        self.assertGreater(pressure_errors[0] / pressure_errors[1], 3.0)
        self.assertLess(pressure_errors[1], 0.2)

    def test_fixed_point_is_independent_of_relaxation(self):
        tol = 1e-11  # converge tightly so that only the fixed point is compared
        reference = nozzle.solve_nozzle(33, 0.7, 0.3, tol=tol).mass_flow.mean()
        for variant, alpha_u, alpha_p in (
            ("SIMPLE", 0.5, 0.5),
            ("SIMPLE", 0.8, 0.2),
            ("SIMPLEC", 0.7, 1.0),
        ):
            result = nozzle.solve_nozzle(33, alpha_u, alpha_p, variant, tol=tol)
            self.assertTrue(result.converged)
            self.assertAlmostEqual(result.mass_flow.mean(), reference, places=9)

    def test_too_little_relaxation_diverges(self):
        self.assertFalse(nozzle.solve_nozzle(33, 0.8, 0.8).converged)

    def test_simplec_matches_simple_with_complementary_pressure_factor(self):
        for alpha_u in (0.5, 0.7):
            simple = nozzle.solve_nozzle(33, alpha_u, 1.0 - alpha_u).iterations
            simplec = nozzle.solve_nozzle(33, alpha_u, 1.0, "SIMPLEC").iterations
            self.assertLess(abs(simple - simplec), 0.15 * simple)


if __name__ == "__main__":
    unittest.main()
