#!/usr/bin/env python3
"""Run examples headlessly, validate their PNGs, and report failures.

Examples::

    python tools/run_scripts.py
    python tools/run_scripts.py pod lid_driven --jobs 4
    python tools/run_scripts.py --output results --json-report results/report.json
    python tools/run_scripts.py --list

Each example runs from its own directory. --steps is passed only when --help
advertises it. --timeout covers both argument discovery and execution.
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JOBS = min(4, os.cpu_count() or 2)


@dataclass(frozen=True)
class ScriptResult:
    script: Path
    ok: bool
    elapsed: float
    output: str

    def to_dict(self):
        return {
            "script": self.script.as_posix(),
            "ok": self.ok,
            "elapsed_seconds": round(self.elapsed, 3),
            "output": self.output,
        }


def positive_int(value):
    """Reject invalid limits before creating threads or subprocesses."""
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive integer") from exc
    if result <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return result


def discover(filters):
    scripts = sorted((ROOT / "scripts").glob("*/*/main.py"))
    if filters:
        scripts = [
            script
            for script in scripts
            if any(
                value in script.parent.relative_to(ROOT).as_posix() for value in filters
            )
        ]
    return scripts


def headless_environment():
    """Set plotting/display backends and avoid BLAS oversubscription across jobs."""
    return dict(
        os.environ,
        MPLBACKEND="Agg",
        SDL_VIDEODRIVER="dummy",
        SDL_AUDIODRIVER="dummy",
        PYGAME_HIDE_SUPPORT_PROMPT="1",
        OPENBLAS_NUM_THREADS="1",
        OMP_NUM_THREADS="1",
        MKL_NUM_THREADS="1",
    )


def run(cmd, cwd, env, timeout):
    """Run a separate process group and kill its children on timeout."""
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    try:
        output, _ = proc.communicate(timeout=max(timeout, 0.001))
        return proc.returncode, output, False
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        output, _ = proc.communicate()
        return None, output, True


def validate_output(directory):
    """Check that output contains readable PNG images, not just named files."""
    from PIL import Image

    images = sorted(directory.glob("*.png"))
    if not images:
        return "no PNG written to --output"
    for path in images:
        try:
            with Image.open(path) as image:
                if image.format != "PNG":
                    return f"not a PNG: {path.name}"
                image.verify()
        except (OSError, SyntaxError) as exc:
            return f"invalid PNG {path.name}: {exc}"
    return None


def run_script(script, steps, timeout, out_root):
    relative = script.parent.relative_to(ROOT)
    environment = headless_environment()
    started = time.monotonic()

    def result(ok, output):
        return ScriptResult(relative, ok, time.monotonic() - started, output)

    try:
        code, help_text, timed_out = run(
            [sys.executable, "main.py", "--help"], script.parent, environment, timeout
        )
        if timed_out or code != 0:
            return result(
                False,
                "--help timed out:\n" + help_text
                if timed_out
                else "--help failed:\n" + help_text,
            )

        out_dir = Path(out_root) / "__".join(relative.parts)
        command = [sys.executable, "main.py", "--no-show", "--output", str(out_dir)]
        if "--steps" in help_text:
            command += ["--steps", str(steps)]
        remaining = timeout - (time.monotonic() - started)
        if remaining <= 0:
            return result(False, f"timed out after {timeout}s during --help")
        code, output, timed_out = run(command, script.parent, environment, remaining)
        if timed_out:
            return result(False, f"timed out after {timeout}s\n{output}")
        if code != 0:
            return result(False, f"exit code {code}\n{output}")
        error = validate_output(out_dir)
        return result(error is None, output if error is None else f"{error}\n{output}")
    except OSError as exc:
        return result(False, f"could not run script: {exc}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "filters", nargs="*", help="substrings of relative script paths"
    )
    parser.add_argument(
        "--steps", type=positive_int, default=10, help="value passed to --steps"
    )
    parser.add_argument(
        "--timeout",
        type=positive_int,
        default=120,
        help="seconds per example including --help",
    )
    parser.add_argument("--jobs", type=positive_int, default=DEFAULT_JOBS)
    parser.add_argument(
        "--list", action="store_true", help="list matching examples without running"
    )
    parser.add_argument(
        "--output",
        type=Path,
        metavar="DIR",
        help="retain PNGs in a new run directory under DIR",
    )
    parser.add_argument(
        "--json-report",
        type=Path,
        metavar="FILE",
        help="write results and full script logs as JSON",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    scripts = discover(args.filters)
    if not scripts:
        print("no scripts matched")
        return 1
    if args.list:
        for script in scripts:
            print(script.parent.relative_to(ROOT).as_posix())
        return 0

    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
        out_root = Path(tempfile.mkdtemp(prefix="run-", dir=args.output.resolve()))
        output_context = nullcontext(out_root)
        print(f"Keeping outputs in {out_root}", flush=True)
    else:
        output_context = tempfile.TemporaryDirectory()

    results = []
    with output_context as out_root, ThreadPoolExecutor(args.jobs) as pool:
        jobs = [
            pool.submit(run_script, script, args.steps, args.timeout, out_root)
            for script in scripts
        ]
        for job in as_completed(jobs):
            result = job.result()
            results.append(result)
            print(
                f"{'PASS' if result.ok else 'FAIL'}  {result.elapsed:6.1f}s  {result.script}",
                flush=True,
            )

    results.sort(key=lambda result: result.script)
    failures = [result for result in results if not result.ok]
    for result in failures:
        tail = "\n".join(result.output.strip().splitlines()[-20:])
        print(f"\n--- {result.script} ---\n{tail}")
    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "passed": len(results) - len(failures),
            "total": len(results),
            "output_directory": str(out_root) if args.output else None,
            "results": [result.to_dict() for result in results],
        }
        args.json_report.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\n{len(results) - len(failures)}/{len(results)} scripts passed")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
