"""Beam solver, buckling curves, failure criteria and fatigue against closed forms."""

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


beams = load_example("algorithms", "beams_shear_moment_diagrams")
buckling = load_example("plots", "beams_buckling_curves")
envelopes = load_example("plots", "beams_failure_envelopes")
fatigue = load_example("plots", "fatigue_sn_and_goodman")

L = 5.0  # m
EI = 2.0e7  # N m^2
W = 12.0e3  # N/m
P = 8.0e3  # N


def solve(beam):
    nodes, v, theta, reactions = beams.solve_beam(beam, n_elements=100)
    x = beams.evaluation_points(beam)
    shear, moment = beams.internal_forces(beam, reactions, x)
    return nodes, v, theta, reactions, x, shear, moment


class BeamSolverTests(unittest.TestCase):
    def test_simply_supported_uniform_load(self):
        beam = beams.Beam(
            L, EI, [(0.0, "pin"), (L, "roller")], distributed=[(0.0, L, W, W)]
        )
        nodes, v, _, reactions, _, _, moment = solve(beam)
        np.testing.assert_allclose([r.force for r in reactions], [W * L / 2] * 2)
        self.assertAlmostEqual(moment.max(), W * L**2 / 8, delta=1e-6 * W * L**2)
        mid = np.argmin(np.abs(nodes - L / 2))
        self.assertAlmostEqual(-v[mid], 5 * W * L**4 / (384 * EI), delta=1e-10)

    def test_cantilever_tip_load(self):
        beam = beams.Beam(L, EI, [(0.0, "fixed")], point_loads=[(L, P)])
        _, v, theta, reactions, x, shear, moment = solve(beam)
        self.assertAlmostEqual(-v[-1], P * L**3 / (3 * EI), delta=1e-10)
        self.assertAlmostEqual(-theta[-1], P * L**2 / (2 * EI), delta=1e-10)
        self.assertAlmostEqual(reactions[0].force, P, delta=1e-8 * P)
        self.assertAlmostEqual(reactions[0].couple, -P * L, delta=1e-8 * P * L)
        np.testing.assert_allclose(moment, -P * (L - x), atol=1e-6 * P * L)
        np.testing.assert_allclose(shear[x < L], P, atol=1e-6 * P)

    def test_propped_cantilever_redundant(self):
        beam = beams.propped_cantilever()
        w, length = 10.0e3, beam.length
        _, v, _, reactions, _, _, moment = solve(beam)
        self.assertAlmostEqual(reactions[1].force, 3 * w * length / 8, delta=1e-3)
        self.assertAlmostEqual(reactions[0].couple, -w * length**2 / 8, delta=1e-2)
        self.assertAlmostEqual(moment.max(), 9 * w * length**2 / 128, delta=1.0)
        coefficient = (39 + 55 * np.sqrt(33)) / 65536  # delta_max = c w L^4 / EI
        self.assertAlmostEqual(
            -v.min(), coefficient * w * length**4 / beam.ei, delta=1e-6
        )

    def test_reactions_satisfy_equilibrium(self):
        for beam in (beams.overhanging_beam(), beams.propped_cantilever()):
            _, _, _, reactions = beams.solve_beam(beam)
            force, moment = beams.equilibrium_residual(beam, reactions)
            self.assertLess(abs(force), 1e-6 * 1e5)
            self.assertLess(abs(moment), 1e-6 * 1e6)

    def test_overhanging_beam_hand_values(self):
        beam = beams.overhanging_beam()
        _, _, _, reactions, x, _, moment = solve(beam)
        np.testing.assert_allclose(
            [r.force for r in reactions], [16e3, 29e3], rtol=1e-9
        )
        self.assertAlmostEqual(moment.max(), 12.8e3, delta=1.0)
        self.assertAlmostEqual(moment.min(), -30e3, delta=1.0)
        self.assertAlmostEqual(moment[-1], 0.0, delta=1e-3)

    def test_linear_load_moment(self):
        # Triangular load 0 -> w0 on a simply supported span: M_max = w0 L^2/(9 sqrt 3).
        w0 = 12.0e3
        beam = beams.Beam(
            6.0, EI, [(0.0, "pin"), (6.0, "roller")], distributed=[(0.0, 6.0, 0, w0)]
        )
        _, _, _, reactions, _, _, moment = solve(beam)
        np.testing.assert_allclose([r.force for r in reactions], [12e3, 24e3])
        self.assertAlmostEqual(
            moment.max(), w0 * 36 / (9 * np.sqrt(3)), delta=1e-4 * w0 * 36
        )


class BucklingTests(unittest.TestCase):
    def test_effective_length_factors(self):
        expected = {
            "Pinned-pinned": 1.0,
            "Fixed-free": 2.0,
            "Fixed-pinned": 0.69915,  # from tan(kL) = kL, kL = 4.4934
            "Fixed-fixed": 0.5,
        }
        for condition, k in expected.items():
            with self.subTest(condition=condition):
                self.assertAlmostEqual(
                    buckling.effective_length_factor(condition), k, delta=2e-4
                )

    def test_euler_load(self):
        p_cr, _, _ = buckling.buckling_mode("Pinned-pinned", length=3.0, ei=EI)
        self.assertAlmostEqual(p_cr / (np.pi**2 * EI / 9.0), 1.0, delta=1e-6)

    def test_johnson_tangent_to_euler(self):
        lam = buckling.transition_slenderness()
        self.assertAlmostEqual(
            buckling.johnson_stress(lam) / buckling.euler_stress(lam), 1.0, places=12
        )
        h = 1e-4
        slope_j = (
            buckling.johnson_stress(lam + h) - buckling.johnson_stress(lam - h)
        ) / (2 * h)
        slope_e = (buckling.euler_stress(lam + h) - buckling.euler_stress(lam - h)) / (
            2 * h
        )
        self.assertAlmostEqual(slope_j / slope_e, 1.0, places=6)
        self.assertAlmostEqual(buckling.johnson_stress(lam), buckling.SIGMA_Y / 2)

    def test_secant_formula_limits(self):
        # Small eccentricity: the curve approaches min(yield, Euler).
        for lam in (40.0, 200.0):
            stress = buckling.secant_stress([lam], 1e-6)[0]
            target = min(buckling.SIGMA_Y, buckling.euler_stress(lam))
            self.assertAlmostEqual(stress / target, 1.0, delta=0.01)

    def test_southwell_recovers_critical_load(self):
        p_true, loads, delta = buckling.southwell_readings()
        p_fit, d0 = buckling.southwell_fit(loads, delta)
        self.assertAlmostEqual(p_fit / p_true, 1.0, delta=0.01)
        self.assertAlmostEqual(d0 / buckling.STRUT_CROOKEDNESS, 1.0, delta=0.05)


class FailureCriteriaTests(unittest.TestCase):
    def test_pure_shear(self):
        tau = 100e6
        self.assertAlmostEqual(
            envelopes.safety_von_mises(tau, -tau),
            envelopes.SIGMA_Y / (np.sqrt(3) * tau),
        )
        self.assertAlmostEqual(
            envelopes.safety_tresca(tau, -tau), envelopes.SIGMA_Y / (2 * tau)
        )

    def test_envelope_points_lie_on_envelopes(self):
        for s1, s2 in ((107.7e6, -9.9e6), (100e6, 64.9e6), (-80e6, -150e6)):
            e1, e2 = envelopes.envelope_point(envelopes.safety_von_mises, s1, s2)
            self.assertAlmostEqual(envelopes.von_mises(e1, e2) / envelopes.SIGMA_Y, 1.0)
            e1, e2 = envelopes.envelope_point(envelopes.safety_tresca, s1, s2)
            self.assertAlmostEqual(envelopes.tresca(e1, e2) / envelopes.SIGMA_Y, 1.0)

    def test_tresca_is_never_less_conservative(self):
        rng = np.random.default_rng(1)
        for s1, s2 in rng.uniform(-300e6, 300e6, (200, 2)):
            self.assertLessEqual(
                envelopes.safety_tresca(s1, s2),
                envelopes.safety_von_mises(s1, s2) + 1e-12,
            )

    def test_coulomb_mohr_fourth_quadrant(self):
        s1, s2 = 50e6, -400e6
        n = envelopes.safety_coulomb_mohr(s1, s2)
        self.assertAlmostEqual(n * s1 / envelopes.S_UT - n * s2 / envelopes.S_UC, 1.0)


class FatigueTests(unittest.TestCase):
    def test_goodman_safety_factor(self):
        s_e, s_ut, sa, sm = 192e6, 600e6, 100e6, 150e6
        n = fatigue.safety_goodman(sa, sm, s_e, s_ut)
        self.assertAlmostEqual(n, 1 / (100 / 192 + 150 / 600))
        self.assertAlmostEqual(n * sa / s_e + n * sm / s_ut, 1.0)

    def test_gerber_point_on_parabola(self):
        s_e, sa, sm = 192e6, 100e6, 150e6
        n = fatigue.safety_gerber(sa, sm, s_e)
        self.assertAlmostEqual(n * sa / s_e + (n * sm / fatigue.S_UT) ** 2, 1.0)

    def test_sn_curve_end_points(self):
        _, s_e = fatigue.endurance_limits()
        f = fatigue.fatigue_strength_fraction()
        self.assertAlmostEqual(
            fatigue.fatigue_strength(1e3, s_e) / (f * fatigue.S_UT), 1
        )
        self.assertAlmostEqual(
            fatigue.fatigue_strength(1e6 * (1 - 1e-12), s_e) / s_e, 1.0, places=6
        )
        life = fatigue.cycles_to_failure(250e6, s_e)
        self.assertAlmostEqual(fatigue.fatigue_strength(life, s_e) / 250e6, 1.0)
        self.assertTrue(np.isinf(fatigue.cycles_to_failure(0.9 * s_e, s_e)))

    def test_rainflow_astm_example(self):
        cycles = fatigue.rainflow([-2, 1, -3, 5, -1, 3, -4, 4, -2])
        counts = {}
        for rng, _, n in cycles:
            counts[rng] = counts.get(rng, 0.0) + n
        self.assertEqual(counts, {3.0: 0.5, 4.0: 1.5, 6.0: 0.5, 8.0: 1.0, 9.0: 0.5})

    def test_repeating_block_closes_all_cycles(self):
        history = fatigue.random_history(n=60)
        cycles = fatigue.rainflow(history, repeating=True)
        largest = max(c[0] for c in cycles)
        self.assertAlmostEqual(largest, history.max() - history.min())
        total = sum(n for _, _, n in cycles)
        self.assertAlmostEqual(
            total, (len(fatigue.turning_points(history)) - 1) / 2, delta=1
        )

    def test_miner_sum(self):
        _, s_e = fatigue.endurance_limits()
        amps = [300e6, 250e6]
        lives = fatigue.cycles_to_failure(amps, s_e)
        cycles = [(2 * a, 0.0, 1.0) for a in amps for _ in range(10)]
        total, _, _, _ = fatigue.miner_damage(cycles, s_e)
        self.assertAlmostEqual(total, 10 / lives[0] + 10 / lives[1])


if __name__ == "__main__":
    unittest.main()
