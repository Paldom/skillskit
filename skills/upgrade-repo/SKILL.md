---
name: upgrade-repo
description: Brings a repository scaffolded by an older skillskit up to the current template - refreshes the validator, eval runner, hooks, authoring docs and bundled dev skills, then reports the customized files to merge by hand. Use when the tooling in an existing skills repo is stale, was generated months ago, or is missing newer capabilities. Not for creating a repository, authoring a skill, or publishing.
license: MIT
argument-hint: [--apply]
---

# upgrade-repo

A scaffolded repo owns its files outright — its own validator, hooks, docs and
bundled dev skills — so nothing links it back to skillskit and no later
improvement reaches it. This walks that link on demand.

Read `references/upgrade-log.md` before reporting anything: it is the record of
what changed, and it carries the manual steps the script cannot perform.

## When NOT to use

- Creating a new skills repository → `create-skill-repo`.
- Authoring or fixing a skill in this repo → `add-skill`.
- Publishing to skills.sh → `publish-repo`.
- Upgrading application dependencies (npm, pip) — this only touches skillskit's
  own scaffold files.

## Workflow

1. **Report first, always.** Run the script in report mode; it never writes
   without `--apply`:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/upgrade_repo.py" --repo .
   ```
   It locates the template from the installed `create-skill-repo` skill. If it
   cannot, stop and give the user the two commands it prints — do not hand-copy
   files as a workaround, and do not guess at their content.
2. **Explain the drift.** The script splits its output in two: **MANAGED** files
   (no per-repo content, safe to overwrite) and **CUSTOMIZED** files (Makefile,
   CI, `AGENTS.md`, settings — merged by hand, never written). Map each differing
   file to its entry in `references/upgrade-log.md` and tell the user *why* each
   changed, not just that it did. Skip log entries whose files all already match.
3. **Confirm, then apply.** With the user's go-ahead:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/upgrade_repo.py" --repo . --apply
   ```
   This writes the MANAGED tier only. `skills/` — the repo's own product — is
   never touched, nor are README, CHANGELOG, `skills.sh.json` or the manifests.
4. **Do the manual steps.** Work the **Manual** list of each applicable log entry
   in order: wire new targets into the `Makefile` and CI, adopt convention changes
   in `AGENTS.md`. Edit these files rather than overwriting them — the repo's own
   jobs and rules must survive.
5. **Run the gate.** `make check` must exit 0. Expect genuine failures the first
   time a repo is scored by a check it never had: fix the **description** the
   failure points at, never the eval — the eval is the specification. If a gate
   cannot be satisfied, report it rather than loosening it.
6. **Record it.** Add a line to the repo's `CHANGELOG.md` naming the upgrade and
   the log entries adopted, so the next upgrade knows where this one stopped.

## Output spec (Definition of Done)

- Report shown and explained before any write
- MANAGED tier applied (or "already current" stated), `skills/` untouched
- Every applicable Manual step done, or explicitly listed as deferred with a reason
- `make check` green, or the failure reported with the description it points at
- Repo `CHANGELOG.md` records the upgrade

## Gotchas

- **Never edit a CUSTOMIZED file by overwriting it.** A repo's CI has jobs the
  template does not; the Makefile may have extra targets. Merge, don't replace.
- Files carrying `{{PLACEHOLDER}}` tokens (`docs/deploying.md`, `CONTRIBUTING.md`,
  `SECURITY.md`, `SUPPORT.md`, the plugin manifests) are substituted at scaffold
  time, so they are excluded from both tiers — a byte comparison would always
  differ. When one changes materially the log says so; re-read it from the
  template by hand.
- A failing gate after an upgrade is the upgrade working. The repo was never
  measured by that check before; a real defect surfacing is the point.
- Leave everything uncommitted for the owner to review, as everywhere else in
  this kit.

## Files

- `scripts/upgrade_repo.py` — tiered comparison against the current template;
  `--apply` writes the managed tier and nothing else.
- `references/upgrade-log.md` — what changed, when, and the manual follow-ups.
