"""Strength-of-materials scripts: Mohr's circle, Kirsch, torsion, axial bars, Ramberg-Osgood."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(category, name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mohr = load_example("algorithms", "materials_mohr_circle")
axial = load_example("algorithms", "materials_axial_bar_fem")
curves = load_example("plots", "materials_stress_strain_curves")
kirsch = load_example("plots", "materials_kirsch_hole")
torsion = load_example("plots", "materials_torsion_shear_distribution")

STATES = [
    (80.0, -40.0, 50.0),
    (60.0, 20.0, 25.0),
    (-30.0, 10.0, -45.0),
    (0.0, 0.0, 70.0),
]


class MohrCircleTests(unittest.TestCase):
    def test_invariants_are_preserved_by_rotation(self):
        for sx, sy, txy in STATES:
            for theta in np.linspace(-np.pi, np.pi, 13):
                a, b, c = mohr.transform(sx, sy, txy, theta)
                self.assertAlmostEqual(a + b, sx + sy, places=10)
                self.assertAlmostEqual(a * b - c**2, sx * sy - txy**2, places=8)

    def test_principal_sum_and_direction(self):
        for sx, sy, txy in STATES:
            s1, s2, theta_p = mohr.principal(sx, sy, txy)
            self.assertAlmostEqual(s1 + s2, sx + sy, places=10)
            a, b, c = mohr.transform(sx, sy, txy, theta_p)
            self.assertAlmostEqual(c, 0.0, places=10)
            self.assertAlmostEqual(a, s1, places=10)
            self.assertAlmostEqual(b, s2, places=10)

    def test_principal_stresses_are_eigenvalues(self):
        for sx, sy, txy in STATES:
            s1, s2, _ = mohr.principal(sx, sy, txy)
            eig = np.linalg.eigvalsh(np.array([[sx, txy], [txy, sy]]))
            np.testing.assert_allclose([s2, s1], eig, atol=1e-10)

    def test_max_shear_plane(self):
        for sx, sy, txy in STATES:
            s1, s2, _ = mohr.principal(sx, sy, txy)
            tau_max, theta_s, tau_abs = mohr.max_shear(sx, sy, txy)
            a, b, c = mohr.transform(sx, sy, txy, theta_s)
            self.assertAlmostEqual(c, tau_max, places=10)
            self.assertAlmostEqual(a, 0.5 * (sx + sy), places=10)
            self.assertGreaterEqual(tau_abs, tau_max - 1e-12)
        # Both principal stresses positive: out-of-plane shear governs.
        _, _, tau_abs = mohr.max_shear(60.0, 20.0, 25.0)
        self.assertAlmostEqual(tau_abs, 0.5 * (40.0 + np.hypot(20.0, 25.0)), places=10)


class KirschTests(unittest.TestCase):
    def test_peak_hoop_stress_is_three(self):
        _, s_tt, _ = kirsch.kirsch_polar(1.0, np.pi / 2.0)
        self.assertAlmostEqual(s_tt, 3.0, places=12)
        _, s_tt, _ = kirsch.kirsch_polar(1.0, 0.0)
        self.assertAlmostEqual(s_tt, -1.0, places=12)
        theta = np.linspace(0.0, 2.0 * np.pi, 721)
        _, edge, _ = kirsch.kirsch_polar(1.0, theta)
        self.assertAlmostEqual(edge.max(), 3.0, places=10)

    def test_hole_edge_is_traction_free(self):
        theta = np.linspace(0.0, 2.0 * np.pi, 37)
        s_rr, _, t_rt = kirsch.kirsch_polar(1.0, theta)
        np.testing.assert_allclose(s_rr, 0.0, atol=1e-12)
        np.testing.assert_allclose(t_rt, 0.0, atol=1e-12)

    def test_far_field_is_uniaxial(self):
        s_xx, s_yy, t_xy = kirsch.kirsch_cartesian(
            np.array([300.0, 0.0]), np.array([0.0, 300.0])
        )
        np.testing.assert_allclose(s_xx, 1.0, atol=1e-4)
        np.testing.assert_allclose(s_yy, 0.0, atol=1e-4)
        np.testing.assert_allclose(t_xy, 0.0, atol=1e-4)

    def test_ligament_formula_matches_field(self):
        r = np.array([1.0, 1.5, 2.0, 4.0])
        s_xx, _, _ = kirsch.kirsch_cartesian(np.zeros_like(r), r)
        np.testing.assert_allclose(s_xx, kirsch.ligament_stress(r), rtol=1e-12)

    def test_ligament_force_balances_remote_load(self):
        # The ligament a < y < R carries the remote load sigma R of the unholed plate.
        y = np.linspace(1.0, 2000.0, 400001)
        force = np.trapezoid(kirsch.ligament_stress(y), y)
        self.assertAlmostEqual(force, 2000.0, delta=1e-2)


class TorsionTests(unittest.TestCase):
    def test_circular_shaft_formulas(self):
        d = 0.030
        torque = 318.3
        j = torsion.polar_moment(d)
        self.assertAlmostEqual(j, np.pi * d**4 / 32.0, places=18)
        tau = torsion.shaft_shear(torque, d / 2, d)
        self.assertAlmostEqual(tau, 16.0 * torque / (np.pi * d**3), delta=1e-6)

    def test_hollow_shaft_ratios(self):
        ratio = torsion.polar_moment(1.0, 0.8) / torsion.polar_moment(1.0)
        self.assertAlmostEqual(ratio, 1.0 - 0.8**4, places=12)

    def test_rectangle_coefficients(self):
        table = {
            1.0: (0.208, 0.141),
            2.0: (0.246, 0.229),
            4.0: (0.282, 0.281),
            10.0: (0.312, 0.312),
        }
        for aspect, (alpha_ref, beta_ref) in table.items():
            alpha, beta = torsion.rectangle_coefficients(aspect)
            self.assertAlmostEqual(float(alpha), alpha_ref, delta=1.5e-3)
            self.assertAlmostEqual(float(beta), beta_ref, delta=1.5e-3)
        alpha, beta = torsion.rectangle_coefficients(1000.0)
        self.assertAlmostEqual(float(beta), 1.0 / 3.0, delta=1e-3)

    def test_thin_tube_matches_thin_circle(self):
        # Bredt-Batho for a thin circular tube agrees with T rho / J as t -> 0.
        r_m, t, torque = 0.05, 1e-4, 100.0
        tau_bredt = torque / (2.0 * np.pi * r_m**2 * t)
        j = torsion.polar_moment(2 * r_m + t, 2 * r_m - t)
        tau_exact = torsion.shaft_shear(torque, r_m, 2 * r_m + t, 2 * r_m - t)
        self.assertAlmostEqual(tau_bredt / tau_exact, 1.0, delta=1e-5)
        self.assertGreater(j, 0.0)

    def test_tube_shear_flow(self):
        q, stresses, twist = torsion.tube_properties()
        self.assertAlmostEqual(q, 1000.0 / (2 * 0.1 * 0.05), places=8)
        self.assertAlmostEqual(stresses["right"], q / 2e-3, places=6)
        self.assertGreater(twist, 0.0)


class AxialBarTests(unittest.TestCase):
    def test_fe_matches_compatibility_solution(self):
        x, ea, alpha = axial.build_mesh([axial.STEEL, axial.ALUMINIUM], 3)
        for load, dt in ((60e3, 0.0), (0.0, 30.0), (60e3, 30.0), (-25e3, -40.0)):
            u, n, reactions = axial.solve_bar(x, ea, alpha, dt, {3: load})
            n_ab, n_bc, u_b = axial.hand_solution(load, dt)
            np.testing.assert_allclose(n[:3], n_ab, rtol=1e-10, atol=1e-6)
            np.testing.assert_allclose(n[3:], n_bc, rtol=1e-10, atol=1e-6)
            self.assertAlmostEqual(u[3], u_b, delta=1e-13)
            self.assertAlmostEqual(reactions.sum() + load, 0.0, delta=1e-6)

    def test_free_thermal_expansion_has_no_stress(self):
        x, ea, alpha = axial.build_mesh([axial.STEEL], 4)
        u, n, _ = axial.solve_bar(x, ea, alpha, 50.0, fixed=(0,))
        np.testing.assert_allclose(n, 0.0, atol=1e-6)
        self.assertAlmostEqual(
            u[-1], axial.STEEL[3] * 50.0 * axial.STEEL[0], delta=1e-14
        )

    def test_fully_constrained_bar_stress(self):
        x, ea, alpha = axial.build_mesh([axial.ALUMINIUM], 2)
        _, n, _ = axial.solve_bar(x, ea, alpha, 60.0)
        sigma = n / axial.ALUMINIUM[1]
        np.testing.assert_allclose(sigma, -70e9 * 23e-6 * 60.0, rtol=1e-12)

    def test_taper_converges_at_second_order(self):
        exact = axial.taper_exact()
        errors = [abs(axial.taper_fem(m) - exact) for m in (8, 16, 32)]
        orders = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(orders, 2.0, atol=0.05)

    def test_strain_energy_equals_external_work(self):
        x, ea, alpha = axial.build_mesh([axial.STEEL, axial.ALUMINIUM], 4)
        u, _, _ = axial.solve_bar(x, ea, alpha, 0.0, {4: 60e3})
        self.assertAlmostEqual(
            axial.strain_energy(x, ea, u), 0.5 * 60e3 * u[4], places=8
        )


class RambergOsgoodTests(unittest.TestCase):
    def test_offset_yield_equals_parameter(self):
        for n in (5.0, 8.0, 15.0):
            self.assertAlmostEqual(
                curves.offset_yield(200e3, 350.0, n), 350.0, places=6
            )

    def test_considere_condition_at_uts(self):
        _, uts, eps_t, sig_t = curves.ultimate_point()
        h = 1e-3 * sig_t
        slope = (
            2.0
            * h
            / (
                curves.ramberg_osgood_strain(sig_t + h)
                - curves.ramberg_osgood_strain(sig_t - h)
            )
        )
        self.assertAlmostEqual(slope / sig_t, 1.0, delta=5e-3)
        self.assertAlmostEqual(uts, sig_t * np.exp(-eps_t), delta=1e-9 * uts)

    def test_engineering_true_conversion(self):
        eps_e, sig_e = curves.engineering_from_true(np.log(1.2), 600.0)
        self.assertAlmostEqual(eps_e, 0.2, places=12)
        self.assertAlmostEqual(sig_e, 500.0, places=10)

    def test_toughness_of_linear_curve(self):
        eps = np.linspace(0.0, 0.0025, 11)
        self.assertAlmostEqual(curves.toughness(eps, 120e3 * eps), 0.375, places=12)


if __name__ == "__main__":
    unittest.main()
