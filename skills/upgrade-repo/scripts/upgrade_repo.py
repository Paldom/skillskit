#!/usr/bin/env python3
"""Bring a repo scaffolded by an older skillskit up to the current template.

A scaffolded repo owns its files outright: it carries its own copy of the
validator, the eval runner, the hooks, the authoring docs, and the bundled dev
skills. Nothing links it back to skillskit, so an improvement shipped here never
reaches it. This script is that link, run on demand.

Two tiers, because the two kinds of file cannot be treated alike:

  MANAGED    infrastructure with no per-repo content — safe to overwrite with
             --apply once the user has seen the list.
  CUSTOMIZED files a repo is expected to edit (Makefile, CI, AGENTS.md,
             settings, toolchain config). One that EXISTS and differs is never
             written — merging it is a judgement call, and the upgrade log says
             what to merge. One the repo simply does not have yet is created:
             there is no customization to destroy, and without that a repo could
             never adopt a config file introduced after it was scaffolded.

Everything else is out of scope and untouched — above all `skills/`, which is
the repo's own product, plus README, CHANGELOG, skills.sh.json and the plugin
manifests, which are its identity.

Known limit: template files carrying `{{PLACEHOLDER}}` tokens (docs/deploying.md,
CONTRIBUTING.md, SECURITY.md, SUPPORT.md, the manifests) are substituted at
scaffold time, so a byte comparison would always differ. They are excluded from
both tiers; when one of them changes materially, the upgrade log says so.

Usage:
    python3 upgrade_repo.py --repo .                    # report drift
    python3 upgrade_repo.py --repo . --apply            # write the MANAGED tier
    python3 upgrade_repo.py --repo . --template DIR     # explicit template

Exit codes: 0 = repo already current (or --apply succeeded), 1 = drift found
(report mode) or the template could not be located.
"""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import sys
from pathlib import Path

MANAGED = (
    "scripts/validate_skills.py",
    "scripts/run_evals.py",
    "scripts/test_run_evals.py",
    "scripts/test_validate_skills.py",
    ".claude/hooks/validate_skill_file.py",
    ".claude/hooks/guard_bash.py",
    ".claude/hooks/lint_python_file.py",
    "docs/skill-authoring.md",
    "docs/evals.md",
    "docs/readme-standard.md",
    ".claude/skills/add-skill/SKILL.md",
    ".claude/skills/add-skill/evals/evals.json",
    ".claude/skills/publish-repo/SKILL.md",
    ".claude/skills/publish-repo/evals/evals.json",
)

CUSTOMIZED = (
    "Makefile",
    ".github/workflows/ci.yml",
    "AGENTS.md",
    ".claude/settings.json",
    # Toolchain config a repo is expected to tune: rule selection, extra hooks,
    # extra dev dependencies. Overwriting these would throw that tuning away.
    "ruff.toml",
    ".pre-commit-config.yaml",
    "requirements-dev.txt",
)

# Where a file the kit ships would live. Anything here that is in neither list
# above is unclassified — see check_coverage().
MANAGED_DIRS = ("scripts", ".claude/hooks", ".claude/skills", "docs")

# Substituted at scaffold time, so a byte comparison is meaningless.
PLACEHOLDER = "{{"

TEMPLATE_TAIL = Path("create-skill-repo") / "assets" / "template"


def find_template(explicit: Path | None, script: Path) -> Path | None:
    """Locate create-skill-repo's bundled template.

    Order: an explicit --template, then the sibling skill as installed next to
    this one, then the same sibling in a skillskit source checkout.
    """
    candidates: list[Path] = []
    if explicit:
        candidates.append(explicit)
    skill_dir = os.environ.get("CLAUDE_SKILL_DIR")
    if skill_dir:
        candidates.append(Path(skill_dir).parent / TEMPLATE_TAIL)
    # <root>/skills/upgrade-repo/scripts/this.py -> <root>/skills/create-skill-repo/...
    candidates.append(script.parent.parent.parent / TEMPLATE_TAIL)
    for candidate in candidates:
        if (candidate / "scripts" / "validate_skills.py").is_file():
            return candidate.resolve()
    return None


def check_coverage(template: Path) -> list[str]:
    """Template files under MANAGED_DIRS that neither list covers.

    Without this, adding a file to the template and forgetting to classify it
    here upgrades nothing and says nothing — the silent half-upgrade this whole
    skill exists to prevent.
    """
    known = set(MANAGED) | set(CUSTOMIZED)
    unclassified = []
    for directory in MANAGED_DIRS:
        base = template / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.name == ".DS_Store":
                continue
            rel = path.relative_to(template).as_posix()
            if rel in known:
                continue
            try:
                if PLACEHOLDER in path.read_text(encoding="utf-8"):
                    continue  # scaffold-substituted, deliberately out of scope
            except (OSError, UnicodeDecodeError):
                pass
            unclassified.append(rel)
    return unclassified


def classify(template: Path, repo: Path, group: tuple[str, ...]) -> tuple[list[str], list[str]]:
    """Split `group` into (differs, missing-from-repo). Absent upstream = skipped."""
    differs, missing = [], []
    for rel in group:
        source, target = template / rel, repo / rel
        if not source.is_file():
            continue  # not part of this template version
        if not target.exists():
            missing.append(rel)
        elif not filecmp.cmp(source, target, shallow=False):
            differs.append(rel)
    return differs, missing


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--repo", type=Path, default=Path.cwd(), help="repo to upgrade (default: cwd)")
    ap.add_argument("--template", type=Path, help="path to create-skill-repo's assets/template")
    ap.add_argument(
        "--apply", action="store_true", help="write the MANAGED tier (CUSTOMIZED is never written)"
    )
    args = ap.parse_args()

    repo = args.repo.resolve()
    template = find_template(args.template, Path(__file__).resolve())
    if template is None:
        print(
            "ERROR: could not locate skillskit's template. Install skillskit into this\n"
            "       repo and retry, or pass the path explicitly:\n"
            "         npx skills add Paldom/skillskit\n"
            "         python3 upgrade_repo.py --repo . --template <path>/skills/create-skill-repo/assets/template",
            file=sys.stderr,
        )
        return 1
    if not (repo / "scripts" / "validate_skills.py").is_file():
        print(
            f"ERROR: {repo} does not look like a skillskit-scaffolded repo "
            "(no scripts/validate_skills.py)",
            file=sys.stderr,
        )
        return 1

    print(f"template: {template}")
    print(f"repo:     {repo}\n")

    managed_diff, managed_missing = classify(template, repo, MANAGED)
    custom_diff, custom_missing = classify(template, repo, CUSTOMIZED)

    # A property of the template, not of this repo — so it is reported even when
    # the repo is otherwise current.
    unclassified = check_coverage(template)

    if not (managed_diff or managed_missing or custom_diff or custom_missing):
        print("OK: repo is current — every managed and customized file matches the template")
        if unclassified:
            print("\nUNCLASSIFIED (shipped by the template, covered by neither tier —")
            print("classify them in upgrade_repo.py; they are NOT being upgraded):")
            for rel in unclassified:
                print(f"  ? {rel}")
        return 0

    if managed_diff or managed_missing or custom_missing:
        verb = "applying" if args.apply else "would apply"
        print(f"MANAGED ({verb} — safe to write, nothing of yours is lost):")
        for rel in managed_missing:
            print(f"  + {rel}  (missing — new since this repo was scaffolded)")
        for rel in managed_diff:
            print(f"  ~ {rel}")
        # A customizable file the repo does not have yet has no customization to
        # destroy, so creating it is safe. Only a file that EXISTS and differs is
        # a judgement call — otherwise a repo could never adopt a new config at all.
        for rel in custom_missing:
            print(f"  + {rel}  (customizable, but absent — nothing to preserve)")
    if custom_diff:
        print("\nCUSTOMIZED (yours to merge — never written, and expected to keep")
        print("differing once merged; check each against the upgrade log):")
        for rel in custom_diff:
            print(f"  ! {rel}")
            print(f"      diff -u {repo / rel} {template / rel}")

    if unclassified:
        print("\nUNCLASSIFIED (shipped by the template, covered by neither tier —")
        print("classify them in upgrade_repo.py; they are NOT being upgraded):")
        for rel in unclassified:
            print(f"  ? {rel}")

    if not args.apply:
        print("\nReport only. Re-run with --apply to write the MANAGED tier.")
        return 1

    for rel in managed_missing + managed_diff + custom_missing:
        source, target = template / rel, repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if os.access(source, os.X_OK):
            target.chmod(target.stat().st_mode | 0o111)
    print(
        f"\nApplied {len(managed_missing) + len(managed_diff) + len(custom_missing)} file(s). "
        "Nothing under skills/ was touched, and no existing customized file was overwritten."
    )
    print("Next: read the upgrade log for manual follow-ups, then run `make check`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
