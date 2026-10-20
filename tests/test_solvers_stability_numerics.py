"""Linear solvers, nonlinear iterations, von Neumann factors and time-integrator stability."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np
from scipy.sparse import diags, identity, kron
from scipy.sparse.linalg import spsolve

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / "algorithms" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


solvers = load_example("iterative_linear_solvers")
nonlinear = load_example("picard_vs_newton")
vonneumann = load_example("von_neumann_amplification")
integrators = load_example("time_integrator_stability")
monitoring = load_example("residual_monitoring")


def poisson_direct(f, h):
    """Reference solution of the five-point system with a sparse direct solver."""
    n = f.shape[0] - 2
    t = diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(n, n))
    a = (kron(t, identity(n)) + kron(identity(n), t)) / h**2
    u = np.zeros_like(f)
    u[1:-1, 1:-1] = spsolve(a.tocsc(), f[1:-1, 1:-1].ravel()).reshape(n, n)
    return u


class IterativeLinearSolverTests(unittest.TestCase):
    N = 15

    def setUp(self):
        self.h = solvers.grid_spacing(self.N)
        self.f = solvers.random_rhs(self.N)
        self.u_ref = poisson_direct(self.f, self.h)

    def test_every_method_reaches_the_direct_solution(self):
        for method in solvers.METHODS:
            u, history = solvers.solve(method, self.N)
            self.assertLess(history[-1], solvers.TOLERANCE, method)
            err = np.max(np.abs(u - self.u_ref)) / np.max(np.abs(self.u_ref))
            self.assertLess(err, 1e-6, method)

    def test_jacobi_rate_matches_spectral_radius(self):
        _, history = solvers.solve("Jacobi", self.N)
        rate = (history[-1] / history[-201]) ** (1 / 200)
        self.assertAlmostEqual(rate, solvers.jacobi_spectral_radius(self.N), places=3)

    def test_gauss_seidel_rate_is_jacobi_rate_squared(self):
        _, history = solvers.solve("Gauss-Seidel", self.N)
        rate = (history[-1] / history[-101]) ** (1 / 100)
        self.assertAlmostEqual(
            rate, solvers.jacobi_spectral_radius(self.N) ** 2, places=3
        )

    def test_optimal_sor_beats_gauss_seidel_and_neighbouring_omegas(self):
        omega = solvers.optimal_omega(self.N)
        counts = {
            w: len(solvers.sor(self.f, self.h, w)[1])
            for w in (1.0, omega - 0.1, omega, omega + 0.05)
        }
        self.assertLess(5 * counts[omega], counts[1.0])
        self.assertLessEqual(counts[omega], counts[omega - 0.1])
        self.assertLessEqual(counts[omega], counts[omega + 0.05])

    def test_multigrid_iterations_are_independent_of_n(self):
        counts = [len(solvers.solve("Multigrid V(2,1)", n)[1]) for n in (15, 31, 63)]
        self.assertLessEqual(max(counts) - min(counts), 1)
        self.assertLess(max(counts), 12)

    def test_cg_iterations_grow_like_sqrt_kappa(self):
        counts = [len(solvers.solve("CG", n)[1]) for n in (15, 31, 63)]
        ratios = np.array(counts[1:]) / np.array(counts[:-1])
        np.testing.assert_allclose(ratios, 2.0, atol=0.3)  # sqrt(kappa) ~ N

    def test_restriction_and_prolongation_preserve_smooth_fields(self):
        n = 31
        x = np.linspace(0, 1, n + 2)
        xc = np.linspace(0, 1, (n - 1) // 2 + 2)
        fine = np.outer(x * (1 - x), x * (1 - x))
        coarse = np.outer(xc * (1 - xc), xc * (1 - xc))
        np.testing.assert_allclose(
            solvers.restrict_full_weighting(fine), coarse, atol=2e-3
        )
        np.testing.assert_allclose(solvers.prolong_bilinear(coarse), fine, atol=2e-3)

    def test_weighted_jacobi_damps_modes_by_predicted_factor(self):
        n = solvers.SMOOTHING_INTERVALS
        x = np.linspace(0, 1, n + 1)
        omega = 2.0 / 3.0
        for k in (3, 20, 44, 60):
            e = solvers.weighted_jacobi_1d(np.sin(k * np.pi * x), omega, 1)
            np.testing.assert_allclose(
                e,
                solvers.jacobi_damping_factor(k, n, omega) * np.sin(k * np.pi * x),
                atol=1e-12,
            )
        high = np.arange(n // 2, n)
        self.assertLessEqual(
            np.max(np.abs(solvers.jacobi_damping_factor(high, n, omega))), 1 / 3 + 1e-12
        )


class PicardNewtonTests(unittest.TestCase):
    def setUp(self):
        self.x, self.h = nonlinear.grid()
        self.u0 = nonlinear.linear_guess(self.x)

    def test_jacobian_matches_finite_differences(self):
        rng = np.random.default_rng(0)
        u = self.u0 + 0.1 * rng.standard_normal(self.u0.shape)
        u[0], u[-1] = nonlinear.U_LEFT, nonlinear.U_RIGHT
        ab = nonlinear.jacobian_bands(u, self.h)
        m = len(u) - 2
        dense = np.diag(ab[1]) + np.diag(ab[0, 1:], 1) + np.diag(ab[2, :-1], -1)
        eps = 1e-7
        fd = np.zeros((m, m))
        r0 = nonlinear.residual(u, self.h)[1:-1]
        for j in range(m):
            up = u.copy()
            up[j + 1] += eps
            fd[:, j] = (nonlinear.residual(up, self.h)[1:-1] - r0) / eps
        np.testing.assert_allclose(dense, fd, atol=1e-3 * np.max(np.abs(dense)))

    def test_newton_converges_quadratically(self):
        u, iterates, history = nonlinear.newton(self.u0, self.h)
        self.assertLess(history[-1], nonlinear.TOLERANCE)
        errors = nonlinear.error_sequence(iterates, u)
        self.assertGreater(nonlinear.convergence_order(errors), 1.8)

    def test_under_relaxed_picard_converges_linearly(self):
        u_ref = nonlinear.newton(self.u0, self.h)[0]
        u, iterates, history = nonlinear.picard(
            self.u0, self.h, alpha=nonlinear.UNDER_RELAXATION
        )
        self.assertLess(history[-1], nonlinear.TOLERANCE)
        np.testing.assert_allclose(u, u_ref, atol=1e-9)
        errors = nonlinear.error_sequence(iterates, u_ref)
        tail = errors[(errors > 1e-9) & (errors < 1e-3)]
        ratios = tail[1:] / tail[:-1]
        mean_rate = (tail[-1] / tail[0]) ** (1 / (len(tail) - 1))
        self.assertTrue(0.3 < mean_rate < 0.5)
        self.assertGreater(
            ratios.min(), 0.2
        )  # no speed-up as the error shrinks: linear

    def test_discrete_solution_is_second_order_accurate(self):
        errors = []
        for n in (64, 128, 256):
            x, h = nonlinear.grid(n)
            u = nonlinear.newton(nonlinear.linear_guess(x), h)[0]
            errors.append(np.max(np.abs(u - nonlinear.exact_solution(x))))
        orders = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(orders, 2.0, atol=0.15)

    def test_pseudo_transient_continuation_rescues_the_hard_guess(self):
        ug = nonlinear.hard_guess(self.x)
        full = nonlinear.newton(ug, self.h)[2]
        ptc = nonlinear.newton(ug, self.h, pseudo_dt=nonlinear.PSEUDO_TIME_STEP)
        self.assertGreater(full[-1], 1.0)
        self.assertLess(ptc[2][-1], nonlinear.TOLERANCE)
        np.testing.assert_allclose(
            ptc[0], nonlinear.newton(self.u0, self.h)[0], atol=1e-9
        )


class VonNeumannTests(unittest.TestCase):
    theta = np.linspace(1e-6, np.pi, 1001)

    def test_stable_schemes_satisfy_g_le_one_up_to_cfl_limit(self):
        for scheme in ("Upwind", "Lax-Friedrichs", "Lax-Wendroff"):
            for c in (0.1, 0.5, 0.9, 1.0):
                g = np.abs(vonneumann.advection_amplification(scheme, self.theta, c))
                self.assertLessEqual(g.max(), 1 + 1e-12, (scheme, c))
            g = np.abs(vonneumann.advection_amplification(scheme, self.theta, 1.1))
            self.assertGreater(g.max(), 1.0, scheme)

    def test_ftcs_advection_is_unconditionally_unstable(self):
        for c in (0.01, 0.5, 1.0):
            g = np.abs(vonneumann.advection_amplification("FTCS", self.theta, c))
            np.testing.assert_allclose(g**2, 1 + c**2 * np.sin(self.theta) ** 2)

    def test_diffusion_limits(self):
        for r in (0.1, 0.5):
            g = vonneumann.diffusion_amplification("FTCS", self.theta, r)
            self.assertLessEqual(np.max(np.abs(g)), 1 + 1e-12)
        self.assertGreater(
            abs(vonneumann.diffusion_amplification("FTCS", np.pi, 0.51)), 1
        )
        for scheme in ("BTCS", "Crank-Nicolson"):
            for r in (0.5, 10, 1000):
                g = vonneumann.diffusion_amplification(scheme, self.theta, r)
                self.assertLessEqual(np.max(np.abs(g)), 1 + 1e-12)

    def test_marching_reproduces_amplification_factor(self):
        n, k, c = 64, 5, 0.7
        x = np.arange(n) / n
        theta = 2 * np.pi * k / n
        u0 = np.exp(2j * np.pi * k * x)
        for scheme in vonneumann.ADVECTION_SCHEMES:
            u1 = vonneumann.advection_step(u0, scheme, c)
            np.testing.assert_allclose(
                u1,
                vonneumann.advection_amplification(scheme, theta, c) * u0,
                atol=1e-12,
            )
        r = 0.4
        for scheme in ("FTCS", "BTCS", "Crank-Nicolson"):
            u1 = vonneumann.diffusion_march(u0.real, scheme, r, 1)
            np.testing.assert_allclose(
                u1,
                vonneumann.diffusion_amplification(scheme, theta, r) * u0.real,
                atol=1e-12,
            )

    def test_upwind_damping_matches_modified_equation(self):
        a, dx, c = 1.0, 0.01, 0.8
        dt = c * dx / a
        nu_num = vonneumann.numerical_viscosity_upwind(a, dx, c)
        theta = 0.05  # long wave, where the modified equation is accurate
        k = theta / dx
        g = np.abs(vonneumann.advection_amplification("Upwind", theta, c))
        self.assertAlmostEqual(-np.log(g) / dt / (nu_num * k**2), 1.0, places=2)

    def test_lax_wendroff_phase_error_is_second_order(self):
        c = 0.5
        errors = [
            abs(1 - vonneumann.relative_phase_speed("Lax-Wendroff", t, c))
            for t in (0.1, 0.05)
        ]
        self.assertAlmostEqual(np.log2(errors[0] / errors[1]), 2.0, places=1)


class TimeIntegratorTests(unittest.TestCase):
    def test_observed_orders(self):
        errors = integrators.order_study()
        expected = {
            "Explicit Euler": 1,
            "Implicit Euler": 1,
            "RK2": 2,
            "AB2": 2,
            "BDF2": 2,
            "Crank-Nicolson": 2,
            "RK3 (SSP)": 3,
            "RK4": 4,
        }
        for method, p in expected.items():
            self.assertAlmostEqual(
                integrators.observed_order(errors[method]), p, delta=0.1, msg=method
            )

    def test_rk_boundary_points_have_unit_amplification(self):
        for name in integrators.RK_COEFFS:
            z = integrators.rk_boundary(name, n_rays=90)
            np.testing.assert_allclose(
                np.abs(integrators.rk_stability_function(name, z)), 1.0, atol=1e-8
            )

    def test_known_stability_intervals(self):
        self.assertAlmostEqual(
            integrators.real_axis_limit("Explicit Euler"), -2.0, places=4
        )
        self.assertAlmostEqual(integrators.real_axis_limit("RK4"), -2.7853, places=3)
        self.assertAlmostEqual(
            integrators.imaginary_axis_limit("RK3 (SSP)"), np.sqrt(3), places=3
        )
        self.assertAlmostEqual(
            integrators.imaginary_axis_limit("RK4"), 2 * np.sqrt(2), places=3
        )
        self.assertEqual(integrators.imaginary_axis_limit("Explicit Euler"), 0.0)
        self.assertEqual(integrators.imaginary_axis_limit("RK2"), 0.0)

    def test_multistep_boundary_locus_has_unit_root(self):
        for name in ("AB2", "BDF2"):
            z = integrators.boundary_locus(name, n=37)[1:-1]
            z = z[np.isfinite(z)]
            np.testing.assert_allclose(
                integrators.multistep_growth(name, z), 1.0, atol=1e-8
            )

    def test_a_and_l_stability(self):
        z = -np.logspace(-2, 6, 50)
        self.assertTrue(
            np.all(
                np.abs(integrators.implicit_stability_function("Crank-Nicolson", z))
                <= 1
            )
        )
        self.assertTrue(np.all(integrators.multistep_growth("BDF2", z) <= 1 + 1e-12))
        self.assertLess(
            abs(integrators.implicit_stability_function("Implicit Euler", -1e6)), 1e-5
        )
        self.assertGreater(
            abs(integrators.implicit_stability_function("Crank-Nicolson", -1e6)), 0.99
        )
        self.assertLess(integrators.multistep_growth("BDF2", -1e6)[0], 1e-2)

    def test_stiff_problem_explicit_fails_implicit_works(self):
        a, b, y0, exact = integrators.stiff_problem()
        n = int(round(integrators.STIFF_T_END / integrators.STIFF_DT))
        _, y = integrators.integrate("RK4", a, b, y0, integrators.STIFF_T_END, n)
        self.assertTrue(np.isnan(y[-1]))
        for method in ("Implicit Euler", "BDF2"):
            t, y = integrators.integrate(method, a, b, y0, integrators.STIFF_T_END, n)
            self.assertLess(np.max(np.abs(y[2:] - exact(t[2:]))), 0.03, method)

    def test_central_advection_eigenvalues_lie_on_imaginary_axis(self):
        central, upwind, diffusion = integrators.operator_eigenvalues()
        np.testing.assert_allclose(central.real, 0.0, atol=1e-15)
        moving = central[np.abs(central) > 1e-12]
        self.assertTrue(
            np.all(
                np.abs(integrators.rk_stability_function("Explicit Euler", moving)) > 1
            )
        )
        self.assertTrue(
            np.all(np.abs(integrators.rk_stability_function("RK4", central)) <= 1)
        )
        self.assertTrue(
            np.all(
                np.abs(integrators.rk_stability_function("Explicit Euler", upwind))
                <= 1 + 1e-12
            )
        )
        self.assertTrue(
            np.all(
                np.abs(integrators.rk_stability_function("Explicit Euler", diffusion))
                <= 1 + 1e-12
            )
        )


class ResidualMonitoringTests(unittest.TestCase):
    def test_direct_solution_is_second_order(self):
        errors = []
        for n in (15, 31, 63):
            x, _, _, _ = monitoring.setup(n)
            xx, yy = np.meshgrid(x, x, indexing="ij")
            phi = monitoring.direct_solution(n)
            errors.append(np.max(np.abs(phi - monitoring.exact_solution(xx, yy))))
        orders = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(orders, 2.0, atol=0.1)

    def test_error_decays_at_gauss_seidel_rate_and_residual_bounds_error(self):
        mon = monitoring.monitored_solve(n=15, sweeps=400, keep=())
        h = 1.0 / 16
        rate = (mon["error"][-1] / mon["error"][-101]) ** (1 / 100)
        self.assertAlmostEqual(rate, np.cos(np.pi * h) ** 2, places=4)
        # ||e|| / ||phi_h|| <= kappa ||r|| / ||b||, and r^0 = b for the zero initial guess
        kappa = 1.0 / np.tan(0.5 * np.pi * h) ** 2
        self.assertTrue(np.all(mon["error"] <= kappa * mon["res_initial"]))

    def test_wall_flux_converges_to_exact_value(self):
        q = []
        for n in (31, 63):
            q.append(monitoring.wall_flux(monitoring.direct_solution(n), 1.0 / (n + 1)))
        errors = np.abs(np.array(q) - monitoring.exact_wall_flux())
        self.assertGreater(np.log2(errors[0] / errors[1]), 1.8)

    def test_incompatible_neumann_problem_stalls(self):
        res, mean = monitoring.neumann_solve(n=16, sweeps=600)
        self.assertGreater(res[-1], 0.05)
        self.assertAlmostEqual(res[-1], res[-50], places=6)
        drift = np.diff(mean[-50:])
        np.testing.assert_allclose(drift, drift.mean(), rtol=1e-3)
        res_ok, _ = monitoring.neumann_solve(n=16, sweeps=600, mean_source=0.0)
        self.assertLess(res_ok[-1], 1e-6)


if __name__ == "__main__":
    unittest.main()
