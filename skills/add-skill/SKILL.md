---
name: add-skill
description: Authors or improves an Agent Skill in the current repo via the eval-first workflow - scope one purpose, write trigger evals, draft SKILL.md, validate, benchmark. Use when the user asks to create, add, write, refine, fix, or benchmark a skill ("add a skill for X", "improve triggering of Y"). Not for scaffolding a new repo (create-skill-repo) or distilling research packs (skill-from-research).
license: MIT
argument-hint: <skill-name or idea>
---

# add-skill

Builds one production-quality skill in `skills/<name>/`, eval-first, in whatever
repository you are currently in. Read `references/skill-authoring.md` and
`references/evals.md` once per session before starting — they are the rulebook
this workflow enforces (repos scaffolded by `create-skill-repo` also carry them
as `docs/`). If invoked as `/add-skill <args>`, treat `$ARGUMENTS` as the skill
name or idea to scope in step 1.

## When NOT to use

- Creating a new skills *repository* → `create-skill-repo`.
- Turning a research pack into one or more skills → `skill-from-research` (it
  drives this workflow per skill after distilling the pack).
- Infrastructure work (hooks, CI, validators) → plain editing, PR-level scrutiny.
- A "skill" that merely restates what the model already does well → don't build
  it; a skill must fix a specific observed failure.

## Workflow

1. **Scope.** State in one sentence what the skill does and the concrete failure
   it fixes. If the sentence needs "and", split into multiple skills, one at a
   time. Check the repo's existing skill catalog for overlap — near-neighbor
   descriptions steal each other's triggers; plan disjoint wording.
2. **Gather.** Read the repo's `.local/` recursively if present (research,
   examples, constraints — never cite `.local/` paths from a skill). Research
   beyond it: web-search for current facts, official docs, and prior art; verify
   anything load-bearing against primary sources. Verified facts the skill
   depends on go into `skills/<name>/references/` as cleaned, committed files.
3. **Evals first.** Create `skills/<name>/evals/evals.json` per
   `references/evals.md`: ≥8 `should_trigger` (vary formality, typos, terseness),
   ≥8 `should_not_trigger` (near-misses sharing keywords), 3–5 `quality` cases
   with plain-language `expected_behavior` assertions. If you can't write these,
   the scope is unclear — back to step 1.
4. **Draft SKILL.md.** Frontmatter: `name` == folder name; `description` on a
   **single line**, third person, `[what] + [use when …] + [not for …]`, 150–400
   chars, trigger keywords in the first ~120. Body per
   `references/skill-authoring.md`: purpose → when/when-not → numbered workflow →
   output spec → gotchas → pointers. Under 500 lines; deterministic steps as
   `scripts/` (non-zero exit on failure); long material as `references/` with a
   TOC. Reference bundled files via `${CLAUDE_SKILL_DIR}` so installed copies work.
5. **Validate.** If the repo has a validator (`make check` /
   `scripts/validate_skills.py`), it must exit 0 — fix every error, triage every
   warning. If it has none, self-check against the frontmatter rules in the
   authoring reference (single-line description, name==folder, length bounds).
6. **Trigger self-test.** For ≥3 should-trigger and ≥2 should-not-trigger
   prompts, reason explicitly: would the description alone route this prompt
   here against every other installed skill? Fix the description, not the evals.
7. **Measure.** Scan the available-skills list for Anthropic's official
   `skill-creator` (typically `skill-creator:skill-creator`; the plugin-qualified
   name varies by marketplace — match on name/description, don't hardcode). If
   present, invoke it as a subskill via the Skill tool, scoped to *measure only*:
   it runs each quality case as with-skill vs baseline subagents, grades
   assertions, and benchmarks pass rate / time / tokens. Hand it cases from
   `evals/evals.json` translated per "Automated harness" in
   `references/evals.md`, and follow that section's guardrails (workspace-only
   writes, cases-run check, description acceptance gate). If it's absent, run
   the manual protocol instead and say so — it certifies triggering only, not
   quality uplift; never let a skipped Measure pass silently as "measured".
8. **Register.** Update the repo's README catalog, `CHANGELOG.md`, and
   `skills.sh.json` grouping when those exist (schema shape: `"groupings":
   [{"title": ..., "description": ..., "skills": [...]}]` — not `groups`/`name`;
   skills.sh silently ignores a non-conforming file). Re-check sibling
   descriptions for new overlap.

## Output spec (Definition of Done)

- `skills/<name>/` with SKILL.md + evals/evals.json (+ scripts/references as needed)
- Repo validator green (or the self-check documented when no validator exists)
- Measured: official skill-creator benchmark when installed, else the manual
  protocol from `references/evals.md` — state which ran (the fallback certifies
  triggering only)
- Catalog/CHANGELOG/groupings updated where present
- A 3-line summary: purpose, trigger phrase examples, known limitations

## Gotchas

- Keep `description` on ONE physical line — multi-line values have failed to
  load in some runtimes; never work around a repo's validator.
- Don't paste failed eval prompts verbatim into the description (overfitting);
  generalize the missing verb/noun instead.
- Over-triggering fix = add targeted "Not for …" noun phrases from the actual
  false-positive overlap; don't delete positive triggers.
- Model upgrades shift routing — note that evals should be re-run after the next
  model release.

## Files

- `references/skill-authoring.md` — anatomy, frontmatter rules, description
  formula, body structure, gotchas, anti-patterns.
- `references/evals.md` — evals.json format and the trigger/quality protocol.
