"""Verify solvers against conservation laws and analytical eigenmodes."""

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


wave = load_example("2d_wave_simulation")
heat = load_example("1d_heat_and_wave_equations")
quantum = load_example("schroedinger_equation")


class SimulationTests(unittest.TestCase):
    def test_wave_fixed_edges_and_zero_velocity_start(self):
        simulation = wave.WaveSimulation(nx=31, ny=23)
        original = simulation.u.copy()
        laplacian = (
            np.diff(original[1:-1], n=2, axis=1) / simulation.dx**2
            + np.diff(original[:, 1:-1], n=2, axis=0) / simulation.dy**2
        )
        simulation.advance()
        expected = original[1:-1, 1:-1] + 0.5 * simulation.dt**2 * laplacian
        np.testing.assert_allclose(simulation.u[1:-1, 1:-1], expected, atol=1e-14)
        simulation.advance(20)
        np.testing.assert_array_equal(simulation.u[[0, -1]], 0.0)
        np.testing.assert_array_equal(simulation.u[:, [0, -1]], 0.0)
        self.assertEqual(simulation.steps, 21)

    def test_wave_standing_mode(self):
        simulation = wave.WaveSimulation(length=1, nx=61, ny=51)
        mode = np.sin(np.pi * (simulation.X + 1) / 2) * np.sin(
            np.pi * (simulation.Y + 1) / 2
        )
        mode[[0, -1]] = 0
        mode[:, [0, -1]] = 0
        _, first = wave.leapfrog_step(
            mode, mode, simulation.dx, simulation.dy, simulation.dt
        )
        simulation.u = mode.copy()
        simulation.u_prev = mode + 0.5 * (first - mode)
        simulation.advance(20)
        expected = mode * np.cos(np.pi / np.sqrt(2) * simulation.time)
        np.testing.assert_allclose(simulation.u, expected, atol=1e-4)

    def test_heat_matches_analytical_diffusion(self):
        simulation = heat.HeatWaveSimulation(
            length=1, nx=81, diffusivity=0.1, total_time=1
        )
        initial = np.sin(np.pi * simulation.x)
        initial[[0, -1]] = 0
        simulation.heat[:] = initial
        simulation.advance(25)
        expected = initial * np.exp(-0.1 * np.pi**2 * simulation.time)
        np.testing.assert_allclose(simulation.heat, expected, atol=5e-5)
        self.assertLess(np.linalg.norm(simulation.heat), np.linalg.norm(initial))

    def test_1d_wave_matches_standing_mode(self):
        simulation = heat.HeatWaveSimulation(length=1, nx=81, total_time=1)
        mode = np.sin(np.pi * simulation.x)
        mode[[0, -1]] = 0
        simulation.wave[:] = mode
        simulation.wave_prev[:] = mode
        simulation.wave_prev[1:-1] += 0.5 * simulation.courant2 * np.diff(mode, n=2)
        simulation.advance(20)
        np.testing.assert_allclose(
            simulation.wave, mode * np.cos(np.pi * simulation.time), atol=2e-5
        )

    def test_schrodinger_conserves_probability_and_phase(self):
        simulation = quantum.SchrodingerSimulation(length=8, n=32, dt=0.02)
        k = 2 * np.pi / 8
        initial = np.exp(1j * k * simulation.X) / 8
        simulation.psi = initial.copy()
        simulation.advance(100)
        expected = initial * np.exp(-0.5j * k**2 * simulation.time)
        np.testing.assert_allclose(simulation.psi, expected, atol=1e-13)
        self.assertAlmostEqual(simulation.norm, 1.0, places=12)
        self.assertEqual(simulation.steps, 100)

    def test_cached_schrodinger_steps_match_reference(self):
        simulation = quantum.SchrodingerSimulation(n=16)
        expected = simulation.psi.copy()
        k2 = quantum.squared_wavenumbers(16, simulation.dx)
        potential = quantum.potential(simulation.X, simulation.Y)
        for _ in range(7):
            expected = quantum.evolve(expected, simulation.dt, k2, potential)
        simulation.advance(7)
        np.testing.assert_allclose(simulation.psi, expected, atol=1e-14)

    def test_batch_and_individual_steps_agree(self):
        factories = (
            lambda: wave.WaveSimulation(nx=13, ny=11),
            lambda: heat.HeatWaveSimulation(nx=21, total_time=1),
            lambda: quantum.SchrodingerSimulation(n=16),
        )
        for factory, field in zip(factories, ("u", "wave", "psi")):
            batch, individual = factory(), factory()
            batch.advance(5)
            for _ in range(5):
                individual.advance()
            np.testing.assert_array_equal(
                getattr(batch, field), getattr(individual, field)
            )
            self.assertEqual(batch.time, individual.time)

    def test_invalid_parameters_and_negative_steps(self):
        for factory in (
            lambda: wave.WaveSimulation(cfl_safety=2),
            lambda: heat.HeatWaveSimulation(courant=2),
            lambda: quantum.SchrodingerSimulation(dt=0),
        ):
            with self.assertRaises(ValueError):
                factory()
        with self.assertRaises(ValueError):
            quantum.SchrodingerSimulation(n=8).advance(-1)


cavity = load_example("lid_driven_cavity")
lbm = load_example("lattice_boltzmann_cylinder_flow")


class FlowSolverTests(unittest.TestCase):
    def test_cavity_keeps_wall_conditions_and_pressure_gauge(self):
        simulation = cavity.CavitySimulation(n_points=17)
        simulation.advance(10)
        np.testing.assert_array_equal(simulation.u[-1], cavity.LID_VELOCITY)
        np.testing.assert_array_equal(simulation.u[0], 0.0)
        np.testing.assert_array_equal(simulation.u[:-1, [0, -1]], 0.0)
        np.testing.assert_array_equal(simulation.v[[0, -1]], 0.0)
        np.testing.assert_array_equal(simulation.v[:, [0, -1]], 0.0)
        self.assertAlmostEqual(simulation.p.mean(), 0.0, places=12)
        self.assertTrue(np.isfinite(simulation.u).all())
        self.assertEqual(simulation.steps, 10)

    def test_cavity_batch_matches_single_iterations(self):
        batch, single = cavity.CavitySimulation(13), cavity.CavitySimulation(13)
        batch.advance(5)
        for _ in range(5):
            single.advance()
        for name in ("u", "v", "p"):
            np.testing.assert_array_equal(getattr(batch, name), getattr(single, name))

    def test_lbm_equilibrium_recovers_density_and_momentum(self):
        rho = np.full((24, 16), 1.2)
        velocity = np.zeros((2, 24, 16))
        velocity[0] = 0.03
        velocity[1] = -0.02
        populations = lbm.equilibrium(rho, velocity)
        np.testing.assert_allclose(lbm.compute_density(populations), rho, atol=1e-14)
        np.testing.assert_allclose(
            lbm.compute_velocity(populations, rho), velocity, atol=1e-14
        )

    def test_lbm_uniform_flow_is_stationary_without_obstacle(self):
        velocity = np.zeros((2, 24, 16))
        velocity[0] = 0.03
        populations = lbm.equilibrium(1.0, velocity)
        initial = populations.copy()
        for _ in range(10):
            lbm.lbm_step(
                populations, np.zeros((24, 16), dtype=bool), velocity, relaxation=1.5
            )
        np.testing.assert_allclose(populations, initial, atol=1e-14)

    def test_lbm_speed_uses_current_populations_and_masks_cylinder(self):
        simulation = lbm.LatticeBoltzmannSimulation((36, 24))
        simulation.advance(3)
        velocity = lbm.compute_velocity(
            simulation.populations, lbm.compute_density(simulation.populations)
        )
        np.testing.assert_allclose(
            simulation.speed[~simulation.obstacle],
            np.linalg.norm(velocity, axis=0)[~simulation.obstacle],
        )
        self.assertTrue(np.isnan(simulation.speed[simulation.obstacle]).all())
        self.assertEqual(simulation.steps, 3)
