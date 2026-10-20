"""Integrating a surface pressure and shear field over boundary faces into forces.

A CFD solver reports pressure and wall shear stress on the faces of the body
surface; the force is the sum over faces of (-p n + tau_w) A and the moment
the sum of r x (-p n + tau_w) A. This script does that integration for a
circular cylinder represented by N flat faces, as on a CFD surface mesh, with
three pressure fields: potential flow (zero drag, d'Alembert's paradox),
potential flow with circulation (lift rho U Gamma, Kutta-Joukowski) and an
illustrative separated-flow model in which the potential-flow pressure is
cut off at a constant base pressure. It also integrates a hydrostatic field
(buoyancy) and shows how the face-sum converges with the number of faces.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

RADIUS = 0.5  # cylinder radius a (m)
U_INF = 2.0  # free-stream speed along +x (m/s)
RHO = 1000.0  # fluid density (kg/m^3)
G = 9.81  # gravitational acceleration (m/s^2)
CIRCULATION_FRACTION = 0.5  # Gamma = -fraction * 2 pi a U (clockwise, lift up)
BASE_PRESSURE_COEFF = -1.2  # C_pb of the separated-flow model (-)
N_FIGURE = 36  # faces drawn in the surface panel
N_SEQUENCE = (8, 16, 32, 64, 128, 256, 512)  # faces in the convergence study


def cylinder_faces(n, radius=RADIUS):
    """Flat faces of an n-gon inscribed in the circle.

    Returns vertices (n, 2), face centroids (n, 2), outward unit normals
    (n, 2) and face lengths (n,), i.e. areas per unit span.
    """
    phi = 2.0 * np.pi * np.arange(n + 1) / n
    vertices = radius * np.column_stack((np.cos(phi), np.sin(phi)))
    start, end = vertices[:-1], vertices[1:]
    centroids = 0.5 * (start + end)
    edge = end - start
    lengths = np.hypot(edge[:, 0], edge[:, 1])
    normals = np.column_stack((edge[:, 1], -edge[:, 0])) / lengths[:, None]
    return vertices[:-1], centroids, normals, lengths


def integrate_loads(centroids, normals, areas, pressure, shear=None, origin=(0.0, 0.0)):
    """Force (Fx, Fy) and moment Mz of the traction -p n + tau over the faces.

    ``pressure`` holds one value per face and ``shear`` an optional (n, 2)
    array of wall shear stress vectors. The moment is about ``origin``.
    """
    traction = -pressure[:, None] * normals
    if shear is not None:
        traction = traction + shear
    face_force = traction * areas[:, None]
    r = centroids - np.asarray(origin)
    moment = np.sum(r[:, 0] * face_force[:, 1] - r[:, 1] * face_force[:, 0])
    return face_force.sum(axis=0), moment


def potential_cp(phi, circulation=0.0, u_inf=U_INF, radius=RADIUS):
    """Surface C_p = 1 - (u_phi / U)^2 of potential flow past a cylinder.

    phi is measured counterclockwise from +x (the rear stagnation point
    without circulation) and u_phi = -2 U sin(phi) + Gamma / (2 pi a).
    """
    u_phi = -2.0 * u_inf * np.sin(phi) + circulation / (2.0 * np.pi * radius)
    return 1.0 - (u_phi / u_inf) ** 2


def separated_cp(phi, base_cp=BASE_PRESSURE_COEFF):
    """Illustrative separated flow: potential C_p, but never below C_pb.

    Once the potential-flow pressure on the front falls to the base pressure
    it stays there over the whole rear of the cylinder.
    """
    theta = np.pi - np.mod(phi, 2.0 * np.pi)  # angle from the front stagnation point
    theta = np.abs(np.mod(theta + np.pi, 2.0 * np.pi) - np.pi)
    theta_sep = np.arcsin(np.sqrt((1.0 - base_cp) / 4.0))
    cp = 1.0 - 4.0 * np.sin(theta) ** 2
    return np.where(theta < theta_sep, cp, base_cp)


def coefficients(force, u_inf=U_INF, radius=RADIUS, rho=RHO):
    """Drag and lift coefficients per unit span, F / (rho U^2 a)."""
    q = 0.5 * rho * u_inf**2
    return force[0] / (q * 2 * radius), force[1] / (q * 2 * radius)


def face_angles(centroids):
    return np.arctan2(centroids[:, 1], centroids[:, 0])


def loads_for(n, case):
    """Integrated force and moment on n faces for one named case."""
    _, c, nrm, area = cylinder_faces(n)
    phi = face_angles(c)
    q = 0.5 * RHO * U_INF**2
    gamma = -CIRCULATION_FRACTION * 2.0 * np.pi * RADIUS * U_INF
    if case == "potential":
        p = q * potential_cp(phi)
    elif case == "circulation":
        p = q * potential_cp(phi, gamma)
    elif case == "separated":
        p = q * separated_cp(phi)
    elif case == "hydrostatic":
        p = -RHO * G * c[:, 1]  # gauge pressure relative to the centre depth
    else:
        raise ValueError(case)
    return integrate_loads(c, nrm, area, p)


def make_figure(study):
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.2), width_ratios=(1.15, 1, 1.15))
    gamma = -CIRCULATION_FRACTION * 2.0 * np.pi * RADIUS * U_INF

    ax = axes[0]
    phi = np.linspace(-np.pi, np.pi, 721)
    theta_deg = np.degrees(np.pi - np.mod(phi, 2 * np.pi))  # from front, -180..180
    order = np.argsort(theta_deg)
    for cp, label, color in (
        (potential_cp(phi), "potential flow", "tab:blue"),
        (
            potential_cp(phi, gamma),
            f"with circulation $\\Gamma$ = {gamma:.2f} m$^2$/s",
            "tab:green",
        ),
        (
            separated_cp(phi),
            f"separated model, $C_{{pb}}$ = {BASE_PRESSURE_COEFF:g}",
            "tab:orange",
        ),
    ):
        ax.plot(theta_deg[order], cp[order], color=color, lw=2, label=label)
    ax.set_xlim(-180, 180)
    ax.set_xticks(np.arange(-180, 181, 60))
    ax.set_xlabel("Angle from front stagnation point $\\theta$ (degrees)", fontsize=11)
    ax.set_ylabel("Pressure coefficient $C_p$", fontsize=11)
    ax.set_title("(a) Surface pressure distributions", fontsize=12)
    ax.legend(fontsize=9.5, loc="lower left")
    ax.grid(True, ls="--", lw=0.5, alpha=0.6)

    ax = axes[1]
    verts, c, nrm, area = cylinder_faces(N_FIGURE)
    cp = separated_cp(face_angles(c))
    polys = [
        [
            verts[i],
            verts[(i + 1) % N_FIGURE],
            0.82 * verts[(i + 1) % N_FIGURE],
            0.82 * verts[i],
        ]
        for i in range(N_FIGURE)
    ]
    coll = PolyCollection(
        polys, array=cp, cmap="RdBu_r", edgecolors="k", linewidths=0.4
    )
    coll.set_clim(-1.5, 1.5)
    ax.add_collection(coll)
    arrows = -cp[:, None] * nrm * 0.18
    # Pressure (C_p > 0) arrows end on the face; suction arrows start on it.
    tails = np.where(cp[:, None] > 0, c - arrows, c)
    ax.quiver(
        tails[:, 0],
        tails[:, 1],
        arrows[:, 0],
        arrows[:, 1],
        angles="xy",
        scale_units="xy",
        scale=1,
        width=0.004,
        color="k",
    )
    ax.annotate(
        "", xy=(-0.95, 0), xytext=(-1.25, 0), arrowprops={"arrowstyle": "->", "lw": 2}
    )
    ax.text(-1.25, 0.06, "$U_\\infty$", fontsize=12)
    fig.colorbar(coll, ax=ax, label="$C_p$ on each face", fraction=0.046)
    ax.set_xlim(-1.3, 1.0)
    ax.set_ylim(-0.9, 0.9)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$ (m)", fontsize=11)
    ax.set_ylabel("$y$ (m)", fontsize=11)
    ax.set_title(
        f"(b) Face tractions $-C_p\\,\\mathbf{{n}}$, {N_FIGURE} faces", fontsize=12
    )

    ax = axes[2]
    n = np.array(N_SEQUENCE, dtype=float)
    ax.loglog(
        n, study["buoyancy_err"], "o-", color="tab:blue", label="buoyancy, rel. error"
    )
    ax.loglog(
        n,
        study["lift_err"],
        "s-",
        color="tab:green",
        label="lift vs $\\rho U |\\Gamma|$, rel. error",
    )
    ax.loglog(
        n,
        study["cd_err"],
        "^-",
        color="tab:orange",
        label="separated $C_d$, change from finest",
    )
    ax.loglog(
        n, study["buoyancy_err"][0] * (n / n[0]) ** -2, "k--", lw=1, label="slope $-2$"
    )
    ax.set_xlabel("Number of surface faces $N$", fontsize=11)
    ax.set_ylabel("Error of the face sum", fontsize=11)
    ax.set_title("(c) Convergence with surface resolution", fontsize=12)
    ax.legend(fontsize=9.5, loc="lower left")
    ax.grid(True, which="both", ls="--", lw=0.5, alpha=0.6)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    gamma = -CIRCULATION_FRACTION * 2.0 * np.pi * RADIUS * U_INF
    lift_exact = -RHO * U_INF * gamma
    buoyancy_exact = RHO * G * np.pi * RADIUS**2
    n_fine = N_SEQUENCE[-1]
    cd_fine = coefficients(loads_for(n_fine, "separated")[0])[0]
    study = {"buoyancy_err": [], "lift_err": [], "cd_err": []}
    for n in N_SEQUENCE:
        fb, _ = loads_for(n, "hydrostatic")
        fl, ml = loads_for(n, "circulation")
        fp, _ = loads_for(n, "potential")
        fs, _ = loads_for(n, "separated")
        cd, cl = coefficients(fs)
        study["buoyancy_err"].append(abs(fb[1] - buoyancy_exact) / buoyancy_exact)
        study["lift_err"].append(abs(fl[1] - lift_exact) / lift_exact)
        study["cd_err"].append(abs(cd - cd_fine) / cd_fine)
        print(
            f"N = {n:4d}: buoyancy = {fb[1]:8.2f} N/m (exact {buoyancy_exact:.2f}), "
            f"potential drag = {fp[0]:+.1e} N/m, lift = {fl[1]:8.2f} N/m "
            f"(rho U |Gamma| = {lift_exact:.2f}), circulation drag = {fl[0]:+.1e}, "
            f"moment = {ml:+.1e} N, separated C_d = {cd:.4f}, C_l = {cl:+.1e}"
        )
    study = {k: np.array(v) for k, v in study.items()}
    study["cd_err"][-1] = np.nan  # the finest mesh is the reference
    print(
        f"separated-flow model: C_d = {cd_fine:.4f} with C_pb = {BASE_PRESSURE_COEFF}"
    )

    fig = make_figure(study)
    finish_figures(
        {"fluid_loading_surface_force_integration.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
