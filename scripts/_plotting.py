"""Shared layouts for examples that visualize the same numerical quantities."""

import matplotlib.pyplot as plt


def plot_pod_mode_pairs(x, y, t, modes, coefficients, energy_fractions=None):
    """Plot spatial contours beside their amplitude-scaled temporal coefficients.

    Spatial modes have shape (len(x), len(y), n_modes); coefficients have
    shape (n_modes, len(t)). Optional energy fractions are shown in titles.
    """
    n_modes = modes.shape[-1]
    if modes.shape != (len(x), len(y), n_modes) or coefficients.shape != (
        n_modes,
        len(t),
    ):
        raise ValueError("mode and coefficient shapes must match the spatial/time axes")
    if n_modes < 1:
        raise ValueError("at least one mode is needed for plotting")
    fig, axes = plt.subplots(n_modes, 2, figsize=(12, 10), squeeze=False)
    for i, (spatial_ax, temporal_ax) in enumerate(axes):
        title = f"Mode {i + 1}"
        if energy_fractions is not None:
            title += f" ({100 * energy_fractions[i]:.1f}% TKE)"
        contours = spatial_ax.contourf(x, y, modes[:, :, i].T, cmap="jet", levels=50)
        fig.colorbar(contours, ax=spatial_ax)
        spatial_ax.set(xlabel="x (mm)", ylabel="y (mm)", title=title)
        temporal_ax.plot(t, coefficients[i])
        temporal_ax.set(xlabel="t (s)", ylabel=f"$a_{i + 1}(t)$", title=title)
    fig.tight_layout()
    return fig
