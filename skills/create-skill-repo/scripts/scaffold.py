#!/usr/bin/env python3
"""Scaffold a new Agent Skills repository as a GitHub repo (gh repo create).

Usage:
    scaffold.py <name> --description "One engaging benefit-led sentence" --idea "High-level intent"
                [--owner Paldom] [--gitignore Python] [--public] [--topics t1,t2]
                [--dest DIR] [--template DIR] [--local-only] [--no-git] [--keep-on-fail]

Default flow: create the repo on GitHub via `gh repo create <owner>/<name> --private
-d <description> --gitignore <tech> --license mit --add-readme --clone`, use the
clone as the folder, overlay the bundled template into it (tokens substituted, JSON-escaped
inside *.json; the GitHub tech .gitignore is merged, README/LICENSE stubs
replaced), chmod hooks/scripts, VALIDATE, set repo topics. The script NEVER runs
`git commit` or `git push` - the overlay stays in the working tree for the owner
to review, commit, and push. The seeded .local/PROMPT.md goal must fit in 4000
characters (enforced before any network action). On any failure after creation
the local clone is removed unless --keep-on-fail, and remote-cleanup
instructions are printed (the script never deletes remote repos either).
`--local-only` is the offline mode (folder + git init, no GitHub). The final
line on success is `SCAFFOLD OK: <path>` (grep for it). Stdlib only.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
OWNER_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$")
GITIGNORE_RE = re.compile(r"^[A-Za-z0-9+._-]+$")
TOPIC_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,34}$")
RESERVED = ("claude", "anthropic")
DEFAULT_TOPICS = ("agent-skills", "claude-code", "skills", "skills-sh")
SKIP_FILES = {".DS_Store"}
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")


def fail(msg: str, dest: Path | None = None, keep: bool = False,
         remote_note: str | None = None) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    if dest is not None and dest.exists() and not keep:
        shutil.rmtree(dest, ignore_errors=True)
        print(f"Cleaned up partial scaffold at {dest}", file=sys.stderr)
    elif dest is not None and dest.exists():
        print(f"Partial scaffold kept at {dest} (--keep-on-fail)", file=sys.stderr)
    if remote_note:
        print(remote_note, file=sys.stderr)
    sys.exit(1)


def delete_hint(remote: str) -> str:
    return ("  Delete it with: gh auth refresh -h github.com -s delete_repo"
            f" && gh repo delete {remote} --yes\n"
            "  (or via the repository's Settings page on GitHub)")


def bundled_template(script_path: Path) -> Path:
    """The repo scaffold ships inside this skill: <skill>/assets/template."""
    return script_path.parent.parent / "assets" / "template"


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    except (OSError, FileNotFoundError) as exc:
        return subprocess.CompletedProcess(cmd, 127, stdout="", stderr=f"{cmd[0]}: {exc}")


def is_our_clone(dest: Path, remote: str) -> bool:
    """True only if dest is a git clone whose origin points at <remote>."""
    if not (dest / ".git").is_dir():
        return False
    url = run(["git", "remote", "get-url", "origin"], dest).stdout.strip()
    url = url.removesuffix(".git")
    return url.endswith(f"github.com/{remote}") or url.endswith(f"github.com:{remote}")


def merged_gitignore(existing: str, ours: str) -> str:
    """Append our template .gitignore to the GitHub-generated tech one, skipping
    pattern lines the tech template already covers (comments are kept)."""
    have = {ln.strip() for ln in existing.splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")}
    block = [ln for ln in ours.splitlines()
             if not (ln.strip() and not ln.lstrip().startswith("#") and ln.strip() in have)]
    return (existing.rstrip("\n") + "\n\n# --- Agent Skills scaffold ---\n"
            + "\n".join(block).strip("\n") + "\n")


def gh_auth_check(cwd: Path) -> None:
    """Verify the ACTIVE github.com account is authenticated with the workflow
    scope (gh auth status exits 1 if ANY known account is broken, so scope the
    check to the active one where supported)."""
    auth = run(["gh", "auth", "status", "--hostname", "github.com", "--active"], cwd)
    if auth.returncode != 0 and "unknown flag" in (auth.stderr or "").lower():
        auth = run(["gh", "auth", "status", "--hostname", "github.com"], cwd)
    if auth.returncode != 0:
        fail("gh is not authenticated — run `gh auth login` first (or use --local-only)\n"
             + (auth.stderr or auth.stdout).strip())
    scopes_line = next((ln for ln in (auth.stdout + auth.stderr).splitlines()
                        if "Token scopes:" in ln), "")
    if scopes_line and "workflow" not in scopes_line:
        fail("the gh token lacks the `workflow` scope (needed to push .github/workflows/) — "
             "run: gh auth refresh -h github.com -s workflow")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("name", help="kebab-case repo name, e.g. python-skills or icon-designer")
    ap.add_argument("--description", required=True,
                    help="one professional, benefit-led sentence; becomes the GitHub repo description and README intro")
    ap.add_argument("--idea", required=True, help="the user's high-level intent; seeds .local/PROMPT.md")
    ap.add_argument("--owner", default=None, help="GitHub owner/org (default: the authenticated gh user)")
    ap.add_argument("--gitignore", default="Python", metavar="TEMPLATE",
                    help="GitHub .gitignore template for the repo's technology (default: Python; see gh api gitignore/templates)")
    ap.add_argument("--public", action="store_true", help="create the repo public (default: private)")
    ap.add_argument("--topics", default="", help="extra comma-separated repo topics (added to the defaults)")
    ap.add_argument("--dest", type=Path, default=None, help="parent directory (default: current directory)")
    ap.add_argument("--template", type=Path, default=None, help="template directory override")
    ap.add_argument("--local-only", action="store_true",
                    help="offline mode: local folder + git init, no GitHub repo")
    ap.add_argument("--no-git", action="store_true", help="implies --local-only and skips git init/commit")
    ap.add_argument("--keep-on-fail", action="store_true", help="keep the folder if scaffolding fails")
    args = ap.parse_args()
    if args.no_git:
        args.local_only = True

    # ---- input validation (all before any filesystem or network change) ----
    name = args.name.strip()
    if not NAME_RE.match(name):
        fail(f"name {name!r} must be kebab-case: ^[a-z0-9]+(-[a-z0-9]+)*$")
    if len(name) > 64:
        fail(f"name is {len(name)} chars (max 64)")
    for word in RESERVED:
        if word in name:
            fail(f"name must not contain reserved word {word!r}")
    description = args.description.strip()
    if len(description) < 20 or any(ord(c) < 32 or ord(c) == 127 for c in description):
        fail("--description must be a single substantial line (>= 20 chars, no control characters)")
    if len(description) > 350:
        fail(f"--description is {len(description)} chars (max 350 — it becomes the GitHub repo description)")
    idea = args.idea.strip()
    if len(idea) < 10 or any((ord(c) < 32 and c != "\n") or ord(c) == 127 for c in idea):
        fail("--idea must carry real intent (>= 10 chars; newlines allowed, other control characters not)")
    for label, value in (("--description", description), ("--idea", idea)):
        m = PLACEHOLDER_RE.search(value)
        if m:
            fail(f"{label} contains {m.group(0)!r}, which collides with the template's "
                 "{{TOKEN}} placeholders — rephrase it (e.g. lowercase or spaced braces)")
    if args.owner:
        owner = args.owner.strip()
    elif args.local_only:
        fail("--owner is required with --local-only (no gh session to resolve it from)")
    else:
        proc = run(["gh", "api", "user", "--jq", ".login"], Path.cwd())
        owner = proc.stdout.strip()
        if proc.returncode != 0 or not owner:
            fail("could not resolve the GitHub owner - run `gh auth login` or pass --owner")
    if not OWNER_RE.match(owner):
        fail(f"--owner {owner!r} is not a valid GitHub owner (letters/digits/hyphens, no spaces)")
    gitignore_tpl = args.gitignore.strip()
    if not GITIGNORE_RE.match(gitignore_tpl):
        fail(f"--gitignore {gitignore_tpl!r} is not a valid template name (see gh api gitignore/templates)")
    topics = list(DEFAULT_TOPICS) + [t.strip() for t in args.topics.split(",") if t.strip()]
    for t in topics:
        if not TOPIC_RE.match(t):
            fail(f"topic {t!r} is invalid (lowercase letters/digits/hyphens, must start alphanumeric, <= 35 chars)")

    if args.template:
        template = args.template.resolve()
        if not (template / "README.md").is_file():
            fail(f"--template {template} does not look like a template (no README.md)")
    else:
        template = bundled_template(Path(__file__).resolve())
        if not (template / "README.md").is_file():
            fail(f"bundled template missing at {template} - reinstall the skill or pass --template")
    # The seeded goal prompt must stay within the 4000-char /goal budget.
    prompt_tpl = template / ".local" / "PROMPT.md"
    if prompt_tpl.is_file():
        final_len = len(prompt_tpl.read_text(encoding="utf-8").replace("{{IDEA}}", idea))
        if final_len > 4000:
            fail(f"the seeded .local/PROMPT.md would be {final_len} chars (max 4000) - "
                 f"shorten --idea by at least {final_len - 4000} chars or trim the template prompt")
    dest_parent = (args.dest or Path.cwd()).resolve()
    if not dest_parent.is_dir():
        fail(f"--dest {dest_parent} does not exist or is not a directory")
    dest = dest_parent / name
    if dest.exists():
        fail(f"{dest} already exists — pick another name or remove it first")
    remote = f"{owner}/{name}"

    tokens = {
        "{{REPO_NAME}}": name,
        "{{REPO_TITLE}}": " ".join(part.capitalize() for part in name.split("-")),
        "{{REPO_DESCRIPTION}}": description,
        "{{GITHUB_OWNER}}": owner,
        "{{YEAR}}": str(datetime.date.today().year),
        "{{IDEA}}": idea,
    }

    # ---- GitHub preflight + repo creation (default mode) ----
    created_remote: str | None = None
    if not args.local_only:
        if run(["gh", "--version"], dest_parent).returncode != 0:
            fail("gh CLI not found — install it (https://cli.github.com) or use --local-only")
        gh_auth_check(dest_parent)
        if run(["gh", "repo", "view", remote], dest_parent).returncode == 0:
            fail(f"https://github.com/{remote} already exists — pick another name or delete it first")
        known = run(["gh", "api", "gitignore/templates", "--jq", ".[]"], dest_parent)
        if known.returncode == 0 and gitignore_tpl not in known.stdout.split():
            fail(f"--gitignore {gitignore_tpl!r} is not a GitHub template "
                 f"(names are case-sensitive; see gh api gitignore/templates)")
        if dest.exists():  # re-check right before creating (shrink the race window)
            fail(f"{dest} appeared while preparing — pick another name or remove it first")

        visibility = "--public" if args.public else "--private"
        proc = run(["gh", "repo", "create", remote, visibility,
                    "--description", description, "--gitignore", gitignore_tpl,
                    "--license", "mit", "--add-readme", "--clone"], dest_parent)
        if proc.returncode != 0:
            # Never delete or claim ownership of a remote we can't prove this run
            # created; only clean the local folder if it is provably our clone.
            note = None
            if run(["gh", "repo", "view", remote], dest_parent).returncode == 0:
                note = (f"NOTE: https://github.com/{remote} exists on GitHub. If this failed run "
                        f"created it (it did not exist during preflight), remove it:\n{delete_hint(remote)}")
            local = dest if is_our_clone(dest, remote) else None
            if local is None and dest.exists():
                print(f"NOTE: left {dest} untouched (not created by this run)", file=sys.stderr)
            fail(f"gh repo create failed: {(proc.stderr or proc.stdout).strip()}",
                 local, args.keep_on_fail, note)
        created_remote = remote
        print((proc.stdout or "").strip() or f"Created https://github.com/{remote}")
        if not (dest / ".git").is_dir():
            fail(f"gh repo create did not clone into {dest} as expected",
                 dest if is_our_clone(dest, remote) else None, args.keep_on_fail,
                 f"NOTE: the remote repo https://github.com/{remote} was created by this run "
                 f"and still exists.\n{delete_hint(remote)}")
    else:
        try:
            dest.mkdir(parents=False, exist_ok=False)
        except OSError as exc:
            fail(f"could not create {dest}: {exc}")

    remote_note = (f"NOTE: the remote repo https://github.com/{remote} was created by this run "
                   f"and still exists.\n{delete_hint(remote)}") if created_remote else None
    try:
        scaffold_into(template, dest, tokens, args, created_remote, remote_note, topics)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - cleanup guarantee over specificity
        fail(f"unexpected error while scaffolding: {exc!r}", dest, args.keep_on_fail, remote_note)
    return 0


def scaffold_into(template: Path, dest: Path, tokens: dict, args,
                  remote: str | None, remote_note: str | None, topics: list[str]) -> None:
    name = tokens["{{REPO_NAME}}"]
    owner = tokens["{{GITHUB_OWNER}}"]
    keep = args.keep_on_fail

    # ---- overlay the bundled template into dest with token substitution ----
    leftover: list[str] = []
    for src in sorted(template.rglob("*")):
        if not src.is_file() or src.name in SKIP_FILES:
            continue
        rel = src.relative_to(template)
        if rel.name == "_gitignore":
            rel = rel.with_name(".gitignore")
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            text = src.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            shutil.copy2(src, target)  # binary asset: copy verbatim
            continue
        is_json = src.suffix == ".json"
        for token, value in tokens.items():
            # json.dumps produces a quoted JSON string; strip the quotes to get
            # the escaped payload so quotes/backslashes can't corrupt manifests.
            text = text.replace(token, json.dumps(value)[1:-1] if is_json else value)
        if rel == Path(".gitignore") and target.is_file():
            text = merged_gitignore(target.read_text(encoding="utf-8"), text)
        target.write_text(text, encoding="utf-8")
        for m in PLACEHOLDER_RE.finditer(text):
            leftover.append(f"{rel}: {m.group(0)}")
    if leftover:
        fail("unreplaced placeholder tokens:\n  " + "\n  ".join(leftover), dest, keep, remote_note)

    for script_dir in (dest / "scripts", dest / ".claude" / "hooks"):
        if script_dir.is_dir():
            for f in script_dir.glob("*.py"):
                f.chmod(f.stat().st_mode | 0o111)

    # ---- validate BEFORE any commit so broken scaffolds are never committed ----
    validator = dest / "scripts" / "validate_skills.py"
    proc = run([sys.executable, str(validator), "--root", str(dest)], dest)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    if proc.returncode != 0:
        fail("validator failed on the fresh scaffold (see report above)", dest, keep, remote_note)

    # ---- git: repo setup only. The script NEVER commits or pushes - the
    # overlay stays in the working tree for the owner to review and commit. ----
    branch = "main"
    if not args.no_git:
        if remote is None:  # local-only: init the repo (no commit)
            proc = run(["git", "init", "-b", "main"], dest)
            if proc.returncode != 0:  # git < 2.28 has no -b (or git is missing entirely)
                proc = run(["git", "init"], dest)
                if proc.returncode != 0:
                    fail(f"git init failed: {proc.stderr.strip()}", dest, keep, remote_note)
                proc = run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], dest)
                if proc.returncode != 0:
                    fail(f"could not set default branch to main: {proc.stderr.strip()}", dest, keep, remote_note)
        else:
            got = run(["git", "symbolic-ref", "--short", "HEAD"], dest).stdout.strip()
            branch = got or branch
            if branch != "main":
                print(f"WARNING: default branch is {branch!r}, not 'main' — CI push triggers and "
                      "the ruleset advice below assume main; consider renaming.", file=sys.stderr)

    # ---- repo polish (non-fatal): topics improve GitHub discoverability ----
    if remote is not None:
        cmd = ["gh", "repo", "edit", remote]
        for t in topics:
            cmd += ["--add-topic", t]
        proc = run(cmd, dest)
        if proc.returncode != 0:
            print(f"WARNING: could not set topics ({(proc.stderr or proc.stdout).strip()}) — "
                  f"set them later with: gh repo edit {remote} --add-topic <topic>", file=sys.stderr)

    if remote is not None:
        print(f"\nCreated: https://github.com/{remote} ({'public' if args.public else 'private'}) — "
              "scaffold left UNCOMMITTED for your review")
    print(f"Scaffolded: {dest}")
    print("Next steps:")
    print(f"  1. review the scaffold, then commit + push it yourself:")
    print(f"     git -C {name} add -A && git -C {name} commit -m 'chore: scaffold {name}'"
          + (f" && git -C {name} push" if remote is not None else ""))
    print(f"  2. (optional) drop research/sources into {name}/.local/")
    print(f"  3. cd {name} && claude")
    print("  4. paste the contents of .local/PROMPT.md (starts with /goal)")
    step = 5
    if remote is None:
        print(f"  {step}. publish later: gh repo create {owner}/{name} --private --source {name} --push")
        step += 1
    if not args.public:
        print(f"  {step}. when ready to go public: gh repo edit {owner}/{name} --visibility public"
              " --accept-visibility-change-consequences")
        step += 1
    print(f"  {step}. then on GitHub: enable Private Vulnerability Reporting (public repos only;"
          " Settings -> Advanced Security)")
    print(f"     and add a ruleset on {branch}: require PR + code-owner review + the `validate` check,"
          " block force pushes")
    print(f"SCAFFOLD OK: {dest}")


if __name__ == "__main__":
    sys.exit(main())
