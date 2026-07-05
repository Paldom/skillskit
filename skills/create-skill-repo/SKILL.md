---
name: create-skill-repo
description: Scaffolds a new standalone Agent Skills repository - created on GitHub via gh repo create (private, MIT), cloned locally, the bundled template overlaid and validated, .local/PROMPT.md seeded; the overlay stays uncommitted for owner review. Use when the user wants to create or scaffold a skill repo or collection ("create python-skills"). Not for adding skills to an existing repo.
license: MIT
argument-hint: <repo-name> [one-line idea]
---

# create-skill-repo

Stamps out a new skills repository: `gh repo create` provisions it on GitHub
(**private** by default, MIT license, technology `.gitignore`, README) and clones
it into the current directory; the **bundled template** (`assets/template/` inside
this skill) is then overlaid — OSS hygiene files, CI with a skills.sh consumer
job, validation hooks, in-repo `add-skill`/`publish-repo` dev skills,
plugin/marketplace manifests, `skills.sh.json`, and a gitignored `.local/PROMPT.md`
that drives the follow-up authoring session. The scaffold overlay is left **uncommitted** (GitHub's repo
creation makes only its own initial commit): the owner reviews, commits, pushes. Reference:
<https://cli.github.com/manual/gh_repo_create>. If invoked as
`/create-skill-repo <args>`, `$ARGUMENTS` is `<repo-name> [idea]`.

## When NOT to use

- Writing or fixing a skill inside an existing repo → `add-skill` (or that repo's
  bundled copy).
- Turning a research pack into skills → `skill-from-research` (it calls this
  skill when a new repo is actually needed).
- Improving the scaffold itself → edit `assets/template/` in a skillskit checkout
  (changes affect future repos only).

## Workflow

1. **Derive the four inputs** from the user's request; ask only if genuinely absent:
   - `name`: kebab-case repo name. Single skill → the skill's name
     (`icon-designer`); collection → a plural theme (`python-skills`).
   - `description`: one professional, benefit-led sentence with plain category
     keywords — it becomes the GitHub repo description, README intro, and plugin
     manifest. ≤ ~250 chars, no hype words.
   - `idea`: the user's high-level intent, 1–4 sentences, as literally as
     possible — it seeds `.local/PROMPT.md` for the in-repo authoring session.
   - `gitignore`: the GitHub `.gitignore` template matching the skills' dominant
     technology (`Python` default — the scaffold's own tooling is Python).
2. **Scaffold** (deterministic — always via the script, never hand-copy or raw `gh`):
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/scaffold.py" \
     <name> --description "<description>" --idea "<idea>" [--gitignore <Template>]
   ```
   Options: `--owner <github-owner>` (default: the authenticated `gh` user),
   `--public` (default private), `--topics extra1,extra2` (added to
   `agent-skills,claude-code,skills,skills-sh`), `--dest DIR` (default: cwd),
   `--local-only` (offline: folder + git init, no GitHub; requires `--owner`),
   `--keep-on-fail`. The script validates inputs (including that the seeded
   `.local/PROMPT.md` goal fits 4000 characters — shorten the idea if it fails),
   checks `gh` auth (needs the `workflow` scope), refuses names taken locally or
   on GitHub, validates the scaffold, and cleans up the local clone on failure.
   It NEVER runs git commit/push (the owner does) and never deletes remote
   repos — on failure it prints the exact cleanup command instead.
3. **Verify**: success ⇔ the script's final line is `SCAFFOLD OK: <path>` (exit 0).
   On failure, read its report, fix the cause (never by weakening the generated
   repo's `scripts/validate_skills.py`), and re-run.
4. **Hand off** — tell the user exactly:
   ```
   cd <name> && claude
   # then paste the contents of .local/PROMPT.md (starts with /goal)
   ```
   Mention: the repo shell is live (private) on GitHub but the scaffold is
   uncommitted — review, commit, push (exact commands are in the script output);
   `.local/` is gitignored — drop research packs/sources there before starting;
   publishing to skills.sh later runs via the repo's bundled `/publish-repo`.

## Output spec

New folder `<name>/` under the current directory: a clone of the freshly created
GitHub repo (private, MIT, tech `.gitignore` merged with the template's), overlay
left uncommitted for owner review, validator passing, repo topics set,
`.local/PROMPT.md` filled with the idea (≤4000 chars, enforced), no leftover
`{{PLACEHOLDER}}` tokens anywhere.

## Gotchas

- Requires an authenticated `gh` (`gh auth login`) with the `workflow` scope; the
  script prints the exact `gh auth refresh` command if missing.
- Names must match `^[a-z0-9]+(-[a-z0-9]+)*$` and must not contain
  "claude"/"anthropic" (reserved by the skills spec); free locally and on GitHub.
- `--gitignore` values are case-sensitive GitHub template names
  (`gh api gitignore/templates`); the script pre-checks them.
- The template ships its gitignore as `_gitignore` (a live one inside skill
  assets would be applied by the host repo's git); the script restores the real
  name during overlay — don't "fix" it in the assets.
- `.local/PROMPT.md` is personal and machine-local — no committed copy exists in
  generated repos.

## Files

- `scripts/scaffold.py` — the deterministic scaffolder (stdlib only).
- `assets/template/` — the complete repo scaffold that gets overlaid.
