#!/usr/bin/env python3
"""Render vertical Shorts/Reels videos of the simulations in one go.

Examples::

    python tools/make_reels.py --list
    python tools/make_reels.py lid_driven kelvin
    python tools/make_reels.py --seconds 20 --output reels --jobs 2
    python tools/make_reels.py lid_driven -- --compare-ghia

Each simulation runs headless from its own folder with ``--reel`` and writes
``OUTPUT/<simulation>.mp4`` (1080x1920 H.264). Arguments after ``--`` are
passed to every selected script. Long default runs (for example the lattice
Boltzmann flow) take as long as the simulation itself; ``--steps`` shortens
them.
"""

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_scripts import (  # noqa: E402
    ROOT,
    discover,
    headless_environment,
    positive_int,
    run,
)


@dataclass(frozen=True)
class ReelResult:
    name: str
    ok: bool
    elapsed: float
    output: str


def positive_float(value):
    try:
        result = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive number") from exc
    if not 0 < result < float("inf"):
        raise argparse.ArgumentTypeError("expected a positive number")
    return result


def simulations(filters):
    """Simulation scripts whose folder name contains any of the filters."""
    scripts = [s for s in discover([]) if s.parent.parent.name == "simulations"]
    if filters:
        scripts = [s for s in scripts if any(f in s.parent.name for f in filters)]
    return scripts


def is_mp4(path):
    """Cheap container check: an MP4 starts with an ``ftyp`` box."""
    try:
        with open(path, "rb") as stream:
            header = stream.read(12)
    except OSError:
        return False
    return len(header) == 12 and header[4:8] == b"ftyp"


def render(script, output, args):
    name = script.parent.name
    target = (output / f"{name}.mp4").resolve()
    command = [
        sys.executable, "main.py", "--reel", str(target),
        "--reel-seconds", str(args.seconds), "--reel-fps", str(args.fps),
    ]  # fmt: skip
    if args.steps is not None:
        command += ["--steps", str(args.steps)]
    command += args.extra
    started = time.monotonic()
    try:
        code, log, timed_out = run(
            command, script.parent, headless_environment(), args.timeout
        )
    except OSError as exc:
        return ReelResult(name, False, time.monotonic() - started, str(exc))
    elapsed = time.monotonic() - started
    if timed_out:
        return ReelResult(
            name, False, elapsed, f"timed out after {args.timeout}s\n{log}"
        )
    if code != 0:
        return ReelResult(name, False, elapsed, f"exit code {code}\n{log}")
    if not is_mp4(target):
        return ReelResult(name, False, elapsed, f"no MP4 written to {target}\n{log}")
    size = target.stat().st_size / 1e6
    return ReelResult(name, True, elapsed, f"{target} ({size:.1f} MB)")


def parse_args(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    extra = []
    if "--" in argv:
        split = argv.index("--")
        argv, extra = argv[:split], argv[split + 1 :]
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        epilog="Arguments after -- are passed to every selected simulation.",
    )
    parser.add_argument("filters", nargs="*", help="substrings of simulation names")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reels",
        metavar="DIR",
        help="folder for the MP4 files (default: reels/ in the repository)",
    )
    parser.add_argument(
        "--seconds", type=positive_float, default=30.0, help="reel length (default: 30)"
    )
    parser.add_argument(
        "--fps", type=positive_int, default=30, help="frame rate (default: 30)"
    )
    parser.add_argument(
        "--steps", type=positive_int, help="frames to simulate (default: per script)"
    )
    parser.add_argument(
        "--jobs", type=positive_int, default=2, help="reels rendered in parallel"
    )
    parser.add_argument(
        "--timeout",
        type=positive_int,
        default=3600,
        help="seconds per simulation (default: 3600)",
    )
    parser.add_argument(
        "--list", action="store_true", help="list matching simulations and exit"
    )
    args = parser.parse_args(argv)
    args.extra = extra
    return args


def main(argv=None):
    args = parse_args(argv)
    scripts = simulations(args.filters)
    if not scripts:
        print("no simulations matched")
        return 1
    if args.list:
        for script in scripts:
            print(script.parent.name)
        return 0

    args.output.mkdir(parents=True, exist_ok=True)
    results = []
    with ThreadPoolExecutor(args.jobs) as pool:
        jobs = [pool.submit(render, script, args.output, args) for script in scripts]
        for job in as_completed(jobs):
            result = job.result()
            results.append(result)
            summary = result.output if result.ok else "see log below"
            print(
                f"{'DONE' if result.ok else 'FAIL'}  {result.elapsed:7.1f}s  "
                f"{result.name}: {summary}",
                flush=True,
            )

    failures = sorted((r for r in results if not r.ok), key=lambda r: r.name)
    for result in failures:
        tail = "\n".join(result.output.strip().splitlines()[-20:])
        print(f"\n--- {result.name} ---\n{tail}")
    print(f"\n{len(results) - len(failures)}/{len(results)} reels written")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
