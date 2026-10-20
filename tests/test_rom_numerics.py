"""Reduced-order models: POD-Galerkin Burgers and the certified reduced basis."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np
import scipy.sparse.linalg as spla
from scipy.linalg import eigh

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / "algorithms" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


burgers = load_example("pod_galerkin_burgers")
thermal = load_example("reduced_basis_thermal_block")


class PODGalerkinBurgersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grid = burgers.Grid(200)
        cls.u0 = burgers.initial_condition(cls.grid)
        cls.nu, cls.dt, cls.steps = 0.01, 1e-3, 100
        cls.fom = burgers.solve_fom(cls.u0, cls.grid, cls.nu, cls.dt, cls.steps)
        cls.pod = burgers.compute_pod(cls.fom)

    def test_rom_with_all_modes_reproduces_fom(self):
        # Every FOM state lies in mean + span(V), and the ROM uses the same
        # IMEX scheme, so the projected trajectory is the FOM trajectory.
        rank = self.pod.modes.shape[1]
        self.assertLess(rank, self.grid.n)  # the test is not a trivial full basis
        ops = burgers.build_rom(self.pod.mean, self.pod.modes, self.grid)
        coefficients = burgers.solve_rom(ops, self.u0, self.nu, self.dt, self.steps)
        fields = burgers.reconstruct(ops, coefficients)
        self.assertLess(burgers.relative_errors(fields, self.fom).max(), 1e-9)

    def test_error_decreases_with_rank(self):
        errors = []
        for r in (2, 5, 10, 20):
            ops = burgers.build_rom(self.pod.mean, self.pod.modes[:, :r], self.grid)
            fields = burgers.reconstruct(
                ops, burgers.solve_rom(ops, self.u0, self.nu, self.dt, self.steps)
            )
            errors.append(
                burgers.window_error(burgers.relative_errors(fields, self.fom))
            )
        self.assertTrue(np.all(np.diff(errors) < 0), errors)
        self.assertLess(errors[-1], 1e-4)

    def test_offline_operators_match_projected_nonlinear_term(self):
        r = 6
        ops = burgers.build_rom(self.pod.mean, self.pod.modes[:, :r], self.grid)
        a = np.random.default_rng(1).normal(size=r)
        u = ops.mean + ops.modes @ a
        dx = self.grid.dx
        direct = ops.modes.T @ (
            self.nu * burgers.second_derivative(u, dx)
            - u * burgers.first_derivative(u, dx)
        )
        reduced = self.nu * (ops.diffusion_mean + ops.diffusion @ a) - (
            ops.convection_mean
            + ops.convection_linear @ a
            + ops.convection_quadratic @ np.outer(a, a).ravel()
        )
        np.testing.assert_allclose(reduced, direct, rtol=1e-10, atol=1e-10)

    def test_difference_operators_are_second_order(self):
        errors = []
        for n in (50, 100, 200):
            grid = burgers.Grid(n)
            u = np.sin(np.pi * grid.x)
            errors.append(
                np.abs(
                    burgers.first_derivative(u, grid.dx)
                    - np.pi * np.cos(np.pi * grid.x)
                ).max()
            )
        orders = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(orders, 2.0, atol=0.1)


class ReducedBasisThermalBlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = thermal.build_model(n_cells=16, blocks=2)
        cls.operators = thermal.affine_operators(cls.model)
        cls.rng = np.random.default_rng(3)

    def test_affine_assembly_equals_direct_assembly(self):
        for mu in thermal.sample_parameters(self.rng, 5, 3):
            difference = thermal.assemble_affine(
                self.operators, mu
            ) - thermal.assemble_direct(self.model, mu)
            self.assertLess(abs(difference).max(), 1e-12)

    def test_uniform_conductivity_gives_linear_profile(self):
        # Unit flux at y = 0, u = 0 at y = 1, k = 1: u = 1 - y, reproduced by P1.
        u = thermal.truth_solve(self.model, self.operators, np.ones(3))
        y = self.model.points[self.model.free, 1]
        np.testing.assert_allclose(u, 1.0 - y, atol=1e-12)

    def test_coercivity_lower_bound_is_rigorous(self):
        inner = sum(self.operators).toarray()
        for mu in thermal.sample_parameters(self.rng, 5, 3):
            matrix = thermal.assemble_affine(self.operators, mu).toarray()
            alpha = eigh(matrix, inner, eigvals_only=True).min()
            self.assertLessEqual(thermal.coercivity_lower_bound(mu)[0], alpha + 1e-12)

    def test_stable_residual_norm_matches_direct_dual_norm(self):
        rb, operators, _, _, test = thermal.greedy(self.model, n_max=6, tolerance=0.0)
        a = rb.solve(test[:5])
        estimate = rb.residual_norm(test[:5], a)
        lu = spla.splu(rb.inner)
        for k, mu in enumerate(test[:5]):
            residual = self.model.load - thermal.assemble_affine(operators, mu) @ (
                rb.basis @ a[k]
            )
            direct = np.sqrt(residual @ lu.solve(residual))
            self.assertAlmostEqual(estimate[k] / direct, 1.0, places=8)

    def test_error_bound_is_rigorous_and_decays(self):
        _, _, history, _, _ = thermal.greedy(self.model, n_max=16, tolerance=0.0)
        self.assertGreaterEqual(history["eta_min"].min(), 1.0)
        self.assertGreaterEqual(history["output_eta_min"].min(), 1.0)
        # Effectivity never exceeds gamma_UB / alpha_LB = 10 / 0.1.
        self.assertLessEqual(history["eta_max"].max(), 100.0)
        self.assertLess(
            history["error"][-1], 1e-3 * history["error"][0], history["error"]
        )


if __name__ == "__main__":
    unittest.main()
