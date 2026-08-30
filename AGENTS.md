# AGENTS.md

Canonical agent instructions for this repository — `CLAUDE.md` simply imports this
file, so every agent (Claude Code, Copilot, Cursor, Codex, …) reads the same rules.

Agent Skills repository — skills live in `skills/<name>/` (one purpose per skill),
distributed via the plugin manifest in `.claude-plugin/`.

## Commands

- Validate everything (the only gate): `make check` — validator (frontmatter,
  evals, security rules, manifests), `make lint` (ruff), `make evals` (trigger
  scoring), then the self-checks and the copy-sync check
- Validate one file: `python3 scripts/validate_skills.py --file skills/<name>/SKILL.md`
- Re-sync the duplicated copies after editing a source: `python3 scripts/check_sync.py --fix`
- Install the commit-time hooks once per clone: `make hooks`

## Non-negotiable conventions

- **Eval-first**: write `skills/<name>/evals/evals.json` before the SKILL.md body.
- Frontmatter `description` is a **single line** (multi-line silently disables the
  skill), third person. Model-invoked skills add trigger phrasings and a "Not for …"
  exclusion; user-invoked ones (`disable-model-invocation: true`) are never routed,
  so they get one verb-first line and no trigger cases.
- `name` equals the folder name, kebab-case.
- SKILL.md bodies target 25–150 lines (< 500 is the hard ceiling); long material goes
  to `references/` (linked one level deep); deterministic steps go to `scripts/` with
  non-zero exit on failure.
- Files duplicated on purpose (the scaffold template, the `references/` rulebook
  copies) are listed in `scripts/check_sync.py`; edit the source, then `--fix`.
- Shipped Python is **stdlib-only** (skills run on other people's machines); ruff
  and pre-commit are dev tooling, pinned in `requirements-dev.txt`. A ruff finding
  is fixed at the line with a reason (`# noqa: S603` plus why), never by dropping
  the rule from `select` in `ruff.toml`.
- The validator scans skill content and bundled scripts for the patterns registry
  scanners flag (remote payloads, credential exfiltration, `shell=True`,
  instruction-override phrasing). Never suppress a security finding to get green —
  rewrite the instruction.
- **Changing anything under `skills/create-skill-repo/assets/template/` requires an
  entry in `skills/upgrade-repo/references/upgrade-log.md` in the same change** —
  with its Managed files and its Manual steps. Without one the improvement reaches
  newly scaffolded repos and silently skips every repo already generated.
- Every added/changed skill updates the README catalog table, `CHANGELOG.md`, and
  its `skills.sh.json` grouping.
- Publication to skills.sh happens ONLY via the bundled `/publish-repo` skill
  (slash-invoked, needs the owner's go-ahead) — never flip repo visibility ad hoc.
  Deployment model: docs/deploying.md.
- **Never run `git commit` or `git push`.** Leave every change in the working
  tree for the owner to review and commit. (The bash-guard hook additionally
  blocks `--no-verify` and force-pushes as a safety net; the server-side `main`
  ruleset is the real gate.)
- `.local/` is gitignored personal material (only its README is committed) — read
  ALL of it recursively, never commit its contents, never cite it as a committed
  path.

## Where things are

- Authoring rules: `docs/skill-authoring.md` · Eval methodology: `docs/evals.md`
- README shape (enforced by `make check`): `docs/readme-standard.md`
- `.local/` is the gitignored personal working area (research packs, drafts) —
  read it when present, never commit its contents.
- Hooks: `.claude/hooks/` (SKILL.md write-time validation, bash guard) — wired in
  `.claude/settings.json`; changes to them get PR-level scrutiny.
- The `add-skill` skill (`skills/add-skill/`) walks the authoring
  workflow — prefer it over ad-hoc skill writing. The `publish-repo` skill
  (`skills/publish-repo/`) walks skills.sh deployment. The `upgrade-repo` skill
  (`skills/upgrade-repo/`) carries template changes into repos already generated.
