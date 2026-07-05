---
name: publish-repo
description: Publishes the current Agent Skills repository to skills.sh - pre-flight checks, public visibility flip, protections (PVR, rulesets), a gh skill release, consumer-style install verification, telemetry seeding, and repo-page groupings. Use when the user asks to publish, deploy, release, go public, or get listed on skills.sh. Not for authoring skills or scaffolding repositories.
license: MIT
disable-model-invocation: true
argument-hint: [--dry-run]
---

# publish-repo

Deploys the current repository to the skills.sh ecosystem. There is no publish
API — deployment = a public, installable repo plus a first real install that
seeds the catalogue telemetry. This skill makes that sequence deliberate.
Slash-invoked only: it flips repository visibility, which is socially hard to
undo (everything ever pushed becomes visible).

## When NOT to use

- Writing or fixing a skill → `add-skill`.
- Scaffolding a new repo → `create-skill-repo`.
- The repo has zero skills under `skills/` → build first; never publish an
  empty catalogue.
- Routine pushes to an already-public repo → plain git (done by the owner).

## Workflow

1. **Pre-flight (hard gates — stop on any failure):** the working tree must be
   clean and pushed **by the owner** — this skill never runs `git commit` or
   `git push`; if there are uncommitted changes, stop and hand the list to the
   owner instead.
   ```bash
   git status --porcelain          # must be empty
   make check 2>/dev/null || python3 scripts/validate_skills.py   # repo validator, if present
   npx skills add . --list        # every skill under skills/ discovered
   gh skill publish --dry-run     # spec validation (gh >= 2.90; public preview)
   python3 -c "import json; json.load(open('skills.sh.json'))"    # if the file exists
   ```
   Triage every `gh skill` warning: add missing `license:` frontmatter; a
   `.claude/skills/` warning is expected when the repo deliberately bundles its
   own first-party dev skills. Verify README catalogue + CHANGELOG current and
   every skill description benefit-led (it is the listing copy); CI green.
2. **Manual blockers — require explicit user confirmation, never assume:**
   - full-history secret scan (gitleaks/trufflehog) done;
   - personal/private-file review done (everything ever committed goes public).
   With `--dry-run` in `$ARGUMENTS`, stop here and report readiness instead.
3. **Groupings:** ensure `skills.sh.json` lists every skill in exactly one group
   with an engaging one-sentence description per group — it is the repo's
   landing copy on skills.sh.
4. **Flip visibility** (confirm with the user immediately before):
   ```bash
   gh repo edit <owner>/<repo> --visibility public --accept-visibility-change-consequences
   ```
5. **Protections** (public repo unlocks them):
   ```bash
   gh api repos/<owner>/<repo>/private-vulnerability-reporting --method PUT
   ```
   Add a default-branch ruleset — solo-maintainer default: block force pushes
   and deletions only (require-PR would block the owner's direct-push workflow);
   upgrade to require-PR + code-owner review + required checks when outside
   contributors arrive. Add a **tag ruleset** on `v*` (block update + deletion)
   so releases are immutable.
6. **Release** — cut a versioned GitHub release matching
   `.claude-plugin/plugin.json` (or the repo's version source):
   ```bash
   gh skill publish --tag v<version>
   ```
   It re-validates, adds the `agent-skills` topic if missing, and creates the
   release with auto-generated notes. Add `skills-sh` too:
   `gh repo edit <owner>/<repo> --add-topic skills-sh`.
7. **Verify like a consumer, and seed the catalogue** (locally, NOT in CI —
   telemetry is disabled in CI and the first real install is what lists the repo):
   ```bash
   npx skills add <owner>/<repo> --list
   mkdir -p /tmp/skills-verify && cd /tmp/skills-verify
   npx skills add <owner>/<repo> --skill '*' -a claude-code -y
   npx skills list -a claude-code
   ```
8. **Polish:** README badge
   `[![skills.sh](https://skills.sh/b/<owner>/<repo>)](https://skills.sh/<owner>/<repo>)`;
   homepage via `gh repo edit --homepage` (e.g. the skills.sh page); social
   preview image (manual UI step — remind the owner).
9. **Report:** repo URL, skills.sh page URL, install command, release tag,
   protections applied, anything skipped with its unlock condition, and the note
   that the skills.sh page appears only after telemetry processes the seed
   install (pages are cached).

## Output spec

Public repo installable via `npx skills add <owner>/<repo>` (verified by an
actual install), PVR enabled, rulesets active, groupings valid, release cut,
seed install performed, owner told exactly what to expect next.

## Gotchas

- The visibility flip is the point of no return for history — step 2 demands
  explicit confirmation and never self-certifies.
- `npx skills add . --list` reporting "No skills found" means frontmatter or
  layout problems — fix via the repo validator's output, never by restructuring
  blindly.
- The leaderboard/repo page lags the seed install; absence minutes later is
  normal, not failure.
- No Node on the machine? The consumer verification and seed install must run
  somewhere with Node ≥18 — report it as pending, never as done.
