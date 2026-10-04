"""Check the Rayleigh-Taylor solver against linear theory and conservation laws."""

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


rt = load_example("rayleigh_taylor_instability")


def linear_growth_rate(atwood=rt.ATWOOD, mode=1):
    """Boussinesq growth rate of a tanh interface: sigma^2 = A g k / (1 + k delta)."""
    k = 2 * np.pi * mode / rt.WIDTH
    return np.sqrt(atwood * rt.GRAVITY * k / (1 + k * rt.INTERFACE_THICKNESS))


def run_until(simulation, end_time):
    """Advance to ``end_time``; return the times and seeded-mode amplitudes."""
    times, amplitudes = [], []
    while simulation.time < end_time:
        simulation.advance(1)
        times.append(simulation.time)
        amplitudes.append(simulation.mode_velocity())
    return np.array(times), np.array(amplitudes)


class RayleighTaylorTests(unittest.TestCase):
    def test_poisson_solve_inverts_the_five_point_laplacian(self):
        nx, nz = 24, 40
        simulation = rt.RayleighTaylorSimulation(nx=nx, nz=nz)
        dx, dz = simulation.dx, simulation.dz
        omega = np.zeros((nz + 1, nx))
        omega[1:-1] = np.random.default_rng(3).standard_normal((nz - 1, nx))
        psi = rt.solve_streamfunction(omega, simulation.eigenvalues)
        np.testing.assert_array_equal(psi[[0, -1]], 0.0)  # impermeable walls
        laplacian = (np.roll(psi, 1, axis=1) - 2 * psi + np.roll(psi, -1, axis=1))[
            1:-1
        ] / dx**2 + (psi[2:] - 2 * psi[1:-1] + psi[:-2]) / dz**2
        np.testing.assert_allclose(laplacian, -omega[1:-1], atol=1e-10)

    def test_uniform_density_is_not_moved_by_any_flow(self):
        # Every face velocity is a difference of psi, so the discrete divergence
        # vanishes and flux-form advection keeps a uniform field uniform.
        nx, nz = 24, 40
        simulation = rt.RayleighTaylorSimulation(nx=nx, nz=nz, diffusivity=0.0)
        omega = np.zeros((nz + 1, nx))
        omega[1:-1] = 10 * np.random.default_rng(4).standard_normal((nz - 1, nx))
        psi = rt.solve_streamfunction(omega, simulation.eigenvalues)
        d_density, _ = simulation.rates(np.ones((nz, nx)), omega, psi)
        self.assertLess(np.abs(d_density).max(), 1e-9)

    def test_early_growth_rate_matches_linear_theory(self):
        simulation = rt.RayleighTaylorSimulation(
            nx=64, nz=128, amplitude=1e-5, noise=0.0, viscosity=0.0,
            diffusivity=0.0, max_time_step=0.01,
        )  # fmt: skip
        times, amplitudes = run_until(simulation, 2.5)
        first, last = np.searchsorted(times, 1.5), len(times) - 1
        measured = np.log(amplitudes[last] / amplitudes[first]) / (
            times[last] - times[first]
        )
        sigma = linear_growth_rate()
        self.assertAlmostEqual(measured / sigma, 1.0, delta=0.015)
        # The finite interface thickness matters: the sharp-interface rate is 4.5 % higher.
        sharp = np.sqrt(rt.ATWOOD * rt.GRAVITY * 2 * np.pi / rt.WIDTH)
        self.assertGreater(abs(measured / sharp - 1), 0.03)
        # Still linear at the end: the interface moved far less than a wavelength.
        self.assertLess(amplitudes[-1] / sigma, 0.01 * rt.WIDTH)

    def test_stable_stratification_only_oscillates(self):
        amplitude = 1e-3
        stable = rt.RayleighTaylorSimulation(
            nx=32, nz=64, atwood=-rt.ATWOOD, amplitude=amplitude, noise=0.0,
            max_time_step=0.01,
        )  # fmt: skip
        _, amplitudes = run_until(stable, 2.0)
        # Internal gravity wave: w is at most a * sigma, sigma being the same rate.
        self.assertLess(amplitudes.max(), amplitude * linear_growth_rate())
        unstable = rt.RayleighTaylorSimulation(
            nx=32, nz=64, amplitude=amplitude, noise=0.0, max_time_step=0.01
        )
        _, amplitudes = run_until(unstable, 2.0)
        self.assertGreater(amplitudes[-1], 20 * amplitude * linear_growth_rate())

    def test_flat_interface_and_zero_gravity_stay_at_rest(self):
        flat = rt.RayleighTaylorSimulation(nx=32, nz=64, amplitude=0.0, noise=0.0)
        flat.advance(50)
        np.testing.assert_array_equal(flat.vorticity, 0.0)
        np.testing.assert_array_equal(np.ptp(flat.density, axis=1), 0.0)
        weightless = rt.RayleighTaylorSimulation(nx=32, nz=64, gravity=0.0)
        weightless.advance(50)
        np.testing.assert_array_equal(weightless.vorticity, 0.0)

    def test_mean_density_is_conserved_and_bounded(self):
        simulation = rt.RayleighTaylorSimulation(
            nx=32, nz=64, amplitude=0.05, noise=1e-3, max_time_step=0.02
        )
        mean = simulation.density.mean()
        simulation.advance(150)  # well into the nonlinear stage
        self.assertGreater(simulation.mixing_width(), 1.0)
        self.assertAlmostEqual(simulation.density.mean(), mean, places=14)
        # WENO keeps the density within 1 % of the jump of its initial range.
        overshoot = 0.01 * 2 * rt.ATWOOD
        self.assertGreater(simulation.density.min(), 1 - rt.ATWOOD - overshoot)
        self.assertLess(simulation.density.max(), 1 + rt.ATWOOD + overshoot)


if __name__ == "__main__":
    unittest.main()
