"""Check the pseudo-spectral 2D turbulence solver against exact solutions."""

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


turbulence = load_example("decaying_2d_turbulence")


def grid(n):
    x = np.arange(n) * 2 * np.pi / n
    return np.meshgrid(x, x)  # X varies along columns, Y along rows


class DecayingTurbulenceTests(unittest.TestCase):
    def taylor_green(self, n, k, viscosity, hyperviscosity, steps, dt=0.01):
        x, y = grid(n)
        omega = 2 * k**2 * np.sin(k * x) * np.sin(k * y)  # psi = sin(kx) sin(ky)
        simulation = turbulence.TurbulenceSimulation(
            n=n, viscosity=viscosity, hyperviscosity=hyperviscosity, dt=dt,
            omega_hat=np.fft.rfft2(omega),
        )  # fmt: skip
        simulation.advance(steps)
        return omega, simulation

    def test_taylor_green_vortex_decays_exactly(self):
        # omega is proportional to psi, so u . grad(omega) = 0 and only viscosity acts.
        nu, k = 0.01, 2
        omega, simulation = self.taylor_green(32, k, nu, 0.0, steps=100)
        expected = omega * np.exp(-2 * nu * k**2 * simulation.time)
        np.testing.assert_allclose(simulation.vorticity, expected, atol=1e-12)
        self.assertAlmostEqual(simulation.time, 1.0)

    def test_taylor_green_with_hyperviscosity(self):
        nu, nu4, k = 1e-3, 1e-4, 3
        omega, simulation = self.taylor_green(32, k, nu, nu4, steps=50)
        rate = nu * 2 * k**2 + nu4 * (2 * k**2) ** 2  # |k|^2 = 2 k^2
        expected = omega * np.exp(-rate * simulation.time)
        np.testing.assert_allclose(simulation.vorticity, expected, atol=1e-11)

    def test_nonlinear_term_matches_analytic_jacobian(self):
        # psi = sin x + sin 2y: omega = sin x + 4 sin 2y, -u.grad(omega) = 6 cos x cos 2y.
        n = 32
        x, y = grid(n)
        omega = np.sin(x) + 4 * np.sin(2 * y)
        solver = turbulence.SpectralVorticitySolver(n, 0.0, 0.0)
        u, v = solver.velocity(np.fft.rfft2(omega))
        np.testing.assert_allclose(u, 2 * np.cos(2 * y), atol=1e-12)
        np.testing.assert_allclose(v, -np.cos(x), atol=1e-12)
        rate = np.fft.irfft2(solver.nonlinear(np.fft.rfft2(omega)), s=(n, n))
        np.testing.assert_allclose(rate, 6 * np.cos(x) * np.cos(2 * y), atol=1e-11)

    def test_dealiasing_removes_top_third(self):
        n = 48
        mask = turbulence.dealias_mask(n)
        kept_x = np.flatnonzero(mask[0])
        kept_y = np.fft.fftfreq(n, 1 / n)[mask[:, 0]]
        self.assertEqual(kept_x.max(), 15)  # 16 = n/3 would alias onto itself
        self.assertEqual(np.abs(kept_y).max(), 15)
        self.assertEqual(mask.sum(), 16 * 31)

    def test_dealiased_product_is_exact_galerkin_truncation(self):
        n = 48
        rng = np.random.default_rng(1)
        mask = turbulence.dealias_mask(n)
        a_hat = np.fft.rfft2(rng.standard_normal((n, n))) * mask
        b_hat = np.fft.rfft2(rng.standard_normal((n, n))) * mask
        product = np.fft.rfft2(
            np.fft.irfft2(a_hat, s=(n, n)) * np.fft.irfft2(b_hat, s=(n, n))
        )
        dealiased = product * mask / n**2
        # The exact product, on a grid fine enough for no aliasing at all.
        m = 2 * n
        rows = np.r_[0 : n // 2, m - n // 2 : m]  # the n x n modes inside m x m

        def on_fine_grid(coefficients):
            fine = np.zeros((m, m // 2 + 1), complex)
            fine[rows, : n // 2 + 1] = coefficients * (m / n) ** 2
            return np.fft.irfft2(fine, s=(m, m))

        exact = np.fft.rfft2(on_fine_grid(a_hat) * on_fine_grid(b_hat))
        exact = exact[rows, : n // 2 + 1] / m**2
        np.testing.assert_allclose(dealiased, exact * mask, atol=1e-12)
        # The aliasing errors are real; they all land in the removed band.
        self.assertGreater(np.abs(product / n**2 - exact)[~mask].max(), 1e-3)

    def test_energy_and_enstrophy_never_increase(self):
        rng = np.random.default_rng(0)
        simulation = turbulence.TurbulenceSimulation(
            n=64, viscosity=1e-3, hyperviscosity=1e-6, dt=0.01,
            omega_hat=turbulence.initial_vorticity(64, rng, k0=8.0, width=2.0),
        )  # fmt: skip
        simulation.advance(200)
        self.assertEqual(len(simulation.energy), 201)
        self.assertTrue(np.all(np.diff(simulation.energy) <= 0))
        self.assertTrue(np.all(np.diff(simulation.enstrophy) <= 0))
        # Enstrophy cascades to the dissipative small scales; energy decays slower.
        enstrophy_left = simulation.enstrophy[-1] / simulation.enstrophy[0]
        self.assertLess(enstrophy_left, 0.6)
        self.assertLess(enstrophy_left, simulation.energy[-1] / simulation.energy[0])
        # Nothing appears above the dealiasing limit.
        self.assertTrue(np.all(simulation.omega_hat[~simulation.solver.mask] == 0))

    def test_inviscid_run_conserves_energy_and_enstrophy(self):
        simulation = turbulence.TurbulenceSimulation(
            n=64, viscosity=0.0, hyperviscosity=0.0, dt=0.005
        )
        simulation.advance(200)
        energy, enstrophy = np.array(simulation.energy), np.array(simulation.enstrophy)
        # The dealiased (Galerkin) system conserves both exactly; RK4 drifts ~1e-8.
        np.testing.assert_allclose(energy, energy[0], rtol=1e-7)
        np.testing.assert_allclose(enstrophy, enstrophy[0], rtol=1e-7)

    def test_initial_field_has_requested_energy_and_band(self):
        simulation = turbulence.TurbulenceSimulation(n=128)
        self.assertAlmostEqual(simulation.energy[0], turbulence.INITIAL_ENERGY)
        k, spectrum = simulation.initial_spectrum
        self.assertLessEqual(abs(k[spectrum.argmax()] - turbulence.PEAK_WAVENUMBER), 1)
        self.assertAlmostEqual(spectrum.sum(), simulation.energy[0], places=10)
        self.assertAlmostEqual(simulation.vorticity.mean(), 0.0)


if __name__ == "__main__":
    unittest.main()
