#!/usr/bin/env python3
"""Regenerate the content counts and the script index in README.md.

The generated blocks sit between ``<!-- BEGIN GENERATED: name -->`` and
``<!-- END GENERATED: name -->`` markers. Script titles come from the first
``#`` heading of each script README and descriptions from the first sentence
of its first paragraph.

Usage::

    python tools/generate_index.py          # rewrite README.md in place
    python tools/generate_index.py --check  # exit 1 if README.md is out of date
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

CATEGORIES = [
    ("algorithms", "Algorithms"),
    ("plots", "Plots"),
    ("simulations", "Simulations"),
]

EXERCISES_HEADING = re.compile(r"^#{1,6}\s+Exercises\s*$", re.MULTILINE)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def leaf_notes(folder):
    return sorted(p for p in (ROOT / folder).rglob("*.md") if p.name != "README.md")


def script_dirs(category):
    return sorted(p.parent for p in (ROOT / "scripts" / category).glob("*/main.py"))


def title_and_summary(readme):
    title, paragraph = None, []
    for line in readme.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if title is None:
            if stripped.startswith("# "):
                title = stripped[2:].strip()
            continue
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith(("#", "!", "<", "|", "```", "$$")):
            if paragraph:
                break
            continue
        paragraph.append(stripped)
    text = " ".join(paragraph)
    summary = SENTENCE_END.split(text, maxsplit=1)[0] if text else ""
    return title or readme.parent.name, summary


def stats_block():
    notes = leaf_notes("notes")
    with_exercises = sum(
        1 for p in notes if EXERCISES_HEADING.search(p.read_text(encoding="utf-8"))
    )
    rows = [
        ("Theory notes", len(notes), "[`notes/`](notes/)"),
        ("Notes with exercises", with_exercises, "[`notes/`](notes/)"),
        ("Practice guides", len(leaf_notes("practice")), "[`practice/`](practice/)"),
    ]
    names = {
        "algorithms": "Algorithm scripts",
        "plots": "Plot scripts",
        "simulations": "Simulations",
    }
    for key, _ in CATEGORIES:
        rows.append(
            (names[key], len(script_dirs(key)), f"[`scripts/{key}/`](scripts/{key}/)")
        )
    lines = ["| Content | Count | Location |", "| --- | --: | --- |"]
    lines += [f"| {name} | {count} | {where} |" for name, count, where in rows]
    return "\n".join(lines)


def scripts_block():
    parts = []
    for key, label in CATEGORIES:
        parts += [
            f"### {label}",
            "",
            "| Script | Description |",
            "| --- | --- |",
        ]
        for folder in script_dirs(key):
            title, summary = title_and_summary(folder / "README.md")
            rel = folder.relative_to(ROOT).as_posix()
            summary = summary.replace("|", "\\|")
            parts.append(f"| [{title}]({rel}/) | {summary} |")
        parts.append("")
    return "\n".join(parts).rstrip()


def replace_block(text, name, body):
    pattern = re.compile(
        rf"(<!-- BEGIN GENERATED: {name} -->).*?(<!-- END GENERATED: {name} -->)",
        re.DOTALL,
    )
    if not pattern.search(text):
        raise SystemExit(f"README.md is missing the '{name}' generated-block markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n\n{body}\n\n{m.group(2)}", text)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check", action="store_true", help="fail if README.md is stale"
    )
    args = parser.parse_args(argv)

    current = README.read_text(encoding="utf-8")
    updated = replace_block(current, "stats", stats_block())
    updated = replace_block(updated, "scripts", scripts_block())

    if args.check:
        if updated != current:
            print("README.md is out of date; run: python tools/generate_index.py")
            return 1
        print("README.md index is up to date")
        return 0

    if updated != current:
        README.write_text(updated, encoding="utf-8")
        print("README.md updated")
    else:
        print("README.md already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
