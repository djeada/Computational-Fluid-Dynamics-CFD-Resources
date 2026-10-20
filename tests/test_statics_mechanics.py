"""Statics scripts: truss equilibrium, stiffness vs joints, supports, virtual work, friction."""

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


truss = load_example("algorithms", "statics_truss_solver")
vw = load_example("plots", "statics_virtual_work_stability")
friction = load_example("plots", "statics_friction_curves")
centroid = load_example("plots", "statics_composite_centroid")
cables = load_example("plots", "statics_cable_force_polygon")
supports = load_example("plots", "statics_support_reactions")


def joint_residual(nodes, members, support_map, loads, forces, reactions):
    """Net force at every joint: member forces + reactions + loads."""
    matrix = truss.equilibrium_matrix(nodes, members, support_map)
    return (matrix @ np.concatenate([forces, reactions]) + loads.ravel()).reshape(-1, 2)


class TrussTests(unittest.TestCase):
    def setUp(self):
        self.pratt = truss.pratt_truss()
        self.ea = truss.YOUNG_MODULUS * truss.MEMBER_AREA

    def test_every_joint_is_in_equilibrium(self):
        forces, reactions = truss.method_of_joints(*self.pratt)
        residual = joint_residual(*self.pratt, forces, reactions)
        np.testing.assert_allclose(residual, 0.0, atol=1e-8)

    def test_reactions_satisfy_global_equilibrium(self):
        nodes, _, _, loads = self.pratt
        _, reactions = truss.method_of_joints(*self.pratt)
        a_x, a_y, b_y = reactions
        span = nodes[:, 0].max()
        self.assertAlmostEqual(a_x, 0.0, places=6)
        self.assertAlmostEqual(a_y + b_y + loads[:, 1].sum(), 0.0, places=6)
        moment = b_y * span + np.sum(nodes[:, 0] * loads[:, 1])
        self.assertAlmostEqual(moment, 0.0, places=4)
        self.assertAlmostEqual(a_y, 50e3, places=4)

    def test_pratt_member_forces_match_method_of_sections(self):
        forces, _ = truss.method_of_joints(*self.pratt)
        n = truss.N_PANELS
        w, h, p = truss.PANEL_WIDTH, truss.TRUSS_HEIGHT, truss.JOINT_LOAD
        # Midspan top chord: moments about the midspan bottom joint, left half.
        moment = 2.5 * p * 3 * w - p * (2 * w + w)
        top_mid = forces[n + n // 2 - 1]
        self.assertAlmostEqual(top_mid, -moment / h, places=4)
        # The midspan vertical is a zero-force member.
        self.assertAlmostEqual(forces[2 * n + n // 2], 0.0, places=6)

    def test_stiffness_and_joints_give_same_forces_and_reactions(self):
        forces, reactions = truss.method_of_joints(*self.pratt)
        _, forces_k, reactions_k = truss.direct_stiffness(*self.pratt, ea=self.ea)
        np.testing.assert_allclose(forces_k, forces, atol=1e-6)
        np.testing.assert_allclose(reactions_k, reactions, atol=1e-6)

    def test_unit_load_deflection_matches_stiffness(self):
        disp, _, _ = truss.direct_stiffness(*self.pratt, ea=self.ea)
        mid = truss.N_PANELS // 2
        delta = truss.unit_load_deflection(
            *self.pratt, joint=mid, direction=1, ea=self.ea
        )
        self.assertAlmostEqual(delta, disp[mid, 1], delta=1e-12)

    def test_single_bar_elongation_is_pl_over_ea(self):
        nodes = np.array([[0.0, 0.0], [2.0, 0.0]])
        members = np.array([[0, 1]])
        support_map = {0: (True, True), 1: (False, True)}
        loads = np.array([[0.0, 0.0], [1000.0, 0.0]])
        disp, forces, _ = truss.direct_stiffness(
            nodes, members, support_map, loads, ea=1e6
        )
        self.assertAlmostEqual(disp[1, 0], 1000.0 * 2.0 / 1e6)
        self.assertAlmostEqual(forces[0], 1000.0)

    def test_indeterminate_truss_is_rejected_by_joints_but_solved_by_stiffness(self):
        braced = truss.pratt_truss(cross_braced=True)
        degree, deficiency, word = truss.classify_truss(*braced[:3])
        self.assertEqual(
            (degree, deficiency, word), (truss.N_PANELS, 0, "indeterminate")
        )
        with self.assertRaises(ValueError):
            truss.method_of_joints(*braced)
        _, forces, reactions = truss.direct_stiffness(*braced, ea=self.ea)
        residual = joint_residual(*braced, forces, reactions)
        np.testing.assert_allclose(residual, 0.0, atol=1e-6)

    def test_removing_a_diagonal_makes_a_mechanism(self):
        nodes, members, support_map, _ = truss.pratt_truss()
        first_diagonal = 3 * truss.N_PANELS + 1  # chords and verticals come first
        reduced = np.delete(members, first_diagonal, axis=0)
        degree, deficiency, word = truss.classify_truss(nodes, reduced, support_map)
        self.assertEqual((degree, deficiency, word), (-1, 1, "unstable"))


class VirtualWorkTests(unittest.TestCase):
    def test_virtual_work_load_makes_dv_zero(self):
        theta = np.radians(np.linspace(-60, 60, 121))
        theta = theta[np.abs(np.cos(theta)) > 1e-9]
        load = vw.equilibrium_load(theta)
        np.testing.assert_allclose(vw.dv_dtheta(theta, load), 0.0, atol=1e-9)

    def test_derivatives_match_finite_differences(self):
        theta, load, h = np.radians(12.0), 150.0, 1e-5
        dv = (
            vw.potential_energy(theta + h, load) - vw.potential_energy(theta - h, load)
        ) / (2 * h)
        d2v = (vw.dv_dtheta(theta + h, load) - vw.dv_dtheta(theta - h, load)) / (2 * h)
        self.assertAlmostEqual(vw.dv_dtheta(theta, load), dv, places=5)
        self.assertAlmostEqual(vw.d2v_dtheta2(theta, load), d2v, places=4)

    def test_limit_point_is_where_stability_is_lost(self):
        theta_star, p_star = vw.limit_point()
        self.assertAlmostEqual(np.cos(theta_star) ** 3, np.cos(vw.THETA0))
        self.assertAlmostEqual(vw.equilibrium_load(theta_star), p_star, places=8)
        self.assertAlmostEqual(vw.d2v_dtheta2(theta_star, p_star), 0.0, places=8)
        grid = np.radians(np.linspace(0.5, 29.5, 2000))
        self.assertAlmostEqual(vw.equilibrium_load(grid).max(), p_star, delta=1e-3)

    def test_unloaded_equilibria_and_stability(self):
        roots = vw.equilibria(0.0)
        angles = np.degrees([r for r, _ in roots])
        np.testing.assert_allclose(angles, [-30.0, 0.0, 30.0], atol=1e-9)
        self.assertEqual([s for _, s in roots], [True, False, True])


class FrictionTests(unittest.TestCase):
    def test_capstan_formula(self):
        self.assertAlmostEqual(
            friction.capstan_ratio(0.3, 5 * np.pi), np.exp(1.5 * np.pi)
        )
        # Exercise: 100 N holds 10 kN with mu = 0.25 after ln(100)/0.25 rad of wrap.
        wrap = np.log(100.0) / 0.25
        self.assertAlmostEqual(friction.capstan_ratio(0.25, wrap), 100.0)

    def test_capstan_ratio_matches_integrated_belt_equation(self):
        # dT/dbeta = mu T integrated with small steps.
        mu, beta, n = 0.3, 2.0 * np.pi, 20000
        tension = 1.0
        for _ in range(n):
            tension *= 1.0 + mu * beta / n
        self.assertAlmostEqual(tension, friction.capstan_ratio(mu, beta), delta=1e-3)

    def test_friction_regimes(self):
        f = friction.friction_force([10.0, 50.0, 60.0])
        np.testing.assert_allclose(f, [10.0, 50.0, 40.0])

    def test_screw_efficiency_maximum_and_self_locking(self):
        mu = 0.15
        phi = np.arctan(mu)
        lead = np.radians(np.linspace(0.1, 70, 20001))
        eff = friction.screw_efficiency(lead, mu)
        self.assertAlmostEqual(lead[np.argmax(eff)], np.pi / 4 - phi / 2, places=3)
        self.assertLess(friction.screw_efficiency(phi, mu), 0.5)


class CentroidAndEquilibriumTests(unittest.TestCase):
    def test_t_section(self):
        parts = centroid.t_section_parts()
        area, _, y_bar = centroid.composite_centroid(parts)
        self.assertAlmostEqual(area, 4000.0)
        self.assertAlmostEqual(y_bar, 70.0)
        self.assertAlmostEqual(centroid.second_moment(parts, y_bar), 10e6 / 3, places=3)

    def test_parts_table_matches_boundary_polygon(self):
        area, x_bar, y_bar = centroid.composite_centroid(centroid.plate_parts())
        exact = centroid.plate_centroid_exact()
        self.assertAlmostEqual(area, exact[0], delta=1e-5 * area)
        self.assertAlmostEqual(x_bar, exact[1], places=3)
        self.assertAlmostEqual(y_bar, exact[2], places=3)

    def test_polygon_centroid_of_triangle(self):
        area, x, y = centroid.polygon_centroid([[0, 0], [3, 0], [0, 6]])
        self.assertAlmostEqual(area, 9.0)
        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(y, 2.0)

    def test_cable_tensions(self):
        w = 981.0
        t30, t45 = np.radians(30.0), np.radians(45.0)
        u = [[np.cos(t30), np.sin(t30)], [-np.cos(t45), np.sin(t45)]]
        t = cables.concurrent_tensions(u, [0.0, -w])
        np.testing.assert_allclose(t, cables.two_cable_closed_form(w, t30, t45))
        anchors = np.array([[3.0, 0.0, 4.0], [-2.0, 2.0, 5.0], [1.0, -3.0, 6.0]])
        t3 = cables.concurrent_tensions(anchors, [0.0, 0.0, -500.0])
        units = anchors / np.linalg.norm(anchors, axis=1, keepdims=True)
        np.testing.assert_allclose(units.T @ t3, [0.0, 0.0, 500.0], atol=1e-9)
        self.assertTrue(np.all(t3 > 0))

    def test_support_classification_and_beam_reactions(self):
        labels = [
            supports.classify_supports(layout)[2] for _, layout in supports.LAYOUTS
        ]
        self.assertEqual(labels[0], "determinate")
        self.assertEqual(labels[1], "determinate")
        self.assertEqual(labels[2], "indeterminate, degree 1")
        self.assertTrue(labels[3].startswith("improper"))
        self.assertTrue(labels[4].startswith("improper"))
        self.assertTrue(labels[5].startswith("improper"))
        beam, forces = supports.example_beam()
        a_x, a_y, b_y = supports.solve_reactions(beam, forces)
        self.assertAlmostEqual(a_x, 0.0, places=8)
        self.assertAlmostEqual(b_y, 87.5e3 / 6, places=6)
        self.assertAlmostEqual(a_y, 25e3 - 87.5e3 / 6, places=6)


if __name__ == "__main__":
    unittest.main()
