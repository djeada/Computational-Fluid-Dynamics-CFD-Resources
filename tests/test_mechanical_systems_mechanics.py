"""Mechanical systems: four-bar and slider-crank kinematics, gear geometry,
Jeffcott rotor and Campbell diagram, journal-bearing Reynolds solver, pump
affinity laws."""

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


fourbar = load_example("algorithms", "mechanisms_four_bar_linkage")
rotor = load_example("algorithms", "rotor_jeffcott_campbell")
bearing = load_example("algorithms", "bearings_journal_reynolds")
pump = load_example("plots", "hydraulics_pump_system_curve")
gears = load_example("plots", "gears_involute_profile")


class FourBarTests(unittest.TestCase):
    def setUp(self):
        self.theta2 = np.linspace(0.0, 2 * np.pi, 181)
        self.theta3, self.theta4 = fourbar.solve_position(self.theta2)

    def test_loop_closes_at_every_crank_angle(self):
        a, b, c, d = fourbar.CRANK, fourbar.COUPLER, fourbar.ROCKER, fourbar.GROUND
        for branch in (-1, +1):
            t3, t4 = fourbar.solve_position(self.theta2, branch=branch)
            loop = (
                a * np.exp(1j * self.theta2)
                + b * np.exp(1j * t3)
                - c * np.exp(1j * t4)
                - d
            )
            np.testing.assert_allclose(np.abs(loop), 0.0, atol=1e-12)

    def test_freudenstein_equation_holds(self):
        k1, k2, k3 = fourbar.freudenstein_constants(
            fourbar.CRANK, fourbar.COUPLER, fourbar.ROCKER, fourbar.GROUND
        )
        lhs = k1 * np.cos(self.theta4) - k2 * np.cos(self.theta2) + k3
        np.testing.assert_allclose(lhs, np.cos(self.theta2 - self.theta4), atol=1e-12)

    def test_velocity_and_acceleration_match_finite_differences(self):
        w2, h = fourbar.CRANK_SPEED, 1e-5
        t2 = np.array([0.3, 1.7, 3.0, 4.4, 5.9])
        t3, t4 = fourbar.solve_position(t2)
        w3, w4 = fourbar.solve_velocity(t2, t3, t4, w2)
        al3, al4 = fourbar.solve_acceleration(t2, t3, t4, w2, w3, w4)
        tp3, tp4 = fourbar.solve_position(t2 + h)
        tm3, tm4 = fourbar.solve_position(t2 - h)
        # Constant crank speed: d/dt = w2 d/dtheta2.
        np.testing.assert_allclose(w4, w2 * (tp4 - tm4) / (2 * h), rtol=1e-6)
        np.testing.assert_allclose(w3, w2 * (tp3 - tm3) / (2 * h), rtol=1e-6)
        np.testing.assert_allclose(
            al4, w2**2 * (tp4 - 2 * t4 + tm4) / h**2, rtol=1e-3, atol=1e-3
        )
        np.testing.assert_allclose(
            al3, w2**2 * (tp3 - 2 * t3 + tm3) / h**2, rtol=1e-3, atol=1e-3
        )

    def test_transmission_angle_matches_law_of_cosines(self):
        mu = fourbar.transmission_angle(self.theta3, self.theta4)
        np.testing.assert_allclose(
            mu, fourbar.transmission_angle_closed_form(self.theta2), atol=1e-10
        )

    def test_grashof_classification(self):
        cls = fourbar.grashof_class
        self.assertEqual(cls(120, 40, 110, 90), "crank-rocker")
        self.assertEqual(cls(40, 90, 110, 120), "double-crank")
        self.assertEqual(cls(110, 90, 40, 120), "double-rocker (Grashof)")
        self.assertEqual(cls(100, 55, 70, 80), "triple-rocker (non-Grashof)")
        self.assertEqual(cls(100, 50, 100, 50), "change-point")

    def test_crank_rocker_rocker_extremes_are_the_toggle_positions(self):
        t_ext, t_fold, _ = fourbar.limit_positions()
        t3, t4 = fourbar.solve_position(np.array([t_ext, t_fold]))
        # At a toggle position crank and coupler are collinear: rocker speed is zero.
        w3, w4 = fourbar.solve_velocity(np.array([t_ext, t_fold]), t3, t4, 1.0)
        np.testing.assert_allclose(w4, 0.0, atol=1e-9)

    def test_slider_crank_matches_differentiated_position_and_tdc_value(self):
        omega, h = 314.159, 1e-5
        theta = np.array([0.4, 1.0, 2.5])
        x, v, acc = fourbar.slider_crank(theta, omega)
        xp, _, _ = fourbar.slider_crank(theta + h, omega)
        xm, _, _ = fourbar.slider_crank(theta - h, omega)
        np.testing.assert_allclose(v, omega * (xp - xm) / (2 * h), rtol=1e-7)
        np.testing.assert_allclose(acc, omega**2 * (xp - 2 * x + xm) / h**2, rtol=1e-4)
        r, rod = fourbar.SC_CRANK, fourbar.SC_ROD
        _, _, a_tdc = fourbar.slider_crank(np.array([0.0]), omega)
        self.assertAlmostEqual(a_tdc[0], -r * omega**2 * (1 + r / rod), places=6)


class GearTests(unittest.TestCase):
    def test_involute_point_lies_at_unwound_string_length(self):
        rb, t = 0.05, np.linspace(0.1, 1.5, 7)
        x, y = gears.involute_curve(rb, t)
        tangent = np.c_[rb * np.cos(t), rb * np.sin(t)]
        np.testing.assert_allclose(
            np.hypot(x - tangent[:, 0], y - tangent[:, 1]), rb * t, rtol=1e-12
        )

    def test_tooth_is_half_the_circular_pitch_on_the_pitch_circle(self):
        n = 24
        r = gears.gear_geometry(n)["r"]
        self.assertAlmostEqual(
            2 * gears.half_tooth_angle(r, n) * r, np.pi * gears.MODULE / 2
        )

    def test_contact_ratio_of_worked_example(self):
        _, ratio = gears.contact_ratio(20, 60)
        self.assertAlmostEqual(ratio, 1.67, places=2)

    def test_minimum_teeth_without_interference(self):
        phi = np.radians(20.0)
        self.assertEqual(int(np.ceil(gears.min_pinion_teeth(np.inf, phi))), 18)
        self.assertEqual(int(np.ceil(gears.min_pinion_teeth(1.0, phi))), 13)
        self.assertEqual(
            int(np.ceil(gears.min_pinion_teeth(np.inf, np.radians(14.5)))), 32
        )


class JeffcottTests(unittest.TestCase):
    def test_light_damping_peaks_at_critical_speed_with_90_degree_phase(self):
        zeta = 0.02
        s = np.linspace(0.5, 1.5, 200_001)
        amp, phase = rotor.unbalance_response(s, zeta)
        self.assertAlmostEqual(s[np.argmax(amp)], 1.0, delta=1e-3)
        _, ph1 = rotor.unbalance_response(1.0, zeta)
        self.assertAlmostEqual(np.degrees(ph1), 90.0, places=10)
        a1, _ = rotor.unbalance_response(1.0, zeta)
        self.assertAlmostEqual(a1, 1 / (2 * zeta), places=10)

    def test_peak_formula_and_high_speed_self_centring(self):
        s_pk, a_pk = rotor.peak_response(0.1)
        amp, _ = rotor.unbalance_response(
            np.array([s_pk - 1e-4, s_pk, s_pk + 1e-4]), 0.1
        )
        self.assertTrue(amp[1] >= amp[0] and amp[1] >= amp[2])
        self.assertAlmostEqual(amp[1], a_pk, places=10)
        amp_hi, ph_hi = rotor.unbalance_response(100.0, 0.1)
        self.assertAlmostEqual(amp_hi, 1.0, places=3)
        self.assertGreater(np.degrees(ph_hi), 179.0)

    def test_time_integration_reaches_steady_unbalance_response(self):
        for s in (0.7, 1.0, 1.6):
            amp, lag = rotor.integrate_response(s, 0.1)
            amp_ref, lag_ref = rotor.unbalance_response(s, 0.1)
            self.assertAlmostEqual(amp, amp_ref, places=4)
            self.assertAlmostEqual(lag, lag_ref, places=4)


class CampbellTests(unittest.TestCase):
    def setUp(self):
        self.m, self.ip, self.id, self.k = rotor.overhung_rotor()

    def test_non_rotating_frequencies_are_generalised_eigenvalues(self):
        w = rotor.whirl_frequencies(0.0, self.m, self.ip, self.id, self.k)
        mass = np.diag([self.m, self.id])
        ref = np.sqrt(np.sort(np.linalg.eigvals(np.linalg.solve(mass, self.k)).real))
        np.testing.assert_allclose(w[2:], ref, rtol=1e-10)
        np.testing.assert_allclose(-w[:2][::-1], ref, rtol=1e-10)

    def test_gyroscopic_stiffening_splits_forward_and_backward_whirl(self):
        w = rotor.whirl_frequencies(500.0, self.m, self.ip, self.id, self.k)
        w0 = rotor.whirl_frequencies(0.0, self.m, self.ip, self.id, self.k)
        self.assertGreater(w[3], w0[3])  # forward mode stiffened
        self.assertLess(-w[0], w0[3])  # backward mode softened

    def test_critical_speeds_lie_on_the_synchronous_line(self):
        for direction in (+1, -1):
            for spin in rotor.critical_speeds(
                self.m, self.ip, self.id, self.k, direction
            ):
                w = rotor.whirl_frequencies(spin, self.m, self.ip, self.id, self.k)
                self.assertAlmostEqual(
                    np.min(np.abs(w - direction * spin)) / spin, 0.0, places=8
                )

    def test_thin_disk_has_a_single_forward_critical_speed(self):
        self.assertGreater(self.ip, self.id)
        forward = rotor.critical_speeds(self.m, self.ip, self.id, self.k, +1)
        self.assertEqual(forward.size, 1)


class ReynoldsBearingTests(unittest.TestCase):
    def test_full_sommerfeld_solution_matches_closed_form(self):
        for eps in (0.2, 0.5, 0.8):
            theta, p = bearing.solve_long(eps, n_theta=288, cavitation=False)
            exact = bearing.sommerfeld_pressure(theta, eps)
            self.assertLess(np.abs(p - exact).max() / exact.max(), 5e-4)
            s, phi = bearing.sommerfeld_and_attitude(theta, p)
            self.assertAlmostEqual(
                s / bearing.sommerfeld_number_full(eps), 1.0, places=3
            )
            self.assertAlmostEqual(phi, 90.0, places=2)

    def test_second_order_convergence(self):
        eps = 0.6
        errors = []
        for n in (72, 144, 288):
            theta, p = bearing.solve_long(eps, n_theta=n, cavitation=False)
            errors.append(np.abs(p - bearing.sommerfeld_pressure(theta, eps)).max())
        orders = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(orders, 2.0, atol=0.15)

    def test_cavitating_solution_satisfies_complementarity(self):
        theta, p = bearing.solve_long(0.6)
        self.assertGreaterEqual(p.min(), -1e-10)
        a, b, _, _ = bearing.assemble(0.6, bearing.N_THETA)
        a, b = bearing.fix_supply_line(a, b, bearing.N_THETA, 1)
        residual = a @ p - b
        pressurised = p > 1e-8
        np.testing.assert_allclose(residual[pressurised], 0.0, atol=1e-8)
        self.assertGreaterEqual(residual[~pressurised].min(), -1e-8)

    def test_finite_bearing_reproduces_raimondi_boyd_table(self):
        for eps, s_rb, phi_rb in bearing.RAIMONDI_BOYD_LD1[[1, 3, 4]]:
            theta, zeta, p = bearing.solve_finite(eps)
            s, phi = bearing.sommerfeld_and_attitude(theta, p, 2.0, zeta[1] - zeta[0])
            self.assertAlmostEqual(s / s_rb, 1.0, delta=0.02)
            self.assertAlmostEqual(phi, phi_rb, delta=1.0)


class PumpTests(unittest.TestCase):
    def test_affinity_laws_scale_flow_head_and_power(self):
        q0, n0, n1 = 0.02, pump.RATED_RPM, 1100.0
        r = n1 / n0
        h0 = pump.pump_head(q0, n0)
        self.assertAlmostEqual(pump.pump_head(q0 * r, n1), h0 * r**2, places=10)
        self.assertAlmostEqual(
            pump.pump_efficiency(q0 * r, n1), pump.pump_efficiency(q0, n0)
        )
        p0 = pump.shaft_power(q0, h0, pump.pump_efficiency(q0, n0))
        p1 = pump.shaft_power(q0 * r, h0 * r**2, pump.pump_efficiency(q0 * r, n1))
        self.assertAlmostEqual(p1 / p0, r**3, places=10)

    def test_operating_point_is_on_both_curves(self):
        k = pump.system_coefficient()
        for rpm in pump.SPEEDS_RPM:
            q, h = pump.operating_point(rpm, k)
            self.assertAlmostEqual(pump.pump_head(q, rpm), h, places=10)
            self.assertAlmostEqual(pump.system_head(q, k), h, places=10)

    def test_speed_control_needs_less_power_than_throttling(self):
        _, p_thr, p_spd, rpm = pump.flow_reduction(
            pump.system_coefficient(), [0.6, 0.8, 1.0]
        )
        self.assertTrue(np.all(p_spd[:2] < p_thr[:2]))
        self.assertAlmostEqual(p_spd[2], p_thr[2], places=6)
        self.assertAlmostEqual(rpm[2], pump.RATED_RPM, places=6)


if __name__ == "__main__":
    unittest.main()
