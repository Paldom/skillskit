# Setup prompt — research pack to skills.sh-ready repo in one run

A paste-ready `/goal` prompt that orchestrates all four skillskit skills against
a target research pack: **scaffold → distill → refine → validate → publish
pre-flight**; all changes stay uncommitted for the owner's review.

Why this order: `create-skill-repo` runs first when no repo exists (everything
else writes into it); `skill-from-research` owns the pack-to-skills split;
`add-skill` refines individual skills afterwards (disjoint `skills/<name>/`
dirs, so refinements parallelize); `publish-repo` goes last and only as
`--dry-run` — real publication needs committed history and the owner's
explicit go-ahead.

## Prerequisites

```
/plugin marketplace add Paldom/skillskit
/plugin install skillskit@skillskit
```

(or `npx skills add Paldom/skillskit`, or `gh skill install Paldom/skillskit`).
You also need an authenticated `gh` CLI (`create-skill-repo` provisions via
`gh repo create`) and `python3` for the validator.

## The prompt

```
/goal Turn the research pack at <PACK_PATH> into a validated, skills.sh-ready Agent Skills repository using the skillskit skills — scaffold → distill → refine → validate → publish pre-flight — until every skill passes validation with its evals in place, and the change-set is left for my review. Never run git commit or git push — every change stays in the working tree for me. Name each skill explicitly when delegating to subagents (auto-triggering there is unreliable).

Prerequisites (verify first; stop and tell me if missing):
- The skillskit skills resolve in this session (try /add-skill); gh CLI authenticated; python3 available.

Method — ordering matters, respect it:
1. SCAFFOLD (only if no target repo exists): run /create-skill-repo <name> — it provisions a private GitHub repo via gh repo create, clones it, and overlays the bundled template (validator, hooks, CI, manifests); the overlay stays uncommitted. If a skills repo already exists, work from its root and skip this step.
2. DISTILL: run /skill-from-research <PACK_PATH> — inventory the pack, read it in full, verify claims against primary sources, split into single-purpose skills, author each eval-first (evals.json before the SKILL.md body).
3. REFINE (parallelizable): for each skill that fails validation or triggers weakly, run /add-skill <skill-name>. Skills live in disjoint skills/<name>/ dirs, so one subagent per skill is safe — name /add-skill explicitly in each subagent's instructions.
4. VALIDATE: run make check (or scripts/validate_skills.py per file); update the README catalog table, CHANGELOG.md, and skills.sh.json for every added skill. Loop back to step 3 until clean.
5. PUBLISH PRE-FLIGHT (never the real thing): run /publish-repo --dry-run and report its readiness gates. Actual publication (visibility flip, release) is mine — stop and hand me the checklist.
6. HANDOFF: never run git commit or git push. Present the skill list, validation results, and dry-run gate report; leave everything uncommitted for me.

Definition of Done:
- Every claim encoded in a skill traces to the pack or a primary source; each skill is single-purpose with evals.json present.
- make check exits 0; README table, CHANGELOG.md, and skills.sh.json cover every skill.
- /publish-repo --dry-run report produced; no publish action taken.
- All changes left uncommitted, with a summary for the owner's review.
```

## Notes

- Pack already distilled and you just want one skill? Run only `/add-skill`.
- `/publish-repo` is deliberately slash-only (`disable-model-invocation`); the
  dry-run is the ceiling for an autonomous run.
