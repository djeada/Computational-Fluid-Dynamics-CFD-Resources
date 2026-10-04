"""Shared command-line and figure output conventions for the examples.

Keep numerical algorithms and animation lifecycles in the individual examples.
This module imports no plotting libraries so --help stays inexpensive.
"""

import argparse
from pathlib import Path


def positive_int(value: str) -> int:
    """Parse a positive iteration count for argparse."""
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive integer") from exc
    if result < 1:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return result


def positive_float(value: str) -> float:
    """Parse a positive, finite duration or rate for argparse."""
    try:
        result = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive number") from exc
    if not 0 < result < float("inf"):
        raise argparse.ArgumentTypeError("expected a positive number")
    return result


def create_parser(description: str) -> argparse.ArgumentParser:
    """Create an example parser with the shared display and output options."""
    parser = argparse.ArgumentParser(description=description.splitlines()[0])
    parser.add_argument("--no-show", action="store_true", help="do not open a window")
    parser.add_argument(
        "--output", type=Path, metavar="DIR", help="save PNG output in DIR"
    )
    return parser


def save_figure(figure, output: Path, filename: str, **kwargs) -> None:
    """Save a figure using the repository's PNG resolution and cropping."""
    output.mkdir(parents=True, exist_ok=True)
    figure.savefig(output / filename, dpi=100, bbox_inches="tight", **kwargs)


def finish_figures(
    figures: dict, output: Path | None = None, show: bool = True
) -> None:
    """Save and display named figures, then close only the figures we own.

    Keys are output filenames, including the .png extension. Closing runs even
    when saving raises, so repeated programmatic runs do not leak figures.
    """
    import matplotlib.pyplot as plt

    try:
        if output is not None:
            for filename, figure in figures.items():
                save_figure(figure, output, filename)
        if show:
            plt.show()
    finally:
        for figure in figures.values():
            plt.close(figure)
