"""Control scripts: second-order specifications, root locus, margins and PID tuning."""

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


second = load_example("algorithms", "control_second_order_response")
locus = load_example("algorithms", "control_root_locus")
bode = load_example("algorithms", "control_bode_nyquist")
pid = load_example("algorithms", "control_pid_tuning")


class SecondOrderResponseTests(unittest.TestCase):
    def test_overshoot_formula_matches_simulation(self):
        for zeta in (0.1, 0.3, 0.5, 0.7, 0.9):
            t, y = second.step_response(zeta)
            m = second.step_metrics(t, y)
            expected = second.overshoot_formula([zeta])[0]
            self.assertAlmostEqual(m["overshoot"], expected, delta=1e-4)
            self.assertAlmostEqual(
                m["peak_time"], second.peak_time_formula(zeta), delta=2e-3
            )

    def test_no_overshoot_for_critical_and_overdamped(self):
        for zeta in (1.0, 2.0):
            t, y = second.step_response(zeta)
            self.assertLess(second.step_metrics(t, y)["overshoot"], 1e-6)

    def test_inverse_overshoot_relation(self):
        for zeta in (0.2, 0.456, 0.69):
            mp = second.overshoot_formula([zeta])[0]
            self.assertAlmostEqual(second.zeta_from_overshoot(mp), zeta, places=10)

    def test_poles_have_requested_damping(self):
        p = second.poles(0.4, omega_n=5.0)
        np.testing.assert_allclose(np.abs(p), 5.0)
        np.testing.assert_allclose(-p.real / np.abs(p), 0.4)


class RootLocusTests(unittest.TestCase):
    def test_routh_critical_gain_equals_locus_crossing(self):
        k_routh = locus.routh_critical_gain()
        k_locus = locus.locus_crossing_gain()
        self.assertAlmostEqual(k_routh, 70.0, places=5)
        self.assertAlmostEqual(k_locus, k_routh, places=5)
        poles = locus.closed_loop_poles(k_routh)
        omega = locus.crossing_frequency(k_routh)
        self.assertAlmostEqual(omega, np.sqrt(10.0), places=5)
        self.assertAlmostEqual(np.max(np.abs(poles.imag)), omega, places=4)

    def test_routh_sign_changes_count_rhp_roots(self):
        for coeffs in ([1, 2, 3, 4, 5], [1, 1, 2, 2, 3, 5], [1, 6, 11, 66]):
            table = locus.routh_array(coeffs)
            n_rhp = int(np.sum(np.roots(coeffs).real > 1e-9))
            self.assertEqual(locus.sign_changes(table[:, 0]), n_rhp)

    def test_routh_row_of_zeros_uses_auxiliary_polynomial(self):
        # (s + 2)(s^2 + 4): the s^1 row vanishes; auxiliary 2 s^2 + 8.
        table = locus.routh_array([1, 2, 4, 8])
        np.testing.assert_allclose(table[2], [4.0, 0.0])
        self.assertEqual(locus.sign_changes(table[:, 0]), 0)

    def test_asymptotes_and_breakaway(self):
        centroid, angles = locus.asymptotes()
        self.assertAlmostEqual(centroid, -7.0 / 3.0)
        np.testing.assert_allclose(angles, [60.0, 180.0, 300.0])
        ((s_b, k_b),) = locus.breakaway_points()
        self.assertAlmostEqual(s_b, (-14 + np.sqrt(76)) / 6, places=10)
        self.assertAlmostEqual(k_b, -(s_b**3 + 7 * s_b**2 + 10 * s_b), places=10)
        roots = locus.closed_loop_poles(k_b)
        self.assertLess(np.min(np.abs(roots - s_b)), 1e-3)  # double root

    def test_damping_line_gain(self):
        k = locus.damping_line_gain(0.5)
        p = locus.closed_loop_poles(k)
        q = p[p.imag > 0][0]
        self.assertAlmostEqual(-q.real / abs(q), 0.5, places=6)


class BodeNyquistTests(unittest.TestCase):
    def test_bode_margins_match_nyquist_crossings(self):
        for delay in (0.0, bode.DELAY):
            m = bode.bode_margins(delay)
            w_c, re_c = bode.nyquist_real_axis_crossing(delay)
            self.assertAlmostEqual(w_c, m["w_pc"], delta=1e-4 * m["w_pc"])
            self.assertAlmostEqual(-1.0 / re_c, m["gm"], delta=1e-4 * m["gm"])
            w_gc, l_gc = bode.nyquist_unit_circle_crossing(delay)
            pm_nyquist = 180.0 + np.degrees(np.angle(l_gc))
            self.assertAlmostEqual(w_gc, m["w_gc"], delta=1e-3 * m["w_gc"])
            self.assertAlmostEqual(pm_nyquist, m["pm"], delta=0.05)

    def test_delay_free_margins_are_analytic(self):
        # Phase crossover of 1/(s(2s+1)(0.5s+1)) at w^2 = 1/(2 * 0.5) = 1.
        m = bode.bode_margins(0.0)
        self.assertAlmostEqual(m["w_pc"], 1.0, places=8)
        k = bode.loop_gain()
        expected_gm = (2.0 + 0.5) / (2.0 * 0.5 * k)  # (tau_p + tau_m) / (tau_p tau_m K)
        self.assertAlmostEqual(m["gm"], expected_gm, places=8)

    def test_delay_margin_destabilises(self):
        m = bode.bode_margins(0.0)
        just_stable = bode.bode_margins(0.99 * m["delay_margin"])
        unstable = bode.bode_margins(1.01 * m["delay_margin"])
        self.assertGreater(just_stable["pm"], 0.0)
        self.assertLess(unstable["pm"], 0.0)

    def test_encirclements_follow_gain_margin(self):
        for delay in (0.0, bode.DELAY):
            gm = bode.bode_margins(delay)["gm"]
            k = bode.loop_gain()
            self.assertEqual(bode.clockwise_encirclements(delay, k=0.9 * gm * k), 0)
            self.assertEqual(bode.clockwise_encirclements(delay, k=1.1 * gm * k), 2)

    def test_sensitivities_sum_to_one(self):
        loop = bode.loop_response(bode.OMEGA, bode.DELAY)
        s = 1.0 / (1.0 + loop)
        np.testing.assert_allclose(s + loop * s, 1.0, atol=1e-12)


class PidTuningTests(unittest.TestCase):
    def test_closed_loops_reach_setpoint_and_reject_load(self):
        for gains in pid.tunings().values():
            _, y, _, _ = pid.simulate(gains)
            self.assertLess(abs(y[-1] - pid.SETPOINT_STEP), 1e-4)
            _, y_load, _, _ = pid.simulate(gains, setpoint=0.0, load=pid.LOAD_STEP)
            self.assertLess(abs(y_load[-1]), 1e-4)

    def test_saturated_loop_still_reaches_setpoint(self):
        for anti_windup in (False, True):
            _, y, _, u = pid.simulate(
                pid.simc_pi(), u_limits=(pid.U_MIN, pid.U_MAX), anti_windup=anti_windup
            )
            self.assertLess(abs(y[-1] - pid.SETPOINT_STEP), 1e-3)
            self.assertLessEqual(u.max(), pid.U_MAX + 1e-12)

    def test_anti_windup_reduces_overshoot(self):
        res = {}
        for anti_windup in (False, True):
            t, y, _, _ = pid.simulate(
                pid.simc_pi(), u_limits=(pid.U_MIN, pid.U_MAX), anti_windup=anti_windup
            )
            res[anti_windup] = pid.step_metrics(t, y, pid.SETPOINT_STEP)[0]
        self.assertLess(res[True], 0.5 * res[False])

    def test_ultimate_gain_gives_sustained_oscillation(self):
        k_u, t_u = pid.ultimate_gain_period()
        w_u = 2 * np.pi / t_u
        g = pid.process_response(w_u)
        self.assertAlmostEqual(k_u * abs(g), 1.0, places=10)
        self.assertAlmostEqual(g.real, -1.0 / k_u, places=10)
        self.assertAlmostEqual(g.imag, 0.0, places=10)
        # Proportional control at K_u: peaks of the error neither grow nor decay.
        gains = {"kc": k_u, "ti": 1e15, "td": 0.0}
        t, y, _, _ = pid.simulate(gains, t_end=10 * t_u, dt=0.001)
        late = t > 3 * t_u
        e = (y - pid.SETPOINT_STEP / (1 + 1 / (k_u * pid.PROCESS_GAIN)))[late]
        peaks = [
            e[i] for i in range(1, e.size - 1) if e[i] > e[i - 1] and e[i] >= e[i + 1]
        ]
        ratios = np.array(peaks[1:]) / np.array(peaks[:-1])
        np.testing.assert_allclose(ratios, 1.0, atol=0.02)

    def test_simc_load_iae_equals_ti_over_kc(self):
        # For a PI loop with zero final error the integrated error after a load
        # step d at the process input is |d| Ti / Kc; with no overshoot IAE = IE.
        gains = pid.simc_pi()
        t, y, _, _ = pid.simulate(gains, setpoint=0.0, load=pid.LOAD_STEP, t_end=300)
        expected = abs(pid.LOAD_STEP) * gains["ti"] / gains["kc"]
        self.assertAlmostEqual(pid.iae(t, y, 0.0), expected, delta=0.01 * expected)

    def test_tuning_rules(self):
        zn = pid.zn_step_pid(k=2.0, tau=10.0, theta=3.0)
        self.assertAlmostEqual(zn["kc"], 2.0)
        self.assertAlmostEqual(zn["ti"], 6.0)
        self.assertAlmostEqual(zn["td"], 1.5)
        simc = pid.simc_pi(k=2.0, tau=10.0, theta=3.0)
        self.assertAlmostEqual(simc["kc"], 10.0 / 12.0)
        self.assertAlmostEqual(simc["ti"], 10.0)
        simc_slow = pid.simc_pi(k=1.0, tau=100.0, theta=1.0)
        self.assertAlmostEqual(simc_slow["ti"], 8.0)  # 4 (tau_c + theta) < tau


if __name__ == "__main__":
    unittest.main()
