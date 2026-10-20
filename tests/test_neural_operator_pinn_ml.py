"""Check the PINN and Fourier neural operator examples against exact solutions."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_algorithm(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / "algorithms" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pinn = load_algorithm("pinn_boundary_layer")
fno = load_algorithm("fourier_neural_operator_1d")


class PINNBoundaryLayerTests(unittest.TestCase):
    def setUp(self):
        self.theta = pinn.initial_parameters(np.random.default_rng(3))
        self.x = np.linspace(0.0, 1.0, 9)

    def test_exact_solution_satisfies_problem(self):
        eps = 0.05
        x = np.linspace(0.0, 1.0, 2001)
        u = pinn.exact_solution(x, eps)
        self.assertAlmostEqual(u[0], 0.0, places=14)
        self.assertAlmostEqual(u[-1], 1.0, places=14)
        h = x[1] - x[0]
        du = (u[2:] - u[:-2]) / (2 * h)
        d2u = (u[2:] - 2 * u[1:-1] + u[:-2]) / h**2
        self.assertLess(np.max(np.abs(eps * d2u - du)), 5e-2)

    def test_input_derivatives_match_finite_differences(self):
        h = 1e-5
        u, du, d2u = pinn.network(self.theta, self.x)
        u_plus = pinn.network(self.theta, self.x + h)[0]
        u_minus = pinn.network(self.theta, self.x - h)[0]
        np.testing.assert_allclose(du, (u_plus - u_minus) / (2 * h), atol=1e-6)
        np.testing.assert_allclose(
            d2u, (u_plus - 2 * u + u_minus) / h**2, rtol=1e-4, atol=1e-3
        )

    def test_parameter_jacobian_matches_finite_differences(self):
        eps, h = 0.05, 1e-6
        jac = pinn.residual_jacobian(self.theta, self.x, eps)
        numeric = np.empty_like(jac)
        for i in range(self.theta.size):
            step = np.zeros_like(self.theta)
            step[i] = h
            numeric[:, i] = (
                pinn.residual_vector(self.theta + step, self.x, eps)
                - pinn.residual_vector(self.theta - step, self.x, eps)
            ) / (2 * h)
        np.testing.assert_allclose(jac, numeric, atol=1e-5 * np.abs(jac).max())

    def test_moderate_epsilon_is_accurate(self):
        result = pinn.train_pinn(0.1)
        x = np.linspace(0.0, 1.0, 2001)
        error = pinn.network(result.theta, x)[0] - pinn.exact_solution(x, 0.1)
        self.assertLess(np.max(np.abs(error)), 1e-4)
        self.assertLess(result.loss_history[-1], 1e-8)
        self.assertTrue(np.all(np.diff(result.loss_history) <= 0))

    def test_thin_layer_failure_shows_in_dense_residual(self):
        # The collocation loss is tiny, yet the residual between points is not.
        result = pinn.train_pinn(0.01)
        x = np.linspace(0.0, 1.0, 4001)
        self.assertLess(result.loss_history[-1], 1e-6)
        self.assertGreater(np.max(np.abs(pinn.pde_residual(result.theta, x, 0.01))), 1)


class FourierNeuralOperatorTests(unittest.TestCase):
    def setUp(self):
        self.f_train, self.u_train = fno.make_training_set(np.random.default_rng(0))

    def test_synthesis_is_resolution_independent(self):
        coef = fno.random_coefficients(np.random.default_rng(1), 1, 10)
        coarse = fno.synthesize(coef, 32)[0]
        fine = fno.synthesize(coef, 128)[0]
        np.testing.assert_allclose(coarse, fine[::4], atol=1e-12)

    def test_noise_free_fit_recovers_exact_multiplier(self):
        rng = np.random.default_rng(2)
        coef = fno.random_coefficients(rng, 20, 31)
        f = fno.synthesize(coef, 64)
        u = fno.synthesize(fno.solve_exact(coef), 64)
        weights = fno.fit_spectral_weights(f, u, 31)
        np.testing.assert_allclose(
            weights, fno.exact_multiplier(np.arange(32)), rtol=1e-10, atol=1e-14
        )

    def test_noisy_fit_matches_low_modes(self):
        weights = fno.fit_spectral_weights(self.f_train, self.u_train, 16)
        exact = fno.exact_multiplier(np.arange(17))
        self.assertLess(np.max(np.abs(weights - exact) / exact), 1e-2)

    def test_zero_shot_error_is_small_and_grid_independent(self):
        weights = fno.fit_spectral_weights(self.f_train, self.u_train, 16)
        test_coef = fno.random_coefficients(np.random.default_rng(5), 1, 48)
        errors = fno.zero_shot_errors(weights, test_coef)
        self.assertLess(errors.max(), 1e-2)
        np.testing.assert_allclose(errors, errors[0], rtol=1e-8)

    def test_more_modes_reduce_error(self):
        test_coef = fno.random_coefficients(np.random.default_rng(5), 1, 48)
        errors = [
            fno.zero_shot_errors(
                fno.fit_spectral_weights(self.f_train, self.u_train, k), test_coef
            )[0]
            for k in (4, 8, 16)
        ]
        self.assertTrue(errors[0] > errors[1] > errors[2])


if __name__ == "__main__":
    unittest.main()
