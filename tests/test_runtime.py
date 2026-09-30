"""Import safety, figure ownership, and subprocess runner failure reporting."""

import importlib.util
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from scripts._common import finish_figures  # noqa: E402
from tools import run_scripts  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


class FigureTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_finish_closes_owned_figures_and_preserves_other_figures(self):
        unrelated = plt.figure()
        owned = plt.figure()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "nested"
            finish_figures({"plot.png": owned}, output=target, show=False)
            self.assertTrue((target / "plot.png").is_file())
        self.assertTrue(plt.fignum_exists(unrelated.number))
        self.assertFalse(plt.fignum_exists(owned.number))

    def test_save_failure_still_closes_owned_figures(self):
        figure = plt.figure()
        with patch.object(figure, "savefig", side_effect=OSError("disk unavailable")):
            with tempfile.TemporaryDirectory() as directory, self.assertRaises(OSError):
                finish_figures({"plot.png": figure}, Path(directory), show=False)
        self.assertFalse(plt.fignum_exists(figure.number))

    def test_examples_import_without_running_or_opening_figures(self):
        for index, path in enumerate(sorted((ROOT / "scripts").glob("*/*/main.py"))):
            with self.subTest(path=path):
                name = f"import_safety_example_{index}"
                spec = importlib.util.spec_from_file_location(name, path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[name] = module
                with (
                    patch.object(
                        plt, "show", side_effect=AssertionError("show on import")
                    ),
                    patch.object(
                        plt, "figure", side_effect=AssertionError("figure on import")
                    ),
                    redirect_stdout(io.StringIO()) as output,
                ):
                    spec.loader.exec_module(module)
                self.assertEqual(output.getvalue(), "")
                self.assertTrue(callable(module.main))
                del sys.modules[name]


class RunnerTests(unittest.TestCase):
    def test_invalid_limits_are_rejected(self):
        for flag in ("--jobs", "--steps", "--timeout"):
            with (
                self.subTest(flag=flag),
                patch("sys.stderr", new=io.StringIO()),
                self.assertRaises(SystemExit) as error,
            ):
                run_scripts.parse_args([flag, "0"])
            self.assertEqual(error.exception.code, 2)

    def test_discovery_uses_repository_relative_names(self):
        self.assertEqual(len(run_scripts.discover([])), 57)
        matches = run_scripts.discover(["algorithms/pod"])
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].parent.name, "pod")

    def test_png_validation_rejects_missing_or_corrupt_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            self.assertIn("no PNG", run_scripts.validate_output(path))
            (path / "invalid.png").write_text("not an image")
            self.assertIn("invalid PNG", run_scripts.validate_output(path))
            (path / "invalid.png").unlink()
            figure = plt.figure()
            figure.savefig(path / "valid.png")
            plt.close(figure)
            self.assertIsNone(run_scripts.validate_output(path))

    def test_timeout_stops_subprocess(self):
        code, output, timed_out = run_scripts.run(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            ROOT,
            os.environ.copy(),
            0.05,
        )
        self.assertTrue(timed_out)
        self.assertIsNone(code)

    def test_help_failure_is_reported(self):
        script = run_scripts.discover(["algorithms/pod"])[0]
        with patch.object(run_scripts, "run", return_value=(2, "bad arguments", False)):
            result = run_scripts.run_script(script, 10, 30, "/unused")
        self.assertFalse(result.ok)
        self.assertIn("--help failed", result.output)
        self.assertIn("bad arguments", result.output)

    def test_execution_uses_remaining_timeout_and_optional_steps(self):
        script = run_scripts.discover(["algorithms/pod"])[0]
        with (
            patch.object(
                run_scripts,
                "run",
                side_effect=[(0, "--steps", False), (0, "done", False)],
            ) as run,
            patch.object(run_scripts, "validate_output", return_value=None),
            patch.object(run_scripts.time, "monotonic", side_effect=[10, 12, 15]),
        ):
            result = run_scripts.run_script(script, 7, 30, "/unused")
        self.assertTrue(result.ok)
        self.assertEqual(result.elapsed, 5)
        self.assertEqual(run.call_args.args[-1], 28)
        self.assertEqual(run.call_args.args[0][-2:], ["--steps", "7"])
