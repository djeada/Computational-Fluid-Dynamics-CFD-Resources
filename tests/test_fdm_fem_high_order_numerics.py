"""Finite-difference weights, 1D finite elements, spectral differentiation and DG advection."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / "algorithms" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fd = load_example("finite_difference_stencils")
fem = load_example("fem_1d_poisson")
spectral = load_example("spectral_vs_finite_difference")
dg = load_example("dg_linear_advection")


def rates(h, err):
    h, err = np.asarray(h, float), np.asarray(err, float)
    return np.log(err[:-1] / err[1:]) / np.log(h[:-1] / h[1:])


class FiniteDifferenceStencilTests(unittest.TestCase):
    def test_known_weights(self):
        cases = [
            ((0, 1), 1, [-1, 1]),
            ((-1, 0, 1), 1, [-0.5, 0, 0.5]),
            ((-2, -1, 0), 1, [0.5, -2, 1.5]),
            ((-2, -1, 0, 1, 2), 1, [1 / 12, -2 / 3, 0, 2 / 3, -1 / 12]),
            ((-1, 0, 1), 2, [1, -2, 1]),
            ((-2, -1, 0, 1, 2), 2, [-1 / 12, 4 / 3, -5 / 2, 4 / 3, -1 / 12]),
        ]
        for offsets, m, expected in cases:
            with self.subTest(offsets=offsets, m=m):
                np.testing.assert_allclose(
                    fd.fd_weights(offsets, m), expected, atol=1e-12
                )

    def test_fornberg_matches_vandermonde(self):
        offsets = np.array([-3.0, -1.5, -0.5, 0.0, 0.7, 2.0])
        c = fd.fornberg_weights(0.0, offsets, 3)
        for m in range(4):
            np.testing.assert_allclose(
                c[:, m], fd.fd_weights(offsets, m), rtol=1e-9, atol=1e-9
            )

    def test_truncation_error_terms(self):
        for offsets, m, order, coeff in (
            ((-1, 0, 1), 1, 2, 1 / 6),
            ((-2, -1, 0, 1, 2), 1, 4, -1 / 30),
            ((-1, 0, 1), 2, 2, 1 / 12),
            ((0, 1), 1, 1, 0.5),
        ):
            p, c = fd.truncation_error(offsets, fd.fd_weights(offsets, m), m)
            self.assertEqual(p, order)
            self.assertAlmostEqual(c, coeff, places=12)

    def test_observed_orders_on_smooth_function(self):
        h = np.array([0.08, 0.04, 0.02])
        for offsets, order in (((0, 1), 1), ((-1, 0, 1), 2), ((-2, -1, 0, 1, 2), 4)):
            err = [
                abs(
                    fd.apply_stencil(fd.test_function, 1.0, hh, offsets)
                    - fd.test_derivative(1.0)
                )
                for hh in h
            ]
            np.testing.assert_allclose(rates(h, err), order, atol=0.1)

    def test_compact_scheme_is_sixth_order(self):
        h, err = fd.compact_errors(np.array([32, 64, 128]))
        np.testing.assert_allclose(rates(h, err), 6.0, atol=0.1)

    def test_modified_wavenumber_of_central_difference(self):
        theta = np.linspace(0.0, np.pi, 50)
        np.testing.assert_allclose(
            fd.modified_wavenumber((-1, 0, 1), theta), np.sin(theta), atol=1e-12
        )
        backward = fd.modified_wavenumber((-1, 0), theta)
        np.testing.assert_allclose(backward.imag, -(1 - np.cos(theta)), atol=1e-12)
        # The compact symbol is the derivative of a periodic grid function.
        n = 32
        x = 2 * np.pi * np.arange(n) / n
        du = fd.compact_derivative(np.sin(3 * x), 2 * np.pi / n)
        k_eff = fd.compact_modified_wavenumber(3 * 2 * np.pi / n) / (2 * np.pi / n)
        np.testing.assert_allclose(du, k_eff * np.cos(3 * x), atol=1e-12)

    def test_points_per_wavelength_second_order(self):
        # sin(theta)/theta = 1 - theta^2/6 gives theta = sqrt(0.06) for 1%.
        ppw = fd.points_per_wavelength(lambda t: np.sin(t), 0.01)
        self.assertAlmostEqual(ppw, 2 * np.pi / np.sqrt(0.06), delta=0.2)


class FiniteElementTests(unittest.TestCase):
    def test_element_stiffness_matrices(self):
        k1, f1 = fem.element_matrices(0.0, 0.5, 1, f=np.ones_like)
        np.testing.assert_allclose(k1, [[2, -2], [-2, 2]], atol=1e-12)
        np.testing.assert_allclose(f1, [0.25, 0.25], atol=1e-12)
        k2, f2 = fem.element_matrices(0.0, 1.0, 2, f=np.ones_like)
        np.testing.assert_allclose(
            k2, np.array([[7, -8, 1], [-8, 16, -8], [1, -8, 7]]) / 3.0, atol=1e-12
        )
        np.testing.assert_allclose(f2, [1 / 6, 2 / 3, 1 / 6], atol=1e-12)

    def test_p1_nodal_values_are_exact(self):
        for n in (3, 4, 7):
            _, nodes, _, u = fem.solve(n, 1)
            np.testing.assert_allclose(u, fem.exact_solution(nodes), atol=1e-10)

    def test_constant_load_three_elements(self):
        _, nodes, _, u = fem.solve(3, 1, f=np.ones_like)
        np.testing.assert_allclose(u[1:3], [1 / 9, 1 / 9], atol=1e-12)

    def test_p2_reproduces_quadratic_exactly(self):
        vertices, nodes, conn, u = fem.solve(2, 2, f=lambda x: 2.0 * np.ones_like(x))
        np.testing.assert_allclose(u, nodes * (1 - nodes), atol=1e-12)

    def test_convergence_orders(self):
        for degree, l2_order, h1_order in ((1, 2, 1), (2, 3, 2)):
            h, l2, h1 = fem.convergence(degree, (8, 16, 32))
            np.testing.assert_allclose(rates(h, l2), l2_order, atol=0.05)
            np.testing.assert_allclose(rates(h, h1), h1_order, atol=0.05)


class SpectralTests(unittest.TestCase):
    def test_fourier_derivative_reaches_round_off(self):
        err = spectral.max_error(
            spectral.fourier_derivative, spectral.smooth, spectral.smooth_derivative, 40
        )
        self.assertLess(err, 1e-12)

    def test_differentiation_matrix_matches_fft(self):
        x = spectral.grid(24)
        d = spectral.fourier_differentiation_matrix(24)
        np.testing.assert_allclose(
            d @ spectral.smooth(x),
            spectral.fourier_derivative(spectral.smooth(x)),
            atol=1e-12,
        )

    def test_finite_difference_orders(self):
        n = np.array([64, 128, 256])
        for order in (2, 4):
            err = [
                spectral.max_error(
                    lambda u, o=order: spectral.fd_derivative(u, o),
                    spectral.smooth,
                    spectral.smooth_derivative,
                    m,
                )
                for m in n
            ]
            np.testing.assert_allclose(rates(1.0 / n, err), order, atol=0.1)

    def test_chebyshev_exact_for_polynomials_and_spectral(self):
        d, x = spectral.chebyshev(6)
        np.testing.assert_allclose(d @ x**5, 5 * x**4, atol=1e-11)
        self.assertLess(spectral.chebyshev_error(30), 1e-11)

    def test_kink_destroys_spectral_convergence(self):
        res = spectral.kink_study()
        n, err = res["Fourier spectral"]
        self.assertAlmostEqual(spectral.slopes(n, err)[-1], 0.5, delta=0.05)

    def test_three_halves_rule_removes_aliasing(self):
        check = spectral.aliasing_check()
        self.assertAlmostEqual(check["plain"][1], 0.25, places=12)
        self.assertAlmostEqual(check["3/2 padded"][1], 0.0, places=12)
        self.assertAlmostEqual(check["3/2 padded"][0], 0.25, places=12)
        # Padding reproduces the exact truncated product of random band-limited data.
        rng = np.random.default_rng(3)
        n = 16
        u_hat = np.fft.fft(rng.normal(size=n))
        v_hat = np.fft.fft(rng.normal(size=n))
        u_hat[n // 2] = v_hat[n // 2] = 0.0
        full = np.convolve(np.fft.fftshift(u_hat), np.fft.fftshift(v_hat)) / n
        exact = np.fft.ifftshift(full[n // 2 : n // 2 + n])
        exact[n // 2] = 0.0
        np.testing.assert_allclose(
            spectral.pad_product(u_hat, v_hat), exact, atol=1e-10
        )


class DiscontinuousGalerkinTests(unittest.TestCase):
    def test_order_p_plus_one(self):
        n_values, study = dg.convergence_study(degrees=(1, 2, 3), n_values=(16, 32, 64))
        for p, err in study.items():
            with self.subTest(p=p):
                np.testing.assert_allclose(
                    dg.observed_orders(n_values, err), p + 1, atol=0.15
                )

    def test_p0_upwind_equals_first_order_upwind_scheme(self):
        solver = dg.DGAdvection(10, 0)
        c = solver.project(dg.smooth_wave)
        u = c[:, 0]
        expected = -dg.ADVECTION_SPEED * (u - np.roll(u, 1)) / solver.h
        np.testing.assert_allclose(solver.rhs(c)[:, 0], expected, atol=1e-12)

    def test_mass_conserved_and_energy_decays(self):
        solver = dg.DGAdvection(20, 2)
        c0 = solver.project(dg.pulses)
        c = solver.advance(c0, 0.3)
        self.assertAlmostEqual(solver.mass(c), solver.mass(c0), places=12)
        self.assertLess(solver.energy(c), solver.energy(c0))

    def test_central_flux_conserves_semi_discrete_energy(self):
        solver = dg.DGAdvection(12, 2, flux="central")
        c = solver.project(dg.pulses)
        m = np.arange(3)
        # d/dt ||u_h||^2 = 2 sum c M dc/dt must vanish for the central flux.
        rate = np.sum(c * solver.h / (2 * m + 1) * solver.rhs(c))
        self.assertAlmostEqual(rate, 0.0, places=10)

    def test_constant_state_is_preserved(self):
        solver = dg.DGAdvection(8, 3)
        c0 = solver.project(lambda x: 2.0 + 0.0 * x)
        np.testing.assert_allclose(solver.advance(c0, 0.1), c0, atol=1e-13)


if __name__ == "__main__":
    unittest.main()
