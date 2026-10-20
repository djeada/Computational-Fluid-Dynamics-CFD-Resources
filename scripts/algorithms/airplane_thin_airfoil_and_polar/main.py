"""Thin-airfoil theory, a Hess-Smith panel method and a light-aircraft drag polar.

For a NACA 4-digit section (NACA 2412 by default) the script integrates the
camber-line slope to obtain the thin-airfoil zero-lift angle, lift slope 2*pi,
quarter-chord moment and chordwise loading, and checks them against an
inviscid Hess-Smith panel method (constant sources plus one uniform vortex
strength with the Kutta condition). It then builds the finite-wing lift curve
a/(1 + a/(pi e AR)), the drag polar C_D = C_D0 + k C_L^2 with the maximum
lift-to-drag ratio marked, and the power-required curve of a 1100 kg light
aircraft.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

DEFAULT_CODE = "2412"  # 2 % camber at 40 % chord, 12 % thick
N_PANELS = 160  # panels around the airfoil (even number)
ALPHA_CP = 4.0  # deg, angle of attack of the pressure-distribution figure
ALPHA_RANGE = np.arange(-6.0, 12.01, 1.0)  # deg, lift-curve angles

# Representative four-seat light aircraft (sea level).
RHO = 1.225  # kg/m^3, air density
G = 9.81  # m/s^2
MASS = 1100.0  # kg
WING_AREA = 16.2  # m^2
SPAN = 11.0  # m
OSWALD = 0.80  # span efficiency factor e
CD0 = 0.027  # zero-lift drag coefficient of the whole aircraft
CL_MAX = 1.6  # clean-wing maximum lift coefficient (sets the stall speed)


# --------------------------------------------------------------------------
# Geometry
# --------------------------------------------------------------------------
def parse_naca4(code):
    """Return (m, p, t) as chord fractions from a 4-digit NACA code."""
    if len(code) != 4 or not code.isdigit():
        raise ValueError(f"expected a 4-digit NACA code, got {code!r}")
    return int(code[0]) / 100, int(code[1]) / 10, int(code[2:]) / 100


def camber_slope(x, m, p):
    """Slope dz/dx of the NACA 4-digit mean camber line on a unit chord."""
    x = np.asarray(x, dtype=float)
    if m == 0 or p == 0:
        return np.zeros_like(x)
    return np.where(x < p, 2 * m / p**2 * (p - x), 2 * m / (1 - p) ** 2 * (p - x))


def camber_line(x, m, p):
    """Mean camber line z(x) of a NACA 4-digit section on a unit chord."""
    x = np.asarray(x, dtype=float)
    if m == 0 or p == 0:
        return np.zeros_like(x)
    return np.where(
        x < p,
        m / p**2 * (2 * p * x - x**2),
        m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x**2),
    )


def naca4_panels(code, n_panels=N_PANELS):
    """Panel end points, clockwise from the lower trailing edge, closed TE.

    Uses cosine spacing in x and the closed-trailing-edge thickness
    coefficient -0.1036 so that the first and last points coincide.
    """
    m, p, t = parse_naca4(code)
    beta = np.linspace(0.0, np.pi, n_panels // 2 + 1)
    x = 0.5 * (1 - np.cos(beta))
    yt = (
        5
        * t
        * (
            0.2969 * np.sqrt(x)
            - 0.1260 * x
            - 0.3516 * x**2
            + 0.2843 * x**3
            - 0.1036 * x**4
        )
    )
    zc = camber_line(x, m, p)
    theta = np.arctan(camber_slope(x, m, p))
    xu, yu = x - yt * np.sin(theta), zc + yt * np.cos(theta)
    xl, yl = x + yt * np.sin(theta), zc - yt * np.cos(theta)
    xs = np.concatenate([xl[::-1], xu[1:]])
    ys = np.concatenate([yl[::-1], yu[1:]])
    return xs, ys


# --------------------------------------------------------------------------
# Thin-airfoil theory
# --------------------------------------------------------------------------
def _theta_p(p):
    return np.arccos(1 - 2 * p) if 0 < p < 1 else 0.0


def zero_lift_angle(code):
    """alpha_L0 = -(1/pi) int_0^pi dz/dx (cos(theta) - 1) dtheta, in radians."""
    m, p, _ = parse_naca4(code)

    def integrand(th):
        return camber_slope(0.5 * (1 - np.cos(th)), m, p) * (np.cos(th) - 1)

    value, _ = quad(integrand, 0.0, np.pi, points=[_theta_p(p)], limit=200)
    return -value / np.pi


def fourier_coefficients(code, alpha, n_terms=20):
    """Thin-airfoil coefficients A_0 ... A_n at angle of attack alpha (rad)."""
    m, p, _ = parse_naca4(code)

    def slope(th):
        return camber_slope(0.5 * (1 - np.cos(th)), m, p)

    pts = [_theta_p(p)]
    a = np.zeros(n_terms + 1)
    a[0] = alpha - quad(slope, 0, np.pi, points=pts, limit=200)[0] / np.pi
    for n in range(1, n_terms + 1):
        integral = quad(
            lambda th, n=n: slope(th) * np.cos(n * th),
            0,
            np.pi,
            points=pts,
            limit=200,
        )[0]
        a[n] = 2 / np.pi * integral
    return a


def thin_airfoil_coefficients(code, alpha):
    """Return (c_l, c_m about c/4) from thin-airfoil theory at alpha (rad)."""
    a = fourier_coefficients(code, alpha, n_terms=2)
    cl = np.pi * (2 * a[0] + a[1])
    cm_quarter = np.pi / 4 * (a[2] - a[1])
    return cl, cm_quarter


def thin_airfoil_loading(code, alpha, x):
    """Chordwise load Delta C_p = C_p,lower - C_p,upper from thin-airfoil theory."""
    a = fourier_coefficients(code, alpha)
    th = np.arccos(1 - 2 * np.asarray(x))
    dcp = a[0] * (1 + np.cos(th)) / np.sin(th)
    for n in range(1, len(a)):
        dcp = dcp + a[n] * np.sin(n * th)
    return 4 * dcp


# --------------------------------------------------------------------------
# Hess-Smith panel method
# --------------------------------------------------------------------------
def panel_influence(xs, ys):
    """Normal and tangential influence of unit sources and the unit vortex.

    Returns (An, At, Bn, Bt): An[i, j], At[i, j] are the normal and tangential
    velocities at control point i induced by a unit source density on panel j;
    Bn[i], Bt[i] those induced by a unit counter-clockwise vortex density on
    every panel. Also returns midpoints, unit tangents, normals and lengths.
    """
    xa, ya, xb, yb = xs[:-1], ys[:-1], xs[1:], ys[1:]
    length = np.hypot(xb - xa, yb - ya)
    tx, ty = (xb - xa) / length, (yb - ya) / length
    nx, ny = -ty, tx  # outward for a clockwise ordering
    xm, ym = 0.5 * (xa + xb), 0.5 * (ya + yb)

    # Control point i expressed in the local frame of panel j.
    dx, dy = xm[:, None] - xa[None, :], ym[:, None] - ya[None, :]
    xl = dx * tx[None, :] + dy * ty[None, :]
    yl = dx * nx[None, :] + dy * ny[None, :]
    r1 = np.hypot(xl, yl)
    r2 = np.hypot(xl - length[None, :], yl)
    beta = np.arctan2(yl, xl - length[None, :]) - np.arctan2(yl, xl)
    beta = np.where(beta > np.pi, beta - 2 * np.pi, beta)
    beta = np.where(beta < -np.pi, beta + 2 * np.pi, beta)
    np.fill_diagonal(beta, np.pi)
    log_term = np.log(r1 / r2)
    np.fill_diagonal(log_term, 0.0)

    # Local velocities of a unit source (us, vs) and a unit ccw vortex (uv, vv).
    us, vs = log_term / (2 * np.pi), beta / (2 * np.pi)
    uv, vv = -beta / (2 * np.pi), log_term / (2 * np.pi)

    def to_global(u, v):
        return u * tx[None, :] + v * nx[None, :], u * ty[None, :] + v * ny[None, :]

    usx, usy = to_global(us, vs)
    uvx, uvy = to_global(uv, vv)
    an = usx * nx[:, None] + usy * ny[:, None]
    at = usx * tx[:, None] + usy * ty[:, None]
    bn = (uvx * nx[:, None] + uvy * ny[:, None]).sum(axis=1)
    bt = (uvx * tx[:, None] + uvy * ty[:, None]).sum(axis=1)
    geometry = dict(xm=xm, ym=ym, tx=tx, ty=ty, nx=nx, ny=ny, length=length)
    return an, at, bn, bt, geometry


def solve_panels(xs, ys, alpha):
    """Solve the Hess-Smith system at alpha (rad) for unit free-stream speed.

    Returns a dict with the surface tangential speed, C_p, c_l from pressure
    integration, c_l from Kutta-Joukowski, c_m about the quarter chord and the
    clockwise circulation.
    """
    an, at, bn, bt, geo = panel_influence(xs, ys)
    n = len(geo["length"])
    ux, uy = np.cos(alpha), np.sin(alpha)
    a = np.zeros((n + 1, n + 1))
    rhs = np.zeros(n + 1)
    a[:n, :n] = an
    a[:n, n] = bn
    rhs[:n] = -(ux * geo["nx"] + uy * geo["ny"])
    # Kutta condition: equal speeds leaving the trailing edge on both sides.
    a[n, :n] = at[0] + at[-1]
    a[n, n] = bt[0] + bt[-1]
    rhs[n] = -(
        ux * (geo["tx"][0] + geo["tx"][-1]) + uy * (geo["ty"][0] + geo["ty"][-1])
    )
    sol = np.linalg.solve(a, rhs)
    q, gamma = sol[:n], sol[n]

    vt = at @ q + gamma * bt + ux * geo["tx"] + uy * geo["ty"]
    cp = 1 - vt**2
    fx = np.sum(-cp * geo["nx"] * geo["length"])
    fy = np.sum(-cp * geo["ny"] * geo["length"])
    cl_pressure = fy * np.cos(alpha) - fx * np.sin(alpha)
    # Pitching moment about (0.25, 0); nose-up is clockwise, so the sign flips.
    rx, ry = geo["xm"] - 0.25, geo["ym"]
    cm = np.sum(cp * geo["length"] * (rx * geo["ny"] - ry * geo["nx"]))
    circulation = -gamma * geo["length"].sum()  # clockwise positive
    return dict(
        x=geo["xm"],
        y=geo["ym"],
        cp=cp,
        vt=vt,
        cl=cl_pressure,
        cl_kj=2 * circulation,
        cm_quarter=cm,
        circulation=circulation,
        source_sum=np.sum(q * geo["length"]),
    )


# --------------------------------------------------------------------------
# Finite wing and aircraft performance
# --------------------------------------------------------------------------
def aspect_ratio(span=SPAN, area=WING_AREA):
    return span**2 / area


def induced_drag_factor(ar, e=OSWALD):
    """k in C_D = C_D0 + k C_L^2."""
    return 1 / (np.pi * e * ar)


def finite_wing_slope(a2d, ar, e=OSWALD):
    """Lift-curve slope of a finite wing, a / (1 + a/(pi e AR)) per radian."""
    return a2d / (1 + a2d / (np.pi * e * ar))


def drag_polar(cl, cd0=CD0, k=None):
    k = induced_drag_factor(aspect_ratio()) if k is None else k
    return cd0 + k * cl**2


def max_lift_to_drag(cd0=CD0, k=None):
    """Return (C_L*, (L/D)_max) for a parabolic polar."""
    k = induced_drag_factor(aspect_ratio()) if k is None else k
    cl_star = np.sqrt(cd0 / k)
    return cl_star, 1 / (2 * np.sqrt(cd0 * k))


def level_flight_speed(cl, mass=MASS, rho=RHO, area=WING_AREA):
    """Speed at which lift equals weight for lift coefficient cl."""
    return np.sqrt(2 * mass * G / (rho * area * cl))


def power_required(speed, mass=MASS, rho=RHO, area=WING_AREA, cd0=CD0, k=None):
    """Power D V needed for steady level flight at the given speeds (W)."""
    k = induced_drag_factor(aspect_ratio()) if k is None else k
    q = 0.5 * rho * speed**2
    cl = mass * G / (q * area)
    return q * area * (cd0 + k * cl**2) * speed


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def plot_pressure(code, xs, ys, alpha_deg):
    alpha = np.radians(alpha_deg)
    res = solve_panels(xs, ys, alpha)
    n_half = len(res["x"]) // 2
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))

    ax = axes[0]
    ax.plot(
        res["x"][n_half:], res["cp"][n_half:], color="tab:blue", label="Upper surface"
    )
    ax.plot(
        res["x"][:n_half], res["cp"][:n_half], color="tab:orange", label="Lower surface"
    )
    ax.invert_yaxis()
    ax.axhline(0, color="0.6", lw=0.8)
    ax.set_xlabel("$x/c$")
    ax.set_ylabel("$C_p$ (negative up)")
    ax.set_title(
        f"(a) Panel-method $C_p$, NACA {code}, $\\alpha = {alpha_deg:g}^\\circ$"
    )
    inset = ax.inset_axes([0.45, 0.06, 0.5, 0.22])
    inset.fill(xs, ys, color="0.8", ec="0.3")
    inset.set_aspect("equal")
    inset.axis("off")
    ax.legend(loc="upper right", fontsize=10)
    ax.text(
        0.35,
        0.55,
        f"$c_l$ = {res['cl']:.3f} (pressure)\n$c_l$ = {res['cl_kj']:.3f} (Kutta-Joukowski)",
        transform=ax.transAxes,
        fontsize=10,
    )
    ax.grid(alpha=0.3)

    ax = axes[1]
    x_lower = res["x"][:n_half][::-1]
    cp_lower = res["cp"][:n_half][::-1]
    cp_upper = np.interp(x_lower, res["x"][n_half:], res["cp"][n_half:])
    xt = np.linspace(0.005, 0.995, 400)
    ax.plot(
        x_lower,
        cp_lower - cp_upper,
        color="tab:blue",
        label="Panel method (12 % thick)",
    )
    ax.plot(
        xt,
        thin_airfoil_loading(code, alpha, xt),
        "--",
        color="tab:red",
        label="Thin-airfoil theory",
    )
    ax.set_ylim(0, 4)
    ax.set_xlabel("$x/c$")
    ax.set_ylabel(r"$\Delta C_p = C_{p,l} - C_{p,u}$")
    ax.set_title("(b) Chordwise load: panel method vs thin-airfoil theory")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig, res


def plot_lift_and_polar(code, xs, ys):
    alpha = np.radians(ALPHA_RANGE)
    alpha_l0 = zero_lift_angle(code)
    cl_thin = 2 * np.pi * (alpha - alpha_l0)
    cl_panel = np.array([solve_panels(xs, ys, a)["cl"] for a in alpha])
    ar = aspect_ratio()
    a3d = finite_wing_slope(2 * np.pi, ar)
    cl_wing = a3d * (alpha - alpha_l0)

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))
    ax = axes[0]
    ax.plot(
        ALPHA_RANGE, cl_panel, "o", ms=5, color="tab:blue", label="Panel method (2D)"
    )
    ax.plot(
        ALPHA_RANGE,
        cl_thin,
        color="tab:red",
        label=r"Thin airfoil, $2\pi(\alpha - \alpha_{L0})$",
    )
    ax.plot(
        ALPHA_RANGE,
        cl_wing,
        color="tab:green",
        label=f"Finite wing, AR = {ar:.2f}, e = {OSWALD}",
    )
    ax.axhline(0, color="0.6", lw=0.8)
    ax.axvline(np.degrees(alpha_l0), color="0.6", lw=0.8, ls=":")
    ax.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax.set_ylabel("Lift coefficient")
    ax.set_title(f"(a) Inviscid lift curves, NACA {code}")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(alpha=0.3)

    k = induced_drag_factor(ar)
    cl = np.linspace(-0.2, CL_MAX, 200)
    cd = drag_polar(cl, k=k)
    cl_star, ld_max = max_lift_to_drag(k=k)
    ax = axes[1]
    ax.plot(cd, cl, color="tab:blue", label=r"$C_D = C_{D0} + k C_L^2$")
    ax.plot(
        [0, 2 * CD0 * 1.6],
        [0, 2 * CD0 * 1.6 * ld_max],
        "--",
        color="0.4",
        label="Tangent from origin",
    )
    ax.plot(
        2 * CD0,
        cl_star,
        "o",
        color="tab:red",
        ms=8,
        label=f"$(L/D)_{{max}}$ = {ld_max:.1f} at $C_L$ = {cl_star:.2f}",
    )
    ax.set_xlim(0, 0.18)
    ax.set_xlabel("Drag coefficient $C_D$")
    ax.set_ylabel("Lift coefficient $C_L$")
    ax.set_title(f"(b) Drag polar, $C_{{D0}}$ = {CD0}, k = {k:.4f}")
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(alpha=0.3)

    ax = axes[2]
    v_stall = level_flight_speed(CL_MAX)
    v = np.linspace(v_stall, 75, 300)
    ax.plot(
        v, power_required(v, k=k) / 1e3, color="tab:blue", label="Power required $DV$"
    )
    v_md = level_flight_speed(cl_star)
    v_mp = level_flight_speed(np.sqrt(3 * CD0 / k))
    ax.plot(
        v_md,
        power_required(v_md, k=k) / 1e3,
        "o",
        color="tab:red",
        ms=8,
        label=f"Minimum drag, {v_md:.1f} m/s",
    )
    ax.plot(
        v_mp,
        power_required(v_mp, k=k) / 1e3,
        "s",
        color="tab:green",
        ms=8,
        label=f"Minimum power, {v_mp:.1f} m/s",
    )
    ax.axvline(v_stall, color="0.5", ls=":", lw=1)
    ax.text(v_stall + 0.5, 120, f"stall\n{v_stall:.1f} m/s", fontsize=9)
    ax.set_ylim(0, 140)
    ax.set_xlabel("True airspeed $V$ (m/s)")
    ax.set_ylabel("Power (kW)")
    ax.set_title(f"(c) Level flight, m = {MASS:.0f} kg, sea level")
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig, dict(
        alpha_l0=alpha_l0,
        slope_panel=np.polyfit(alpha, cl_panel, 1)[0],
        alpha_l0_panel=-np.polyfit(alpha, cl_panel, 1)[1]
        / np.polyfit(alpha, cl_panel, 1)[0],
        a3d=a3d,
        k=k,
        cl_star=cl_star,
        ld_max=ld_max,
        v_md=v_md,
        v_mp=v_mp,
        v_stall=v_stall,
    )


def parse_args(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--naca",
        default=DEFAULT_CODE,
        metavar="CODE",
        help=f"four-digit NACA designation (default: {DEFAULT_CODE})",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    xs, ys = naca4_panels(args.naca)
    fig_cp, res = plot_pressure(args.naca, xs, ys, ALPHA_CP)
    fig_cl, summary = plot_lift_and_polar(args.naca, xs, ys)

    cl_thin, cm_thin = thin_airfoil_coefficients(args.naca, np.radians(ALPHA_CP))
    print(f"NACA {args.naca}, {len(xs) - 1} panels")
    print(
        f"  thin airfoil: alpha_L0 = {np.degrees(summary['alpha_l0']):.3f} deg, "
        f"c_l({ALPHA_CP:g} deg) = {cl_thin:.3f}, c_m,c/4 = {cm_thin:.4f}"
    )
    print(
        f"  panel method: alpha_L0 = {np.degrees(summary['alpha_l0_panel']):.3f} deg, "
        f"dc_l/dalpha = {summary['slope_panel']:.3f} /rad, c_l({ALPHA_CP:g} deg) = "
        f"{res['cl']:.3f} (K-J {res['cl_kj']:.3f}), c_m,c/4 = {res['cm_quarter']:.4f}"
    )
    print(f"  finite wing: AR = {aspect_ratio():.2f}, a_3D = {summary['a3d']:.3f} /rad")
    print(
        f"  polar: k = {summary['k']:.4f}, C_L* = {summary['cl_star']:.3f}, "
        f"(L/D)max = {summary['ld_max']:.2f}"
    )
    print(
        f"  speeds: stall {summary['v_stall']:.1f} m/s, min power {summary['v_mp']:.1f} m/s, "
        f"min drag {summary['v_md']:.1f} m/s"
    )

    finish_figures(
        {
            "airplane_airfoil_pressure.png": fig_cp,
            "airplane_lift_curve_and_polar.png": fig_cl,
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
