"""Fit a lift curve with stall using a numpy MLP, hand-written backprop and Adam.

Eighty noisy samples of a synthetic lift curve C_L(alpha) (thin-airfoil slope
blended into flat-plate post-stall lift) are split into 60 training and 20
validation points. A 1-32-32-1 tanh network is trained full-batch with Adam on
the mean-squared error. The figure shows the network prediction at several
epochs and the training and validation loss history.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0
N_SAMPLES = 80  # noisy C_L samples
N_VALIDATION = 20  # samples held out for validation
ALPHA_MIN, ALPHA_MAX = -10.0, 25.0  # angle-of-attack range, degrees
ALPHA_STALL = 14.0  # centre of the attached/separated blend, degrees
STALL_SHARPNESS = 0.6  # steepness of the blend, 1/degree
NOISE_STD = 0.03  # standard deviation of the C_L noise (dimensionless)
HIDDEN_LAYERS = (32, 32)  # neurons per hidden layer
EPOCHS = 2000  # full-batch Adam iterations
LEARNING_RATE = 1e-2  # initial Adam step size
FINAL_LEARNING_RATE = 1e-4  # step size after the last epoch (exponential decay)
SNAPSHOT_EPOCHS = (30, 150, 500, EPOCHS)  # epochs whose prediction is plotted


def lift_coefficient(alpha_deg):
    """Synthetic lift curve: 2*pi*alpha before stall, sin(2*alpha) after it."""
    alpha = np.radians(alpha_deg)
    attached = 2.0 * np.pi * alpha
    separated = np.sin(2.0 * alpha)
    blend = 1.0 / (1.0 + np.exp(-STALL_SHARPNESS * (alpha_deg - ALPHA_STALL)))
    return (1.0 - blend) * attached + blend * separated


def make_dataset(seed=SEED):
    """Return (alpha_train, cl_train, alpha_val, cl_val) as column vectors."""
    rng = np.random.default_rng(seed)
    alpha = rng.uniform(ALPHA_MIN, ALPHA_MAX, N_SAMPLES)
    cl = lift_coefficient(alpha) + NOISE_STD * rng.standard_normal(N_SAMPLES)
    order = rng.permutation(N_SAMPLES)
    val, train = order[:N_VALIDATION], order[N_VALIDATION:]
    return alpha[train, None], cl[train, None], alpha[val, None], cl[val, None]


def scale_alpha(alpha_deg):
    """Map the angle-of-attack range linearly onto [-1, 1]."""
    return 2.0 * (alpha_deg - ALPHA_MIN) / (ALPHA_MAX - ALPHA_MIN) - 1.0


def init_params(layer_sizes, rng):
    """Xavier (Glorot) normal weights and zero biases for each layer."""
    params = []
    for n_in, n_out in zip(layer_sizes[:-1], layer_sizes[1:]):
        weight = rng.standard_normal((n_in, n_out)) * np.sqrt(2.0 / (n_in + n_out))
        params.append((weight, np.zeros(n_out)))
    return params


def forward(params, x):
    """Return the network output and the layer activations needed by backward.

    Hidden layers use tanh, the output layer is linear. Rows of x are samples.
    """
    activations = [x]
    a = x
    for index, (weight, bias) in enumerate(params):
        z = a @ weight + bias
        a = z if index == len(params) - 1 else np.tanh(z)
        activations.append(a)
    return a, activations


def mse_loss(prediction, target):
    """Mean-squared error over all samples and outputs."""
    return float(np.mean((prediction - target) ** 2))


def backward(params, activations, target):
    """Gradients of the mean-squared error with respect to every (W, b).

    delta_L = 2 (y_hat - y) / N for the linear output; going back one layer,
    delta_{l-1} = (delta_l W_l^T) * (1 - a_{l-1}^2) for tanh.
    """
    prediction = activations[-1]
    delta = 2.0 * (prediction - target) / prediction.size
    grads = [None] * len(params)
    for index in range(len(params) - 1, -1, -1):
        weight, _ = params[index]
        a_prev = activations[index]
        grads[index] = (a_prev.T @ delta, delta.sum(axis=0))
        if index > 0:
            delta = (delta @ weight.T) * (1.0 - a_prev**2)
    return grads


class Adam:
    """Adam optimiser (Kingma and Ba, 2015) for a list of (W, b) tuples."""

    def __init__(self, params, lr=LEARNING_RATE, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr, self.beta1, self.beta2, self.eps = lr, beta1, beta2, eps
        self.m = [np.zeros_like(p) for pair in params for p in pair]
        self.v = [np.zeros_like(p) for pair in params for p in pair]
        self.t = 0

    def step(self, params, grads):
        """Return updated parameters after one Adam step."""
        self.t += 1
        flat_p = [p for pair in params for p in pair]
        flat_g = [g for pair in grads for g in pair]
        updated = []
        for i, (p, g) in enumerate(zip(flat_p, flat_g)):
            self.m[i] = self.beta1 * self.m[i] + (1.0 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1.0 - self.beta2) * g**2
            m_hat = self.m[i] / (1.0 - self.beta1**self.t)
            v_hat = self.v[i] / (1.0 - self.beta2**self.t)
            updated.append(p - self.lr * m_hat / (np.sqrt(v_hat) + self.eps))
        return [(updated[2 * k], updated[2 * k + 1]) for k in range(len(params))]


def train(
    params,
    x_train,
    y_train,
    epochs=EPOCHS,
    lr=LEARNING_RATE,
    lr_final=None,
    x_val=None,
    y_val=None,
    snapshot_epochs=(),
):
    """Full-batch Adam training on the mean-squared error.

    The step size decays exponentially from lr to lr_final (constant if
    lr_final is None).
    Returns the final parameters, a history dict with the training (and, if
    given, validation) loss after every epoch, and a dict of parameter copies
    at the requested snapshot epochs.
    """
    optimiser = Adam(params, lr=lr)
    history = {"train": np.empty(epochs), "val": np.empty(epochs)}
    snapshots = {}
    decay = 1.0 if lr_final is None else (lr_final / lr) ** (1.0 / max(epochs - 1, 1))
    for epoch in range(1, epochs + 1):
        optimiser.lr = lr * decay ** (epoch - 1)
        _, activations = forward(params, x_train)
        params = optimiser.step(params, backward(params, activations, y_train))
        history["train"][epoch - 1] = mse_loss(forward(params, x_train)[0], y_train)
        history["val"][epoch - 1] = (
            mse_loss(forward(params, x_val)[0], y_val) if x_val is not None else np.nan
        )
        if epoch in snapshot_epochs:
            snapshots[epoch] = [(w.copy(), b.copy()) for w, b in params]
    return params, history, snapshots


def fit_lift_curve(seed=SEED, epochs=EPOCHS):
    """Train on the synthetic lift-curve data and return everything to plot."""
    alpha_tr, cl_tr, alpha_va, cl_va = make_dataset(seed)
    cl_mean, cl_std = cl_tr.mean(), cl_tr.std()
    x_tr, x_va = scale_alpha(alpha_tr), scale_alpha(alpha_va)
    y_tr, y_va = (cl_tr - cl_mean) / cl_std, (cl_va - cl_mean) / cl_std

    rng = np.random.default_rng(seed + 1)
    params = init_params((1, *HIDDEN_LAYERS, 1), rng)
    snapshot_epochs = tuple(e for e in SNAPSHOT_EPOCHS if e <= epochs)
    params, history, snapshots = train(
        params,
        x_tr,
        y_tr,
        epochs,
        LEARNING_RATE,
        FINAL_LEARNING_RATE,
        x_va,
        y_va,
        snapshot_epochs,
    )
    # Report losses in physical units: MSE scales with the output variance.
    history = {key: value * cl_std**2 for key, value in history.items()}

    def predict(p, alpha_deg):
        return forward(p, scale_alpha(alpha_deg))[0] * cl_std + cl_mean

    return {
        "data": (alpha_tr, cl_tr, alpha_va, cl_va),
        "params": params,
        "history": history,
        "snapshots": snapshots,
        "predict": predict,
    }


def make_figure(result):
    alpha_tr, cl_tr, alpha_va, cl_va = result["data"]
    alpha_fine = np.linspace(ALPHA_MIN, ALPHA_MAX, 400)[:, None]
    history = result["history"]
    colors = plt.get_cmap("viridis")(np.linspace(0.0, 0.85, len(result["snapshots"])))

    fig, (ax_fit, ax_loss) = plt.subplots(1, 2, figsize=(13, 5))
    ax_fit.plot(
        alpha_fine, lift_coefficient(alpha_fine), "k--", lw=1.5, label="true $C_L$"
    )
    ax_fit.plot(alpha_tr, cl_tr, "o", color="0.45", ms=5, label="training samples")
    ax_fit.plot(
        alpha_va, cl_va, "s", mfc="none", mec="tab:red", ms=6, label="validation"
    )
    for color, (epoch, params) in zip(colors, result["snapshots"].items()):
        ax_fit.plot(
            alpha_fine,
            result["predict"](params, alpha_fine),
            color=color,
            lw=2,
            label=f"MLP, epoch {epoch}",
        )
    ax_fit.set_xlabel(r"angle of attack $\alpha$ [$^\circ$]", fontsize=12)
    ax_fit.set_ylabel("lift coefficient $C_L$ [-]", fontsize=12)
    ax_fit.set_title("Network prediction during training", fontsize=13)
    ax_fit.legend(fontsize=10, loc="upper left")
    ax_fit.grid(True, lw=0.5, alpha=0.5)

    epochs = np.arange(1, history["train"].size + 1)
    ax_loss.loglog(epochs, history["train"], color="tab:blue", label="training")
    ax_loss.loglog(epochs, history["val"], color="tab:red", label="validation")
    ax_loss.axhline(
        NOISE_STD**2, color="0.3", ls=":", label=r"noise variance $\sigma^2$"
    )
    ax_loss.set_xlabel("epoch", fontsize=12)
    ax_loss.set_ylabel(r"MSE [$C_L^2$]", fontsize=12)
    ax_loss.set_title("Loss history (full-batch Adam, decaying step)", fontsize=13)
    ax_loss.legend(fontsize=10)
    ax_loss.grid(True, which="both", lw=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    result = fit_lift_curve()
    train_mse, val_mse = result["history"]["train"][-1], result["history"]["val"][-1]
    print(f"final training RMSE   = {np.sqrt(train_mse):.4f}")
    print(f"final validation RMSE = {np.sqrt(val_mse):.4f}")
    print(f"noise standard deviation = {NOISE_STD:.4f}")

    finish_figures(
        {"mlp_regression.png": make_figure(result)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
