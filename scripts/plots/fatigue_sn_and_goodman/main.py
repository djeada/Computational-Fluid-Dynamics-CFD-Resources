"""High-cycle fatigue of a steel shaft: S-N curve, mean-stress diagram and Miner's rule.

Panel (a) is the stress-life (S-N) line between 10^3 and 10^6 cycles for a
polished specimen and for the machined shaft after the Marin factors, with the
endurance limit beyond the knee. Panel (b) is the Haigh diagram with the
Goodman, Gerber and Soderberg lines and the first-cycle yield line, an
operating point and its safety factor along a radial load line. Panels (c)
and (d) apply rainflow counting (ASTM E1049) to a seeded random stress
history, convert every counted cycle to an equivalent fully reversed
amplitude with the Goodman relation and sum the damage with the
Palmgren-Miner rule.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

MPA = 1.0e6
S_UT = 600.0 * MPA  # ultimate tensile strength (Pa)
S_Y = 450.0 * MPA  # yield strength (Pa)
DIAMETER = 0.030  # shaft diameter for the size factor (m)
SURFACE_A, SURFACE_B = 4.51, -0.265  # Marin surface factor for machined steel (MPa)
K_RELIABILITY = 0.897  # 90% reliability factor
N_LOW, N_KNEE = 1.0e3, 1.0e6  # ends of the finite-life line (cycles)

EXAMPLE_AMPLITUDE = 250.0 * MPA  # fully reversed amplitude marked on the S-N curve (Pa)
OPERATING_MEAN = 150.0 * MPA  # sigma_m of the operating point (Pa)
OPERATING_AMPLITUDE = 100.0 * MPA  # sigma_a of the operating point (Pa)

HISTORY_REVERSALS = 400  # turning points in the random block
HISTORY_MEAN = 60.0 * MPA  # mean of the random stress history (Pa)
HISTORY_SCALE = 115.0 * MPA  # standard deviation of the peaks about the mean (Pa)
SEED = 7


def marin_factors(s_ut=S_UT, d=DIAMETER):
    """Surface (machined), size (rotating, 2.79 <= d <= 51 mm), load, temperature, reliability."""
    k_a = SURFACE_A * (s_ut / MPA) ** SURFACE_B
    k_b = 1.24 * (d * 1e3) ** -0.107
    return {"k_a": k_a, "k_b": k_b, "k_c": 1.0, "k_d": 1.0, "k_e": K_RELIABILITY}


def endurance_limits(s_ut=S_UT, d=DIAMETER):
    """Specimen endurance limit S'_e = 0.5 S_ut and the component value S_e (Pa)."""
    s_e_prime = 0.5 * s_ut if s_ut <= 1400 * MPA else 700 * MPA
    return s_e_prime, s_e_prime * np.prod(list(marin_factors(s_ut, d).values()))


def fatigue_strength_fraction(s_ut=S_UT):
    """Fraction f of S_ut reached at 10^3 cycles (sigma'_F = S_ut + 345 MPa estimate)."""
    s_e_prime, _ = endurance_limits(s_ut)
    sigma_f = s_ut + 345 * MPA
    b = -np.log10(sigma_f / s_e_prime) / np.log10(2 * N_KNEE)
    return sigma_f / s_ut * (2 * N_LOW) ** b


def basquin_constants(s_e, s_ut=S_UT):
    """Constants of S_f = a N^b through (10^3, f S_ut) and (10^6, S_e)."""
    f = fatigue_strength_fraction(s_ut)
    a = (f * s_ut) ** 2 / s_e
    b = -np.log10(f * s_ut / s_e) / 3.0
    return a, b


def fatigue_strength(n_cycles, s_e, s_ut=S_UT):
    """S-N curve: Basquin line up to the knee, endurance limit beyond (Pa)."""
    a, b = basquin_constants(s_e, s_ut)
    n = np.asarray(n_cycles, dtype=float)
    return np.where(n < N_KNEE, a * n**b, s_e)


def cycles_to_failure(amplitude, s_e, s_ut=S_UT):
    """Inverse of the S-N curve; infinite life at or below the endurance limit."""
    a, b = basquin_constants(s_e, s_ut)
    amp = np.asarray(amplitude, dtype=float)
    with np.errstate(divide="ignore"):
        life = (amp / a) ** (1.0 / b)
    return np.where(amp > s_e, life, np.inf)


def safety_goodman(sa, sm, s_e, s_ut=S_UT):
    return 1.0 / (sa / s_e + sm / s_ut)


def safety_soderberg(sa, sm, s_e, s_y=S_Y):
    return 1.0 / (sa / s_e + sm / s_y)


def safety_gerber(sa, sm, s_e, s_ut=S_UT):
    """Safety factor on a radial load line against the Gerber parabola."""
    if sm == 0:
        return s_e / sa
    ratio = 2 * sm * s_e / (s_ut * sa)
    return 0.5 * (s_ut / sm) ** 2 * (sa / s_e) * (-1 + np.sqrt(1 + ratio**2))


def safety_yield(sa, sm, s_y=S_Y):
    """Langer first-cycle yield line sigma_a + sigma_m = S_y."""
    return s_y / (sa + abs(sm))


def goodman_equivalent_amplitude(sa, sm, s_ut=S_UT):
    """Fully reversed amplitude with the same Goodman damage (tensile mean only)."""
    return np.asarray(sa) / (1.0 - np.maximum(np.asarray(sm), 0.0) / s_ut)


def turning_points(series):
    """Keep only the peaks and valleys (reversals) of a series."""
    x = np.asarray(series, dtype=float)
    x = x[np.concatenate(([True], np.diff(x) != 0))]
    if x.size < 3:
        return x
    slope = np.diff(x)
    keep = np.concatenate(([True], slope[1:] * slope[:-1] < 0, [True]))
    return x[keep]


def rainflow(series, repeating=False):
    """Rainflow counting (ASTM E1049-85, three-point method).

    Returns a list of (range, mean, count) with count 1.0 or 0.5. With
    repeating=True the series is one block of a history that repeats, so it is
    rotated to start and end at its largest peak; every cycle then closes and
    the largest range is counted once per block.
    """
    points = turning_points(series)
    if repeating:
        start = int(np.argmax(points))
        points = turning_points(np.concatenate((points[start:], points[: start + 1])))
    cycles = []
    stack = []
    for point in points:
        stack.append(point)
        while len(stack) >= 3:
            x_range = abs(stack[-1] - stack[-2])
            y_range = abs(stack[-2] - stack[-3])
            if x_range < y_range:
                break
            mean = 0.5 * (stack[-2] + stack[-3])
            if len(stack) == 3:
                cycles.append((y_range, mean, 0.5))
                stack.pop(0)
            else:
                cycles.append((y_range, mean, 1.0))
                last = stack.pop()
                del stack[-2:]
                stack.append(last)
    for a, b in zip(stack[:-1], stack[1:], strict=True):
        cycles.append((abs(b - a), 0.5 * (a + b), 0.5))
    return cycles


def miner_damage(cycles, s_e, s_ut=S_UT):
    """Palmgren-Miner damage sum of rainflow cycles and the per-cycle damage."""
    ranges, means, counts = (np.array(c) for c in zip(*cycles, strict=True))
    amp = goodman_equivalent_amplitude(ranges / 2, means, s_ut)
    damage = counts / cycles_to_failure(amp, s_e, s_ut)
    return damage.sum(), amp, counts, damage


def random_history(n=HISTORY_REVERSALS, seed=SEED):
    """Alternating peaks and valleys of a seeded random stress block (Pa)."""
    rng = np.random.default_rng(seed)
    size = np.abs(rng.normal(0.0, HISTORY_SCALE, n))
    sign = np.where(np.arange(n) % 2 == 0, 1.0, -1.0)
    return HISTORY_MEAN + sign * size


def plot_sn(ax, s_e_prime, s_e):
    n = np.logspace(3, 8, 400)
    ax.loglog(
        n,
        fatigue_strength(n, s_e_prime) / MPA,
        color="tab:blue",
        lw=2.2,
        label=f"polished specimen, $S'_e$ = {s_e_prime / MPA:.0f} MPa",
    )
    ax.loglog(
        n,
        fatigue_strength(n, s_e) / MPA,
        color="tab:orange",
        lw=2.2,
        label=f"machined shaft, $S_e$ = {s_e / MPA:.0f} MPa",
    )
    f = fatigue_strength_fraction()
    ax.plot(N_LOW, f * S_UT / MPA, "o", color="k")
    ax.annotate(
        f"$f S_{{ut}}$ = {f * S_UT / MPA:.0f} MPa (f = {f:.3f})",
        (N_LOW, f * S_UT / MPA),
        xytext=(10, 8),
        textcoords="offset points",
        fontsize=10,
    )
    ax.axvline(N_KNEE, color="0.5", lw=0.8, ls="--")
    amp = EXAMPLE_AMPLITUDE
    life = cycles_to_failure(amp, s_e)
    ax.plot([1e3, life, life], [amp / MPA, amp / MPA, 30], ":", color="tab:red")
    ax.annotate(
        f"$\\sigma_{{ar}}$ = {amp / MPA:.0f} MPa: N = {life:.2e}",
        (life, amp / MPA),
        xytext=(8, 8),
        textcoords="offset points",
        color="tab:red",
        fontsize=10,
    )
    a, b = basquin_constants(s_e)
    ax.text(
        2e6,
        0.7 * s_e / MPA,
        f"shaft: $S_f$ = {a / MPA:.0f} $N^{{{b:.4f}}}$ MPa",
        fontsize=10,
    )
    ax.set(
        xlim=(1e3, 1e8),
        ylim=(100, 700),
        xlabel="cycles to failure N",
        ylabel="fully reversed stress amplitude (MPa)",
        title="(a) Stress-life (S-N) curves",
    )
    ticks = [100, 150, 200, 300, 400, 500, 600]
    ax.set_yticks(ticks, [str(t) for t in ticks])
    ax.minorticks_off()
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, which="both", lw=0.5, alpha=0.4)


def plot_haigh(ax, s_e):
    sm = np.linspace(0, S_UT, 300)
    ax.plot(
        sm / MPA, s_e * (1 - sm / S_UT) / MPA, color="tab:blue", lw=2.2, label="Goodman"
    )
    ax.plot(
        sm / MPA,
        s_e * (1 - (sm / S_UT) ** 2) / MPA,
        color="tab:orange",
        lw=2.2,
        label="Gerber",
    )
    sm_s = np.linspace(0, S_Y, 200)
    ax.plot(
        sm_s / MPA,
        s_e * (1 - sm_s / S_Y) / MPA,
        color="tab:green",
        lw=2.2,
        label="Soderberg",
    )
    ax.plot(
        [0, S_Y / MPA],
        [S_Y / MPA, 0],
        "--",
        color="tab:red",
        lw=1.5,
        label="yield (Langer)",
    )
    sa, smo = OPERATING_AMPLITUDE, OPERATING_MEAN
    n_g = safety_goodman(sa, smo, s_e)
    ax.plot([0, 1.8 * smo / MPA], [0, 1.8 * sa / MPA], ":", color="k", lw=1)
    ax.plot(smo / MPA, sa / MPA, "o", color="k", ms=8)
    ax.plot(n_g * smo / MPA, n_g * sa / MPA, "x", color="tab:blue", ms=9, mew=2)
    text = (
        f"operating point ($\\sigma_m$, $\\sigma_a$) = ({smo / MPA:.0f}, {sa / MPA:.0f}) MPa\n"
        f"Goodman n = {n_g:.2f}, Gerber n = {safety_gerber(sa, smo, s_e):.2f}\n"
        f"Soderberg n = {safety_soderberg(sa, smo, s_e):.2f}, yield n = {safety_yield(sa, smo):.2f}"
    )
    ax.annotate(
        text,
        (smo / MPA, sa / MPA),
        xytext=(0.4, 0.56),
        textcoords="axes fraction",
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "0.3"},
    )
    ax.set(
        xlim=(0, S_UT / MPA * 1.02),
        ylim=(0, S_Y / MPA * 1.02),
        xlabel=r"mean stress $\sigma_m$ (MPa)",
        ylabel=r"stress amplitude $\sigma_a$ (MPa)",
        title=f"(b) Haigh diagram, $S_{{ut}}$ = {S_UT / MPA:.0f} MPa, $S_y$ = {S_Y / MPA:.0f} MPa",
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, lw=0.5, alpha=0.5)


def plot_history(ax, history):
    shown = 60
    ax.plot(
        np.arange(shown),
        history[:shown] / MPA,
        color="tab:blue",
        marker="o",
        ms=3,
        lw=1,
    )
    ax.axhline(
        HISTORY_MEAN / MPA,
        color="0.4",
        lw=0.8,
        ls="--",
        label=f"mean {HISTORY_MEAN / MPA:.0f} MPa",
    )
    ax.set(
        xlabel="reversal number",
        ylabel=r"stress $\sigma$ (MPa)",
        title=f"(c) First {shown} of {history.size} reversals of the random block",
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, lw=0.5, alpha=0.5)


def plot_damage(ax, amp, counts, damage, total, s_e):
    bins = np.linspace(0, amp.max() / MPA * 1.02, 16)
    hist, _ = np.histogram(amp / MPA, bins=bins, weights=counts)
    dmg, _ = np.histogram(amp / MPA, bins=bins, weights=damage)
    centers = 0.5 * (bins[1:] + bins[:-1])
    width = 0.9 * (bins[1] - bins[0])
    ax.bar(
        centers, hist, width=width, color="tab:blue", alpha=0.7, label="counted cycles"
    )
    ax.set(
        xlabel=r"Goodman-equivalent amplitude $\sigma_{ar}$ (MPa)",
        ylabel="cycles per block",
    )
    ax.axvline(
        s_e / MPA,
        color="tab:red",
        lw=1.2,
        ls="--",
        label=f"$S_e$ = {s_e / MPA:.0f} MPa",
    )
    twin = ax.twinx()
    twin.plot(
        centers, 100 * dmg / total, "s-", color="tab:orange", label="share of damage"
    )
    twin.set_ylabel("share of block damage (%)")
    ax.set_title(
        f"(d) Rainflow + Miner: D = {total:.2e} per block, life = {1 / total:.0f} blocks"
    )
    lines = ax.get_legend_handles_labels()
    lines2 = twin.get_legend_handles_labels()
    ax.legend(
        lines[0] + lines2[0], lines[1] + lines2[1], loc="upper center", fontsize=9
    )
    ax.grid(True, lw=0.5, alpha=0.5)


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    s_e_prime, s_e = endurance_limits()
    for name, value in marin_factors().items():
        print(f"{name} = {value:.3f}")
    a, b = basquin_constants(s_e)
    print(f"S'_e = {s_e_prime / MPA:.1f} MPa, S_e = {s_e / MPA:.1f} MPa")
    print(f"f = {fatigue_strength_fraction():.4f}, a = {a / MPA:.1f} MPa, b = {b:.5f}")
    sa, sm = OPERATING_AMPLITUDE, OPERATING_MEAN
    print(
        f"operating point: Goodman {safety_goodman(sa, sm, s_e):.3f}, "
        f"Gerber {safety_gerber(sa, sm, s_e):.3f}, Soderberg "
        f"{safety_soderberg(sa, sm, s_e):.3f}, yield {safety_yield(sa, sm):.3f}"
    )
    history = random_history()
    cycles = rainflow(history, repeating=True)
    total, amp, counts, damage = miner_damage(cycles, s_e)
    print(
        f"rainflow: {counts.sum():.1f} cycles per block, Miner damage {total:.3e}, "
        f"life {1 / total:.0f} blocks"
    )

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    plot_sn(axes[0, 0], s_e_prime, s_e)
    plot_haigh(axes[0, 1], s_e)
    plot_history(axes[1, 0], history)
    plot_damage(axes[1, 1], amp, counts, damage, total, s_e)
    fig.tight_layout()

    finish_figures(
        {"fatigue_sn_and_goodman.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
