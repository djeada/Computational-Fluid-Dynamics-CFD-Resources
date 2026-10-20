"""Sobol sensitivity indices of a synthetic drag model by the Saltelli scheme.

A synthetic drag coefficient C_d(p_1, ..., p_5) with linear main effects, one
two-parameter interaction, one quadratic effect and one inert parameter has
first-order and total Sobol indices that can be written down exactly. The
script estimates both sets of indices with the Saltelli sampling scheme
(first-order estimator of Saltelli et al. 2010, total-effect estimator of
Jansen 1999), compares the estimates with the analytic values, and plots the
estimation error against the number of model evaluations for plain Monte Carlo
and scrambled Sobol (quasi-Monte Carlo) samples.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import qmc

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 11
CD_BASE = 0.30  # drag coefficient of the baseline car (x = 0)
LINEAR = np.array([0.012, 0.008, 0.006, 0.004, 0.0])  # dC_d per unit x_i
INTERACTION_13 = 0.010  # coefficient of x_1 x_3
QUADRATIC_4 = 0.006  # coefficient of x_4^2
PARAMETER_NAMES = [
    "rear window\nangle",
    "ride\nheight",
    "diffuser\nangle",
    "trunk lid\nangle",
    "battery\nz-position",
]
N_BAR = 2**13  # base sample size for the bar chart
N_CONVERGENCE = 2 ** np.arange(5, 15)  # base sample sizes for the error plot
N_REPEATS = 20  # independent repetitions per sample size


def drag_model(p):
    """Synthetic C_d for normalised parameters p in [0, 1]^5 (rows are designs)."""
    x = 2.0 * np.asarray(p) - 1.0  # map to [-1, 1]
    return (
        CD_BASE
        + x @ LINEAR
        + INTERACTION_13 * x[:, 0] * x[:, 2]
        + QUADRATIC_4 * (x[:, 3] ** 2 - 1.0 / 3.0)
    )


def analytic_indices():
    """Exact first-order and total indices for x_i ~ U(-1, 1) independent.

    Var(x) = 1/3, Var(x^2) = 4/45 and Var(x_1 x_3) = 1/9; all terms of the
    model are mutually uncorrelated, so the variance splits term by term.
    """
    partial = LINEAR**2 / 3.0
    partial[3] += QUADRATIC_4**2 * 4.0 / 45.0
    v_13 = INTERACTION_13**2 / 9.0
    total_variance = partial.sum() + v_13
    first = partial / total_variance
    total = first.copy()
    total[[0, 2]] += v_13 / total_variance
    return first, total, total_variance


def saltelli_indices(model, a, b):
    """First-order (Saltelli 2010) and total (Jansen 1999) index estimates.

    a and b are independent (N, k) sample matrices. The cost is N (k + 2)
    model evaluations. Outputs are centred by their sample mean first.
    """
    f_a, f_b = model(a), model(b)
    # Subtracting the sample mean leaves the estimators unbiased but removes
    # the large-mean noise term (C_d is about 0.3, its spread only about 0.01).
    offset = np.mean(np.concatenate([f_a, f_b]))
    f_a, f_b = f_a - offset, f_b - offset
    variance = np.var(np.concatenate([f_a, f_b]))
    k = a.shape[1]
    first = np.empty(k)
    total = np.empty(k)
    for i in range(k):
        ab = a.copy()
        ab[:, i] = b[:, i]  # A with column i taken from B
        f_ab = model(ab) - offset
        first[i] = np.mean(f_b * (f_ab - f_a)) / variance
        total[i] = 0.5 * np.mean((f_a - f_ab) ** 2) / variance
    return first, total


def sample_matrices(n, k, rng, method):
    """Two independent (n, k) matrices from Monte Carlo or scrambled Sobol."""
    if method == "mc":
        points = rng.random((n, 2 * k))
    else:
        points = qmc.Sobol(d=2 * k, scramble=True, seed=rng).random(n)
    return points[:, :k], points[:, k:]


def convergence_study(n_values, rng, n_repeats=N_REPEATS):
    """RMS over repetitions of the largest index error, for MC and QMC."""
    first_exact, total_exact, _ = analytic_indices()
    k = LINEAR.size
    errors = {}
    for method in ("mc", "qmc"):
        rows = []
        for n in n_values:
            worst = []
            for _ in range(n_repeats):
                a, b = sample_matrices(int(n), k, rng, method)
                first, total = saltelli_indices(drag_model, a, b)
                worst.append(
                    max(
                        np.abs(first - first_exact).max(),
                        np.abs(total - total_exact).max(),
                    )
                )
            rows.append(np.sqrt(np.mean(np.square(worst))))
        errors[method] = np.array(rows)
    return errors


def make_figure(first, total, first_exact, total_exact, n_values, errors):
    fig, (ax_bar, ax_conv) = plt.subplots(
        1, 2, figsize=(13, 5), gridspec_kw={"width_ratios": [1.4, 1.0]}
    )
    k = first.size
    pos = np.arange(k)
    width = 0.38
    ax_bar.bar(pos - width / 2, first, width, color="tab:blue", label="$S_i$ estimate")
    ax_bar.bar(
        pos + width / 2, total, width, color="tab:orange", label="$S_{Ti}$ estimate"
    )
    ax_bar.scatter(
        pos - width / 2, first_exact, marker="_", s=600, color="k", lw=2.5, zorder=3
    )
    ax_bar.scatter(
        pos + width / 2,
        total_exact,
        marker="_",
        s=600,
        color="k",
        lw=2.5,
        zorder=3,
        label="analytic value",
    )
    ax_bar.set_xticks(pos)
    ax_bar.set_xticklabels(
        [f"$p_{i + 1}$ {name}" for i, name in enumerate(PARAMETER_NAMES)]
    )
    ax_bar.set_ylabel("Sobol index")
    ax_bar.set_ylim(0.0, 0.7)
    ax_bar.set_title(f"Indices from N = {N_BAR} base samples ({N_BAR * (k + 2)} runs)")
    ax_bar.legend(loc="upper right")
    ax_bar.grid(True, axis="y", alpha=0.3)

    evaluations = n_values * (k + 2)
    ax_conv.loglog(
        evaluations, errors["mc"], "o-", color="tab:blue", label="Monte Carlo"
    )
    ax_conv.loglog(
        evaluations, errors["qmc"], "s-", color="tab:green", label="scrambled Sobol"
    )
    ref = errors["mc"][0] * np.sqrt(evaluations[0] / evaluations)
    ax_conv.loglog(evaluations, ref, "k--", lw=1, label=r"$\propto N^{-1/2}$")
    ax_conv.set_xlabel("model evaluations $N(k+2)$")
    ax_conv.set_ylabel("RMS of largest index error")
    ax_conv.set_title(f"Convergence ({N_REPEATS} repetitions per point)")
    ax_conv.grid(True, which="both", alpha=0.3)
    ax_conv.legend()

    fig.tight_layout()
    return fig


def parse_args(argv=None):
    return create_parser(__doc__).parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    rng = np.random.default_rng(SEED)
    first_exact, total_exact, variance = analytic_indices()
    a, b = sample_matrices(N_BAR, LINEAR.size, rng, "qmc")
    first, total = saltelli_indices(drag_model, a, b)
    print(f"Var(C_d) = {variance:.4e}")
    for i in range(LINEAR.size):
        print(
            f"p{i + 1}: S = {first[i]:.3f} (exact {first_exact[i]:.3f}), "
            f"S_T = {total[i]:.3f} (exact {total_exact[i]:.3f})"
        )
    errors = convergence_study(N_CONVERGENCE, rng)
    for n, e_mc, e_qmc in zip(N_CONVERGENCE, errors["mc"], errors["qmc"]):
        print(f"N = {n:6d}: MC error {e_mc:.4f}, Sobol error {e_qmc:.4f}")

    fig = make_figure(first, total, first_exact, total_exact, N_CONVERGENCE, errors)
    finish_figures(
        {"sobol_sensitivity_analysis.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
