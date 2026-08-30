#!/usr/bin/env python3
"""Fail when a file that is deliberately duplicated in this repo drifts apart.

Two kinds of copy exist here, and nothing else compares either of them:

  1. The scaffold template (`skills/create-skill-repo/assets/template/`) ships the
     gate — validator, eval runner, hooks, authoring docs — and those copies are
     what every scaffolded repo inherits. A fix applied only at the top level
     silently never reaches a repo the kit creates.
  2. `docs/*.md` is mirrored into `skills/*/references/` so an installed skill
     carries its own rulebook and works outside this repo.

Both are ordinary files, not symlinks. This script is the missing comparison.

Files that legitimately diverge (deploying.md, ci.yml, Makefile, README, and the
`references/evals.md` copies, which carry skill-specific sections) are absent from
PAIRS on purpose. Add a pair only when the two copies must be byte-identical.

Usage: python3 scripts/check_sync.py [--fix]
Exit codes: 0 = in sync, 1 = drift (or a source file is missing).
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATE = "skills/create-skill-repo/assets/template"

# (source of truth, mirror that must match it byte for byte)
PAIRS: tuple[tuple[str, str], ...] = (
    # 1. the scaffold template
    ("scripts/validate_skills.py", f"{TEMPLATE}/scripts/validate_skills.py"),
    ("scripts/run_evals.py", f"{TEMPLATE}/scripts/run_evals.py"),
    ("scripts/test_run_evals.py", f"{TEMPLATE}/scripts/test_run_evals.py"),
    ("scripts/test_validate_skills.py", f"{TEMPLATE}/scripts/test_validate_skills.py"),
    ("docs/skill-authoring.md", f"{TEMPLATE}/docs/skill-authoring.md"),
    ("docs/evals.md", f"{TEMPLATE}/docs/evals.md"),
    ("docs/readme-standard.md", f"{TEMPLATE}/docs/readme-standard.md"),
    (".claude/hooks/validate_skill_file.py", f"{TEMPLATE}/.claude/hooks/validate_skill_file.py"),
    (".claude/hooks/guard_bash.py", f"{TEMPLATE}/.claude/hooks/guard_bash.py"),
    (".claude/hooks/lint_python_file.py", f"{TEMPLATE}/.claude/hooks/lint_python_file.py"),
    (".claude/settings.json", f"{TEMPLATE}/.claude/settings.json"),
    # The quality toolchain a scaffolded repo inherits.
    ("ruff.toml", f"{TEMPLATE}/ruff.toml"),
    (".pre-commit-config.yaml", f"{TEMPLATE}/.pre-commit-config.yaml"),
    ("requirements-dev.txt", f"{TEMPLATE}/requirements-dev.txt"),
    # 2. the rulebook each authoring skill ships with itself
    ("docs/skill-authoring.md", "skills/add-skill/references/skill-authoring.md"),
    ("docs/skill-authoring.md", "skills/skill-from-research/references/skill-authoring.md"),
)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", type=Path, default=Path.cwd(), help="repo root (default: cwd)")
    ap.add_argument("--fix", action="store_true", help="copy each source over its mirror")
    args = ap.parse_args()

    root = args.root.resolve()
    drifted: list[str] = []
    for src_rel, dst_rel in PAIRS:
        source, mirror = root / src_rel, root / dst_rel
        if not source.is_file():
            print(f"ERROR {src_rel}: listed in PAIRS but missing from the repo", file=sys.stderr)
            drifted.append(dst_rel)
            continue
        if mirror.is_file() and mirror.read_bytes() == source.read_bytes():
            continue
        if args.fix:
            mirror.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, mirror)
            print(f"synced {dst_rel}")
        else:
            what = "differs from" if mirror.is_file() else "is missing, expected a copy of"
            print(
                f"ERROR {dst_rel}: {what} {src_rel} — run `python3 scripts/check_sync.py --fix`",
                file=sys.stderr,
            )
            drifted.append(dst_rel)

    if args.fix:
        print("OK: copies synced")
        return 0
    print(f"{'FAIL' if drifted else 'OK'}: {len(drifted)} copy/copies out of sync")
    return 1 if drifted else 0


if __name__ == "__main__":
    sys.exit(main())
