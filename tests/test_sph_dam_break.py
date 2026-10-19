"""SPH dam break: kernel, conservation, hydrostatics and energy."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np
from scipy.integrate import quad

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / "simulations" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sph = load_example("sph_dam_break")
H = sph.SMOOTHING_RATIO  # smoothing length in units of the spacing dp = 1


def lattice_sums(offset, h=H):
    """Kernel sums over a unit square lattice seen from a point at ``offset``."""
    grid = np.arange(-6, 7, dtype=float)
    rx, ry = (offset[0] - grid)[None, :], (offset[1] - grid)[:, None]
    rx, ry = np.broadcast_arrays(rx, ry)
    r = np.hypot(rx, ry).ravel()
    weight = np.array([sph.kernel(value, h) for value in r])
    slope = np.array([sph.kernel_derivative(value, h) for value in r])
    with np.errstate(invalid="ignore", divide="ignore"):
        scale = np.where(r > 0, slope / r, 0.0)
    gradient_x, gradient_y = scale * rx.ravel(), scale * ry.ravel()
    return weight, gradient_x, gradient_y, rx.ravel(), ry.ravel()


def free_cloud(seed=1):
    """A jittered patch of fluid with random velocities, no walls, no gravity."""
    rng = np.random.default_rng(seed)
    simulation = sph.SPHDamBreakSimulation(particles_across=4)
    dp = simulation.spacing
    x, y = sph.lattice(0.0, 0.0, 15, 15, dp)
    n = x.size
    simulation.x = x + 0.2 * dp * rng.uniform(-1, 1, n)
    simulation.y = y + 0.2 * dp * rng.uniform(-1, 1, n)
    simulation.vx, simulation.vy = rng.normal(0, 1, n), rng.normal(0, 1, n)
    simulation.rho = sph.REST_DENSITY * (1 + 0.01 * rng.uniform(-1, 1, n))
    simulation.n_fluid = n
    simulation.gravity = np.zeros(2)
    size = 2 * simulation.h
    simulation.grid = np.array([-2 * size, -2 * size, size, 40, 40], dtype=float)
    simulation.update_rates()
    return simulation


def mechanical_energy(simulation):
    """Kinetic, potential and elastic (Tait) energy of the fluid per unit depth."""
    f = simulation.n_fluid
    rho, rho0, gamma = simulation.rho[:f], sph.REST_DENSITY, sph.TAIT_EXPONENT
    b = rho0 * sph.SOUND_SPEED**2 / gamma
    # e(rho) = integral of p / rho^2 from rho0 to rho
    elastic = b / ((gamma - 1) * rho0**gamma) * (
        rho ** (gamma - 1) - rho0 ** (gamma - 1)
    ) + b * (1 / rho - 1 / rho0)
    kinetic = 0.5 * simulation.speed**2
    potential = sph.GRAVITY * simulation.y[:f]
    return simulation.mass * np.sum(kinetic + potential + elastic)


class SPHDamBreakTests(unittest.TestCase):
    def test_kernel_is_normalised(self):
        integral, _ = quad(lambda r: 2 * np.pi * r * sph.kernel(r, H), 0, 2 * H)
        self.assertAlmostEqual(integral, 1.0, places=10)
        self.assertEqual(sph.kernel(2 * H, H), 0.0)
        for offset in ((0, 0), (0.5, 0), (0.5, 0.5), (0.3, 0.7)):
            weight = lattice_sums(offset)[0]
            self.assertAlmostEqual(weight.sum(), 1.0, delta=2e-3)

    def test_kernel_gradient(self):
        for r in (0.3, 1.0, 1.7, 2.5):
            slope = (sph.kernel(r + 1e-6, H) - sph.kernel(r - 1e-6, H)) / 2e-6
            self.assertAlmostEqual(sph.kernel_derivative(r, H), slope, places=8)
        # On a symmetric lattice the gradients cancel, and -sum r grad W V = I.
        for offset in ((0, 0), (0.5, 0), (0.5, 0.5)):
            _, gx, gy, rx, ry = lattice_sums(offset)
            self.assertAlmostEqual(gx.sum(), 0.0, places=12)
            self.assertAlmostEqual(gy.sum(), 0.0, places=12)
            self.assertAlmostEqual(-np.sum(rx * gx), 1.0, delta=0.03)
            self.assertAlmostEqual(-np.sum(ry * gy), 1.0, delta=0.03)
            self.assertAlmostEqual(np.sum(rx * gy), 0.0, places=12)

    def test_pair_forces_conserve_momentum_and_angular_momentum(self):
        simulation = free_cloud()
        m = simulation.mass
        force_scale = m * np.abs(simulation.ax).sum()
        self.assertLess(abs(m * simulation.ax.sum()) / force_scale, 1e-14)
        self.assertLess(abs(m * simulation.ay.sum()) / force_scale, 1e-14)

        def invariants():
            s = simulation
            return np.array([s.vx.sum(), s.vy.sum(), np.sum(s.x * s.vy - s.y * s.vx)])

        before = invariants()
        momentum_scale = np.abs(simulation.vx).sum()
        simulation.advance(200)
        self.assertGreater(simulation.speed.max(), 0.5)  # the cloud is moving
        np.testing.assert_allclose(
            invariants(), before, rtol=0, atol=1e-12 * momentum_scale
        )

    def test_column_at_rest_stays_hydrostatic(self):
        # A tank as wide as the column: the water cannot collapse.
        simulation = sph.SPHDamBreakSimulation(particles_across=10, tank_width=0.5)
        f = simulation.n_fluid
        simulation.advance(1200)  # t = 0.44 s, several sound crossings
        depth = sph.COLUMN_HEIGHT - simulation.y[:f]
        exact = sph.REST_DENSITY * sph.GRAVITY * depth
        scale = sph.REST_DENSITY * sph.GRAVITY * sph.COLUMN_HEIGHT
        error = simulation.pressure[:f] - exact
        self.assertLess(np.sqrt(np.mean(error**2)) / scale, 0.015)
        self.assertLess(np.abs(error).max() / scale, 0.03)
        self.assertLess(simulation.speed.max(), 0.01 * sph.FREE_FALL_SPEED)

    def test_dam_break_dissipates_energy_and_stays_in_the_tank(self):
        simulation = sph.SPHDamBreakSimulation(particles_across=12)
        start = mechanical_energy(simulation)
        times, front, energy = [0.0], [simulation.surge_front()], [start]
        while simulation.time < 0.6:  # the surge reaches the far wall
            simulation.advance(50)
            times.append(simulation.time)
            front.append(simulation.surge_front())
            energy.append(mechanical_energy(simulation))
        # Artificial viscosity only removes energy; the walls do no work.
        self.assertLess(max(energy) - start, 0.005 * start)
        self.assertLess(energy[-1], start)
        # Until it hits the far wall the front advances, never faster than the
        # shallow-water (Ritter) front a + 2 sqrt(g 2a) t.
        wall = sph.TANK_WIDTH - simulation.spacing
        arrival = next(k for k, x in enumerate(front) if x > wall)
        self.assertTrue(np.all(np.diff(front[: arrival + 1]) > 0))
        celerity = np.sqrt(sph.GRAVITY * sph.COLUMN_HEIGHT)
        ritter = sph.COLUMN_WIDTH + 2 * celerity * np.array(times)
        self.assertTrue(np.all(np.array(front) <= ritter))
        f = simulation.n_fluid
        x, y = simulation.x[:f], simulation.y[:f]
        self.assertTrue(np.all((x > 0) & (x < sph.TANK_WIDTH)))
        self.assertTrue(np.all((y > 0) & (y < sph.TANK_HEIGHT)))


if __name__ == "__main__":
    unittest.main()
